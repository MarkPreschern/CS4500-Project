import unittest
import sys

sys.path.append('../')

from State import State
from Player import Player
from Board import Board
from Color import Color
from collections import OrderedDict
import tkinter as tk
from ext.MockHelper import MockHelper

from exceptions.AvatarAlreadyPlacedException import AvatarAlreadyPlacedException
from exceptions.AvatarNotPlacedException import AvatarNotPlacedException
from exceptions.NonExistentAvatarException import NonExistentAvatarException
from exceptions.InvalidPositionException import InvalidPositionException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.UnclearPathException import UnclearPathException
from exceptions.PlaceOutOfTurnException import PlaceOutOfTurnException
from exceptions.NoMoreTurnsException import NoMoreTurnsException
from exceptions.GameNotStartedException import GameNotStartedException
from exceptions.NoMoreTurnsException import NoMoreTurnsException
from exceptions.MoveOutOfTurnException import MoveOutOfTurnException


class StateTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StateTests, self).__init__(*args, **kwargs)

        # Initialize some players for testing
        self.__p1 = Player(1, "John", 20, Color.RED)
        self.__p2 = Player(2, "George", 21, Color.WHITE)
        self.__p3 = Player(3, "Gary", 22, Color.BLACK)
        self.__p4 = Player(4, "Jeanine", 23, Color.BROWN)
        self.__p5 = Player(5, "Jen", 22, Color.RED)

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

    def init_test_success(self):
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Assert the board is equal
        self.assertEqual(self.__b, state._State__board)

        # Assert the player dict is equal
        expected_players = OrderedDict()
        expected_players.sort(key=lambda p: p.age)

        expected_players[1] = self.__p1
        expected_players[2] = self.__p2
        expected_players[3] = self.__p3

        self.assertSequenceEqual(expected_players, state._State__players)

        # Assert the placements dictionary is initialized to the proper val
        self.assertEqual(state._State__placements, {})

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
        # Test failure of place_avatar due to avatar id not being in game
        with self.assertRaises(NonExistentAvatarException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar(14, (0, 0))

    def test_place_avatar_fail4(self):
        # Test failure of place_avatar due invalid position
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar(2, "Hello")

    def test_place_avatar_success(self):
        # Test successful placement of avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        state.place_avatar(1, (1, 0))

        expected = {1: (1, 0)}

        self.assertSequenceEqual(state._State__placements, expected)

        # Test a second placement
        state.place_avatar(4, (0, 0))

        expected = {1: (1, 0), 4: (0, 0)}

        self.assertSequenceEqual(state._State__placements, expected)

    def test_place_avatar_repeat_placement(self):
        # Test failure of place_avatar when a player tries to make their
        # initial placements more than once
        with self.assertRaises(AvatarAlreadyPlacedException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.place_avatar(1, (0, 0))

    def test_place_avatar_repeat_position(self):
        # Test failure of place_avatar when placing on a tile that another
        # player is already on
        with self.assertRaises(InvalidPositionException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            state.place_avatar(0, (1, 0))

            # This should raise the exception
            state.place_avatar(4, (1, 0))

    def test_place_avatar_hole(self):
        # Test failure of place_avatar when placing on a hole
        with self.assertRaises(InvalidPositionException):
            new_b = Board.homogeneous(3, 3, 2)
            new_b.remove_tile((0, 0))

            state = State(new_b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state.place_avatar(1, (0, 0))

    def test_move_avatar_fail1(self):
        # Test failure of place_avatar due to invalid avatar id type
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.move_avatar("Hello", (1, 0))

    def test_move_avatar_fail2(self):
        # Test failure of move_avatar due to avatar id < 0
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.move_avatar(-1, (1, 0))

    def test_move_avatar_fail3(self):
        # Test failure of move_avatar due to avatar id not being in game
        with self.assertRaises(NonExistentAvatarException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.move_avatar(99, (0, 0))

    def test_move_avatar_fail4(self):
        # Test failure of move_avatar due invalid position
        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            state.place_avatar(2, (0, 0))
            state.move_avatar(2, "Hello")

    def test_move_avatar_fail5(self):
        # Test failure of move_avatar due target position
        # being the same as starting position
        with self.assertRaises(UnclearPathException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

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

            # Make sure p1 can move
            self.assertTrue(state.can_player_move(self.__p1.id))
            self.assertEqual(state.current_player, self.__p1.id)

            state.move_avatar(2, (0, 0))

    def test_move_avatar_success(self):
        # Test successful move of avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(0, (4, 0))
        # Player 2 place
        state.place_avatar(3, (0, 1))
        # Player 3 place
        state.place_avatar(6, (2, 2))
        # Player 1 place
        state.place_avatar(1, (1, 0))
        # Player 2 place
        state.place_avatar(4, (2, 0))
        # Player 3 place
        state.place_avatar(7, (3, 2))
        # Player 1 place
        state.place_avatar(2, (1, 1))
        # Player 2 place
        state.place_avatar(5, (4, 1))
        # Player 3 place
        state.place_avatar(8, (3, 0))

        # Test a move
        state.move_avatar(1, (0, 0))
        expected = {0: (4, 0), 1: (0, 0), 2: (1, 1), 3: (0, 1), 4: (2, 0),
                    5: (4, 1), 6: (2, 2), 7: (3, 2), 8: (3, 0)}

        self.assertSequenceEqual(state._State__placements, expected)

        # Test a second move
        state.move_avatar(3, (2, 1))
        expected = {0: (4, 0), 1: (0, 0), 2: (1, 1), 3: (2, 1), 4: (2, 0),
                    5: (4, 1), 6: (2, 2), 7: (3, 2), 8: (3, 0)}

        self.assertSequenceEqual(state._State__placements, expected)

    def test_move_through_another_avatar(self):
        # Tests failing move due to an avatar in the way
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(0, (4, 0))
        # Player 2 place
        state.place_avatar(3, (0, 1))
        # Player 3 place
        state.place_avatar(6, (2, 1))
        # Player 1 place
        state.place_avatar(1, (1, 0))
        # Player 2 place
        state.place_avatar(4, (2, 0))
        # Player 3 place
        state.place_avatar(7, (3, 2))
        # Player 1 place
        state.place_avatar(2, (1, 1))
        # Player 2 place
        state.place_avatar(5, (4, 1))
        # Player 3 place
        state.place_avatar(8, (3, 0))

        with self.assertRaises(UnclearPathException):
            state.move_avatar(1, (3, 1))

    def test_move_to_another_player(self):
        # Tests failing move due to an avatar being at target
        # position
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        # Player 1 place
        state.place_avatar(0, (4, 0))
        # Player 2 place
        state.place_avatar(3, (0, 1))
        # Player 3 place
        state.place_avatar(6, (2, 1))
        # Player 1 place
        state.place_avatar(1, (1, 0))
        # Player 2 place
        state.place_avatar(4, (2, 0))
        # Player 3 place
        state.place_avatar(7, (3, 2))
        # Player 1 place
        state.place_avatar(2, (1, 1))
        # Player 2 place
        state.place_avatar(5, (4, 1))
        # Player 3 place
        state.place_avatar(8, (3, 0))

        with self.assertRaises(UnclearPathException):
            state.move_avatar(1, (2, 1))

    def test_move_avatar_no_placement(self):
        # Test failure of move_avatar when a player tries to move
        # without an initial placement
        with self.assertRaises(AvatarNotPlacedException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state.move_avatar(1, (0, 0))

    def test_move_avatar_to_hole(self):
        # Test failure of move_avatar when a player tries to move
        # to a hole
        with self.assertRaises(UnclearPathException):
            new_b = Board.homogeneous(2, 5, 3)
            new_b.remove_tile((0, 0))

            state = State(new_b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Player 1 place
            state.place_avatar(0, (4, 0))
            # Player 2 place
            state.place_avatar(3, (0, 1))
            # Player 3 place
            state.place_avatar(6, (2, 1))
            # Player 1 place
            state.place_avatar(1, (1, 0))
            # Player 2 place
            state.place_avatar(4, (2, 0))
            # Player 3 place
            state.place_avatar(7, (3, 2))
            # Player 1 place
            state.place_avatar(2, (1, 1))
            # Player 2 place
            state.place_avatar(5, (4, 1))
            # Player 3 place
            state.place_avatar(8, (3, 0))

            # This should raise the exception
            state.move_avatar(1, (0, 0))

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
            state.place_avatar(0, (1, 0))
            # Player 2 place
            state.place_avatar(3, (0, 1))
            # Player 3 place
            state.place_avatar(6, (4, 0))
            # Player 1 place
            state.place_avatar(1, (2, 1))
            # Player 2 place
            state.place_avatar(4, (2, 0))
            # Player 3 place
            state.place_avatar(7, (3, 2))
            # Player 1 place
            state.place_avatar(2, (1, 1))
            # Player 2 place
            state.place_avatar(5, (4, 1))
            # Player 3 place
            state.place_avatar(8, (3, 1))

            # This should raise the exception
            state.move_avatar(0, (4, 0))

    def test_can_player_move_fail1(self):
        # Tests failing can_player_move due to invalid
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
            self.assertTrue(state.can_player_move(self.__p1.id))
            # This should raise the exception
            state.can_player_move("1")

    def test_can_player_move_fail2(self):
        # Tests failing can_player_move due to non-existent
        # player id

        with self.assertRaises(NonExistentPlayerException):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # This should raise the exception
            state.can_player_move(231)

    def test_can_player_move_fail3(self):
        # Tests failing can_player_move due to avatar
        # being surrounded by other avatars

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(0, (3, 1))
        # Place player 2's avatar
        state.place_avatar(2, (5, 0))
        # Place player 3's avatar
        state.place_avatar(4, (0, 0))
        # Place player 4's avatar
        state.place_avatar(6, (4, 0))

        # Place player 1's avatar
        state.place_avatar(1, (1, 0))
        # Place player 2's avatars
        state.place_avatar(3, (3, 0))
        # Place player 3's avatars
        state.place_avatar(5, (6, 0))
        # Place player 4's avatars
        state.place_avatar(7, (2, 0))

        # This should raise the exception
        self.assertFalse(state.can_player_move(4))

    def test_can_player_move_success1(self):
        # Tests successful can_player_move with almost
        # completely surrounded avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatars
        state.place_avatar(0, (1, 0))
        # Place player 2's avatars
        state.place_avatar(2, (3, 0))
        # Place player 3's avatars
        state.place_avatar(4, (5, 2))
        # Place player 4's avatars
        state.place_avatar(6, (0, 0))

        # Place player 1's avatars
        state.place_avatar(1, (6, 1))
        # Place player 2's avatar
        state.place_avatar(3, (6, 0))
        # Place player 3's avatar
        state.place_avatar(5, (5, 0))
        # Place player 4's avatar
        state.place_avatar(7, (2, 0))

        self.assertTrue(state.can_player_move(4))
        self.assertTrue(state.can_anyone_move())

    def test_can_player_move_success2(self):
        # Tests successful can_player_move with almost
        # completely surrounded avatar where not all
        # avatars have been placed yet
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(0, (0, 0))
        # Place player 2's avatar
        state.place_avatar(2, (3, 0))
        # Place player 3's avatar
        state.place_avatar(4, (1, 1))
        # Place player 4's avatar
        state.place_avatar(6, (4, 0))

        # Place player 1's avatar
        state.place_avatar(1, (1, 0))
        # Place player 2's avatar
        state.place_avatar(3, (5, 0))
        # Place player 3's avatar
        state.place_avatar(5, (4, 1))

        # This return false as player 4 has not
        # finished placing their avatars
        self.assertFalse(state.can_player_move(4))
        # No one should be able to move
        self.assertFalse(state.can_anyone_move())

    def test_can_player_move_success3(self):
        # Tests successful can_player_move where one of
        # player's avatars is completely surrounded
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatar
        state.place_avatar(0, (0, 0))
        # Place player 2's avatar
        state.place_avatar(2, (3, 0))
        # Place player 3's avatar
        state.place_avatar(4, (1, 1))
        # Place player 4's avatar
        state.place_avatar(6, (4, 0))

        # Place player 1's avatar
        state.place_avatar(1, (1, 0))
        # Place player 2's avatar
        state.place_avatar(3, (5, 0))
        # Place player 3's avatar
        state.place_avatar(5, (4, 1))
        # Place player 4's avatar
        state.place_avatar(7, (3, 1))

        self.assertTrue(state.can_player_move(4))

    def test_get_avatars_by_player_id_fail1(self):
        # Tests get_avatars_by_player_id failing due to
        # invalid player_id
        state = State(self.__b, players=[
            self.__p1,
            self.__p2])

        with self.assertRaises(TypeError):
            state.get_avatars_by_player_id(-1)

        with self.assertRaises(TypeError):
            state.get_avatars_by_player_id('hoola hoop')

    def test_get_avatars_by_player_id_success1(self):
        # Tests successful get_avatars_by_player_id
        # that returns player's avatars' ids
        state = State(self.__b, players=[
            self.__p1,
            self.__p2])

        expected = [0, 1, 2, 3]

        self.assertEqual(state.get_avatars_by_player_id(1), expected)

    def test_get_player_order1(self):
        # Tests player order for two players
        state = State(self.__b, players=[
            self.__p2,
            self.__p1])

        self.assertSequenceEqual(state.get_player_order(), [self.__p1.id, self.__p2.id])

    def test_get_player_order2(self):
        # Tests player order for four players
        state = State(self.__b, players=[
            self.__p3,
            self.__p1,
            self.__p5,
            self.__p2])

        self.assertSequenceEqual(state.get_player_order(),
                                 [self.__p1.id, self.__p2.id,
                                  self.__p3.id, self.__p5.id])

    def test_place_out_of_turn(self):
        # Test the case where the player places out of turn
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Have player 2 place when it's player 1's turn
        with self.assertRaises(PlaceOutOfTurnException):
            state.place_avatar(3, (0, 0))

    def test_move_out_of_turn(self):
        # Test the case where the player moves out of turn
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements
        state.place_avatar(0, (0, 0))
        state.place_avatar(2, (1, 0))
        state.place_avatar(4, (0, 1))
        state.place_avatar(6, (1, 1))
        state.place_avatar(1, (2, 0))
        state.place_avatar(3, (2, 1))
        state.place_avatar(5, (3, 0))
        state.place_avatar(7, (3, 1))

        # Have player 2 place when it's player 1's turn
        with self.assertRaises(MoveOutOfTurnException):
            state.move_avatar(4, (4, 0))

    def test_game_started(self):
        # Test successful progress of game started field based on player placements

        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Ensure the game hasn't started until all avatars are placed
        self.assertFalse(state.game_started)

        # Set up the board with placements
        state.place_avatar(0, (0, 0))
        state.place_avatar(2, (1, 0))
        state.place_avatar(4, (0, 1))
        state.place_avatar(6, (1, 1))

        # Ensure again that the game hasn't started until all avatars are placed
        self.assertFalse(state.game_started)

        state.place_avatar(1, (2, 0))
        state.place_avatar(3, (2, 1))
        state.place_avatar(5, (3, 0))
        state.place_avatar(7, (3, 1))

        # Game should be started
        self.assertTrue(state.game_started)

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
        state.place_avatar(0, (0, 0))
        state.place_avatar(2, (1, 0))
        state.place_avatar(4, (0, 1))
        state.place_avatar(6, (1, 1))
        state.place_avatar(1, (2, 0))
        state.place_avatar(3, (2, 1))
        state.place_avatar(5, (3, 0))
        state.place_avatar(7, (3, 1))

        # Current order is p1, p2, p3, p4
        self.assertEqual(state.current_player, 1)

        # Valid move that should trigger no exceptions and cause current player to
        # increment
        state.move_avatar(1, (4, 0))

        # Play moves to p2
        self.assertNotEqual(state.current_player, 1)
        self.assertEqual(state.current_player, 2)

        # Make move for p2
        state.move_avatar(3, (4, 1))

        # Play moves to p3
        self.assertNotEqual(state.current_player, 2)
        self.assertEqual(state.current_player, 3)

        # Make move for p3
        state.move_avatar(5, (5, 0))

        # Play moves to p4
        self.assertNotEqual(state.current_player, 3)
        self.assertEqual(state.current_player, 4)

        # Make move for p4
        state.move_avatar(7, (5, 1))

        # Play moves to p1
        self.assertNotEqual(state.current_player, 4)
        self.assertEqual(state.current_player, 1)

    def test_player_skip_when_no_moves(self):
        # Test the functionality of skipping players when they cannot make any moves
        new_b = Board.homogeneous(3, 5, 2)
        state = State(new_b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. all of player 2's avatars are
        # blocked
        state.place_avatar(0, (3, 0))
        state.place_avatar(2, (0, 0))
        state.place_avatar(4, (1, 0))
        state.place_avatar(6, (2, 0))
        state.place_avatar(1, (3, 1))
        state.place_avatar(3, (0, 1))
        state.place_avatar(5, (1, 1))
        state.place_avatar(7, (2, 1))

        # Verify that it is player 1's turn
        self.assertEqual(state.current_player, 1)

        # Move one of player 1's avatars
        state.move_avatar(1, (4, 1))

        # Verify that it is not p1, p2, nor p3's turn
        self.assertNotEqual(state.current_player, 1)
        self.assertNotEqual(state.current_player, 2)
        self.assertNotEqual(state.current_player, 3)

        # Verify that it is actually player 4's turn and that p2 and p3 have been skipped
        self.assertEqual(state.current_player, 4)

    def test_game_over(self):
        # Test the game until the game is over

        # This exception will be thrown when the game ends
        with self.assertRaises(NoMoreTurnsException):
            new_b = Board.homogeneous(3, 5, 2)
            state = State(new_b, players=[
                self.__p1,
                self.__p2,
                self.__p3,
                self.__p4])

            # Set up the board with placements s.t. only 2 moves can be made
            state.place_avatar(0, (3, 0))
            state.place_avatar(2, (0, 0))
            state.place_avatar(4, (1, 0))
            state.place_avatar(6, (2, 0))
            state.place_avatar(1, (3, 1))
            state.place_avatar(3, (0, 1))
            state.place_avatar(5, (1, 1))
            state.place_avatar(7, (2, 1))

            # Make move 1 for p1
            state.move_avatar(1, (4, 1))

            # Mave move 2 for p3, meaning game should end because all tiles are either
            # occupied or holes
            state.move_avatar(6, (4, 0))
