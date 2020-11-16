import sys
import unittest

from strategy import Strategy

sys.path.append('Player/')
sys.path.append('../../../Common')

from player import Player
from player_entity import PlayerEntity
from board import Board
from color import Color
from position import Position
from state import State
from unittest.mock import patch


class PlayerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlayerTests, self).__init__(*args, **kwargs)

        # Initialize boards
        self.__board1 = Board.homogeneous(2, 5, 3)

        # Initialize some players for testing
        self.__p1 = PlayerEntity("John", Color.RED)
        self.__p2 = PlayerEntity("George", Color.WHITE)
        self.__p3 = PlayerEntity("Gary", Color.BLACK)

        self.__p4 = PlayerEntity("Bot X", Color.RED)
        self.__p5 = PlayerEntity("Bot Y", Color.BROWN)
        self.__p6 = PlayerEntity("Bot Z", Color.BLACK)
        self.__p7 = PlayerEntity("Bot W", Color.WHITE)

        # ========================== STATE 1 ==========================

        # Initialize a premature state
        self.__state1 = State(self.__board1, [self.__p4, self.__p5, self.__p6, self.__p7])

        # ========================== STATE 2 ==========================

        # Initialize a finalized state where at least two more rounds are possible
        self.__state2 = State(self.__board1, [self.__p1, self.__p2, self.__p3])
        # Place all avatars
        # Player 1 place
        self.__state2.place_avatar(Color.RED,  Position(4, 2))
        # Player 2 place
        self.__state2.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3 place
        self.__state2.place_avatar(Color.BLACK,  Position(2, 1))
        # Player 1 place
        self.__state2.place_avatar(Color.RED,  Position(1, 0))
        # Player 2 place
        self.__state2.place_avatar(Color.WHITE,  Position(2, 0))
        # Player 3 place
        self.__state2.place_avatar(Color.BLACK,  Position(3, 1))
        # Player 1 place
        self.__state2.place_avatar(Color.RED,  Position(1, 1))
        # Player 2 place
        self.__state2.place_avatar(Color.WHITE,  Position(4, 1))
        # Player 3 place
        self.__state2.place_avatar(Color.BLACK,  Position(3, 0))

    def test_init_fail1(self):
        # Tests init failing due to invalid color
        with self.assertRaises(TypeError):
            Player('bob', '')

    def test_init_fail2(self):
        # Tests init failing due to invalid player name
        with self.assertRaises(TypeError):
            Player(123, Color.BLACK)

    def test_init_fail3(self):
        # Tests init failing due to invalid search depth
        with self.assertRaises(TypeError):
            Player('bob', Color.BLACK, '1')

    def test_init_fail4(self):
        # Tests init failing due to invalid search depth value
        with self.assertRaises(TypeError):
            Player('bob', Color.BLACK, 0)

    def test_init_success(self):
        # Tests successful init
        p =  Player('drew', Color.BROWN)

        self.assertEqual(p.color, Color.BROWN)
        self.assertIsNone(p.state)
        self.assertEqual(p.name, 'drew')
        self.assertEqual(p.kicked_reason, '')

    def test_get_placement_fail1(self):
        # Tests get_placement that fails due to invalid state
        # Make up player
        p = Player('bob', Color.BROWN)

        with self.assertRaises(TypeError):
            p.get_placement('not a state')

    def test_get_placement_success(self):
        # Tests get_placement that succeeds
        p = Player('bob', Color.BROWN)

        # Patch Strategy.place_penguin
        with patch.object(Strategy, 'place_penguin') as mock:
            p.get_placement(self.__state1)

        # Make sure Strategy.place_penguin was called with the
        # right params
        mock.assert_called_with(Color.BROWN, self.__state1)
        # Make sure state got updated
        self.assertEqual(p.state, self.__state1)

    def test_get_action_fail1(self):
        # Tests get_action that fails due to invalid state.
        p = Player('bob', Color.BROWN)

        with self.assertRaises(TypeError):
            p.get_action('not a state')

    def test_get_action_success(self):
        # Tests get_action that succeeds
        p = Player('bob', Color.BROWN)

        # Patch Strategy.get_best_action
        with patch.object(Strategy, 'get_best_action') as mock:
            p.get_action(self.__state1)

        # Make sure Strategy.get_action was called with the
        # right params
        mock.assert_called_with(self.__state1, p._Player__search_depth)
        # Make sure state got updated
        self.assertEqual(p.state, self.__state1)

    def test_kick_player_success(self):
        # Tests successful kick player
        p = Player('bob', Color.BLACK)
        # Make up reason to kick player
        reason = 'placing outside the bounds of the board'
        # Kick player
        p.kick(reason)

        self.assertEqual(p.kicked_reason, reason)

    def test_sync_fail1(self):
        # Tests failing sync due to invalid state
        p = Player('bob', Color.BROWN)

        with self.assertRaises(TypeError):
            p.sync('invalid state')

    def test_sync_success(self):
        # Tests successful sync
        p = Player('bob', Color.BROWN)
        # Make assertion
        self.assertIsNone(p.state)
        # Sync
        p.sync(self.__state1)
        # Make assertion
        self.assertEqual(p.state, self.__state1)

    def test_game_over_fail1(self):
        # Tests game_over that fails due to invalid leaderboard
        p = Player('bob', Color.BROWN)

        with self.assertRaises(TypeError):
            p.game_over('', [], [])

    def test_game_over_fail2(self):
        # Tests game_over that fails due to invalid cheating_players
        p = Player('bob', Color.BROWN)

        with self.assertRaises(TypeError):
            p.game_over([], '', [])

    def test_game_over_fail3(self):
        # Tests game_over that fails due to invalid failing_players
        p = Player('bob', Color.BROWN)

        with self.assertRaises(TypeError):
            p.game_over([], [], '')

    def test_game_over_success(self):
        # Tests successful game_over
        p = Player('bob', Color.BROWN)

        p.game_over([], [], [])
