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
import gc
gc.enable()
gc.set_threshold(1000,1000,1000)

import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from configuration_trading import TICKER, BASE_CURRENCY,MARKET
from oracle import format_binance_data
from database_utils import orderbook_storage
from genetic_algorithm import get_filepaths_list
from configuration_backtest import *
from configuration_backtest import ORDERBOOK_BACKTESTING_FOLDER
from configuration_trading import TICKER, BASE_CURRENCY
import asyncio
import websockets
import json

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
        date (string): '2023-02-15_23'
    """
    string_database_name = filepath.split("/")[-1]
    date_string = string_database_name.split('_')[1]  # year-month-day
    hours_string = filepath.split("_")[2].split(".")[0][:2] # hours
    dt = datetime.strptime(date_string + " " + hours_string, "%Y-%m-%d %H")
    return dt


async def call_api(socket):
    msg = {"method": "SUBSCRIBE", "params":
            [
            f"{TICKER.lower()+BASE_CURRENCY.lower()}@depth" # btcusdt@depth
            ],
            "id": 1
            }
    async with websockets.connect('wss://stream.binance.com:9443/ws/'+TICKER.lower()+BASE_CURRENCY.lower()+'@depth') as ws:
        while True:
            await ws.send(json.dumps(msg))
            response = await asyncio.wait_for(ws.recv(), timeout=2)
            response = json.loads(response)
            
            try:
                pprint(response['a'])
            except:
                print(response)
            print('-'*100)

            try:
                ask = response["a"]
                bid = response["b"]
                timestamp = datetime.now()
            except:
                ask = None
                bid = None
                timestamp = datetime.now()
            finally:
                datapoint_orderbook = str(timestamp)[:19]+'|'+str(ask)+'|'+str(bid)
                socket.send(bytes(datapoint_orderbook.encode('utf-8')))

            await asyncio.sleep(0.41)


def get_orderbook_database(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    QUERY = f"""SELECT * FROM {MARKET}"""
    results = pd.read_sql_query(QUERY,con=conn)
    return results


def get_orderbook_parquet(database_path):
    results = pd.read_parquet(database_path, engine='pyarrow')
    return results


def fake_streamer( socket ):
    list_of_database_files = get_filepaths_list( filepath_to_check = ORDERBOOK_BACKTESTING_FOLDER )
    # sorted_filepaths = sorted(list_of_database_files, key=get_file_date)
    sorted_filepaths = sorted(list_of_database_files)

    for file_db in sorted_filepaths:
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
                datapoint_orderbook = str(timestamp)+'|'+str(ask)+'|'+str(bid)
                #my_list_bytes = json.dumps(datapoint_orderbook)
                socket.send(bytes(datapoint_orderbook.encode('utf-8')))

            except StopIteration:
                #socket.send_string('kill')
                break

            time.sleep(0.08)
    
    socket.send_string('kill')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Set bind link for consumer')
    parser.add_argument('--link', dest='link', default="tcp://*:5557",
                        help='Set bind link for consumer (default: "tcp://*:5557")')
    args = parser.parse_args()

    if BACKTEST_MODE:
        #signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()
        producer_socket = context.socket(zmq.PUB)
        producer_socket.bind(args.link)
        fake_streamer(socket=producer_socket)

    if not BACKTEST_MODE:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()        
        node_socket = context.socket(zmq.PUB)
        node_socket.bind(args.link)

        while True:
            try:
                asyncio.get_event_loop().run_until_complete(call_api(socket=node_socket))
            except websockets.exceptions.ConnectionClosedError:
                print('lost connection')
                node_socket.close()
                time.sleep(0.01)
                context.destroy()
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                context = zmq.Context()
                node_socket = context.socket(zmq.PUB)
                node_socket.bind(args.link)

            except zmq.error.ZMQError:
                print('retry connection with zmq')
                node_socket.close()
                time.sleep(0.01)
                context.destroy()
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                context = zmq.Context()
                node_socket = context.socket(zmq.PUB)
                node_socket.bind(args.link)

            except asyncio.exceptions.CancelledError:
                node_socket.close()
                time.sleep(0.01)
                context.destroy()
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                context = zmq.Context()
                node_socket = context.socket(zmq.PUB)
                node_socket.bind(args.link)
                asyncio.get_event_loop().run_until_complete(call_api(socket=node_socket))
