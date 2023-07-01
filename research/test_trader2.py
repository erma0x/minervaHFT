import websocket
import json

# Define the websocket URL and the subscription request:
ws_url = "wss://stream.binance.com:9443"
#ws_url = "wss://ws-api.binance.com:443/ws-api/v3"
#ws_url = "wss://ws-api.binance.com:443/"

subscription_request = {
    "method": "SUBSCRIBE",
    "params": [
        "ethusdt@depth"
    ],
    "id": 1
}

# Define a callback function to process messages:
def on_message(ws, message):
    # Parse the message as JSON:
    message_json = json.loads(message)

    # Check if message is an update to the order book:
    if "e" in message_json and message_json["e"] == "depthUpdate":
        # Extract the bid and ask prices and quantities:
        bids = message_json["b"]  # List of [price, quantity] pairs for bids
        asks = message_json["a"]  # List of [price, quantity] pairs for asks

        # Print the current order book:
        print("ORDER BOOK FOR BTCUSDT:")
        print("Bids:")
        for i, bid in enumerate(bids):
            price, quantity = bid
            print(f"  {i+1}. Price: {price:.2f}, Quantity: {quantity:.6f}")
        print("Asks:")
        for i, ask in enumerate(asks):
            price, quantity = ask
            print(f"  {i+1}. Price: {price:.2f}, Quantity: {quantity:.6f}")
        print("-" * 30)

ws = websocket.WebSocketApp(ws_url, on_message=on_message)
ws.on_open = lambda _: ws.send(json.dumps(subscription_request))

ws.run_forever()