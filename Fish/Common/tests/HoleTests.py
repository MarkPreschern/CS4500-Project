import sys
import unittest

sys.path.append('../')

from Hole import Hole


class HoleTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(HoleTests, self).__init__(*args, **kwargs)

    def test_is_hole(self):
        # Tests if a hole is a hole
        self.assertTrue(Hole().is_hole)

    def test_is_tile(self):
        # Tests if a hole is a tile
        self.assertFalse(Hole().is_tile)
