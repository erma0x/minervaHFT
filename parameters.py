MARKET = 'BTCUSDT'
DATA_FILE_NAME = f'{MARKET}.csv'

REQUEST_TIME_INTERVAL = 0.1
LIMIT_KLINES = 50
N_TICKS_VIZUALIZER = 100
RUNNING = True

TOPICS_DATASTRAMER = ['orderbook', 'price']#,'klines']
DATASTREAMER_URL = 'ipc://127.0.0.1:5678'

TOPICS_ORACLE = ['trade']
ORACLE_URL = 'ipc://127.0.0.1:5679'

yheader = ['start_time','Open','High','Low','Close','Volume','end_time','quote_asset_volume','numbers_of_trades','taker_buy_base_asset_volume','ignore','taker_sell_base_asset_volume','maker_sell_base_asset_volume','maker_buy_base_asset_volume']

TRADING_OPERATION = {'side':'',
                        'symbol':'',
                        'take_profits':[],
                        'entry_prices':[],
                        'stop_losses':[],
                        'laverage':1 }

# EXAMPLE                        
EXAMPLE_TRADING_OPERATION = {'side': 'buy',
                            'symbol': 'ETH-PERP',
                            'take_profits': ['21000', '21020','21030'],
                            'entry_prices': ['20900', '20800'], 
                            'stop_losses': ['20700','20600'],
                            'laverage': 10}
