import zmq
import time
import hashlib

class BlockchainNode:
    def __init__(self, port):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % self.port)
        self.chain = []

    def run(self):
        while True:
            message = self.socket.recv_json()
            self.handle_message(message)
            print(self.chain)

    def handle_message(self, message):
        timestamp = message['timestamp']
        data = message['data']
        previous_hash = self.get_previous_hash()
        hash = self.calculate_hash(timestamp, data, previous_hash)
        block = {'timestamp': timestamp, 'data': data, 'previous_hash': previous_hash, 'hash': hash}
        self.chain.append(block)
        self.socket.send_json({'status': 'OK'})

    def get_previous_hash(self):
        if len(self.chain) == 0:
            return '0'
        else:
            return self.chain[-1]['hash']

    def calculate_hash(self, timestamp, data, previous_hash):
        hash_string = str(timestamp) + str(data) + str(previous_hash)
        hash = hashlib.sha256(hash_string.encode()).hexdigest()
        return hash
    
node = BlockchainNode(5555)
node.run()