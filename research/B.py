import zmq

context = zmq.Context()

def producer():
    producer_socket = context.socket(zmq.PUSH)
    producer_socket.connect("tcp://localhost:5557")
    producer_socket.send_string("Hello from B.py")

if __name__ == '__main__':
    producer()