import sys
import unittest


sys.path.append("../Fish/Common")

from board import Board
from position import Position
from tile import Tile
from xstate import _board_to_json, _state_to_json, _str_to_color, _get_next_position, _get_next_state, initialize_state
from hole import Hole
from state import State
from color import Color
from player import Player
from movement_direction import MovementDirection


class XStateTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(XStateTests, self).__init__(*args, **kwargs)

        Board.DISABLE_SPRITE_MANAGER = True

    def test_board_to_json_fail1(self):
        # Fails due to invalid board

        with self.assertRaises(TypeError):
            _board_to_json('')

    def test_board_to_json_success1(self):
        # Tests successful board to json
        b = Board.homogeneous(2, 4, 2)

        self.assertSequenceEqual(_board_to_json(b),
                                 [[2, 2], [2, 2], [2, 2], [2, 2]])

    def test_board_to_json_success2(self):
        # Tests successful board to json
        b = Board({
            Position(0, 0): Tile(5),
            Position(0, 1): Tile(3),
            Position(0, 2): Tile(2),
            Position(1, 0): Hole(),
            Position(1, 1): Hole(),
            Position(1, 2): Tile(2),
            Position(2, 0): Tile(3),
            Position(2, 1): Tile(4),
            Position(2, 2): Hole(),
            Position(3, 0): Hole(),
            Position(3, 1): Tile(1),
            Position(3, 2): Tile(5)
        })

        self.assertSequenceEqual(_board_to_json(b),
                                 [[5, 3, 2], [0, 0, 2], [3, 4, 0], [0, 1, 5]])

    def test_state_to_json_fail1(self):
        # Fails due to state provided not being State
        with self.assertRaises(TypeError):
            _state_to_json('blah')

    def test_state_to_json_success1(self):
        # Successful state to json. State is one in which
        # all avatars have been placed
        state = State(Board.homogeneous(4, 4, 3), [
            Player(1, 'bob', Color.WHITE),
            Player(2, 'bob', Color.BROWN),
            Player(3, 'bob', Color.BLACK)
        ])

        # Player 1 place
        state.place_avatar(1, Position(0, 1))
        # Player 2 place
        state.place_avatar(2, Position(1, 0))
        # Player 3 place
        state.place_avatar(3, Position(1, 1))
        # Player 1 place
        state.place_avatar(1, Position(1, 2))
        # Player 2 place
        state.place_avatar(2, Position(2, 0))
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        # Player 1 place
        state.place_avatar(1, Position(2, 2))
        # Player 2 place
        state.place_avatar(2, Position(3, 1))
        # Player 3 place
        state.place_avatar(3, Position(3, 2))

        # Get jsonified version
        result = _state_to_json(state)

        # Make up expected json
        expected_json = {
            'players': [
                {'score': 0, 'places': [[0, 1], [1, 2], [2, 2]], 'color': 'white'},
                {'score': 0, 'places': [[1, 0], [2, 0], [3, 1]], 'color': 'brown'},
                {'score': 0, 'places': [[1, 1], [2, 1], [3, 2]], 'color': 'black'}
            ],
            'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
        }

        self.assertDictEqual(result, expected_json)

    def test_state_to_json_success2(self):
        # Successful state to json. State is one in which
        # only some avatars have been placed
        state = State(Board.homogeneous(4, 4, 3), [
            Player(1, 'bob', Color.WHITE),
            Player(2, 'bob', Color.BROWN),
            Player(3, 'bob', Color.BLACK)
        ])

        # Player 1 place
        state.place_avatar(1, Position(0, 1))
        # Player 2 place
        state.place_avatar(2, Position(1, 0))
        # Player 3 place
        state.place_avatar(3, Position(1, 1))
        # Player 1 place
        state.place_avatar(1, Position(1, 2))
        # Player 2 place
        state.place_avatar(2, Position(2, 0))
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        # Player 1 place
        state.place_avatar(1, Position(2, 2))

        # Get jsonified version
        result = _state_to_json(state)

        # Make up expected json
        expected_json = {
            'players': [
                {'score': 0, 'places': [[0, 1], [1, 2], [2, 2]], 'color': 'white'},
                {'score': 0, 'places': [[1, 0], [2, 0]], 'color': 'brown'},
                {'score': 0, 'places': [[1, 1], [2, 1]], 'color': 'black'}
            ],
            'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
        }

        self.assertDictEqual(result, expected_json)

    def test_state_to_json_success3(self):
        # Successful state to json. State is one in which
        # no avatars have been placed
        state = State(Board.homogeneous(4, 4, 3), [
            Player(1, 'bob', Color.WHITE),
            Player(2, 'bob', Color.BROWN),
            Player(3, 'bob', Color.BLACK)
        ])

        # Get jsonified version
        result = _state_to_json(state)

        # Make up expected json
        expected_json = {
            'players': [
                {'score': 0, 'places': [], 'color': 'white'},
                {'score': 0, 'places': [], 'color': 'brown'},
                {'score': 0, 'places': [], 'color': 'black'}
            ],
            'board': [[4, 4, 4], [4, 4, 4], [4, 4, 4], [4, 4, 4]]
        }

        self.assertDictEqual(result, expected_json)

    def test_str_to_color_fail1(self):
        # Fails due to invalid color_str
        with self.assertRaises(TypeError):
            _str_to_color(214)

    def test_str_to_color_fail2(self):
        # Fails due to color not existing
        with self.assertRaises(ValueError):
            _str_to_color("gray")

    def test_str_to_color_success(self):
        # Tests a series of successful color
        # conversions

        self.assertEqual(_str_to_color("red"), Color.RED)
        self.assertEqual(_str_to_color("white"), Color.WHITE)
        self.assertEqual(_str_to_color("brown"), Color.BROWN)
        self.assertEqual(_str_to_color("black"), Color.BLACK)

    def test_get_next_position_fail1(self):
        # Fails due to position being invalid
        with self.assertRaises(TypeError):
            _get_next_position('bla', MovementDirection.Top)

    def test_get_next_position_fail2(self):
        # Fails due to movement direction being invalid
        with self.assertRaises(TypeError):
            _get_next_position(Position(0, 0), 'bla')

    def test_get_next_position_fail3(self):
        # Fails due to both invalid being invalid
        with self.assertRaises(TypeError):
            _get_next_position('suh', 'bla')

    def test_get_next_position_success1(self):
        # Tests a series of successful _get_next_position

        self.assertEqual(_get_next_position(Position(0, 0), MovementDirection.BottomRight),
                         Position(1, 0))
        self.assertEqual(_get_next_position(Position(0, 0), MovementDirection.TopLeft),
                         Position(-1, -1))
        self.assertEqual(_get_next_position(Position(0, 0), MovementDirection.Bottom),
                         Position(2, 0))
        self.assertEqual(_get_next_position(Position(4, 2), MovementDirection.Top),
                         Position(2, 2))
        self.assertEqual(_get_next_position(Position(4, 2), MovementDirection.TopLeft),
                         Position(3, 1))
        self.assertEqual(_get_next_position(Position(4, 2), MovementDirection.BottomLeft),
                         Position(5, 1))
        self.assertEqual(_get_next_position(Position(4, 2), MovementDirection.TopRight),
                         Position(3, 2))

    def testinitialize_state_fail1(self):
        # Fails due to json_obj being invalid
        with self.assertRaises(TypeError):
            initialize_state('')

    def testinitialize_state_fail2(self):
        # Fails due to json_obj not containing players
        with self.assertRaises(ValueError):
            initialize_state({'board': []})

    def testinitialize_state_fail3(self):
        # Fails due to json_obj not containing board
        with self.assertRaises(ValueError):
            initialize_state({'players': []})
    
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

        # Expected state after getting next state
        expected_state = {
            'players': [
                {'score': 0, 'places': [[1, 1], [2, 1], [3, 1]], 'color': 'black'},
                {'score': 0, 'places': [[0, 1], [1, 2], [3, 2]], 'color': 'brown'},
                {'score': 4, 'places': [[3, 0], [2, 0], [0, 0]], 'color': 'white'}
            ],
            'board': [[4, 4, 4], [0, 4, 4], [4, 4, 4], [4, 4, 4]]
        }

        # Get next state
        next_state = _get_next_state(state)
        
        # Make sure json representations of the states are as expected
        self.assertDictEqual(expected_state, _state_to_json(next_state))
