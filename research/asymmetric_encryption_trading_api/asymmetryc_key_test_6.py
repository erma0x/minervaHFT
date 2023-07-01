#!/usr/bin/env python3

import os
import requests
import time
import hmac
import hashlib
import base64

timestamp =str(int(time.time() * 1000))

API_KEY = "k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY"
PRIVATE_KEY_PATH = "keyfile.key"

with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = f.read()

API_METHOD = "GET"
API_CALL = "api/v3/account"
API_PARAMS = "recvWindow=5000"

api_params_with_timestamp = f"{API_PARAMS}&timestamp={timestamp}"


query_string = f'timestamp={timestamp}'

def hashing(query_string,secret):
    return hmac.new(secret, query_string.encode("utf-8"), hashlib.sha256).hexdigest()


signature = hashing() #hmac.new(private_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
signature_b64 = base64.b64encode(signature).decode()


# Send the request:
url = f"https://api.binance.com/{API_CALL}?{api_params_with_timestamp}&signature={signature_b64}"
headers = {'Accept': 'Application/json',"X-MBX-APIKEY": API_KEY}

print(f'URL {url}')
response = requests.request(API_METHOD, url, headers=headers)

# Print response:
print(response.text)