import signal
import zmq
import numpy as np
import pandas as pd

signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt(zmq.SUBSCRIBE, b'')

ask_orderbook = pd.DataFrame(columns = ['price', 'volume'])

while True:
    message = socket.recv()
    timestamp = message.decode().split('|')[0]
    ask = message.decode().split('|')[1]
    
    obj_list = message.decode().split('|')
    data_timestamp = obj_list[0]
    ask = obj_list[1]
    bid = obj_list[2]

    ask_array = np.zeros((100,2), dtype=float, order='C')
    bid_array = np.zeros((100,2), dtype=float, order='C')

    for element in ask.split('['):
        raw_list = element.replace('[','').replace(']','')
        object_list = raw_list.split(',')
        if len(object_list)>=2:
            price = float(object_list[0])
            volume = float(object_list[1])
            new = np.array([volume,price])
            ask_array = np.vstack((ask_array, new ))

    for element in bid.split('['):
        raw_list = element.replace('[','').replace(']','')
        object_list = raw_list.split(',')
        if len(object_list)>=2:
            price = float(object_list[0])
            volume = float(object_list[1])
            new = np.array([volume,price])
            bid_array = np.vstack((bid_array, new ))

    print(bid_array)
    # print 
    # oracle ->