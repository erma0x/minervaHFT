import zmq

# Crea un socket di tipo server
context = zmq.Context()
server_socket = context.socket(zmq.PULL)
server_socket.bind("tcp://*:5550")

# Crea un socket di destinazione
destination_socket = context.socket(zmq.PUSH)
destination_socket.connect("tcp://localhost:5560")

while True:
    # Riceve il messaggio dal socket del server
    message = server_socket.recv_string()
    print(f"Server ricevuto il messaggio: {message}")

    # Riproietta il messaggio al socket di destinazione
    destination_socket.send_string(message)
    print(f"Server ha inoltrato il messaggio al destinatario: {message}")

