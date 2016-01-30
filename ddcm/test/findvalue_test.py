import asyncio
import logging
import json
import unittest
import socket

import ddcm

from . import const
from . import utils

class FindValueTest(unittest.TestCase):
    @utils.MultiNetworkTestCase(["A", "B", "C"])
    async def test_find_value(self, loop, configs, services):
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
        await sA.store(key, value)
        resultA = await sA.find_value(key)
        resultB = await sB.find_value(key)
        resultC = await sC.find_value(key)
        def check_result(result):
            self.assertEqual(result[0], key)
            self.assertEqual(result[1], value)
        check_result(resultA)
        check_result(resultB)
        check_result(resultC)    
