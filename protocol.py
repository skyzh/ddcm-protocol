import struct
import const
from rpc import KademliaRPC
import random
import asyncio
import codecs
import utils
from remote import Remote

class KademliaProtocol:
    def __init__(self, selfNode, rpc, server, loop):
        self.selfNode = selfNode
        self.loop = loop
        self.rpc = rpc
        self.server = server

    async def _do_send(self, writer, data):
        writer.write(data)
        await writer.drain()

    async def _do_pong(self, writer, echo):
        await self._do_send(writer, self.rpc.pack_pong(self.selfNode, echo))

    async def _do_ping(self, writer):
        await asyncio.sleep(random.random() * 2)
        await self._do_send(writer, self.rpc.pack_ping(self.selfNode, utils.get_echo_bytes()))

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
        # await self._do_pong(echo)

    async def _handle_store(self, echo, remoteNode, data):
        pass
        
    async def _handle_findNode(self, echo, remoteNode, data):
        pass

    async def _handle_findValue(self, echo, remoteNode, data):
        pass

    async def _handle_pong(self, echo, remoteNode, data):
        print("".join(["RPC: Recv Command ",
            "PONG",
            " Echo ",
            codecs.encode(echo, "hex").decode(),
            " Remote ",
            codecs.encode(remoteNode, "hex").decode()
        ]))

    async def handle(self, reader):
        command, echo, remoteNode, data = await self.rpc.read_command(reader)
        if command == const.kad.command.PING:
            await self._handle_ping(echo, remoteNode, data)
        elif command == const.kad.command.STORE:
            await self._handle_store(echo, remoteNode, data)
        elif command == const.kad.command.FIND_NODE:
            await self._handle_findNode(echo, remoteNode, data)
        elif command == const.kad.command.FIND_VALUE:
            await self._handle_findValue(echo, remoteNode, data)
        elif command == const.kad.command.PONG:
            await self._handle_pong(echo, remoteNode, data)
