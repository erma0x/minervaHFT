import zmq
import time
context = zmq.Context()
publisher = context.socket (zmq.PUB)
publisher.bind("ipc://nasdaq-feed")


/api/v3/ticker/price

while True:
    message = subscriber.recv()
    publisher.send(message)