import sys
import unittest


sys.path.append("../Fish/Common")
sys.path.append("../4/Other")

from board import Board
from position import Position
from tile import Tile
from xtree import _action_to_json, _get_next_state, _find_action_to_neighboring_tile, _get_next_position
from xstate import _state_to_json, initialize_state
from hole import Hole
from state import State
from color import Color
from player import Player
from action import Action
from movement_direction import MovementDirection
from exceptions.InvalidActionException import InvalidActionException
from exceptions.GameNotRunningException import GameNotRunningException


class XTreeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(XTreeTests, self).__init__(*args, **kwargs)

        Board.DISABLE_SPRITE_MANAGER = True

    def test_action_to_json_success(self):
        # Test success of action to json

        # Initialize positions for action
        pos1 = Position(0, 0)
        pos2 = Position(2, 0)

        # Initialize action
        action1 = Action(pos1, pos2)

        self.assertCountEqual(_action_to_json(action1), [[0, 0], [2, 0]])
    
    def test_action_to_json_fail(self):
        # Test failure of action_to_json due to invalid type of action
        with self.assertRaises(TypeError):
            _action_to_json("Hello")
    
    def test_get_next_state_success(self):
        # Test successful get next state
        json_obj = {
            'players': [
                {'score': 0, 'places': [[1, 0], [2, 0], [0, 0]], 'color': 'white'},
                {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'}
            ],
            'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
        }

        # Initialize state from json object
        state = initialize_state(json_obj)

        # From position and to position for a valid action 
        pos1 = Position(2, 0)
        pos2 = Position(3, 0)

        # Get next state
        next_state = _get_next_state(state, pos1, pos2)

        expected_state = {
            'players': [
                {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'},
                {'score': 4, 'places': [[1, 0], [3, 0], [0, 0]], 'color': 'white'}
            ],
            'board': [[4, 4, 4], [4, 4, 4], [0, 4, 4], [4, 4, 4]]
        }

        self.assertDictEqual(_state_to_json(next_state), expected_state)
    
    def test_get_next_state_fail1(self):
        # Test failure of get_next_state due to invalid type for state
        with self.assertRaises(TypeError):
            _get_next_state("Hello", Position(0, 1), Position(1, 2))
    
    def test_get_next_state_fail2(self):
        # Test failure of get_next_state due to invalid type for from_pos
        with self.assertRaises(TypeError):
            json_obj = {
                'players': [
                    {'score': 0, 'places': [[1, 0], [2, 0], [0, 0]], 'color': 'white'},
                    {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                    {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'}
                ],
                'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
            }

            # Initialize state from json object
            state = initialize_state(json_obj)

            _get_next_state(state, 4, Position(1, 2))
    
    def test_get_next_state_fail3(self):
        # Test failure of get_next_state due to invalid type for to_pos
        with self.assertRaises(TypeError):
            json_obj = {
                'players': [
                    {'score': 0, 'places': [[1, 0], [2, 0], [0, 0]], 'color': 'white'},
                    {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                    {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'}
                ],
                'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
            }

            # Initialize state from json object
            state = initialize_state(json_obj)

            _get_next_state(state, Position(1, 2), 4)

    def test_get_next_state_fail4(self):
        # Test failure of get_next_state due to invalid action
        with self.assertRaises(InvalidActionException):
            json_obj = {
                'players': [
                    {'score': 0, 'places': [[1, 0], [2, 0], [0, 0]], 'color': 'white'},
                    {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                    {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'}
                ],
                'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
            }

            # Initialize state from json object
            state = initialize_state(json_obj)

            # Get next state
            _get_next_state(state, Position(1, 1), Position(1, 0))
    
    def test_find_action_to_neighboring_tile_fail1(self):
        # Test failing find action to neighboring tile due to invalid state type
        with self.assertRaises(TypeError):
            _find_action_to_neighboring_tile("Hello", Position(3, 4))

    def test_find_action_to_neighboring_tile_fail2(self):
        # Test failing find action to neighboring tile due to invalid position type
        with self.assertRaises(TypeError):
            json_obj = {
                'players': [
                    {'score': 0, 'places': [[1, 0], [2, 0], [0, 0]], 'color': 'white'},
                    {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                    {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'}
                ],
                'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
            }

            # Initialize state from json object
            state = initialize_state(json_obj)

            _find_action_to_neighboring_tile(state, "Hello")


