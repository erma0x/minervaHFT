import zmq
import time

while True:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    message = {'timestamp': time.time(), 'data': 'Hello, world!'}
    socket.send_json(message)
    response = socket.recv_json()
    print(response)
    time.sleep(0.4)