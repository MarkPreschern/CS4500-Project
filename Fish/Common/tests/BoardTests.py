import unittest
import sys

sys.path.append('../')

from Board import Board
from Tile import Tile
from Hole import Hole
from ext.MockHelper import MockHelper
import tkinter as tk
from MovementDirection import MovementDirection


class BoardTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BoardTests, self).__init__(*args, **kwargs)

        # initialize tkinter
        tk.Tcl()

        # prevent __get_sprite from getting called as
        # tkinter is not initialized
        with MockHelper(Board, "_Board__get_sprite"):
            self.__no_hole_board1 = Board.min_oft_and_holes(4, [(2,3), (1,2)])

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
            Board.min_oft_and_holes(-10, [])

    def test_min_oft_and_holes_fail2(self):
        # Tests min_oft_and_holes failing due to an invalid
        # minimum number of one fish tiles being provided.
        with self.assertRaises(ValueError):
            Board.min_oft_and_holes(10, (1, 2))

    def test_min_oft_and_holes_success1(self):
        # Tests successful min_oft_and_holes with holes

        # prevent __load_sprites from getting called as
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            board = Board.min_oft_and_holes(4, [(1, 0)])

            # Retrive tiles
            tiles = board.tiles

            # Make sure we have a large enough board to
            # accomodate tiles asked for
            self.assertGreaterEqual(len(tiles), 5)

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
            self.assertEqual(hole_cnt, 1)
            # Make sure we have at least min # provided
            # of one fish tiles
            self.assertGreaterEqual(one_fish_tile_cnt, 4)

    def test_min_oft_and_holes_success2(self):
        # Tests successful min_oft_and_holes with no holes

        # prevent __load_sprites from getting called as
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            board = Board.min_oft_and_holes(10, [])

            # Retrive tiles
            tiles = board.tiles

            # Make sure we have a large enough board to
            # accommodate tiles asked for
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

    def test_render_fail1(self):
        # Tests failing render due to an invalid frame being
        # provided
        with self.assertRaises(TypeError):
            self.__no_hole_board1.render('ohai')
    
    def test_get_reachable_positions_homogenous(self):
        # Test get_reachable_positions for a homogenous board

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            # Create a board with 5 rows and 2 columns
            b = Board.homogeneous(3, 5, 2)

            # Reachable positions from (0, 0)
            expected_1 = [(1, 0), (2, 1), (3, 1), (2, 0), (4, 0)]
            actual_1 = b.get_reachable_positions((0, 0))

            # Reachable positions from (3, 0)
            expected_2 = [(2, 0), (1, 0), (2, 1), (1, 1), (4, 1), (4, 0)]
            actual_2 = b.get_reachable_positions((3, 0))

            # Reachable positions from (2, 1)
            expected_3 = [(1, 0), (0, 0), (0, 1), (1, 1), (3, 1), (4, 1), (3, 0), (4, 0)]
            actual_3 = b.get_reachable_positions((2, 1))

            # Assert that both the expected lists and actual output have the same
            # elements the same number of times (i.e. lists are equal ignoring order)
            self.assertCountEqual(expected_1, actual_1)
            self.assertCountEqual(expected_2, actual_2)
            self.assertCountEqual(expected_3, actual_3)

    def test_get_reachable_positions_with_holes(self):
        # Test get_reachable_positions for a board with holes

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            # Create a board with 5 rows and 2 columns
            b = Board.homogeneous(3, 5, 2)
            b.remove_tile((1, 0))

            # Reachable positions from (0, 0)
            # Hole removes (1, 0), (2, 1), and (3, 1)
            expected_1 = [(2, 0), (4, 0)]
            actual_1 = b.get_reachable_positions((0, 0))

            # Reachable positions from (3, 0)
            # Hole removes (1, 0)
            expected_2 = [(2, 0), (2, 1), (1, 1), (4, 1), (4, 0)]
            actual_2 = b.get_reachable_positions((3, 0))

            # Reachable positions from (2, 1)
            # Hole removes (1, 0) and (0, 0)
            expected_3 = [(0, 1), (1, 1), (3, 1), (4, 1), (3, 0), (4, 0)]
            actual_3 = b.get_reachable_positions((2, 1))
            
            # Assert that inserting a hole interrupts the straight line paths
            # and reduces the number of reachable positions
            self.assertCountEqual(expected_1, actual_1)
            self.assertCountEqual(expected_2, actual_2)
            self.assertCountEqual(expected_3, actual_3)
    
    def test_get_reachable_positions_with_all_holes(self):
        # Test get_reachable_positions on a board with all holes

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            # Create board with 2 rows and 1 column
            b = Board.homogeneous(3, 2, 1)

            # Verify that there are reachable tiles prior to removal
            expected_1 = [(1, 0)]
            actual_1 = b.get_reachable_positions((0, 0))

            expected_2 = [(0, 0)]
            actual_2 = b.get_reachable_positions((1, 0))

            self.assertCountEqual(expected_1, actual_1)
            self.assertCountEqual(expected_2, actual_2)

            # Remove all tiles
            b.remove_tile((0, 0))
            b.remove_tile((1, 0))

            expected_3_4 = []
            actual_3 = b.get_reachable_positions((0, 0))
            actual_4 = b.get_reachable_positions((1, 0))

            # Verify that get_reachable_tiles does not include/traverse over
            # holes when building the list of reachable positions
            self.assertEqual(expected_3_4, actual_3)
            self.assertEqual(expected_3_4, actual_4)

    def test_get_reachable_positions_fail1(self):
        # Test failed reachable position computation due to invalid position typing
        with self.assertRaises(TypeError):
            self.__no_hole_board1.get_reachable_positions([0])
    
    def test_get_reachable_positions_fail2(self):
        # Test failed reachable position computation due to invalid position on board
        with self.assertRaises(ValueError):
            self.__no_hole_board1.get_reachable_positions((100, -5))
    
    def test_get_reachable_positions_on_single_tile(self):
        # Test get_reachable_positions on a board with one tile

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            b = Board.homogeneous(3, 1, 1)

            self.assertEqual(b.get_reachable_positions((0, 0)), [])
    
    def test_compute_edge_list(self):
        # Test compute edge list on a standard board

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            b = Board.homogeneous(3, 3, 2)

            expected = {
                (0, 0) : {
                    MovementDirection.BottomRight : (1, 0),
                    MovementDirection.Bottom : (2, 0)},
                (0, 1) : {
                    MovementDirection.BottomLeft : (1, 0),
                    MovementDirection.Bottom : (2, 1),
                    MovementDirection.BottomRight : (1, 1)
                },
                (1, 0) : {
                    MovementDirection.BottomLeft : (2, 0),
                    MovementDirection.TopLeft : (0, 0),
                    MovementDirection.BottomRight : (2, 1),
                    MovementDirection.TopRight : (0, 1)
                },
                (1, 1) : {
                    MovementDirection.BottomLeft : (2, 1),
                    MovementDirection.TopLeft : (0, 1)
                }, 
                (2, 0) : {
                    MovementDirection.Top : (0, 0),
                    MovementDirection.TopRight : (1, 0)
                },
                (2, 1) : {
                    MovementDirection.TopLeft : (1, 0),
                    MovementDirection.Top : (0, 1),
                    MovementDirection.TopRight : (1, 1)
                }
            }

            self.assertDictEqual(b._Board__compute_reachable_edge_list(), expected)

            # Should also be the same after removing one tile
            b.remove_tile((0, 0))

            self.assertDictEqual(b._Board__compute_reachable_edge_list(), expected)

    def test_compute_edge_list_one_tile(self):
        # Test compute edge list on a board with one tile

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            b = Board.homogeneous(3, 1, 1)

            self.assertDictEqual(b._Board__compute_reachable_edge_list(), {(0, 0) : {}})

    def test_find_straight_path(self):
        # Test find straight path on a standard board

        # Prevent load sprites from being called because
        # tkinter is not initialized
        with MockHelper(Board, "_Board__load_sprites"):
            b = Board.homogeneous(3, 3, 2)

            # Test a tile with multiple tiles in a row - we already know finding neighbors works
            # from testing edge list
            top_right = b._Board__find_straight_path((2, 0), MovementDirection.TopRight)
            
            self.assertCountEqual(top_right, [(1, 0), (0, 1)])

            # See path shorten after removing a tile
            b.remove_tile((1, 0))

            top_right = b._Board__find_straight_path((2, 0), MovementDirection.TopRight)

            self.assertEqual(top_right, [])

            # Verify empty path for direction that (2, 0) does not have neighbors
            top_left = b._Board__find_straight_path((2, 0), MovementDirection.TopLeft)
            self.assertEqual(top_left, [])

            # Verify invalid board positions return no straight path
            no_path = b._Board__find_straight_path((100, -5), MovementDirection.TopRight)
            self.assertEqual(no_path, [])
    
    def test_find_straight_path_fail1(self):
        # Test failed find straight path due to invalid pos
        with self.assertRaises(TypeError):
            self.__no_hole_board1._Board__find_straight_path([100, -5], MovementDirection.Top)
    
    def test_find_straight_path_fail2(self):
        # Test failed find straight path due to invalid direction
        with self.assertRaises(TypeError):
            self.__no_hole_board1._Board__find_straight_path((0, 0), "TopRight")

    def test_find_straight_path_fail3(self):
        # Test failed find straight path due to invalid edge list
        with self.assertRaises(TypeError):
            self.__no_hole_board1._Board__find_straight_path((0, 0), MovementDirection.TopRight, edge_list = [(0, 0), (1, 0)])