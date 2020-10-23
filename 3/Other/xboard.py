#!/usr/bin/python3

# Imports
import json
import re
import sys

sys.path.append("../Fish/Common/")

from tile import Tile
from hole import Hole
from board import Board
from position import Position


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


def initialize_board(json_board: list) -> Board:
    """
    Initialize a Board object based on the given json representation of the board.

    :param json_board: the json representation of a board as provided by the testing specifications
    :return: a Board object consisting of the tiles described by the board_json
    """
    # Dict to store tile objects
    tiles = {}

    # Determine the maximum row length so that we can determine whether we need to pad certain rows with 0's
    max_row_length = max(map(lambda x: len(x), json_board))

    # Iterate through each row in the json board
    for row in range(len(json_board)):
        # Current row in the board
        current_row = json_board[row]

        # Iterate through all columns in the current row (and, if row length
        # is shorter than the maximum, iterate extra times to pad with zeros)
        for current_col in range(max_row_length):
            try:
                # The current position
                current_pos = Position(row, current_col)

                # The number of fish according to the json object
                num_fish = current_row[current_col] if current_col < len(current_row) else 0

                # Initialize a new tile/hole according to the number provided
                new_tile = Tile(num_fish) if num_fish > 0 else Hole()

                # Add the tile to the current collection of tiles
                tiles[current_pos] = new_tile
            except ValueError:
                raise ValueError("Issue initializing tile because of an invalid number of fish.")
            except TypeError:
                raise TypeError("Issue initializing tile because a non-integer value was encountered.")
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
    Execute the main program logic of xboard. Specifically, take
    in a valid board json object from STDIN and output the number of
    reachable positions from the given position.
    """
    # Initialzie input
    current_input = ""
    # Continuously read input from STDIN
    for k in sys.stdin:
        # Append the current character to the input
        current_input = current_input + k

    try:
        input_json = json.loads(current_input)
        validate_input_json(input_json)

        board = initialize_board(input_json['board'])

        # Get the number of reachable positions from the specified position in the json input
        pos = input_json['position']
        number_of_positions = len(board.get_reachable_positions(Position(pos[0], pos[1])))

        # Output number of positions to standard out
        print(number_of_positions)
    except ValueError as e1:
        print(f'ERROR: {e1}')
    except TypeError as e2:
        print(f'ERROR: {e2}')
    except json.JSONDecodeError as e3:
        print(f'ERROR: {e3}')

    # If input has ended, clear the current input to prepare for the next set of input
    current_input = ""
