from binance.client import Client

# Inserisci le tue chiavi API e segrete qui
api_key = "Er7Ua2ZqgH2CwWC3mVMkPXyc6nhtZURQKobesJ2Vmq5mDs74dB3iiOTli5B0QdTt"
api_secret = "Qp4Gvgl2XIionrAlFVdyKOBR08e4qjbw8kS7emBlcYjcT1nmEHxS7XgFioud7nRS"

# Crea un oggetto client per l'API di Binance
client = Client(api_key, api_secret)

# Ottieni il balance del tuo account di BNB
balance = client.get_asset_balance(asset='USDT')

# Stampa il balance del tuo account di BNB
print(f" Balance: {balance}")
