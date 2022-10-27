import sys
MARKET = 'BTCUSDT'
DATA_FILE_NAME = f'{MARKET}.csv'
REQUEST_TIME_INTERVAL = 0.4
N_TICKS_VIZUALIZER = 10
ORACLE_LINK = 'ipc://127.0.0.1:5678'

header = ['start_time','Open','High','Low','Close','Volume','end_time','quote_asset_volume','numbers_of_trades','taker_buy_base_asset_volume','ignore','taker_sell_base_asset_volume','maker_sell_base_asset_volume','maker_buy_base_asset_volume']

base_operation_data_structure = {'side':'',
                        'symbol':'',
                        'take_profits':[],
                        'entry_prices':[],
                        'stop_losses':[],
                        'laverage':10 }
                        
# {'side': 'buy',
#  'symbol': 'ETH-PERP',
#  'take_profits': ['3400', '3300','3200'],
#  'entry_prices': ['2900', '3000'], 
# 'stop_losses': ['2000','1900'],
# 'laverage': 10}
