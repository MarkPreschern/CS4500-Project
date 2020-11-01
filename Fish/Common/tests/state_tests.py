import sys
import unittest

sys.path.append('../')

from state import State
from player_entity import PlayerEntity
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
        self.__p1 = PlayerEntity("John", Color.RED)
        self.__p2 = PlayerEntity("George", Color.WHITE)
        self.__p3 = PlayerEntity("Gary", Color.BLACK)
        self.__p4 = PlayerEntity("Jeanine", Color.BROWN)
        self.__p5 = PlayerEntity("Jen", Color.BROWN)

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

            state.place_avatar(Color.RED,  Position(0, 0))
            state.place_avatar(Color.WHITE,  Position(1, 0))
            state.place_avatar(Color.BLACK,  Position(2, 0))
            state.place_avatar(Color.RED,  Position(4, 0))
            state.place_avatar(Color.WHITE,  Position(3, 0))
            state.place_avatar(Color.BLACK,  Position(2, 2))
            state.place_avatar(Color.RED,  Position(0, 1))
            state.place_avatar(Color.WHITE,  Position(3, 1))
            state.place_avatar(Color.BLACK,  Position(1, 1))
            state.place_avatar(Color.RED,  Position(3, 2))

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

        state.place_avatar(Color.RED,  Position(1, 0))

        expected = {Color.RED: [Position(1, 0)], Color.WHITE: [], Color.BLACK: []}

        self.assertSequenceEqual(state.placements, expected)

        # Test a second placement
        state.place_avatar(Color.WHITE,  Position(0, 0))

        expected = {Color.RED: [Position(1, 0)], Color.WHITE: [Position(0, 0)], Color.BLACK: []}

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
            state.place_avatar(Color.RED,  Position(1, 0))

            # This should raise the exception
            state.place_avatar(Color.WHITE,  Position(1, 0))

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
            state.place_avatar(Color.RED,  Position(0, 0))

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
        state.place_avatar(Color.RED,  Position(1, 0))
        state.place_avatar(Color.WHITE,  Position(1, 1))

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
            state.place_avatar(Color.RED,  Position(0, 0))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(0, 1))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(2, 2))
            # Player 1 place
            state.place_avatar(Color.RED,  Position(1, 0))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(2, 0))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(3, 1))
            # Player 1 place
            state.place_avatar(Color.RED,  Position(1, 1))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(2, 1))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(3, 0))

            # Make sure p1 can move
            self.assertFalse(state._State__is_player_stuck(self.__p1.color))
            self.assertEqual(state.current_player, self.__p1.color)

            state.move_avatar(Position(0, 0), Position(0, 0))

    def test_move_avatar_success(self):
        # Test successful move of avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(Color.RED,  Position(4, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(2, 2))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(1, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(2, 0))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 2))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(1, 1))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(4, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))

        # Test a move
        state.move_avatar(Position(1, 0), Position(0, 0))
        expected = {
                Color.RED: [Position(4, 0), Position(0, 0), Position(1, 1)],
                Color.WHITE: [Position(0, 1), Position(2, 0), Position(4, 1)],
                Color.BLACK: [Position(2, 2), Position(3, 2), Position(3, 0)]
        }

        self.assertSequenceEqual(state.placements, expected)

        # Test a second move
        state.move_avatar(Position(0, 1), Position(2, 1))
        expected = {Color.RED: [Position(4, 0), Position(0, 0), Position(1, 1)],
                    Color.WHITE: [Position(2, 1), Position(2, 0), Position(4, 1)],
                    Color.BLACK: [Position(2, 2), Position(3, 2), Position(3, 0)]
                    }

        self.assertSequenceEqual(state.placements, expected)

    def test_move_through_another_avatar(self):
        # Tests failing move due to an avatar in the way
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(Color.RED,  Position(4, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(2, 1))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(1, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(2, 0))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 2))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(1, 1))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(4, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))

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
        state.place_avatar(Color.RED,  Position(4, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(2, 1))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(1, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(2, 0))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 2))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(1, 1))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(4, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))

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
            state.place_avatar(Color.RED,  Position(4, 0))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(0, 1))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(2, 1))
            # Player 1 place
            state.place_avatar(Color.RED,  Position(1, 0))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(2, 0))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(3, 2))
            # Player 1 place
            state.place_avatar(Color.RED,  Position(1, 1))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(4, 1))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(3, 0))

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
            state.place_avatar(Color.RED,  Position(1, 0))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(0, 1))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(4, 0))
            # Player 1 place
            state.place_avatar(Color.RED,  Position(2, 1))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(2, 0))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(3, 2))
            # Player 1 place
            state.place_avatar(Color.RED,  Position(1, 1))
            # Player 2 place
            state.place_avatar(Color.WHITE,  Position(4, 1))
            # Player 3 place
            state.place_avatar(Color.BLACK,  Position(3, 1))

            # This should raise the exception
            state.move_avatar(Position(1, 0), Position(4, 0))

    def test_is_player_stuck_fail1(self):
        # Tests failing is_player_stuck due to invalid
        # player_color

        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            # Player 1 place
            state.place_avatar(0, (0, 0))
            # Player 2 place
            state.place_avatar(Color.BLACK,  (0, 1))
            # Player 3 place
            state.place_avatar(6, (2, 2))
            # Player 1 place
            state.place_avatar(Color.RED,  (1, 0))
            # Player 2 place
            state.place_avatar(Color.BROWN,  (2, 0))
            # Player 3 place
            state.place_avatar(7, (3, 1))
            # Player 1 place
            state.place_avatar(Color.WHITE,  (1, 1))
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
        # player color

        with self.assertRaises(NonExistentPlayerException):
            state = State(self.__b, players=[
                self.__p4,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state._State__is_player_stuck(Color.RED)

            self.assertNotIn(Color.RED, state.stuck_players)

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
        state.place_avatar(Color.RED,  Position(3, 1))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(0, 0))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(4, 0))

        # Place player 1's avatar
        state.place_avatar(Color.RED,  Position(1, 0))
        # Place player 2's avatars
        state.place_avatar(Color.WHITE,  Position(3, 0))
        # Place player 3's avatars
        state.place_avatar(Color.BLACK,  Position(6, 0))
        # Place player 4's avatars
        state.place_avatar(Color.BROWN,  Position(2, 0))

        self.assertTrue(state._State__is_player_stuck(Color.BROWN))
        # Make sure player id 4 is among stuck players
        self.assertIn(Color.BROWN, state.stuck_players)

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
        state.place_avatar(Color.RED,  Position(1, 0))
        # Place player 2's avatars
        state.place_avatar(Color.WHITE,  Position(3, 0))
        # Place player 3's avatars
        state.place_avatar(Color.BLACK,  Position(5, 2))
        # Place player 4's avatars
        state.place_avatar(Color.BROWN,  Position(0, 0))

        # Place player 1's avatars
        state.place_avatar(Color.RED,  Position(6, 1))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(6, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(5, 0))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(2, 0))

        self.assertFalse(state._State__is_player_stuck(Color.BROWN))
        self.assertNotIn(Color.BROWN, state.stuck_players)
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
        state.place_avatar(Color.RED,  Position(0, 0))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(3, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(1, 1))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(4, 0))

        # Place player 1's avatar
        state.place_avatar(Color.RED,  Position(1, 0))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(4, 1))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(3, 1))

        self.assertFalse(state._State__is_player_stuck(Color.BROWN))
        # Make sure player id 4 is NOT among stuck players
        self.assertNotIn(Color.BROWN, state.stuck_players)

    def test_player_order1(self):
        # Tests player order for two players
        state = State(self.__b, players=[
            self.__p2,
            self.__p1])

        self.assertSequenceEqual(state.player_order, [self.__p2.color, self.__p1.color])

    def test_player_order2(self):
        # Tests player order for four players
        state = State(self.__b, players=[
            self.__p3,
            self.__p1,
            self.__p5,
            self.__p2])

        self.assertSequenceEqual(state.player_order,
                                 [self.__p3.color, self.__p1.color, self.__p5.color, self.__p2.color])

    def test_game_started(self):
        # Test successful progress of game started field based on player placements
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements
        state.place_avatar(Color.RED,  Position(0, 0))
        state.place_avatar(Color.WHITE,  Position(1, 0))
        state.place_avatar(Color.BLACK,  Position(0, 1))
        state.place_avatar(Color.BROWN,  Position(1, 1))
        state.place_avatar(Color.RED,  Position(2, 0))
        state.place_avatar(Color.WHITE,  Position(2, 1))
        state.place_avatar(Color.BLACK,  Position(3, 0))
        state.place_avatar(Color.BROWN,  Position(3, 1))

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
        state.place_avatar(Color.RED,  Position(0, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(1, 0))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(0, 1))
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(1, 1))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(2, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(2, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(3, 1))

        # Current order is p1, p2, p3, p4
        self.assertEqual(state.current_player, Color.RED)

        # Valid move that should trigger no exceptions and cause current player to
        # increment
        state.move_avatar(Position(2, 0), Position(4, 0))

        # Play moves to p2
        self.assertNotEqual(state.current_player, Color.RED)
        self.assertEqual(state.current_player, Color.WHITE)

        # Make move for p2
        state.move_avatar(Position(2, 1), Position(4, 1))

        # Play moves to p3
        self.assertNotEqual(state.current_player, Color.WHITE)
        self.assertEqual(state.current_player, Color.BLACK)

        # Make move for p3
        state.move_avatar(Position(3, 0), Position(5, 0))

        # Play moves to p4
        self.assertNotEqual(state.current_player, Color.BLACK)
        self.assertEqual(state.current_player, Color.BROWN)

        # Make move for p4
        state.move_avatar(Position(3, 1), Position(5, 1))

        # Play moves to p1
        self.assertNotEqual(state.current_player, Color.BROWN)
        self.assertEqual(state.current_player, Color.RED)

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
        state.place_avatar(Color.RED,  Position(3, 0))
        state.place_avatar(Color.WHITE,  Position(0, 0))
        state.place_avatar(Color.BLACK,  Position(1, 0))
        state.place_avatar(Color.BROWN,  Position(2, 0))
        state.place_avatar(Color.RED,  Position(3, 1))
        state.place_avatar(Color.WHITE,  Position(0, 1))
        state.place_avatar(Color.BLACK,  Position(1, 1))
        state.place_avatar(Color.BROWN,  Position(2, 1))

        # Verify that it is player 1's turn
        self.assertEqual(state.current_player, Color.RED)
        self.assertSequenceEqual(state.player_order, [Color.RED, Color.WHITE, Color.BLACK, Color.BROWN])

        # Move one of player 1's avatars
        state.move_avatar(Position(3, 1), Position(4, 1))

        # Verify that it is actually player 4's turn and that p2 and p3 have been skipped
        self.assertEqual(state.current_player, Color.BROWN)
        self.assertSequenceEqual(state.player_order, [Color.BROWN, Color.RED, Color.WHITE, Color.BLACK])

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
        state.place_avatar(Color.RED,  Position(0, 0))
        state.place_avatar(Color.WHITE,  Position(3, 0))
        state.place_avatar(Color.BLACK,  Position(1, 0))
        state.place_avatar(Color.BROWN,  Position(2, 0))
        state.place_avatar(Color.RED,  Position(0, 1))
        state.place_avatar(Color.WHITE,  Position(3, 1))
        state.place_avatar(Color.BLACK,  Position(1, 1))
        state.place_avatar(Color.BROWN,  Position(2, 1))

        # Verify that it is player 1's turn
        self.assertEqual(state.current_player, Color.WHITE)
        self.assertSequenceEqual(state.player_order, [Color.WHITE, Color.BLACK, Color.BROWN, Color.RED])

        # Move one of player 1's avatars
        state.move_avatar(Position(3, 1), Position(4, 1))

        # Verify that it is actually player 4's turn and that p2 and p3 have been skipped
        self.assertEqual(state.current_player, Color.BROWN)
        self.assertSequenceEqual(state.player_order, [Color.BROWN, Color.RED, Color.WHITE, Color.BLACK])

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
        state.place_avatar(Color.RED,  Position(3, 0))
        # Player 2
        state.place_avatar(Color.WHITE,  Position(0, 0))
        # Player 3
        state.place_avatar(Color.BLACK,  Position(1, 0))
        # Player 4
        state.place_avatar(Color.BROWN,  Position(2, 0))
        # Player 1
        state.place_avatar(Color.RED,  Position(3, 1))
        # Player 2
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3
        state.place_avatar(Color.BLACK,  Position(1, 1))
        # Player 4
        state.place_avatar(Color.BROWN,  Position(2, 1))

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
        state.place_avatar(Color.RED,  Position(0, 0))
        # Player 2
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3
        state.place_avatar(Color.BLACK,  Position(1, 0))
        # Player 4
        state.place_avatar(Color.BROWN,  Position(1, 1))
        # Player 1
        state.place_avatar(Color.RED,  Position(2, 0))
        # Player 2
        state.place_avatar(Color.WHITE,  Position(2, 1))
        # Make sure player 1 is still up
        self.assertEqual(state.player_order, [Color.RED, Color.WHITE, Color.BLACK, Color.BROWN])
        # Player 3
        state.place_avatar(Color.BLACK,  Position(3, 0))
        # Make sure player 1 is not longer up and 2 is up instead
        self.assertEqual(state.player_order, [Color.WHITE, Color.BLACK, Color.BROWN, Color.RED])
        # Player 4
        state.place_avatar(Color.BROWN,  Position(3, 1))

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
        state.place_avatar(Color.RED,  Position(3, 0))
        # Player 2
        state.place_avatar(Color.WHITE,  Position(0, 0))
        # Player 3
        state.place_avatar(Color.BLACK,  Position(1, 0))
        # Player 4
        state.place_avatar(Color.BROWN,  Position(2, 0))
        # Player 1
        state.place_avatar(Color.RED,  Position(3, 1))
        # Player 2
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3
        state.place_avatar(Color.BLACK,  Position(1, 1))
        # Player 4
        state.place_avatar(Color.BROWN,  Position(2, 1))

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
        # Tests failing get_player_score due to player_color being invalid
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
        # Tests failing get_player_score due to player_color not
        # existing

        # Setup state
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            ])

        with self.assertRaises(NonExistentPlayerException):
            state.get_player_score(Color.BROWN)

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
        for k in [Color.RED, Color.WHITE, Color.BROWN, Color.BLACK]:
            self.assertEqual(state.get_player_score(k), 0)

        # Player 1 place
        state.place_avatar(Color.RED,  Position(0, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(2, 1))
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(4, 1))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(5, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(4, 0))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(3, 1))

        # Make sure everyone's score is still 0
        for k in [Color.RED, Color.WHITE, Color.BLACK, Color.BROWN]:
            self.assertEqual(state.get_player_score(k), 0)

        # Player 1 make a move
        state.move_avatar(Position(0, 0), Position(1, 0))

        # Make sure player 1 has a score of 2 (board is homogeneous
        # with the same no. fish to each tile)
        self.assertEqual(state.get_player_score(Color.RED), 2)
        # Make sure everyone else is at 0
        self.assertEqual(state.get_player_score(Color.WHITE), 0)
        self.assertEqual(state.get_player_score(Color.BLACK), 0)
        self.assertEqual(state.get_player_score(Color.BROWN), 0)

        # Player 2 make a move
        state.move_avatar(Position(0, 1), Position(1, 1))

        # Make sure player 1 & 2 have a score of 2
        self.assertEqual(state.get_player_score(Color.RED), 2)
        self.assertEqual(state.get_player_score(Color.WHITE), 2)
        # Make sure everyone else is at 0
        self.assertEqual(state.get_player_score(Color.BLACK), 0)
        self.assertEqual(state.get_player_score(Color.BROWN), 0)

    def test_move_log_success1(self):
        # Tests move log
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(Color.RED,  Position(0, 0))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(3, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(1, 1))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(4, 0))

        # Place player 1's avatar
        state.place_avatar(Color.RED,  Position(4, 1))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(2, 0))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(3, 1))

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
        state.place_avatar(Color.RED,  Position(0, 0))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(3, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(1, 1))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(4, 0))

        # Finish placing
        # Place player 1's avatar
        state.place_avatar(Color.RED,  Position(4, 1))
        # Place player 2's avatar
        state.place_avatar(Color.WHITE,  Position(5, 0))
        # Place player 3's avatar
        state.place_avatar(Color.BLACK,  Position(2, 0))
        # Place player 4's avatar
        state.place_avatar(Color.BROWN,  Position(3, 1))

        # Make a move on behalf of player 1
        state.move_avatar(Position(0, 0), Position(2, 1))

        # Make sure player one is at the end, and player 2 is next up
        self.assertSequenceEqual(state.player_order, [Color.WHITE, Color.BLACK, Color.BROWN, Color.RED])

        # Make another move
        state.move_avatar(Position(5, 0), Position(6, 0))

        # Make sure player two is at the end, and player 3 is next up
        self.assertSequenceEqual(state.player_order, [Color.BLACK, Color.BROWN, Color.RED, Color.WHITE])
    
    def test_get_player_positions_success(self):
        # Test successful get player positions
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(Color.RED,  Position(0, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(0, 1))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(2, 1))
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(4, 1))
        # Player 1 place
        state.place_avatar(Color.RED,  Position(5, 0))
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(4, 0))
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(3, 1))

        # Check that player positions are correctly obtained and in the proper order
        self.assertEqual(state.get_player_positions(Color.RED), [Position(0, 0), Position(5, 0)])
        self.assertEqual(state.get_player_positions(Color.WHITE), [Position(0, 1), Position(4, 0)])
        self.assertEqual(state.get_player_positions(Color.BLACK), [Position(2, 1), Position(3, 0)])
        self.assertEqual(state.get_player_positions(Color.BROWN), [Position(4, 1), Position(3, 1)])

        # Move player 1 avatar
        state.move_avatar(Position(5, 0), Position(6, 1))

        self.assertEqual(state.get_player_positions(Color.RED), [Position(0, 0), Position(6, 1)])
    
    def test_get_player_positions_fail1(self):
        # Test failure of get_player_positions due to invalid player id type
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(Color.RED,  Position(0, 0))
        
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
        state.place_avatar(Color.RED,  Position(0, 0))
        
        with self.assertRaises(TypeError):
            state.get_player_positions("hey")
    
    def test_get_player_positions_fail3(self):
        # Test failure of get_player_positions due to player not being in the game
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p4])
        
        with self.assertRaises(NonExistentPlayerException):
            state.get_player_positions(Color.BLACK)

    def test_has_everyone_placed_success1(self):
        # Tests a series of has_everyone_placed
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Player 1 place
        state.place_avatar(Color.RED,  Position(0, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(0, 1))
        self.assertFalse(state.has_everyone_placed())
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(2, 1))
        self.assertFalse(state.has_everyone_placed())
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(4, 1))
        self.assertFalse(state.has_everyone_placed())
        # Player 1 place
        state.place_avatar(Color.RED,  Position(5, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 2 place
        state.place_avatar(Color.WHITE,  Position(4, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 3 place
        state.place_avatar(Color.BLACK,  Position(3, 0))
        self.assertFalse(state.has_everyone_placed())
        # Player 4 place
        state.place_avatar(Color.BROWN,  Position(3, 1))
        self.assertTrue(state.has_everyone_placed())

    def test_get_player_by_color_fail1(self):
        # Tests get_player_by_color failing due to invalid player_color (type wise)
        # Tests a series of has_everyone_placed
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        with self.assertRaises(TypeError):
            state.get_player_by_color('')

    def test_get_player_by_color_fail2(self):
        # Tests get_player_by_color failing due to invalid player_color (not in the game)
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            ])

        with self.assertRaises(NonExistentPlayerException):
            state.get_player_by_color(Color.BROWN)

    def test_get_player_by_color_success(self):
        # Tests successful get_player_by_color
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        self.assertEqual(state.get_player_by_color(Color.RED), self.__p1)
        self.assertEqual(state.get_player_by_color(Color.BLACK), self.__p3)
        self.assertEqual(state.get_player_by_color(Color.WHITE), self.__p2)
        self.assertEqual(state.get_player_by_color(Color.BROWN), self.__p4)

    def test_deepcopy(self):
        # Tests successful deep copy of state
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Place a bunch of avatars
        state.place_avatar(Color.RED,  Position(0, 0))
        state.place_avatar(Color.WHITE,  Position(0, 1))
        state.place_avatar(Color.BLACK,  Position(0, 2))
        state.place_avatar(Color.BROWN,  Position(1, 2))
        state.place_avatar(Color.RED,  Position(1, 0))
        state.place_avatar(Color.WHITE,  Position(1, 1))
        state.place_avatar(Color.BLACK,  Position(2, 2))
        state.place_avatar(Color.BROWN,  Position(2, 1))

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
        self.assertEqual(copied_state.get_player_score(Color.RED), 2)
        self.assertEqual(copied_state.get_player_score(Color.RED), state.get_player_score(Color.RED))
        # Make sure other players' scores are the same
        self.assertEqual(copied_state.get_player_score(Color.WHITE), 0)
        self.assertEqual(copied_state.get_player_score(Color.BLACK), 0)
        self.assertEqual(copied_state.get_player_score(Color.BROWN), 0)
        # Make sure possible actions are the same
        self.assertEqual(copied_state.get_possible_actions(), state.get_possible_actions())

    def test_remove_player_fail1(self):
        # Tests remove_player failing due to invalid Color (type-wise)
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        with self.assertRaises(TypeError):
            state.remove_player('ok')

    def test_remove_player_fail2(self):
        # Tests remove_player failing due to in valid Color
        # (player with provided color does not exist)
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            ])

        with self.assertRaises(NonExistentPlayerException):
            state.remove_player(Color.BROWN)

    def test_remove_player_fail3(self):
        # Tests remove_player failing due to the player having
        # already been removed
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            ])

        # Remove
        state.remove_player(Color.RED)

        with self.assertRaises(NonExistentPlayerException):
            # Remove again
            state.remove_player(Color.RED)

    def test_remove_player_success1(self):
        # Tests successful remove_player on a state where no avatars
        # have been placed

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4
            ])

        # Make sure player to remove is there
        self.assertIn(Color.BROWN, state.player_order)
        self.assertIn(Color.BROWN, state.placements)
        # Remove player
        state.remove_player(Color.BROWN)
        # Check again
        self.assertNotIn(Color.BROWN, state.player_order)
        self.assertNotIn(Color.BROWN, state.placements)

    def test_remove_player_success2(self):
        # Tests successful remove_player on a state where the current player
        # is being removed

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4
            ])

        # Make sure player to remove is there
        self.assertIn(Color.RED, state.player_order)
        self.assertIn(Color.RED, state.placements)
        self.assertEqual(Color.RED, state.current_player)
        # Remove player
        state.remove_player(Color.RED)
        # Check again
        self.assertNotIn(Color.RED, state.player_order)
        self.assertNotIn(Color.RED, state.placements)
        self.assertNotEqual(state.current_player, Color.RED)

    def test_remove_player_success3(self):
        # Tests successful remove_player on a state where placement
        # have been made and continue to be made after a player is remove.
        # It tests to verify that positions on avatars rest open
        # up when their respective player gets removed.

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4
            ])

        # Place a bunch of avatars
        state.place_avatar(Color.RED,  Position(0, 0))
        state.place_avatar(Color.WHITE,  Position(0, 1))
        state.place_avatar(Color.BLACK,  Position(0, 2))
        state.place_avatar(Color.BROWN,  Position(1, 2))

        self.assertEqual(state.players_no, 4)
        # Make sure player to remove is there
        self.assertIn(Color.BROWN, state.player_order)
        self.assertIn(Color.BROWN, state.placements)
        # Make sure player we're gonna remove after is there
        self.assertIn(Color.BLACK, state.placements)
        self.assertIn(Color.BLACK, state.player_order)
        # Make sure position is occupied
        self.assertFalse(state.is_position_open(Position(1, 2)))
        # Remove player
        state.remove_player(Color.BROWN)
        # Check again
        self.assertNotIn(Color.BROWN, state.player_order)
        self.assertNotIn(Color.BROWN, state.placements)
        # Make sure player we're gonna remove after is still there
        self.assertIn(Color.BLACK, state.placements)
        self.assertIn(Color.BLACK, state.player_order)
        # Make sure position opens up and tile is not removed
        self.assertTrue(state.is_position_open(Position(1, 2)))

        state.place_avatar(Color.RED,  Position(1, 0))
        state.place_avatar(Color.WHITE,  Position(1, 1))
        state.place_avatar(Color.BLACK,  Position(2, 2))

        # Make sure black player's positions are closed prior to him
        # being removed
        self.assertFalse(state.is_position_open(Position(2, 2)))
        self.assertFalse(state.is_position_open(Position(0, 2)))

        self.assertEqual(state.players_no, 3)
        # Remove another player
        state.remove_player(Color.BLACK)

        # Make sure player neither removed players are there
        self.assertNotIn(Color.BLACK, state.placements)
        self.assertNotIn(Color.BLACK, state.player_order)
        # Make sure both of black player's position have now become
        # available
        self.assertTrue(state.is_position_open(Position(2, 2)))
        self.assertTrue(state.is_position_open(Position(0, 2)))
        self.assertEqual(state.players_no, 2)

    def test_remove_player_success4(self):
        # Tests successful remove_player on a case wherein both placements
        # and moves have been made and players become unstuck
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4
        ])

        self.assertEqual(state.players_no, 4)

        # Place a bunch of avatars
        state.place_avatar(Color.RED, Position(0, 0))
        state.place_avatar(Color.BLACK, Position(2, 0))
        state.place_avatar(Color.BROWN, Position(5, 0))
        state.place_avatar(Color.RED, Position(6, 1))
        state.place_avatar(Color.WHITE, Position(6, 0))
        state.place_avatar(Color.BLACK, Position(4, 0))
        state.place_avatar(Color.BROWN, Position(3, 0))

        # Make move
        state.move_avatar(Position(0, 0), Position(1, 0))

        # Make sure BLACK is stuck now
        self.assertIn(Color.BLACK, state.stuck_players)
        # Make sure WHITE is stuck
        self.assertIn(Color.WHITE, state.stuck_players)

        # Make sure position we just moved to is now closed
        self.assertFalse(state.is_position_open(Position(1, 0)))

        # Make sure RED still exists
        self.assertIn(Color.RED, state.placements)
        self.assertIn(Color.RED, state.player_order)

        # Remove player
        state.remove_player(Color.RED)

        # Make sure BLACK is unstuck now
        self.assertNotIn(Color.BLACK, state.stuck_players)
        # Make sure WHITE is still stuck
        self.assertIn(Color.WHITE, state.stuck_players)

        # Make sure position we just moved to is now open
        self.assertTrue(state.is_position_open(Position(1, 0)))

        # Make sure player removed player isn't there
        self.assertNotIn(Color.RED, state.placements)
        self.assertNotIn(Color.RED, state.player_order)
        self.assertEqual(state.players_no, 3)

        # Remove BROWN
        state.remove_player(Color.BROWN)
        # Make sure WHITE is unstuck now
        self.assertNotIn(Color.WHITE, state.stuck_players)
        # Make sure player removed player isn't there
        self.assertNotIn(Color.BROWN, state.placements)
        self.assertNotIn(Color.BROWN, state.player_order)
        self.assertEqual(state.players_no, 2)
