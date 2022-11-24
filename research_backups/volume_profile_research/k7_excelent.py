import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import electrocardiogram

from scipy.signal import find_peaks

#x = electrocardiogram()[2000:4000]


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl


from binance import Client  # , ThreadedWebsocketManager, ThreadedDepthCacheManager


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


orderbook = get_orderbook_depth()

x = np.array(orderbook['asks'])[:, 0]
y = np.array(orderbook['asks'])[:, 1]

THRESHOLD_BTCUSDT = max(y)/2

peaks, _ = find_peaks(y, height=0, threshold=THRESHOLD_BTCUSDT, prominence=5)


# TROVA MINIMI
# peaks, _ = find_peaks( -y, height = 0, threshold = THRESHOLD_BTCUSDT, prominence = 5) #, distance = 1

# i picchi sono effettivamente quelli che vedo? -> setta threshold
# distanza dal picco precendente -> setta distanza

# bin = x
# intensita = y

# AUTOMATIZZARE QUANTI PICCHI CI SONO?
# AUTOMATIZZARE IL FIT DELLE GAUSSIANE

# SOLUZIONE 1
# grid search con fit gaussiana random +x,-x

# SOLUZIONE 2
# il limite e' quello dove trovi un minimo nel range di -x,+x
# i minimi del picco li prendo come i due minimi locali accanto al massimo


# invece che dargli in ingresso y
plt.plot(peaks, y[peaks], "x")
plt.plot(x, y)

plt.axhline(y=THRESHOLD_BTCUSDT, color='r', linestyle='-',
            xmin=min(x), xmax=max(x))  # <- min/max peaks
plt.plot(np.zeros_like(y), "--", color="gray")

plt.show()
