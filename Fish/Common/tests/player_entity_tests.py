import sys
import unittest

from position import Position

sys.path.append('../')

from player_entity import PlayerEntity
from color import  Color


class PlayerEntityTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlayerEntityTests, self).__init__(*args, **kwargs)

    def test_init_fail1(self):
        # Tests failing constructor due to invalid name

        with self.assertRaises(TypeError):
            PlayerEntity(23, Color.BLACK)

    def test_init_fail2(self):
        # Tests failing constructor due to invalid color
        with self.assertRaises(TypeError):
            PlayerEntity('T-Bone', 'BLACK')

    def test_init_success(self):
        # Tests successful Avatar constructor
        player = PlayerEntity('seth', Color.WHITE)

        self.assertEqual(player.name, 'seth')
        self.assertEqual(player.color, Color.WHITE)
        self.assertEqual(player.score, 0)
        self.assertEqual(player.places, [])

    def test_add_place_fail1(self):
        # Tests a failing add_place due to invalid position (type-wise)
        player = PlayerEntity('seth', Color.WHITE)

        with self.assertRaises(TypeError):
            player.add_place('ok')

    def test_add_place_success1(self):
        # Tests a series of successful add_place calls
        player = PlayerEntity('seth', Color.WHITE)

        player.add_place(Position(1, 0))
        self.assertEqual(player.places, [Position(1, 0)])

        player.add_place(Position(2, 0))
        self.assertEqual(player.places, [Position(1, 0), Position(2, 0)])

        player.add_place(Position(5, 3))
        self.assertEqual(player.places, [Position(1, 0), Position(2, 0), Position(5, 3)])

    def test_swap_places_fail1(self):
        # Tests a failing swap_places due to invalid src (type-wise)
        player = PlayerEntity('seth', Color.WHITE)

        player.add_place(Position(1, 0))
        player.add_place(Position(2, 0))

        with self.assertRaises(TypeError):
            player.swap_places('', Position(1, 1))

    def test_swap_places_fail2(self):
        # Tests a failing swap_places due to invalid dst (type-wise)
        player = PlayerEntity('seth', Color.WHITE)

        player.add_place(Position(1, 0))
        player.add_place(Position(2, 0))

        with self.assertRaises(TypeError):
            player.swap_places(Position(1, 0), '')

    def test_swap_places_fail3(self):
        # Tests a failing swap_places due to invalid src (non existent)
        player = PlayerEntity('seth', Color.WHITE)

        player.add_place(Position(1, 0))
        player.add_place(Position(2, 0))

        with self.assertRaises(ValueError):
            player.swap_places(Position(1, 1), Position(2, 1))

    def test_swap_places_success1(self):
        # Tests a successful swap_places
        player = PlayerEntity('seth', Color.WHITE)

        # Add places
        player.add_place(Position(1, 0))
        player.add_place(Position(2, 0))

        # Swap
        player.swap_places(Position(1, 0), Position(2, 1))
        self.assertEqual(player.places, [Position(2, 1), Position(2, 0)])

        # Swap
        player.swap_places(Position(2, 0), Position(2, 2))
        self.assertEqual(player.places, [Position(2, 1), Position(2, 2)])

    def test_score_fail1(self):
        # Tests failing score due to invalid type
        player = PlayerEntity('iBot', Color.WHITE)

        with self.assertRaises(TypeError):
            player.score = -1

    def test_score_fail2(self):
        # Tests failing score due to invalid type
        player = PlayerEntity('iBot', Color.WHITE)

        with self.assertRaises(TypeError):
            player.score = 'whaa'

    def test_score_success(self):
        # Tests successful score setter & getter
        player = PlayerEntity('iBot', Color.WHITE)

        # Increment player's score by 10
        player.score += 10

        # Run check
        self.assertEqual(player.score, 10)
