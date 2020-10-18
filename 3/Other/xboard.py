#!/usr/bin/python3

# Imports
import glob
import json
import re
import sys

sys.path.append("../Fish/Common/")

from tile import Tile
from hole import Hole
from board import Board

# The pattern for the input filepaths
INPUT_FILEPATH = "Tests/*-in.json"

# The pattern for the output filepaths
OUTPUT_FILEPATH = "Tests/*-out.json"


def fail_test(test_no: int, msg=None):
    """
    Output a message indicating that the test failed.

    :param test_no: the number of the json files being tested (i.e. test_no = 1 for 1-in.json, 1-out.json)
    :param msg: an optional error message to append to the one printed out (can be configured to give more info)
    """
    # Initialize error message
    error_msg = "ERROR: Test #{} failed".format(test_no)

    # Append the extra message if provided
    if msg:
        error_msg = error_msg + " - " + str(msg)

    # Print the message to stdout
    print(error_msg)


def pass_test(test_no: int, msg=None):
    """
    Output a message indicating that the test passed.

    :param test_no: the number of the json files being tested (i.e. test_no = 1 for 1-in.json, 1-out.json)
    :param msg: an optional success message to append to the one printed out (can be configured to give more info)
    """
    # Initialize success message
    success_msg = "SUCCESS: Test #{} passed".format(test_no)

    # Append the extra message if provided
    if msg:
        success_msg = success_msg + " - " + str(msg)

    # Print the message to stdout
    print(success_msg)


def validate_input_json(input_json: dict) -> bool:
    """
    Validate the input json and ensure it matches the testing specifications

    :param input_json: the input json for the appropriate input file
    :return: a boolean indicating if the input_json is valid
    """
    # Validate the input json format
    # If position is not present in the input_json, print an error and end the test
    if "position" not in input_json.keys():
        raise ValueError("Expected position in test, but no position was provided.")

    # If board is not present in the input_json, print an error and end the test
    if "board" not in input_json.keys():
        raise ValueError("Expected board in test, but no board was provided.")

    # If the value of the 'position' field is not a list, print an error and end the test
    if not isinstance(input_json['position'], list):
        raise TypeError("Expected a JSON array for position.")

    # If the value of the 'board' field is not a list, print an error and end the test
    if not isinstance(input_json['board'], list):
        raise TypeError("Expected a JSON array for board.")

    # If the value of the 'position' field is not the specified length, print an error and end the test 
    if not len(input_json['position']) == 2:
        raise ValueError("Expected position of length 2 but length was {}".format(len(input_json['position'])))

    # If the value of the 'board' field is not at least length 1 (i.e. does not have at least one row),
    # print an error and end the test
    if len(input_json['board']) < 1:
        raise ValueError("Cannot have a board of length 0.")

    # On successful validation, return True
    return True


def validate_output_json(output_json: int) -> bool:
    """
    Validate the output json provided by the output file for a given test.

    :param output_json: the output json for the corresponding test number that will be validated
    :return: a boolean indicating if the provided output json is valid
    """
    # Validate the output json format for the corresponding file
    if not isinstance(output_json, int):
        raise TypeError("Output file does not have the proper format (expected a number)")

    # On successful validation, return True
    return True


def initialize_board(json_board: list) -> Board:
    """
    Initialize a Board object based on the given json representation of the board.

    :param json_board: the json representation of a board as provided by the testing specifications
    :return: a Board object consisting of the tiles described by the board_json
    """
    # Keep track of the current row and column
    current_row = 0
    current_col = 0

    # Dict to store tile objects
    tiles = {}

    # Iterate through each row in the json board
    for row in json_board:
        for _ in row:
            try:
                # The current position
                current_pos = (current_row, current_col)

                # The number of fish according to the json object
                num_fish = json_board[current_row][current_col]

                # Initialize a new tile/hole according to the number provided
                new_tile = Tile(num_fish) if num_fish > 0 else Hole()

                # Add the tile to the current collection of tiles
                tiles[current_pos] = new_tile

                # Move to the next column
                current_col += 1
            except ValueError:
                raise ValueError("Issue initializing tile because of an invalid number of fish.")
            except TypeError:
                raise TypeError("Issue initializing tile because a non-integer value was encountered.")

        # Move to the next row and reset columns
        current_row += 1
        current_col = 0

    try:
        # Disable sprite rendering for testing purposes
        Board.DISABLE_SPRITE_MANAGER = True

        # Initialize a board with the given dictionary of tiles
        board = Board(tiles)
        return board
    except ValueError:
        raise ValueError("Could not initialize board - perhaps there was an error initializing the tiles?")


def xboard():
    """
    Execute the main program logic of xboard. Specifically,
    test that the number of tiles reachable from the given position
    on the specified board from the input JSON matches the expected value
    given in the output JSON for all test numbers present in the Tests directory.
    """
    # Read input/output files
    input_files = glob.glob(INPUT_FILEPATH)
    output_files = glob.glob(OUTPUT_FILEPATH)

    # Test all input files
    for filepath in input_files:
        # Extract the end of the filepath (excluding all parent directories for ease of processing)
        end_of_filepath = re.search(r'/[0-9]-in.json', filepath).group(0)

        # Extract the file number from the input file
        file_no = end_of_filepath.strip("/").strip("-in.json")

        # Determine the proper output filepath for the current test number
        matching_output_file = OUTPUT_FILEPATH.replace("*", file_no)

        # If the necessary output file does not exist, skip this test
        if matching_output_file not in output_files:
            fail_test(file_no, "Matching output file does not exist.")
            continue

        # Once there is a matching output file, read the input file and convert to json
        with open(filepath, "r") as input_obj, open(matching_output_file) as output_obj:
            # Read the string from the input file and convert to json
            input_json = json.loads(input_obj.read())

            # Read the string from the output file and convert to json
            output_json = json.loads(output_obj.read())

            # Validate the input and output json
            try:
                validate_input_json(input_json)
                validate_output_json(output_json)
            except ValueError as e1:
                fail_test(file_no, str(e1))
                continue
            except TypeError as e2:
                fail_test(file_no, str(e2)) 
                continue

            # Create a board object with the proper representation
            board = None
            try:
                board = initialize_board(input_json['board'])
            except ValueError as e1:
                fail_test(file_no, str(e1))
                continue
            except TypeError as e2:
                fail_test(file_no, str(e2))
                continue

            # Get the number of reachable positions from the specified position in the json input
            pos = input_json['position']
            number_of_positions = len(board.get_reachable_positions((pos[0], pos[1])))

            # Compare the number of reachable positions to the value in the output file
            if number_of_positions != output_json:
                fail_test(file_no, "Expected: {}; Actual: {}".format(output_json, number_of_positions))
            else:
                pass_test(file_no)