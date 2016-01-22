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
        selfNode = selfNode or 0
        route = ddcm.Route(
            None, None, kSize,
            selfNode
        )
        def __deco(func):
            def _deco(*args, **kwargs):
                kwargs['route'] = route
                kwargs['selfNode'] = selfNode
                ret = func(*args, **kwargs)

                return ret
            return _deco
        return __deco

    @TestCase(20, None)
    def test_addNode(self, route, selfNode):
        node = self.get_random_node()
        route.addNode(node)
        bucket = route.buckets[route.getBucket(node.hash)]
        self.assertFalse(bucket.isNewNode(node))

    @TestCase(20, None)
    def test_removeNode(self, route, selfNode):
        node = self.get_random_node()
        route.addNode(node)
        bucket = route.buckets[route.getBucket(node.hash)]
        self.assertFalse(bucket.isNewNode(node))
        route.removeNode(node)
        self.assertTrue(bucket.isNewNode(node))

    @TestCase(
        2,
        0
    )
    def test_addNode_split(self, route, selfNode):
        nodes = map(
            self.get_id_node, [
                2 ** 155,
                2 ** 156,
                2 ** 157,
                2 ** 158,
                2 ** 159
            ]
        )
        for node in nodes:
            route.addNode(node)

        self.assertEqual(len(route.buckets), 4)

    @TestCase(
        20,
        0
    )

    def test_findNeighbors(self, route, selfNode):
        nodes = [self.get_id_node(i) for i in range(2 ** 80, 2 ** 80 + 10)]
        for node in nodes:
            route.addNode(node)
        neighbors = route.findNeighbors(self.get_id_node(0))
        for distance, node in neighbors:
            self.assertTrue(node in nodes)
            self.assertNotEqual(selfNode, node.id)
