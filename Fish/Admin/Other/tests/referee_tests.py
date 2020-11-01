import unittest
import sys

sys.path.append('Player/')
sys.path.append('Admin/')
sys.path.append('Admin/Other')
sys.path.append('../../../Common')

from referee import Referee
from player import Player
from color import Color

class RefereeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RefereeTests, self).__init__(*args, **kwargs)
        self.__p1 = Player('Bob')
        self.__p2 = Player('Jim')
        self.__p3 = Player('Marley')
        self.__p4 = Player('Elon')
        self.__p5 = Player('Elon')

        self.__legal_colors = [Color.WHITE, Color.BLACK, Color.RED, Color.BROWN]

    def test_init_fail1(self):
        # Tests failing init due to rows being invalid
        with self.assertRaises(TypeError):
            Referee('', 2, [self.__p1, self.__p2])

        with self.assertRaises(TypeError):
            Referee(0, 2, [self.__p1, self.__p2])

    def test_init_fail2(self):
        # Tests failing init due to cols being invalid
        with self.assertRaises(TypeError):
            Referee(2, '2', [self.__p1, self.__p2])

        with self.assertRaises(TypeError):
            Referee(2, 0, [self.__p1, self.__p2])

    def test_init_fail3(self):
        # Tests failing init due to player list being invalid (type-wise)
        with self.assertRaises(TypeError):
            Referee(2, 2, 'what')

    def test_init_fail4(self):
        # Tests failing init due to player list being invalid (not containing player objects)
        with self.assertRaises(TypeError):
            Referee(2, 2, ['what', 'ok'])

    def test_init_fail5(self):
        # Tests failing init due to player list being invalid (having too few players)
        with self.assertRaises(ValueError):
            Referee(2, 2, [self.__p1])

    def test_init_fail6(self):
        # Tests failing init due to player list being invalid (having too many players)
        with self.assertRaises(ValueError):
            Referee(2, 2, [self.__p1, self.__p2, self.__p3, self.__p4, self.__p5])

    def test_init_fail7(self):
        # Tests failing init due to inappropriate board dimensions to accomodate all
        # players
        with self.assertRaises(ValueError):
            Referee(1, 2, [self.__p1, self.__p2, self.__p3, self.__p4])

    def test_init_success1(self):
        # Tests successful 4-player init
        referee = Referee(2, 4, [self.__p1, self.__p2, self.__p3, self.__p4])

        # Make sure all player got assigned colors
        for player in referee.players:
            self.assertIn(player.color, self.__legal_colors)
            self.__legal_colors.remove(player.color)

        self.assertEqual(referee.cheating_players, [])
        self.assertEqual(referee.failing_players, [])
        self.assertFalse(referee.started)

    def test_init_success2(self):
        # Tests successful 2-player init
        referee = Referee(5, 10, [self.__p1, self.__p2])

        # Make sure all player got assigned colors
        for player in referee.players:
            self.assertIn(player.color, self.__legal_colors)
            self.__legal_colors.remove(player.color)

        self.assertEqual(referee.cheating_players, [])
        self.assertEqual(referee.failing_players, [])
        self.assertFalse(referee.started)

    def test_start_success1(self):
        # Tests successful start in which everybody succeeds in
        # placing avatar
        referee = Referee(4, 5, [self.__p1, self.__p2])

        referee.start()
