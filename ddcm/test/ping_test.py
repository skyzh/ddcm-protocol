import asyncio
import logging
import json
import unittest
import socket

import ddcm

from . import const
from . import utils

class PingTest(unittest.TestCase):
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

    def PingTestCase(func):
        async def _deco(*args, **kwargs):
            ret = await func(*args, **kwargs)

            loop, service, config, self = kwargs['loop'], kwargs['service'], kwargs['config'], kwargs['self']

            await asyncio.wait(
                [asyncio.ensure_future(
                    self.handle_events(service)
                )],
                timeout = const.test.PING_TIMEOUT
            )

            for event_list in [self.ping_sent, self.ping_recved, self.pong_sent, self.pong_recved]:
                event_list.sort()

            self.assertEqual(len(self.ping_sent), const.test.PING_COUNT)
            self.assertEqual(len(self.ping_recved), const.test.PING_COUNT)
            self.assertEqual(len(self.pong_sent), const.test.PING_COUNT)
            self.assertEqual(len(self.pong_recved), const.test.PING_COUNT)
            self.assertEqual(self.ping_sent, self.pong_recved)
            self.assertEqual(self.ping_sent, self.ping_recved)
            self.assertEqual(self.ping_sent, self.pong_sent)

            return ret
        return _deco

    @utils.NetworkTestCase
    @PingTestCase
    async def test_ping(self, loop, config, service):
        await asyncio.wait(
            [service.tcpService.call.ping(ddcm.Remote(
                host = "127.0.0.1",
                port = config["server"]["port"]
            )) for i in range(const.test.PING_COUNT)]
        )
    """
    @utils.NetworkTestCase
    @PingTestCase
    async def test_ping_ipv6(self, loop, config, service):
        await asyncio.wait(
            [service.tcpService.call.ping(ddcm.Remote(
                host = "::1",
                port = config["server"]["port"]
            )) for i in range(const.test.PING_COUNT)]
        )
    """
