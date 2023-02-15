#!/usr/bin/env python3
# STREAMER
SAVE_LIVE_DATA_IN_SQL = False
BACKTEST_MODE = True
ORDERBOOK_DATABASE = f'orderbook_small.db'
counter_live_datapoints = 0

# ORACLE Trading algorithm 
PRINT_ANY_DATA = False
PRINT_BASIC_DATA = False 
PRINT_ALGORITHM = False
PLOT_DATA = False

import sys
INITIAL_CAPITAL =  10_000
EQUITY = INITIAL_CAPITAL
REQUEST_TIME_INTERVAL = 0.4
LEVERAGE = 10
# PERPETUAL CONTRACT KUCOINFUTURES FEE STRUCTURE
TAKER_FEES = 0.0006 # (0,1) % 
MAKER_FEES = 0.0002 # (0,1) %

# TIMING without visualizer 0.8 / 1.6 seconds
# TIMING with    visualizer 2.3 / 3.0 seconds
ROOT_PATH = sys.path[0]
STRATEGY_FOLDER = ROOT_PATH+'/strategies/'

WEBSOCKET_ORDERBOOK_BINANCE = 'wss://stream.binance.com:9443/ws'
MOCK_ORDERBOOK_DATABASE_PATH = ROOT_PATH+f"/orderbook.db"
DATASTREAMER_URL = "ipc://127.0.0.1:5678"
ORACLE_URL = "ipc://127.0.0.1:5679"
TRADING_OPERATION = {}
EQUITY_ARRAY = []
TRADE_ORDERBOOK = {}
TRADE_ID = 0
UNREALIZED_PNL = 0
REALIZED_PNL = 0
TRADING_OPERATION = {"side": "",  # string LONG/SHORT
                     "symbol": "",  # string BTCUSDT/ETH-PERP/...
                     "take_profits": [],  # floats "30", "31"
                     "entry_prices": [],  # floats "29", "28"
                     "stop_losses": [],  # floats "23", "24"
                     "laverage": ""}  # int "2"/"5"/"10"/"20"/"50"/"100"

# EXAMPLE_TRADING_OPERATION = {"side": "LONG",
#                              "symbol": "BTCUSDT",
#                              "take_profits": ["21000", "21020", "21030"],
#                              "entry_prices": ["20900", "20800"],
#                              "stop_losses": ["20700", "20600"],
#                              "laverage": "10"}

# BINANCE_KLINES_HEADER = ["start_time", "Open", "High", "Low", "Close", "Volume", "end_time", "quote_asset_volume", "numbers_of_trades",
#                          "taker_buy_base_asset_volume", "ignore", "taker_sell_base_asset_volume", "maker_sell_base_asset_volume", "maker_buy_base_asset_volume"]
