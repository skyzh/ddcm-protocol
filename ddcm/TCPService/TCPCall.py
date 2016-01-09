from .. import utils

class TCPCall(object):
    """Command
    Provides ways to send commands
    """
    def __init__(self, loop, service):
        self.loop = loop
        self.service = service

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
        reader, writer = await remote.connect_tcp(self.loop)
        await self.service.protocol._do_pong_ping(writer, echo)
        writer.close()
        await self.service.event.do_pong_ping(remote, echo)

    async def pong_store(self, remote, echo):
        """

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