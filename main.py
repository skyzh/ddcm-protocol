#!/usr/bin/env python3.5

import hashlib
import random
import asyncio
from server import KademliaServer
from node import Node

loop = asyncio.get_event_loop()

server = KademliaServer(
    loop=loop,
    node=Node(bytes(random.getrandbits(8) for i in range(20)))
)

loop.run_until_complete(server.start_server())

print('Serving on {}'.format(server.server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.run_until_complete(server.stop_server())

loop.close()
