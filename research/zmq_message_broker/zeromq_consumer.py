#!/usr/bin/env python3
import zmq
# , REQUEST_TIME_INTERVAL, , MARKET
from configuration_backtest import DATASTREAMER_URL, ORACLE_URL, TOPICS_DATASTRAMER, EXAMPLE_TRADING_OPERATION
import time

if __name__ == '__main__':

    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    print('starting')
    
    subscriber_datastreamer = context.socket(zmq.SUB)
    subscriber_datastreamer.setsockopt(zmq.SUBSCRIBE, bytes(''.encode()))
    subscriber_datastreamer.setsockopt(zmq.RCVBUF, 0)
    subscriber_datastreamer.connect(DATASTREAMER_URL)

    while True:
        message = sub.recv_string()
        print(message)