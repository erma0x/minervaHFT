#!/usr/bin/env python3

import requests
import time
import os
import json
import websocket
import argparse
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import os
import zmq
import signal
from binance import Client as binance_client

from configuration_backtest import *
from configuration_strategy import MARKET
from oracle import format_binance_data
from database_utils import orderbook_storage


def get_orderbook_database(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    QUERY = f"""SELECT * FROM {MARKET}"""
    results = pd.read_sql_query(QUERY,con=conn)
    return results

def fake_streamer(socket):

    orderbook = get_orderbook_database(database_path = BACKTEST_ORDERBOOK_DATABASE)
    ask_generator = (item for item in orderbook.ask)
    bid_generator = (item for item in orderbook.bid)
    time_generator = (item for item in orderbook.timestamp)
    counter=0
    START_TIME = datetime.now()

    while True:        

        try:
            if PRINT_TIMESTAMP:
                os.system('clear')
                counter+=1
                print('🔶 Backtest streamer')
                print(f" data      {counter}")
                print(f" minutes   {round(counter*0.4/60,2)}")
                print(f" exec time {str(datetime.now()-START_TIME)[:-7]}")

            ask = next(ask_generator)
            bid = next(bid_generator)
            timestamp = next(time_generator)
            
            datapoint_orderbook = str(timestamp)+'|'+str(ask)+'|'+str(bid)
            #my_list_bytes = json.dumps(datapoint_orderbook)
            socket.send(bytes(datapoint_orderbook.encode('utf-8')))
            #producer.send_string(datapoint_orderbook)

        except StopIteration as stop_error:
            socket.send(b'kill')
            exit()

        finally:
            time.sleep(0.01)


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
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:5555')

        print(f'\n 🚀 backtester streaming...\n')
        while True:
            fake_streamer(socket=socket)


    if not BACKTEST_MODE:
        client = binance_client()
     
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:5555')

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