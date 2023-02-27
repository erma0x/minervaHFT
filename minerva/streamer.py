#!/usr/bin/env python3

import requests
import time
import os
import json
import websocket
import argparse
from pprint import pprint
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import os
import zmq
import signal
from binance import Client as binance_client
import gc
gc.enable()
gc.set_threshold(1000,1000,1000)

import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from minerva.configuration_backtest import *
from minerva.configuration_strategy import MARKET
from minerva.oracle import format_binance_data
from minerva.database_utils import orderbook_storage
from minerva.genetic_algorithm import get_filepaths_list
from minerva.configuration_backtest import ORDERBOOK_BACKTESTING_FOLDER


def get_orderbook_database(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    QUERY = f"""SELECT * FROM {MARKET}"""
    results = pd.read_sql_query(QUERY,con=conn)
    return results


def get_orderbook_parquet(database_path):
    results = pd.read_parquet(database_path, engine='pyarrow')
    return results

def get_file_date_sql(filepath):
    """get the filepath date

    Args:
        database filepath (string): example: orderbook_2023-02-15_23:56

    Returns:
        date (string): 2023-02-15_23
    """
    #print(filepath)
    date_string = filepath.split("_")[1]  # year-month-day
    hours_string = filepath.split("_")[2].split(".")[0][:2] # hours
    dt = datetime.strptime(date_string + " " + hours_string, "%Y-%m-%d_%H")
    return dt

def get_file_date(filepath): # PARQUET
    """get the filepath date

    Args:
        database filepath (string): example: orderbook_2023-02-15_23:56

    Returns:
        date (string): 2023-02-15_23
    """
    #print(filepath)
    string_database_name = filepath.split("/")[-1]
    date_string = string_database_name.split('_')[1]  # year-month-day
    hours_string = filepath.split("_")[2].split(".")[0][:2] # hours
    dt = datetime.strptime(date_string + " " + hours_string, "%Y-%m-%d %H")
    return dt


def fake_streamer( socket ):
    
    list_of_database_files = get_filepaths_list( filepath_to_check = ORDERBOOK_BACKTESTING_FOLDER )
    # sorted_filepaths = sorted(list_of_database_files, key=get_file_date)
    sorted_filepaths = sorted(list_of_database_files)

    for file_db in sorted_filepaths: ###############################################
        gc.collect()
        #orderbook = get_orderbook_database(database_path = file_db)
        orderbook = get_orderbook_parquet(database_path = file_db)
        ask_generator = (item for item in orderbook.ask)
        bid_generator = (item for item in orderbook.bid)
        time_generator = (item for item in orderbook.timestamp)
        counter=0
        START_TIME = datetime.now()

        for i in time_generator:        

            if PRINT_TIMESTAMP:
                os.system('clear')
                counter+=1
                print(f'\n 🚀 backtester streaming...\n')
                print(f'backtesting {file_db}')
                print(f" data      {counter}")
                print(f" minutes   {round(counter*0.4/60,2)}")
                print(f" exec time {str(datetime.now()-START_TIME)[:-7]}")
                
            try:
                ask = next(ask_generator)
                bid = next(bid_generator)
                timestamp = next(time_generator)

                #print(f'ask {ask}')
                
                datapoint_orderbook = str(timestamp)+'|'+str(ask)+'|'+str(bid)
                #my_list_bytes = json.dumps(datapoint_orderbook)
                #print(datapoint_orderbook)
                socket.send(bytes(datapoint_orderbook.encode('utf-8')))
                #producer.send_string(datapoint_orderbook)

            except StopIteration:
                #socket.send_string('kill')
                break

            time.sleep(0.1)
    
    socket.send_string('kill')
    #exit()

def on_message(ws, message):
    # Funzione di callback per il ricevimento dei dati dal websocket
    try:
        counter_live_datapoints +=1
        if PRINT_TIMESTAMP:
            print(f'\n\t Live data {counter_live_datapoints} ,  {round(counter_live_datapoints*0.4/60,2)} minutes')
        
        data = json.loads(message)
        ask = data['a'] 
        bid = data['b']
        timestamp = datetime.now()
        
        datapoint_orderbook = str(timestamp)+'|'+str(ask)+'|'+str(bid)
        #my_list_bytes = json.dumps(datapoint_orderbook)
        socket.send(bytes(datapoint_orderbook.encode('utf-8')))
        #producer.send_string(datapoint_orderbook)

    except StopIteration as stop_error:
        #socket.send(bytes(datapoint_orderbook.encode('utf-8')))

        print(f'\n\t end data feed!')
    finally:
        time.sleep(0.4)


def get_live_orderbook(client,socket,ticker='BTCUSDT', limit_=200):
    try:
        depth = client.get_order_book(symbol=ticker, limit=limit_)
        data = format_binance_data(depth)

        ask = data['asks']
        bid = data['bids']
        timestamp = datetime.now()
        
        if PRINT_TIMESTAMP:
            os.system('clear')
            print(f'\n\tlive streaming! {timestamp}')  

        datapoint_orderbook = str(timestamp)+'|'+str(ask)+'|'+str(bid)
        socket.send(bytes(datapoint_orderbook.encode('utf-8')))
        
        if SAVE_LIVE_DATA_IN_SQL:
            orderbook_storage(ask=ask,bid=bid, database_path=ORDERBOOK_DATABASE)

        time.sleep(0.4)
    except:
        time.sleep(1)


if __name__ == '__main__':
    
    if BACKTEST_MODE:
        #signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()
        producer_socket = context.socket(zmq.PUB)
        producer_socket.bind("tcp://127.0.0.1:5556")
        fake_streamer(socket=producer_socket)

    if not BACKTEST_MODE:
        client = binance_client()
     
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:5557')

        print('live orderbook streamer')
        while True:
            get_live_orderbook(client, socket, MARKET)

    # if BACKTESTING in ('0',0):
    #     print('Testing live streaming')       
    #     signal.signal(signal.SIGINT, signal.SIG_DFL)
    #     context = zmq.Context()
    #     socket = context.socket(zmq.PUB)
    #     socket.bind('tcp://*:5555') 

    #     WEBSOCKET_URL = "wss://fstream.binance.com/BTCUSDT@depth"
    #     ws = websocket.WebSocketApp(WEBSOCKET_URL)
    #     ws.on_message = on_message # Imposta la funzione di callback per il ricevimento dei dati
    #     while True:
    #         ws.run_forever()