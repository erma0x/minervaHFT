
import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

""" This is a very simple script working on Binance API
- work with USER_DATA endpoint with no third party dependency
- work with testnet
Provide the API key and secret, and it's ready to go
Because USER_DATA endpoints require signature:
- call `send_signed_request` for USER_DATA endpoints
- call `send_public_request` for public endpoints
```python
python spot.py
```
"""

KEY = "k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY"
PRIVATE_KEY_PATH = "keyfile.key"
SECRET = ""

with open(PRIVATE_KEY_PATH, "r") as f:
    SECRET = f.read()

#BASE_URL = "https://api.binance.com"  # production base url
BASE_URL = 'https://testnet.binance.vision' # testnet base url

""" ======  begin of functions, you don't need to touch ====== """

import hmac
import hashlib
from Crypto.PublicKey import RSA

def sign_with_rsa(file_path, message):
    with open(file_path, "rb") as key_file:
        private_key = RSA.import_key(key_file.read())

    message_bytes = message.encode("utf-8")
    signature = hmac.new(private_key.export_key(), message_bytes, hashlib.sha256).hexdigest()

    return signature


def hashing(query_string):
    return hmac.new(bytes(SECRET.encode("utf-8")), query_string.encode("utf-8"), hashlib.sha256).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request("GET")(url=url)
    return response.json()


# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + sign_with_rsa(PRIVATE_KEY_PATH,query_string) #hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()



response = send_signed_request("GET", "/api/v3/account")
print(response)
