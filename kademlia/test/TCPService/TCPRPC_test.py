import asyncio
import logging
import unittest

import kademlia

from .. import const

class TCPRPCTest(unittest.TestCase):

    def test_pack_ping(self):
        config = kademlia.utils.load_config("config.json")

        loop = asyncio.get_event_loop()
        loop.set_debug(config['debug']['asyncio']['enabled'])

        tcpRPC = kademlia.TCPService.TCPRPC.TCPRPC(config, loop)
        tcpNode = kademlia.Node(
            id = kademlia.utils.dump_node_hex(config["node"]["id"]),
            remote = kademlia.Remote(
                host = config["server"]["host"],
                port = config["server"]["port"]
            )
        )
