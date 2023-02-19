#!/usr/bin/env python3
import os
import shutil
import random
from pprint import pprint
import math
import numpy as np

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from configuration_backtest import ROOT_PATH, STRATEGIES_FOLDER
from configuration_genetic_algorithm import MUTATION_RATE, GENERATION_SIZE, POPULATION_SIZE, GET_BEST_INITIAL_POPULATION
from configuration_strategy import *

from threading_utils import run_strategies
from minerva.strategy_generator import strategy_generator

def get_list_filepath_strategies(filepath_strategies):
    try:
        obj = os.scandir(filepath_strategies)
    except FileNotFoundError:
        obj = []
    list_of_files = []
    
    for entry in obj :
        if entry.is_file() and entry.name not in ("__init__.py","__pycache__") :
            list_of_files.append(filepath_strategies+entry.name)
    
    return list_of_files


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

def mutate_strategy(filepath_strategies):
    """mutate file parameters with random values of the same type

    Args:
        filepath (string): strategy file path strategies to mutate
    """
    list_of_files = get_list_filepath_strategies(filepath_strategies=filepath_strategies)

    for filepath in list_of_files:
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

                                if key == 'THRESHOLD_SHORT':
                                    value = mutate_float(value=value, min=MIN_THRESHOLD_SHORT, max=MAX_THRESHOLD_SHORT)

                                if key == 'THRESHOLD_LONG':
                                    value = mutate_float(value=value, min=MIN_THRESHOLD_LONG, max=MAX_THRESHOLD_LONG)

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
    list_of_files = get_list_filepath_strategies(filepath_strategies=filepath_strategies)
    
    population = []
    for filepath_strategy in list_of_files:
        with open(filepath_strategy, 'r') as f:
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
            child[key] = -0.001   # (parent1[key]+parent2[key])/2

        if random.random() < 0.5:
            child[key] = parent1[key]
        
        else:
            child[key] = parent2[key]

    return child

def genetic_algorithm(population, fitness_function,pop_size=2):
    
    parents = selection(population, fitness_function)
    
    mutate_strategy(filepath_strategies = STRATEGIES_FOLDER)
    
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

def selection(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[:int(math.floor(len(population) // 3)) ]

def fitness_function(individual):
    return individual['fitness']
    
def get_best(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[0]

def save_best(population, fitness_function):
    best = get_best(population, fitness_function)

    best_number_counter = 0
    path = f'./bests/best_{best_number_counter}.py'
    while os.path.exists(path):
        best_number_counter+=1
        path = f'./bests/best_{best_number_counter}.py'

    with open(path, 'w') as f:
        for key, value in best.items():
            if type(value) == str:
                f.write(f"{key} = '{value}'\n")
            else:
                f.write(f"{key} = {value}\n")


def remove_folder(folder_path):
    # Try to remove the tree; if it fails, throw an error using try...except.
    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        pass
        #print("minerva-Error removing the folder %s - %s." % (e.filename, e.strerror))

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == '__main__':

    os.system('clear')
    
    print(f'\n\t 🧬 Minerva genetic algorithm \n')
    print(f'{Fore.LIGHTGREEN_EX} generation size {Style.RESET_ALL} {GENERATION_SIZE} ')
    print(f'{Fore.LIGHTGREEN_EX} population size {Style.RESET_ALL} {POPULATION_SIZE} ')
    print(f'{Fore.LIGHTGREEN_EX} mutation rate   {Style.RESET_ALL} {round(MUTATION_RATE*100,2)} % \n ')


    # runs/expmeriment_1/generation_0/s0.py => runs/expmeriment_2/generation_0/s0.py
    # remove for reanitialization
    remove_folder(STRATEGIES_FOLDER)

    create_folder(STRATEGIES_FOLDER)


    if GET_BEST_INITIAL_POPULATION == True:
        # TO IMPLEMENT
        pass 

    else:
        # initialize random population 
        for i in range(POPULATION_SIZE):
            strategy_generator()

    POPULATION = get_population( filepath_strategies = STRATEGIES_FOLDER )

    for generation_number in range(GENERATION_SIZE):
        
        POPULATION = genetic_algorithm( population = POPULATION , fitness_function = fitness_function, pop_size = POPULATION_SIZE)
        
        run_strategies() 

    exit()