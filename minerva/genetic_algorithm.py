#!/usr/bin/env python3

# SUPER IMPORTANT
# da mettere in ogni file coinvolto
# lancia python3 minerva/genetic_algorithm.py
# oppure python3 minerva/streamer.py --live True
#      + python3 minerva/oracle --strategy ./strategies/balenottera_azzurra.py

import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

import shutil
import random
from pprint import pprint
import math
import numpy as np

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from minerva.configuration_backtest import ROOT_PATH, STRATEGIES_FOLDER
from minerva.configuration_genetic_algorithm import MUTATION_RATE, GENERATION_SIZE, POPULATION_SIZE, GET_BEST_INITIAL_POPULATION
from minerva.configuration_strategy import *
from minerva.threading_utils import run_strategies
from minerva.strategy_generator import strategy_generator

def get_filepaths_list(filepath_to_check: str):
    """Returns a list of strategies fielpaths for a given filepath_strategies"""
    try:
        obj = os.scandir(filepath_to_check)
    except FileNotFoundError:
        obj = []
    list_of_files = []
    
    for entry in obj :
        if entry.is_file() and entry.name not in ("__init__.py","__pycache__") :
            list_of_files.append(filepath_to_check+'/'+entry.name)
    
    return list_of_files


def mutate_int(value,min,max):
    """
    mutate an integer value between min and max 
    with a random increament (-min,+min)
    """
    increment = min
    value = int(value) + random.randint(-increment,increment)
    
    if value >= max:
        value = value - int(math.floor(max / random.uniform(2.0,4.0)))

    if value <= min:
        value = value + int(math.floor(max / random.uniform(2.0,4.0)))

    return value

def mutate_float(value,min,max):
    """
    mutate a float value with a gaussian distribution
    mu : mean its equal to the given value
    sigma : standard deviation its equal to 1/10 of max value
    """
    sigma = max/10
    mu = float(value)
    value = np.random.normal(mu, sigma, 1)
    while value >= max:
        value = value - max / 100

    while value <= min:
        value = value + max / 100
    return float(value)


def mutate_strategy(population):
    new_population = []
    for i in population:
        individual = {}
        for key, value in i.items():
            if random.random() < MUTATION_RATE:
                if key == 'LIMIT_ORDER_BOOK':
                    value = mutate_int(value=value, min=MIN_LIMIT_ORDERBOOK_DATA, max=MAX_LIMIT_ORDERBOOK_DATA)

                if key == 'RELATIVE_THRESHOLD_DIV':
                    value = mutate_int(value=value, min=MIN_RELATIVE_THRESHOLD_DIV, max=MAX_RELATIVE_THRESHOLD_DIV)

                if key == 'MAX_SECONDS_TRADE_OPEN':
                    value = mutate_int(value=value, min=MIN_MAX_SECONDS_TRADE_OPEN, max=MAX_MAX_SECONDS_TRADE_OPEN)

                if key == 'PEAK_DISTANCE_DIVISOR':
                    value = mutate_int(value=value, min=MIN_PEAK_DISTANCE_DIVISOR, max=MAX_PEAK_DISTANCE_DIVISOR)

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

                if key == 'K1':
                    value = mutate_float(value=value, min=MIN_K, max=MAX_K)

                if key == 'K2':
                    value = mutate_float(value=value, min=MIN_K, max=MAX_K)

                if key == 'K3':
                    value = mutate_float(value=value, min=MIN_K, max=MAX_K)

                if key == 'W_I':
                    value = mutate_float(value=value, min=MIN_WINDOW_INCREMENT, max=MAX_WINDOW_INCREMENT)
            individual[key] = value
        new_population.append(individual)
    return new_population


def get_population(filepath_strategies):
    """
    Description:
        read the population in a file directory
        and return a list of dictionaries

    Args:
        filepath_strategies (string): file path with the strategies

    Returns:
        population: list of individuals
    """
    list_of_files = get_filepaths_list(filepath_to_check = filepath_strategies )
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
    """
    Description:
        get 2 random individuals within the given population and
        switch the values between them. Set the new fitness value to 0.

    Args:
        parent1 (dictionary): trading strategy parameters dictionary 
        parent2 (dictionary): trading strategy parameters dictionary 

    Returns:
        child (dictionary): trading strategy parameters dictionary 
    """
    child = {}
    for key in parent1.keys():
        if key == 'fitness':
            child[key] =  (parent1[key]+parent2[key])/2

        else:
            child[key] = parent2[key]

    return child



def genetic_algorithm(population, fitness_function, generation_number = 0, pop_size = 2):

    parents = selection(population, fitness_function)
    
    children = []
    if pop_size > len(children):
        while pop_size > len(children):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents) 
            child = crossover(parent1, parent2)

            if child not in children:
                children.append(child)
    
    mutated_children = mutate_strategy(children) # generation + 1
    NEW_GENERATION_FOLDER = STRATEGIES_FOLDER.replace(f'generation_{generation_number}',f'generation_{generation_number+1}')
    save_population(population = mutated_children, dir_name = NEW_GENERATION_FOLDER )
    children = get_population(filepath_strategies = NEW_GENERATION_FOLDER )
    return children

def selection(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[:int(math.floor(len(population) // 3)) ]

def fitness_function(individual):
    return individual['fitness']
    
def get_best(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[0]


def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        print("===> Error removing the folder %s - %s." % (e.filename, e.strerror))

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_population(population, dir_name):
    create_folder(dir_name) #os.makedirs(dir_name, exist_ok=True)
    for i, item in enumerate(population):
        filename = f"{dir_name}/strategy_{i}.py"
        with open(filename, 'w') as f:
            for key,value in item.items():
               f.write(f"{key} = {value}\n")
               

def get_best_initial_population(path, fitness_function, pop_size = 5 ):
    POP = get_population(path)
    sorted_population = sorted(POP, key = fitness_function, reverse=True)
    INITIAL_POPULATION = []
    while len(INITIAL_POPULATION)< pop_size:
        INITIAL_POPULATION.append(sorted_population[0])
        sorted_population = sorted_population[1:]
    
    return INITIAL_POPULATION

if __name__ == '__main__':

    os.system('clear')
    
    print(f'\n\t 🧬 Minerva genetic algorithm \n')
    print(f'{Fore.LIGHTGREEN_EX} generation size {Style.RESET_ALL} {GENERATION_SIZE} ')
    print(f'{Fore.LIGHTGREEN_EX} population size {Style.RESET_ALL} {POPULATION_SIZE} ')
    print(f'{Fore.LIGHTGREEN_EX} mutation rate   {Style.RESET_ALL} {round(MUTATION_RATE*100,2)} % \n ')


    # runs/expmeriment_1/generation_0/s0.py => runs/expmeriment_2/generation_0/s0.py
    experiment_number = 0
    experiment_directory = ROOT_PATH+f'/runs/experiment_{experiment_number}/'
    while os.path.exists(experiment_directory):
        experiment_number+=1
        experiment_directory = ROOT_PATH+f'/runs/experiment_{experiment_number}/'

    os.makedirs(experiment_directory, exist_ok=True)
    generation_number = 0

    # remove for reanitialization
    # remove_folder(STRATEGIES_FOLDER)

    create_folder(STRATEGIES_FOLDER)


    if GET_BEST_INITIAL_POPULATION == True:
        BEST_INITIAL_POP = get_best_initial_population(STRATEGIES_FOLDER,fitness_function=fitness_function, pop_size = POPULATION_SIZE)

    else:
        # initialize random population 
        for i in range(POPULATION_SIZE):
            strategy_generator(STRATEGIES_FOLDER+'/')

    POPULATION = get_population( filepath_strategies = STRATEGIES_FOLDER )

    for generation_number in range(1,GENERATION_SIZE+1):

        run_strategies() 

        POPULATION = genetic_algorithm( population = POPULATION , fitness_function = fitness_function, generation_number = generation_number, pop_size = POPULATION_SIZE)
        
    exit()