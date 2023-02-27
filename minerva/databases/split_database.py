import os
import sqlite3

# Apri la connessione al database
conn = sqlite3.connect('database.db')

# Esegui una query per contare il numero di righe nella tabella BTCUSDT
query = "SELECT COUNT(*) FROM BTCUSDT"
cursor = conn.cursor()
cursor.execute(query)
num_rows = cursor.fetchone()[0]
print(f"Numero di righe nella tabella BTCUSDT: {num_rows}")

# Dividi i dati in file da 5000 righe o meno
chunk_size = 5000
offset = 0
while offset < num_rows:
    # Esegui una query per selezionare le righe dal database
    query = f"SELECT * FROM BTCUSDT LIMIT {chunk_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Scrivi le righe in un nuovo file
    filename = f"BTCUSDT_{offset // chunk_size}.csv"
    with open(filename, 'w') as f:
        for row in rows:
            row_str = ','.join(str(x) for x in row)
            f.write(row_str + '\n')

    # Incrementa l'offset
    offset += chunk_size

# Chiudi la connessione al database
conn.close()

# Sposta i file nella cartella
os.makedirs('output', exist_ok=True)
for filename in os.listdir('.'):
    if filename.startswith('BTCUSDT_'):
        os.rename(filename, os.path.join('output', filename))