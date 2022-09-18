import time
from crypto.crypto_hash import crypto_hash

GENESIS_DATA = {
    "timestamp": 1,
    "last_hash": "and there were nothing...",
    "hash": "until we created light!",
    "data": []
}

class Block ():
    def __init__ (self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    @staticmethod
    def mine_block (last_block, data):
        timestamp = time.time_ns ()
        last_hash = last_block.hash
        hash = crypto_hash (timestamp, last_hash, data)

        return Block (timestamp, last_hash, hash, data)

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
            "}"
        )
