# app/blockchain/blockchain.py
# Simple Blockchain Audit Ledger (persistent)

import json
import time
import os
from app.core.sha256 import sha256
from app.core.merkle import merkle_root

BLOCKCHAIN_FILE = "app/data/blockchain.json"


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0, hash_value=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = merkle_root(transactions)
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash_value or self.compute_hash()

    def compute_hash(self):
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.transactions) +
            str(self.merkle_root) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return sha256(block_string.encode())


class Blockchain:
    difficulty = 3

    def __init__(self, filename="app/data/blockchain.json"):
        self.filename = filename
        self.chain = []

        if os.path.exists(self.filename):
            self.load()
        else:
            self.create_genesis_block()
            self.save()

    def load(self):
        with open(self.filename, "r") as f:
            data = json.load(f)

        self.chain = []
        for b in data:
            block = Block(
                b["index"],
                b["timestamp"],
                b["transactions"],
                b["previous_hash"],
                b["nonce"]
            )
            block.hash = b["hash"]
            self.chain.append(block)

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith("0" * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        block.hash = computed_hash
        return block.hash

    def add_block(self, transactions):
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.last_block().hash
        )

        self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.save()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def save(self):
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)
