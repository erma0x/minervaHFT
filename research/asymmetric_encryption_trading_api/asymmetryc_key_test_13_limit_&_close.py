from binance.spot import Spot

client = Spot()
print(client.time())

api_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

with open("keyfile.key", 'rb') as f:
    private_key = f.read()

client = Spot(api_key=api_key, private_key=private_key)
print('-'*100)
print(client.user_asset()[0]['free'])


#Post a new order
params = {
    'symbol': 'ETHUSDT',
    'side': 'BUY',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.01,
    'price': 1800,
    'newClientOrderId':'1',
}


# 1900
response = client.new_order(**params)
print('NEW ORDER')
print(response)
print('-'*100)
print('OPEN ORDERS')
print(client.get_open_orders())

import time
time.sleep(15)

params = {
    'symbol': 'ETHUSDT',
    'side': "SELL",
    'type': "MARKET",
    'quantity': 0.01,
    'price': 1800,
    'newClientOrderId':'1',
}

client = Spot(api_key=api_key, private_key=private_key)
#response = client.cancel_open_orders(symbol='ETHUSDT')
response = client.cancel_order(symbol='ETHUSDT',origClientOrderId='1')

print('-'*100)
print(f'response {response}')
