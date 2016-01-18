import asyncio
import logging
import json
import unittest
import socket

import ddcm

from . import const
from . import utils

class FindNodeTest(unittest.TestCase):
    async def handle_events(self, service):
        pong_count = 0
        self.ping_sent = []
        self.ping_recved = []
        self.pong_sent = []
        self.pong_recved = []
        while pong_count < const.test.PING_COUNT:
            event = await service.debugQueue.get()
            if event["type"] is ddcm.const.kad.event.SEND_PING:
                self.ping_sent.append(event["data"]["echo"])
            if event["type"] is ddcm.const.kad.event.HANDLE_PONG_PING:
                self.pong_recved.append(event["data"]["echo"])
                pong_count += 1
            if event["type"] is ddcm.const.kad.event.SEND_PONG_PING:
                self.pong_sent.append(event["data"]["echo"])
            if event["type"] is ddcm.const.kad.event.HANDLE_PING:
                self.ping_recved.append(event["data"]["echo"])

    def FindNodeTestCase(func):
        async def _deco(*args, **kwargs):
            ret = await func(*args, **kwargs)

            loop, services, configs, self = kwargs['loop'], kwargs['services'], kwargs['configs'], kwargs['self']

            await asyncio.wait(
                [asyncio.ensure_future(
                    self.handle_events(service)
                )],
                timeout = const.test.PING_TIMEOUT
            )

            return ret
        return _deco

    @utils.MultiNetworkTestCase("A")
    @utils.MultiNetworkTestCase("B")
    @utils.MultiNetworkTestCase("C")
    @FindNodeTestCase
    async def test_ping(self, loop, configs, services):
        pass
