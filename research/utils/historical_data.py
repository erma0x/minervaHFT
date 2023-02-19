import dateutil
import pytz
import requests
import pandas as pd

def utc2timestamp(s): 
    return int(dateutil.parser.parse(s).replace(tzinfo=pytz.utc).timestamp() * 1000)


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

        url = 'https://api.binance.us/api/v3/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (
            interval_str, LIMIT_KLINES, symbol, start_t, end_t)
        d = requests.get(url).json()
        data += d

    df = pd.DataFrame(
        data, columns='time Open High Low Close Volume a b c d e f'.split())
    return df
    # return df.astype({'time':'datetime64[ms]', 'Open':float, 'High':float, 'Low':float, 'Close':float, 'Volume':float})

