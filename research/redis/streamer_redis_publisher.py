import zmq
import time
from multiprocessing import Process
from configuration_backtest import DATASTREAMER_URL, TOPICS_DATASTRAMER, REQUEST_TIME_INTERVAL, LIMIT_KLINES
from datetime import datetime, timedelta
import redis

def get_orderbook_redis():
    pass

def datastream_publisher():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(DATASTREAMER_URL)

    while True:
        for topic in TOPICS_DATASTRAMER:
            if topic == 'orderbook':
                #object = get_orderbook_redis()  # order book
                last_time = list(conn.keys())[-1] 
                last_orderbook = conn.get(last_time)
            
            publisher.send_string(str(last_time) + '@'+str(last_orderbook))

        print("Data published ", topic, object)
        time.sleep(REQUEST_TIME_INTERVAL)


if __name__ == "__main__":
    conn = redis.Redis('localhost')
    a = Process(target=datastream_publisher, args=())
    a.start()
