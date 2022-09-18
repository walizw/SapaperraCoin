import hashlib
import json

def crypto_hash (*args):
    str_args = sorted (map (lambda x:json.dumps (x), args))
    joined_data = "".join (str_args)
    return hashlib.sha256 (joined_data.encode ("utf-8")).hexdigest ()
