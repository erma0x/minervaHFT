import unittest
import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('tests/',''))


import signal
import os
import zmq
from datetime import datetime,timedelta

signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt(zmq.SUBSCRIBE, b'')

START_TIME = datetime.now()
MAX_SECONDS_TRADE_OPEN = 10

counter_messages = 0 
print('Starting')
while True:
    message = socket.recv_multipart()
    counter_messages+=1
    os.system('clear')
        
    print(f"Received: {message}")


    #if message == [b'kill']:
     #   exit()



    print('Test oracle')
    print(f' data      {counter_messages}')  
    print(f' exec time {str(datetime.now()-START_TIME)[:-7]}')


    if message == 'kill': exit()
