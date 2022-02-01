from crypt import methods
import hashlib
import json
from time import time
from urllib import response
from flask import Flask, request
# from numpy import block

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

    def new_transaction(self, sender, recipient, amount):
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
    # Employ proof of work algorithm
    last_block = blockchain.last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    # Reward the miner
    blockchain.new_transaction(sender = "0", recipient = node_identifier, amount = 1)
    # Create the new block and add it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        "message": "The new block has been forged.",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    # Check if required data is present
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values", 400
    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f"Transaction is scheduled to be added to Block No. {index}"}
    return jsonify, 201

@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


    