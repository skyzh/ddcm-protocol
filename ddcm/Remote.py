import asyncio
import socket

class Remote(object):
    def __init__(self, host=None, port=None, family=socket.AF_UNSPEC):
        self.host = host
        self.port = port

    async def connect_tcp(self, loop=None):
        return await asyncio.open_connection(self.host, self.port, loop=loop)
