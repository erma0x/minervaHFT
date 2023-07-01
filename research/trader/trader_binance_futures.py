from binance.client import Client
from binance.exceptions import BinanceAPIException

def binance_trader(trading_operation, api_key, api_secret):
    # Check if the trading operation has all the necessary parameters
    if not all(key in trading_operation for key in ['symbol', 'side', 'leverage', 'buy', 'sell', 'stoploss']):
        raise ValueError('Missing parameters in the trading operation')

    client = Client(api_key, api_secret)

    # Set the leverage
    try:
        client.futures_change_leverage(symbol=trading_operation['symbol'], leverage=trading_operation['leverage'])
    except BinanceAPIException as e:
        print(e)
        return False

    # Place the buy order
    try:
        buy_order = client.futures_create_order(
            symbol=trading_operation['symbol'],
            side=trading_operation['side'].upper(),
            type=Client.ORDER_TYPE_MARKET,
            quantity=trading_operation['buy'][0]
        )
    except BinanceAPIException as e:
        print(e)
        return False

    # Place the sell order
    try:
        sell_order = client.futures_create_order(
            symbol=trading_operation['symbol'],
            side=trading_operation['side'].upper(),
            type=Client.ORDER_TYPE_MARKET,
            quantity=trading_operation['sell'][0]
        )
    except BinanceAPIException as e:
        print(e)
        return False

    # Place the stop loss order
    try:
        stop_loss_order = client.futures_create_order(
            symbol=trading_operation['symbol'],
            side='SELL' if trading_operation['side'].upper() == 'LONG' else 'BUY',
            type=Client.ORDER_TYPE_STOP_MARKET,
            stopPrice=trading_operation['stoploss'][0],
            quantity=trading_operation['sell'][0]
        )
    except BinanceAPIException as e:
        print(e)
        return False

    return (buy_order, sell_order, stop_loss_order)