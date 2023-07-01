from trader import get_keys, get_full_binance_balance
from binance.spot import Spot
from pprint import pprint
import time
import datetime
import os
from colorama import Fore, Back, Style
from trader import get_all_assets

if __name__ == "__main__":

    api_key, private_key = get_keys('lorenzo')
    client = Spot( api_key = api_key , private_key = private_key)

    while True:
        assets = get_all_assets(client=client)
        open_positions = client.get_open_orders()
        
        THEORETHICAL_FITNESS = 0.02
        EMPIRICAL = 0.015
        os.system('clear')
        print(f'\n\t{Fore.GREEN}░▒▓▆▅▃▂▁ 𝐁𝐚𝐥𝐚𝐧𝐜𝐞 𝐎𝐛𝐬𝐞𝐫𝐯𝐞𝐫 ▁▂▃▅▆▓▒░')
        print(f'\t\t{str(datetime.datetime.now())[:21]} {Style.RESET_ALL}')
        print(f"\n\t💵 USDT {assets['USDT']}")
        print(f"\t🪙  ETH  {assets['ETH']}")
        print(f"\n\t empirical \t%/24h {EMPIRICAL}")            # (balance usdt - initial usdt / initial usdt )*100 / num days
        print(f"\t theoretical \t%/24h {THEORETHICAL_FITNESS}") # from the fitness file with backtesting data
        print(f"""{Fore.BLUE}
    open orders    
------------------------------------------------{Style.RESET_ALL}
""")
        pprint(open_positions)
        #print(client.get_order(symbol=TICKER,orderId=6509186086))
        time.sleep(2)