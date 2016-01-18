#!/usr/bin/env python3

import sys
import argparse
import asyncio
import functools

import ddcm

parser = argparse.ArgumentParser(description='DDCM Command Line Client')

parser.add_argument('--config', help='config file path')

args = parser.parse_args()

def main():
    def handle_input():
        command = input()
        if command.startswith("ping"):
            host, port = command.split(' ')[1].split(':')
            asyncio.ensure_future(
                service.tcpService.call.ping(ddcm.Remote(
                    host = host,
                    port = int(port)
                )),
                loop = loop
            )
        if command.startswith("loopping"):
            host, port = command.split(' ')[1].split(':')
            asyncio.ensure_future(
                asyncio.wait([
                    service.tcpService.call.ping(ddcm.Remote(
                        host = host,
                        port = int(port)
                    )) for i in range(100)
                ]),
                loop = loop
            )
        if command.startswith("trace route"):
            for distance, node in service.route.findNeighbors(service.tcpService.node):
                print("%(distance)d %(id)s (%(host)s,%(port)d)" % {
                    "distance": distance,
                    "id": node.get_hash_string(),
                    "host": node.remote.host,
                    "port": node.remote.port
                })
        print("READY.")
    async def handle_events():
        while True:
            event = await service.debugQueue.get()
            if event["type"] is ddcm.const.kad.event.SERVICE_SHUTDOWN:
                break
            if event["type"] is ddcm.const.kad.event.HANDLE_PING:
                print("Recved PING from %(target)s" % {
                    "target": event["data"]["remoteNode"].get_hash_string()
                })
            if event["type"] is ddcm.const.kad.event.HANDLE_PONG_PING:
                print("Recved PONG from %(target)s" % {
                    "target": event["data"]["remoteNode"].get_hash_string()
                })
            if event["type"] is ddcm.const.kad.event.SEND_PING:
                print("PING Sent")

    config = ddcm.utils.load_config("config/config" + args.config + ".json" or "config.json")

    loop = asyncio.get_event_loop()
    loop.set_debug(config['debug']['asyncio']['enabled'])

    service = ddcm.Service(config, loop)

    loop.run_until_complete(service.start())

    loop.add_reader(sys.stdin, handle_input)

    try:
        loop.run_until_complete(handle_events())
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(service.stop())

main()
