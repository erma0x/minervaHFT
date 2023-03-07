import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))
import time
import pickle
from minerva.configuration_backtest import ROOT_PATH

def get_filepaths(directory):
    """
    Restituisce una lista di tutti i file path all'interno della directory (ricorsivamente)
    """
    filepaths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith('.pickle'):
                filepaths.append(filepath)
    return filepaths


fitness_values = []

for experiment_number in range(157,209,1):
    generations_filepath = ROOT_PATH + f'/runs/experiment_{experiment_number}/'
    pickle_files = get_filepaths(generations_filepath)

    for filename in pickle_files:

        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                fitness_value = data['fitness']
                trades = data['#trades']
                gain_24_h = data['gain_24_h']
                counter_messages = data['msg']
                generation_number = int(filename.split('generation_')[1].split('/')[0])
                strategy_number = int(filename.split('strategy_')[1].split('.pickle')[0])

                fitness_values.append((fitness_value, trades, gain_24_h,counter_messages, experiment_number,generation_number,strategy_number))
        except:
            pass

#print(fitness_values)
sorted_data = sorted(fitness_values, key=lambda x: x[0]) # ordina in base al primo valore di ogni elemento

#print(sorted_data)

TOP_NUMBER = 10
top_strategy = sorted_data[-TOP_NUMBER:][::-1] # prendi i primi 10 elementi in ordine decrescente

for i in top_strategy:
    print(i)