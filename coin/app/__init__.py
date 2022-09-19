from flask import Flask, jsonify

from blockchain.blockchain import Blockchain

app = Flask (__name__)
blockchain = Blockchain ()

for i in range (3):
    blockchain.add_block (i)

@app.route ("/blockchain")
def route_blockchain ():
    return jsonify (blockchain.to_json ())

app.run ()
