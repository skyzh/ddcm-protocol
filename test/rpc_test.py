#!/usr/bin/env python3.5
import sys
sys.path.append("..")

import rpc
import asyncio

from protocol import KademliaProtocol
from rpc import KademliaRPC
from server import KademliaServer
from node import Node
import random
from remote import Remote

def test_rpc(loop):
    loop = asyncio.get_event_loop()

    server_server = KademliaServer(
        loop=loop,
        node=Node(bytes(random.getrandbits(8) for i in range(20))),
        rpc=KademliaRPC()
    )

    server_client = KademliaServer(
        loop=loop,
        node=Node(bytes(random.getrandbits(8) for i in range(20))),
        port=8175,
        rpc=KademliaRPC()
    )

    loop.run_until_complete(server_server.start_server())
    loop.run_until_complete(server_client.start_server())
    tasks_client = [
        server_client.ping(Remote("127.0.0.1", 8654)) for i in range(2)
    ]
    tasks_server = [
        server_server.ping(Remote("127.0.0.1", 8175)) for i in range(2)
    ]
    loop.run_until_complete(
        asyncio.gather(
            asyncio.wait(tasks_client),
            asyncio.wait(tasks_server)
        )
    )
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(server_server.stop_server())
    loop.run_until_complete(server_client.stop_server())

    loop.close()

def main():
    loop = asyncio.get_event_loop()
    test_rpc(loop)
    loop.close()

main()
