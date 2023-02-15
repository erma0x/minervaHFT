import signal
import zmq


signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt(zmq.SUBSCRIBE, b'status')

while True:
    message = socket.recv_multipart()
    print(f'Received: {message}')
