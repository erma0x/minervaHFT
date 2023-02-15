import os
import zmq
import time
from multiprocessing import Process
from configuration_backtest import DATASTREAMER_URL, MARKET, TOPICS_DATASTRAMER, REQUEST_TIME_INTERVAL, LIMIT_KLINES
import datetime
from datetime import datetime, timedelta
from binance import Client

def get_orderbook_depth(client,ticker='BTCUSDT', limit_=200):
    while True:
        try:
            depth = client.get_order_book(symbol=ticker, limit=limit_)
            return (format_binance_data(depth))
        
        except:
            os.system('clear')
            print('error connection with binance')
            time.sleep(0.1)

def datastream_publisher():
    client = Client()
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(DATASTREAMER_URL)

    while True:

        for topic in TOPICS_DATASTRAMER:

            if topic == 'price':
                object = get_instant_price(market_=MARKET)  # spot price

            if topic == 'orderbook':
                object = get_orderbook_depth(client=client,ticker=MARKET, limit_=100)  # order book

            # klines_required = True
            # KLINES_FILE = 'history_required.txt'

            # with open(KLINES_FILE,'r') as f:
            #     if f.readlines():
            #         klines_required = True

            # with open(KLINES_FILE,'+w') as f:
            #     f.write('')

            if topic == 'klines':  # and klines_required
                START_DATE = datetime.today()
                END_DATE = datetime.today() - timedelta(days=1)

                START_DATE = str(START_DATE)[:10]
                END_DATE = str(END_DATE)[:10]

                #object = download_price_history( symbol = MARKET, start_time = START_DATE , end_time = END_DATE)
                price_history_dataFrame = download_price_history(
                    symbol='BTCUSDT', start_time='2022-11-01', end_time='2022-11-02')
                object = price_history_dataFrame.to_json()

            publisher.send_string(str(topic) + '@'+str(object))

            print("Data published ", topic, object)

        time.sleep(REQUEST_TIME_INTERVAL)


if __name__ == "__main__":
    a = Process(target=datastream_publisher, args=())
    a.start()
