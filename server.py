from protocol import KademliaProtocol
import asyncio
from remote import Remote
import utils
import random

class KademliaServer(object):
    def __init__(self, ksize=20, alpha=3, node=None, host="127.0.0.1", port=8654, loop=None, rpc=None):
        """Init

        Args:
            kbucket: KBucket Object
            alpha: Parallel Operations
            node: Self Node
            remote: Server Address
            loop: Loop Object
            rpc: RPC Message Object
        """
        self.ksize = ksize
        self.alpha = alpha
        self.node = node
        self.host = host
        self.port = port
        self.loop = loop
        self.rpc = rpc

    async def handle(self, reader, writer):
        await self.protocol.handle(reader)
        writer.close()

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle, self.host, self.port, loop=self.loop)
        self.protocol = KademliaProtocol(self.node, self.rpc, self, self.loop)
        return self.server

    async def stop_server(self):
        self.server.close()
        await self.server.wait_closed()

    async def ping(self, remote):
        """Ping

        Args:
            remote: Remote Destination
        Returns:
            Remote Node
        """
        reader, writer = await remote.open_connection(self.loop)
        await self.protocol._do_ping(writer)
        writer.close()

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
