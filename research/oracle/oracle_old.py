#!/usr/bin/env python3
import zmq
# , REQUEST_TIME_INTERVAL, , MARKET
from configuration_backtest import DATASTREAMER_URL, ORACLE_URL, TOPICS_DATASTRAMER, EXAMPLE_TRADING_OPERATION
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
    #publisher = context.socket(zmq.PUB)
    #publisher.bind(ORACLE_URL)

    sub = context.socket(zmq.SUB)

    #for topic in TOPICS_DATASTRAMER:
    print('starting')
    
    subscriber_datastreamer = context.socket(zmq.SUB)
    for topic in ['orderbook']:
        subscriber_datastreamer.setsockopt(
            zmq.SUBSCRIBE, bytes(topic.encode()))
        subscriber_datastreamer.setsockopt(zmq.RCVBUF, 0)
        subscriber_datastreamer.connect(DATASTREAMER_URL)

    while True:
        print('ok')
        message = sub.recv_string()
        print(message)

        #publisher.send_string('trade'+'@'+str(EXAMPLE_TRADING_OPERATION))
        #print(EXAMPLE_TRADING_OPERATION)
        time.sleep(1)
