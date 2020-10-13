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
from exceptions.InvalidPosition import InvalidPosition


class StateTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StateTests, self).__init__(*args, **kwargs)

        # Initialize some players for testing
        self.p1 = Player(1, "John", 20, Color.RED)
        self.p2 = Player(2, "George", 21, Color.WHITE)
        self.p3 = Player(3, "Gary", 22, Color.GREEN
        self.p4 = Player(4, "Jeanine", 23, Color.BROWN)
        self.p5 = Player(5, "Jen", 22, Color.RED)

        # Initialize board for testing
        self.b = Board.homogenous(3, 3, 2)


    def init_test_fail1(self):
        # Tests constructor failing due to invalid board
        state = State(['hello', 'Buick'],
                      players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

    def init_test_fail2(self):
        # Tests constructor failing due to invalid player list
        with self.assertRaises(TypeError):
            state = State(self.b, players={
                1: self.p1, 
                2: self.p2, 
                3: self.p3})

    def init_test_fail3(self):
        # Test constructor failing due to player list not containing all players
        with self.assertRaises(TypeError):
            state = State(self.b, players=[
                self.p1, 
                self.p2, 
                "Hello"])
    
    def init_test_fail4(self):
        # Test constructor failing due to number of players being smaller than the minimum
        with self.assertRaises(ValueError):
            state = State(self.b, players=[self.p2])
    
    def init_test_fail5(self):
        # Test constructor failing due to number of players being larger than the max
        with self.assertRaises(ValueError):
            state = State(self.b, players=[
                self.p2, 
                self.p1, 
                self.p3, 
                self.p4, 
                self.p5])
    
    def init_test_success(self):
        state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

        # Assert the board is equal
        self.assertEqual(self.b, state._State__board)

        # Assert the player dict is equal
        expected_players = OrderedDict()
        expected_players.sort(key=lambda p: p.age)

        expected_players[1] = self.p1
        expected_players[2] = self.p2
        expected_players[3] = self.p3

        self.assertSequenceEqual(expected_players, state._State__players)

        # Assert the placements dictionary is initialized to the proper val
        self.assertEqual(state._State__placements, {})

    def test_place_avatar_fail1(self):
        # Test failure of place_avater due to invalid player id type
        with self.assertRaises(TypeError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

            state.place_avatar("Hello", (1, 0))
    
    def test_place_avatar_fail2(self):
        # Test failure of place_avater due to player id <= 0
        with self.assertRaises(TypeError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
            
            state.place_avatar(-1, (1, 0))
    
    def test_place_avatar_fail3(self):
        # Test failure of place_avatar due to player id not being in game
        with self.assertRaises(ValueError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
            
            state.place_avatar(4, (0, 0))
    
    def test_place_avatar_fail4(self):
        # Test failure of place_avatar due invalid position
        with self.assertRaises(ValueError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
            
            state.place_avatar(2, "Hello")
    
    def test_place_avatar_success(self):
        # Test successful placement of avatar
        state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
        
        state.place_avatar(1, (1, 0))

        expected = OrderedDict
        expected.sort(key=lambda p: p.age)
        expected[1] = (1, 0)

        self.assertSequenceEqual(self._State__placements, expected)

        # Test a second placement
        state.place_avatar(2, (0, 0))

        expected[2] = (0, 0)

        self.assertSequenceEqual(self._State__placements, expected)

    
    def test_place_avatar_repeat_placement(self):
        # Test failure of place_avater when a player tries to make their 
        # initial placements more than once
        with self.assertRaises(AvatarAlreadyPlacedException):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
        
            # Successful placement
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.place_avatar(1, (0, 0))

    def test_place_avatar_repeat_position(self):
        # Test failure of place_avatar when placing on a tile that another
        # player is already on
        with self.assertRaises(InvalidPosition):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
        
            # Successful placement
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.place_avatar(2, (1, 0))
    
    def test_place_avatar_hole(self):
        # Test failure of place_avatar when placing on a hole
        with self.assertRaises(InvalidPosition):
            new_b = Board.homogenous(3, 3, 2)
            new_b.remove_tile(0, 0)

            state = State(new_b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

            # This should raise the exception
            state.place_avatar(1, (0, 0))
    
    def test_move_avatar_fail1(self):
        # Test failure of place_avater due to invalid player id type
        with self.assertRaises(TypeError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

            state.move_avatar("Hello", (1, 0))
    
    def test_move_avatar_fail2(self):
        # Test failure of move_avater due to player id <= 0
        with self.assertRaises(TypeError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
            
            state.move_avatar(-1, (1, 0))
    
    def test_move_avatar_fail3(self):
        # Test failure of move_avatar due to player id not being in game
        with self.assertRaises(ValueError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
            
            state.move_avatar(4, (0, 0))
    
    def test_move_avatar_fail4(self):
        # Test failure of move_avatar due invalid position
        with self.assertRaises(ValueError):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
            
            state.place_avatar(2, (0, 0))
            state.move_avatar(2, "Hello")
    
    def test_move_avatar_success(self):
        # Test successful placement of avatar
        state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
        
        state.place_avatar(1, (1, 0))

        expected = OrderedDict
        expected.sort(key=lambda p: p.age)

        # Test a move
        state.move_avatar(1, (0, 0))
        expected[1] = (0, 0)

        self.assertSequenceEqual(self._State__placements, expected)

        # Test a second move
        state.move_avatar(1, (2, 0))
        expected[1] = (2, 0)

        self.assertSequenceEqual(self._State__placements, expected)


    # ********************************************************************
    # TODO: Test movement where a player attempts to move through another
    # player or to another player
    # ********************************************************************
    def test_move_through_another_player(self):
        pass

    def test_move_to_another_player(self):
        pass

    def test_move_avatar_no_placement(self):
        # Test failure of move_avatar when a player tries to move
        # without an initial placement
        with self.assertRaises(AvatarNotPlacedException):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

            # This should raise the exception
            state.move_avatar(1, (0, 0))

    def test_move_avatar_to_hole(self):
        # Test failure of move_avatar when a player tries to move
        # to a hole
        with self.assertRaises(InvalidPosition):
            new_b = Board.homogenous(3, 3, 2)
            new_b.remove_tile(0, 0)

            state = State(new_b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

            # Successful placement
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.move_avatar(1, (0, 0))
    
    def test_move_avatar_no_straight_line(self):
        # Test failure of move avatar when a player attempts
        # to move to a tile that is not along a straight
        # path from their starting position
        with self.assertRaises(InvalidPosition):
            state = State(self.b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])

            # Successful placement
            state.place_avatar(1, (1, 0))

            # This should raise the exception
            state.move_avatar(1, (2, 1))
    
    def test_can_anyone_move(self):
        # Test success of can anyone move during different
        # game state conditions

        new_b = Board.homogenous(3, 3, 2)
        state = State(new_b, players=[
                          self.p1, 
                          self.p2, 
                          self.p3])
        
        # Make initial placements
        state.place_avatar(1, (0, 0))
        state.place_avatar(2, (2, 0))
        state.place_avatar(3, (1, 1))

        self.assertTrue(state.can_anyone_move())

        # Make players 1 and 2 unable to move
        new_b.remove_tile((1, 0))

        self.assertTrue(state.can_anyone_move())

        # Make player 3 unable to move
        new_b.remove_tile((0, 1))
        new_b.remove_tile((2, 1))

        self.assertFalse(state.can_anyone_move())

        
    

        


