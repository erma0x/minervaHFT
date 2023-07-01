import zmq
import socket
import time
import ast
import numpy as np
import datetime
from datetime import datetime, timedelta
def np_array(input_str):
    input_list = ast.literal_eval(input_str)

    # Convert list of lists to 2D np.array
    output_array = np.array(input_list, dtype = float)
    delete_indices = np.where(output_array[:, 1] == '0.00000000')[0]
    # Eliminiamo le righe
    filtered_data = np.delete(output_array, delete_indices, axis=0)
    return filtered_data

# Setup dei socket

context = zmq.Context()
server_socket = context.socket(zmq.SUB)
server_socket.connect("tcp://127.0.0.1:5550")
server_socket.connect("tcp://127.0.0.1:5551")
server_socket.connect("tcp://127.0.0.1:5552")
server_socket.connect("tcp://127.0.0.1:5553")
server_socket.connect("tcp://127.0.0.1:5554")
server_socket.setsockopt(zmq.SUBSCRIBE, b'')

#server_socket.bind("tcp://*:5560")

# Loop infinito di ricezione e invio
while True:
    # Ricezione dei messaggi
    messages = []
    start_time = time.time()
    while True:
        try:
            # Riceve messaggi da ogni consumer socket
            messages.append(server_socket.recv_string())#flags=zmq.NOBLOCK))
        except zmq.Again:
            # Se non ci sono più messaggi, esce dal loop di ricezione
            pass

        #print(messages)
        elapsed_time = time.time() - start_time
        if elapsed_time > 0.1:# or messages:
            # Se sono passati almeno 0.1 secondi o ci sono messaggi, esce dal loop di ricezione
            break
    
    # Invio dei messaggi ricevuti al producer socket
    for message in messages:
        #try:
            date_format = '%Y-%m-%d %H:%M:%S'
            datetime_object = datetime.strptime(message.split('|')[0], date_format)
            time_difference = datetime.now() - datetime_object
            print(time_difference)
            if time_difference < timedelta(seconds=1) and ast.literal_eval(message.split('|')[1]):
                print(message.split('|')[1])
                ask = np_array(message.split('|')[1])
                bid = np_array(message.split('|')[2])
                
                    # Connessione al socket di destinazione
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.connect(('127.0.0.1', 5560))
                target_socket.sendall('message')
                target_socket.close()
                print(ask)
                print('sended!')

                #except:
                #    pass