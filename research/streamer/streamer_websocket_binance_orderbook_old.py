import os
import json
import websocket
import requests

# Imposta l'URL del websocket di Binance
WEBSOCKET_URL = "wss://fstream.binance.com/ws/btcusdt@depth"

ws = websocket.WebSocketApp(WEBSOCKET_URL)

# Apri il websocket
#ws.connect(WEBSOCKET_URL)
  

# Funzione di callback per il ricevimento dei dati dal websocket
def on_message(ws, message):

  # Decodifica il messaggio JSON
  data = json.loads(message)

  # Estrai il prezzo di BTCUSDT dai dati
  ask = data['a']
  bid = data['b']
  # Stampa il prezzo
  #print(f"Prezzo attuale di BTCUSDT: {price}")

# Imposta la funzione di callback per il ricevimento dei dati
ws.on_message = on_message

# Avvia il websocket in modalità asincrona
while True:
  ws.run_forever()

