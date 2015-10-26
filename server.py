from protocol import KademliaProtocol
import asyncio
from remote import Remote
import utils
import random

class KademliaServer(object):
    def __init__(self, ksize=20, alpha=3, node=None, host="127.0.0.1", port=8654, loop=None, rpc=None):
        self.ksize = ksize
        self.alpha = alpha
        self.node = node
        self.host = host
        self.port = port
        self.loop = loop
        self.rpc = rpc

    async def handle(self, reader, writer):
        await self.protocol.handle(reader, writer)

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle, self.host, self.port, loop=self.loop)
        self.protocol = KademliaProtocol(self.node, self.rpc, self, self.loop)
        return self.server

    async def stop_server(self):
        self.server.close()
        await self.server.wait_closed()

    async def ping(self, remote):
        reader, writer = await remote.open_connection(self.loop)
        await self.protocol._do_ping(writer)
        writer.close()
