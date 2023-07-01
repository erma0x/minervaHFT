from binance.spot import Spot

client = Spot()

print(client.time())

api_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

with open("keyfile.key", 'rb') as f:
    private_key = f.read()

client = Spot(api_key=api_key, private_key=private_key)
print('-'*100)
print(client.user_asset()[0]['free'])


params = {
    'symbol': 'ETHUSDT',
    'side': 'BUY',
    'type': 'MARKET',
    'quantity': 0.01,
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
    'quantity': 0.011,
}

client = Spot(api_key=api_key, private_key=private_key)
response = client.new_order(**params)


print('-'*100)
print(f'response {response}')
