import sys
import unittest

sys.path.append('../')

from state import State
from player import Player
from board import Board
from color import Color
from collections import OrderedDict
from position import Position
from action import Action

from exceptions.InvalidActionException import InvalidActionException
from exceptions.InvalidPositionException import InvalidPositionException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.UnclearPathException import UnclearPathException


class StateTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StateTests, self).__init__(*args, **kwargs)

        # Initialize some players for testing
        self.__p1 = Player(1, "John", Color.RED)
        self.__p2 = Player(2, "George", Color.WHITE)
        self.__p3 = Player(3, "Gary", Color.BLACK)
        self.__p4 = Player(4, "Jeanine", Color.BROWN)
        self.__p5 = Player(5, "Jen", Color.RED)

        # Initialize board for testing
        self.__b = Board.homogeneous(2, 7, 3)

    def init_test_fail1(self):
        # Tests constructor failing due to invalid board
        with self.assertRaises(TypeError):
            State(['hello', 'Buick'],
                  players=[
                      self.__p1,
                      self.__p2,
                      self.__p3])

    def init_test_fail2(self):
        # Tests constructor failing due to invalid player list
        with self.assertRaises(TypeError):
            State(self.__b, players={
                1: self.__p1,
                2: self.__p2,
                3: self.__p3})

    def init_test_fail3(self):
        # Test constructor failing due to player list not containing all players
        with self.assertRaises(TypeError):
            State(self.__b, players=[
                self.__p1,
                self.__p2,
                "Hello"])

    def init_test_fail4(self):
        # Test constructor failing due to number of players being smaller than the minimum
        with self.assertRaises(ValueError):
            State(self.__b, players=[self.__p2])

    def init_test_fail5(self):
        # Test constructor failing due to number of players being larger than the max
        with self.assertRaises(ValueError):
            State(self.__b, players=[
                self.__p2,
                self.__p1,
                self.__p3,
                self.__p4,
                self.__p5])

    def init_test_success1(self):
        # test a successful constructor with 3 players
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Assert the board is equal
        self.assertEqual(self.__b, state.board)

        # Assert the player dict is equal
        expected_players = OrderedDict()
        expected_players.sort(key=lambda p: p.age)

        expected_players[1] = self.__p1
        expected_players[2] = self.__p2
        expected_players[3] = self.__p3

        self.assertSequenceEqual(expected_players, state._State__players)

        self.assertEqual(state.players_no, 3)
        self.assertEqual(state.avatars_per_player, 3)

        # Assert the placements dictionary is initialized to the proper val
        self.assertEqual(state.placements, {})

    def init_test_success2(self):
        # test a successful constructor with 4 players
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Assert the board is equal
        self.assertEqual(self.__b, state.board)

        # Assert the player dict is equal
        expected_players = OrderedDict()
        expected_players.sort(key=lambda p: p.age)

        expected_players[1] = self.__p1
        expected_players[2] = self.__p2
        expected_players[3] = self.__p3
        expected_players[4] = self.__p4

        self.assertSequenceEqual(expected_players, state._State__players)

        self.assertEqual(state.players_no, 4)
        self.assertEqual(state.avatars_per_player, 2)

        # Assert the placements dictionary is initialized to the proper val
        self.assertEqual(state.placements, {})

    def test_place_avatar_fail1(self):
        # Test failure of place_avater due to invalid player id type
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar("Hello", (1, 0))

    def test_place_avatar_fail2(self):
        # Test failure of place_avatar due to avatar id < 0
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar(-1, (1, 0))

    def test_place_avatar_fail3(self):
        # Test failure of place_avatar due to there being no more
        # avatars to place
        with self.assertRaises(InvalidActionException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar(1, Position(0, 0))
            state.place_avatar(2, Position(1, 0))
            state.place_avatar(3, Position(2, 0))
            state.place_avatar(1, Position(4, 0))
            state.place_avatar(2, Position(3, 0))
            state.place_avatar(3, Position(2, 2))
            state.place_avatar(1, Position(0, 1))
            state.place_avatar(2, Position(3, 1))
            state.place_avatar(3, Position(1, 1))
            state.place_avatar(1, Position(3, 2))

    def test_place_avatar_fail4(self):
        # Test failure of place_avatar due invalid position
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar("Hello")

    def test_place_avatar_success(self):
        # Test successful placement of avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        state.place_avatar(1, Position(1, 0))

        expected = {1: [Position(1, 0)], 2: [], 3: []}

        self.assertSequenceEqual(state.placements, expected)

        # Test a second placement
        state.place_avatar(2, Position(0, 0))

        expected = {1: [Position(1, 0)], 2: [Position(0, 0)], 3: []}

        self.assertSequenceEqual(state.placements, expected)

    def test_place_avatar_repeat_position(self):
        # Test failure of place_avatar when placing on a tile that another
        # player is already on
        with self.assertRaises(InvalidPositionException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            state.place_avatar(1, Position(1, 0))

            # This should raise the exception
            state.place_avatar(2, Position(1, 0))

    def test_place_avatar_hole(self):
        # Test failure of place_avatar when placing on a hole
        with self.assertRaises(InvalidPositionException):
            new_b = Board.homogeneous(3, 3, 2)
            new_b.remove_tile(Position(0, 0))

            state = State(new_b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state.place_avatar(1, Position(0, 0))

    def test_is_position_open_fail1(self):
        # Tests is_position_open failing due to invalid position (type-wise)

        # Make up new state
        state = State(Board.homogeneous(3, 3, 2), players=[
            self.__p1,
            self.__p2,
            self.__p3])

        with self.assertRaises(TypeError):
            state.is_position_open('hello dora')

    def test_is_position_open_fail2(self):
        # Tests is_position_open failing due to invalid position (outside
        # the bounds of the board)

        # Make up new state
        state = State(Board.homogeneous(3, 3, 2), players=[
            self.__p1,
            self.__p2,
            self.__p3])

        with self.assertRaises(InvalidPositionException):
            state.is_position_open(Position(3, 1))

    def test_is_position_open_success1(self):
        # Tests a series of is_position_open calls on a hole, tile
        # and avatar

        # Make up board with a hole in it
        b = Board.homogeneous(3, 3, 2)
        b.remove_tile(Position(0, 0))

        # Make up state
        state = State(b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Place some avatars
        state.place_avatar(1, Position(1, 0))
        state.place_avatar(2, Position(1, 1))

        # Check if position is open on a hole
        self.assertFalse(state.is_position_open(Position(0, 0)))
        # Check if position is open on a avatar
        self.assertFalse(state.is_position_open(Position(1, 0)))
        self.assertFalse(state.is_position_open(Position(1, 1)))
        # Check if position is open on an open tile
        self.assertTrue(state.is_position_open(Position(2, 1)))

    def test_move_avatar_fail1(self):
        # Test failure of place_avatar due to invalid dst
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.move_avatar(Position(0, 0), -3)

    def test_move_avatar_fail2(self):
        # Test failure of move_avatar due to invalid src
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.move_avatar(-1, Position(1, 0))

    def test_is_player_stuck_fail3(self):
        # Test failure of is_player_stuck due target position
        # being the same as starting position
        with self.assertRaises(UnclearPathException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Player 1 place
            state.place_avatar(1, Position(0, 0))
            # Player 2 place
            state.place_avatar(2, Position(0, 1))
            # Player 3 place
            state.place_avatar(3, Position(2, 2))
            # Player 1 place
            state.place_avatar(1, Position(1, 0))
            # Player 2 place
            state.place_avatar(2, Position(2, 0))
            # Player 3 place
            state.place_avatar(3, Position(3, 1))
            # Player 1 place
            state.place_avatar(1, Position(1, 1))
            # Player 2 place
            state.place_avatar(2, Position(2, 1))
            # Player 3 place
            state.place_avatar(3, Position(3, 0))

            # Make sure p1 can move
            self.assertFalse(state._State__is_player_stuck(self.__p1.id))
            self.assertEqual(state.current_player, self.__p1.id)

            state.move_avatar(Position(0, 0), Position(0, 0))

    def test_move_avatar_success(self):
        # Test successful move of avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(1, Position(4, 0))
        # Player 2 place
        state.place_avatar(2, Position(0, 1))
        # Player 3 place
        state.place_avatar(3, Position(2, 2))
        # Player 1 place
        state.place_avatar(1, Position(1, 0))
        # Player 2 place
        state.place_avatar(2, Position(2, 0))
        # Player 3 place
        state.place_avatar(3, Position(3, 2))
        # Player 1 place
        state.place_avatar(1, Position(1, 1))
        # Player 2 place
        state.place_avatar(2, Position(4, 1))
        # Player 3 place
        state.place_avatar(3, Position(3, 0))

        # Test a move
        state.move_avatar(Position(1, 0), Position(0, 0))
        expected = {
                1: [Position(4, 0), Position(0, 0), Position(1, 1)],
                2: [Position(0, 1), Position(2, 0), Position(4, 1)],
                3: [Position(2, 2), Position(3, 2), Position(3, 0)]
        }

        self.assertSequenceEqual(state.placements, expected)

        # Test a second move
        state.move_avatar(Position(0, 1), Position(2, 1))
        expected = {1: [Position(4, 0), Position(0, 0), Position(1, 1)],
                    2: [Position(2, 1), Position(2, 0), Position(4, 1)],
                    3: [Position(2, 2), Position(3, 2), Position(3, 0)]
                    }

        self.assertSequenceEqual(state.placements, expected)

    def test_move_through_another_avatar(self):
        # Tests failing move due to an avatar in the way
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(1, Position(4, 0))
        # Player 2 place
        state.place_avatar(2, Position(0, 1))
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        # Player 1 place
        state.place_avatar(1, Position(1, 0))
        # Player 2 place
        state.place_avatar(2, Position(2, 0))
        # Player 3 place
        state.place_avatar(3, Position(3, 2))
        # Player 1 place
        state.place_avatar(1, Position(1, 1))
        # Player 2 place
        state.place_avatar(2, Position(4, 1))
        # Player 3 place
        state.place_avatar(3, Position(3, 0))

        with self.assertRaises(UnclearPathException):
            state.move_avatar(Position(1, 0), Position(3, 1))

    def test_move_to_another_player(self):
        # Tests failing move due to an avatar being at target
        # position
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(1, Position(4, 0))
        # Player 2 place
        state.place_avatar(2, Position(0, 1))
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        # Player 1 place
        state.place_avatar(1, Position(1, 0))
        # Player 2 place
        state.place_avatar(2, Position(2, 0))
        # Player 3 place
        state.place_avatar(3, Position(3, 2))
        # Player 1 place
        state.place_avatar(1, Position(1, 1))
        # Player 2 place
        state.place_avatar(2, Position(4, 1))
        # Player 3 place
        state.place_avatar(3, Position(3, 0))

        with self.assertRaises(UnclearPathException):
            state.move_avatar(Position(1, 0), Position(2, 1))

    def test_move_avatar_no_placement(self):
        # Test failure of move_avatar when a player tries to move
        # without an initial placement
        with self.assertRaises(InvalidActionException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state.move_avatar(Position(0, 0), Position(1, 0))

    def test_move_avatar_to_hole(self):
        # Test failure of move_avatar when a player tries to move
        # to a hole
        with self.assertRaises(UnclearPathException):
            new_b = Board.homogeneous(2, 5, 3)
            new_b.remove_tile(Position(0, 0))

            state = State(new_b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Player 1 place
            state.place_avatar(1, Position(4, 0))
            # Player 2 place
            state.place_avatar(2, Position(0, 1))
            # Player 3 place
            state.place_avatar(3, Position(2, 1))
            # Player 1 place
            state.place_avatar(1, Position(1, 0))
            # Player 2 place
            state.place_avatar(2, Position(2, 0))
            # Player 3 place
            state.place_avatar(3, Position(3, 2))
            # Player 1 place
            state.place_avatar(1, Position(1, 1))
            # Player 2 place
            state.place_avatar(2, Position(4, 1))
            # Player 3 place
            state.place_avatar(3, Position(3, 0))

            # This should raise the exception
            state.move_avatar(Position(1, 0), Position(0, 0))

    def test_move_avatar_no_straight_line(self):
        # Test failure of move avatar when a player attempts
        # to move to a tile that is not along a straight
        # path from their starting position
        with self.assertRaises(UnclearPathException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            # Player 1 place
            state.place_avatar(1, Position(1, 0))
            # Player 2 place
            state.place_avatar(2, Position(0, 1))
            # Player 3 place
            state.place_avatar(3, Position(4, 0))
            # Player 1 place
            state.place_avatar(1, Position(2, 1))
            # Player 2 place
            state.place_avatar(2, Position(2, 0))
            # Player 3 place
            state.place_avatar(3, Position(3, 2))
            # Player 1 place
            state.place_avatar(1, Position(1, 1))
            # Player 2 place
            state.place_avatar(2, Position(4, 1))
            # Player 3 place
            state.place_avatar(3, Position(3, 1))

            # This should raise the exception
            state.move_avatar(Position(1, 0), Position(4, 0))

    def test_is_player_stuck_fail1(self):
        # Tests failing is_player_stuck due to invalid
        # player_id

        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            # Player 1 place
            state.place_avatar(0, (0, 0))
            # Player 2 place
            state.place_avatar(3, (0, 1))
            # Player 3 place
            state.place_avatar(6, (2, 2))
            # Player 1 place
            state.place_avatar(1, (1, 0))
            # Player 2 place
            state.place_avatar(4, (2, 0))
            # Player 3 place
            state.place_avatar(7, (3, 1))
            # Player 1 place
            state.place_avatar(2, (1, 1))
            # Player 2 place
            state.place_avatar(5, (2, 1))
            # Player 3 place
            state.place_avatar(8, (3, 0))

            # Make sure p1 can move avatar id 0
            self.assertTrue(state._State__is_player_stuck(self.__p1.id))
            # This should raise the exception
            state._State__is_player_stuck("1")

    def test_is_player_stuck_fail2(self):
        # Tests failing is_player_stuck due to non-existent
        # player id

        with self.assertRaises(NonExistentPlayerException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state._State__is_player_stuck(231)

            self.assertNotIn(321, state.stuck_players)

    def test_is_player_stuck_success1(self):
        # Tests is_player_stuck that return true due to avatar
        # being surrounded by other avatars

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(1, Position(3, 1))
        # Place player 2's avatar
        state.place_avatar(2, Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(0, 0))
        # Place player 4's avatar
        state.place_avatar(4, Position(4, 0))

        # Place player 1's avatar
        state.place_avatar(1, Position(1, 0))
        # Place player 2's avatars
        state.place_avatar(2, Position(3, 0))
        # Place player 3's avatars
        state.place_avatar(3, Position(6, 0))
        # Place player 4's avatars
        state.place_avatar(4, Position(2, 0))

        self.assertTrue(state._State__is_player_stuck(4))
        # Make sure player id 4 is among stuck players
        self.assertIn(4, state.stuck_players)

    def test_is_player_stuck_success2(self):
        # Tests successful is_player_stuck with almost
        # completely surrounded avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatars
        state.place_avatar(1, Position(1, 0))
        # Place player 2's avatars
        state.place_avatar(2, Position(3, 0))
        # Place player 3's avatars
        state.place_avatar(3, Position(5, 2))
        # Place player 4's avatars
        state.place_avatar(4, Position(0, 0))

        # Place player 1's avatars
        state.place_avatar(1, Position(6, 1))
        # Place player 2's avatar
        state.place_avatar(2, Position(6, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(5, 0))
        # Place player 4's avatar
        state.place_avatar(4, Position(2, 0))

        self.assertFalse(state._State__is_player_stuck(4))
        self.assertNotIn(4, state.stuck_players)
        self.assertTrue(state.can_anyone_move())

    def test_is_player_stuck_success3(self):
        # Tests successful is_player_stuck where one of
        # player's avatars is completely surrounded
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(1, Position(0, 0))
        # Place player 2's avatar
        state.place_avatar(2, Position(3, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(1, 1))
        # Place player 4's avatar
        state.place_avatar(4, Position(4, 0))

        # Place player 1's avatar
        state.place_avatar(1, Position(1, 0))
        # Place player 2's avatar
        state.place_avatar(2, Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(4, 1))
        # Place player 4's avatar
        state.place_avatar(4, Position(3, 1))

        self.assertFalse(state._State__is_player_stuck(4))
        # Make sure player id 4 is NOT among stuck players
        self.assertNotIn(4, state.stuck_players)

    def test_player_order1(self):
        # Tests player order for two players
        state = State(self.__b, players=[
            self.__p2,
            self.__p1])

        self.assertSequenceEqual(state.player_order, [self.__p2.id, self.__p1.id])

    def test_player_order2(self):
        # Tests player order for four players
        state = State(self.__b, players=[
            self.__p3,
            self.__p1,
            self.__p5,
            self.__p2])

        self.assertSequenceEqual(state.player_order,
                                 [self.__p3.id, self.__p1.id, self.__p5.id, self.__p2.id])

    def test_game_started(self):
        # Test successful progress of game started field based on player placements
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements
        state.place_avatar(1, Position(0, 0))
        state.place_avatar(2, Position(1, 0))
        state.place_avatar(3, Position(0, 1))
        state.place_avatar(4, Position(1, 1))
        state.place_avatar(1, Position(2, 0))
        state.place_avatar(2, Position(2, 1))
        state.place_avatar(3, Position(3, 0))
        state.place_avatar(4, Position(3, 1))

    def test_current_player_updates(self):
        # Test the proper updates of the current_player field based
        # on valid game movements and player order
        # Test successful progress of game started field based on player placements

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements
        # Player 1 place
        state.place_avatar(1, Position(0, 0))
        # Player 2 place
        state.place_avatar(2, Position(1, 0))
        # Player 3 place
        state.place_avatar(3, Position(0, 1))
        # Player 4 place
        state.place_avatar(4, Position(1, 1))
        # Player 1 place
        state.place_avatar(1, Position(2, 0))
        # Player 2 place
        state.place_avatar(2, Position(2, 1))
        # Player 3 place
        state.place_avatar(3, Position(3, 0))
        # Player 4 place
        state.place_avatar(4, Position(3, 1))

        # Current order is p1, p2, p3, p4
        self.assertEqual(state.current_player, 1)

        # Valid move that should trigger no exceptions and cause current player to
        # increment
        state.move_avatar(Position(2, 0), Position(4, 0))

        # Play moves to p2
        self.assertNotEqual(state.current_player, 1)
        self.assertEqual(state.current_player, 2)

        # Make move for p2
        state.move_avatar(Position(2, 1), Position(4, 1))

        # Play moves to p3
        self.assertNotEqual(state.current_player, 2)
        self.assertEqual(state.current_player, 3)

        # Make move for p3
        state.move_avatar(Position(3, 0), Position(5, 0))

        # Play moves to p4
        self.assertNotEqual(state.current_player, 3)
        self.assertEqual(state.current_player, 4)

        # Make move for p4
        state.move_avatar(Position(3, 1), Position(5, 1))

        # Play moves to p1
        self.assertNotEqual(state.current_player, 4)
        self.assertEqual(state.current_player, 1)

    def test_player_skip_when_no_moves1(self):
        # Test the functionality of skipping players when they cannot make any moves
        new_b = Board.homogeneous(3, 5, 2)
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. all of player 2's avatars are
        # blocked
        state.place_avatar(1, Position(3, 0))
        state.place_avatar(2, Position(0, 0))
        state.place_avatar(3, Position(1, 0))
        state.place_avatar(4, Position(2, 0))
        state.place_avatar(1, Position(3, 1))
        state.place_avatar(2, Position(0, 1))
        state.place_avatar(3, Position(1, 1))
        state.place_avatar(4, Position(2, 1))

        # Verify that it is player 1's turn
        self.assertEqual(state.current_player, 1)
        self.assertSequenceEqual(state.player_order, [1, 2, 3, 4])

        # Move one of player 1's avatars
        state.move_avatar(Position(3, 1), Position(4, 1))

        # Verify that it is actually player 4's turn and that p2 and p3 have been skipped
        self.assertEqual(state.current_player, 4)
        self.assertSequenceEqual(state.player_order, [4, 1, 2, 3])

    def test_player_skip_when_no_moves2(self):
        # Test the functionality of skipping the first player right after
        # placement when it cannot make any moves
        new_b = Board.homogeneous(3, 5, 2)
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. all of player 2's avatars are
        # blocked
        state.place_avatar(1, Position(0, 0))
        state.place_avatar(2, Position(3, 0))
        state.place_avatar(3, Position(1, 0))
        state.place_avatar(4, Position(2, 0))
        state.place_avatar(1, Position(0, 1))
        state.place_avatar(2, Position(3, 1))
        state.place_avatar(3, Position(1, 1))
        state.place_avatar(4, Position(2, 1))

        # Verify that it is player 1's turn
        self.assertEqual(state.current_player, 2)
        self.assertSequenceEqual(state.player_order, [2, 3, 4, 1])

        # Move one of player 1's avatars
        state.move_avatar(Position(3, 1), Position(4, 1))

        # Verify that it is actually player 4's turn and that p2 and p3 have been skipped
        self.assertEqual(state.current_player, 4)
        self.assertSequenceEqual(state.player_order, [4, 1, 2, 3])

    def test_game_over1(self):
        # Test the game until the game is over

        # Setup board
        new_b = Board.homogeneous(3, 5, 2)
        # Setup state
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. only 2 moves can be made
        # Player 1
        state.place_avatar(1, Position(3, 0))
        # Player 2
        state.place_avatar(2, Position(0, 0))
        # Player 3
        state.place_avatar(3, Position(1, 0))
        # Player 4
        state.place_avatar(4, Position(2, 0))
        # Player 1
        state.place_avatar(1, Position(3, 1))
        # Player 2
        state.place_avatar(2, Position(0, 1))
        # Player 3
        state.place_avatar(3, Position(1, 1))
        # Player 4
        state.place_avatar(4, Position(2, 1))

        # Make move 1 for p1
        state.move_avatar(Position(3, 1), Position(4, 1))

        # Make sure at least one player can still move
        self.assertTrue(state.can_anyone_move())

        # Make move 2 for p4, meaning game should end because all tiles are either
        # occupied or holes
        state.move_avatar(Position(2, 0), Position(4, 0))

        # Make sure no one can move (game over)
        self.assertFalse(state.can_anyone_move())

    def test_game_over2(self):
        # Test game over from the get-go (right after placement)
        # Test the game until the game is over

        # Setup board
        new_b = Board.homogeneous(3, 4, 2)
        # Setup state
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. only 2 moves can be made
        # Player 1
        state.place_avatar(1, Position(0, 0))
        # Player 2
        state.place_avatar(2, Position(0, 1))
        # Player 3
        state.place_avatar(3, Position(1, 0))
        # Player 4
        state.place_avatar(4, Position(1, 1))
        # Player 1
        state.place_avatar(1, Position(2, 0))
        # Player 2
        state.place_avatar(2, Position(2, 1))
        # Make sure player 1 is still up
        self.assertEqual(state.player_order, [1, 2, 3, 4])
        # Player 3
        state.place_avatar(3, Position(3, 0))
        # Make sure player 1 is not longer up and 2 is up instead
        self.assertEqual(state.player_order, [2, 3, 4, 1])
        # Player 4
        state.place_avatar(4, Position(3, 1))

        # Make sure it's game over
        self.assertFalse(state.can_anyone_move())

    def test_get_possible_actions_success1(self):
        # Tests a successful get_possible_actions during placing phase

        # Setup board
        new_b = Board.homogeneous(3, 5, 2)
        # Setup state
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Since we're still in placing phase, there should be
        # no actions available
        self.assertEqual(state.get_possible_actions(), [])

    def test_get_possible_actions_success2(self):
        # Tests a successful get_possible_actions during playing phase

        # Setup board
        new_b = Board.homogeneous(3, 5, 2)
        # Setup state
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. only 2 moves can be made
        # Player 1
        state.place_avatar(1, Position(3, 0))
        # Player 2
        state.place_avatar(2, Position(0, 0))
        # Player 3
        state.place_avatar(3, Position(1, 0))
        # Player 4
        state.place_avatar(4, Position(2, 0))
        # Player 1
        state.place_avatar(1, Position(3, 1))
        # Player 2
        state.place_avatar(2, Position(0, 1))
        # Player 3
        state.place_avatar(3, Position(1, 1))
        # Player 4
        state.place_avatar(4, Position(2, 1))

        # Ascertain available actions
        self.assertCountEqual(state.get_possible_actions(), [
            Action(Position(3, 0), Position(4, 0)),
            Action(Position(3, 0), Position(4, 1)),
            Action(Position(3, 1), Position(4, 1))
        ])

        # Make move
        state.move_avatar(Position(3, 1), Position(4, 1))

        # There should only be one action remaining
        self.assertCountEqual(state.get_possible_actions(), [
            Action(Position(2, 0), Position(4, 0))
        ])

        # Make final move
        state.move_avatar(Position(2, 0), Position(4, 0))

        # There should only no actions remaining
        self.assertCountEqual(state.get_possible_actions(), [])

    def test_get_player_score_test_fail1(self):
        # Tests failing get_player_score due to player_id being invalid
        # (type-wise)

        # Setup state
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        with self.assertRaises(TypeError):
            state.get_player_score('nice try')

        with self.assertRaises(TypeError):
            state.get_player_score(-23)

    def test_get_player_score_test_fail2(self):
        # Tests failing get_player_score due to player_id not
        # existing

        # Setup state
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        with self.assertRaises(NonExistentPlayerException):
            state.get_player_score(23)

    def test_get_player_score_test_success(self):
        # Tests successful get_player_score over the course
        # of a game

        # Setup state
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Make sure everyone's score is 0
        for k in range(4):
            self.assertEqual(state.get_player_score(k + 1), 0)

        # Player 1 place
        state.place_avatar(1, Position(0, 0))
        # Player 2 place
        state.place_avatar(2, Position(0, 1))
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        # Player 4 place
        state.place_avatar(4, Position(4, 1))
        # Player 1 place
        state.place_avatar(1, Position(5, 0))
        # Player 2 place
        state.place_avatar(2, Position(4, 0))
        # Player 3 place
        state.place_avatar(3, Position(3, 0))
        # Player 4 place
        state.place_avatar(4, Position(3, 1))

        # Make sure everyone's score is still 0
        for k in range(4):
            self.assertEqual(state.get_player_score(k + 1), 0)

        # Player 1 make a move
        state.move_avatar(Position(0, 0), Position(1, 0))

        # Make sure player 1 has a score of 2 (board is homogeneous
        # with the same no. fish to each tile)
        self.assertEqual(state.get_player_score(1), 2)
        # Make sure everyone else is at 0
        self.assertEqual(state.get_player_score(2), 0)
        self.assertEqual(state.get_player_score(3), 0)
        self.assertEqual(state.get_player_score(4), 0)

        # Player 2 make a move
        state.move_avatar(Position(0, 1), Position(1, 1))

        # Make sure player 1 & 2 have a score of 2
        self.assertEqual(state.get_player_score(1), 2)
        self.assertEqual(state.get_player_score(2), 2)
        # Make sure everyone else is at 0
        self.assertEqual(state.get_player_score(3), 0)
        self.assertEqual(state.get_player_score(4), 0)

    def test_move_log_success1(self):
        # Tests move log
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(1, Position(0, 0))
        # Place player 2's avatar
        state.place_avatar(2, Position(3, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(1, 1))
        # Place player 4's avatar
        state.place_avatar(4, Position(4, 0))

        # Place player 1's avatar
        state.place_avatar(1, Position(4, 1))
        # Place player 2's avatar
        state.place_avatar(2, Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(2, 0))
        # Place player 4's avatar
        state.place_avatar(4, Position(3, 1))

        # No moves have been made yet
        self.assertEqual(state.move_log, [])

        # Make a move
        state.move_avatar(Position(0, 0), Position(2, 1))
        # Check log
        self.assertEqual(state.move_log, [Action(Position(0, 0), Position(2, 1))])

        # Make another move
        state.move_avatar(Position(5, 0), Position(6, 0))
        # Check log
        self.assertCountEqual(state.move_log, [
            Action(Position(0, 0), Position(2, 1)),
            Action(Position(5, 0), Position(6, 0))
        ])

    def test_player_order_success1(self):
        # Tests successful get player order

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(1, Position(0, 0))
        # Place player 2's avatar
        state.place_avatar(2, Position(3, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(1, 1))
        # Place player 4's avatar
        state.place_avatar(4, Position(4, 0))

        # Finish placing
        # Place player 1's avatar
        state.place_avatar(1, Position(4, 1))
        # Place player 2's avatar
        state.place_avatar(2, Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(3, Position(2, 0))
        # Place player 4's avatar
        state.place_avatar(4, Position(3, 1))

        # Make a move on behalf of player 1
        state.move_avatar(Position(0, 0), Position(2, 1))

        # Make sure player one is at the end, and player 2 is next up
        self.assertSequenceEqual(state.player_order, [2, 3, 4, 1])

        # Make another move
        state.move_avatar(Position(5, 0), Position(6, 0))

        # Make sure player two is at the end, and player 3 is next up
        self.assertSequenceEqual(state.player_order, [3, 4, 1, 2])

    def test_get_player_color_success(self):
        # Test successful get player score for all players
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        self.assertEqual(state.get_player_color(1), Color.RED)
        self.assertEqual(state.get_player_color(2), Color.WHITE)
        self.assertEqual(state.get_player_color(3), Color.BLACK)
        self.assertEqual(state.get_player_color(4), Color.BROWN)

    def test_get_player_color_fail1(self):
        # Test failure of get player color due to invalid player id type
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

            state.get_player_color("hello")
    
    def test_get_player_color_fail2(self):
        # Test failure of get player color due to invalid player id type
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

            state.get_player_color(-1)
    
    def test_get_player_color_fail3(self):
        # Test failure of get player color due to player id not being in game
        with self.assertRaises(NonExistentPlayerException):
            state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

            state.get_player_color(5)
    
    def test_get_player_positions_success(self):
        # Test successful get player positions
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(1, Position(0, 0))
        # Player 2 place
        state.place_avatar(2, Position(0, 1))
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        # Player 4 place
        state.place_avatar(4, Position(4, 1))
        # Player 1 place
        state.place_avatar(1, Position(5, 0))
        # Player 2 place
        state.place_avatar(2, Position(4, 0))
        # Player 3 place
        state.place_avatar(3, Position(3, 0))
        # Player 4 place
        state.place_avatar(4, Position(3, 1))

        # Check that player positions are correctly obtained and in the proper order
        self.assertEqual(state.get_player_positions(1), [Position(0, 0), Position(5, 0)])
        self.assertEqual(state.get_player_positions(2), [Position(0, 1), Position(4, 0)])
        self.assertEqual(state.get_player_positions(3), [Position(2, 1), Position(3, 0)])
        self.assertEqual(state.get_player_positions(4), [Position(4, 1), Position(3, 1)])

        # Move player 1 avatar
        state.move_avatar(Position(5, 0), Position(6, 1))

        self.assertEqual(state.get_player_positions(1), [Position(0, 0), Position(6, 1)])
    
    def test_get_player_positions_fail1(self):
        # Test failure of get_player_positions due to invalid player id type
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(1, Position(0, 0))
        
        with self.assertRaises(TypeError):
            state.get_player_positions(-2)
    
    def test_get_player_positions_fail2(self):
        # Test failure of get_player_positions due to invalid player id type
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(1, Position(0, 0))
        
        with self.assertRaises(TypeError):
            state.get_player_positions("hey")
    
    def test_get_player_positions_fail3(self):
        # Test failure of get_player_positions due to player not being in the game
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])
        
        with self.assertRaises(NonExistentPlayerException):
            state.get_player_positions(5)

    def test_has_everyone_placed_success1(self):
        # Tests a series of has_everyone_placed
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(1, Position(0, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 2 place
        state.place_avatar(2, Position(0, 1))
        self.assertFalse(state.has_everyone_placed())
        # Player 3 place
        state.place_avatar(3, Position(2, 1))
        self.assertFalse(state.has_everyone_placed())
        # Player 4 place
        state.place_avatar(4, Position(4, 1))
        self.assertFalse(state.has_everyone_placed())
        # Player 1 place
        state.place_avatar(1, Position(5, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 2 place
        state.place_avatar(2, Position(4, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 3 place
        state.place_avatar(3, Position(3, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 4 place
        state.place_avatar(4, Position(3, 1))
        self.assertTrue(state.has_everyone_placed())

    def test_get_player_by_id_fail1(self):
        # Tests get_player_by_id failing due to invalid player_id (type wise)
        # Tests a series of has_everyone_placed
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        with self.assertRaises(TypeError):
            state.get_player_by_id('')

    def test_get_player_by_id_fail2(self):
        # Tests get_player_by_id failing due to invalid player_id (not in the game)
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        with self.assertRaises(NonExistentPlayerException):
            state.get_player_by_id(99)

    def test_get_player_by_id_success(self):
        # Tests successful get_player_by_id
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        self.assertEqual(state.get_player_by_id(1), self.__p1)
        self.assertEqual(state.get_player_by_id(3), self.__p3)
        self.assertEqual(state.get_player_by_id(2), self.__p2)
        self.assertEqual(state.get_player_by_id(4), self.__p4)

    def test_deepcopy(self):
        # Tests successful deep copy of state
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Place a bunch of avatars
        state.place_avatar(1, Position(0, 0))
        state.place_avatar(2, Position(0, 1))
        state.place_avatar(3, Position(0, 2))
        state.place_avatar(4, Position(1, 2))
        state.place_avatar(1, Position(1, 0))
        state.place_avatar(2, Position(1, 1))
        state.place_avatar(3, Position(2, 2))
        state.place_avatar(4, Position(2, 1))

        # Make a move for p1
        state.move_avatar(Position(0, 0), Position(2, 0))

        # Make deep copy
        copied_state = state.deepcopy()

        # Make sure board was deep copied
        self.assertNotEqual(copied_state.board, state)
        # Make sure player list was deep copied
        self.assertNotEqual(copied_state._State__players, state._State__players)
        # Make sure placements are the same
        self.assertEqual(copied_state.placements, state.placements)
        # Make sure current player is the same
        self.assertEqual(copied_state.current_player, state.current_player)
        # Make sure player 1's score is the same
        self.assertEqual(copied_state.get_player_score(1), 2)
        self.assertEqual(copied_state.get_player_score(1), state.get_player_score(1))
        # Make sure other players' scores are the same
        self.assertEqual(copied_state.get_player_score(2), 0)
        self.assertEqual(copied_state.get_player_score(3), 0)
        self.assertEqual(copied_state.get_player_score(4), 0)
        # Make sure possible actions are the same
        self.assertEqual(copied_state.get_possible_actions(), state.get_possible_actions())
