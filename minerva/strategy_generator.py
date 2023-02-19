import random
import os
from configuration_strategy import *
from configuration_backtest import STRATEGIES_FOLDER

def strategy_generator(strategies_folder):
    """
    STRATEGY FILE GENERATOR

    MARKET = 'BTCUSDT'
    LIMIT_ORDER_BOOK =  500
    RELATIVE_THRESHOLD_DIV = 10 # int (2,100) "relative operative trading THRESHOLD refered to : max_local_volume/relative_THRESHOLD "
    THRESHOLD_SHORT = 0.63
    THRESHOLD_LONG = 0.37
    MAX_CONCURRENT_OPEN_TRADES = 6
    MAX_SECONDS_TRADE_OPEN = 360
    PEAK_DISTANCE_DIVISOR = 50  # "peak_distance = limit_orderbook/peak_distance_divisor"
    SL_PRICE_BUFFER = 0.5       # "add absolute price buffer for the stop loss, is the distance in price from the sl peak"
    TP_PRICE_BUFFER = 0.5       # " add absolute price buffer for the take profit, is the distance in price from the tp peak"
    MARKET = "BTCUSDT" # BTCUSDT 
    PERCENTAGE_PER_TRADE = 0.01 # 0.01 = 1%
    GAIN_PERCENTAGE_24H = 0.2
    """

    LIMIT_ORDERBOOK =  random.randint(MIN_LIMIT_ORDERBOOK_DATA, MAX_LIMIT_ORDERBOOK_DATA)
    RELATIVE_THRESHOLD_DIV = random.randint(MIN_RELATIVE_THRESHOLD_DIV, MAX_RELATIVE_THRESHOLD_DIV) # int (2,100) "relative operative trading THRESHOLD refered to : max_local_volume/relative_THRESHOLD "
    THRESHOLD_SHORT = round(random.uniform(MIN_THRESHOLD_SHORT, MAX_THRESHOLD_SHORT), 2)
    THRESHOLD_LONG = round(random.uniform(MIN_THRESHOLD_LONG, MAX_THRESHOLD_LONG), 2)
    MAX_SECONDS_TRADE_OPEN = random.randint(MIN_MAX_SECONDS_TRADE_OPEN, MAX_MAX_SECONDS_TRADE_OPEN)
    PEAK_DISTANCE_DIVISOR = random.randint(MIN_PEAK_DISTANCE_DIVISOR, MAX_PEAK_DISTANCE_DIVISOR) #"peak_distance = limit_orderbook/peak_distance_divisor"
    SL_PRICE_BUFFER = round(random.uniform(MIN_SL_PRICE_BUFFER, MAX_SL_PRICE_BUFFER), 2) #"add absolute price buffer for the stop loss, is the distance in price from the sl peak"
    TP_PRICE_BUFFER = round(random.uniform(MIN_TP_PRICE_BUFFER, MAX_TP_PRICE_BUFFER), 2) #"add absolute price buffer for the take profit, is the distance in price from the tp peak"
    PERCENTAGE_PER_TRADE = round(random.uniform(MIN_PERCENTAGE_PER_TRADE, MAX_PERCENTAGE_PER_TRADE), 4) # 0.01 = 1%
    
    fitness = 0

    N_STRATEGY = 0
    PATH_FILE = f"{strategies_folder}strategy_{N_STRATEGY}.py"
    
    while os.path.exists(PATH_FILE):
        N_STRATEGY += 1
        PATH_FILE = PATH_FILE.replace(f'strategy_{N_STRATEGY-1}',f'strategy_{N_STRATEGY}')

    with open(PATH_FILE, "w") as file:
        file.write("MARKET = '{}'\n".format(MARKET))
        file.write("LIMIT_ORDER_BOOK = {}\n".format(LIMIT_ORDERBOOK))
        file.write("RELATIVE_THRESHOLD_DIV = {}\n".format(RELATIVE_THRESHOLD_DIV))
        file.write("THRESHOLD_SHORT = {}\n".format(THRESHOLD_SHORT))
        file.write("THRESHOLD_LONG = {}\n".format(THRESHOLD_LONG))
        file.write("MAX_SECONDS_TRADE_OPEN = {}\n".format(MAX_SECONDS_TRADE_OPEN))
        file.write("PEAK_DISTANCE_DIVISOR = {}\n".format(PEAK_DISTANCE_DIVISOR))
        file.write("SL_PRICE_BUFFER = {}\n".format(SL_PRICE_BUFFER))
        file.write("TP_PRICE_BUFFER = {}\n".format(TP_PRICE_BUFFER))
        file.write("PERCENTAGE_PER_TRADE = {}\n".format(PERCENTAGE_PER_TRADE))
        file.write("fitness = {}\n".format(fitness))

if __name__ == "__main__":
    strategy_generator( strategies_folder = STRATEGIES_FOLDER )