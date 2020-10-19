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
                current_pos = Position(current_row, current_col)

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

        # Since we are guaranteed valid input, the input JSON value will
        # always end with a } character. At this point, we begin our
        # parsing of JSON input
        if '}' in k:            
            try:
                input_json = json.loads(current_input)
                validate_input_json(input_json)

                board = initialize_board(input_json['board'])

                # Get the number of reachable positions from the specified position in the json input
                pos = input_json['position']
                number_of_positions = len(board.get_reachable_positions((pos[0], pos[1])))

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
