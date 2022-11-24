MARKET = "BTCUSDT"
REQUEST_TIME_INTERVAL = 0.4
LIMIT_KLINES = 50
N_TICKS_VIZUALIZER = 100
TOPICS_DATASTRAMER = ["orderbook", "price"]  # ,"klines"]
TOPICS_ORACLE = ["trade"]

DATASTREAMER_URL = "ipc://127.0.0.1:5678"
ORACLE_URL = "ipc://127.0.0.1:5679"
BINANCE_KLINES_HEADER = ["start_time", "Open", "High", "Low", "Close", "Volume", "end_time", "quote_asset_volume", "numbers_of_trades",
                         "taker_buy_base_asset_volume", "ignore", "taker_sell_base_asset_volume", "maker_sell_base_asset_volume", "maker_buy_base_asset_volume"]

TRADING_OPERATION = {"side": "",  # string LONG/SHORT
                     "symbol": "",  # string BTCUSDT/ETH-PERP/...
                     "take_profits": [],  # floats "30", "31"
                     "entry_prices": [],  # floats "29", "28"
                     "stop_losses": [],  # floats "23", "24"
                     "laverage": ""}  # int "2"/"5"/"10"/"20"/"50"/"100"

EXAMPLE_TRADING_OPERATION = {"side": "LONG",
                             "symbol": "BTCUSDT",
                             "take_profits": ["21000", "21020", "21030"],
                             "entry_prices": ["20900", "20800"],
                             "stop_losses": ["20700", "20600"],
                             "laverage": "10"}
