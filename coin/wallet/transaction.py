import uuid
import time

from wallet.wallet import Wallet

class Transaction ():
    def __init__ (self, sender_wallet, recipient, amount):
        self.id = str (uuid.uuid4 ())
        self.output = self.create_output (sender_wallet, recipient, amount)
        self.input = self.create_input (sender_wallet, self.output)

    def create_output (self, sender_wallet, recipient, amount):
        if amount > sender_wallet.balance:
            raise Exception ("Amount exceeds balance")

        output = {}
        output [recipient] = amount
        output [sender_wallet.address] = sender_wallet.balance - amount

        return output

    def create_input (self, sender_wallet, output):
        return {
            "timestamp": time.time_ns (),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign (output)
        }

    def update (self, sender_wallet, recipient, amount):
        if amount > self.output [sender_wallet.address]:
            raise Exception ("Amount exceeds balance")

        if recipient in self.output:
            self.output [recipient] = self.output [recipient] + amount
        else:
            self.output [recipient] = amount

        self.output [sender_wallet.address] = \
            self.output [sender_wallet.address] - amount

        self.input = self.create_input (sender_wallet, self.output)
