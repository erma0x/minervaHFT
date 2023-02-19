from configuration_backtest import ORACLE_URL
import zmq
import time

if __name__ == '__main__':

    contex_oracle = zmq.Context()
    socket_oracle = contex_oracle.socket(zmq.SUB)
    socket_oracle.connect(ORACLE_URL)
    socket_oracle.subscribe("")  # Subscribe to all topics

    print("Starting receiver loop ...")
    while True:
        msg = socket_oracle.recv_string()
        print("msg")
