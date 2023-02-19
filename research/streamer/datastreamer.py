import os
import json
import websocket
from database_utils import orderbook_storage, create_database
from configuration_backtest import ORDERBOOK_DATABASE, WEBSOCKET_ORDERBOOK_BINANCE

def on_open(ws):
    print("orderbook streamer [OPEN]")
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params":
        ["btcusdt@depth"], #,"btcusdt@trade"],
         "id": 1
         }

    ws.send(json.dumps(subscribe_message))

def on_message(ws, message):
    orderbook_storage(ask=json.loads(message)['a'],bid=json.loads(message)['b'],database_path=ORDERBOOK_DATABASE)

def on_close(ws):
    print("closed connection")        

if not os.path.isfile(ORDERBOOK_DATABASE):
    create_database(ORDERBOOK_DATABASE)

ws = websocket.WebSocketApp(WEBSOCKET_ORDERBOOK_BINANCE, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()

