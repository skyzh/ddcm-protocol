import asyncio
import logging
import unittest
import random
import struct

import ddcm

from . import const
from . import utils

class RouteTest(unittest.TestCase):
    def get_random_node(self):
        return ddcm.Node(
            ddcm.utils.get_random_node_id()
        )
    def get_id_node(self, id):
        return ddcm.Node(
            id.to_bytes(20, byteorder='big')
        )
    def TestCase(func):
        def _deco(*args, **kwargs):
            kwargs['bucket'] = bucket
            ret = func(*args, **kwargs)
        return deco

    def test_addNode(self):
        selfNode = self.get_random_node()
        route = ddcm.Route(None, None, 20, selfNode)
        route.addNode(self.get_random_node())
