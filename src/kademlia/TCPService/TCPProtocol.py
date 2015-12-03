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

    async def _do_pong_ping(self, writer, echo):
        await self._do_send(
            writer,
            self.service.rpc.pack_pong(self.service.node, echo)
        )

    async def _do_ping(self, writer):
        await self._do_send(writer, self.service.rpc.pack_ping(self.service.node, utils.get_echo_bytes()))

    async def _do_store(self, key, value):
        pass

    async def _do_findNode(self, nodeID):
        pass

    async def _do_findValue(self, key):
        pass

    async def _handle_ping(self, echo, remoteNode, data):
        self.__logger__.info("".join([
            "PING ",
            codecs.encode(echo, "hex").decode(),
            " from ",
            remoteNode.get_hash_string()
        ]))
        await self.service.call.pong_ping(remoteNode.remote, echo)

    async def _handle_store(self, echo, remoteNode, data):
        pass

    async def _handle_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_findValue(self, echo, remoteNode, data):
        pass

    async def _handle_pong_ping(self, echo, remoteNode, data):
        self.__logger__.info("".join([
            "PONG ",
            codecs.encode(echo, "hex").decode(),
            " from ",
            remoteNode.get_hash_string()
        ]))

    async def _handle_pong_store(self, echo, remoteNode, data):
        pass

    async def _handle_pong_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_pong_findValue(self, echo, remoteNode, data):
        pass

    async def handle(self, reader):
        command, echo, remoteNode, data = await self.service.rpc.read_command(reader)
        if command == const.kad.command.PING:
            await self._handle_ping(echo, remoteNode, data)
        elif command == const.kad.command.STORE:
            await self._handle_store(echo, remoteNode, data)
        elif command == const.kad.command.FIND_NODE:
            await self._handle_findNode(echo, remoteNode, data)
        elif command == const.kad.command.FIND_VALUE:
            await self._handle_findValue(echo, remoteNode, data)
        elif command == const.kad.command.PONG:
            await self._handle_pong_ping(echo, remoteNode, data)
        elif command == const.kad.command.PONG_STORE:
            await self._handle_pong_store(echo, remoteNode, data)
        elif command == const.kad.command.PONG_FIND_NODE:
            await self._handle_pong_findNode(echo, remoteNode, data)
        elif command == const.kad.command.PONG_FIND_VALUE:
            await self._handle_pong_findValue(echo, remoteNode, data)
        else:
            # TODO: Handle Unknown Command
            pass
