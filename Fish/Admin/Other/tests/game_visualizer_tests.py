import unittest
import sys
import random

sys.path.append('Player/')
sys.path.append('Admin/')
sys.path.append('Admin/Other')
sys.path.append('../../../Common')

from game_visualizer import GameVisualizer
from player import Player
from referee import Referee

class GameVisualizerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameVisualizerTests, self).__init__(*args, **kwargs)

        self.__p1 = Player(name='a')
        self.__p2 = Player(name='b')
        self.__p3 = Player(name='c')
        self.__p4 = Player(name='d')

        self.__p5 = Player(name='e', search_depth=5)
        self.__p6 = Player(name='f', search_depth=5)

        # Set seed to add some predictability as to what kind of board
        # the referee is gonna setup
        random.seed(900)

        Referee.DIFFICULTY_FACTOR = 1

    def test_init_fail1(self):
        # Tests failing init due to invalid list of players
        with self.assertRaises(TypeError):
            GameVisualizer({'not a list': 'duh'})

    def test_init_fail2(self):
        # Tests failing init due to invalid board_row_no
        with self.assertRaises(TypeError):
            GameVisualizer([ self.__p1, self.__p2 ], 'nope')

    def test_init_fail3(self):
        # Tests failing init due to invalid board_col_no
        with self.assertRaises(TypeError):
            GameVisualizer([ self.__p1, self.__p2 ], 2, 'nope')

    def test_run1(self):
        # Tests that a game with 0 render timeout on a 5x5 board with 2 players completes
        GameVisualizer.RENDER_TIMEOUT = 0

        gameVisualizer = GameVisualizer([self.__p1, self.__p2])

        gameVisualizer.run()

        self.assertTrue(True) # assert that the game ran through completely

    def test_run2(self):
        # Tests that a game with 0 render timeout on a 5x5 board with 4 players completes
        GameVisualizer.RENDER_TIMEOUT = 0

        gameVisualizer = GameVisualizer([self.__p1, self.__p2, self.__p3, self.__p4])

        gameVisualizer.run()

        self.assertTrue(True)  # assert that the game ran through completely

    def test_run_timeout_success(self):
        # Tests that a game where all of it's players timeout still completes
        GameVisualizer.RENDER_TIMEOUT = 0

        gameVisualizer = GameVisualizer([self.__p5, self.__p6])

        gameVisualizer.run()

        self.assertTrue(True)  # assert that the game ran through completely

