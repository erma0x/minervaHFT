import json
import time
import os
from utils.get_orderbook import get_orderbook

data = get_orderbook()
filepath_orderbook= 'orderbook.txt'
mode = 'a+' if os.path.exists(filepath_orderbook) else 'w+'

with open(filepath_orderbook, mode) as outfile:
    outfile.write(str(data))
    outfile.write("\n")
    outfile.close()