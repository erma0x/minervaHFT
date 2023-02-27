import time
import subprocess
import zmq
import threading
import os
import psutil

context = zmq.Context()

def consumer(process):
    consumer_socket = context.socket(zmq.PULL)
    consumer_socket.bind("tcp://*:5557")
    while True:
        msg = consumer_socket.recv_string()
        print(msg)
        if msg == "end":
            print(f'kill {process.pid}')
            os.kill(process.pid,9)
            break
            
def main():

    for i in range(5):
        #p1 = subprocess.Popen(['python3', 'B.py'])
        process_ = subprocess.Popen(['python3', 'C.py'])

        consumer_thread = threading.Thread(target=consumer, args=(process_,))
        consumer_thread.start()
        streaming = True
        # Resta in attesa del messaggio "end"
        while streaming:
            time.sleep(0.01)
            if not psutil.pid_exists( process_.pid ):
                streaming = False


            

if __name__ == '__main__':
    main()