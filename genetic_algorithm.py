#!/usr/bin/env python3
import os
import shutil
import random
from pprint import pprint
import math
import numpy as np

from configuration_backtest import ROOT_PATH
from configuration_genetic_algorithm import *
from configuration_strategy import *

from threading_utilities import run_strategies
from generator import strategy_generator



def mutate_int(value,min,max):
    increment = min
    value = int(value) + random.randint(-increment,increment)
    
    if value >= max:
        value = value - int(math.floor(max / random.uniform(2.0,4.0)))

    if value <= min:
        value = value + int(math.floor(max / random.uniform(2.0,4.0)))

    return value

def mutate_float(value,min,max):
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


def get_population(filepath_strategies):
    obj = os.scandir(filepath_strategies)
    list_of_files = []
    
    for entry in obj :
        if entry.is_file() and entry.name not in ("__init__.py","__pycache__") :
            list_of_files.append(entry.name)
    
    population = []
    for filepath_strategy in list_of_files:
        with open(filepath_strategies+filepath_strategy, 'r') as f:
            data = f.readlines()
            individual = {}
            for i in range(len(data)):
                if '=' in data[i]:
                    data[i] = data[i].replace('\n', '').replace(' ', '')
                    key = data[i].split('=')[0]
                    value = data[i].split('=')[1]
                    if '[' in str(value):
                        value = str(value[1:-1])
                    if key != 'MARKET':
                        if '.' not in value: # int
                            individual[key] = int(value)
                        else: # float
                            individual[key] = float(value)
                    else:
                        individual[key] = value.replace("'",'')
            population.append(individual)

    return population


def crossover(parent1, parent2):
    child = {}
    for key in parent1:
        if key == 'fitness':
            child[key] = (parent1[key]+parent2[key])/2
        if random.random() < 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]

    return child

def genetic_algorithm(population, fitness_function,pop_size=2):
    # SELEZIONE
    parents = selection(population, fitness_function)
    
    # MUTAZIONE
    
    # CROSS OVER
    children = []
    if pop_size > len(children):
        while pop_size > len(children):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents) 
            child = crossover(parent1, parent2)
            if child not in children:
                children.append(child)

    return children

# Funzione di selezione fittness
def selection(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[:len(population) // 2]

def get_best(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[0]

def save_best(population, fitness_function):
    best = get_best(population, fitness_function)
    with open('best.py', 'w') as file_handle:
        file_handle.write(str(best))

# Funzione di fitness
def fitness_function(individual):
    return individual['fitness']

def remove_folder(folder_path):
    # Try to remove the tree; if it fails, throw an error using try...except.
    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        print("Error removing the folder %s - %s." % (e.filename, e.strerror))


if __name__ == '__main__':

    print(f' Minerva Genetic Algorithm \n')

    STRATEGY_PATH = ROOT_PATH +"/strategies/"

    # remove the old directory for reanitialization
    remove_folder(STRATEGY_PATH)

    # create a new directory
    if not os.path.exists(STRATEGY_PATH):
        os.makedirs(STRATEGY_PATH)

    # initialize the population
    for i in range(POPULATION_SIZE):
        strategy_generator()

    population = get_population( filepath_strategies = STRATEGY_PATH )

    for i in range(GENERATION_SIZE):
        
        population = genetic_algorithm( population = population , fitness_function = fitness_function, pop_size = POPULATION_SIZE)
        
        # test with oracles the new population # MULTITHREAD and Test with oracles  => print(BEST_PE RFORMANCE, BEST_ID)
        run_strategies() 
        # le strategie non si bloccano, devo fare blocchi di generazioni.

        # save the best strategy in a file
        BEST = get_best(population, fitness_function)
        get_best(population, fitness_function)
        save_best(population, fitness_function) 
        print(f"best      {BEST}")
        print(f'len pop   {len(population)}')

        # mutation 
        # alla fine ho lasciato la cosa piu easy 
        # e' stato un hackaton con me stesso della madonna  ############################### ############### >> WIN ? 
