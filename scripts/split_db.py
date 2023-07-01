import pandas as pd
import sqlite3
import os
db_files = [f for f in os.listdir('.') if f.endswith('.db')]

def get_db_files(directory):
    db_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".db"):
            db_files.append(os.path.join(directory, filename))
    return db_files

db_files = get_db_files('/home/ephemeral/Documents/minervaHFT/minerva/databases/big')
for input_file in db_files:
    # Imposta il nome del file di input
    #input_file = "minerva/databases/big/orderbook_2023-02-17_14:00.db"
    orderbook_name =  input_file.split('/')[-1][:-3]
    table_name = "BTCUSDT"  # Imposta il nome della tabella da dividere
    rows_per_file = 2500   # Imposta il numero di righe per file

    # Crea la cartella per i file di output se non esiste
    if not os.path.exists("output_parquet"):
        os.makedirs("output_parquet")

    # Connette al database e seleziona la tabella
    conn = sqlite3.connect(input_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]

    # Legge la tabella in blocchi di dimensione rows_per_file e salva ciascun blocco in un file .parquet
    def create_folder(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    id_counter = 0
    for i in range(0, row_count, rows_per_file):
        
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {rows_per_file} OFFSET {i}", conn)
        create_folder("minerva/databases/big_test_parquet3/")
        output_file = f"minerva/databases/big_test_parquet3/{orderbook_name}_{table_name}_{id_counter}.parquet"
        id_counter+=1
        df.to_parquet(output_file)
        print(f'database split completed part {id_counter}')

    # Chiude la connessione al database
    cursor.close()
