import asyncio
import logging
import json
import unittest
import socket
import random

import ddcm

from . import const
from . import utils

class StoreTest(unittest.TestCase):
    async def handle_events(self, service):
        pong_count = 0
        self.ping_sent = []
        self.ping_recved = []
        self.pong_sent = []
        self.pong_recved = []
        self.pair_sent, self.pair_recved = [], []

        while pong_count < const.test.STORE_COUNT:
            event = await service.debugQueue.get()
            if event["type"] is ddcm.const.kad.event.SEND_STORE:
                self.ping_sent.append(event["data"]["echo"])
                self.pair_sent.append(event["data"]["data"])
            if event["type"] is ddcm.const.kad.event.HANDLE_PONG_STORE:
                self.pong_recved.append(event["data"]["echo"])
                pong_count += 1
            if event["type"] is ddcm.const.kad.event.SEND_PONG_STORE:
                self.pong_sent.append(event["data"]["echo"])
            if event["type"] is ddcm.const.kad.event.HANDLE_STORE:
                self.ping_recved.append(event["data"]["echo"])
                self.pair_recved.append(event["data"]["data"])

    def StoreTestCase(func):
        async def _deco(*args, **kwargs):
            ret = await func(*args, **kwargs)

            loop, service, config, self = kwargs['loop'], kwargs['service'], kwargs['config'], kwargs['self']

            await asyncio.wait(
                [asyncio.ensure_future(
                    self.handle_events(service)
                )],
                timeout = const.test.STORE_TIMEOUT
            )

            await service.stop()

            for event_list in [self.ping_sent, self.ping_recved, self.pong_sent, self.pong_recved, self.pair_sent, self.pair_recved]:
                event_list.sort()

            self.assertEqual(len(self.ping_sent), const.test.STORE_COUNT)
            self.assertEqual(len(self.ping_recved), const.test.STORE_COUNT)
            self.assertEqual(len(self.pong_sent), const.test.STORE_COUNT)
            self.assertEqual(len(self.pong_recved), const.test.STORE_COUNT)
            self.assertEqual(self.ping_sent, self.pong_recved)
            self.assertEqual(self.ping_sent, self.ping_recved)
            self.assertEqual(self.ping_sent, self.pong_sent)

            for sent, recved in zip(self.pair_sent, self.pair_recved):
                self.assertEqual(sent, recved)

            for data in self.pair_sent:
                self.assertEqual(await service.storage.exist(data[0]), True)
                self.assertEqual(await service.storage.get(data[0]), data[1])

            return ret
        return _deco

    def get_key_pair(self):
        return bytes(random.getrandbits(8) for i in range(20)), bytes(random.getrandbits(8) for i in range(120))

    @utils.NetworkTestCase
    @StoreTestCase
    async def test_store(self, loop, config, service):
        await asyncio.wait(
            [service.tcpService.call.store(ddcm.Remote(
                host = "127.0.0.1",
                port = config["server"]["port"]
            ), *self.get_key_pair()) for i in range(const.test.STORE_COUNT)]
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
