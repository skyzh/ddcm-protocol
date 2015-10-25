import struct
import json
import const

class rpc:
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
        return self.pack([
            const.kad.command.PING,
            echo,
            local.id
        ])
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
            local.id
        ])

    def pack(self, data):
        """Pack Data

        Args:
            data: Data to Pack

        Returns:
            Packed Data to Send, in JSON
        """
        return json.dumps(data)
