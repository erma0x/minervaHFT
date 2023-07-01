#!/usr/bin/env python3

import os
import json
import time
from decimal import Decimal
import sqlite3
from datetime import datetime
from configuration_backtest import SQL_DB_TIME
from configuration_trading import MARKET

def dropzeros(number):
  """drop the zeroes of the given number

  Args:
      number (float or int): number to drop zeroes from : e.g 22000 

  Returns:
      number (float or int): number with scientific notation : e.g Decimal('2.2E+4')
  """
  mynum = Decimal(number).normalize()
  return mynum.__trunc__() if not mynum % 1 else float(mynum)


def give_nice_data(ask_or_bid):
  """
  remove zeroes from the data
  Args:
      ask_or_bid: (list) ask or bid lists of lists with a lot of zeroes
  Returns:
      ask_or_bid: (list) ask or bid lists of lists without zeroes
  """
  new_data = []
  squares_generator = ([dropzeros(i[0]),dropzeros(i[1])] for i in ask_or_bid)
  for i in squares_generator:
    new_data.append(i)
  return(new_data)


def create_database(database_path):
    """
    creates a database

    Args:
        database_path (string): database file directory path "./databases/orderbook.db"
    """
    connection_sql_database = sqlite3.connect(database_path)
    cursor = connection_sql_database.cursor()

    cursor.execute(f"CREATE TABLE {MARKET} (timestamp REAL PRIMARY KEY, ask TEXT, bid TEXT)")

    connection_sql_database.commit()
    connection_sql_database.close()


def orderbook_storage(ask,bid,database_path):
    """
    Save the orderbook (timestamp,ask,bid) with SQLlite3 database 

    Args:
        ask (list): list of [[ask_price_level_1,quantity_level_1],[ask_price_level_2,quantity_level_2]]
        bid (list): list of [[bid_price_level_1,quantity_level_1],[bid_price_level_2,quantity_level_2]]
        database_path (str): the databasepath as string example: "home/user/project/orderbook_BTC_USDT.db".
    """
    database_path = f"orderbook_{str(datetime.now())[:SQL_DB_TIME].replace(' ','_')}.db" # minutes

    if not os.path.isfile(database_path):
      create_database(database_path)

    connection_sql_database = sqlite3.connect(database_path)
    cursor = connection_sql_database.cursor()

    new_ask = give_nice_data(ask_or_bid = ask)
    new_bid = give_nice_data(ask_or_bid = bid)

    timestamp = time.time()
    cursor.execute(f"INSERT INTO {MARKET} (timestamp, ask, bid) VALUES (?, ?, ?)", (timestamp, json.dumps(new_ask),json.dumps(new_bid)))

    connection_sql_database.commit()
    connection_sql_database.close()