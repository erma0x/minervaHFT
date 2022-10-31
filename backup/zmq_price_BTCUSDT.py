import requests
import time
import zmq
import json
context = zmq.Context()

MARKET  = 'BTCUSDT'

def get_price(market='BTCUSDT', tick_interval = '1m'): 
    url = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval+'&limit=1'
    data = requests.get(url).json()
    return data[0]

#  Do 10 requests, waiting each time for a response
import zmq
import datetime

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5555")

while True:
    now = datetime.datetime.now()
    nowInMicroseconds = str(now.microsecond)
    socket.send_string(nowInMicroseconds)
    print("sending time in microseconds")
