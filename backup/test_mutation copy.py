# apri tutti i file
# per ogni parametro
# se random.random() > MUTATION_RATE:
#   se int
#   se float
#   se string
import os
import random
import numpy as np
import math

from configuration_backtest import ROOT_PATH
from configuration_genetic_algorithm import *
from configuration_strategy import *

def mutate_int(value,min,max):
    increment = min
    value = int(value) + random.randint(-increment,increment)
    
    if value >= max:
        value = value - int(math.floor(max / random.uniform(2.0,4.0)))

    if value <= min:
        value = value + int(math.floor(max / random.uniform(2.0,4.0)))

    return value

def mutate_float(value,min,max):
    print('Mutating float')

    sigma = max/10
    mu = float(value)
    value = np.random.normal(mu, sigma, 1)
    if value >= max:
        value = value - max / random.uniform(2.0,4.0)

    if value <= min:
        value = value + max / random.uniform(2.0,4.0)

    return value

def mutate_strategy(filepath):
    individual = {}
    with open(filepath, "r") as file:
        data = file.readlines()
        for i in range(len(data)):
            if '=' in data[i]:
                data[i] = data[i].replace('\n', '').replace(' ', '')
                key = data[i].split('=')[0]
                value = data[i].split('=')[1]
                
                if '[' in str(value):
                    value = str(value[1:-1])


                # MUTATION
                if random.random() < MUTATION_RATE:
                    if key not in ('MARKET','fitness'):

                        if '.' not in value: # int
                            if key == 'LIMIT_ORDER_BOOK':
                                value = mutate_int(value=value, min=MIN_LIMIT_ORDERBOOK_DATA, max=MAX_LIMIT_ORDERBOOK_DATA)

                            if key == 'RELATIVE_THRESHOLD_DIV':
                                value = mutate_int(value=value, min=MIN_RELATIVE_THRESHOLD_DIV, max=MAX_RELATIVE_THRESHOLD_DIV)

                            if key == 'MAX_SECONDS_TRADE_OPEN':
                                value = mutate_int(value=value, min=MIN_MAX_SECONDS_TRADE_OPEN, max=MAX_MAX_SECONDS_TRADE_OPEN)

                            if key == 'PEAK_DISTANCE_DIVISOR':
                                value = mutate_int(value=value, min=MIN_PEAK_DISTANCE_DIVISOR, max=MAX_PEAK_DISTANCE_DIVISOR)

                        else: # float 

                            if key == 'THESHOLD_SHORT':
                                value = mutate_float(value=value, min=MIN_THESHOLD_SHORT, max=MAX_THESHOLD_SHORT)

                            if key == 'THESHOLD_LONG':
                                value = mutate_float(value=value, min=MIN_THESHOLD_LONG, max=MAX_THESHOLD_LONG)

                            if key == 'SL_PRICE_BUFFER':
                                value = mutate_float(value=value, min=MIN_SL_PRICE_BUFFER, max=MAX_SL_PRICE_BUFFER)

                            if key == 'TP_PRICE_BUFFER':
                                value = mutate_float(value=value, min=MIN_TP_PRICE_BUFFER, max=MAX_TP_PRICE_BUFFER)

                            if key == 'PERCENTAGE_PER_TRADE':
                                value = mutate_float(value=value, min=MIN_PERCENTAGE_PER_TRADE, max=MIN_PERCENTAGE_PER_TRADE)

                            individual[key] = value

                    else:
                        individual[key] = value    
                
                # CONTINUE
                else: 
                    if key != 'MARKET':
                        if '.' not in value:
                            individual[key] = int(value)
                        else:
                            individual[key] = float(value)

                    else:
                        individual[key] = value

    with open(filepath, "w") as f:
        for key, value in individual.items():
            f.write(f"{key} = {value}\n")
    
STRATEGY_FILEPATH =  ROOT_PATH+'/strategies/s1.py'

mutate_strategy(STRATEGY_FILEPATH)
