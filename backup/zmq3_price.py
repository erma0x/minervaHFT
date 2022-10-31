#!/usr/bin/env python3

import requests
import time
import zmq
from parameters import REQUEST_TIME_INTERVAL, ORACLE_LINK, MARKET
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

if __name__ == '__main__':

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(ORACLE_LINK)

    while True:
        #try:
            #price_data = get_instant_price(market=MARKET)
        price_data = get_full_price(market=MARKET)

        #except:
        #    print('could not get data from the broker')

        #print(price_data['price'])
        #publisher.send(bytes(price_data['price'].encode()))
        
        print(price_data)
        publisher.send(bytes(price_data.encode()))
        
        #except:
        #    print('could not send the data to subribers')

        time.sleep(REQUEST_TIME_INTERVAL)
        