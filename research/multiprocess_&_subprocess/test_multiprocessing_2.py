from multiprocessing import Pool, cpu_count
import time
# sys.path.append(os.path.abspath("/home/el/foo4/stuff")) # e ci metto direttamente la strategia da importare


# tutte le strategie
work = (["strategy_1", 5], ["B", 2], ["C", 1], ["D", 3])

# importa la funzione oracolo(strategia), le strategie

def oracle(data,strategy): # oracle()
    print(" Process %s" % (work_data[0]))
    #time.sleep(int(work_data[1]))


def pool_handler():

    # stramer get data files
    for file in files:
        for datapoint_in in data: 
            
            p = Pool(cpu_count())
            p.map(oracle,work_data)


if __name__ == '__main__':
    pool_handler()