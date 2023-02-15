#!/usr/bin/env python3

import threading
import subprocess
import os

from configuration_backtest import ROOT_PATH


def run_file(file):
    cmd = f"python3 oracle.py --s ./strategies/{file}"
    subprocess.call(cmd, shell=True)


def find_files(path):
    file_list = []
    files = os.scandir(path)
    for file in files:
        if '__' not in str(file): 
            file_list.append(os.path.join(file))
    return file_list


def run_strategies():
    files = find_files(ROOT_PATH+'/strategies/')
    threads = []
    for file in files:
        t = threading.Thread(target=run_file, args=(file,))

        EXEC_IMPORT_STRING=f"""from {file.replace(ROOT_PATH,'').replace('.py','').replace('/','.').replace('.st','st')} import *"""
        exec(EXEC_IMPORT_STRING)       

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# if __name__ == "__main__":
#     run_strategies()