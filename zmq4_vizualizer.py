#!/usr/bin/env python3

from datetime import datetime
from sqlite3 import Timestamp
import time
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zmq

from parameters import  ORACLE_LINK, TOPICS, N_TICKS_VIZUALIZER, DATA_FILE_NAME, MARKET, REQUEST_TIME_INTERVAL


if __name__ == '__main__':

    context = zmq.Context()

    sub = context.socket(zmq.SUB)
    for topic in TOPICS:
        sub.setsockopt(zmq.SUBSCRIBE, bytes(topic.encode()))
        sub.setsockopt(zmq.RCVBUF, 0)
        sub.connect(ORACLE_LINK)
    
    
    plt.ion()
    plt.figure(figsize=(15,12))
    plt.gca()

    price_time_series = pd.Series()
    orderbook = None

    while True:

        message = sub.recv() 
        
        topic = message.decode().split('@')[0]

        print('topic -> ',topic)

        if topic == 'price':

            decoded_message = message.decode().split('@')[1]
            decoded_message = decoded_message.replace("'",'"')
            price = float(json.loads(decoded_message)['price'])
            timestamp = str(datetime.now())[14:22]
            
            if price_time_series.all():
                price_time_series =  price_time_series.append( pd.Series( price , index = [str(timestamp)] ) )

            else:
                price_time_series = pd.Series(price, index = [str(timestamp)])

            while len(price_time_series) > N_TICKS_VIZUALIZER:
                price_time_series = price_time_series.iloc[1:]

            
        if topic == 'orderbook':
            decoded_message = message.decode().split('@')[1]
            decoded_message = decoded_message.replace("'",'"')
            orderbook = json.loads(decoded_message)

        #if topic == 'klines':
        #    pass # add candlestick to candlestick_df


            
        if orderbook and price_time_series.any():
            plt.title(f'{MARKET} live-stream data from binance', color='indigo')
            plt.plot( price_time_series.iloc[-N_TICKS_VIZUALIZER:], color='teal', label = MARKET)
            plt.plot(np.array(orderbook['asks'])[:,1], np.array(orderbook['asks'])[:,0],color='orangered') 
            plt.plot(np.array(orderbook['bids'])[:,1], np.array(orderbook['bids'])[:,0],color='yellowgreen')
            plt.xticks(rotation=45)
            plt.draw()
            plt.pause(0.1)
            plt.clf()
    
    plt.show(block=True)