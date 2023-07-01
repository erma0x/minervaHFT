import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5555")

while True:
    message = """{'index':51,'timestamp':16024201,'data':{'a':[[100,0.1]],'b':[[120,0.2]]},'previous_hash':'B6C86A70AFFC6F7AA32B057DBC3BC4106410557ECD26EB63D1D0F353DB9212FE'}"""
    socket.send_string(message)
    time.sleep(0.4)