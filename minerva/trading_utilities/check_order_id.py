from minerva.trader import get_keys, get_full_binance_balance
from binance.spot import Spot

api_key, private_key = get_keys('lorenzo')

client = Spot( api_key = api_key , private_key = private_key)

TICKER = "ETHUSDT"

print(client.get_order(symbol=TICKER,orderId=6509186086))
print('-'*100)
#print(client.deposit_history())