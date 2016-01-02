import asyncio
import logging
import json
import unittest

import kademlia

from . import const

class PingTest(unittest.TestCase):
    async def handle_events(self, service):
        pong_count = 0
        self.ping_sent = []
        self.pong_recved = []
        while pong_count < const.test.PING_COUNT:
            event = await service.queue.get()
            if event["type"] is kademlia.const.kad.event.SEND_PING:
                self.ping_sent.append(event["data"]["echo"])
            if event["type"] is kademlia.const.kad.event.HANDLE_PONG_PING:
                self.pong_recved.append(event["data"]["echo"])
                pong_count = pong_count + 1

    def test_ping(self):
        config = kademlia.utils.load_config("config.json")

        loop = asyncio.get_event_loop()
        loop.set_debug(config['debug']['asyncio']['enabled'])

        service = kademlia.Service(config, loop)
        loop.run_until_complete(service.start())
        loop.run_until_complete(asyncio.wait(
            [service.tcpService.call.ping(kademlia.Remote(
                host = "127.0.0.1",
                port = config["server"]["port"]
            )) for i in range(const.test.PING_COUNT)]
        ))

        loop.run_until_complete(
            asyncio.wait(
                [asyncio.ensure_future(
                    self.handle_events(service)
                )],
                timeout = const.test.PING_TIMEOUT
            )
        )

        loop.run_until_complete(service.stop())

        loop.close()

        self.ping_sent.sort()
        self.pong_recved.sort()

        self.assertEqual(len(self.ping_sent), const.test.PING_COUNT)
        self.assertEqual(len(self.pong_recved), const.test.PING_COUNT)
        self.assertEqual(self.ping_sent, self.pong_recved)
