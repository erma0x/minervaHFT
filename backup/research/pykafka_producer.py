from pykafka import KafkaClient
import pandas as pd
import sqlite3
from configuration_backtest import MOCK_ORDERBOOK_DATABASE_PATH
import time
import os
import pickle
import json

def generator_name(array):
    # statements
    yield array

def get_orderbook_mock(database_path):
    """
    SELECT (SELECT COUNT(*)
    FROM main AS t2
    WHERE t2.col1 < t1.col1) + (SELECT COUNT(*)
    FROM main AS t3
    WHERE t3.col1 = t1.col1 AND t3.col1 < t1.col1) AS rowNum, * FROM Table_name t1  WHERE rowNum=0 ORDER BY t1.col1 ASC
    """

    conn = sqlite3.connect(database_path)

    # Crea il cursore per eseguire le query
    cursor = conn.cursor()
    QUERY = """SELECT * FROM objects"""
    results = pd.read_sql_query(QUERY,con=conn)
    return results


if __name__ == "__main__":

    client = KafkaClient(hosts="localhost:9092")
    topic = client.topics['orderbook']
    producer = topic.get_sync_producer()

    orderbook = get_orderbook_mock(database_path=MOCK_ORDERBOOK_DATABASE_PATH)
    ask_generator = (item for item in orderbook.ask)
    bid_generator = (item for item in orderbook.bid)
    time_generator = (item for item in orderbook.timestamp)
    #book = (item for item in orderbook.ask)
    counter = 0
    while True:
        try:
            os.system('clear')
            counter+=1
            print(f'\n\t Orderbook backtester with pykafka server\n')
            print(f'\n\t backtested data {counter} = {round(counter*0.4/60,2)} minutes')
            
            ask = next(ask_generator)
            bid = next(bid_generator)
            timestamp = next(time_generator)
            
            datapoint_orderbook = {"timestamp":timestamp,"ask":ask,"bid":bid}
            my_list_bytes = json.dumps(datapoint_orderbook)
            producer.produce(my_list_bytes)


        except StopIteration as stop_error:
            print(f'\n\t END data generation!')
        finally:
            time.sleep(0.4)