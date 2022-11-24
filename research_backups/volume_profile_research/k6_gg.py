import scipy.signal
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

print(x, y)

Npks = 15

i_pk = scipy.signal.find_peaks_cwt(y, widths=range(3, len(x)//Npks))

DX = (np.max(x)-np.min(x))/float(Npks)  # starting guess for component width

# starting guess for (x, amp, width) for each component
guess = np.ravel([[x[i], y[i], DX] for i in i_pk])


fig = mpl.figure()
ax = fig.add_subplot(111)
ax.scatter(x, y)

ax.scatter(i_pk, c='r')
ax.legend()
mpl.show()
