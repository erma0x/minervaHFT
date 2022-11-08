#!/usr/bin/env python3
import zmq
from parameters import DATASTREAMER_URL, ORACLE_URL, TOPICS_DATASTRAMER, EXAMPLE_TRADING_OPERATION #, REQUEST_TIME_INTERVAL, , MARKET

import time

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