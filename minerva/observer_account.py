import os
import time
from binance.client import Client

def get_full_binance_balance(api_key, api_secret):
    client = Client(api_key, api_secret)
    account_info = client.get_account()
    balances = {}
    for entry in account_info['balances']:
        asset = entry['asset']
        balances[asset] = {}
        balances[asset]['free'] = float(entry['free'])
        balances[asset]['locked'] = float(entry['locked'])
    return balances

def get_free_usdt_balance(api_key, api_secret):
    client = Client(api_key, api_secret)
    account_info = client.get_account()
    balances = account_info['balances']
    for balance in balances:
        if balance['asset'] == 'USDT':
            return float(balance['free'])
    return 0.0

"""
usdt_free = balances['USDT']['free']
usdt_locked = balances['USDT']['locked']
btc_free = balances['BTC']['free']
btc_locked = balances['BTC']['locked']
"""

if __name__ == '__main__':
    while True:
        # get starting time
        DAYS_OF_TRADING = 1
        INITIAL_EQUITY = 100
        GAIN_24H_PERCENTAGE = round((get_full_binance_balance()-INITIAL_EQUITY)/INITIAL_EQUITY*100/DAYS_OF_TRADING ,4)

        EMPIRICAL_FITNESS = GAIN_24H_PERCENTAGE
        THERORETICAL_FITNESS = get_finess_strategy()

        os.system('clear')
        print(f'\nTHERORETICAL_FITNESS                    {THERORETICAL_FITNESS}')
        print(f'EMPIRICAL_FITNESS                       {EMPIRICAL_FITNESS}')
        print(f'gain% shift (theoretical - empirical)   {THERORETICAL_FITNESS - EMPIRICAL_FITNESS}')

        time.sleep(1)

# controlla in live la fitness del file e la fintess del account reale
# da questo capisci de il sistema funziona o devi incrementare le fees od altro
# controlla anche per un effettiva conferma fra fitness REAL e fitness TEORICA
