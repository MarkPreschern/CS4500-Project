import unittest
import sys

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

        Referee.DIFFICULTY_FACTOR = 1

    def test_init_fail1(self):
        # Tests failing init due to invalid list of players
        with self.assertRaises(TypeError):
            GameVisualizer({'not a list': 'duh'})

    def test_init_fail2(self):
        # Tests failing init due to invalid board_row_no
        with self.assertRaises(TypeError):
            GameVisualizer([self.__p1, self.__p2], 'nope')

    def test_init_fail3(self):
        # Tests failing init due to invalid board_col_no
        with self.assertRaises(TypeError):
            GameVisualizer([self.__p1, self.__p2], 2, 'nope')

    def test_run1(self):
        # Tests that a game with 0 render timeout on a 5x5 board with 2 players completes
        game_visualizer = GameVisualizer([self.__p1, self.__p2], render_timeout=0)
        report = game_visualizer.run()
        self.assertEqual([], report['cheating_players'])

    def test_run2(self):
        # Tests that a game with 0 render timeout on a 5x5 board with 3 players completes
        game_visualizer = GameVisualizer([self.__p1, self.__p2, self.__p3], render_timeout=0)
        report = game_visualizer.run()
        self.assertEqual([], report['cheating_players'])

    def test_run3(self):
        # Tests that a game with 0 render timeout on a 5x5 board with 4 players completes
        game_visualizer = GameVisualizer([self.__p1, self.__p2, self.__p3, self.__p4], render_timeout=0)
        report = game_visualizer.run()
        self.assertEqual([], report['cheating_players'])
