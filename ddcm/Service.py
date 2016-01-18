import asyncio

from . import utils
from . import const

from .Node import Node
from .Route import Route
from .Remote import Remote
from .Storage import Storage
from .Logger import Logger
from .TCPService import TCPService
from .Route import Route

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

    async def handle_events(self, service, loop):
        def handle_new_node(node):
            service.route.addNode(node)
        debug_enabled = service.config["debug"]["events"]
        while True:
            event = await service.queue.get()
            if debug_enabled:
                await service.debugQueue.put(event)
            if event["type"] is const.kad.event.SERVICE_SHUTDOWN:
                break
            elif event["type"] is const.kad.event.HANDLE_PING:
                asyncio.ensure_future(
                    service.tcpService.call.pong_ping(
                        event["data"]["remoteNode"].remote, event["data"]["echo"]
                    ),
                    loop = loop
                )
            elif event["type"] is const.kad.event.HANDLE_STORE:
                await service.storage.store(*event["data"]["data"])

                asyncio.ensure_future(
                    service.tcpService.call.pong_store(
                        event["data"]["remoteNode"].remote,
                        event["data"]["echo"],
                        event["data"]["data"][0]
                    ),
                    loop = loop
                )
            elif event["type"] is const.kad.event.HANDLE_FIND_NODE:
                asyncio.ensure_future(
                    service.tcpService.call.pong_find_node(
                        event["data"]["remoteNode"].remote,
                        event["data"]["echo"],
                        event["data"]["data"][0],
                        service.route.findNeighbors(event["data"]["data"][0])
                    )
                )
            if event["type"] in const.kad.event.rpc_events_handle:
                handle_new_node(event["data"]["remoteNode"])


    def __init__(self, config, loop):
        self.config = config
        self.loop = loop

        self.queue = asyncio.Queue(
            const.kad.service.MESSAGE_QUEUE_MAXSIZE,
            loop=loop
        )

        self.debugQueue = asyncio.Queue(
            const.kad.service.MESSAGE_QUEUE_MAXSIZE,
            loop=loop
        )

        self.logger = Logger(config["debug"]["logging"])
        self.__logger__ = self.logger.get_logger("Service")


        self.storage = Storage()
        self.route = Route(
            self,
            loop,
            config["kbucket"]["ksize"],
            int.from_bytes(utils.dump_node_hex(config["node"]["id"]), byteorder="big")
        )
        self.tcpService = TCPService(config, self, loop)


    async def start(self):
        await self.tcpService.start()
        self.__logger__.info("DDCM Service has been started.")

        await self.queue.put({
            "service": const.kad.event.Service,
            "type": const.kad.event.SERVICE_START,
            "data": None
        })

        asyncio.ensure_future(self.handle_events(self, self.loop))

    async def stop(self):
        await self.queue.put({
            "service": const.kad.event.Service,
            "type": const.kad.event.SERVICE_SHUTDOWN,
            "data": None
        })

        await self.tcpService.stop()
        self.__logger__.info("DDCM Service has been stopped.")
