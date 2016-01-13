import asyncio

import ddcm

def NetworkTestCase(func):
    def _deco(self, *args, **kwargs):
        config = ddcm.utils.load_config("config.json")

        loop = asyncio.get_event_loop()
        loop.set_debug(config['debug']['asyncio']['enabled'])

        service = ddcm.Service(config, loop)
        loop.run_until_complete(service.start())

        kwargs = {
            'loop': loop,
            'config': config,
            'service': service,
            'self': self
        }

        ret = loop.run_until_complete(func(*args, **kwargs))

        return ret
    return _deco
