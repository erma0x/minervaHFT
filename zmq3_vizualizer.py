#!/usr/bin/env python3

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from parameters import N_TICKS_VIZUALIZER, DATA_FILE_NAME

def plot_order_book(data):
    plt.plot(np.array(data['asks'])[:,0], np.array(data['asks'])[:,1]) 
    plt.plot(np.array(data['bids'])[:,0], np.array(data['bids'])[:,1])


if __name__ == '__main__':

    plt.ion()
    plt.figure(figsize=(15,12))

    while True:

        df_signal_plot = pd.read_csv(DATA_FILE_NAME, index_col=0, parse_dates=True,header=0)
        df_signal_plot.columns = [i.replace(' ','') for i in df_signal_plot.columns]
        plt.plot( df_signal_plot['close'][-N_TICKS_VIZUALIZER:], color='black', label='EUR_USD')
        plt.title('Stream data EURUSD price', color='darkblue')
        plt.xlabel("datetime")
        plt.ylabel("BTCUSDT")
        plt.draw()
        plt.pause(0.1)
        plt.clf()
        time.sleep(1)

    plt.show(block=True)
