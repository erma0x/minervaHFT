#!/usr/bin/env python3

import time
import zmq
from binance import Client #, ThreadedWebsocketManager, ThreadedDepthCacheManager
from parameters import REQUEST_TIME_INTERVAL, DATASTREAMER_URL, MARKET, TOPICS_DATASTRAMER

def get_orderbook_depth(ticker='BTCUSDT',limit_=1000):
    client = Client()
    depth = client.get_order_book(symbol=ticker,limit=limit_)
    return(format_binance_data(depth))

def format_binance_data(data):
    ds = data
    for col in ['asks','bids']:
        for i in range(len(ds[col])):
            ds[col][i][0] = float(data[col][i][0])
            ds[col][i][1] = float(data[col][i][1])
    return ds

if __name__ == '__main__':

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(DATASTREAMER_URL)

    while True:
        orderbook = get_orderbook_depth(ticker=MARKET,limit_=600)
        socket.send_string(f"{orderbook}")
        time.sleep(REQUEST_TIME_INTERVAL)