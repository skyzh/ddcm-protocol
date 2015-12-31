import asyncio
import logging
import json
import unittest

import kademlia

from . import const

class PingTest(unittest.TestCase):
    async def handle_events(self, service):
        self.pong_recved = 0
        while pong_recved < 10:
            event = await service.queue.get()
            if event["type"] is kademlia.const.kad.event.SEND_PING:
                pass
            if event["type"] is kademlia.const.kad.event.HANDLE_PONG_PING:
                self.pong_recved = self.pong_recved + 1

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
            asyncio.ensure_future(
                self.handle_events(service)
            )
        )

        loop.run_until_complete(service.stop())

        loop.close()
