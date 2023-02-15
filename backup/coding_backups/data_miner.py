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

    LIMIT_ORDER_BOOK = 50
    MARKET = 'BTCUSDT'

    orderbook = get_orderbook_depth(ticker=MARKET, limit_=LIMIT_ORDER_BOOK)

    asks_prices = np.array(orderbook['asks'])[:, 0]
    asks_volumes = np.array(orderbook['asks'])[:, 1]
    bids_prices = np.array(orderbook['bids'])[:, 0]
    bids_volumes = np.array(orderbook['bids'])[:, 1]
   
    MID_PRICE = (min(asks_prices) + max(bids_prices) ) / 2

    # prendo Ask e Bid con un filtro
    # Se una delle due e' molto piu grande delle altre allora fai front running

    AB_LEN = 10 #numero di canali prima e dopo A (e B) 
    
    # prendo asks_prices dal prezzo piu basso e prendo i primi X1 in ordine CRESCENTE
    print(asks_prices[:AB_LEN])
    print(asks_volumes[:AB_LEN])
    A = sum(asks_volumes[:AB_LEN])

    # prendo bids_prices dal prezzo piu basso e prendo i primi X1 in ordine DE-CRESCENTE
    print(bids_prices[:AB_LEN])
    print(bids_volumes[:AB_LEN])
    B = sum(bids_volumes[:AB_LEN])

    print(f'A: {A}  B: {B}')
    # A = prendo i primi X1 asks_volumes in ordine CRESCENTE 
    # B = prendo i primi X1 bids_volumes in ordine DE-CRESCENTE 

    THRESHOLD_VOLUME_BTCUSDT = 0.001 # FILTRO OPERATIVO ASSOLUTO
    THESHOLD_SHORT = 0.8
    THESHOLD_LONG = 0.2

    # se A > threshold e B > threshold
    if A > THRESHOLD_VOLUME_BTCUSDT and B > THRESHOLD_VOLUME_BTCUSDT:
        print('FRONT RUNNING')

        OPERATION_PARAMETER = A/(A+B)
    
    # se A / (A+B) > threshold_long and operation=True
        if OPERATION_PARAMETER > THESHOLD_SHORT:
            print('SHORT')

    # se A / (A+B) < threshold_short and operation=True
        if OPERATION_PARAMETER < THESHOLD_LONG:
            print('LONG')
            
    
        max_ask_absolute_volume = max(asks_volumes)
        max_bid_absolute_volume = max(bids_volumes)
        min_ask_price = min(asks_prices)
        max_bid_price = min(asks_prices)
        
        x = np.where(asks_prices == min_ask_price)[0] # find the index of this in the list
        y = np.where(asks_prices == max_bid_price)[0] 
        
        BEST_ASK_OFFER_VOLUME = bids_prices[x]  # lowest ask
        BEST_BID_OFFER_VOLUME = bids_volumes[y] # highest bid

        MICRO_PRICE = (BEST_ASK_OFFER_VOLUME*min_ask_price + BEST_BID_OFFER_VOLUME*max_bid_price) / BEST_ASK_OFFER_VOLUME+BEST_BID_OFFER_VOLUME
        MICRO_PRICE = MICRO_PRICE[0]
        print(f'MICRO price  : {MICRO_PRICE}')
        print(f'MID   price  : {MID_PRICE}')

        THRESHOLD_DIVISOR = 10
        THRESHOLD_BTCUSDT = max(max_ask_absolute_volume, max_bid_absolute_volume) / THRESHOLD_DIVISOR
        LIMIT_ORDER_BOOK_DIVISOR = 10
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
                :, 1], alpha=0.75, height=0.18, color='orangered')
        
        plt.barh(np.array(orderbook['bids'])[:, 0], np.array(orderbook['bids'])[
                :, 1], alpha=0.75, height=0.18, color='yellowgreen')

        # threshold filter
        plt.axvline(x=THRESHOLD_BTCUSDT, color='teal',
                    label='operative filter threshold', linestyle='--', alpha=0.3)

        # mid price
        plt.axhline(y=MID_PRICE, color='indigo', linestyle='-', alpha=0.5)
        plt.show()