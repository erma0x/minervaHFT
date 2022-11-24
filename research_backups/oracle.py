#!/usr/bin/env python3
import zmq
# , REQUEST_TIME_INTERVAL, , MARKET
from configurations import DATASTREAMER_URL, ORACLE_URL, TOPICS_DATASTRAMER, EXAMPLE_TRADING_OPERATION
import time

"""

1. get data => return orderbook, klines

1. set operative filter => return (True/False)

2. spot front running oportunity => return ('LONG'/'SHORT'/ None)

2. spot peaks

3.  set x% above or below the peak ( +- n_channels )
        (try avoid it) kernelizer (spot gaussians borders)


"""

if __name__ == '__main__':

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(ORACLE_URL)

    sub = context.socket(zmq.SUB)

    for topic in TOPICS_DATASTRAMER:
        sub.setsockopt(zmq.SUBSCRIBE, bytes(topic.encode()))
        sub.setsockopt(zmq.RCVBUF, 0)
        sub.connect(DATASTREAMER_URL)

    while True:
        message = sub.recv_string()
        print(message)

        publisher.send_string('trade'+'@'+str(EXAMPLE_TRADING_OPERATION))
        print(EXAMPLE_TRADING_OPERATION)
        time.sleep(10)
