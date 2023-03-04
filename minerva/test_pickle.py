import os,pickle

def store_pickle(new_data,filename):
    filename = filename.replace('\n','').replace(' ','')
    
    if not os.path.isfile(filename):
        with open(filename, "ab") as f:
            print('')

    handle = open(filename, 'rb')
    pickle.dump(new_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


import pickle
  
def store_perfomances(data,filename):
    # Its important to use binary mode
    filename = filename.replace('.py','.pickle')
    dbfile = open(filename, 'ab')
    pickle.dump(data, dbfile)                     
    dbfile.close()

db = {'fitness':12}

store_perfomances(data=db,filename="minerva/runs/experiment_157/generation_0/strategy_3.pickle")

#store_perfomances(data=db,filename=' minerva/runs/experiment_154/generation_0/strategy_1.pickle\'\n'.replace(' ','').replace("'\n",''))
#store_pickle({'fitness':2},"minerva/runs/experiment_154/generation_0/strategy_1.pickle")