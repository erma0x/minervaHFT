#!/usr/bin/env python3

import os
import requests
import time
import hmac
import hashlib
import base64

# Set up authentication:
API_KEY = "k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY"
PRIVATE_KEY_PATH = "keyfile.key"

# Set up the request:

# Set up the request:
API_METHOD = "GET"
API_CALL = "api/v3/account"
API_PARAMS = "recvWindow=5000"


# Load private key:
with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = f.read()

# Sign the request:
timestamp = str(int(time.time() * 1000))

print(f'timestamp {timestamp}')
api_params_with_timestamp = f"{API_PARAMS}&timestamp={timestamp}"
signature = hmac.new(private_key, api_params_with_timestamp.encode(), hashlib.sha256).digest()
signature_b64 = base64.b64encode(signature).decode()

# Send the request:
url = f"https://api.binance.com/{API_CALL}?{api_params_with_timestamp}&signature={signature_b64}"
headers = {'Accept': 'Application/json',"X-MBX-APIKEY": API_KEY}

print(f'URL {url}')
response = requests.request(API_METHOD, url, headers=headers)

# Print response:
print(response.text)