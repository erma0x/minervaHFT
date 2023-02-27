import time
import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5555")

    GENERATIONS = 5
    for generation_number in GENERATIONS:
        for i in range(5):
            time.sleep(2)
            message = "Message from producer: {}".format(i)
            socket.send_string(message)

        socket.send_string("end")

if __name__ == '__main__':
    main()