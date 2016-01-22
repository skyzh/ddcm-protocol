import unittest

import ddcm

from . import const
from . import utils

class NodeTest(unittest.TestCase):
    def test_get_hash_string(self):
        node = ddcm.Node(b'\x9e\x93\x6d\xd8\x92\x6a\x14\xfe\x8b\x8c\x87\x7f\x71\x6e\x7e\x39\x09\xd8\x8d\xb5')
        self.assertEqual("9e936dd8926a14fe8b8c877f716e7e3909d88db5", node.get_hash_string())
    def test_distance(self):
        node = ddcm.Node(b'\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff\x00\xff')
        node_hash = 2 ** 160
        self.assertEqual(node.distance(node_hash), 1467188414129855847846500727007007856308290257151)
