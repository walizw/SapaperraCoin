import time
from crypto_hash import crypto_hash

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
        return Block (1, "and there were nothing...", "until we created light!", [])

    def __repr__ (self):
        return (
            "{\n"
            f"\t\"timestamp\": \"{self.timestamp}\"\n"
            f"\t\"last_hash\": \"{self.last_hash}\"\n"
            f"\t\"hash\": \"{self.hash}\"\n"
            f"\t\"data\": {self.data}\n"
            "}"
        )
