import time
import subprocess
import zmq
import threading
import os

context = zmq.Context()
GENERATIONS = 5
def consumer(processes):

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:5555")

    count = 0
    while True:
        message = socket.recv_string()
        if message == "end":
            for process in processes:
                print('killing processes')
                os.kill(process.pid,9)
            
            count+=1
            if count == GENERATIONS: 
                socket.close()
                socket = context.socket(zmq.PULL)
                socket.connect("tcp://127.0.0.1:5555")
                exit()
        else:
            print("Received message: {}".format(message))

def main():

    processes_list = []

    for i in range(5):
        p = subprocess.Popen(['python3', 'multiprocess_producer_streamer_1.py'])
        processes_list.append(p)

    consumer_thread = threading.Thread(target=consumer, args=(processes_list,),shell=True)
    consumer_thread.start()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()

import zmq
