import sys
import unittest
import constants as ct

sys.path.append('../')

from tile import Tile


class TileTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TileTests, self).__init__(*args, **kwargs)

    def test_init_fail1(self):
        # tests failing init due to an invalid number of fish
        # being provided
        with self.assertRaises(ValueError):
            Tile(ct.MIN_FISH_PER_TILE - 1)

        with self.assertRaises(ValueError):
            Tile(ct.MAX_FISH_PER_TILE + 1)

        with self.assertRaises(ValueError):
            Tile('kthxbye')

    def test_init_success(self):
        # tests successful init
        tile = Tile(2)

        self.assertEqual(tile.fish_no, 2)

    def test_is_hole(self):
        # Tests if a tile is a hole
        self.assertFalse(Tile(2).is_hole)

    def test_is_tile(self):
        # Tests if a tile is a tile (hmm...)
        self.assertTrue(Tile(2).is_tile)
