import zmq
import time
context = zmq.Context()

subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://192.168.55.112:5556")
subscriber.connect("tcp://192.168.55.201:7721")
subscriber.setsockopt(zmq.SUBSCRIBE, "NASDAQ")

publisher = context.socket(zmq.PUB)
publisher.bind("ipc://nasdaq-feed")

while True:
    message = subscriber.recv()
    publisher.send(message)
