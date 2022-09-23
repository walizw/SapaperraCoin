import uuid
import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from config import ADDRESS_PREFIX, STARTING_BALANCE

class Wallet ():
    def __init__ (self):
        self.address = ADDRESS_PREFIX + "".join (str (uuid.uuid4 ()).split ("-"))
        self.balance = STARTING_BALANCE

        self.private_key = ec.generate_private_key (ec.SECP256K1 (),
                                                    default_backend)
        self.public_key = self.private_key.public_key ()

    def sign (self, data):
        return self.private_key.sign (json.dumps (data).encode ("utf-8"),
                                      ec.ECDSA (hashes.SHA256 ()))

    @staticmethod
    def verify (pub_key, data, signature):
        try:
            pub_key.verify (signature,
                            json.dumps (data).encode ("utf-8"),
                            ec.ECDSA (hashes.SHA256 ()))
            return True
        except InvalidSignature:
            return False
