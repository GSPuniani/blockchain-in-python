from crypt import methods
import hashlib
import json
from time import time
import flask
# from numpy import block
import requests

class Blockchain(object):
    def __init__(self):
        # The Blockhain
        self.chain = []
        # List of transactions
        self.current_transactions = []
        # Genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, proof, previous_hash = None):
        """Creates new blocks and adds them to the existing chain."""
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }
        # Set the current transaction list to empty
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self):
        """Adds a new transaction to already existing transactions."""
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """Hashes a block with SHA-256 and orders the dictionary."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        """Calls and returns the last block of the chain."""
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """Implementation of consensus algorithm."""
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """Validates the block."""
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Create the app node
app = Flask(__name__)
node_identifier = str(uuid4()).replace("-", "")

# Initialize the blockchain
blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine():
    return "Mining a new block"




    