import glob
import pickle
import time

import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from minerva.configuration_backtest import STRATEGIES_FOLDER, experiment_number
from minerva.oracle import store_perfomances


def monitor_performances(filepath):
    pickle_files = [f for f in os.listdir(filepath) if f.endswith('.pickle')]
    fitness_values = []
    for filename in pickle_files:
        #try:
            with open(filepath+'/'+filename, "rb") as f:
                try:
                    data = pickle.load(f)
                    fitness_value = data['fitness']
                    trades = data['#trades']
                    gain_24_h = data['gain_24_h']
                    counter_messages = data['msg']

                    fitness_values.append((fitness_value, trades, gain_24_h,counter_messages, filename))
                except EOFError:
                    print('out of input')

        #except FileNotFoundError:
        #    print(f"File {filename} non trovato.")

    fitness_values.sort(reverse=True)

    os.system('clear')
    print(f"filename \t\t#trades \tgain_24_h \tcounter_messages \tgain$")
    for fitness, trades, gain_24_h,counter_messages, filename in fitness_values:
        print(f"{filename} \t{trades} \t{gain_24_h} \t{counter_messages} \t\t{fitness}")
    time.sleep(0.5)


def load_pickle(filename):
    with open(filename, 'rb') as handle:
        unserialized_data = pickle.load(handle)
        return unserialized_data

# store_perfomances(data={'fitness':4,'#trades':2134},filename='minerva/runs/experiment_179/generation_0'+'/strategy_0.py')
# store_perfomances(data={'fitness':3,'#trades':32},filename='minerva/runs/experiment_179/generation_0'+'/strategy_1.py')
# store_perfomances(data={'fitness':2,'#trades':53},filename='minerva/runs/experiment_179/generation_0'+'/strategy_2.py')
# store_perfomances(data={'fitness':1,'#trades':1234},filename='minerva/runs/experiment_179/generation_0'+'/strategy_3.py')

# data = load_pickle('minerva/runs/experiment_179/generation_0'+'/strategy_0.pickle')
# print(data)
# data = load_pickle('minerva/runs/experiment_179/generation_0'+'/strategy_1.pickle')
# print(data)
# data = load_pickle('minerva/runs/experiment_179/generation_0'+'/strategy_2.pickle')
# print(data)
# data = load_pickle('minerva/runs/experiment_179/generation_0'+'/strategy_3.pickle')
# print(data)

GENERATION_NUMBER = 0

while True:
    monitor_performances(filepath='minerva/runs/experiment_208/generation_0')
    
