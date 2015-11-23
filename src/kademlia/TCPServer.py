import random
import asyncio

from . import const
from . import utils

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
    def __init__(self, loop, service,
                host=const.kad.server.TCP_DEFAULT_HOST,
                port=const.kad.server.TCP_DEFAULT_PORT,
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

    async def handle(self, reader, writer):
        data = await self.service.tcpProtocol.handle(reader)
        writer.close()
        self.service.tcpCall.call(data)

    async def start_server(self):
        self.server = await asyncio.start_server(
            self.handle,
            self.host, self.port,
            loop=self.loop
        )
        return self.server

    async def stop_server(self):
        self.server.close()
        await self.server.wait_closed()
        self.server=None
