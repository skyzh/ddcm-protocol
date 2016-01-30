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
from .Handler import Handler

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

        self.debugQueue = asyncio.Queue(
            const.kad.service.MESSAGE_QUEUE_MAXSIZE,
            loop=loop
        )

        self.logger = Logger(config["debug"]["logging"])
        self.__logger__ = self.logger.get_logger("Service")

        self.handler = Handler()

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

        asyncio.ensure_future(self.handler.handle_events(self, self.loop))

    async def stop(self):
        await self.queue.put({
            "service": const.kad.event.Service,
            "type": const.kad.event.SERVICE_SHUTDOWN,
            "data": None
        })

        await self.tcpService.stop()
        self.__logger__.info("DDCM Service has been stopped.")

    async def store(self, key, value):
        def get_store_future(node):
            return self.tcpService.call.store(
                node.remote,
                key,
                value
            )
        queryNode = Node(key)
        futures = []
        commands = [get_store_future(node) for distance, node in self.route.findNeighbors(queryNode)]
        for f in asyncio.as_completed(commands):
            futures.append(await f)
        for f in asyncio.as_completed(futures):
            await f
        await self.storage.store(key, value)
        return True

    async def find_value(self, key):
        def get_findValue_future(node):
            return self.tcpService.call.findValue(
                node.remote,
                key
            )
        queryNode = Node(key)
        futures = []
        commands = [get_findValue_future(node) for distance, node in self.route.findNeighbors(queryNode)]
        for f in asyncio.as_completed(commands):
            futures.append(await f)
        for f in asyncio.as_completed(futures):
            return (await f)["data"]["data"]
        return None

    async def find_node(self, remoteId):
        # Check if node is already in Route
        alpha = self.config["query"]["alpha"]
        queryNode = Node(remoteId)

        def get_findNode_future(node, id):
            return self.tcpService.call.findNode(
                node.remote,
                remoteId
            )
        longest_distance_list = utils.DelayList([2 ** 160])
        nodes_to_ping = {}
        for distance, node in self.route.findNeighbors(queryNode)[:alpha]:
            if distance == 0:
                return node
            nodes_to_ping[node.id] = node
        nodes_queried = []

        while True:
            if not(nodes_to_ping):
                return None

            longest_distance = longest_distance_list.__next__()

            node_to_query = list(nodes_to_ping.items())[:alpha]
            commands = [
                 get_findNode_future(node, remoteId)
                 for (key, node) in node_to_query
            ]
            nodes_queried.extend([key for key, node in node_to_query])
            nodes_to_ping.clear()

            futures = []
            for f in asyncio.as_completed(commands):
                futures.append(await f)

            __longest_distance = 2 ** 160
            for f in asyncio.as_completed(futures):
                _remoteId, count, remoteNodes = (await f)["data"]["data"]
                for remoteNode in remoteNodes:
                    if remoteNode.id == remoteId:
                        return remoteNode
                    if remoteNode.distance(queryNode.hash) <= longest_distance and not(remoteNode.id in nodes_queried):
                        nodes_to_ping[remoteNode.id] = remoteNode
                        __longest_distance = min(
                            __longest_distance,
                            remoteNode.distance(remoteNode.hash)
                        )
            longest_distance_list.data.append(__longest_distance)
