import zmq
import time
import argparse
from datetime import datetime
import json
import asyncio
import websockets

TICKER ="ETH"
BASE_CURRENCY="USDT"

async def call_api():
    parser = argparse.ArgumentParser(description='Set bind link for consumer')
    parser.add_argument('--link', dest='link', default="5550",
                        help='Set bind link for consumer (default: "5550")')
    args = parser.parse_args()

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
                message = {'timestamp':str(timestamp)[:19],'data':{'a':ask,'b':bid}}
                
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect(f"tcp://localhost:{args.link}")
                socket.send_json(message)
                response = socket.recv_json()
                print(response)

            await asyncio.sleep(0.41)



#destination_socket = context.socket(zmq.PUSH)
#destination_socket.connect("tcp://localhost:5560")

while True:
    asyncio.get_event_loop().run_until_complete(call_api())

