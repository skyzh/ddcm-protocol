import struct
import json
import socket

from .. import const

from ..Remote import Remote
from ..Node import Node

class TCPRPC(object):
    def __init__(self, service, loop):
        self.service = service
        self.loop = loop

    def pack_ping(self, local, echo):
        """Pack Ping Message

        Args:
            local: Self Node
            echo: Random Echo Message

        Returns:
            Packed Data to Send
        """
        return b"".join([
            struct.pack('B', const.kad.command.PING),
            echo,
            local.id,
            self.pack_remote(self.service.server.remote)
        ])

    def pack_pong(self, local, echo):
        """Pack Ping Message

        Args:
            local: Self Node
            echo: Recieved Echo Message

        Returns:
            Packed Data to Send
        """
        return b"".join([
            struct.pack('B', const.kad.command.PONG),
            echo,
            local.id,
            self.pack_remote(self.service.server.remote)
        ])

    async def read_ping(self):
        return None
    async def read_pong(self):
        return None

    def pack_findNode(self, local, echo, remote):
        """Pack FindNode Message

        Args:
            local: Self Node
            echo: Random Echo Message
            remote: Hash of Node to Ping

        Returns:
            Packed Data to Send
        """
        return self.pack([
            const.kad.command.PING,
            echo,
            local.id,
            remote
        ])

    def get_command_string(self, id):
        return const.kad.command.COMMANDS[id]

    def pack_remote(self, remote):
        remote_ip = socket.inet_aton(remote.host)
        return b"".join([
            struct.pack('>BH', len(remote_ip), remote.port),
            remote_ip
        ])

    async def read_remote(self, reader):
        ip_size, port = struct.unpack('>BH', await reader.readexactly(3))
        host = socket.inet_ntoa(await reader.readexactly(ip_size))
        return Remote(
            host = host,
            port = port
        )

    async def read_command(self, reader):
        """Read Command

        Args:
            reader: a StreamReader object

        Returns:
            JSON Data
        """
        command, = struct.unpack('B', await reader.readexactly(1))
        echo = await reader.readexactly(4)
        remoteNode = Node(
            id = await reader.readexactly(20),
            remote = await self.read_remote(reader)
        )
        if command == const.kad.command.PING:
            return command, echo, remoteNode, await self.read_ping()
        elif command == const.kad.command.PONG:
            return command, echo, remoteNode, await self.read_pong()
