import zmq
from datetime import datetime
from configuration_trading import *
import json
import asyncio
import websockets
import argparse

async def call_api(socket):
    msg = {"method": "SUBSCRIBE", "params":
            [
            f"{TICKER.lower()+BASE_CURRENCY.lower()}@depth" # btcusdt@depth
            ],
            "id": 1
            }
    async with websockets.connect('wss://stream.binance.com:9443/ws/'+TICKER.lower()+BASE_CURRENCY.lower()+'@depth') as ws:
        while True:
            await ws.send(json.dumps(msg))
            response = await asyncio.wait_for(ws.recv(), timeout=2)
            response = json.loads(response)
            try:
                ask = response["a"]
                bid = response["b"]
            except:
                ask = None
                bid = None
            finally:
                timestamp = datetime.now()
                datapoint_orderbook = str(timestamp)[:19]+'|'+str(ask)+'|'+str(bid)
                print(datapoint_orderbook)
                socket.send(bytes(datapoint_orderbook.encode('utf-8')))

            await asyncio.sleep(0.41)


parser = argparse.ArgumentParser(description='Set bind link for consumer')
parser.add_argument('--link', dest='link', default="5550",
                    help='Set bind link for consumer (default: "5550")')
args = parser.parse_args()

context = zmq.Context()
destination_socket = context.socket(zmq.PUSH)
destination_socket.connect(f"tcp://localhost:{args.link}")
#destination_socket = context.socket(zmq.PUSH)
#destination_socket.connect("tcp://localhost:5560")

while True:
    asyncio.get_event_loop().run_until_complete(call_api(socket=destination_socket))