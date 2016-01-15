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
