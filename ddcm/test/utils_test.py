import ddcm
import unittest

from . import const
from . import utils

class UtilsTest(unittest.TestCase):
    def test_commonPrefix(self):
        self.assertEqual(len(ddcm.utils.commonPrefix([
            b'\xff\xff',
            b'\xff\xfe',
            b'\xff\xfd'
        ])), 8 + 8 - 2)
    def test_dump_node_hex(self):
        node_hex = ddcm.utils.dump_node_hex("9e936dd8926a14fe8b8c877f716e7e3909d88db5")
        self.assertEqual(
            node_hex,
            b'\x9e\x93\x6d\xd8\x92\x6a\x14\xfe\x8b\x8c\x87\x7f\x71\x6e\x7e\x39\x09\xd8\x8d\xb5'
        )
