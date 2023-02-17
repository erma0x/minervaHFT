import ast
import zmq
import time
from configuration_backtest import DATASTREAMER_URL

# python3 built-in libs
import time
import os
import argparse
import math
from datetime import datetime, timedelta
from pprint import pprint
# 3rd party libs
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from binance import Client
# project
from utils import mytimer
from configuration_backtest import TRADING_OPERATION, REQUEST_TIME_INTERVAL

if __name__ == '__main__':

    start = datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("-mk","--market",type=str, default="BTCUSDT", help="choose market where to get data from")
    parser.add_argument("-plt","--plot_data",type=int, default=None, help="stream orderbook data and trading data with matplotlib")
    parser.add_argument("-cap", "--capital",type=int, default=5000,help="initial capital in usd")
    parser.add_argument("-lo", "--limit_orderbook",type=int, default=500,help="limit request of the orderbook from binance")
    parser.add_argument("-rt", "--relative_THRESHOLD",type=int, default=10,help="relative operative trading THRESHOLD refered to : max_local_volume/relative_THRESHOLD ")
    parser.add_argument("-sp", "--short_pressure",type=float, default=0.8,help="A/(A+B) > short_pressure => SHORT")
    parser.add_argument("-lp", "--long_pressure",type=float, default=0.2,help="A/(A+B) < long_pressure => LONG")
    parser.add_argument("-maxt", "--max_councurrent_trades",type=int, default=3,help="max open trades at the same time")
    parser.add_argument("-pkd", "--peak_distance_divisor",type=int, default=10,help="peak_distance = limit_orderbook/peak_distance_divisor")
    parser.add_argument("-slbf", "--stop_loss_price_buffer",type=float, default=0.01,help="add absolute price buffer for the stop loss, is the distance in price from the sl peak")
    parser.add_argument("-tpbf", "--take_profit_price_buffer",type=float, default=0.01,help="add absolute price buffer for the take profit, is the distance in price from the tp peak")
    parser.add_argument("-pt", "--percentage_per_trade",type=float, default=0.03,help="percentage of equity for each trade opened")
    parser.add_argument("-abwind", "--ask_bid_window",type=int, default=10,help="number of ask-bid price channels to be considered in the strategy")
    parser.add_argument("-msto", "--max_seconds_trade_open",type=int, default=60,help="number of seconds")

    args = parser.parse_args()
    
    
    PLOT_DATA = args.plot_data
    INITIAL_CAPITAL =  args.capital
    LIMIT_ORDER_BOOK =  args.limit_orderbook
    RELATIVE_THRESHOLD_DIV =  args.relative_THRESHOLD # int (2,100)

    THRESHOLD_SHORT = args.short_pressure
    THRESHOLD_LONG = args.long_pressure
    MAX_CONCURRENT_OPEN_TRADES = args.max_councurrent_trades
    MAX_SECONDS_TRADE_OPEN = args.max_seconds_trade_open
    PEAK_DISTANCE_DIVISOR = args.peak_distance_divisor
    SL_PRICE_BUFFER = args.stop_loss_price_buffer
    TP_PRICE_BUFFER = args.take_profit_price_buffer
    MARKET = args.market
    PERCENTAGE_PER_TRADE = args.percentage_per_trade
    AB_LEN = args.ask_bid_window # numero di canali prima e dopo A (e B)
    LEVERAGE = 10
    # PERPETUAL CONTRACT KUCOINFUTURES FEE STRUCTURE
    TAKER_FEES = 0.0006 # (0,1) % 
    MAKER_FEES = 0.0002 # (0,1) %

    # Trading algorithm 
    # TIMING without visualizer 0.8 / 1.6 seconds
    # TIMING with    visualizer 2.3 / 3.0 seconds
    EQUITY = INITIAL_CAPITAL
    TRADING_OPERATION = {}
    EQUITY_ARRAY = []
    TRADE_ORDERBOOK = {}
    TRADE_ID = 0
    UNREALIZED_PNL = 0
    REALIZED_PNL = 0


    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect(DATASTREAMER_URL)
    sock.subscribe("") # Subscribe to all topics


    # if PLOT_DATA:
    #     #plt.style.use('dark_background')
    #     plt.ion()
    #     plt.figure(figsize=(12, 8), dpi=20, facecolor='w', edgecolor='k')
    #     plt.gca()

    print('STARTING...')
    while True:
    
        my_timer = mytimer.Timer()
        my_timer.start()

        TRADING_OPERATION = {}
        LONG_OPERATIONS,SHORT_OPERATIONS = 0, 0

        raw_data = sock.recv_string() # ZMQ
        #raw_orderbook = raw_data.split('@')[1]
        #print(raw_data.split('@')[1])
        #result = ast.literal_eval(raw_data.encode())
        raw_orderbook = raw_data.split('@')[1][2:]
        
        orderbook = ast.literal_eval(raw_orderbook)
        print(type(orderbook))

        #pprint(raw_orderbook)
        #orderbook = get_orderbook_depth(ticker=MARKET, limit_=LIMIT_ORDER_BOOK)
        #orderbook = ast.literal_eval(raw_orderbook)
        #result = ast.literal_eval(raw_orderbook)
        #print(orderbook)
        #print(orderbook['asks'])
        #orderbook =  #
        asks_prices = np.array(orderbook['asks'])[:, 0]
        asks_volumes = np.array(orderbook['asks'])[:, 1]
        bids_prices = np.array(orderbook['bids'])[:, 0]
        bids_volumes = np.array(orderbook['bids'])[:, 1]
    
        MID_PRICE = (min(asks_prices) + max(bids_prices) ) / 2

        # prendo Ask e Bid con un filtro
        # Se una delle due e' molto piu grande delle altre allora fai front running
        # prendo asks_prices dal prezzo piu basso e prendo i primi X1 in ordine CRESCENTE
        A = sum(asks_volumes[:AB_LEN])
        # prendo bids_prices dal prezzo piu basso e prendo i primi X1 in ordine DE-CRESCENTE
        B = sum(bids_volumes[:AB_LEN])

        # ENTRY algorithm
        # se A > THRESHOLD e B > THRESHOLD
        #if A > THRESHOLD_VOLUME_BTCUSDT => short
        #if B > THRESHOLD_VOLUME_BTCUSDT  and  a/(a+b)   =>   long

        OPERATION_PARAMETER = A / ( A + B )

        OPERATION_SIDE = ""
        MAX_LONG_POSITIONS = LONG_OPERATIONS <= math.floor(MAX_CONCURRENT_OPEN_TRADES/2)
        MAX_SHORT_POSITIONS = SHORT_OPERATIONS <= math.floor(MAX_CONCURRENT_OPEN_TRADES/2)

        if OPERATION_PARAMETER > THRESHOLD_SHORT and MAX_SHORT_POSITIONS:
            OPERATION_SIDE = "SHORT" 

        elif OPERATION_PARAMETER < THRESHOLD_LONG and MAX_LONG_POSITIONS:
            OPERATION_SIDE = "LONG" 
        
        else:
            OPERATION_SIDE = "STOP"

        # POSITIONING algorithm
        # trova il primo picco sopra
        # trova il secondo picco sotto (e fammeli vedere)
        # metti TP nel picco sopra (LONG), entry nel microprice a market
        # e SL nel picco sotto - SL_BELOW_PRICE (eg. 5.0 su BTCUSDT)
        # segnati Entry TP e SL come TRADING_OPERATION
        # calcola il Rendimento/Rischio  =>long (TP-ENTRY/ENTRY-SL) 
        # se R/R > 0.8 allora COMUNICA la operazione a visualizer e trader

        max_ask_absolute_volume = max(asks_volumes)
        max_bid_absolute_volume = max(bids_volumes)
        min_ask_price = min(asks_prices)
        max_bid_price = min(asks_prices)
        
        x = np.where(asks_prices == min_ask_price)[0] # find the index of this in the list
        y = np.where(asks_prices == max_bid_price)[0] 
        
        BEST_ASK_OFFER_VOLUME = bids_prices[x]  # lowest ask
        BEST_BID_OFFER_VOLUME = bids_volumes[y] # highest bid

        MICRO_PRICE = (BEST_ASK_OFFER_VOLUME*max_bid_price + BEST_BID_OFFER_VOLUME*min_ask_price) / BEST_ASK_OFFER_VOLUME+BEST_BID_OFFER_VOLUME
        MICRO_PRICE = MICRO_PRICE[0]

        THRESHOLD_BTCUSDT = max(max_ask_absolute_volume, max_bid_absolute_volume) / RELATIVE_THRESHOLD_DIV
        
        # number of channels / int
        PEAK_DISTANCE = int(round(LIMIT_ORDER_BOOK / PEAK_DISTANCE_DIVISOR))

        peaks_asks, _1 = find_peaks(
            asks_volumes, height=0, THRESHOLD=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)
        peaks_bids, _2 = find_peaks(
            bids_volumes, height=0, THRESHOLD=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)

        # ci sono picchi vicino al prezzo?
        #if asks_prices[peaks_asks[0]] - MID_PRICE  < 5.0 and MID_PRICE - bids_prices[peaks_bids[0]] < 5.0:
            
        # esiste un segnale per andare long o short?
        # ci sono troppe operazioni aperte?

        # long or short
        REWARD_RISK_RATEO = 0
        if peaks_bids.any():
            if len(TRADE_ORDERBOOK) < MAX_CONCURRENT_OPEN_TRADES and MID_PRICE - bids_prices[peaks_bids[0]]  < 20 :
                if OPERATION_SIDE=="LONG":
                    TAKE_PROFIT = asks_prices[peaks_asks[0]] - TP_PRICE_BUFFER
                    STOP_LOSS = bids_prices[peaks_asks[0]] + SL_PRICE_BUFFER
                    ENTRY = MID_PRICE
                    REWARD_RISK_RATEO = (TAKE_PROFIT-ENTRY)/(ENTRY-STOP_LOSS)
        
        if peaks_asks.any():
            if len(TRADE_ORDERBOOK) < MAX_CONCURRENT_OPEN_TRADES and asks_prices[peaks_asks[0]] - MID_PRICE  < 5.0:
                if OPERATION_SIDE=="SHORT":
                    TAKE_PROFIT = bids_prices[peaks_asks[0]] + TP_PRICE_BUFFER
                    STOP_LOSS = asks_prices[peaks_asks[0]] - SL_PRICE_BUFFER
                    ENTRY = MID_PRICE
                    REWARD_RISK_RATEO = (ENTRY-TAKE_PROFIT)/(STOP_LOSS-ENTRY)

        # risk maneagement part and FINAL part
        if REWARD_RISK_RATEO > 3.0:

            POSITION_SIZE = EQUITY * PERCENTAGE_PER_TRADE * LEVERAGE
            N_TOKEN_CONTRACT = POSITION_SIZE / MID_PRICE 
            TRADING_OPERATION = {"side": OPERATION_SIDE,
                                "symbol": MARKET,  
                                "take_profits": [TAKE_PROFIT],
                                "entry_prices": [ENTRY],  
                                "stop_losses": [STOP_LOSS],
                                "leverage": str(LEVERAGE),
                                "n_token":N_TOKEN_CONTRACT,
                                "usd_position":POSITION_SIZE,
                                "reward_risk_rateo":REWARD_RISK_RATEO,
                                "start_time":datetime.now(),
                                "running_time":0}
                                    
            TRADE_ID += 1
            TRADE_ORDERBOOK[TRADE_ID] = TRADING_OPERATION # RUN TRADE 



        my_timer.stop()

        EXECUTION_TIME = datetime.now() - start

        # Print in the Shell
        os.system('clear')
        #DAY1 = EXECUTION_TIME.seconds/(60*60*24)
        MINUTES = EXECUTION_TIME.seconds/60
        HOURS = MINUTES/60
        DAYS = HOURS/24
        print(f'passed days     {DAYS}')
        #print(f'theoretical gain % {((EQUITY-INITIAL_CAPITAL)/INITIAL_CAPITAL*100)/DAYS }')
        if DAYS:
            print(f'theoretical gain 1day % {((EQUITY-INITIAL_CAPITAL)/INITIAL_CAPITAL*100)/DAYS }')
        print(f'market          {MARKET}')
        print(f'running time    {EXECUTION_TIME.seconds} seconds')
        print(f'mid-price       {MID_PRICE}')
        print(f'micro-price     {MICRO_PRICE}')
        print(f'ASK pressure    {round(A/(A+B),2)*100} %')
        print(f'execution time  {round(my_timer.elapsed,2)}',)

        #print(f'win-rate')

        peak_prices_ask = [asks_prices[peaks_asks[i]] for i in range(len(peaks_asks))]
        peak_prices_bid = [bids_prices[peaks_bids[i]] for i in range(len(peaks_bids))]

        print(f'ASK peaks       {peak_prices_ask}')
        print(f'BID peaks       {peak_prices_bid}')
        
        #if peaks_asks.any():
        #    print(asks_prices[peaks_asks[0]]-MID_PRICE)
        #print(peaks_asks)
           # [peaks_asks[0]] - MID_PRICE)

        if TRADE_ORDERBOOK:
            pprint(TRADE_ORDERBOOK)
        
        if my_timer.elapsed < REQUEST_TIME_INTERVAL:
            time.sleep( REQUEST_TIME_INTERVAL + 0.01 - my_timer.elapsed )
                                                                 
        if EQUITY < INITIAL_CAPITAL*0.7: # max drowdown! # implement here
            break

    # plt.show(block=True)

    sock.close()
    ctx.term()