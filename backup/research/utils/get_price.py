import requests
from datetime import datetime

def get_full_price(market='BTCUSDT'):
    """
    input:
    market: [string] example of market 'BTCUSDT'
    
    output:
    klines: [list] 

    """
    price = get_price(market_=market, tick_interval='1m')

    taker_buy_base_asset_volume = float(price[7])
    total_volume = float(price[0])

    maker_sell_base_asset_volume = taker_buy_base_asset_volume
    taker_sell_base_asset_volume = total_volume - taker_buy_base_asset_volume
    maker_buy_base_asset_volume = taker_sell_base_asset_volume

    price.append(taker_sell_base_asset_volume)
    price.append(maker_sell_base_asset_volume)
    price.append(maker_buy_base_asset_volume)

    current_time = str(datetime.datetime.now())[:-7]
    price.insert(0, current_time)

    row = str(price).replace('[', '').replace(']', '').replace("'", "")

    return row

def get_instant_price(market_='BTCUSDT'):
    url = 'https://api.binance.com/api/v3/ticker/price?symbol='+market_
    data = requests.get(url).json()
    return data


def get_price(market_='BTCUSDT', tick_interval='1m'):
    url = 'https://api.binance.com/api/v3/klines?symbol=' + \
        market_+'&interval='+tick_interval+'&limit=1'
    data = requests.get(url).json()
    return data[0]