import unittest
import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('tests/',''))
from configuration_backtest import ROOT_PATH
from configuration_genetic_algorithm import GENERATION_SIZE
from genetic_algorithm import get_population, get_best,fitness_function, save_best


def get_champion_each_generation():
    ALL_TIME_CHAMPIONS = []
    for generation_number in range(GENERATION_SIZE):
        root_dir = ROOT_PATH.replace('minervaHFT/minerva','minervaHFT')+f'/runs/experiment_1/generation_{generation_number}'
        POPULATION = get_population( root_dir )
        CHAMPION = get_best( POPULATION , fitness_function = fitness_function )
        ALL_TIME_CHAMPIONS.append(CHAMPION)
    return ALL_TIME_CHAMPIONS


def get_best_champion(fitness_function):
    ALL_TIME_CHAMPIONS = get_champion_each_generation()
    BEST_CHAMPION = get_best( ALL_TIME_CHAMPIONS , fitness_function = fitness_function )
    return(BEST_CHAMPION)

def get_good_initial_bot(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[0]


def get_best_initial_population(path, fitness_function, pop_size = 5 ):
    POP = get_population(path)
    #get_best(POP , fitness_function = fitness_function)
    sorted_population = sorted(POP, key = fitness_function, reverse=True)
    INITIAL_POPULATION = []

    while len(INITIAL_POPULATION)< pop_size:
        INITIAL_POPULATION.append(sorted_population[0])
        sorted_population = sorted_population[1:]
    
    return INITIAL_POPULATION

# ALL_TIME_CHAMPIONS = get_champion_each_generation()
# get_best_champion(fitness_function = fitness_function)

root_dir = ROOT_PATH.replace('minervaHFT/minerva','minervaHFT')+f'/runs/experiment_1/generation_0'
print(root_dir)
BEST_INITIAL_POP = get_best_initial_population(root_dir,fitness_function=fitness_function,pop_size=2)
print(BEST_INITIAL_POP)