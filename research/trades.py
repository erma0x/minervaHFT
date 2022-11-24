import requests
from pprint import pprint
resp = requests.get('https://api.binance.us/api/v3/aggTrades?symbol=LTCBTC')
print(resp.json())