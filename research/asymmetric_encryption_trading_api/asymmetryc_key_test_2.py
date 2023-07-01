from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import time
import hashlib
import hmac
import http

public_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

url = "/api/v3/account"
method = "GET"

# imposta i parametri della richiesta API
params = {
    "timestamp": int(time.time() * 1000),
    "recvWindow": 5000,
}

# crea la stringa di query concatenando i parametri
query_string = "&".join([f"{k}={v}" for k, v in params.items()])

message_string = f"{method}\n{url}\n{query_string}\n"

print(message_string)

digest = SHA256.new()
digest.update(message_string.encode('utf-8'))


with open ("keyfile.key", "r") as myfile:
    private_key = bytes(myfile.read().encode('utf-8')) #RSA.importKey(myfile.read())

digest_key = SHA256.new()
digest_key.update(private_key)

signature = hmac.new(key=bytes(message_string.encode('utf-8')), msg=digest, digestmod=hashlib.sha256 ).hexdigest()
print(signature)

query_string += f"&signature={signature}"
print(query_string)

conn = http.client.HTTPSConnection("api.binance.com")


headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "X-MBX-APIKEY": signature,
    "recvWindow" : 5000
}

print(conn)

# esegui la richiesta API utilizzando il metodo HTTP, l'endpoint dell'API, la stringa di query e l'intestazione HTTP
conn.request(method, url + "?" + query_string, "", headers)

# ottieni la risposta dalla connessione HTTPS
response = conn.getresponse()

if response.status == 200:
    data = response.read()
    print(data.decode("utf-8"))
    print('SUCCESS!')
else:
    print(f"Request failed with status code {response.status}")

conn.close()