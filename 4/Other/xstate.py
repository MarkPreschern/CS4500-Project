import sys
import json

sys.path.append("../3/Other")
sys.path.append("../Fish/Common")

from xboard import initialize_board
from player_entity import PlayerEntity
from board import Board
from movement_direction import MovementDirection
from color import Color
from action import Action
from exceptions.InvalidActionException import InvalidActionException
from exceptions.GameNotRunningException import GameNotRunningException
from game_tree import GameTree
from position import Position
from state import State

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
    for k in sys.stdin:
        input_obj += k

    # Load from read string
    json_obj = json.loads(input_obj)

    # Initialize state from json
    init_state = initialize_state(json_obj)

    # Get next state for first avatar
    state = _get_next_state(init_state)

    # If there is no next state for first avatar, print False
    if state is None:
        print(json.dumps(False))
    else:
        # Write JSON to STDOUT
        print(json.dumps(_state_to_json(state)))


def _board_to_json(board: Board) -> []:
    """
    Converts given Board object to an array, where
    each entry is an array that represents a row on the board.
    Each said array is an ordered series of numbers that represents
    the number of fish on the tiles.

    :param board: Board object to parse
    :return: resulting array
    """
    if not isinstance(board, Board):
        raise TypeError('Expected Board for board!')

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
    Produces JSON for given state.

    :param state: state to produce JSON for
    :return: resulting json dictionary
    """
    # Check params
    if not isinstance(state, State):
        raise TypeError('Expected State object or None!')

    json_obj = dict()

    json_obj['board'] = _board_to_json(state.board)
    json_obj['players'] = []

    player_order = state.player_order

    # Cycle over player order
    for player_color in player_order:
        # Initialize dictionary in which to store player data
        player_obj = {}

        # Gather player data
        player_obj['score'] = state.get_player_score(player_color)
        player_obj['places'] = [[pos.x, pos.y] for pos in state.get_player_positions(player_color)]
        player_obj['color'] = player_color.name.lower()

        # Append player object to list
        json_obj['players'].append(player_obj)

    return json_obj


def _str_to_color(color_str: str) -> Color:
    """
    Converts a string color to a Color object.

    :param color_str: string to parse
    :return: Color object
    """
    if not isinstance(color_str, str):
        raise TypeError('Expected str for color_str!')

    # Capitalize
    color_str = color_str.upper()

    # Make sure color exists
    if color_str not in Color.__dict__:
        raise ValueError('Not such color!')

    return Color[color_str]


def initialize_state(json_obj: dict) -> State:
    """
    Initializes a State object from the given json representation of a state.

    :param json_obj: json object (dictionary) containing player list and board
    :return: the state described by the json obj as a State object
    """
    if not isinstance(json_obj, dict):
        raise TypeError('Expected dict for json_obj!')

    if 'players' not in json_obj.keys():
        raise ValueError('Expected players in object!')

    if 'board' not in json_obj.keys():
        raise ValueError('Expected board in object!')

    # Retrieve player list
    player_list = json_obj['players']
    board_json = json_obj['board']

    # Get board from json
    board = initialize_board(board_json)

    # Initialize empty collection to hold players
    players = []

    # Initialize collection to hold player ids and their
    # avatar placements
    player_placements = {}

    # Cycle over each json object in the json list
    for player in player_list:
        # Make up Player object
        new_player = PlayerEntity("", _str_to_color(player['color']))

        # Update player score to whatever the current score is in the state
        new_player.score = player['score']

        # Add player object to players list
        players.append(new_player)

        # Insert placement
        player_placements.update({_str_to_color(player['color']): player['places']})

    # Make up state with board and players
    state = State(board, players)

    # Determine the maximum number of avatars for a single player
    avatars_per_player_no = max(map(lambda x: len(x), player_placements.values()))

    # For each i in the number of avatars per player
    for i in range(avatars_per_player_no):
        # For each player, place i-th avatar if possible
        for p_color, p_placements in player_placements.items():
            # Retrieve current player's i-th avatar
            try:
                placement = player_placements[p_color][i]

                # Convert to Position object
                position_to_place = Position(placement[0], placement[1])

                # Place current player's avatar at position
                state.place_avatar(p_color, position_to_place)
            except IndexError:
                continue

    return state


def _get_next_state(state: State) -> State:
    """
    Produces the subsequent game state from trying to move first player's
    first avatar in an order of directions. If said avatar cannot go
    in any of the specified directions, None is returned.

    :param state: state containing starting player list and board as extracted by initialize_state
    :return: resulting state or False.
    """
    if not isinstance(state, State):
        raise TypeError("Expected State for state.")

    # Get player's placements
    player_placements = state.placements

    first_player_color = state.players[0].color

    # Get first player's first avatar's position
    first_avatar_pos = player_placements[first_player_color][0]
    first_avatar_pos = Position(first_avatar_pos[0], first_avatar_pos[1])

    # Possible actions that can be taken from this state
    possible_actions = state.get_possible_actions()

    # Attempt to move in a number of directions
    for direction in directions_to_try:
        # first_avatar_pos
        next_pos = _get_next_position(first_avatar_pos, direction)

        try:  
            # Set current action
            action = Action(first_avatar_pos, next_pos)

            # Check if the current action is in the list of possible actions
            if action in possible_actions:
                state.move_avatar(first_avatar_pos, next_pos)

                return state
        except InvalidActionException:
            pass
        except GameNotRunningException:
            return None

    return None


def _get_next_position(position: Position, direction: MovementDirection):
    """
    Retrieves the subsequent position from the given position one step
    in the given direction.

    :param position: position to start from
    :param direction: direction to go in
    """
    # Validate params
    if not isinstance(position, Position):
        raise TypeError('Expected Position object for position!')

    if not isinstance(direction, MovementDirection):
        raise TypeError('Expected MovementDirection for direction!')

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
