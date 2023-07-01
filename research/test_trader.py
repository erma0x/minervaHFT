from binance.spot import Spot
from trader import trader_spot, get_keys
import time
import binance

api_key, private_key = get_keys(name_account='lorenzo')

client = Spot(api_key=api_key, private_key=private_key)

params = {
    'symbol': 'ETHUSDT',
    'side': 'BUY',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.01,
    'price': 2101.52,
    'newClientOrderId':'1',
}
response = client.new_order(**params)


time.sleep(5)

client = Spot(api_key=api_key, private_key=private_key)

try:
    response = client.cancel_order(symbol='ETHUSDT',origClientOrderId='1')

except binance.error.ClientError:
    params = {
        'symbol': 'ETHUSDT',
        'side': "SELL",
        'type': "MARKET",
        'quantity': 0.01,
    }
    response = client.new_order(**params)

finally:
    print(response)

print(f'response {response}')
print('-'*100)
