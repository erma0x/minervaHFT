from binance.spot import Spot
import time

client = Spot()

print(client.time())

api_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

with open("keyfile.key", 'rb') as f:
    private_key = f.read()

client = Spot(api_key=api_key, private_key=private_key)
print('-'*100)
print(client.user_asset(asset='ETH'))#[0]['free'])


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
#client = Spot(api_key=api_key, private_key=private_key)

if client.user_asset(asset='ETH'):
    
    # SE L"ORDINE E' STATO FILLATO
    #if client.get_open_orders()[0]["clientOrderId"] == "1":
        params = {
            'symbol': 'ETHUSDT',
            'side': 'SELL',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': 0.01,
            'price': 1909,
            'newClientOrderId':'1',
        }
        response = client.new_order(**params)