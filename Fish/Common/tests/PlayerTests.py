import sys
import unittest

sys.path.append('../')

from Player import Player
from Color import  Color


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
