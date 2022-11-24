import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from binance import Client


def get_orderbook_depth(ticker='BTCUSDT', limit_=200):
    client = Client()
    depth = client.get_order_book(symbol=ticker, limit=limit_)
    return (format_binance_data(depth))


def format_binance_data(data):
    ds = data
    for col in ['asks', 'bids']:
        for i in range(len(ds[col])):
            ds[col][i][0] = float(data[col][i][0])
            ds[col][i][1] = float(data[col][i][1])
    return ds


def func(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


if __name__ == '__main__':
    """
    PRENDI DATI

    TROVA PICCHI ASK
    TROVA PICCHI BID

    PLOTTA ORDERBOOK
    PLOTTA THRESHOLD
    PLOTTA PREZZO
    PLOTTA PICCHI

        TROVA MINIMI 
    peaks, _ = find_peaks( -y, height = 0, threshold = THRESHOLD_BTCUSDT, prominence = 5) #, distance = 1

    i picchi sono effettivamente quelli che vedo? -> setta threshold
    distanza dal picco precendente -> setta distanza

    bin = x
    intensita = y

    AUTOMATIZZARE QUANTI PICCHI CI SONO?
    AUTOMATIZZARE IL FIT DELLE GAUSSIANE

    SOLUZIONE 1
    grid search con fit gaussiana random +x,-x

    SOLUZIONE 2
    il limite e' quello dove trovi un minimo nel range di -x,+x 
    i minimi del picco li prendo come i due minimi locali accanto al massimo

    """

    LIMIT_ORDER_BOOK = 1000
    MARKET = 'BTCUSDT'

    orderbook = get_orderbook_depth(ticker=MARKET, limit_=LIMIT_ORDER_BOOK)

    asks_prices = np.array(orderbook['asks'])[:, 0]
    asks_volumes = np.array(orderbook['asks'])[:, 1]
    bids_prices = np.array(orderbook['bids'])[:, 0]
    bids_volumes = np.array(orderbook['bids'])[:, 1]

    MID_PRICE = (min(np.array(orderbook['asks'])[
                 :, 0]) + max(np.array(orderbook['bids'])[:, 0])) / 2

    print(f'mid price {MARKET} {MID_PRICE}')
    print('asks_volumes', asks_volumes[-5:])
    print(asks_prices[-2:], '==', asks_volumes[-2:])

    max_ask = max(asks_volumes)
    max_bid = max(bids_volumes)

    THRESHOLD_DIVISOR = 4
    THRESHOLD_BTCUSDT = max(max_ask, max_bid) / THRESHOLD_DIVISOR
    LIMIT_ORDER_BOOK_DIVISOR = 20
    # number of channels / int
    PEAK_DISTANCE = int(round(LIMIT_ORDER_BOOK / LIMIT_ORDER_BOOK_DIVISOR))

    peaks_asks, _1 = find_peaks(
        asks_volumes, height=0, threshold=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)
    peaks_bids, _2 = find_peaks(
        bids_volumes, height=0, threshold=THRESHOLD_BTCUSDT, distance=PEAK_DISTANCE)

    # peaks
    plt.scatter(asks_volumes[peaks_asks],
                asks_prices[peaks_asks], marker="*", color='blue')
    plt.scatter(bids_volumes[peaks_bids],
                bids_prices[peaks_bids], marker="*", color='red')

    # ask and bid bars
    plt.barh(np.array(orderbook['asks'])[:, 0], np.array(orderbook['asks'])[
             :, 1], alpha=0.6, height=0.5, color='orangered')
    plt.barh(np.array(orderbook['bids'])[:, 0], np.array(orderbook['bids'])[
             :, 1], alpha=0.6, height=0.5, color='yellowgreen')

    # threshold filter
    plt.axvline(x=THRESHOLD_BTCUSDT, color='teal',
                label='operative filter threshold', linestyle='--', alpha=0.3)

    # mid price
    plt.axhline(y=MID_PRICE, color='indigo', linestyle='-', alpha=0.5)
    plt.show()
