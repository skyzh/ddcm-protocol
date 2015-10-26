import asyncio

class Remote:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
    async def open_connection(self, loop=None):
        return await asyncio.open_connection(self.host, self.port, loop=loop)
