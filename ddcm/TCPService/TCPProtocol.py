import random
import asyncio
import codecs
import struct

from .. import utils
from .. import const

class TCPProtocol(object):
    """TCPProtocol

    Protocol used in TCP Connections between Peers.
    """
    def __init__(self, loop, service):
        self.loop = loop
        self.service = service

        self.__logger__ = self.service.logger.get_logger("TCPProtocol")

    async def _do_send(self, writer, data):
        writer.write(data)
        await writer.drain()

    async def _do_ping(self, writer, echo):
        await self._do_send(
            writer,
            self.service.rpc.pack_ping(
                self.service.node,
                self.service.server.remote,
                echo
            )
        )

    async def _do_pong_ping(self, writer, echo):
        await self._do_send(
            writer,
            self.service.rpc.pack_pong(
                self.service.node,
                self.service.server.remote,
                echo
            )
        )


    async def _do_store(self, writer, echo, key, value):
        await self._do_send(
            writer,
            self.service.rpc.pack_store(
                self.service.node,
                self.service.server.remote,
                echo,
                key,
                value
            )
        )

    async def _do_pong_store(self, writer, echo, key):
        await self._do_send(
            writer,
            self.service.rpc.pack_pong_store(
                self.service.node,
                self.service.server.remote,
                echo,
                key
            )
        )

    async def _do_findNode(self, echo, nodeID):
        pass

    async def _do_findValue(self, echo, key):
        pass

    async def _handle_ping(self, echo, remoteNode, data):
        self.__logger__.info("".join([
            "PING ",
            codecs.encode(echo, "hex").decode(),
            " from ",
            remoteNode.get_hash_string()
        ]))

        await self.service.event.handle_ping(echo, remoteNode, data)

        asyncio.ensure_future(
            self.service.call.pong_ping(remoteNode.remote, echo),
            loop = self.loop
        )

    async def _handle_pong_ping(self, echo, remoteNode, data):
        self.__logger__.info("".join([
            "PONG ",
            codecs.encode(echo, "hex").decode(),
            " from ",
            remoteNode.get_hash_string()
        ]))
        await self.service.event.handle_pong_ping(echo, remoteNode, data)

    async def _handle_store(self, echo, remoteNode, data):
        self.__logger__.info("".join([
            "STORE ",
            codecs.encode(echo, "hex").decode(),
            " from ",
            remoteNode.get_hash_string()
        ]))

        await self.service.storage.store(*data)

        await self.service.event.handle_store(echo, remoteNode, data)

        asyncio.ensure_future(
            self.service.call.pong_store(remoteNode.remote, echo, data[0]),
            loop = self.loop
        )

    async def _handle_pong_store(self, echo, remoteNode, data):
        self.__logger__.info("".join([
            "PONG_STORE ",
            codecs.encode(echo, "hex").decode(),
            " from ",
            remoteNode.get_hash_string()
        ]))
        await self.service.event.handle_pong_store(echo, remoteNode, data)


    async def _handle_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_pong_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_findValue(self, echo, remoteNode, data):
        pass

    async def _handle_pong_findValue(self, echo, remoteNode, data):
        pass

    async def _handle_reduce(self, echo, remoteNode, data):
        pass

    async def _handle_pong_reduce(self, echo, remoteNode, data):
        pass

    async def handle(self, reader):
        command, echo, remoteNode, data = await self.service.rpc.read_command(reader)
        _data = (echo, remoteNode, data)
        if command is const.kad.command.PING:
            await self._handle_ping(*_data)
        elif command is const.kad.command.STORE:
            await self._handle_store(*_data)
        elif command is const.kad.command.FIND_NODE:
            await self._handle_findNode(*_data)
        elif command is const.kad.command.FIND_VALUE:
            await self._handle_findValue(*_data)
        elif command is const.kad.command.PONG:
            await self._handle_pong_ping(*_data)
        elif command is const.kad.command.PONG_STORE:
            await self._handle_pong_store(*_data)
        elif command is const.kad.command.PONG_FIND_NODE:
            await self._handle_pong_findNode(*_data)
        elif command is const.kad.command.PONG_FIND_VALUE:
            await self._handle_pong_findValue(*_data)
        elif command is const.kad.command.REDUCE:
            await self._handle_reduce(*_data)
        elif command is const.kad.command.PONG_REDUCE:
            await self._handle_pong_reduce(*_data)
        else:
            # TODO: Handle Unknown Command
            pass
