#!/usr/bin/env python3

import os
import subprocess
import time

# Set up authentication:
API_KEY = "k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY"
PRIVATE_KEY_PATH = "keyfile.key"

# Set up the request:
API_METHOD = "GET"
API_CALL = "api/v3/account"
API_PARAMS = "recvWindow=60000"

# Sign the request:
timestamp = str(int(time.time() * 1000))
api_params_with_timestamp = f"{API_PARAMS}&timestamp={timestamp}"
with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = f.read()

signature = subprocess.check_output(
    ["openssl", "dgst", "-sha256", "-sign", "/dev/stdin"],
    input=api_params_with_timestamp.encode(),
    env={"OPENSSL_CONF": "/dev/null"},
    cwd=os.getcwd(),
)
signature = subprocess.check_output(
    ["openssl", "enc", "-base64", "-A"],
    input=signature,
    env={"OPENSSL_CONF": "/dev/null"},
    cwd=os.getcwd(),
).decode().strip()

# Send the request:
curl_cmd = [
    "curl", "-H", f"X-MBX-APIKEY: {API_KEY}", "-X", API_METHOD,
    f"https://api.binance.com/{API_CALL}?{api_params_with_timestamp}",
    "--data-urlencode", f"signature={signature}"
]
response = subprocess.check_output(curl_cmd).decode().strip()

# Parse the response:
for balance in response.split('"balance":'):
    if balance.startswith('"USDT'):
        usdt_balance = balance.split(',')[0].strip('"')
        print(f"Your USDT balance: {usdt_balance}")
        break
else:
    print("USDT balance not found in response")