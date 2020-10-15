import sys
import unittest

sys.path.append('../')

from Avatar import Avatar
from Color import  Color


class AvatarTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AvatarTests, self).__init__(*args, **kwargs)

    def test_init_fail1(self):
        # Tests failing Avatar constructor due to invalid id
        with self.assertRaises(TypeError):
            Avatar('', 23, Color.BLACK)

    def test_init_fail2(self):
        # Tests failing Avatar constructor due to invalid player_id

        with self.assertRaises(TypeError):
            Avatar(1, '23', Color.BLACK)

    def test_init_fail3(self):
        # Tests failing Avatar constructor due to invalid color
        with self.assertRaises(TypeError):
            Avatar(2, 23, 'BLACK')

    def test_init_success(self):
        # Tests successful Avatar constructor
        avatar = Avatar(1, 23, Color.BLACK)

        self.assertEqual(avatar.id, 1)
        self.assertEqual(avatar.player_id, 23)
        self.assertEqual(avatar.color, Color.BLACK)
