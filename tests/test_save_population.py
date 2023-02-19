import os
import json
import pathlib

from genetic_algorithm import get_population
from configuration_backtest import STRATEGIES_FOLDER, ROOT_PATH

def save_population(population, dir_name):

    os.makedirs(dir_name, exist_ok=True)

    for i, item in enumerate(population):
        filename = f"{dir_name}/strategy_{i}.py"
        with open(filename, 'w') as f:
            for key, value in item.items():
                if "MARKET" in str(key):
                    f.write(f"{key} = '{value}'\n")

                elif "[" in str(value):
                    f.write(f"{key} = '{float(str(value).replace('[','').replace(']',''))}'\n")

                else:
                    f.write(f"{key} = {value}\n")
            
if __name__ == '__main__':

    GENERATIONS = 5
    for i in range(GENERATIONS):
        
        generation_strategy_folder = str(pathlib.Path(f"{ROOT_PATH.replace('HFT/minerva','HFT/')+f'/runs/experiment_1/generation_{i}/'}"))
        POPULATION = get_population(filepath_strategies = generation_strategy_folder )
        print(f'strategy_folder {generation_strategy_folder}')
        
        
        save_path = pathlib.Path(ROOT_PATH.replace('HFT/minerva','HFT/')+f'/runs/experiment_1/generation_{i+1}/')
        print(f'save {save_path}')
        save_population( population = POPULATION, dir_name = save_path )

