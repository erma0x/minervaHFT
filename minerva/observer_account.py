import os
import time
from binance.client import Client
from trader import check_balance


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
    THERORETICAL_FITNESS = get_finess_strategy()

    while True:
        # get starting time
        DAYS_OF_TRADING = 1
        INITIAL_EQUITY = 100

        ticker = "ETH"
        assets = get_full_binance_balance()
        GAIN_24H_PERCENTAGE = round((-INITIAL_EQUITY)/INITIAL_EQUITY*100/DAYS_OF_TRADING ,4)

        EMPIRICAL_FITNESS = GAIN_24H_PERCENTAGE

        os.system('clear')
        print(f'\nTHERORETICAL_FITNESS                         {THERORETICAL_FITNESS}')
        print(f'EMPIRICAL_FITNESS                              {EMPIRICAL_FITNESS}')
        print(f'theoretical% shift (theoretical - empirical)   {THERORETICAL_FITNESS - EMPIRICAL_FITNESS}')
        print(f'open positions                                 {} ')
        time.sleep(1)

# controlla in live la fitness del file e la fintess del account reale
# da questo capisci de il sistema funziona o devi incrementare le fees od altro
# controlla anche per un effettiva conferma fra fitness REAL e fitness TEORICA
