#!/usr/bin/env python3
import asyncio
import logging
import json
import unittest

import kademlia

from . import const

class PingTest(unittest.TestCase):
    async def when_ping(self):
        pass

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

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        loop.run_until_complete(service.stop())

        loop.close()


if __name__ == '__main__':
    unittest.main()
