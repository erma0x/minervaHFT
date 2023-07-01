from binance.spot import Spot

client = Spot()

print(client.time())

api_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

with open("keyfile.key", 'rb') as f:
    private_key = f.read()

client = Spot(api_key=api_key, private_key=private_key)
print(client.account())
print('-'*100)
print(client.account_status())
print('-'*100)
print(client.account_snapshot("SPOT"))
print(client.exchange_info())
print(client.api_trading_status())
print(client.time())
print(client.user_asset()[0]['free'])
