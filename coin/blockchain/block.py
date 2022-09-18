import time
from crypto.crypto_hash import crypto_hash

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "and there were nothing...",
    "hash": "until we created light!",
    "data": [],
    "difficulty": 3,
    "nonce": "genesis_nonce"
}

class Block ():
    def __init__ (self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

        self.difficulty = difficulty
        self.nonce = nonce

    @staticmethod
    def mine_block (last_block, data):
        timestamp = time.time_ns ()
        last_hash = last_block.hash
        difficulty = last_block.difficulty
        nonce = 0
        hash = crypto_hash (timestamp, last_hash, data, difficulty, nonce)

        while hash [0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns ()
            hash = crypto_hash (timestamp, last_hash, data, difficulty, nonce)

        return Block (timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis ():
        return Block (**GENESIS_DATA)

    def __repr__ (self):
        return (
            "{\n"
            f"\t\"timestamp\": \"{self.timestamp}\"\n"
            f"\t\"last_hash\": \"{self.last_hash}\"\n"
            f"\t\"hash\": \"{self.hash}\"\n"
            f"\t\"data\": {self.data}\n"
            f"\t\"difficulty\": {self.difficulty}\n"
            f"\t\"nonce\": {self.nonce}\n"
            "}"
        )
