from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import requests
import time

query_string = "timestamp=1681303027307"
private_key = "./keyfile.key"
API_KEY = "k8TBbZRX9BieC4LDEwPd2IPsQ0JQ0DdXFCdEthEKn9T2w7AZsLSqX3zPbpsXyCKY"

def rsa_hashing(private_key, payload, passphrase=None):
    with open (private_key, "r") as private_key_file:
        private_key = RSA.importKey(private_key_file.read(), passphrase=passphrase)
    h = SHA256.new(payload.encode("utf-8"))
    signature = pkcs1_15.new(private_key).sign(h)
    return b64encode(signature).decode("utf-8")


print("RSA sign with the string: ")
print(query_string)
print("and return:")
signature = rsa_hashing(private_key, query_string)
print(signature)
print("\n")


API_METHOD = "GET"
API_CALL = "api/v3/account"
API_CALL = "/sapi/v1/account/apiTradingStatus"
API_PARAMS = "recvWindow=60000"
timestamp =str(int(time.time() * 1000))

api_params_with_timestamp = f"{API_PARAMS}&timestamp={timestamp}"

BASE_URL = "https://api.binance.com"
#BASE_URL = 'https://testnet.binance.vision' # testnet base url

url = f"{BASE_URL}/{API_CALL}?{api_params_with_timestamp}&signature={signature}"
headers = {"X-MBX-APIKEY": API_KEY}

print(f' URL        {url}')
print(f' API method {API_METHOD}')
print(f' API call   {API_CALL}')

response = requests.request(API_METHOD, url, headers=headers)
print(response.text)
print(response.status_code)
# Parse the response:
# for balance in response.split('"balance":'):
#     if balance.startswith('"USDT'):
#         usdt_balance = balance.split(',')[0].strip('"')
#         print(f"Your USDT balance: {usdt_balance}")
#         break
# else:
#     print("USDT balance not found in response")