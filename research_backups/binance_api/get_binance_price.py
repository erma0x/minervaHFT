#!/usr/bin/env python3
# coding: utf-8
import os
import requests
import asyncio
from datetime import datetime
from math import floor
from binance import AsyncClient, BinanceSocketManager


def timestamp_to_date(time):
    time = str(time)
    return (datetime.fromtimestamp(int(time[:-3])).strftime('%d-%m-%Y %H:%M:%S'))


async def get_data(client, token_pair='BNBUSDT'):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol=token_pair) as stream:
        res = await stream.recv()
        print('date: ', timestamp_to_date(
            res['k']['T']), ' closing price: ', res['k']['c'], ' volume: ', res['k']['V'])
        return (res['k']['c'])  # closing price


async def main():
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')
    client = await AsyncClient.create(api_key, api_secret)
    my_symbols = ['ETH', 'BTC']
    while True:
        for symbol in my_symbols:
            price = await get_data(client, token_pair=symbol+'USDT')

            # save

            print(symbol+'USDT: ', price)
            print('-'*80)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
