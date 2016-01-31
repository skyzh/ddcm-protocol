from .. import utils

from ..Node import Node
from ..Remote import Remote
from ..Route import Route

from .TCPServer import TCPServer
from .TCPProtocol import TCPProtocol
from .TCPRPC import TCPRPC
from .TCPCall import TCPCall
from .TCPEvent import TCPEvent

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
        self.logger = self.service.logger
        self.__logger__ = self.logger.get_logger("TCPService")

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
            id = utils.dump_node_hex(self.config["node"]["id"]),
            remote = Remote(
                host = self.config["server"]["host"],
                port = self.config["server"]["port"]
            )
        )
        self.event = TCPEvent(
            service = self,
            loop = self.loop
        )
        self.queue = self.service.queue
        self.storage = self.service.storage
        self.route = Route(self, loop, config["kbucket"]["ksize"], self.node)
        self.handler = self.service.handler


    async def start(self):
        await self.server.start_server()
        self.__logger__.info("DDCM TCP Service has been started.")
        self.__logger__.info("DDCM TCP Service is listening on " + self.config["server"]["host"] + ":" + str(self.config["server"]["port"]))

    async def stop(self):
        await self.server.stop_server()
        self.__logger__.info("DDCM TCP Service has been stopped.")
