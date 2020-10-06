import unittest
import sys

sys.path.append('../')

from Board import Board
from Tile import Tile
from Hole import Hole
from ext.MockHelper import MockHelper
import tkinter as tk


class BoardTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BoardTests, self).__init__(*args, **kwargs)

        # initialize tkinter
        tk.Tcl()

        # prevent __get_sprite from getting called as
        # tkinter is not initialized
        #with MockHelper(Board, "_Board__get_sprite"):
        #    self.__good_board1 = Board.homogeneous(10)

    def test_init_fail1(self):
        # Tests constructor failing due to invalid tiles collection
        # type being passed
        with self.assertRaises(ValueError):
            Board(['rows'])

    def test_init_fail2(self):
        # Tests constructor failing due to tiles collection
        # missing points
        with self.assertRaises(ValueError):
            Board({(0, 0): Tile(2), (0, 1): Tile(2),
                   (1, 1): Tile(2)})

    def test_init_fail3(self):
        # Tests constructor failing due to there being invalid
        # tiles in the collection
        with self.assertRaises(ValueError):
            Board({(0, 0): Tile(2), (0, 1): Tile(2),
                   (1, 0): Hole(), (1, 1): None})

    def test_init_success(self):
        # Tests successful constructor
        # Make sure __load_sprites() is called upon init
        with MockHelper(Board, "_Board__load_sprites"):
            # Create board with 10 rows x 20 cols
            b = Board({(0, 0): Tile(2), (0, 1): Tile(2),
                   (1, 0): Hole(), (1, 1): Hole()})

            # Check externally accessible properties
            self.assertEqual(b.rows, 2)
            self.assertEqual(b.cols, 2)
            self.assertEqual(b.tile_no, 4)

    def test_min_oft_and_holes_fail1(self):
        # Tests min_oft_and_holes failing due to an invalid
        # minimum number of one fish tiles being provided.
        with self.assertRaises(ValueError):
            Board.min_oft_and_holes(-10, 10)

    def test_min_oft_and_holes_fail2(self):
        # Tests min_oft_and_holes failing due to an invalid
        # minimum number of one fish tiles being provided.
        with self.assertRaises(ValueError):
            Board.min_oft_and_holes(10, -10)