import asyncio
import logging
import unittest
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

import kademlia

from .. import const

class TCPRPCTest(unittest.TestCase):

    def test_pack_ping(self):
        config = kademlia.utils.load_config("config.json")

        loop = asyncio.get_event_loop()
        loop.set_debug(config['debug']['asyncio']['enabled'])

        service = kademlia.Service(config, loop)
        echo = kademlia.utils.get_echo_bytes()

        rsock, wsock = socketpair()

        reader, writer = loop.run_until_complete(
            asyncio.open_connection(sock=rsock, loop=loop)
        )

        wsock.send(
            service.tcpService.rpc.pack_ping(service.tcpService.node, echo)
        )

        _command, _echo, _remoteNode, _data = loop.run_until_complete(
            asyncio.ensure_future(
                service.tcpService.rpc.read_command(reader)
            )
        )
        writer.close()
        wsock.close()

        self.assertEqual(_command, kademlia.const.kad.command.PING)
        self.assertEqual(echo, _echo)
