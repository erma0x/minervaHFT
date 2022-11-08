klines_required = False
KLINES_FILE = 'history_required.txt'

with open(KLINES_FILE,'r') as f:
    if f.readlines():
        print('do work')

with open(KLINES_FILE,'+w') as f:
    f.write('')