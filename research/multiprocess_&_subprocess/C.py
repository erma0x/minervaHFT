import time
import zmq

context = zmq.Context()

def producer():
    producer_socket = context.socket(zmq.PUSH)
    producer_socket.connect("tcp://localhost:5557")
    producer_socket.send_string("Hello from C.py")

    time.sleep(5)  # Attende 5 secondi
    producer_socket.send_string("end")
    producer_socket.close()

if __name__ == '__main__':
    producer()