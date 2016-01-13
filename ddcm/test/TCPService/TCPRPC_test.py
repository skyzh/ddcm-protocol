import asyncio
import logging
import unittest
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

import ddcm

from .. import const

class TCPRPCTest(unittest.TestCase):
    def TestCase(func):
        def _deco(*args, **kwargs):
            config = ddcm.utils.load_config("config.json")

            loop = asyncio.get_event_loop()
            loop.set_debug(config['debug']['asyncio']['enabled'])

            service = ddcm.Service(config, loop)
            echo = ddcm.utils.get_echo_bytes()

            rsock, wsock = socketpair()

            reader, writer = loop.run_until_complete(
                asyncio.open_connection(sock=rsock, loop=loop)
            )

            kwargs = {
                'reader': reader,
                'wsock': wsock,
                'tcpService': service.tcpService,
                'echo': echo,
                'loop': loop
            }

            ret = func(*args, **kwargs)

            writer.close()
            wsock.close()

            return ret
        return _deco

    @TestCase
    def test_pack_ping(self, loop, reader, wsock, tcpService, echo):
        wsock.send(
            tcpService.rpc.pack_ping(
                tcpService.node,
                tcpService.server.remote,
                echo
            )
        )

        _command, _echo, _remoteNode, _data = loop.run_until_complete(
            asyncio.ensure_future(
                tcpService.rpc.read_command(reader)
            )
        )


        self.assertEqual(_command, ddcm.const.kad.command.PING)
        self.assertEqual(echo, _echo)

    @TestCase
    def test_pack_pong_ping(self, loop, reader, wsock, tcpService, echo):
        wsock.send(
            tcpService.rpc.pack_pong(
                tcpService.node,
                tcpService.server.remote,
                echo
            )
        )

        _command, _echo, _remoteNode, _data = loop.run_until_complete(
            asyncio.ensure_future(
                tcpService.rpc.read_command(reader)
            )
        )


        self.assertEqual(_command, ddcm.const.kad.command.PONG)
        self.assertEqual(echo, _echo)
