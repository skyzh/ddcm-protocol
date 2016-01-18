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
        while True:
            name, event = await queue.get()
            if event["type"] is ddcm.const.kad.event.SERVICE_SHUTDOWN:
                break
            if event["type"] is ddcm.const.kad.event.SEND_PING:
                pass
            if event["type"] is ddcm.const.kad.event.HANDLE_PONG_PING:
                pass
            if event["type"] is ddcm.const.kad.event.SEND_PONG_PING:
                pass
            if event["type"] is ddcm.const.kad.event.HANDLE_PING:
                pass

    def FindNodeTestCase(func):
        async def _deco(*args, **kwargs):
            ret = await func(*args, **kwargs)

            loop, services, configs, self = kwargs['loop'], kwargs['services'], kwargs['configs'], kwargs['self']
            await asyncio.wait(
                [asyncio.ensure_future(
                    self.handle_events(kwargs['loop'], kwargs['services'])
                )],
                timeout = const.test.PING_TIMEOUT
            )

            return ret
        return _deco

    @utils.MultiNetworkTestCase(["A", "B", "C"])
    @FindNodeTestCase
    async def test_findNode(self, loop, configs, services):
        sA, sB, sC = services["A"], services["B"], services["C"]
        await sA.tcpService.call.ping(sB.tcpService.node.remote)
