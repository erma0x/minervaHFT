import asyncio
import websockets
import json

msg = {"method": "SUBSCRIBE", "params":
        [
        "btcusdt@depth"
        ],
        "id": 1
        }

async def call_api():
    async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@depth') as ws:
        while True:
            await ws.send(json.dumps(msg))
            response = await asyncio.wait_for(ws.recv(), timeout=2)
            response = json.loads(response)
            print(f"response ==> {response}")
            await asyncio.sleep(0.41)

asyncio.get_event_loop().run_until_complete(call_api())