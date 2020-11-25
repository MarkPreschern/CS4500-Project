from Fish.Player.player import Player
import sys
import unittest

sys.path.append('../')
sys.path.append('../sprites')
sys.path.append('../../Admin')
sys.path.append('../../Admin/Other')
sys.path.append('../../Player')

from game_visualizer import GameVisualizer
from player_entity import PlayerEntity
from player import Player
from color import Color


class VisualizerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(VisualizerTests, self).__init__(*args, **kwargs)

        # Initialize some players for testing
        self.__p1 = Player("John")
        self.__p2 = Player("George")
        self.__p3 = Player("Gary")
        self.__p4 = Player("Jeanine")
        self.__p5 = Player("Jen")

    def fails_without_player_list(self):
        with self.assertRaises(TypeError):
            GameVisualizer('player1', 4, 4)

    def fails_without_board_dims(self):
        with self.assertRaises(TypeError):
            GameVisualizer([self.__p1, self.__p2], 'whoops', 4)

    def fails_with_0_dimensions(self):
        with self.assertRaises(TypeError):
            GameVisualizer([self.__p1, self.__p2], 2, 0)

    def fails_with_5_players(self):
        with self.assertRaises(ValueError):
            GameVisualizer([self.__p1, self.__p2, self.__p3, self.__p4, self.__p5], 3, 3, 1)

    def test_2_players_success(self):
        # test a successful constructor with 2 players
        game_viz = GameVisualizer([self.__p1, self.__p2], 4, 4, 0, 3)
        final_game_report = game_viz.run()
        self.assertEqual([], final_game_report['cheating_players'])

    def test_3_players_success(self):
        # test a successful constructor with 2 players
        game_viz = GameVisualizer([self.__p1, self.__p2, self.__p3], 5, 5, 0, 3)
        final_game_report = game_viz.run()
        self.assertEqual([], final_game_report['cheating_players'])

    def test_4_players_success(self):
        # test a successful constructor with 3 players
        game_viz = GameVisualizer([self.__p1, self.__p2, self.__p3, self.__p4], 3, 3)
        final_game_report = game_viz.run()
        self.assertEqual([], final_game_report['cheating_players'])