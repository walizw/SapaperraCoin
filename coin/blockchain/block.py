import time

from crypto.crypto_hash import crypto_hash
from crypto.hex_to_binary import hex_to_binary

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

        while hex_to_binary (hash) [0:difficulty] != "0" * difficulty:
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

    @staticmethod
    def is_valid_block (last_block, new_block):
        if new_block.last_hash != last_block.hash:
            raise Exception ("The new block last_hash must be correct.")

        if hex_to_binary (new_block.hash) [0:new_block.difficulty] != "0" * new_block.difficulty:
            raise Exception ("The proof-of-work requirement was not met.")

        if abs (last_block.difficulty - new_block.difficulty) > 1:
            raise Exception ("Difficulty should be adjusted just by one.")

        reconstructed_hash = crypto_hash (
            new_block.timestamp,
            new_block.last_hash,
            new_block.data,
            new_block.nonce,
            new_block.difficulty
        )

        if new_block.hash != reconstructed_hash:
            raise Exception ("The new block hash must be correct.")

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
