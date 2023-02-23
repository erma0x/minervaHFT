#!/usr/bin/env python3
from datetime import datetime
import sys, os
ROOT_PATH = sys.path[0]


experiment_number = 0
EXPERIMENT_FOLDER = ROOT_PATH+f'/runs/experiment_{experiment_number}/'

while os.path.exists(EXPERIMENT_FOLDER):
    experiment_number+=1
    EXPERIMENT_FOLDER = ROOT_PATH+f'/runs/experiment_{experiment_number}/'


STRATEGIES_FOLDER = ROOT_PATH+f'/runs/experiment_{experiment_number}/generation_0/'
while os.path.exists(STRATEGIES_FOLDER):
    experiment_number+=1
    STRATEGIES_FOLDER = ROOT_PATH+f'/runs/experiment_{experiment_number}/generation_0/'

#TEST_STRATEGY_FOLDER = ROOT_PATH+f'/tests/runs/experiment_{experiment_number}/generation_0/'

EXPERIMENT_NUMBER = 0

# STREAMER
SAVE_LIVE_DATA_IN_SQL = False
BACKTEST_MODE = True
PRINT_TIMESTAMP = True

ALLOW_LONG_OPERATIONS = True
ALLOW_SHORT_OPERATIONS = False


# SAVE LIVE DATA IN THIS FILE
SQL_DB_TIME = 13 # 10 days # 13 hours # 16 minutes
ORDERBOOK_DATABASE = f"orderbook_{str(datetime.now())[:SQL_DB_TIME].replace(' ','_')}.db" # hours

# BACKTESTING MODE DATABASE PATH
BACKTEST_ORDERBOOK_DATABASE = ROOT_PATH+f'/databases/orderbook.db'
ORDERBOOK_BACKTESTING_FOLDER = ROOT_PATH+f'/databases/backtesting/'


counter_live_datapoints = 0

# ORACLE Trading algorithm 
PRINT_ANY_DATA = False
PRINT_BASIC_DATA = False 
PRINT_ALGORITHM = False
PLOT_DATA = False


INITIAL_CAPITAL =  10_000
EQUITY = INITIAL_CAPITAL
REQUEST_TIME_INTERVAL = 0.4
LEVERAGE = 1

# PERPETUAL CONTRACT KUCOINFUTURES FEE STRUCTURE
TAKER_FEES = 0.0006 # (0,1) % 
MAKER_FEES = 0.0002 # (0,1) %

# TIMING without visualizer 0.8 / 1.6 seconds
# TIMING with    visualizer 2.3 / 3.0 seconds
STRATEGY_FOLDER = ROOT_PATH+'/strategies/'

WEBSOCKET_ORDERBOOK_BINANCE = 'wss://stream.binance.com:9443/ws'
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
