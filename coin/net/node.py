from p2pnetwork.node import Node
from p2pnetwork.nodeconnection import NodeConnection

from blockchain.blockchain import Blockchain
from blockchain.block import Block

import json

class SapaperraConnection (NodeConnection):
    def __init__ (self, main_node, sock, id, host, port, blockchain):
        super (SapaperraConnection, self).__init__ (main_node, sock, id, host, port)
        self.blockchain = blockchain

class SapaperraNode (Node):
    def __init__ (self, host, port, blockchain, id=None, callback=None, max_connections=0):
        super (SapaperraNode, self).__init__ (host, port, id, callback, max_connections)
        self.blockchain = blockchain

    def outbound_node_connected (self, connected_node):
        # When an outbound node connects to us, we will send them our blockchain
        self.send_to_node (connected_node, json.dumps (self.blockchain.to_json ()))

    def inbound_node_connected (self, connected_node):
        # When we connect to a node, we will send our blockchain as well
        self.send_to_nodes (json.dumps (self.blockchain.to_json ()))

    def node_message(self, connected_node, data):
        # print("node_message from " + connected_node.id + ": " + str(data))
        if type (data) == list:
            try:
                new_chain = Blockchain.from_json (data)
                self.blockchain.replace_chain (new_chain.chain)
            except Exception as e:
                print (f"Error replacing incoming blockchain: {e}")
        elif type (data) == dict:
            # A single block
            block = Block.from_json (data)
            potential_chain = self.blockchain.chain [:]
            potential_chain.append (block)

            try:
                self.blockchain.replace_chain (potential_chain)
            except Exception as e:
                print (f"Error replacing incoming blockchain: {e}")

    def create_new_connection (self, connection, id, host, port):
        return SapaperraConnection (self, connection, id, host, port, self.blockchain)
