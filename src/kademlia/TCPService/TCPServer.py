import random
import asyncio

from .. import utils
from .. import const

from ..Remote import Remote

class TCPServer(object):
    """TCP Server

    Provides TCP Protocol for Kademlia Service.

    Func:
        ping, store, findValue, findNode: Call Remote Peer in these commands
                                          in TCP Protocol
        pong_ping, pong_store, pong_findNode, pong_findNode: Pong Remote Peer

        start_server: Start Kademlia TCP Server
        stop_server:  Stop Kademlia TCP Server
    """
    def __init__(
        self, loop, service,
        host = const.kad.server.TCP_DEFAULT_HOST,
        port = const.kad.server.TCP_DEFAULT_PORT,
    ):
        """Init

        Args:
            host:    TCP Server Host. Default 127.0.0.1
            port:    TCP Server Port. Default 8567
            loop:    Asyncio Loop Object
            service: Kademlia Service
        """
        self.host, self.port = host, port
        self.loop = loop
        self.service = service
        self.server = None
        self.remote = Remote(
            host = host,
            port = port
        )

    async def handle(self, reader, writer):
        remote = Remote()
        remote.host, remote.port = writer.get_extra_info("peername")
        data = await self.service.protocol.handle(reader)
        writer.close()

    async def start_server(self):
        self.server = await asyncio.start_server(
            self.handle,
            self.host, self.port,
            loop = self.loop
        )
        return self.server

    async def stop_server(self):
        self.server.close()
        await self.server.wait_closed()
        self.server = None
