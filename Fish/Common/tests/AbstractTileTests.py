import sys
import unittest

sys.path.append('../')

from AbstractTile import AbstractTile


class AbstractTileTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AbstractTileTests, self).__init__(*args, **kwargs)

    def test_is_hole(self):
        # Tests if a hole is a hole
        self.assertFalse(AbstractTile().is_hole)

    def test_is_tile(self):
        # Tests if a hole is a tile
        self.assertFalse(AbstractTile().is_tile)
