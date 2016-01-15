import asyncio
import logging
import unittest
import random
import struct

import ddcm

from . import const
from . import utils

class KBucketTest(unittest.TestCase):
    def get_random_node(self):
        return ddcm.Node(
            ddcm.utils.get_random_node_id()
        )
    def get_id_node(self, id):
        return ddcm.Node(
            id.to_bytes(20, byteorder='big')
        )

    def TestCase(left, right, kSize):
        bucket = ddcm.KBucket(left, right, kSize)
        def __deco(func):
            def _deco(*args, **kwargs):
                kwargs['bucket'] = bucket
                ret = func(*args, **kwargs)

                return ret
            return _deco
        return __deco

    @TestCase(1, 2 ** 4 - 1, 20)
    def test_split(self, bucket):
        bucket.addNode(self.get_id_node(7))
        bucket.addNode(self.get_id_node(8))
        one, two = bucket.split()
        self.assertEqual(one.range, (1, 7))
        self.assertEqual(two.range, (8, 15))
        self.assertEqual(len(one), 1)
        self.assertEqual(len(two), 1)


    @TestCase(1, 2 ** 4 - 1, 5)
    def test_addNode(self, bucket):
        self.assertTrue(bucket.addNode(self.get_random_node()))
        self.assertTrue(bucket.addNode(self.get_random_node()))
        self.assertTrue(bucket.addNode(self.get_random_node()))
        self.assertTrue(bucket.addNode(self.get_random_node()))
        self.assertTrue(bucket.addNode(self.get_random_node()))
        self.assertFalse(bucket.addNode(self.get_random_node()))

    @TestCase(1, 2 ** 4 - 1, 5)
    def test_addNode_order(self, bucket):
        nodes = [self.get_random_node() for i in range(3)]
        for node in nodes:
            bucket.addNode(node)
        for index, node in enumerate(bucket.getNodes()):
            self.assertEqual(node, nodes[index])

    @TestCase(1, 2 ** 4 - 1, 5)
    def test_isNewNode(self, bucket):
        nodes = [self.get_random_node() for i in range(2)]
        bucket.addNode(nodes[0])
        self.assertFalse(bucket.isNewNode(nodes[0]))
        self.assertTrue(bucket.isNewNode(nodes[1]))
