import sys
import json

from action import Action
from exceptions.InvalidActionException import InvalidActionException
from game_tree import GameTree
from position import Position
from state import State

sys.path.append("../3/Other")
sys.path.append("../Fish/Common")

from xboard import initialize_board
from player import Player
from board import Board
from movement_direction import MovementDirection
from color import Color

directions_to_try = [MovementDirection.Top, MovementDirection.TopRight, MovementDirection.BottomRight,
                     MovementDirection.Bottom, MovementDirection.BottomLeft, MovementDirection.TopLeft]


def xstate() -> None:
    """
    Reads in a game state from STDIN and writes the next game state to STDOUT.
    The next game state is the one resulting from the first player's first penguin moving
    in the first permissible direction. If said penguin cannot move in any direction then
    False is written to STDOUT instead.
    """

    # Initialize objects to read to
    input_obj = ""

    # Read from STDIN indefinitely until stream is closed
    #for k in sys.stdin:
    #    input_obj += k

    fh = open('Tests/1-in.json', 'r')

    # Load from read string
    json_obj = json.load(fh)

    # Get state from json
    state = _get_next_state(json_obj['players'], json_obj['board'])

    # Write JSON to STDOUT
    print(_state_to_json(state))


def _board_to_json(board: Board) -> []:
    """
    Converts given Board object to an array, where
    each entry is an array that represents a row on the board.
    Each said array is an ordered series of numbers that represents
    the number of fish on the tiles.

    :param board: Board object to parse
    :return: resulting array
    """
    # Create two dimensional matrix as a place holder with the
    # right dimensions
    matrix = []

    # Create place holders in matrix
    for i in range(board.rows):
        matrix.append([])
        for j in range(board.cols):
            matrix[i].append(0)

    # Cycle over tiles and set items in matrix
    for pos, tile in board.tiles.items():
        matrix[pos[0]][pos[1]] = tile.fish_no

    return matrix


def _state_to_json(state: State) -> dict:
    """
    Produces JSON for given state or False if
    state is None.

    :param state: state to produce JSON for
    :return: resulting json dictionary
    """
    # Return JSON "False" if state is None
    if state is None:
        return json.dumps(False)

    json_obj = dict()

    json_obj['board'] = _board_to_json(state.board)
    json_obj['players'] = []

    player_order = state.get_player_order()

    # Cycle over player order
    for player_id in player_order:
        # Initialize dictionary in which to store player data
        player_obj = {}

        # Gather player data
        player_obj['score'] = state.get_player_score(player_id)
        player_obj['places'] = [[pos.x, pos.y] for pos in state.get_player_positions(player_id)]
        player_obj['color'] = state.get_player_color(player_id).name.lower()

        # Append player object to list
        json_obj['players'].append(player_obj)

    return json.dumps(json_obj)


def _str_to_color(color_str: str) -> Color:
    """
    Converts a string color to a Color object.

    :param color_str: string to parse
    :return: Color object
    """
    return Color[color_str.upper()]


def _get_next_state(player_list_json: dict, board_json: dict) -> State:
    """
    Produces the subsequent game state from trying to move first player's
    first avatar in an order of directions. If said avatar cannot go
    in any of the specified directions, None is returned.

    :param player_list_json: a dict containing a list of players
                             including their color, places and score
    :param board_json:       board json
    :return: resulting state or False.
    """
    # Get board from json
    board = initialize_board(board_json)

    # Initialize counter to generate player ids
    player_id_counter = 1

    # Initialize empty collection to hold players
    players = []

    # Initialize collection to hold player ids and their
    # avatar placements
    player_placements = {}

    # Cycle over each json object in the json list
    for player in player_list_json:
        # Make up Player object
        players.append(Player(player_id_counter, "", player_id_counter,
                              _str_to_color(player['color'])))
        # Insert placement
        player_placements.update({player_id_counter: player['places']})
        # Increment id counter
        player_id_counter += 1

    # Make up state with board and players
    state = State(board, players)

    # Get first player's first avatar's position
    first_avatar_pos = player_placements[1][0]
    first_avatar_pos = Position(first_avatar_pos[0], first_avatar_pos[1])

    # Determine the number of avatars per player
    avatars_per_player_no = len(player_placements[1])

    # For each i in the number of avatars per player
    for i in range(avatars_per_player_no):
        # For each player, place i-th avatar
        for p_id, p_placements in player_placements.items():
            # Retrieve current player's i-th avatar
            placement = player_placements[p_id][i]
            # Convert to Position object
            position_to_place = Position(placement[0], placement[1])

            # Place current player's avatar at position
            state.place_avatar(position_to_place)

    # Attempt to move in a number of directions
    for direction in directions_to_try:
        # first_avatar_pos
        next_pos = _get_next_position(first_avatar_pos, direction)

        try:
            # Try action on game state
            new_state = GameTree.try_action(state, Action(first_avatar_pos, next_pos))
            return new_state
        except InvalidActionException:
            pass

    return None


def _get_next_position(position: Position, direction: MovementDirection):
    """
    Retrieves the subsequent position from the given position one step
    in the given direction.

    :param position: position to start from
    :param direction: direction to go in
    """
    if direction == MovementDirection.Top:
        next_position = Position(position.x - 2, position.y)
    elif direction == MovementDirection.Bottom:
        next_position = Position(position.x + 2, position.y)
    elif direction == MovementDirection.TopLeft:
        next_y = (position.y - 1) if position.x % 2 == 0 else position.y
        next_position = Position(position.x - 1, next_y)
    elif direction == MovementDirection.TopRight:
        next_y = position.y if position.x % 2 == 0 else position.y + 1
        next_position = Position(position.x - 1, next_y)
    elif direction == MovementDirection.BottomRight:
        next_y = position.y if position.x % 2 == 0 else position.y + 1
        next_position = Position(position.x + 1, next_y)
    elif direction == MovementDirection.BottomLeft:
        next_y = (position.y - 1) if position.x % 2 == 0 else position.y
        next_position = Position(position.x + 1, next_y)
    else:
        next_position = -1

    return next_position
