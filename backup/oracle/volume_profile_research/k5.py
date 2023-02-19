import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl


from binance import Client  # , ThreadedWebsocketManager, ThreadedDepthCacheManager


def get_orderbook_depth(ticker='BTCUSDT', limit_=20):
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

# print(orderbook)
# print(type(orderbook))
# x = np.linspace(0, 10, 100)
# y = func(x, 1, 5, 2)
# yn = y + 0.2 * np.random.normal(size=len(x))

x = np.array(orderbook['asks'])[:, 0]
yn = np.array(orderbook['asks'])[:, 1]
# yn = y + 0.2 * np.random.normal(size=len(x))


fig = mpl.figure()
ax = fig.add_subplot(111)
ax.scatter(x, yn)

# # Executing curve_fit on noisy data
popt, pcov = curve_fit(func, x, yn)

# #popt returns the best fit values for parameters of the given model (func)
# print(popt)

ym = func(x, popt[0], popt[1], popt[2])
ax.plot(x, ym, c='r', label='Best fit')
ax.legend()
mpl.show()
# #fig.savefig('model_fit.png')
