import zmq

# Crea un socket di tipo server
context = zmq.Context()
server_socket = context.socket(zmq.PULL)
server_socket.bind("tcp://*:5550")
# server_socket.bind("tcp://*:5551")
# server_socket.bind("tcp://*:5552")
# server_socket.bind("tcp://*:5553")
# server_socket.bind("tcp://*:5553")

# Crea un socket di destinazione
destination_socket = context.socket(zmq.PUSH)
destination_socket.connect("tcp://localhost:5560")

while True:
    message = server_socket.recv_string()
    print(f"Server ricevuto il messaggio: {message}")
    destination_socket.send_string(message)
    print(f"Server ha inoltarato il messaggio al destinatario: {message}")