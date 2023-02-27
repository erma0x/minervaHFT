import subprocess
import time
import zmq
import signal
from progress.bar import FillingSquaresBar, FillingCirclesBar, PixelBar,ChargingBar

#for i in range(5):
    # Apre il processo

import gc
import os,sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from minerva.configuration_genetic_algorithm import *
from minerva.configuration_backtest import *
from minerva.threading_utils import find_files
from minerva.genetic_algorithm import *


def start_oracle(file):
    oracle_file = file.split('/minervaHFT/')[1]
    return subprocess.Popen(['python3', f'minerva/oracle.py -s {oracle_file}'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

def start_streamer():
    return subprocess.Popen(['python3', f'minerva/streamer.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)



    #for generation_number in range(GENERATIONS)
def test_genetic_algorithm(): 

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
    NEW_GENERATION_FOLDER = STRATEGIES_FOLDER
    for generation_number in range(0,GENERATIONS):

        files = find_files(NEW_GENERATION_FOLDER)

        processes_list = []
        for file in files:
            oracle_file = file.split('/minervaHFT/')[1]
            process = subprocess.Popen(['python3', f'minerva/oracle.py -s {oracle_file}'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            processes_list.append(process)
            
            print(f'pid {process.pid} python3 minerva/oracle.py -s {oracle_file}')

        process = 
        
        print(f'pid {process.pid} python3 minerva/streamer.py')
        processes_list.append(process)

        #signal.signal(signal.SIGINT, signal.SIG_DFL)
        context = zmq.Context()
        consumer_socket = context.socket(zmq.SUB)
        consumer_socket.connect("tcp://127.0.0.1:5556")
        consumer_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        
        print('lunching zmq consumer socket for killing the processes')
        
        counter = 0

        gc.enable()
        gc.set_threshold( 2000 , 1000 , 1000)

        bar = ChargingBar(f'\n\t generation {generation_number} ', max = 5000)    

        time.sleep(5)
        while True:
            msg = consumer_socket.recv_string() # orderbook
            
            os.system('clear')

            # print(f' msg: {counter}')
            # print(gc.get_count())

            bar.next()
            counter+=1

            if msg == 'kill':
                print('')
                for process in processes_list:
                    print(f' kill {process.pid}')
                    process.kill() # OR #os.kill(process.pid,9)
                break

            time.sleep(0.03)

        bar.finish()

        print('get old population')
        POPULATION = get_population(filepath_strategies = NEW_GENERATION_FOLDER )
        NEW_GENERATION_FOLDER = NEW_GENERATION_FOLDER.replace(f'generation_{generation_number}',f'generation_{generation_number+1}')

        print('selection')
        parents = selection(POPULATION, fitness_function)
        
        print('cross over')
        children = []
        if POPULATION_SIZE > len(children):
            while POPULATION_SIZE > len(children):
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)
                #print(POPULATION)  ####################### FIX CROSS OVER
                child = mutate_strategy(crossover(parent1, parent2))
                if child not in children:
                    children.append(child)

                time.sleep(1)
                print(f' {len(parents)} adults are trying to have sex')
                print(f' {len(children)} babies')

        print('mutation')
        print(f'save population {NEW_GENERATION_FOLDER}')
        save_population(population = children, dir_name = NEW_GENERATION_FOLDER )
        print('get population')
        POPULATION = get_population(filepath_strategies = NEW_GENERATION_FOLDER )
        

if __name__ == "__main__":
    test_genetic_algorithm()