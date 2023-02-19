#!/usr/bin/env python3

import time
import argparse
import sys, os

ROOT_PATH = sys.path[0]


# update single performace value in python file
def update_performance(performance,performance_name, absolute_path,relative_path):
    with open(absolute_path, "r") as file:
        contents = file.readlines()
        for i in range(len(contents)):
            if performance_name in contents[i]:
                contents[i] = f"{performance_name} = {performance}"

    with open(absolute_path, "w") as file:
        file.writelines(contents)
    
    EXEC_IMPORT_STRING=f"""from {relative_path.replace('/','.').replace('.py','').replace('.st','st')} import *"""
    #print("EXECUTION STRING: " + EXEC_IMPORT_STRING)
    exec(EXEC_IMPORT_STRING)



if __name__ == '__main__':
        
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strategy_path", type=str, default='/strategies/s1.py', help="python stategy configuration file path for backtesting and optimization")

    args = parser.parse_args()

    ABSOLUTE_STRATEGY_PATH =  ROOT_PATH + args.strategy_path
    STRATEGY_PATH = args.strategy_path
   

    if os.path.exists(ABSOLUTE_STRATEGY_PATH):
        EXEC_IMPORT_STRING=f"""from {STRATEGY_PATH.replace('.py','').replace('/','.').replace('.st','st')} import *"""

        print(f"Running strategy configuration => {STRATEGY_PATH}")
        print(f"Execution string => {EXEC_IMPORT_STRING}")

        exec(EXEC_IMPORT_STRING)
            
        print(f"Market imported => {MARKET}")
        
        update_performance(performance=17 ,performance_name = "GAIN_PERCENTAGE_24H" , absolute_path = ABSOLUTE_STRATEGY_PATH, relative_path = STRATEGY_PATH)
        
    else:
        print("Nothing to import")


#update_performance(101,'GAIN_PERCENTAGE_24H',STRATEGY_PATH)