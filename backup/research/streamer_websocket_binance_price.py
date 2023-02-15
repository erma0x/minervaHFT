import os
import json
import websocket
import requests

# Imposta l'URL del websocket di Binance
WEBSOCKET_URL = "wss://fstream.binance.com/ws/btcusdt@ticker"

ws = websocket.WebSocketApp(WEBSOCKET_URL)

# Apri il websocket
#ws.connect(WEBSOCKET_URL)
  

# Funzione di callback per il ricevimento dei dati dal websocket
def on_message(ws, message):

  # Decodifica il messaggio JSON
  data = json.loads(message)

  # Estrai il prezzo di BTCUSDT dai dati
  price = data["c"] # prezzo di chiusura
  # Stampa il prezzo
  os.system('clear')
  print(f"Prezzo attuale di BTCUSDT: {price}")

# Imposta la funzione di callback per il ricevimento dei dati
ws.on_message = on_message

# Avvia il websocket in modalità asincrona
while True:
  ws.run_forever()

# data example
#{'e': '24hrTicker', 'E': 1671411787327, 's': 'BTCUSDT', 'p': '49.90', 'P': '0.298', 'w': '16733.88', 'c': '16767.30', 'Q': '1.100', 'o': '16717.40', 'h': '16872.00', 'l': '16656.00', 'v': '189640.874', 'q': '3173427964.02', 'O': 1671325380000, 'C': 1671411787322, 'F': 3149060476, 'L': 3150210307, 'n': 1149805}