from .TCPServer import TCPServer
from .TCPProtocol import TCPProtocol
from .TCPRPC import TCPRPC
from .Node import Node
from .Route import Route
from .TCPCall import TCPCall
from .Remote import Remote
from . import utils

class Service(object):
    """Service

    An Object provides all Kademlia Objects

    Vars:
        config:       Service config
        loop:         Asyncio Loop Object
        tcpServer:    Kademlia TCP Server
        udpServer:    Kademlia UDP Server
        tcpProtocol:  Kademlia TCP Protocol
        udpProtocol:  Kademlia UDP Protocol
        route:        Kademlia KBuckets
        tcpNode:      Present Node on TCP
        storage:      Kademlia Key-Value Storage
        tcpRPC:       Kademlia Message Compress Module for TCP
        udpRPC:       Kademlia Message Compress Module for UDP
        daemonServer: Kademlia Daemon Server
        tcpCall:      Remote Call Service on TCP Protocol
    """
    def __init__(self, config, loop):
        self.config = config
        self.loop = loop
        self.tcpServer = TCPServer(
            service = self,
            loop = self.loop,
            host = self.config["server"]["host"],
            port = self.config["server"]["port"]
        )
        self.tcpRPC = TCPRPC(
            service = self,
            loop = self.loop
        )
        self.tcpProtocol = TCPProtocol(
            service = self,
            loop = self.loop
        )
        self.tcpCall = TCPCall(
            service = self,
            loop = self.loop
        )
        self.tcpNode = Node(
            id=utils.get_random_node_id(),
            remote=Remote(
                host = self.config["server"]["host"],
                port = self.config["server"]["port"]
            )
        )

    async def start(self):
        await self.tcpServer.start_server()

    async def stop(self):
        await self.tcpServer.stop_server()
