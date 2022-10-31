#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import time
import datetime
import requests
from parameters import DATA_FILE_NAME, INTERVAL_OF_SECONDS, header, MARKET

def get_price(market='BTCUSDT', tick_interval = '1m'): 
    url = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval+'&limit=1'
    data = requests.get(url).json()
    return data[0]

def init_file():
    if not os.path.isfile(DATA_FILE_NAME):
        os.system(f"touch {sys.path[0]+'/'+DATA_FILE_NAME}")
        with open(DATA_FILE_NAME,  "+a") as f:
            f.write(str(header).replace("'","").replace('[','').replace(']','').replace(' ','') + '\n')
            f.close()

if __name__ == '__main__':
    
    init_file()

    while True:

        price = get_price(market = MARKET, tick_interval = '1m')

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

        row = str(price).replace('[','').replace(']','').replace("'","") + '\n'
        
        with open(DATA_FILE_NAME, "+a") as f:
            f.write(row)
            f.close()
            
        time.sleep( INTERVAL_OF_SECONDS )