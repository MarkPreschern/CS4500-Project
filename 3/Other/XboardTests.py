import json
import os
import sys
import unittest

from io import StringIO
from unittest.mock import patch

import xboard

sys.path.append("../Fish/Common")

from board import Board
from tile import Tile
from hole import Hole
from position import Position


class XboardTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(XboardTests, self).__init__(*args, **kwargs)

    def test_validate_input_json_input_success(self):
        # Test successful json validation based on the format specified by the assignment

        # Create valid json object
        valid_json = json.loads("{\"position\":[0, 0], \"board\":[[0, 1, 1], [1, 1, 1]]}")

        # Validate input json with test #4
        self.assertTrue(xboard.validate_input_json(valid_json))

    def test_validate_input_json_with_no_position(self):
        # Test failure of json validation due to lack of position object

        # Create json object with no position
        invalid_json = json.loads("{\"board\":[[0, 1, 1], [1, 1, 1]]}")

        with self.assertRaises(ValueError):
            xboard.validate_input_json(invalid_json)

    def test_validate_input_json_with_no_board(self):
        # Test failure of json validation due to lack of position object

        # Create json object with no board
        invalid_json = json.loads("{\"position\":[0, 0]}")

        with self.assertRaises(ValueError):
            xboard.validate_input_json(invalid_json)

    def test_validate_input_json_with_invalid_position_type(self):
        # Test failure of json validation due value of position not being a list

        # Create json object with invalid position type
        invalid_json = json.loads("{\"position\":\"hello\", \"board\":[[0, 1, 1], [1, 1, 1]]}")

        with self.assertRaises(TypeError):
            xboard.validate_input_json(invalid_json)

    def test_validate_input_json_with_invalid_board_type(self):
        # Test failure of json validation due to value of board not being a list

        # Create json object with no list
        invalid_json = json.loads("{\"position\":\"hello\", \"board\":4}")

        with self.assertRaises(TypeError):
            xboard.validate_input_json(invalid_json)

    def test_validate_input_json_with_invalid_position_length(self):
        # Test failure of json validation due to position not being of length 2

        # Create json object with invalid position length
        invalid_json = json.loads("{\"position\":[0], \"board\":[[0, 1, 1], [1, 1, 1]]}")

        with self.assertRaises(ValueError):
            xboard.validate_input_json(invalid_json)

    def test_validate_input_json_with_invalid_board_length(self):
        # Test failure of json validation due to board being length 0

        # Create json object with invalid position length
        invalid_json = json.loads("{\"position\":[0, 0], \"board\":[]}")

        with self.assertRaises(ValueError):
            xboard.validate_input_json(invalid_json)

    def test_initialize_board_success(self):
        # Test successful validation of a board object from valid board json

        # Create json board object based on the provided representation
        valid_json = json.loads("[[1, 0], [3, 5], [2, 4]]")

        # Board obtained from the initialize_board function
        result_board = xboard.initialize_board(valid_json)

        # Test properties of the board
        self.assertTrue(isinstance(result_board, Board))
        self.assertEquals(result_board.rows, 3)
        self.assertEquals(result_board.cols, 2)
        self.assertEquals(result_board.tile_no, 6)

        # Expected tile dict
        expected_tiles = \
        {
            Position(0, 0): Tile(1),
            Position(0, 1): Hole(),
            Position(1, 0): Tile(3),
            Position(1, 1): Tile(5),
            Position(2, 0): Tile(2),
            Position(2, 1): Tile(4)
        }

        # Verify all the positions in the board are the same as expected
        self.assertCountEqual(expected_tiles.keys(), result_board.tiles.keys())
        
        # Verify that all tiles have the correct number of fish
        for key in expected_tiles:
            tile = expected_tiles[key]

            # Tile on initialized board
            actual_tile = result_board.get_tile(key)

            # Assert both tiles are the same type
            self.assertEqual(tile.is_tile, actual_tile.is_tile)

            # If the tiles are both tiles, assert that the ones on the board
            # have the expected number of fish
            if tile.is_tile:
                self.assertEqual(tile.fish_no, actual_tile.fish_no)

    def test_initialize_board_invalid_tile_type(self):
        # Test failure to initialize board due to the board containing an invalid type
        
        # Invalid json board representation
        invalid_json = json.loads("[[1, 0, 0], [\"one\", 0, 0]]")

        with self.assertRaises(TypeError):
            result_board = xboard.initialize_board(invalid_json)

    def test_initialize_board_invalid_tile_no(self):
        # Test failure to initialize board due to a board containing a number outside the acceptable range
        
        # Invalid json board representation
        invalid_json = json.loads("[[1, 0, 0], [1, 8, 0]]")

        with self.assertRaises(ValueError):
            result_board = xboard.initialize_board(invalid_json)

    def test_initialize_board_padding(self):
        # Test successful initialize board with need for padding

        # Invalid json board representation
        valid_json = json.loads("[[1], [1, 2], [0, 2, 3]]")

        # Board obtained from the initialize_board function
        result_board = xboard.initialize_board(valid_json)

        # Test properties of the board
        self.assertTrue(isinstance(result_board, Board))
        self.assertEquals(result_board.rows, 3)
        self.assertEquals(result_board.cols, 3)
        self.assertEquals(result_board.tile_no, 9)

        # Expected tile dict
        expected_tiles = \
        {
            Position(0, 0): Tile(1),
            Position(0, 1): Hole(),
            Position(0, 2): Hole(),
            Position(1, 0): Tile(1),
            Position(1, 1): Tile(2),
            Position(1, 2): Hole(),
            Position(2, 0): Hole(),
            Position(2, 1): Tile(2),
            Position(2, 2): Tile(3)
        }

        # Verify all the positions in the board are the same as expected
        self.assertCountEqual(expected_tiles.keys(), result_board.tiles.keys())
        
        # Verify that all tiles have the correct number of fish
        for key in expected_tiles:
            tile = expected_tiles[key]

            # Tile on initialized board
            actual_tile = result_board.get_tile(key)

            # Assert both tiles are the same type
            self.assertEqual(tile.is_tile, actual_tile.is_tile)

            # If the tiles are both tiles, assert that the ones on the board
            # have the expected number of fish
            if tile.is_tile:
                self.assertEqual(tile.fish_no, actual_tile.fish_no)
    
    def test_initialize_board_padding2(self):
        # Test initializing board with the need for padding less readily apparent

        # Invalid json board representation
        valid_json = json.loads("[[1, 3, 4], [1, 2], [1, 0, 3, 5, 4], [0, 2, 3]]")

        # Board obtained from the initialize_board function
        result_board = xboard.initialize_board(valid_json)

        # Test properties of the board
        self.assertTrue(isinstance(result_board, Board))
        self.assertEquals(result_board.rows, 4)
        self.assertEquals(result_board.cols, 5)
        self.assertEquals(result_board.tile_no, 20)

        # Expected tile dict
        expected_tiles = \
        {
            Position(0, 0): Tile(1),
            Position(0, 1): Tile(3),
            Position(0, 2): Tile(4),
            Position(0, 3): Hole(),
            Position(0, 4): Hole(),
            Position(1, 0): Tile(1),
            Position(1, 1): Tile(2),
            Position(1, 2): Hole(),
            Position(1, 3): Hole(),
            Position(1, 4): Hole(),
            Position(2, 0): Tile(1),
            Position(2, 1): Hole(),
            Position(2, 2): Tile(3),
            Position(2, 3): Tile(5),
            Position(2, 4): Tile(4),
            Position(3, 0): Hole(),
            Position(3, 1): Tile(2),
            Position(3, 2): Tile(3),
            Position(3, 3): Hole(),
            Position(3, 4): Hole()
        }

        # Verify all the positions in the board are the same as expected
        self.assertCountEqual(expected_tiles.keys(), result_board.tiles.keys())
        
        # Verify that all tiles have the correct number of fish
        for key in expected_tiles:
            tile = expected_tiles[key]

            # Tile on initialized board
            actual_tile = result_board.get_tile(key)

            # Assert both tiles are the same type
            self.assertEqual(tile.is_tile, actual_tile.is_tile)

            # If the tiles are both tiles, assert that the ones on the board
            # have the expected number of fish
            if tile.is_tile:
                self.assertEqual(tile.fish_no, actual_tile.fish_no)