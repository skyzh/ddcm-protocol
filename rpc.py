import struct
import json
import const
import struct

class KademliaRPC:
    def __init__(self):
        pass
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
            local.id
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
            local.id
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

    def pack(self, data):
        """Pack Data

        Args:
            data: Data to Pack

        Returns:
            Packed Data to Send, in JSON
        """
        json_data = json.dumps(data).encode()
        size_data = struct.pack('>H', len(json_data))
        return size_data + json_data

    def get_command_string(self, id):
        return const.kad.command.COMMANDS[id]

    async def read_command(self, reader):
        """Read Command

        Args:
            reader: a StreamReader object

        Returns:
            JSON Data
        """
        command, = struct.unpack('B', await reader.readexactly(1))
        echo = await reader.readexactly(4)
        remoteNode = await reader.readexactly(20)
        if command == const.kad.command.PING:
            return command, echo, remoteNode, await self.read_ping()
        elif command == const.kad.command.PONG:
            return command, echo, remoteNode, await self.read_pong()
