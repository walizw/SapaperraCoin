from blockchain.block import Block

class Blockchain ():
    def __init__ (self):
        self.chain = [Block.genesis ()]

    def add_block (self, data):
        self.chain.append (Block.mine_block (self.chain [-1], data))

    def replace_chain (self, chain):
        if len (chain) <= len (self.chain):
            raise Exception ("The incoming chain must be longer.")

        try:
            Blockchain.is_valid_chain (chain)
        except Exception as e:
            raise Exception (f"The incoming chain is invalid: {e}.")

        self.chain = chain

    def to_json (self):
        return list (map (lambda block:block.to_json (), self.chain))

    @staticmethod
    def is_valid_chain (chain):
        if chain [0] != Block.genesis ():
            raise Exception ("The genesis block must be valid")

        for i in range (1, len (chain)):
            block = chain [i]
            last_block = chain [i - 1]
            Block.is_valid_block (last_block, block)

    def __repr__ (self):
        return f"Blockchain: {self.chain}"
