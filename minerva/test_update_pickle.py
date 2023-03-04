import pickle
from datetime import datetime

def store_pickle(your_data,filename):
    with open(filename, 'wb') as handle:
        pickle.dump(your_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(filename):
    with open(filename, 'rb') as handle:
        unserialized_data = pickle.load(handle)
        return unserialized_data

start_time =  datetime.now()
fitness = {'fitness': 21}
#store_pickle( fitness , 'minerva/fitness.pickle' )
end_time = datetime.now()
print("Tempo di esecuzione 1: {} secondi".format(end_time - start_time))
your_data = {'fitness': 22}

#store_pickle( your_data , 'minerva/test.pickle' )

start_time =  datetime.now()

import time
while True:
    data = load_pickle('minerva/runs/experiment_142/generation_0/strategy_5.pickle' )
    #end_time = datetime.now()
    #print("Tempo di esecuzione 2: {} secondi".format(end_time - start_time))
    print(data)
    time.sleep(1)