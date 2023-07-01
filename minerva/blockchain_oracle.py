import zmq
import hashlib
import json

# DublinKetchup89 hash iniziale
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        #block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(str(self.data).encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "01/01/2022", "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def main():
    context = zmq.Context()

    # Node 1
    node1_socket = context.socket(zmq.PULL)
    node1_socket.bind("tcp://*:5555")

    # Node 2
    node2_socket = context.socket(zmq.PULL)
    node2_socket.bind("tcp://*:5556")

    blockchain = Blockchain()

    while True:
        # Node 1 receives a new block from Node 2
        message = node1_socket.recv()
        print("NODE 1")
        new_block = eval(message) #json.loads(message.decode('utf-8'))
        new_block["hash"] = hashlib.sha256(str(new_block).encode()).hexdigest()
        print(new_block)
        blockchain.add_block(Block(new_block["index"], new_block["timestamp"], new_block["data"], new_block["previous_hash"]))
        #node1_socket.send(b"Block added to Node 1's blockchain.")

        # Node 2 receives a new block from Node 1
        print("NODE 2")
        message = node2_socket.recv()
        new_block = eval(message) #json.loads(message.decode())
        new_block["hash"] = hashlib.sha256(str(new_block).encode()).hexdigest()
        print(new_block)
        blockchain.add_block(Block(new_block["index"], new_block["timestamp"], new_block["data"], new_block["previous_hash"]))
        #node2_socket.send(b"Block added to Node 2's blockchain.")

if __name__ == '__main__':
    main()