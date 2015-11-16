import random
import asyncio

import const
import utils

from Protocol import Protocol
from Remote import Remote

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
    def __init__(self,
                host=const.kad.server.TCP_DEFAULT_HOST,
                port=const.kad.server.TCP_DEFAULT_PORT,
                loop, service):
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
        await self.service.tcpProtocol.handle(reader)
        writer.close()

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

    async def ping(self, remote):
        """Ping

        Args:
            remote: Remote Destination
        Returns:
            Remote Node
        """
        reader, writer = await remote.connect_tcp(self.loop)
        
    async def store(self, key, value):
        """Store

        Args:
            key: Key
            value: Value
        Returns:
            None
        """
        pass

    async def findNode(self, remote):
        """findNode

        Args:
            remote: Remote Hash
        Returns:
            Remote Node
        """
        pass

    async def findValue(self, key):
        """findValue

        Args:
            key: Key
        Returns:
            (key, value)
        """
        pass

    async def pong_ping(self, remote, echo):
        """Pong

        Args:
            remote: Remote Destination
            echo: Echo Value
        Returns:
            None
        """
        pass

    async def pong_store(self, remote, echo):
        """Pong

        Args:
            remote: Remote Destination
            echo: Echo Value
        Returns:
            None
        """
        pass

    async def pong_findNode(self, remote, echo):
        """Pong

        Args:
            remote: Remote Destination
            echo: Echo Value
        Returns:
            None
        """
        pass

    async def pong_findValue(self, remote, echo):
        """Pong

        Args:
            remote: Remote Destination
            echo: Echo Value
        Returns:
            None
        """
        pass
