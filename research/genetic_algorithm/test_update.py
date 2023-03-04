
import os,sys
from datetime import datetime
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

from minerva.oracle import update_performance, update_performance_json

def update_performance_pickle(new_value, filename):
    # apri il file in modalità di lettura e scrittura
    with open(filename, "r+") as f:
        # carica il contenuto del file JSON in una variabile
        data = json.load(f)

        # cerca la chiave "fitness" e sostituisci il valore
        if "fitness" in data:
            data["fitness"] = new_value

        # torna all'inizio del file e sovrascrivi il contenuto con i dati modificati
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


start_time =  datetime.now()

# stampa il tempo di esecuzione
update_performance(1,'minerva/runs/experiment_136/generation_0/strategy_1.py')

end_time = datetime.now()
print("Tempo di esecuzione 1: {} secondi".format(end_time - start_time))

start_time =  datetime.now()



update_performance_json(2,'minerva/runs/experiment_136/generation_0/strategy_1.json')


end_time = datetime.now()

print("Tempo di esecuzione 2: {} secondi".format(end_time - start_time))
