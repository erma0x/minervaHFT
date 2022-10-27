#!/usr/bin/env python3
import zmq
from parameters import ORACLE_LINK #, REQUEST_TIME_INTERVAL, , MARKET

if __name__ == '__main__':

    context = zmq.Context()

    # subscriber = context.socket(zmq.SUB)
    # subscriber.connect('ipc://127.0.0.1:5678')
    # subscriber.setsockopt(zmq.SUBSCRIBE, b"BTCUSDT")
    # publisher = context.socket (zmq.PUB)
    # publisher.bind("ipc://nasdaq-feed")

    sub = context.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b'')
    sub.setsockopt(zmq.RCVBUF, 0)
    sub.connect(ORACLE_LINK)

    while True:
        message = sub.recv()
        print(message.decode())
        
        #publisher.send(message)
