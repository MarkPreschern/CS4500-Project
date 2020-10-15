import json
import os
import sys
import unittest

from io import StringIO
from unittest.mock import patch

import xboard

sys.path.append("../Fish/Common")

from Board import Board
from Tile import Tile
from Hole import Hole


class XboardTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(XboardTests, self).__init__(*args, **kwargs)

    def test_xboard_no_output_file(self):
        # Test the case where there is an input file with no corresponding output file

        # Mock stdout
        with patch("sys.stdout", new=StringIO()) as mocked_stdout:
            # Create a test input file
            os.system("touch Tests/4-in.json")

            # Run the xboard method, which would produce an error message upon finding
            # an input file with no corresponding output file
            xboard.xboard()

            # Initialize expected output
            expected_output = "SUCCESS: Test #1 passed\n"
            expected_output = expected_output + "SUCCESS: Test #2 passed\n"
            expected_output = expected_output + "SUCCESS: Test #3 passed\n"
            expected_output = expected_output + "ERROR: Test #4 failed - Matching output file does not exist.\n"

            # Remove temporary test input file for cleanup
            os.system("rm Tests/4-in.json")

            # Assert that the mocked standard output is equal to the expected output
            self.assertEqual(mocked_stdout.getvalue(), expected_output)

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

    def test_validate_output_json_success(self):
        # Test success of output json validation

        # Create valid json object that matches the specified format
        valid_json = json.loads("4")

        self.assertTrue(xboard.validate_output_json(valid_json))

    def test_validate_output_json_with_invalid_count_type(self):
        # Test failure of output json validation due to value in output not being an integer

        # Create json object with invalid output format
        valid_json = json.loads("\"hello\"")

        with self.assertRaises(TypeError):
            xboard.validate_output_json(valid_json)

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
            (0, 0): Tile(1),
            (0, 1): Hole(),
            (1, 0): Tile(3),
            (1, 1): Tile(5),
            (2, 0): Tile(2),
            (2, 1): Tile(4)
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

    def test_initialize_board_invalid_setup(self):
        # Test failure due to the board being in an invalid format

        # Invalid json board representation
        invalid_json = json.loads("[[1], [1, 2], [0, 2, 3]]")

        with self.assertRaises(ValueError):
            result_board = xboard.initialize_board(invalid_json)

    def test_fail_test_no_msg(self):
        # Test fail_test with no message

        # Mock stdout
        with patch("sys.stdout", new=StringIO()) as mocked_stdout:
            xboard.fail_test(4)

            # Initialize expected output
            expected_output = "ERROR: Test #4 failed\n"

            self.assertEqual(expected_output, mocked_stdout.getvalue())

    def test_pass_test_no_msg(self):
        # Test pass_test with no message

        # Mock stdout
        with patch("sys.stdout", new=StringIO()) as mocked_stdout:
            xboard.pass_test(4)

            # Initialize expected output
            expected_output = "SUCCESS: Test #4 passed\n"

            self.assertEqual(expected_output, mocked_stdout.getvalue())

    def test_fail_test_msg(self):
        # Test fail_test with a message

        # Mock stdout
        with patch("sys.stdout", new=StringIO()) as mocked_stdout:
            xboard.fail_test(4, "This is a failure.")

            # Initialize expected output
            expected_output = "ERROR: Test #4 failed - This is a failure.\n"

            self.assertEqual(expected_output, mocked_stdout.getvalue())

    def test_pass_test_msg(self):
        # Test pass_test with a message

        # Mock stdout
        with patch("sys.stdout", new=StringIO()) as mocked_stdout:
            xboard.pass_test(4, "This is a success.")

            # Initialize expected output
            expected_output = "SUCCESS: Test #4 passed - This is a success.\n"

            self.assertEqual(expected_output, mocked_stdout.getvalue())