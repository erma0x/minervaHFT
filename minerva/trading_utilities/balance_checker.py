import os
import time
import datetime
from binance.spot import Spot
from minerva.trader import check_balance, get_keys

if __name__ == "__main__":
    api_key, private_key = get_keys(name_account='lorenzo')
    client = Spot( api_key = api_key , private_key = private_key)

    while True:
        balance = check_balance( client = client, ticker = "USDT",balance_type='free' )
        
        os.system('clear')
        print(f"\n\t Your USDT free balance is: {balance}")
        print(f"\n\t {str(datetime.datetime.now())[:22]}")
        
        time.sleep(0.8)
    
