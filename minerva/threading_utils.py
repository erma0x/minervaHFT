#!/usr/bin/env python3

import threading
import subprocess
from multiprocessing import Process
import zmq
import os
import time

from configuration_backtest import ROOT_PATH, STRATEGIES_FOLDER


def run_oracle(file):
    
    process_id = subprocess.call(cmd, shell=True)
    return process_id

def run_streamer():
    cmd = f"python3 minerva/streamer.py"
    process_id = subprocess.call(cmd, shell=True)
    return process_id


def find_files(path):
    file_list = []
    files = os.scandir(path)
    for file in files:
        if '__' not in str(file): 
            file_list.append(os.path.join(file))
    return tuple(file_list)

def run_command(cmd):
    process_id = subprocess.Popen(cmd, shell=True)
    return process_id

def run_strategies():    
        files = find_files(STRATEGIES_FOLDER)
        
        processes_list = []
        for file in files:
            print(f'python3 minerva/oracle.py -s {file}')
            process = subprocess.Popen(['python3', f'minerva/oracle.py -s {file}'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            processes_list.append(process)
            print(f'process id lunched {process.pid}')
        
        process = subprocess.Popen(['python3', f'minerva/streamer.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #process = subprocess.Popen(['python3', f'minerva/streamer_test.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        print('streamer lunched')
        processes_list.append(process)

        #signal.signal(signal.SIGINT, signal.SIG_DFL)

        context = zmq.Context()
        consumer_socket = context.socket(zmq.SUB)
        consumer_socket.bind("tcp://*:5557")
        consumer_socket.setsockopt(zmq.SUBSCRIBE, b'')
        print('consumer socket')
        counter=0
        while True:
            msg = consumer_socket.recv_string() # orderbook
            os.system('clear')
            print(f'#msg: {counter}')
            counter+=1
            if msg == 'kill':
                for process in processes_list:
                    print(f'kill {process.pid}')
                    process.kill()
                    #os.kill(process.pid,9)
                break

            # Aspetta 1 secondo prima di riaprire il processo
            time.sleep(0.1)

if __name__ == "__main__":
    run_strategies()