from . import TCPServer
from . import TCPProtocol
from . import RPC
from . import Node
from . import Route
from . import TCPCall


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
        selfNode:     Present Node
        storage:      Kademlia Key-Value Storage
        RPC:          Kademlia Message Compress Module
        daemonServer: Kademlia Daemon Server
        tcpCall:      Remote Call Service on TCP Protocol
    """
    def __init__(self, config, loop):
        self.config = config
        self.loop = loop
        self.tcpServer = TCPServer(
            service = self,
            loop = self.loop,
            host = self.config.server.host,
            port = self.config.server.port
        )
        self.rpc = RPC(
            service = self,
            loop = self.loop
        )
        self.tcpProtocol = TCPProtocol(
            service = self,
            loop = self.loop
        )
        self.route = Route(
            service = self,
            loop = self.loop
        )
        self.tcpCall = TCPCall(
            service = self,
            loop = self.loop
        )

    async def handle(self):
        await self.tcpServer.start_server()
