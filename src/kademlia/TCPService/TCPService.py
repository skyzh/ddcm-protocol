from kademlia import utils

from kademlia.Node import Node
from kademlia.Remote import Remote

from .TCPServer import TCPServer
from .TCPProtocol import TCPProtocol
from .TCPRPC import TCPRPC
from .TCPCall import TCPCall

class TCPService(object):
    """TCPService

    An Object provides all Kademlia Objects of TCP

    Vars:
        server:    Kademlia TCP Server
        protocol:  Kademlia TCP Protocol
        node:      Present Node on TCP
        rpc:       Kademlia Message Compress Module for TCP
        call:      Remote Call Service on TCP Protocol

    """
    def __init__(self, config, service, loop):
        self.loop = loop
        self.service = service
        self.config = config

        self.server = TCPServer(
            service = self,
            loop = self.loop,
            host = self.config["server"]["host"],
            port = self.config["server"]["port"]
        )
        self.rpc = TCPRPC(
            service = self,
            loop = self.loop
        )
        self.protocol = TCPProtocol(
            service = self,
            loop = self.loop
        )
        self.call = TCPCall(
            service = self,
            loop = self.loop
        )
        self.node = Node(
            id = utils.get_random_node_id(),
            remote = Remote(
                host = self.config["server"]["host"],
                port = self.config["server"]["port"]
            )
        )

    async def start(self):
        await self.server.start_server()

    async def stop(self):
        await self.server.stop_server()
