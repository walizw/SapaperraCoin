import time

from crypto.crypto_hash import crypto_hash
from config import MINE_RATE

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
        difficulty = Block.adjust_difficulty (last_block, timestamp)
        nonce = 0
        hash = crypto_hash (timestamp, last_hash, data, difficulty, nonce)

        while hash [0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns ()
            difficulty = Block.adjust_difficulty (last_block, timestamp)
            hash = crypto_hash (timestamp, last_hash, data, difficulty, nonce)

        return Block (timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis ():
        return Block (**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty (last_block, new_timestamp):
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

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
