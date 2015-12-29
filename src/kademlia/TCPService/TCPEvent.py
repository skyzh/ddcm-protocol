from .. import const

class TCPEvent(object):
    """TCPEvent
    Handle TCP Events
    """
    def __init__(self, loop, service):
        self.loop = loop
        self.service = service
        self.enabled = self.service.config["debug"]["events"]

    def add_event(self, event_type, data = None):
        if self.enabled:
            self.service.queue.put_nowait({
                "service": const.kad.event.TCPService,
                "type": event_type,
                "data": data
            })
    
