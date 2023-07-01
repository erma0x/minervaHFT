import zmq
import time


# Crea un socket di tipo server
context = zmq.Context()
# Crea un socket di destinazione
destination_socket = context.socket(zmq.PUSH)
destination_socket.connect("tcp://localhost:5561")

while True:
    message = 'example'
    # Riproietta il messaggio al socket di destinazione
    destination_socket.send_string(message)
    #print(f"Server ha inoltrato il messaggio al destinatario: {message}")
    time.sleep(0.4)