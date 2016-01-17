import asyncio
import logging
import unittest
import random
import struct

import ddcm

from . import const
from . import utils

class RouteTest(unittest.TestCase):
    def SetUp(self):
        self.selfNode = self.get_random_node()

    def get_random_node(self):
        return ddcm.Node(
            ddcm.utils.get_random_node_id()
        )
    def get_id_node(self, id):
        return ddcm.Node(
            id.to_bytes(20, byteorder='big')
        )

    def TestCase(kSize, selfNode):
        route = ddcm.Route(None, None, kSize, selfNode)
        def __deco(func):
            def _deco(*args, **kwargs):
                kwargs['route'] = route
                ret = func(*args, **kwargs)

                return ret
            return _deco
        return __deco
    @TestCase(20, None)
    def test_addNode(self, route):
        node = self.get_random_node()
        route.addNode(node)
        bucket = route.buckets[route.getBucket(node)]
        self.assertFalse(bucket.isNewNode(node))

    @TestCase(20, None)
    def test_removeNode(self, route):
        node = self.get_random_node()
        route.addNode(node)
        bucket = route.buckets[route.getBucket(node)]
        self.assertFalse(bucket.isNewNode(node))
        route.removeNode(node)
        self.assertTrue(bucket.isNewNode(node))
