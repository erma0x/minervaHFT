import json
import time
import os
from pathlib import Path
from utils.get_orderbook import get_orderbook

if __name__ == '__main__':
    filepath_orderbook_json = Path("orderbook.json")
    mode = '+a' if os.path.exists(filepath_orderbook_json) else '+w'
    MARKET = 'BTCUSDT'
    REQUEST_TIME_INTERVAL = 0.4 # seconds (binance)
    #while True:
    ID_DATA=0
    with open(f"orderbook_{MARKET}.json", "r+") as data_file:
        orderbook = get_orderbook(MARKET) 
        file_data = json.load(data_file)
        #ID_DATA+=1
        #file_data['lastUpdateId'].append(orderbook)
        #file_data.seek(0)
              
        # output -> dict
        # keys lastUpdateId, asks, bids
        # "lastUpdateId": 28168355605, "bids": [[16541.5, 0.001],...], "asks": [[16541.5, 0.001],...]
#        file_data.update(orderbook, data_file)

        json.dumps(orderbook, data_file)
        time.sleep(REQUEST_TIME_INTERVAL)