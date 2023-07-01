import zmq

# Crea un socket di tipo server
context = zmq.Context()
server_socket = context.socket(zmq.PULL)
server_socket.bind("tcp://*:5560")

while True:
    message = server_socket.recv_string()
    print(f"fake oracle ha ricevuto il messaggio: {message}")