import os
import time
from binance import Client  # , ThreadedWebsocketManager, ThreadedDepthCacheManager

def get_orderbook(ticker='BTCUSDT', limit_=200):
    while True:
        try:
            client = Client()
            depth = client.get_order_book(symbol=ticker, limit=limit_)
            return (format_binance_data(depth))
        
        except:
            os.system('clear')
            print('error connection with binance')
            time.sleep(0.1)

def format_binance_data(data):
    ds = data
    for col in ['asks', 'bids']:
        for i in range(len(ds[col])):
            ds[col][i][0] = float(data[col][i][0])
            ds[col][i][1] = float(data[col][i][1])
    return ds