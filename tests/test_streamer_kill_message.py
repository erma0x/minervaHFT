import signal
import time
import zmq
from datetime import datetime,timedelta


signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')

for i in range(50):
    socket.send(b'test')
    socket.send(b'kill')
    time.sleep(0.01)