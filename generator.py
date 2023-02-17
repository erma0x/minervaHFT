import random
import os
from configuration_strategy import *

def strategy_generator():
    """
    STRATEGY FILE GENERATOR

    MARKET = 'BTCUSDT'
    LIMIT_ORDER_BOOK =  500
    RELATIVE_THRESHOLD_DIV = 10 # int (2,100) "relative operative trading threshold refered to : max_local_volume/relative_threshold "
    THESHOLD_SHORT = 0.63
    THESHOLD_LONG = 0.37
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
    RELATIVE_THRESHOLD_DIV = random.randint(MIN_RELATIVE_THRESHOLD_DIV, MAX_RELATIVE_THRESHOLD_DIV) # int (2,100) "relative operative trading threshold refered to : max_local_volume/relative_threshold "
    THESHOLD_SHORT = round(random.uniform(MIN_THESHOLD_SHORT, MAX_THESHOLD_SHORT), 2)
    THESHOLD_LONG = round(random.uniform(MIN_THESHOLD_LONG, MAX_THESHOLD_LONG), 2)
    MAX_SECONDS_TRADE_OPEN = random.randint(MIN_MAX_SECONDS_TRADE_OPEN, MAX_MAX_SECONDS_TRADE_OPEN)
    PEAK_DISTANCE_DIVISOR = random.randint(MIN_PEAK_DISTANCE_DIVISOR, MAX_PEAK_DISTANCE_DIVISOR) #"peak_distance = limit_orderbook/peak_distance_divisor"
    SL_PRICE_BUFFER = round(random.uniform(MIN_SL_PRICE_BUFFER, MAX_SL_PRICE_BUFFER), 2) #"add absolute price buffer for the stop loss, is the distance in price from the sl peak"
    TP_PRICE_BUFFER = round(random.uniform(MIN_TP_PRICE_BUFFER, MAX_TP_PRICE_BUFFER), 2) #"add absolute price buffer for the take profit, is the distance in price from the tp peak"
    PERCENTAGE_PER_TRADE = round(random.uniform(MIN_PERCENTAGE_PER_TRADE, MAX_PERCENTAGE_PER_TRADE), 4) # 0.01 = 1%
    
    fitness = 0

    N_STRATEGY = 0
    PATH_FILE = f"./strategies/s{N_STRATEGY}.py"
    
    while os.path.exists(PATH_FILE):
        N_STRATEGY += 1
        PATH_FILE = PATH_FILE.replace(f's{N_STRATEGY-1}',f's{N_STRATEGY}')

    with open(PATH_FILE, "w") as file:
        file.write("MARKET = '{}'\n".format(MARKET))
        file.write("LIMIT_ORDER_BOOK = {}\n".format(LIMIT_ORDERBOOK))
        file.write("RELATIVE_THRESHOLD_DIV = {}\n".format(RELATIVE_THRESHOLD_DIV))
        file.write("THESHOLD_SHORT = {}\n".format(THESHOLD_SHORT))
        file.write("THESHOLD_LONG = {}\n".format(THESHOLD_LONG))
        file.write("MAX_SECONDS_TRADE_OPEN = {}\n".format(MAX_SECONDS_TRADE_OPEN))
        file.write("PEAK_DISTANCE_DIVISOR = {}\n".format(PEAK_DISTANCE_DIVISOR))
        file.write("SL_PRICE_BUFFER = {}\n".format(SL_PRICE_BUFFER))
        file.write("TP_PRICE_BUFFER = {}\n".format(TP_PRICE_BUFFER))
        file.write("PERCENTAGE_PER_TRADE = {}\n".format(PERCENTAGE_PER_TRADE))
        file.write("fitness = {}\n".format(fitness))

if __name__ == "__main__":
    strategy_generator()