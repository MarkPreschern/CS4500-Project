import unittest
import sys

sys.path.append('../')

from State import State
from Player import Player
from Board import Board
from Color import Color
from collections import OrderedDict

from exceptions.AvatarAlreadyPlacedException import AvatarAlreadyPlacedException
from exceptions.AvatarNotPlacedException import AvatarNotPlacedException
from exceptions.NonExistentAvatarException import NonExistentAvatarException
from exceptions.InvalidPositionException import InvalidPositionException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.UnclearPathException import UnclearPathException


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
        state.place_avatar(2, (0, 0))

        expected = {1: (1, 0), 2: (0, 0)}

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
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.place_avatar(2, (1, 0))

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
        with self.assertRaises(ValueError):
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

            state.place_avatar(2, (0, 0))
            state.move_avatar(2, (0, 0))

    def test_move_avatar_success(self):
        # Test successful move of avatar
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        state.place_avatar(1, (1, 0))
        # Test a move
        state.move_avatar(1, (0, 0))
        expected = {1: (0, 0)}

        self.assertSequenceEqual(state._State__placements, expected)

        # Test a second move
        state.move_avatar(1, (2, 0))
        expected = {1: (2, 0)}

        self.assertSequenceEqual(state._State__placements, expected)

    # ********************************************************************
    # TODO: Test movement where a player attempts to move through another
    # avatar or to another avatar
    # ********************************************************************

    def test_move_through_another_avatar(self):
        # Tests failing move due to an avatar in the way
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        state.place_avatar(1, (1, 0))
        state.place_avatar(2, (2, 1))

        with self.assertRaises(UnclearPathException):
            state.move_avatar(1, (3, 1))

    def test_move_to_another_player(self):
        # Tests failing move due to an avatar being at target
        # position
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3])

        state.place_avatar(1, (1, 0))
        state.place_avatar(2, (2, 1))

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
            new_b = Board.homogeneous(3, 3, 2)
            new_b.remove_tile((0, 0))

            state = State(new_b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            state.place_avatar(1, (1, 0))

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
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.move_avatar(1, (4, 0))

    def test_can_player_move_fail1(self):
        # Tests failing can_player_move due to invalid
        # player_id

        with self.assertRaises(TypeError):
            state = State(self.__b, players=[
                self.__p1,
                self.__p2,
                self.__p3])

            # Successful placement
            state.place_avatar(1, (1, 0))

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
        # Place player 1's avatars
        state.place_avatar(0, (0, 0))
        state.place_avatar(1, (1, 0))
        # Place player 2's avatars
        state.place_avatar(2, (3, 0))
        state.place_avatar(3, (5, 0))
        # Place player 3's avatars
        state.place_avatar(4, (6, 0))
        state.place_avatar(5, (3, 1))
        # Place player 4's avatars
        state.place_avatar(6, (2, 0))
        state.place_avatar(7, (4, 0))

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
        state.place_avatar(0, (0, 0))
        state.place_avatar(1, (1, 0))
        # Place player 2's avatars
        state.place_avatar(2, (3, 0))
        state.place_avatar(3, (5, 0))
        # Place player 3's avatars
        state.place_avatar(4, (1, 1))
        state.place_avatar(5, (3, 1))
        # Place player 4's avatars
        state.place_avatar(6, (2, 0))
        state.place_avatar(7, (4, 0))

        # This should raise the exception
        self.assertTrue(state.can_player_move(4))

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
        # Place player 1's avatars
        state.place_avatar(0, (0, 0))
        state.place_avatar(1, (1, 0))
        # Place player 2's avatars
        state.place_avatar(2, (3, 0))
        state.place_avatar(3, (5, 0))
        # Place player 3's avatars
        state.place_avatar(4, (1, 1))
        state.place_avatar(5, (3, 1))
        # Place player 4's avatars
        # state.place_avatar(6, (2, 0))
        state.place_avatar(7, (4, 0))

        # This return false as player 4 has not
        # finished placing their avatars
        self.assertFalse(state.can_player_move(4))

    def test_can_player_move_success3(self):
        # Tests successful can_player_move where one of
        # player's avatars is completely surrounded
        state = State(self.__b, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Successful placement
        # Place player 1's avatars
        state.place_avatar(0, (0, 0))
        state.place_avatar(1, (1, 0))
        # Place player 2's avatars
        state.place_avatar(2, (3, 0))
        state.place_avatar(3, (5, 0))
        # Place player 3's avatars
        state.place_avatar(4, (1, 1))
        state.place_avatar(5, (4, 0))
        # Place player 4's avatars
        state.place_avatar(6, (2, 0))
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
