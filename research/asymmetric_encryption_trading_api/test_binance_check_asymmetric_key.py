from Crypto.PublicKey import RSA
from OpenSSL import SSL
import socket
import hashlib
import os

import http.client
import urllib.parse
import json
import time
import hashlib
import hmac
import base64

# leggi la chiave pubblica dal file "keyfile.pub"
#with open("keyfile.pub", "r") as f:
#    public_key = f.read().strip()

public_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

# leggi la chiave privata dal file "keyfile.key"
with open("keyfile.key", "r") as f:
    private_file = f.read()#.decode('hex')[::-1].encode('hex')
    private_key = RSA.construct((private_file,16))
    print(private_key)
    #private_key = RSA.importKey(private_file)

#print(private_key)


# definisci l'endpoint dell'API di Binance e il metodo HTTP
url = "/api/v3/account"
method = "GET"

# imposta i parametri della richiesta API
params = {
    "timestamp": int(time.time() * 1000),
    "recvWindow": 5000,
}

# crea la stringa di query concatenando i parametri
query_string = "&".join([f"{k}={v}" for k, v in params.items()])

# crea la stringa di messaggio concatenando il metodo HTTP, l'endpoint dell'API, la stringa di query e il corpo della richiesta (vuoto)
message_string = f"{method}\n{url}\n{query_string}\n"

# crea l'hash SHA256 della stringa di messaggio utilizzando la chiave privata
#signature = hmac.new(private_key.encode(), message_string.encode(), hashlib.sha256).hexdigest()
signature = hmac.new(key=private_key, message_string, digestmod=hashlib.sha256).hexdigest()

# aggiungi la firma alla stringa di query
query_string += f"&signature={signature}"

# crea la connessione HTTPS a api.binance.com
conn = http.client.HTTPSConnection("api.binance.com")

# crea l'intestazione HTTP con la chiave pubblica
headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "X-MBX-APIKEY": public_key,
}

# esegui la richiesta API utilizzando il metodo HTTP, l'endpoint dell'API, la stringa di query e l'intestazione HTTP
conn.request(method, url + "?" + query_string, "", headers)

# ottieni la risposta dalla connessione HTTPS
response = conn.getresponse()

# stampa la risposta se la richiesta ha avuto successo
if response.status == 200:
    data = response.read()
    print(data.decode("utf-8"))
    print('SUCCESS!')
else:
    print(f"Request failed with status code {response.status}")

# chiudi la connessione HTTPS
conn.close()
