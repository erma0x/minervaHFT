import os
import zmq
import time
from multiprocessing import Process
from configuration_backtest import DATASTREAMER_URL, MARKET, TOPICS_DATASTRAMER, REQUEST_TIME_INTERVAL, LIMIT_KLINES
import datetime
from datetime import datetime, timedelta
from binance import Client
from configuration_backtest import MOCK_ORDERBOOK_DATABASE_PATH
import sqlite3
import pandas as pd
import json

def format_binance_data(data):
    ds = data
    cols = ['asks','bids']
    for col in cols:
        for i in range(len(ds[col])):
            ds[col][i][0] = float(data[col][i][0])
            ds[col][i][1] = float(data[col][i][1])
    return ds

def get_orderbook_mock(database_path):
    """
    SELECT (SELECT COUNT(*)
    FROM main AS t2
    WHERE t2.col1 < t1.col1) + (SELECT COUNT(*)
    FROM main AS t3
    WHERE t3.col1 = t1.col1 AND t3.col1 < t1.col1) AS rowNum, * FROM Table_name t1  WHERE rowNum=0 ORDER BY t1.col1 ASC
    """

    conn = sqlite3.connect(database_path)

    # Crea il cursore per eseguire le query
    cursor = conn.cursor()
    QUERY = """SELECT * FROM objects"""
    results = pd.read_sql_query(QUERY,con=conn)
    return results


def get_orderbook_depth(client,ticker='BTCUSDT', limit_=200):
    while True:
        try:
            depth = client.get_order_book(symbol=ticker, limit=limit_)
            return (format_binance_data(depth))
        
        except:
            os.system('clear')
            print('error connection with binance')
            time.sleep(0.1)

def mock_datastreamer():
    client = Client()
    context = zmq.Context()

    producer = context.socket(zmq.PUB)
    producer.bind(DATASTREAMER_URL)

    orderbook = get_orderbook_mock(database_path=MOCK_ORDERBOOK_DATABASE_PATH)
    ask_generator = (item for item in orderbook.ask)
    bid_generator = (item for item in orderbook.bid)
    time_generator = (item for item in orderbook.timestamp)
    counter = 0
    while True:        

        try:
            os.system('clear')
            counter+=1
            print(f'\n\t Orderbook backtester with pykafka server\n')
            print(f'\n\t backtested data {counter} = {round(counter*0.4/60,2)} minutes')
            
            ask = next(ask_generator)
            bid = next(bid_generator)
            timestamp = next(time_generator)
            
            datapoint_orderbook = str(timestamp)+'|'+str(ask)+'|'+str(bid)
            #my_list_bytes = json.dumps(datapoint_orderbook)
            producer.send_string(datapoint_orderbook)
            print(,datapoint_orderbook)

        except StopIteration as stop_error:
            print(f'\n\t END data generation!')
        finally:
            time.sleep(0.4)


if __name__ == "__main__":
    a = Process(target = mock_datastreamer, args=()) # <--- CHANGE THIS FOR TESTING
    a.start()
