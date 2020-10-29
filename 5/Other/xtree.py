import sys
import json

sys.path.append("../3/Other")
sys.path.append("../4/Other")
sys.path.append("../Fish/Common")

from xboard import initialize_board
from xstate import initialize_state, _get_next_position
from player import Player
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


def xtree() -> None:
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

    # Convert from and to position to a Position object
    from_pos = Position(json_obj['from'][0], json_obj['from'][1])
    to_pos = Position(json_obj['to'][0], json_obj['to'][1])

    # Initialize State object from json representation of state
    init_state = initialize_state(json_obj['state'])

    # Get the state after player 1 takes their first action
    state = _get_next_state(init_state, from_pos, to_pos)

    # Find an action Player 2 can take to reach a neighboring tile from player 1
    action = _find_action_to_neighboring_tile(state, to_pos)

    # If there is no next state for first avatar, print False
    if action is None:
        print(json.dumps(False))
    else:
        # Write JSON to STDOUT
        print(json.dumps(_action_to_json(action)))


def _action_to_json(action: Action) -> list:
    """
    Convert an Action to its valid JSON representation.
    An action in JSON is a list consisting of two positions, where a position
    is a list containing two integers (represents a row/column location).

    i.e. an Action is a [Position, Position] or False
    a Position is a [Integer, Integer]

    :param action: The action that will be converted to JSON
    :return: a list containing two JSON positions (note that Actions that are "false" are handled outside this function)
    """
    if not isinstance(action, Action):
        raise TypeError("Expected an Action for action.")

    # Extract positions from action
    from_pos = action[0]
    to_pos = action[1]

    # Return a list containing the two JSON representations of positions
    return [[from_pos[0], from_pos[1]], [to_pos[0], to_pos[1]]]


def _get_next_state(state: State, from_pos: Position, to_pos: Position) -> State:
    """
    Produces the subsequent game state from trying to move the first player's avatars
    from the given start position to the given end position. If the given action is illegal,
    an exception will be thrown. If the game has not been started fully yet, None will be returned.

    :param state: state containing starting player list and board as extracted by initialize_state
    :param from_pos: the starting position for the first player's desired action
    :param to_pos: the ending position for the first player's desired action
    :return: resulting state from executing Action(from_pos, to_pos)
    """
    if not isinstance(state, State):
        raise TypeError("Expected State for state.")
    if not isinstance(from_pos, Position):
        raise TypeError("Expected Position for from_pos.")
    if not isinstance(to_pos, Position):
        raise TypeError("Expected Position for to_pos.")

    # Initialize player placements
    player_placements = state.placements

    # Verify that from_pos is one of player 1's current positions
    if from_pos not in player_placements[1]:
        raise InvalidActionException("Expected from_pos to be one of player 1's current placements")

    # Attempt action
    try:
        new_state = GameTree.try_action(GameTree(state), Action(from_pos, to_pos))
        return new_state
    except InvalidActionException as e:
        raise e
    except GameNotRunningException:
        pass

    return None


def _find_action_to_neighboring_tile(state: State, to_pos: Position) -> Action:
    """
    Finds the action the second player can take to move to one of the tiles
    that neighbors the first player's ending position if it exists.  
    Otherwise, None is returned. 
    
    Actions will be searched for by checking neighboring
    tiles in the following order: North, Northeast, Southeast, South, Southwest, Northwest.
    
    If there are multiple avatars that can reach neighboring tiles, a tie breaking algorithm
    will choose the action with the top-most row of the from position, the left-most column
    of the from position, the top-most row of the to position, and the left-most column
    of the to position in that order.

    :param state: the current state resulting from the first player successfully executing their desired action
    :param to_pos: the position of the tile that the first player landed on after executing their action
    :return: an Action the second player can take to get to a neighboring tile or None if no such action exists
    """
    if not isinstance(state, State):
        raise TypeError("Expected State for state.")
    if not isinstance(to_pos, Position):
        raise TypeError("Expected Position for to_pos.")
    
    # Get player placements from state
    player_placements = state.placements 

    # Search each direction and see if any of player 2's positions can reach a neighboring tile
    # in that direction
    for direction in directions_to_try:
        # The new target position for player 2 in the current direction
        new_pos = _get_next_position(to_pos, direction)

        # List to store the potential valid actions to reach the neighboring tile in the current direction
        valid_actions = []

        for pos in player_placements[2]:
            try:
                # The action to be tried
                new_action = Action(pos, new_pos)

                # Try the action
                gt = GameTree(state)
                gt.try_action(new_action)
                
                # If this point is reached with no exception, it is a valid action.
                valid_actions.append(new_action)
            except InvalidActionException:
                pass
            except GameNotRunningException:
                return None
        
        # If any valid actions were found, either return one of them or tiebreak
        if len(valid_actions) > 0:
            return min(valid_actions)
    
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
