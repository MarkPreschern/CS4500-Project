import unittest
import sys
from unittest.mock import patch

sys.path.append('Player/')
sys.path.append('Admin/')
sys.path.append('Admin/Other')
sys.path.append('Admin/Other/mocks')
sys.path.append('../../../Common')

from manager import Manager
from player import Player


class ManagerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ManagerTests, self).__init__(*args, **kwargs)

        self.__p1 = Player('Bob')
        self.__p2 = Player('Jim')
        self.__p3 = Player('Marley')
        self.__p4 = Player('Elon')
        self.__p5 = Player('Damien')
        self.__p6 = Player('Roger Dodger')
        self.__p7 = Player('Nathan')
        self.__p8 = Player('Sam')
        self.__p9 = Player('Doug')
        self.__p10 = Player('Sebastian')
        self.__p11 = Player('iHaxor')
        self.__p12 = Player('Razorsharp')
        self.__p13 = Player('Sony')
        self.__p14 = Player('Sony 2')
        self.__p15 = Player('Sony 3')
        self.__p16 = Player('Sony 4')
        self.__p17 = Player('Sony 5')

    def test_divide_players1(self):
        # Tests a 6 = 4 + 2 player divide
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4, self.__p5, self.__p6])

        self.assertEqual(manager._Manager__divide_players(),
                         [[self.__p1, self.__p2, self.__p3, self.__p4],
                          [self.__p5, self.__p6]])

    def test_divide_players2(self):
        # Tests a 5 = 3 + 2 player divide
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4, self.__p5])

        self.assertEqual(manager._Manager__divide_players(),
                         [[self.__p1, self.__p2, self.__p3],
                          [self.__p4, self.__p5]])

    def test_divide_players3(self):
        # Tests a 17 = 4 + 4 + 4 + 3 + 2 player divide
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4, self.__p5, self.__p6, self.__p7,
                           self.__p8, self.__p9, self.__p10, self.__p11, self.__p12, self.__p13, self.__p14,
                           self.__p15, self.__p16, self.__p17])

        self.assertEqual(manager._Manager__divide_players(),
                         [[self.__p1, self.__p2, self.__p3, self.__p4],
                          [self.__p5, self.__p6, self.__p7, self.__p8],
                          [self.__p9, self.__p10, self.__p11, self.__p12],
                          [self.__p13, self.__p14, self.__p15],
                          [self.__p16, self.__p17]])

    @patch("constants.MIN_PLAYERS", 3)
    def test_divide_players4(self):
        # Tests a 17 = 4 + 4 + 3 + 3 + 3 player divide with MIN_PLAYERS mocked to 3
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4, self.__p5, self.__p6, self.__p7,
                           self.__p8, self.__p9, self.__p10, self.__p11, self.__p12, self.__p13, self.__p14,
                           self.__p15, self.__p16, self.__p17])

        self.assertEqual(manager._Manager__divide_players(),
                         [[self.__p1, self.__p2, self.__p3, self.__p4],
                          [self.__p5, self.__p6, self.__p7, self.__p8],
                          [self.__p9, self.__p10, self.__p11],
                          [self.__p13, self.__p14, self.__p15],
                          [self.__p12, self.__p16, self.__p17]])

    def test_make_round_games1(self):
        # Tests the making of a 1-game round
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4])

        round_games = manager._Manager__make_round_games()

        # Make sure we have the right number of games
        self.assertEqual(len(round_games), 1)

        # Make sure each game has the right players in it
        self.assertEqual(round_games[0]._Referee__players, [self.__p1, self.__p2, self.__p3, self.__p4])

    def test_make_round_games2(self):
        # Tests the making of a 5-game round
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4, self.__p5, self.__p6, self.__p7,
                           self.__p8, self.__p9, self.__p10, self.__p11, self.__p12, self.__p13, self.__p14,
                           self.__p15, self.__p16, self.__p17])

        round_games = manager._Manager__make_round_games()

        # Make sure we have the right number of games
        self.assertEqual(len(round_games), 5)

        # Make sure each game has the right players in it
        self.assertEqual(round_games[0]._Referee__players, [self.__p1, self.__p2, self.__p3, self.__p4])
        self.assertEqual(round_games[1]._Referee__players, [self.__p5, self.__p6, self.__p7, self.__p8])
        self.assertEqual(round_games[2]._Referee__players, [self.__p9, self.__p10, self.__p11, self.__p12])
        self.assertEqual(round_games[3]._Referee__players, [self.__p13, self.__p14, self.__p15])
        self.assertEqual(round_games[4]._Referee__players, [self.__p16, self.__p17])

    def test_run_round1(self):
        # Tests the running of a 1-game round
        manager = Manager([self.__p1, self.__p2, self.__p3, self.__p4])

        winners, losers = manager._Manager__run_round()

        # Make sure we have the right number of games
        self.assertEqual(len(winners), 1)
        self.assertCountEqual(winners, [self.__p4])
        # self.assertCountEqual(losers, [self.__p2, self.__p3, self.__p4])
