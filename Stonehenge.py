import hashlib
import json
from time import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash='1', nonce=100)  # Create the genesis block

    def create_block(self, nonce, previous_hash=None):
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash or self.chain[-1].compute_hash(),
            timestamp=time(),
            transactions=self.transactions,
            nonce=nonce
        )
        self.transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.transactions.append(Transaction(sender, recipient, amount))
        return self.get_last_block().index + 1

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    def is_valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def mine_block(self):
        last_block = self.get_last_block()
        last_proof = last_block.nonce
        proof = self.proof_of_work(last_proof)
        self.add_transaction(sender='0', recipient='miner_address', amount=1)  # Reward for mining
        self.create_block(proof, last_block.compute_hash())
        return self.get_last_block()

# Example usage
blockchain = Blockchain()
print("Blockchain created with genesis block.")

blockchain.add_transaction(sender='Alice', recipient='Bob', amount=10)
blockchain.add_transaction(sender='Bob', recipient='Charlie', amount=5)

mined_block = blockchain.mine_block()
print(f"New block mined: {mined_block.__dict__}")

print("Blockchain:")
for block in blockchain.chain:
    print(block.__dict__)