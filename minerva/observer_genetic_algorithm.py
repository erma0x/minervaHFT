import os
import time
from pprint import pprint

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from minerva.genetic_algorithm import get_best, get_population, fitness_function, get_filepaths_list
from minerva.configuration_backtest import STRATEGY_FOLDER


def monitor_performances(directory_path):
    """ 

    get all the filepath strategies in a directory
    read all the files in the directory
    print name of the filepath ID
    print the fitness in each file 
    print the best strategy founded
    
    if best strategy not in ALL_BEST_STRATEGIES:
        save the best strategy in ALL_BEST_STRATEGIES
    
    
    Args:
        directory_path (string): filepath strategies directory
    """
    list_of_files = get_filepaths_list(directory_path)
    results = []
    BEST = {}

    # READ FITNESS AND SORT
    for file_name in list_of_files:
        with open(file_name, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            if 'fitness' in last_line:
                if '[' in last_line:
                    last_line = last_line.replace('[', '').replace(']', '')
                fitness_value = float(last_line.split('=')[1].strip())
                results.append((file_name, fitness_value))

    results_sorted = sorted(results, key=lambda x: x[1], reverse=True)

    # GET BEST
    POPULATION = get_population( filepath_strategies = STRATEGY_FOLDER )
    print(POPULATION)
    if POPULATION != []:
        BEST = get_best( population = POPULATION, fitness_function = fitness_function)        
        
        TMP = BEST.copy() 
        TMP['fitness'] = 0

        if TMP not in ALL_BEST_STRATEGIES:
            ALL_BEST_STRATEGIES.append(TMP)

    # PRINT
    os.system('clear')
    print(f'\n\t  {Fore.BLUE}   Observer  {Style.RESET_ALL} ')
    print(f'\n {Fore.CYAN} ID  \t\t 💰 24h% {Style.RESET_ALL} \n')
    for file_name, fitness_value in results_sorted:
        if fitness_value > 0:
            print(f" {file_name.replace('.py','').replace('s','')} \t\t {Fore.GREEN} {round(fitness_value,3)} {Style.RESET_ALL}  ")
        else:
            print(f" {file_name.replace('.py','').replace('s','')} \t\t {Fore.RED} {round(fitness_value,3)}{Style.RESET_ALL}  ")

    if BEST:
        print('-----------------BEST STRATEGY-----------------------')
        pprint(f'{Fore.CYAN} {BEST} {Style.RESET_ALL}')
        print('-----------------------------------------------------')
           

    time.sleep(0.5)

if __name__ == '__main__':
    colorama_init()
    
    ALL_BEST_STRATEGIES = []
    while True:
        monitor_performances(directory_path = STRATEGY_FOLDER)