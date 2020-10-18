import sys
import unittest

sys.path.append('../')

from player import Player
from color import  Color


class PlayerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlayerTests, self).__init__(*args, **kwargs)

    def test_init_fail1(self):
        # Tests failing Player constructor due to invalid id
        with self.assertRaises(TypeError):
            Player('', 'okay', 20, Color.BLACK)

    def test_init_fail2(self):
        # Tests failing Player constructor due to invalid name

        with self.assertRaises(TypeError):
            Player(1, 23, 20, Color.BLACK)

    def test_init_fail3(self):
        # Tests failing Player constructor due to invalid age

        with self.assertRaises(TypeError):
            Player(1, 'Bob', 'old', Color.BLACK)

    def test_init_fail4(self):
        # Tests failing Player constructor due to invalid color
        with self.assertRaises(TypeError):
            Player(2, 'T-Bone', 20, 'BLACK')

    def test_init_success(self):
        # Tests successful Avatar constructor
        player = Player(1, 'seth', 23, Color.WHITE)

        self.assertEqual(player.id, 1)
        self.assertEqual(player.name, 'seth')
        self.assertEqual(player.age, 23)
        self.assertEqual(player.color, Color.WHITE)
        self.assertEqual(player.score, 0)

    def test_score_fail1(self):
        # Tests failing score due to invalid type
        player = Player(99, 'iBot', 100, Color.WHITE)

        with self.assertRaises(TypeError):
            player.score = -1

    def test_score_fail2(self):
        # Tests failing score due to invalid type
        player = Player(99, 'iBot', 100, Color.WHITE)

        with self.assertRaises(TypeError):
            player.score = 'whaa'

    def test_score_success(self):
        # Tests successful score setter & getter
        player = Player(99, 'iBot', 100, Color.WHITE)

        # Increment player's score by 10
        player.score += 10

        # Run check
        self.assertEqual(player.score, 10)
