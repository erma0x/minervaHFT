
import os,sys
import time
from binance.spot import Spot
from trader import get_keys,get_all_assets
from configuration_trading import ETH_ROUND_NUMBER, MARKET
import math
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))


def cancel_all_open_orders(apy_key_, api_secret_):
    client = Spot(api_key=apy_key_, private_key=api_secret_)
    if client.get_open_orders():
        response = client.cancel_open_orders(symbol=TICKER+BASE_CURRENCY)
        print(f"Canceling open orders on {TICKER}")
        return response

def sell_all_tokens(_apy_key, _api_secret):
    client = Spot(api_key=_apy_key, private_key=_api_secret)
    assets = get_all_assets(client=client)

    token_quantity = round(assets[TICKER]*0.98,ETH_ROUND_NUMBER+2) 
    if token_quantity:
        params = {
            'symbol': MARKET,
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': token_quantity,
        }
        print(params)
        response = client.new_order(**params)
        print('All token are in market sell orders')
        return response
    else:
        print('No token founded')
        return 0

def reset_account(api_key, api_secret):
    cancel_all_open_orders(api_key,api_secret)
    time.sleep(2)
    sell_all_tokens(api_key,api_secret)

if __name__ == "__main__":
    # reset token quantity in USDT
    TICKER = "ETH"
    BASE_CURRENCY = "USDT"
    api_key, private_key = get_keys( name_account = "lorenzo" )
    reset_account(api_key, private_key)
