from .. import utils

class TCPCall(object):
    """Command
    Provides ways to send commands
    """
    def __init__(self, loop, service):
        self.loop = loop
        self.service = service

    def get_call_future(self, echo):
        return self.service.handler.get_call_future(echo)

    async def ping(self, remote):
        """Ping

        Args:
            remote: Remote Destination
        Returns:
            Remote Node
        """
        reader, writer = await remote.connect_tcp(self.loop)
        echo = utils.get_echo_bytes()
        await self.service.protocol._do_ping(writer, echo)
        writer.close()

        await self.service.event.do_ping(remote, echo)

        return self.get_call_future(echo)

    async def store(self, remote, key, value):
        """Store

        Args:
            remote: Remote Destination
            key: Key
            value: Value
        Returns:
            None
        """
        echo = utils.get_echo_bytes()
        data = (echo, key, value)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_store(writer, *data)
        writer.close()

        await self.service.event.do_store(remote, *data)

        return self.get_call_future(echo)


    async def findNode(self, remote, remoteId):
        """findNode

        Args:
            remote: Remote Destination
            remoteId: Remote Hash
        Returns:
            (Remote ID, Remote Node)
        """
        echo = utils.get_echo_bytes()
        data = (echo, remoteId)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_findNode(writer, *data)
        writer.close()

        await self.service.event.do_findNode(remote, *data)

        return self.get_call_future(echo)

    async def findValue(self, remote, key):
        """findValue

        Args:
            remote: Remote Destination
            key: Key
        Returns:
            (key, value)
        """
        echo = utils.get_echo_bytes()
        data = (echo, key)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_findValue(writer, *data)
        writer.close()

        await self.service.event.do_findValue(remote, *data)

        return self.get_call_future(echo)

    async def findReduce(self, remote, keyStart, keyEnd):
        """findReduce

        Args:
            remote: Remote Destination
            keyStart: Start Key
            keyEnd: End Key
        Returns:
            (keyStart, keyEnd, value)
        """
        echo = utils.get_echo_bytes()
        data = (echo, keyStart, keyEnd)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_reduce(writer, *data)
        writer.close()

        await self.service.event.do_reduce(remote, *data)

        return self.get_call_future(echo)

    async def pong_ping(self, remote, echo):
        """pong_ping

        Args:
            remote: Remote Destination
            echo: Echo Value
        Returns:
            None
        """
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_pong_ping(writer, echo)
        writer.close()
        await self.service.event.do_pong_ping(remote, echo)

    async def pong_store(self, remote, echo, key):
        """pong_store

        Args:
            remote: Remote Destination
            echo: Echo Value
            key: Key Saved
        Returns:
            None
        """
        data = (echo, key)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_pong_store(writer, *data)
        writer.close()

        await self.service.event.do_pong_store(remote, *data)

    async def pong_findNode(self, remote, echo, remoteId, remoteNodes):
        """pong_findNode

        Args:
            remote: Remote Destination
            echo: Echo Value
            remoteId: Remote ID found
            remoteNodes: Remote Nodes
        Returns:
            None
        """
        data = (echo, remoteId, remoteNodes)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_pong_findNode(writer, *data)
        writer.close()

        await self.service.event.do_pong_findNode(remote, *data)


    async def pong_findValue(self, remote, echo, key, value):
        """pong_findeValue

        Args:
            remote: Remote Destination
            echo: Echo Value
            key: Key found
            value: value found
        Returns:
            None
        """
        data = (echo, key, value)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_pong_findValue(writer, *data)
        writer.close()

        await self.service.event.do_pong_findValue(remote, *data)


    async def pong_findReduce(self, remote, echo, keyStart, keyEnd, value):
        """pong_findReduce

        Args:
            remote: Remote Destination
            keyStart: Start Key
            keyEnd: End Key
            value: Reduced value
        Returns:
            None
        """
        data = (echo, keyStart, keyEnd, value)
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_pong_reduce(writer, *data)
        writer.close()

        await self.service.event.do_pong_reduce(remote, *data)
