from binance.spot import Spot
import time
from timeit import default_timer
from trader import ritiro, withdraw

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
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.01,
    'price': 1905,
    'newClientOrderId':'1',
}


# 1900
print('NEW ORDER')
response = client.new_order(**params)
start = default_timer()

#print(response)
print('-'*100)
print('OPEN ORDERS')
print(client.get_open_orders())
ENTRY_ORDER_NOT_FILLED = True
#client = Spot(api_key=api_key, private_key=private_key)

# entra a limite
# se ci sono ordini aperti ed il prezzo e' arrivato a questa cifra vendi a mercato
# oppure se e' passato troppo tempo

print("wait to sell")

while ENTRY_ORDER_NOT_FILLED:
    time.sleep(0.41)
    
    # IF ORDER ID FILLED
    if not client.get_open_orders():

        ENTRY_ORDER_NOT_FILLED = False
        duration = default_timer() - start
        print(duration) 
        
                             # Please use WebSocket Streams for live updates to avoid polling the API
        if duration > 10.0 : #or float(client.ticker_price('ETHUSDT')["price"]) > 1910.0:
        # SE L"ORDINE E' STATO FILLATO
        #if client.get_open_orders()[0]["clientOrderId"] == "1":
            params = {
                'symbol': 'ETHUSDT',
                'side': 'SELL',
                'type': 'MARKET',
                'quantity': 0.01,
                'newClientOrderId':'1',
            }

            response = client.new_order(**params)