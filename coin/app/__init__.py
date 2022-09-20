from flask import Flask, jsonify

from blockchain.blockchain import Blockchain

app = Flask (__name__)
blockchain = Blockchain ()

for i in range (3):
    blockchain.add_block (i)

@app.route ("/blockchain")
def route_blockchain ():
    return jsonify (blockchain.to_json ())

@app.route ("/blockchain/mine")
def route_blockchain_mine ():
    transaction_data = "Transaction data goes here"
    blockchain.add_block (transaction_data)
    return jsonify (blockchain.chain [-1].to_json ())

app.run ()
