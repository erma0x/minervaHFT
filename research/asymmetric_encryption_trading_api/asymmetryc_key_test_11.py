import hashlib
import hmac
import time
import requests
from Crypto.PublicKey import RSA

api_key = 'k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY'

# with open("keyfile.key", "r") as f:
#     secret_key = RSA.import_key(f.read())

with open("keyfile.key", 'rb') as f:
    secret_key = f.read()


base_url = 'https://api.binance.com'

# Define the API endpoint and parameters
endpoint = '/api/v3/account'
params = {
    'timestamp': int(time.time() * 1000)
}

# Add the API key to the parameters
params['recvWindow'] = 60000
params['apiKey'] = api_key


# Generate the query string from the parameters
query_string = '&'.join([f"{k}={v}" for k, v in params.items()])

# Generate the signature using the secret key
signature = hmac.new(secret_key, query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Add the signature to the parameters
params['signature'] = signature

# Make the API request
response = requests.get(f"{base_url}{endpoint}", params=params)

# Print the response
print(response.json())

