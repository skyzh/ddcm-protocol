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

        loop.run_until_complete(service.stop())
        return ret
    return _deco

def MultiNetworkTestCase(names):
    def __deco(func):
        def _deco(self, *args, **kwargs):
            config = ddcm.utils.load_config("config.json")

            loop = asyncio.get_event_loop()
            loop.set_debug(config['debug']['asyncio']['enabled'])

            configs = {}
            services = {}

            for name in names:
                _config = ddcm.utils.load_config("ddcm/test/config/config" + name + ".json")
                service = ddcm.Service(_config, loop)
                loop.run_until_complete(service.start())

                services[name] = service
                configs[name] = _config

            kwargs = {
                'loop': loop,
                'configs': configs,
                'services': services,
                'self': self
            }

            ret = loop.run_until_complete(func(*args, **kwargs))

            for name in services:
                loop.run_until_complete(services[name].stop())

            return ret
        return _deco
    return __deco
