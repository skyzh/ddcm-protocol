#!/usr/bin/env python3
import asyncio

import kademlia

loop = asyncio.get_event_loop()

service = kademlia.Service({
    "server": {
        'host': "127.0.0.1",
        'port': 8963
    }
}, loop)

loop.run_until_complete(service.start())

print("Kademlia Service has been started.")
# print(service.tcpServer.server.sockets[0].getsockname())
loop.run_until_complete(service.tcpCall.ping(kademlia.Remote(
    host="127.0.0.1",
    port=8963
)))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.run_until_complete(service.stop())

loop.close()
