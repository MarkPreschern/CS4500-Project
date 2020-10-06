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
        with MockHelper(Board, "_Board__get_sprite"):
            self.__no_hole_board1 = Board.min_oft_and_holes(10, 0)

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
        # Make sure __load_sprites() is not called upon init
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

    def test_min_oft_and_holes_success1(self):
        # Tests successful min_oft_and_holes with holes

        # prevent __load_sprites from getting called as
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            board = Board.min_oft_and_holes(10, 2)

            # Retrive tiles
            tiles = board.tiles

            # Make sure we have a large enough board to
            # accomodate tiles asked for
            self.assertGreaterEqual(len(tiles), 12)

            # Initialize counts
            hole_cnt = 0
            one_fish_tile_cnt = 0

            # Cycle over tiles and count
            for _, tile in tiles.items():
                if tile.is_tile:
                    # Increment one fish tile count if it's only
                    # one fish
                    if tile.fish_no == 1:
                        one_fish_tile_cnt += 1
                elif tile.is_hole:
                    hole_cnt += 1
                else:
                    raise ValueError(f'Tile is neither hole nor tile: {type(tile)}!')

            # Make sure we have the right number of holes
            self.assertEqual(hole_cnt, 2)
            # Make sure we have at least min # provided
            # of one fish tiles
            self.assertGreaterEqual(one_fish_tile_cnt, 10)

    def test_min_oft_and_holes_success2(self):
        # Tests successful min_oft_and_holes with no holes

        # prevent __load_sprites from getting called as
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            board = Board.min_oft_and_holes(10, 0)

            # Retrive tiles
            tiles = board.tiles

            # Make sure we have a large enough board to
            # accomodate tiles asked for
            self.assertGreaterEqual(len(tiles), 10)

            # Initialize counts
            hole_cnt = 0
            one_fish_tile_cnt = 0

            # Cycle over tiles and count
            for _, tile in tiles.items():
                if tile.is_tile:
                    # Increment one fish tile count if it's only
                    # one fish
                    if tile.fish_no == 1:
                        one_fish_tile_cnt += 1
                elif tile.is_hole:
                    hole_cnt += 1
                else:
                    raise ValueError(f'Tile is neither hole nor tile: {type(tile)}!')

            # Make sure we have the right number of holes
            self.assertEqual(hole_cnt, 0)
            # Make sure we have at least min # provided
            # of one fish tiles
            self.assertGreaterEqual(one_fish_tile_cnt, 10)

    def test_homogeneous_fail1(self):
        # Tests failing homogeneous due to an invalid number
        # of tile_fish no
        with self.assertRaises(ValueError):
            Board.homogeneous('ok')

        with self.assertRaises(ValueError):
            Board.homogeneous(0)

        with self.assertRaises(ValueError):
            Board.homogeneous(210)

    def test_homogeneous_fail2(self):
        # Tests failing homogeneous due to an invalid number
        # of rows
        with self.assertRaises(ValueError):
            Board.homogeneous(1, -1)

    def test_homogeneous_fail3(self):
        # Tests failing homogeneous due to an invalid number
        # of cols
        with self.assertRaises(ValueError):
            Board.homogeneous(1, 1, -1)

    def test_homogeneous_success1(self):
        # Tests successful homogeneous with no given size
        b = Board.homogeneous(3)

        for tile in b.tiles.values():
            self.assertTrue(tile.is_tile)
            self.assertTrue(tile.fish_no, 3)

    def test_homogeneous_success2(self):
        # Tests successful homogeneous with given size
        b = Board.homogeneous(3, 12, 3)

        self.assertEqual(b.rows, 12)
        self.assertEqual(b.cols, 3)
        self.assertEqual(b.tile_no, 12 * 3)
        self.assertEqual(len(b.tiles.values()), 12 * 3)

        for tile in b.tiles.values():
            self.assertTrue(tile.is_tile)
            self.assertTrue(tile.fish_no, 3)

    def test_remove_tile_fail1(self):
        # Tests failing remove_tile due to point provided
        # being invalid
        with self.assertRaises(ValueError):
            self.__no_hole_board1.remove_tile([12, 'ok'])

    def test_remove_tile_fail2(self):
        # Tests failing remove_tile due to point provided
        # not existing
        with self.assertRaises(ValueError):
            self.__no_hole_board1.remove_tile((32, 23))

    def test_remove_tile_success(self):
        # Tests successful remove_tile
        self.__no_hole_board1.remove_tile((0, 0))
        # Tile should not be a hole
        self.assertTrue(self.__no_hole_board1.get_tile((0, 0)).is_hole)

    def test_get_tile_fail1(self):
        # Tests failing get_tile due to point being invalid
        with self.assertRaises(TypeError):
            self.__no_hole_board1.get_tile('ok')

    def test_get_tile_fail2(self):
        # Tests failing get_tile due to non-existent point
        with self.assertRaises(ValueError):
            self.__no_hole_board1.get_tile((120, 10))

    def test_get_tile_success(self):
        # Tests successful get_tile
        # Make sure __load_sprites() is not called upon init
        with MockHelper(Board, "_Board__load_sprites"):
            tile1 = Tile(2)
            tile2 = Tile(3)

            # Create board with 10 rows x 20 cols
            b = Board({(0, 0): tile1, (0, 1): tile2})

            self.assertEqual(b.get_tile((0, 0)), tile1)
            self.assertEqual(b.get_tile((0, 1)), tile2)

    def test_render_tile_fail1(self):
        # Tests failing render_tile due to an invalid point being
        # provided
        with self.assertRaises(TypeError):
            self.__no_hole_board1.render_tile(tk.Frame(), [])

    def test_render_tile_fail2(self):
        # Tests failing render_tile due to an invalid frame being
        # provided
        with self.assertRaises(TypeError):
            self.__no_hole_board1.render_tile('ohai', (0, 0))

    def test_render_tile_success(self):
        # Tests successful render_tile
        canvas = self.__no_hole_board1.render_tile(tk.Frame(), (0, 0))

        self.assertIsInstance(canvas, tk.Canvas)
