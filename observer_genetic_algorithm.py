import os
from configuration_backtest import ROOT_PATH
import time
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from genetic_algorithm import get_best, get_population, fitness_function
from configuration_backtest import STRATEGY_FOLDER
from pprint import pprint
# Imposta il percorso della directory contenente i file

directory_path = ROOT_PATH+'/strategies/'

def monitor_performances(directory_path):
    file_list = [f for f in os.listdir(directory_path) if f.endswith('.py')]

    results = []

    for file_name in file_list:
        with open(os.path.join(directory_path, file_name), 'r') as f:
            lines = f.readlines()
            try:
                last_line = lines[-1]
                if 'fitness' in last_line:
                    if '[' in last_line:
                        last_line = last_line.replace('[', '').replace(']', '')
                    fitness_value = float(last_line.split('=')[1].strip())
                    results.append((file_name, fitness_value))
            except:
                pass

    results_sorted = sorted(results, key=lambda x: x[1], reverse=True)
    os.system('clear')
    print(f'\n\t  {Fore.YELLOW}   Observer  {Style.RESET_ALL} ')
    print(f'\n {Fore.CYAN} ID  \t\t 💰 24h% {Style.RESET_ALL} \n')
    for file_name, fitness_value in results_sorted:
        if fitness_value > 0:
            print(f" {file_name.replace('.py','').replace('s','')} \t\t {Fore.GREEN} {round(fitness_value,3)} {Style.RESET_ALL}  ")
        else:
            print(f" {file_name.replace('.py','').replace('s','')} \t\t {Fore.RED} {round(fitness_value,3)}{Style.RESET_ALL}  ")

    population = get_population( filepath_strategies = STRATEGY_FOLDER )

    # get best id
    BEST = get_best( population=population, fitness_function=fitness_function)
    pprint(BEST)
    
    time.sleep(1)

if __name__ == '__main__':
    colorama_init()

    while True:
        monitor_performances(directory_path=directory_path)