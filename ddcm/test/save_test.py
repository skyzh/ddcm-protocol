import asyncio
import logging
import json
import unittest
import socket

import ddcm

from . import const
from . import utils

class SaveTest(unittest.TestCase):
    @utils.MultiNetworkTestCase(["A", "B", "C"])
    async def test_save_data(self, loop, configs, services):
        futures = []
        sA, sB, sC = services["A"], services["B"], services["C"]
        futures.append(
            await sB.tcpService.call.ping(sA.tcpService.node.remote)
        )
        futures.append(
            await sC.tcpService.call.ping(sA.tcpService.node.remote)
        )

        for f in asyncio.as_completed(futures):
            await f
        # Finished Ping
        key = ddcm.utils.get_random_node_id()
        value = ddcm.utils.get_random_node_id()
        result = await sA.store(key, value)
        self.assertTrue(await sC.storage.exist(key))
        self.assertTrue(await sB.storage.exist(key))
        self.assertTrue(await sA.storage.exist(key))
        self.assertEqual(await sC.storage.get(key), value)
        self.assertEqual(await sA.storage.get(key), value)
        self.assertEqual(await sB.storage.get(key), value)
