import struct
import const
import rpc

class KademliaProtocol:
    def __init__(self, selfNode):
        pass

    def ping(self, remote):
        rpc.pack_ping(self.selfNode, remote)

    def store(self, remote, key, value):
        pass
    def findNode(self, remote, nodeID):
        pass
    def findValue(self, remote, key):
        pass
    def _handle_ping(self, remote):
        pass
    def _handle_store(self, remote, key, value):
        pass
    def _handle_findNode(self, remote, key):
        pass
    def _handle_findValue(self, remote, nodeID):
        pass
