#!/usr/bin/env python3
import unittest
import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(str(PROJECT_PATH))


from minerva.configuration_backtest import ORDERBOOK_BACKTESTING_FOLDER

from minerva.streamer import get_file_date, get_orderbook_database, get_filepaths_list

from datetime import datetime

REAL_PATH = ORDERBOOK_BACKTESTING_FOLDER.replace('tests','minerva')
print(REAL_PATH)

list_of_database_files = get_filepaths_list(filepath_to_check=REAL_PATH)
print(list_of_database_files)

sorted_filepaths = sorted(list_of_database_files, key=get_file_date)

print(sorted_filepaths)

# for file_db in sorted_filepaths:
#     orderbook = get_orderbook_database(database_path = file_db)

