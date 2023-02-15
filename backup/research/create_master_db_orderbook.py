import sqlite3
import json
from configuration_backtest import ORDERBOOK_DATABASE

# Crea una nuova connessione al database
conn = sqlite3.connect(ORDERBOOK_DATABASE)

# Crea il cursore per eseguire le query
cursor = conn.cursor()

# Crea la tabella 'objects' nel database
cursor.execute("CREATE TABLE objects (timestamp REAL PRIMARY KEY, ask TEXT, bid TEXT)")

# Commit delle modifiche al database
conn.commit()

# Chiudi la connessione al database
conn.close()
