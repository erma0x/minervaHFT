#!/usr/bin/env python3
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

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

def plot_order_book(data):
    plt.plot(np.array(data['asks'])[:,0], np.array(data['asks'])[:,1]) 
    plt.plot(np.array(data['bids'])[:,0], np.array(data['bids'])[:,1])

depth = get_orderbook_depth(ticker='BTCUSDT')
print(depth)