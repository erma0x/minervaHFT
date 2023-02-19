#!/usr/bin/env python3

import threading
import subprocess
import os

from configuration_backtest import ROOT_PATH, STRATEGIES_FOLDER


def run_oracle(file):
    cmd = f"python3 oracle.py --s {file}"
    subprocess.call(cmd, shell=True)


def run_streamer():
    cmd = f"python3 streamer.py"
    subprocess.call(cmd, shell=True)


def find_files(path):
    file_list = []
    files = os.scandir(path)
    for file in files:
        if '__' not in str(file): 
            file_list.append(os.path.join(file))
    return file_list


def run_strategies():
    files = find_files(STRATEGIES_FOLDER)
    threads = []
    for file in files:
        t = threading.Thread(target=run_oracle, args=(file,))

        EXEC_IMPORT_STRING=f"""from {file.replace(ROOT_PATH,'').replace('.py','').replace('/','.').replace('.runs','runs')} import *"""
        #print('---> ',EXEC_IMPORT_STRING)
        exec(EXEC_IMPORT_STRING)       
        t.start()
        threads.append(t)

    t = threading.Thread(target=run_streamer)
    t.start()
    threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    run_strategies()