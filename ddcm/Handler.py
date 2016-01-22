import asyncio

from . import utils
from . import const

class Handler(object):
    def __init__(self):
        pass
    def get_call_future(self, echo):
        return None
        
    async def handle_events(self, service, loop):
        self.all_event_future = {}
        def handle_new_node(node):
            service.route.addNode(node)
        debug_enabled = service.config["debug"]["events"]
        while True:
            event = await service.queue.get()
            if debug_enabled:
                await service.debugQueue.put(event)
            if event["type"] is const.kad.event.SERVICE_SHUTDOWN:
                break
            elif event["type"] is const.kad.event.HANDLE_PING:
                asyncio.ensure_future(
                    service.tcpService.call.pong_ping(
                        event["data"]["remoteNode"].remote, event["data"]["echo"]
                    ),
                    loop = loop
                )
            elif event["type"] is const.kad.event.HANDLE_STORE:
                await service.storage.store(*event["data"]["data"])

                asyncio.ensure_future(
                    service.tcpService.call.pong_store(
                        event["data"]["remoteNode"].remote,
                        event["data"]["echo"],
                        event["data"]["data"][0]
                    ),
                    loop = loop
                )
            elif event["type"] is const.kad.event.HANDLE_FIND_NODE:
                asyncio.ensure_future(
                    service.tcpService.call.pong_find_node(
                        event["data"]["remoteNode"].remote,
                        event["data"]["echo"],
                        event["data"]["data"][0],
                        service.route.findNeighbors(event["data"]["data"][0])
                    )
                )
            if event["type"] in const.kad.event.rpc_events_handle:
                handle_new_node(event["data"]["remoteNode"])
            if event["type"] in const.kad.event.rpc_events_do:
                pass
