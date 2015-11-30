import random
import asyncio
import codecs
import struct

from . import const
from . import utils

class TCPProtocol(object):
    """TCPProtocol

    Protocol used in TCP Connections between Peers.
    """
    def __init__(self, loop, service):
        self.loop = loop
        self.service = service

    async def _do_send(self, writer, data):
        writer.write(data)
        await writer.drain()

    async def _do_pong_ping(self, writer, echo):
        await self._do_send(
            writer,
            self.service.tcpRPC.pack_pong(self.service.tcpNode, echo)
        )

    async def _do_ping(self, writer):
        await self._do_send(writer, self.service.tcpRPC.pack_ping(self.service.tcpNode, utils.get_echo_bytes()))

    async def _do_store(self, key, value):
        pass

    async def _do_findNode(self, nodeID):
        pass

    async def _do_findValue(self, key):
        pass


    async def _handle_ping(self, echo, remoteNode, data):
        print("".join(["RPC: Recv Command ",
            "PING",
            " Echo ",
            codecs.encode(echo, "hex").decode(),
            " Remote ",
            codecs.encode(remoteNode, "hex").decode()
        ]))
        await self.service.tcpCall.pong_ping(remoteNode.remote, echo)

    async def _handle_store(self, echo, remoteNode, data):
        pass

    async def _handle_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_findValue(self, echo, remoteNode, data):
        pass

    async def _handle_pong_ping(self, echo, remoteNode, data):
        print("".join(["RPC: Recv Command ",
            "PONG",
            " Echo ",
            codecs.encode(echo, "hex").decode(),
            " Remote ",
            codecs.encode(remoteNode, "hex").decode()
        ]))

    async def _handle_pong_store(self, echo, remoteNode, data):
        pass

    async def _handle_pong_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_pong_findValue(self, echo, remoteNode, data):
        pass

    async def handle(self, reader):
        command, echo, remoteNode, data = await self.service.tcpRPC.read_command(reader)
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
