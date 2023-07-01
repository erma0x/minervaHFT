from binance.client import Client
from binance.exceptions import BinanceAPIException

def binance_trader_spot(trading_operation, api_key, api_secret):
    """
    Esegue un'operazione di trading sulla piattaforma Binance.

    Args:
        trading_operation (dict): Dizionario contenente le informazioni sull'operazione di trading da eseguire.
        api_key (str): Chiave API fornita da Binance.
        api_secret (str): Chiave segreta API fornita da Binance.

    Returns:
        dict: Dizionario contenente le informazioni sull'operazione di trading eseguita, incluse le informazioni
        sul prezzo di acquisto, prezzo di vendita e prezzo di stop loss.
    """

    # Connessione all'API di Binance
    client = Client(api_key, api_secret)

    # Esecuzione dell'operazione di trading
    try:
        symbol = trading_operation['symbol']
        entry_price = trading_operation['entry'][0]
        take_profit_price = trading_operation['takeprofit'][0]
        stop_loss_price = trading_operation['stoploss'][0]
        token_quantity = trading_operation['qnt'][0]

        if 'entry' in trading_operation:
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=token_quantity,
                price=entry_price
            )

        if 'takeprofit' in trading_operation:
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=token_quantity,
                price=take_profit_price
            )

        if 'stoploss' in trading_operation:
            order = client.create_oco_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                quantity=token_quantity,
                price=stop_loss_price,
                stopPrice=stop_loss_price,
                stopLimitPrice=stop_loss_price
            )

        return True

    except BinanceAPIException as e:
        return None


if __name__ == '__main__':
    OPERATION = {
        'symbol':'DOGEUSDT',
        'qnt':100,
        'buy': [20000],
        'sell':[21000],
        'stoploss':[19000] } 

    API_KEY = ''
    API_SECRET = ''

    binance_trader_spot( trading_operation = OPERATION, api_key = API_KEY, api_secret = API_SECRET )