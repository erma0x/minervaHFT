import zmq
import requests
import random
import time
import pandas as pd
from  multiprocessing import Process
from parameters import ORACLE_LINK, MARKET, TOPICS, REQUEST_TIME_INTERVAL
from binance import Client #, ThreadedWebsocketManager, ThreadedDepthCacheManager
import datetime


def get_instant_price(market_='BTCUSDT'): 
    url = 'https://api.binance.com/api/v3/ticker/price?symbol='+market_
    data = requests.get(url).json()
    return data

def get_price(market_='BTCUSDT', tick_interval = '1m'): 
    url = 'https://api.binance.com/api/v3/klines?symbol='+market_+'&interval='+tick_interval+'&limit=1'
    data = requests.get(url).json()
    return data[0]


def get_full_price(market=MARKET):

    price = get_price(market_ = market, tick_interval = '1m')

    taker_buy_base_asset_volume = float(price[7])
    total_volume = float(price[0])
    
    maker_sell_base_asset_volume = taker_buy_base_asset_volume
    taker_sell_base_asset_volume = total_volume - taker_buy_base_asset_volume 
    maker_buy_base_asset_volume = taker_sell_base_asset_volume 

    price.append(taker_sell_base_asset_volume)
    price.append(maker_sell_base_asset_volume)
    price.append(maker_buy_base_asset_volume)

    current_time = str(datetime.datetime.now())[:-7]
    price.insert(0, current_time)

    row = str(price).replace('[','').replace(']','').replace("'","")
    
    return row

def get_orderbook_depth(ticker='BTCUSDT',limit_=30):
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

############################
def download_price_history(symbol='BTCUSDT', start_time='2020-06-22', end_time='2020-08-19', interval_mins=1):
    interval_ms = 1000*60*interval_mins
    interval_str = '%sm'%interval_mins if interval_mins<60 else '%sh'%(interval_mins//60)
    start_time = datetime.utc2timestamp(start_time)
    end_time = datetime.utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000*interval_ms):
        end_t = start_t + 1000*interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/fapi/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d
    df = pd.DataFrame(data, columns='time open high low close volume'.split())
    return df.astype({'time':'datetime64[ms]', 'open':float, 'high':float, 'low':float, 'close':float, 'volume':float})

def binance_publisher():
      
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(ORACLE_LINK)

    while True:
        
        for topic in TOPICS:
            
            if topic == 'price':
                object = get_instant_price(market_ = MARKET) # spot price

            if topic == 'orderbook':
                object = get_orderbook_depth(ticker = MARKET, limit_ = 600 ) # order book

            # if topic == 'klines':
            #     object = get_full_price( market = MARKET )
                

            publisher.send_string(str(topic) +'@'+str(object))

            print("Data published ", topic, object)
        
        time.sleep(REQUEST_TIME_INTERVAL)

if __name__ == "__main__":
    a = Process(target=binance_publisher, args=())
    a.start()
