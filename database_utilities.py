#!/usr/bin/env python3

import os
import json
import time
from decimal import Decimal
import sqlite3

def dropzeros(number):
    # e.g 22000 --> Decimal('2.2E+4')
    mynum = Decimal(number).normalize()
    return mynum.__trunc__() if not mynum % 1 else float(mynum)


def give_nice_data(ask_or_bid):
  """ask or bid lists with a lot of zeroes"""
  new_data = []
  squares_generator = ([dropzeros(i[0]),dropzeros(i[1])] for i in ask_or_bid)
  for i in squares_generator:
    new_data.append(i)
  return(new_data)


def create_database(database_path):
    connection_sql_database = sqlite3.connect(database_path)
    cursor = connection_sql_database.cursor()

    cursor.execute("CREATE TABLE BTCUSDT (timestamp REAL PRIMARY KEY, ask TEXT, bid TEXT)")

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
    if not os.path.isfile(database_path):
      create_database(database_path)
    # Crea una nuova connessione al database
    connection_sql_database = sqlite3.connect(database_path)

    # Crea il cursore per eseguire le query
    cursor = connection_sql_database.cursor()

    new_ask = give_nice_data(ask_or_bid = ask)
    new_bid = give_nice_data(ask_or_bid = bid)

    timestamp = time.time()
    cursor.execute("INSERT INTO BTCUSDT (timestamp, ask, bid) VALUES (?, ?, ?)", (timestamp, json.dumps(new_ask),json.dumps(new_bid)))

    connection_sql_database.commit()
    connection_sql_database.close()