import asyncio

from . import utils
from . import const

from .Node import Node
from .Route import Route
from .Remote import Remote
from .Logger import Logger
from .TCPService import TCPService

class Service(object):
    """Service

    An Object provides all Kademlia Objects

    Vars:
        config:       Service config
        loop:         Asyncio Loop Object
        tcpService:   Kademlia Service containing all objects for TCP.
        route:        Kademlia KBuckets
        storage:      Kademlia Key-Value Storage
        daemonServer: Kademlia Daemon Server
        queue:        Kademlia Event Queue
    """

    def __init__(self, config, loop):
        self.config = config
        self.loop = loop

        self.queue = asyncio.Queue(
            const.kad.service.MESSAGE_QUEUE_MAXSIZE,
            loop=loop
        )

        self.logger = Logger(config["debug"]["logging"])
        self.__logger__ = self.logger.get_logger("Service")

        self.tcpService = TCPService(config, self, loop)


    async def start(self):
        await self.tcpService.start()
        self.__logger__.info("DDCM Service has been started.")

    async def stop(self):
        await self.tcpService.stop()
        self.__logger__.info("DDCM Service has been stopped.")
