import time
import zmq
import signal

def main():
    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    context = zmq.Context()
    producer_socket = context.socket(zmq.PUB)
    producer_socket.connect("tcp://localhost:5557")

    #fake_streamer(socket=socket)
    producer_socket.send_string("hello")
    time.sleep(3)
    producer_socket.send_string("kill")

if __name__ == "__main__":
    main()