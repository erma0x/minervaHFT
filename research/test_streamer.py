#!/usr/bin/env python3

from binance.client import Client
import json

# Create a Binance websocket client:
client = Client()

# Set up the subscription:
symbol = "btcusdt"
depth = 5  # Number of levels to return for each bid/ask side
stream_name = f"{symbol}@depth{depth}"
stream_url = f"wss://stream.binance.com:9443/ws/{stream_name}"

# Define a callback function to process messages:
def process_message(message):
    # Parse message as JSON:
    message_json = json.loads(message)

    # Check if message is an update to the order book:
    if "e" in message_json and message_json["e"] == "depthUpdate":
        # Extract the bid and ask prices and quantities:
        bids = message_json["b"]  # List of [price, quantity] pairs for bids
        asks = message_json["a"]  # List of [price, quantity] pairs for asks

        # Print the current order book:
        print(f"ORDER BOOK FOR {symbol.upper()}:")
        print("Bids:")
        for i, bid in enumerate(bids):
            price, quantity = bid
            print(f"  {i+1}. Price: {price:.2f}, Quantity: {quantity:.6f}")
        print("Asks:")
        for i, ask in enumerate(asks):
            price, quantity = ask
            print(f"  {i+1}. Price: {price:.2f}, Quantity: {quantity:.6f}")
        print("-" * 30)

client.s(callback=process_message, symbol=symbol, depth=depth)

# Keep the program running indefinitely:
client.loop_forever()
