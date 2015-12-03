#!/usr/bin/env python3
import asyncio
import logging
import json
import kademlia

loop = asyncio.get_event_loop()

config = kademlia.utils.load_config("config.json")
service = kademlia.Service(config, loop)
loop.run_until_complete(service.start())
# print(service.tcpServer.server.sockets[0].getsockname())
loop.run_until_complete(asyncio.wait(
    [service.tcpService.call.ping(kademlia.Remote(
        host = "127.0.0.1",
        port = 8963
    )) for i in range(10 ** 3)]
))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.run_until_complete(service.stop())

loop.close()
