#!/usr/bin/env python3

# python3 built-in libs
import os
import argparse
import math
from datetime import datetime, timedelta
from pprint import pprint
# 3rd party libs
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
# project
import zmq
from collections import deque
import gc
gc.enable()
gc.set_threshold(1000,1000,1000)
import numpy as np
import ast
import pickle
import os,sys
from binance.spot import Spot
import binance
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minervaHFT/minerva/','minervaHFT/'))
from configuration_trading import TICKER, BASE_CURRENCY, ETH_ROUND_NUMBER, MARKET, TRADING
from configuration_backtest import *
from trader import check_balance, trader_spot, get_keys

def store_perfomances(data,filename):
    filename = filename.replace('.py','.pickle').replace(' ','').replace("'\n",'')
    dbfile = open(filename, 'wb')
    pickle.dump(data, dbfile)                     
    dbfile.close()

def update_performance(performance, performance_name, path):
    'update single performace value in python file'
    with open(path, 'r') as f:
        contents = f.readlines()

    with open(path,"w",encoding='utf-8') as file:
        for i in range(0,len(contents),-1):
            if performance_name in contents[i]:
                contents[i] = f"{performance_name} = {performance}"

def format_binance_data(data):
    ds = data
    for col in ['asks', 'bids']:
        for i in range(len(ds[col])):
            ds[col][i][0] = float(data[col][i][0])
            ds[col][i][1] = float(data[col][i][1])
    return ds

def np_array(input_str):
    input_list = ast.literal_eval(input_str)
    output_array = np.array(input_list, dtype = float) # Convert list of lists to 2D np.array
    delete_indices = np.where(output_array[:, 1] == '0.00000000')[0]
    filtered_data = np.delete(output_array, delete_indices, axis=0) # Delete rows
    return filtered_data

def from_string_to_list_of_lists(ask_or_bid):
    # from string of list of lists to list of lists
    new_list = []
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


starttime = datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--strategy_path", type=str, default='./strategies/s0.py', help="python stategy configuration file path for backtesting and optimization")
args = parser.parse_args()

STRATEGY_PATH = args.strategy_path
#STRATEGY_PATH = STRATEGY_PATH.replace('./strategies/','strategies.') # IF ORACLE

api_key, private_key = get_keys('lorenzo')
client = Spot( api_key = api_key , private_key = private_key)

EXEC_IMPORT_MODULE = STRATEGY_PATH.replace(ROOT_PATH,'').replace('.py','').replace('/','.').replace('..','')

EXEC_IMPORT_STRING=f"""from {EXEC_IMPORT_MODULE} import *"""
exec(EXEC_IMPORT_STRING)
MAX_CONCURRENT_OPEN_TRADES = math.floor(1/PERCENTAGE_PER_TRADE)
GAIN_PERCENTAGE_24H = 0


# if PLOT_DATA:
#     plt.ion()
#     plt.figure(figsize=(12, 8), dpi=20, facecolor='w', edgecolor='k')
#     plt.gca()


context = zmq.Context()
server_socket = context.socket(zmq.PULL)
server_socket.bind("tcp://*:5570")

# container orderbook datastructures
my_buffer_ask = deque( maxlen = 10 )
my_buffer_bid = deque( maxlen = 10 )

TIME_COUNTER = 0
counter_messages = 0

print(f"Starting ... minerva/oracle.py {STRATEGY_PATH} ")

while True:
    message = server_socket.recv_string()
    counter_messages+=1
        
    # FITNESS_DATA = {'fitness':9,'#trades':ID_TRADE_,'gain_24_h':GAIN_PERCENTAGE_24H,'msg':counter_messages}
    # store_perfomances(data = FITNESS_DATA, filename = STRATEGY_PATH)
    
    buffer_object = message.split('|')
    data_timestamp = buffer_object[0]

    bid_array, ask_array = np.empty((2,2)), np.empty((2,2))
    ask_array = np.loadtxt(buffer_object[1])
    bid_array =  np.loadtxt(buffer_object[2])


    if bid_array.any() and ask_array.any():
        # add list of lists to queue
        my_buffer_ask.append(ask_array) 
        my_buffer_bid.append(bid_array)
    
        asks_prices = ask_array[:, 0]
        asks_volumes =  ask_array[:, 1]
        bids_prices =  bid_array[:, 0]
        bids_volumes =  bid_array[:, 1]        

        max_ask_absolute_volume = max(asks_volumes)
        max_bid_absolute_volume = max(bids_volumes)
        min_ask_price = min(asks_prices)
        max_bid_price = max(bids_prices)

        MID_PRICE = (min_ask_price + max_bid_price) / 2

        A = sum(asks_volumes[:W_I]) * K1 +sum(asks_volumes[W_I:W_I*2]) * K2 + sum(asks_volumes[W_I*2:W_I*3] * K3 )

        B = sum(bids_volumes[:W_I]) * K1 +sum(asks_volumes[W_I:W_I*2]) * K2 + sum(asks_volumes[W_I*2:W_I*3] * K3 )

        OPERATION_PARAMETER = round(  A / ( A + B ) ,3 ) # SIGNAL
        OPERATION_SIDE = ""
        if OPERATION_PARAMETER < THRESHOLD_LONG and ALLOW_LONG_OPERATIONS == True:
            OPERATION_SIDE = "LONG" 

    # find the index of this in the list
        x_all = np.where(asks_prices == min_ask_price)[0] 
        y_all = np.where(bids_prices == max_bid_price)[0]

        #if x_all.any():
        #    x = deepcopy(np.where(asks_prices == min_ask_price)[0][0]) # find the index of this in the list
        
        #if y_all.any():
        #    y = deepcopy(np.where(bids_prices == max_bid_price)[0][0])

        BEST_ASK_OFFER_PRICE = asks_prices[x_all] # lowest ask
        BEST_BID_OFFER_PRICE = bids_prices[y_all] # highest bid

        #MICRO_PRICE = (BEST_ASK_OFFER_VOLUME*max_bid_price + BEST_BID_OFFER_VOLUME*min_ask_price) / BEST_ASK_OFFER_VOLUME+BEST_BID_OFFER_VOLUME
        THRESHOLD_TICKER = max(max_ask_absolute_volume, max_bid_absolute_volume) / RELATIVE_THRESHOLD_DIV
        
        # number of channels / int
        PEAK_DISTANCE = int(round(LIMIT_ORDER_BOOK / PEAK_DISTANCE_DIVISOR))

        peaks_asks, _1 = find_peaks(
            asks_volumes, height=0, threshold= THRESHOLD_TICKER, distance=PEAK_DISTANCE)
        peaks_bids, _2 = find_peaks(
            bids_volumes, height=0,  threshold=THRESHOLD_TICKER, distance=PEAK_DISTANCE)

        REWARD_RISK_RATEO = 0
        if peaks_bids.any() and OPERATION_SIDE=="LONG":
            TAKE_PROFIT = get_max_peak_price(peaks_asks,asks_prices) - TP_PRICE_BUFFER
            STOP_LOSS = get_max_peak_price(peaks_bids,bids_prices) - SL_PRICE_BUFFER
            ENTRY = BEST_ASK_OFFER_PRICE
            REWARD_RISK_RATEO = (TAKE_PROFIT-ENTRY)/(ENTRY-STOP_LOSS)
            
            if REWARD_RISK_RATEO > 0.2:

                POSITION_SIZE = EQUITY * 0.3
                N_TOKEN_CONTRACT = 0.02  
                
                if TRADING == True:
                    params = {
                        'symbol': MARKET,
                        'side': 'BUY',
                        'type': 'LIMIT',
                        'timeInForce': 'GTC',
                        'quantity': N_TOKEN_CONTRACT ,
                        'price': ENTRY ,
                        'newClientOrderId':TRADE_ID,
                    }
                    print(params)
                    #response = client.new_order(**params)
                
                TRADING_OPERATION = {
                                    "side": OPERATION_SIDE,
                                    "symbol": MARKET,  
                                    "take_profits": [TAKE_PROFIT],
                                    "entry_prices": [ENTRY],  
                                    "stop_losses": [STOP_LOSS],
                                    "leverage" : str(LEVERAGE),
                                    "n_token" : N_TOKEN_CONTRACT,
                                    "usd_position":POSITION_SIZE,
                                    "reward_risk_rateo":REWARD_RISK_RATEO,
                                    "start_time":datetime.now(),
                                    "running_time":0}

                TRADE_ID = str(int(TRADE_ID)+1)
                TRADE_ORDERBOOK[TRADE_ID] = TRADING_OPERATION 

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

                GAIN = GAIN - GAIN * TAKER_FEES # CALCULATE THE FEES
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
                                            
                    if type(GAIN_PERCENTAGE_24H) != float :
                        GAIN_PERCENTAGE_24H = float(GAIN_PERCENTAGE_24H[0])
                    
                    FITNESS = GAIN_PERCENTAGE_24H
                    FITNESS_DATA = {'fitness':FITNESS,'#trades':ID_TRADE_,'gain_24_h':GAIN_PERCENTAGE_24H,'msg':counter_messages}
                    store_perfomances(data = FITNESS_DATA, filename = STRATEGY_PATH)
                    #update_performance( performance = GAIN_PERCENTAGE_24H , performance_name = "fitness" , path = STRATEGY_PATH )

                    if TRADING == True:
                        try:
                            print(f'cancel order {ID_TRADE_}')
                            #response = client.cancel_order(symbol=MARKET,origClientOrderId=ID_TRADE_)

                        except binance.error.ClientError:
                            params = {
                                'symbol': MARKET,
                                'side': "SELL",
                                'type': "MARKET",
                                'quantity': N_TOKEN_CONTRACT,
                            }
                            print(params)
                            #response = client.new_order(**params)

                    CLOSED_TRADE_ID.append( ID_TRADE_ )

            # DELETE ALL THE CLOSED TRADE FROM THE TRADE ORDERBOOK
            for id_ in CLOSED_TRADE_ID:
                TRADE_ORDERBOOK = del_trade_orderbook(TRADE_ORDERBOOK, id_)

        # APPLY RUNNING TIME UPDATE TO EACH TRADE
        for op in TRADE_ORDERBOOK.items():
            ID_TRADE_ = op[0]
            TRADING_OPERATION_ = op[1]
            START_TIME = TRADING_OPERATION_['start_time']
            TRADING_OPERATION_['running_time'] = datetime.now() - START_TIME                     
            TRADE_ORDERBOOK[ID_TRADE_] = TRADING_OPERATION_ 

        endtime = datetime.now()
        EXECUTION_TIME = endtime - starttime




    #         if PLOT_DATA:
    #             # peaks
    #             plt.scatter(asks_volumes[peaks_asks],
    #                         asks_prices[peaks_asks], marker="*", color='blue',s=1500)
    #             plt.scatter(bids_volumes[peaks_bids],
    #                         bids_prices[peaks_bids], marker="*", color='red',s=1500)

    #             #plt.ylim([0.999*min(asks_prices),max(bids_prices)*1.0001])
    #             #plt.xlim([0,max(max(asks_volumes),max(bids_volumes))*1.05])

    #             # ask and bid bars https://www.youtube.com/watch?v=s4vTksDeG9c
    #             plt.barh(asks_prices, asks_volumes, alpha=0.55, height=0.18, color='orangered')
                
    #             plt.barh(bids_prices,bids_volumes, alpha=0.55, height=0.18, color='yellowgreen')

    #             # THRESHOLD filter
    #             plt.axvline(x=THRESHOLD_TICKER, color='teal',
    #                         label='operative filter THRESHOLD', linestyle='--', alpha=0.9)

    #             plt.axhline(y=MID_PRICE, color='indigo', linestyle='--', alpha=0.6)
    #             plt.axhline(y=min_ask_price, color='red', linestyle='--', alpha=0.6)
    #             plt.axhline(y=max_bid_price, color='green', linestyle='--', alpha=0.6)
                
    #             if TRADE_ORDERBOOK:
    #                 for k,v in TRADE_ORDERBOOK.items():
    #                     TRADING_OPERATION_ = v
    #                     TAKE_PROFIT = TRADING_OPERATION_['take_profits'][0]
    #                     ENTRY = TRADING_OPERATION_['entry_prices'][0]
    #                     STOP_LOSS = TRADING_OPERATION_['stop_losses'][0]
    #                     plt.axhline(y = TAKE_PROFIT, color='forestgreen', linestyle='dashdot', alpha=0.9)
    #                     plt.axhline(y = ENTRY, color='black', linestyle='dashdot', alpha=0.9)
    #                     plt.axhline(y = STOP_LOSS, color='maroon', linestyle='dashdot', alpha=0.9)

    #             plt.draw()
    #             plt.pause(0.1)
    #             plt.clf()


    #         #######################################################################
    #         ###################         PRINT DATA              ###################
    #         #######################################################################

            
    #         if PRINT_ANY_DATA:
    #             os.system('clear')
    #             print(f' python3 minerva/oracle.py -s {STRATEGY_PATH}')
    #             print(f' #Trades                       \t{TRADE_ID}')
    #             print(f' fitness: theoretical gain24h %\t{GAIN_PERCENTAGE_24H}')
                
    #             # if not BACKTEST_MODE:
    #             # EMPIRICAL_GAIN_PERCENTAGE_24H = get_gain_24h_percentage_from_account(initial_capital,ticker):
    #             # print(f' fitness: empirical gain24h %      {EMPIRICAL_GAIN_PERCENTAGE_24H}')
    #             print(f' Theoretical equity      \t{EQUITY}')
    #             print(f' Initial equity     \t{INITIAL_CAPITAL}')
    #             print(f'market              \t{MARKET}')
                
    #             if BACKTEST_MODE:
    #                 print(f'backtested days:\t{DAYS_COUNTER}')
    #                 print(f'data {counter_messages}')

    #             if PRINT_BASIC_DATA:
    #                 print(f'execution time in seconds: {EXECUTION_TIME.seconds}')
    #                 print(f'MID_PRICE       {MID_PRICE}')
    #                 print(f'min_ask_price   {min_ask_price}')
    #                 print(f'max_bid_price   {max_bid_price}')
    #                 print(f'OPERATION_PARAMETER {OPERATION_PARAMETER}')
    #                 print(f'ASK peaks       {peaks_asks}')
    #                 print(f'BID peaks       {peaks_bids}')
    #                 print(f'\nTRADE ORDERBOOK')
    #                 pprint(TRADE_ORDERBOOK)

    #             if PRINT_ALGORITHM:
    #                 print(f'\nDATASTRUCTURES')
    #                 print(f'\nTypes')
    #                 print(f'asks_volumes         {type(asks_volumes)}') 
    #                 print(f'bids_volumes         {type(bids_volumes)}')
    #                 print(f'asks_prices          {type(asks_prices)}') 
    #                 print(f'bids_prices          {type(bids_prices)}')
    #                 print(f'ask_array            {type(ask_array)}') 
    #                 print(f'bid_array            {type(bid_array)}')
    #                 print(f'peaks_asks           {type(peaks_asks)}') 
    #                 print(f'peaks_bids           {type(peaks_bids)}')
    #                 print(f'my_buffer_ask        {type(my_buffer_ask)}') 
    #                 print(f'my_buffer_bid        {type(my_buffer_bid)}')

    #                 print(f'\nLength')
    #                 print(f'asks_volumes         {len(asks_volumes)}') 
    #                 print(f'bids_volumes         {len(bids_volumes)}')
    #                 print(f'asks_prices          {len(asks_prices)}') 
    #                 print(f'bids_prices          {len(bids_prices)}')
    #                 print(f'ask_array            {len(ask_array)}') 
    #                 print(f'bid_array            {len(bid_array)}')
    #                 print(f'peaks_asks           {len(peaks_asks)}') 
    #                 print(f'peaks_bids           {len(peaks_bids)}')
    #                 print(f'my_buffer_ask        {len(my_buffer_ask)}') 
    #                 print(f'my_buffer_bid        {len(my_buffer_bid)}')

    #                 print(f'\nExamples')
    #                 print(f'asks_volumes         {asks_volumes[0]}') 
    #                 print(f'bids_volumes         {bids_volumes[0]}')
    #                 print(f'asks_prices          {asks_prices[0]}') 
    #                 print(f'bids_prices          {bids_prices[0]}')
    #                 print(f'ask_array            {ask_array[0]}') 
    #                 print(f'bid_array            {bid_array[0]}')
    #                 print(f'my_buffer_ask        {my_buffer_ask[-1][-1]}') 
    #                 print(f'my_buffer_bid        {my_buffer_bid[-1][-1]}')

    # plt.show(block=True)