#!/usr/bin/env python3

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pprint import pprint

client = Client()
depth = client.get_order_book(symbol='BTCUSDT',limit=999)
pprint(depth)

#  curl -X "GET" "https://api.binance.us/api/v3/depth?symbol=BTCUSDT"
# MANUALE https://docs.binance.us/#get-aggregate-trades