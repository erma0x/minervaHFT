#!/usr/bin/env python3
from collections import defaultdict
import dateutil.parser
import numpy as np
import pandas as pd
import requests
import pytz


def utc2timestamp(s): return int(dateutil.parser.parse(
    s).replace(tzinfo=pytz.utc).timestamp() * 1000)


def download_price_history(symbol='BTCUSDT', start_time='2020-06-22', end_time='2020-08-19', interval_mins=1):
    interval_ms = 1000*60*interval_mins
    interval_str = '%sm' % interval_mins if interval_mins < 60 else '%sh' % (
        interval_mins//60)
    start_time = utc2timestamp(start_time)
    end_time = utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000*interval_ms):
        end_t = start_t + 1000*interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/fapi/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (
            interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d
    df = pd.DataFrame(
        data, columns='time open high low close volume a b c d e f'.split())
    return df.astype({'time': 'datetime64[ms]', 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})


# reduce to [15, 5, 1] minutes to increase accuracy
df = download_price_history(
    interval_mins=30, start_time='2022-11-1', end_time='2022-11-2')
# print(df.head())

#np.histogram(df, weights=volume)
#df = df[start_time:]
df2 = df.groupby(pd.cut(df.close, bins=20)).sum()

print(df2.head())

#plt.plot(df.time, df.close, legend='Price')
#plt.plot(df.time, df2.a, style='--', legend='VWAP')
#plt.horiz_time_volume(time_volume_profile, draw_va=0.7, draw_poc=1.0)
# plt.show()
