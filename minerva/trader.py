from binance.spot import Spot
import time
from timeit import default_timer


def withdraw_token(ticker='USDT'):
    print(f'ASSET {client.user_asset( asset = ticker )} {ticker}')
    if client.user_asset( asset = ticker ):
        withdraw_qnt = float(client.user_asset(asset=ticker)[0]['free']) - 100.0 #
        if withdraw_qnt > 5:
            print(f"Ritirare {withdraw_qnt} {ticker}")
            #client.withdraw(coin=ticker,amount=withdraw_qnt,address=ADDRESS_WITHDRAW)

        else:
            print('Continua')

def get_all_assets(client):
    assets = client.user_asset()
    balances = {'ETH':0,'USDT':0}
    for asset in assets:
        balances[asset['asset']] = float(asset['free'])+float(asset['locked'])
    return balances

def check_balance(client,ticker="ETH",balance_type='free'):
    try:
        balance_ticker = client.user_asset(asset=ticker)
    except:
        print(f'Error: could not check your {ticker} balance')
        return -1 

    try:
        return balance_ticker[0][balance_type]
    except:
        return 0

def get_full_binance_balance(api_key, api_secret,ticker):
    client = Spot( api_key = api_key , private_key = private_key)
    account_info = client.user_asset(asset=ticker)
    balances = {}
    for entry in account_info['balances']:
        asset = entry['asset']
        balances[asset] = {}
        balances[asset]['free'] = float(entry['free'])
        balances[asset]['locked'] = float(entry['locked'])
    return balances


def trader_spot(trading_operation, client):
    if trading_operation['type'] == 'MARKET':
        params = {
            'symbol': trading_operation['symbol'],
            'side': trading_operation['side'],
            'type': trading_operation['type'],
            'quantity': trading_operation['quantity'],
            'newClientOrderId':trading_operation['id'],
        }

    elif trading_operation['type'] == 'LIMIT':
        params = {
            'symbol': trading_operation['symbol'],
            'side': trading_operation['side'],
            'type': trading_operation['type'],
            'timeInForce': 'GTC',
            'quantity': trading_operation['quantity'],
            'price': trading_operation['price'],
            'newClientOrderId':trading_operation['id'],
        }

    else:
        print("Error: LIMIT or MARKET not fount trading in operation parameters")
        params = {}

    try:
        response = client.new_order(**params)
    except:
        print(f'Error: could not trade with this trading parameters')
        response = None

    return response

def get_keys(name_account):
    with open(f"minerva/keys/{name_account}_small.pub", 'rb') as f:
        api_key = f.read()

    with open(f"minerva/keys/{name_account}.key", 'rb') as f:
        private_key = f.read()

    return api_key, private_key

if __name__ == "__main__":
    
    # ADDRESS_WITHDRAW = "DSKAKPOKSAD"

    api_key, private_key = get_keys('lorenzo')

    client = Spot( api_key = api_key , private_key = private_key)
    
    trading_operation = {
            'symbol': "ETHUSDT",
            'side': "BUY",
            'type': "MARKET",
            'quantity': 0.01,
            'id':"1",
        }
    
    ack = trader_spot(trading_operation = trading_operation, client = client)
    #print(ack)
    print(f"USDT free       {check_balance(ticker='USDT',client=client,balance_type='free')}")
    print(f"USDT locked     {check_balance(ticker='USDT',client=client,balance_type='locked')}")

    trading_operation = {
        'symbol': "ETHUSDT",
        'side': "SELL",
        'type': "MARKET",
        'quantity': 0.01,
        'id':"1",
    }

    ack = trader_spot(trading_operation = trading_operation, client = client)
    #print(ack)

    print(f"free ETH is {check_balance(ticker='ETH',client=client,balance_type='free')}")
    print(f"lock ETH is {check_balance(ticker='ETH',client=client,balance_type='locked')}")
    print(f"free USDT is {check_balance(ticker='USDT',client=client,balance_type='free')}")
    print(f"lock USDT is {check_balance(ticker='USDT',client=client,balance_type='locked')}")

    #withdraw_token("USDT",ADDRESS)