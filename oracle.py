#!/usr/bin/env python3

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
import pandas as pd
from scipy.signal import find_peaks
import signal
# project
import zmq
from configuration_backtest import *
from collections import deque
from copy import deepcopy

# update single performace value in python file
def update_performance(performance,performance_name,path):
    path = path.replace('./strategies/','')
    with open(path.replace(ROOT_PATH*2,ROOT_PATH), "r") as file:
        contents = file.readlines()
        for i in range(len(contents)):
            if performance_name in contents[i]:
                contents[i] = f"{performance_name} = {performance}"

    with open(path.replace(ROOT_PATH*2,ROOT_PATH), "w") as file:
        file.writelines(contents)
    
    EXEC_IMPORT_STRING=f"""from {path.replace(ROOT_PATH,'').replace('/','.').replace('.py','').replace('.st','st')} import *"""
    #print("EXECUTION STRING: " + EXEC_IMPORT_STRING)
    exec(EXEC_IMPORT_STRING)


def format_binance_data(data):
    ds = data
    cols = ['asks','bids']
    for col in cols:
        for i in range(len(ds[col])):
            ds[col][i][0] = float(data[col][i][0])
            ds[col][i][1] = float(data[col][i][1])
    return ds


def from_string_to_list_of_lists(ask_or_bid):
    new_list = []
    # from string of list of lists to list of lists
    for element in ask_or_bid.split('['):
        raw_list = element.replace('[','').replace(']','')
        object_list = raw_list.split(',')
        if len(object_list)>=2:
            price = float(object_list[0])
            volume = float(object_list[1])
            new = np.array([volume,price])
            new_list.append(new)
    return new_list

def del_trade_orderbook(trade_orderbook:dict,trade_id:int):
    copy_ = trade_orderbook.copy()
    for trade_id_ , _ in copy_.items():
        if (trade_id == trade_id_ ):
            del trade_orderbook[trade_id]
    return trade_orderbook


def get_max_peak_price(peaks,prices):
    max_peak_price = 0
    max_peak_index = 0
    for i in peaks:
        if max_peak_price < prices[i]:
            max_peak_price = prices[i]
            max_peak_index = i
    return prices[max_peak_index]

if __name__ == '__main__':
    """
         POSITIONING algorithm
         trova il primo picco sopra
         trova il secondo picco sotto (e fammeli vedere)
         metti TP nel picco sopra (LONG), entry nel microprice a market
         e SL nel picco sotto - SL_BELOW_PRICE (eg. 5.0 su BTCUSDT)
         segnati Entry TP e SL come TRADING_OPERATION
         calcola il Rendimento/Rischio  =>long (TP-ENTRY/ENTRY-SL) 
         se R/R > 0.8 allora COMUNICA la operazione a visualizer e trader


        # ci sono picchi vicino al prezzo?
        #if asks_prices[peaks_asks[0]] - MID_PRICE  < 5.0 and MID_PRICE - bids_prices[peaks_bids[0]] < 5.0:
            
        # esiste un segnale per andare long o short?
        # ci sono troppe operazioni aperte?

    """
    starttime = datetime.now()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strategy_path", type=str, default='/strategies/s1.py', help="python stategy configuration file path for backtesting and optimization")
    args = parser.parse_args()
    STRATEGY_PATH = args.strategy_path
    STRATEGY_PATH = STRATEGY_PATH.replace('./strategies/','')


    EXEC_IMPORT_STRING=f"""from {STRATEGY_PATH.replace(ROOT_PATH,'').replace('.py','').replace('/','.').replace('.strategies','strategies').replace('.strategies.strategies','strategies')} import *"""

    try:
        exec(EXEC_IMPORT_STRING)
    except SyntaxError:
        print(f"SyntaxError string ERROR => {EXEC_IMPORT_STRING}")    

    except ImportError:
        print(f"ImportError string ERROR => {EXEC_IMPORT_STRING}")    



    MAX_CONCURRENT_OPEN_TRADES = math.floor(1/PERCENTAGE_PER_TRADE)

    GAIN_PERCENTAGE_24H = 0
    
    if PLOT_DATA:
        plt.ion()
        plt.figure(figsize=(12, 8), dpi=20, facecolor='w', edgecolor='k')
        plt.gca()
    
    # socket zmq client interface
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:5555')
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    
    # container orderbook datastructures
    my_buffer_ask = deque( maxlen = 50 )
    my_buffer_bid = deque( maxlen = 50 )

    TIME_COUNTER = 0
    counter_messages = 0
    print(f"minerva Oracle ID {STRATEGY_PATH.replace(ROOT_PATH+'/strategies/s','').replace('.py','')}")
    while True:
        #######################################################################
        ###################         NEW DATA                ###################
        #######################################################################
        
        message = socket.recv()
        counter_messages+=1

        if message == [b'kill']:
            exit()

        #print(message)
        buffer_object = message.decode().split('|')
        
        LOAD_DATA_SUCCESS = False

        try:    
            data_timestamp = buffer_object[0]
            # from string of list of lists to list of lists
            ask_array = from_string_to_list_of_lists(buffer_object[1])
            bid_array = from_string_to_list_of_lists(buffer_object[2])
            LOAD_DATA_SUCCESS = True
        except:
            LOAD_DATA_SUCCESS = False
            continue


        if LOAD_DATA_SUCCESS:
            # add list of lists to queue
            my_buffer_ask.append(ask_array) 
            my_buffer_bid.append(bid_array)
        
            asks_prices = deepcopy(np.hsplit(np.array(my_buffer_ask[-1]),2)[1].reshape(-1))
            asks_volumes =  deepcopy(np.hsplit(np.array(my_buffer_ask[-1]),2)[0].reshape(-1))
            bids_prices =  deepcopy(np.hsplit(np.array(my_buffer_bid[-1]),2)[1].reshape(-1))
            bids_volumes =  deepcopy(np.hsplit(np.array(my_buffer_bid[-1]),2)[0].reshape(-1))
            
            max_ask_absolute_volume = deepcopy(max(asks_volumes))
            max_bid_absolute_volume = deepcopy(max(bids_volumes))
            min_ask_price = deepcopy(min(asks_prices))
            max_bid_price = deepcopy(max(bids_prices))

            MID_PRICE = (min_ask_price + max_bid_price) / 2


            #######################################################################
            ###################         SIGNAL GENERATOR        ###################
            #######################################################################
            # Se una delle due e' molto piu grande delle altre allora fai front running
            # A = prendo asks_prices dal prezzo piu basso e prendo i primi X1 in ordine CRESCENTE
            # B = prendo bids_prices dal prezzo piu basso e prendo i primi X1 in ordine DE-CRESCENTE
            # ENTRY algorithm
            # se A > threshold e B > threshold
            # if A > THRESHOLD_VOLUME_BTCUSDT => short
            # if B > THRESHOLD_VOLUME_BTCUSDT  and  a/(a+b)   =>   long

            A = sum(asks_volumes[:50])*3+sum(asks_volumes[50:100])*2+sum(asks_volumes[100:150])

            B = sum(bids_volumes[:50])*3+sum(asks_volumes[50:100])*2+sum(asks_volumes[100:150])

            OPERATION_PARAMETER = round(  A / ( A + B ) ,3 )

            OPERATION_SIDE = ""

            if OPERATION_PARAMETER > THESHOLD_SHORT and SHORT_OPERATIONS:
                OPERATION_SIDE = "SHORT" 

            elif OPERATION_PARAMETER < THESHOLD_LONG and LONG_OPERATIONS:
                OPERATION_SIDE = "LONG" 
            
            else:
                OPERATION_SIDE = "WAIT"

            #######################################################################
            ###################           POSITIONING           ###################
            #######################################################################
            # prendo Ask e Bid con un filtro minimo di volumi THRESHOLD_BTCUSDT

            # take the first volume peak in the ask and in the bid arrays
            x_all = deepcopy(np.where(asks_prices == min_ask_price)[0]) # find the index of this in the list
            y_all = deepcopy(np.where(bids_prices == max_bid_price)[0])

            if x_all.any():
                x = deepcopy(np.where(asks_prices == min_ask_price)[0][0]) # find the index of this in the list
            
            if y_all.any():
                y = deepcopy(np.where(bids_prices == max_bid_price)[0][0])

            BEST_ASK_OFFER_PRICE = asks_prices[x_all] # lowest ask
            BEST_BID_OFFER_PRICE = bids_prices[y_all] # highest bid

            #MICRO_PRICE = (BEST_ASK_OFFER_VOLUME*max_bid_price + BEST_BID_OFFER_VOLUME*min_ask_price) / BEST_ASK_OFFER_VOLUME+BEST_BID_OFFER_VOLUME
            THRESHOLD_BTCUSDT = 0.2 # max(max_ask_absolute_volume, max_bid_absolute_volume) / RELATIVE_THRESHOLD_DIV
            
            # number of channels / int
            PEAK_DISTANCE = int(round(LIMIT_ORDER_BOOK / PEAK_DISTANCE_DIVISOR))

            peaks_asks, _1 = find_peaks(
                asks_volumes, height=0, threshold=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)
            peaks_bids, _2 = find_peaks(
                bids_volumes, height=0, threshold=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)

            # long or short
            REWARD_RISK_RATEO = 0
            if peaks_bids.any():
                #if MID_PRICE - bids_prices[peaks_bids[0]].size  < 20 :
                    if OPERATION_SIDE=="LONG":
                        TAKE_PROFIT = get_max_peak_price(peaks_asks,asks_prices) - TP_PRICE_BUFFER
                        STOP_LOSS = get_max_peak_price(peaks_bids,bids_prices) - SL_PRICE_BUFFER
                        ENTRY = BEST_ASK_OFFER_PRICE
                        REWARD_RISK_RATEO = (TAKE_PROFIT-ENTRY)/(ENTRY-STOP_LOSS)
            
        
            if peaks_asks.any():
                #if asks_prices[peaks_asks[0]] - MID_PRICE  < 5.0:
                    if OPERATION_SIDE=="SHORT":
                        TAKE_PROFIT = get_max_peak_price(peaks_bids,bids_prices) + TP_PRICE_BUFFER 
                        STOP_LOSS = get_max_peak_price(peaks_asks,asks_prices) + SL_PRICE_BUFFER
                        ENTRY = BEST_BID_OFFER_PRICE
                        REWARD_RISK_RATEO = (ENTRY-TAKE_PROFIT)/(STOP_LOSS-ENTRY)

            #######################################################################
            ###################         RISK MANAGER            ###################
            #######################################################################
            
            LONG_OPERATIONS,SHORT_OPERATIONS = 0, 0
            for k,v in TRADE_ORDERBOOK.items():
                if v['side']=='LONG':
                    LONG_OPERATIONS+=1
                if v['side']=='SHORT':
                    SHORT_OPERATIONS+=1

            AVAILABLE_CAPITAL = (SHORT_OPERATIONS + LONG_OPERATIONS) <= MAX_CONCURRENT_OPEN_TRADES

            if REWARD_RISK_RATEO > 0.2 and AVAILABLE_CAPITAL:

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

            #######################################################################
            ###################         MONITOR POSITIONS       ###################
            #######################################################################
            
            TIME_COUNTER += 1
            SECONDS_COUNTER = TIME_COUNTER * REQUEST_TIME_INTERVAL
            MINUTES_COUNTER = SECONDS_COUNTER/60
            HOURS_COUNTER = MINUTES_COUNTER/60
            DAYS_COUNTER = round(HOURS_COUNTER/24,5)

            UNREALIZED_PNL = 0
            if TRADE_ORDERBOOK:
                CLOSED_TRADE_ID = []
                for op in TRADE_ORDERBOOK.items():
                    
                    # EXTRACT DATA
                    ID_TRADE_ = op[0]
                    TRADING_OPERATION_ = op[1]
                    CLOSE_TRADE = False

                    # no more than 50%LONG 50% SHORT
                    OPERATION_SIDE_ = op[1]['side']
                    LONG_OPERATIONS,SHORT_OPERATIONS=0,0
                    if OPERATION_SIDE_ == "LONG":
                        LONG_OPERATIONS+=1
                    if OPERATION_SIDE_ == "SHORT":
                        SHORT_OPERATIONS+=1

                    # GET DATA FROM OPERATION
                    REWARD_RISK_RATEO = op[1]["reward_risk_rateo"]
                    LEVERAGE = int(op[1]['leverage'])
                    POSITION_SIZE = op[1]['usd_position']
                    N_TOKEN_CONTRACT = op[1]['n_token']
                    START_TIME = op[1]["start_time"]

                    # CALCULATE THE POSITION GAIN
                    if OPERATION_SIDE_ == "LONG":
                        GAIN = (BEST_BID_OFFER_PRICE - op[1]['entry_prices'][0]) * N_TOKEN_CONTRACT  
                    if OPERATION_SIDE_ == "SHORT":
                        GAIN = (op[1]['entry_prices'][0] - BEST_ASK_OFFER_PRICE ) * N_TOKEN_CONTRACT 

                    # CALCULATE THE FEES
                    GAIN = GAIN - GAIN * TAKER_FEES

                    UNREALIZED_PNL += GAIN

                    # CLOSE THE POSITION IF TOO MUCH TIME HAS BEEN PASSED
                    if datetime.now() > START_TIME + timedelta(seconds = MAX_SECONDS_TRADE_OPEN ):
                        CLOSE_TRADE = True
                        
                    # TAKE PROFIT
                    if OPERATION_SIDE_ == "LONG":
                        if MID_PRICE >= TRADING_OPERATION_['take_profits'][0]:
                            CLOSE_TRADE=True

                        if MID_PRICE <= TRADING_OPERATION_['stop_losses'][0]:
                            CLOSE_TRADE=True
                            
                    # STOP LOSS
                    if OPERATION_SIDE_ == "SHORT":
                        if MID_PRICE <= TRADING_OPERATION_['take_profits'][0]:
                            CLOSE_TRADE=True

                        if MID_PRICE >= TRADING_OPERATION_['stop_losses'][0]:
                            CLOSE_TRADE=True
                    
                    # CLOSE THE TRADE
                    if CLOSE_TRADE:
                        if OPERATION_SIDE_ == "SHORT":
                            GAIN = (op[1]['entry_prices'][0] - MID_PRICE) * N_TOKEN_CONTRACT
                        
                        if OPERATION_SIDE_ == "LONG":
                            GAIN = (MID_PRICE - op[1]['entry_prices'][0]) * N_TOKEN_CONTRACT

                        GAIN = GAIN - GAIN*TAKER_FEES
                        EQUITY += GAIN

                        GAIN_PERCENTAGE_24H = ((EQUITY-INITIAL_CAPITAL)/INITIAL_CAPITAL * 100 ) / DAYS_COUNTER
                        
                        PERFORMANCE = GAIN_PERCENTAGE_24H

                        update_performance(PERFORMANCE,"fitness",ROOT_PATH+STRATEGY_PATH)

                        CLOSED_TRADE_ID.append(ID_TRADE_)

                # DELETE ALL THE CLOSED TRADE FROM THE TRADE ORDERBOOK
                for id_ in CLOSED_TRADE_ID:
                    TRADE_ORDERBOOK = del_trade_orderbook(TRADE_ORDERBOOK, id_)

            # APPLY RUNNING TIME UPDATE TO EACH TRADE
            for op in TRADE_ORDERBOOK.items():
                ID_TRADE_ = op[0]
                TRADING_OPERATION_ = op[1]
                START_TIME = TRADING_OPERATION_['start_time']
                TRADING_OPERATION_['running_time'] =  datetime.now() - START_TIME                     
                TRADE_ORDERBOOK[ID_TRADE_] = TRADING_OPERATION_ 

            endtime = datetime.now()
            EXECUTION_TIME = endtime - starttime
            #######################################################################
            ###################     END OF THE ALGORITHM        ###################
            #######################################################################

            



            #######################################################################
            ###################         PLOT DATA               ###################
            #######################################################################
            if PLOT_DATA:
                # peaks
                plt.scatter(asks_volumes[peaks_asks],
                            asks_prices[peaks_asks], marker="*", color='blue',s=1500)
                plt.scatter(bids_volumes[peaks_bids],
                            bids_prices[peaks_bids], marker="*", color='red',s=1500)

                #plt.ylim([0.999*min(asks_prices),max(bids_prices)*1.0001])
                #plt.xlim([0,max(max(asks_volumes),max(bids_volumes))*1.05])

                # ask and bid bars https://www.youtube.com/watch?v=s4vTksDeG9c
                plt.barh(asks_prices, asks_volumes, alpha=0.55, height=0.18, color='orangered')
                
                plt.barh(bids_prices,bids_volumes, alpha=0.55, height=0.18, color='yellowgreen')

                # threshold filter
                plt.axvline(x=THRESHOLD_BTCUSDT, color='teal',
                            label='operative filter threshold', linestyle='--', alpha=0.9)

                plt.axhline(y=MID_PRICE, color='indigo', linestyle='--', alpha=0.6)
                plt.axhline(y=min_ask_price, color='red', linestyle='--', alpha=0.6)
                plt.axhline(y=max_bid_price, color='green', linestyle='--', alpha=0.6)
                
                if TRADE_ORDERBOOK:
                    for k,v in TRADE_ORDERBOOK.items():
                        TRADING_OPERATION_ = v
                        TAKE_PROFIT = TRADING_OPERATION_['take_profits'][0]
                        ENTRY = TRADING_OPERATION_['entry_prices'][0]
                        STOP_LOSS = TRADING_OPERATION_['stop_losses'][0]
                        plt.axhline(y = TAKE_PROFIT, color='forestgreen', linestyle='dashdot', alpha=0.9)
                        plt.axhline(y = ENTRY, color='black', linestyle='dashdot', alpha=0.9)
                        plt.axhline(y = STOP_LOSS, color='maroon', linestyle='dashdot', alpha=0.9)

                plt.draw()
                plt.pause(0.1)
                plt.clf()


            #######################################################################
            ###################         PRINT DATA              ###################
            #######################################################################

            if PRINT_ANY_DATA:
                os.system('clear')
                print(f'minerva {STRATEGY_PATH} [ONLINE]')
                print(f' #Trades        {TRADE_ID}')
                print(f' gain24h %      {GAIN_PERCENTAGE_24H}')
                print(f' Actual equity  {EQUITY}')
                print(f' Initial equity {INITIAL_CAPITAL}')
                print(f'market          {MARKET}')
                
                if BACKTEST_MODE:
                    print(f'execution time in days:    {DAYS_COUNTER}')
                    print(f'data {counter_messages}')
                else:
                    MINUTES = EXECUTION_TIME.seconds/60
                    HOURS = MINUTES/60
                    DAYS = round(HOURS/24,5)
                    print(f'execution time in seconds: {EXECUTION_TIME.seconds}')
                    print(f'execution time in days:    {DAYS}')

                if PRINT_BASIC_DATA:
                    if DAYS: print(f'gain 1day % {round(((EQUITY-INITIAL_CAPITAL)/INITIAL_CAPITAL*100)/DAYS,5) }')

                    print(f'MID_PRICE       {MID_PRICE}')
                    print(f'min_ask_price   {min_ask_price}')
                    print(f'max_bid_price   {max_bid_price}')
                    print(f'OPERATION_PARAMETER {OPERATION_PARAMETER}')
                    print(f'ASK peaks       {peaks_asks}')
                    print(f'BID peaks       {peaks_bids}')

                    print(f'\nTRADE ORDERBOOK')
                    pprint(TRADE_ORDERBOOK)

                if PRINT_ALGORITHM:
                    print(f'\nDATASTRUCTURES')
                    print(f'\nTypes')
                    print(f'asks_volumes         {type(asks_volumes)}') 
                    print(f'bids_volumes         {type(bids_volumes)}')
                    print(f'asks_prices          {type(asks_prices)}') 
                    print(f'bids_prices          {type(bids_prices)}')
                    print(f'ask_array            {type(ask_array)}') 
                    print(f'bid_array            {type(bid_array)}')
                    print(f'peaks_asks           {type(peaks_asks)}') 
                    print(f'peaks_bids           {type(peaks_bids)}')
                    print(f'my_buffer_ask        {type(my_buffer_ask)}') 
                    print(f'my_buffer_bid        {type(my_buffer_bid)}')

                    print(f'\nLength')
                    print(f'asks_volumes         {len(asks_volumes)}') 
                    print(f'bids_volumes         {len(bids_volumes)}')
                    print(f'asks_prices          {len(asks_prices)}') 
                    print(f'bids_prices          {len(bids_prices)}')
                    print(f'ask_array            {len(ask_array)}') 
                    print(f'bid_array            {len(bid_array)}')
                    print(f'peaks_asks           {len(peaks_asks)}') 
                    print(f'peaks_bids           {len(peaks_bids)}')
                    print(f'my_buffer_ask        {len(my_buffer_ask)}') 
                    print(f'my_buffer_bid        {len(my_buffer_bid)}')

                    print(f'\nExamples')
                    print(f'asks_volumes         {asks_volumes[0]}') 
                    print(f'bids_volumes         {bids_volumes[0]}')
                    print(f'asks_prices          {asks_prices[0]}') 
                    print(f'bids_prices          {bids_prices[0]}')
                    print(f'ask_array            {ask_array[0]}') 
                    print(f'bid_array            {bid_array[0]}')
                    print(f'my_buffer_ask        {my_buffer_ask[-1][-1]}') 
                    print(f'my_buffer_bid        {my_buffer_bid[-1][-1]}')

    plt.show(block=True)