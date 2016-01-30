import asyncio
import logging
import json
import unittest
import socket

import ddcm

from . import const
from . import utils

class FindNodeTest(unittest.TestCase):
    def create_queue(self, loop, queues):
        async def read_queue(name, queue, targetQueue):
            while True:
                event = await queue.get()
                await targetQueue.put((name, event))
                if event["type"] is ddcm.const.kad.event.SERVICE_SHUTDOWN:
                    break

        targetQueue = asyncio.Queue(
            ddcm.const.kad.service.MESSAGE_QUEUE_MAXSIZE,
            loop=loop
        )
        for queue in queues:
            asyncio.ensure_future(read_queue(queue[0], queue[1], targetQueue))
        return targetQueue

    async def handle_events(self, loop, services):
        queue = self.create_queue(loop, [
            (name, services[name].debugQueue) for name in services
        ])
        self.pong_recved = {"A": 0, "B": 0, "C": 0}
        pong_recved_count = 0
        while pong_recved_count < const.test.PING_MULTI_COUNT * 9:
            name, event = await queue.get()
            if event["type"] is ddcm.const.kad.event.SERVICE_SHUTDOWN:
                break
            if event["type"] is ddcm.const.kad.event.SEND_PING:
                pass
            if event["type"] is ddcm.const.kad.event.HANDLE_PONG_PING:
                """print("[%(name)s] Recved PONG from %(target)s" % {
                    "name": name,
                    "target": event["data"]["remoteNode"].get_hash_string()
                })"""
                self.pong_recved[name] += 1
                pong_recved_count += 1
            if event["type"] is ddcm.const.kad.event.SEND_PONG_PING:
                pass
            if event["type"] is ddcm.const.kad.event.HANDLE_PING:
                pass

    def FindNodePingTestCase(func):
        async def _deco(*args, **kwargs):
            ret = await func(*args, **kwargs)

            loop, services, configs, self = kwargs['loop'], kwargs['services'], kwargs['configs'], kwargs['self']

            await asyncio.wait(
                [asyncio.ensure_future(
                    self.handle_events(loop, services)
                )],
                timeout = const.test.PING_MULTI_TIMEOUT
            )

            self.assertEqual(self.pong_recved['A'], const.test.PING_MULTI_COUNT * 3)
            self.assertEqual(self.pong_recved['B'], const.test.PING_MULTI_COUNT * 3)
            self.assertEqual(self.pong_recved['C'], const.test.PING_MULTI_COUNT * 3)

            return ret
        return _deco

    @utils.MultiNetworkTestCase(["A", "B", "C"])
    @FindNodePingTestCase
    async def test_multi_ping(self, loop, configs, services):
        sA, sB, sC = services["A"], services["B"], services["C"]
        for sX in [sA, sB, sC]:
            for sY in [sA, sB, sC]:
                await asyncio.wait([
                    sX.tcpService.call.ping(sY.tcpService.node.remote)
                    for i in range(const.test.PING_MULTI_COUNT)
                ])
    @utils.MultiNetworkTestCase(["A", "B", "C"])
    async def test_find_node(self, loop, configs, services):
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
        result = await sB.find_node(sC.tcpService.node.id)
        self.assertEqual(result.id, sC.tcpService.node.id)
        self.assertEqual(result.remote.port, sC.tcpService.node.remote.port)
