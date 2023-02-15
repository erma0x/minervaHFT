#!/usr/bin/env python3
from configuration_backtest import DATASTREAMER_URL, ORACLE_URL, TOPICS_DATASTRAMER, TOPICS_ORACLE
from configuration_backtest import N_TICKS_VIZUALIZER,  MARKET, REQUEST_TIME_INTERVAL, TRADING_OPERATION
import zmq
import json
from collections import defaultdict
import dateutil.parser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from datetime import datetime, timedelta
from binance import Client  # , ThreadedWebsocketManager, ThreadedDepthCacheManager


def utc2timestamp(s): 
    return int(dateutil.parser.parse(s).replace(tzinfo=pytz.utc).timestamp() * 1000)


def volume_profile(df):
    start_price = df['Close'].min()
    stop_price = df['Close'].max()

    low = start_price

    # delta means granularity in volume aggregation range, it is delta in price
    # the volume corresponds to price

    # splitting whole price range into blocks
    delta = (stop_price - start_price)/100
    high = 0
    idx_array = []
    vol_array = []
    low_array = []

    while high < stop_price:
        volume = 0
        high = low + delta

        sub_df = df.loc[df['Close'].between(low, high, inclusive=False)]
        low_array.append(low)

        for i in sub_df.index.values:
            volume = volume + df.iloc[i]['Volume']

        vol_array.append(volume)
        low = high

    for idx, var in enumerate(vol_array):
        idx_array.append(idx)
    return low_array, vol_array


def load_trading_operation(message):
    trading_operation = json.loads(message.replace("'", '"'))
    for i in ['take_profits', 'entry_prices', 'stop_losses']:
        trading_operation[i] = [int(x) for x in trading_operation[i]]
    return trading_operation


if __name__ == '__main__':

    context = zmq.Context()

    subscriber_oracle = context.socket(zmq.SUB)

    # contex_oracle = zmq.Context()
    # socket_oracle = contex_oracle.socket(zmq.SUB)
    # socket_oracle.connect(ORACLE_URL)
    # socket_oracle.subscribe("") # Subscribe to all topics

    subscriber_datastreamer = context.socket(zmq.SUB)
    for topic in TOPICS_DATASTRAMER:
        subscriber_datastreamer.setsockopt(
            zmq.SUBSCRIBE, bytes(topic.encode()))
        subscriber_datastreamer.setsockopt(zmq.RCVBUF, 0)
        subscriber_datastreamer.connect(DATASTREAMER_URL)

    price_time_series = pd.Series()
    orderbook = None
    volume_array = None
    TRADING_OPERATION = None

    plt.ion()
    plt.figure(figsize=(20, 8), dpi=80, facecolor='w', edgecolor='k')
    plt.gca()

    # PERPETUAL CONTRACT KUCOINFUTURES FEE STRUCTURE
    TAKER_FEES = 0.0006 # (0,1) % 
    MAKER_FEES = 0.0002 # (0,1) %

    while True:

        message = subscriber_datastreamer.recv_string()
        topic = message.split('@')[0]

        # print('topic -> ',topic)

        # raw_TRADING_OPERATION = socket_oracle.recv_string()
        # TRADING_OPERATION = raw_TRADING_OPERATION.split('@')[1]
        # TRADING_OPERATION = load_trading_operation(message = TRADING_OPERATION)

        if topic == 'price':

            decoded_message = message.split('@')[1]
            decoded_message = decoded_message.replace("'", '"')
            price = float(json.loads(decoded_message)['price'])
            timestamp = str(datetime.now())[14:22]

            if price_time_series.all():
                price_time_series = price_time_series.append(
                    pd.Series(price, index=[str(timestamp)]))

            else:
                price_time_series = pd.Series(price, index=[str(timestamp)])

            while len(price_time_series) > N_TICKS_VIZUALIZER:
                price_time_series = price_time_series.iloc[1:]

        if topic == 'orderbook':

            decoded_message = message.split('@')[1]
            decoded_message = decoded_message.replace("'", '"')
            orderbook = json.loads(decoded_message)

        if topic == 'klines':

            decoded_message = message.split('@')[1]
            #decoded_message = decoded_message.replace("'",'"').replace(",",'","').replace('[','["').replace(']','"]').replace(' ','')

            # LOAD DATASET FROM MESSAGE -> JSON -> PD.DATAFRAME
            #df = pd.DataFrame.from_records(map(json.loads, decoded_message))
            json_object = json.loads(json.dumps(decoded_message))
            #json_object = json.loads(decoded_message)

            candlestick_df = pd.read_json(json_object)
            #candlestick_df = pd.json_normalize(json_object)
            # print(json_object)
            # print(candlestick_df.head())
            # candlestick_df = download_price_history( symbol = MARKET, start_time = START_DATE , end_time = END_DATE)
            price_array, volume_array = volume_profile(candlestick_df)

            # more than 1 day of data
            # if candlestick_df["time"].iloc[:-1] == datetime.today()  :
            #    pass

            # 1. df.time unix to datetime
            # 2. se fra adesso e l'ultimo dato se ne puo'aggiungere un altro
            # 3. rimuovi il primo arrivato (il piu vecchio) ed aggiungi l'ultimo in append
        if topic == 'trading_orderbook':
            TRADE_ORDERBOOK = message.split('@')[1]
            
        # VISUALIZE CHART
        if orderbook and price_time_series.any():  # and volume_array:

            # # spot price#
            # plt.plot(price_time_series.iloc[-N_TICKS_VIZUALIZER:],
            #          color='teal', label=MARKET,  marker='o')

            # #SCALED_ORDERBOOK_PARAM = max(volume_array)/max(np.array(orderbook['asks'])[:,1])

            # # ask orderbook
            # #plt.barh(np.array(orderbook['asks'])[:,0], np.array(orderbook['asks'])[:,1] * SCALED_ORDERBOOK_PARAM , alpha = 0.85, color='orangered')
            # plt.barh(np.array(orderbook['asks'])[
            #          :, 0], np.array(orderbook['asks'])[:, 1])
            # # bid orderbook
            # #plt.barh(np.array(orderbook['bids'])[:,0], np.array(orderbook['bids'])[:,1] * SCALED_ORDERBOOK_PARAM , alpha = 0.85, color='yellowgreen')
            # plt.barh(np.array(orderbook['bids'])[
            #          :, 0], np.array(orderbook['bids'])[:, 1])
            # volume profile
            #plt.barh(price_array, volume_array, alpha = 0.85, color='indigo')



            # plotted = False

            # if TRADING_OPERATION:
            #     SIDE = TRADING_OPERATION['side'] # PRINT text
            #     ENTRIES = TRADING_OPERATION['entry_prices']
            #     TAKE_PROFITS = TRADING_OPERATION['take_profits']
            #     STOP_LOSSES = TRADING_OPERATION['stop_losses']
            #     #print(ENTRIES,TAKE_PROFITS,STOP_LOSSES)
            #     # # ENTRIES
            #     plotted = True
            #     for e in ENTRIES:
            #         plt.axhline(y = e, xmin=0, xmax=1000, alpha = 0.85, color='black', linestyle = '--')

            #     for tp in TAKE_PROFITS:
            #         plt.axhline(y = tp, xmin=0, xmax=1000, alpha = 0.85, color='green', linestyle = '--')

            #     for sl in STOP_LOSSES:
            #         plt.axhline(y = sl, xmin=0, xmax=1000, alpha = 0.85, color='red', linestyle = '--')

            # # SIDE & FILL time
            # plt.annotate(f'ENTRY {SIDE}', xy=(2, 1), xytext=(3, 4),arrowprops=dict(facecolor='blue', shrink=0.05))
            # # SIDE & Exit time
            # plt.annotate(f'EXIT {SIDE}', xy=(2, 1), xytext=(3, 4),arrowprops=dict(facecolor='orange', shrink=0.05))


        # VISUALIZER component to extract as another component
        # TIMING 1.5 seconds
        if PLOT_DATA:
            plt.plot(price_time_series.iloc[-N_TICKS_VIZUALIZER:],
                     color='teal', label=MARKET,  marker='o')
                        # actual price
            plt.axhline(
                price_time_series.iloc[-1], alpha=0.3, color='teal', linestyle='-')

            # peaks
            plt.scatter(asks_volumes[peaks_asks],
                        asks_prices[peaks_asks], marker="*", color='blue')
            plt.scatter(bids_volumes[peaks_bids],
                        bids_prices[peaks_bids], marker="*", color='red')

            # ask and bid bars
            plt.barh(np.array(orderbook['asks'])[:, 0], np.array(orderbook['asks'])[
                    :, 1], alpha=0.75, height=0.18, color='orangered')
            
            plt.barh(np.array(orderbook['bids'])[:, 0], np.array(orderbook['bids'])[
                    :, 1], alpha=0.75, height=0.18, color='yellowgreen')

            # threshold filter
            plt.axvline(x=THRESHOLD_BTCUSDT, color='teal',
                        label='operative filter threshold', linestyle='--', alpha=0.3)

            # mid price
            plt.axhline(y=MID_PRICE, color='indigo', linestyle='--', alpha=0.5)
            plt.axhline(y=MICRO_PRICE, color='indigo', linestyle='-', alpha=0.6)

            # plot trading operation
            if TRADE_ORDERBOOK:
                for op in TRADE_ORDERBOOK.items():
                    TRADING_OPERATION_ = op[1]
                    TAKE_PROFIT = TRADING_OPERATION_['take_profits'][0]
                    ENTRY = TRADING_OPERATION_['entry_prices'][0]
                    STOP_LOSS = TRADING_OPERATION_['stop_losses'][0]
                    plt.axhline(y = TAKE_PROFIT, color='forestgreen', linestyle='dashdot', alpha=0.9)
                    plt.axhline(y = ENTRY, color='black', linestyle='dashdot', alpha=0.9)
                    plt.axhline(y = STOP_LOSS, color='maroon', linestyle='dashdot', alpha=0.9)


            plt.title(f'{MARKET} Binance Data Streamer ', color='white', fontsize=20,
                      fontweight=10, pad='2.0', loc="left", backgroundcolor='black', fontstyle='italic')
            plt.xlabel('time & relative volumes',
                       fontsize='large', fontweight='bold')
            plt.ylabel(f'{MARKET} price', fontsize='large', fontweight='bold')
            plt.xticks(rotation=45)

            plt.draw()
            plt.pause(0.1)
            plt.clf()


    plt.show(block=True)
