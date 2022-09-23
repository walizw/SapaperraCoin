from flask import Flask, jsonify, request

from blockchain.blockchain import Blockchain
from blockchain.block import Block

from net.node import SapaperraNode

import json

app = Flask (__name__)
blockchain = Blockchain ()

node = SapaperraNode ("127.0.0.1", int (input ("Enter sapaperranode port: ")), blockchain)
node.start ()

for i in range (3):
    blockchain.add_block (i)

@app.route ("/blockchain")
def route_blockchain ():
    return jsonify (blockchain.to_json ())

@app.route ("/blockchain/mine")
def route_blockchain_mine ():
    transaction_data = "Transaction data goes here"
    blockchain.add_block (transaction_data)

    node.send_to_nodes (json.dumps (Block.to_json (blockchain.chain [-1])))
    return jsonify (blockchain.chain [-1].to_json ())

@app.route ("/net/connect")
def route_net_connect ():
    ip = request.args.get ("ip")
    port = request.args.get ("port")

    if ip == None or port == None:
        return "Please enter the IP and the port"
    status = node.connect_with_node (ip, int (port))
    if status == False:
        return "There's been a problem connecting with the node"
    return "Connection successul"

app.run (port=int (input ("Enter Blockchain API port: ")))
node.stop ()
