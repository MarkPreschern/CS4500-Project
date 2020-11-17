import unittest
import sys
from unittest.mock import patch
import random
import string


sys.path.append('Player/')
sys.path.append('Admin/')
sys.path.append('Admin/Other')
sys.path.append('Admin/Other/mocks')
sys.path.append('../../../Common')

from manager import Manager
from player import Player
from referee import Referee
from tournament_update_type import TournamentUpdateType
from failing_winner1 import FailingWinner1
from failing_winner2 import FailingWinner2
from tournament_missing_player import TournamentMissingPlayer


class ManagerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ManagerTests, self).__init__(*args, **kwargs)

        self.__far_sight1 = Player(name='Bob', search_depth=2)
        self.__far_sight2 = Player(name='Bob 2', search_depth=2)
        self.__far_sight3 = Player(name='Bob 3', search_depth=2)

        self.__failing_winner1 = FailingWinner1(name='iFail 1')
        self.__failing_winner2 = FailingWinner2(name='iFail 2')

        # Set seed to add some predictability as to what kind of board
        # the referee is gonna setup
        random.seed(900)

        Referee.DIFFICULTY_FACTOR = 1

    def test_init_fail1(self):
        # Tests failing init due to invalid list of players
        with self.assertRaises(TypeError):
            Manager({'not a list': 'duh'})

    def test_init_fail2(self):
        # Tests failing init due to invalid board_row_no
        with self.assertRaises(TypeError):
            Manager([ self.__far_sight1, self.__far_sight2 ], 'nope')

    def test_init_fail3(self):
        # Tests failing init due to invalid board_col_no
        with self.assertRaises(TypeError):
            Manager([ self.__far_sight1, self.__far_sight2 ], 2, 'nope')

    @staticmethod
    def __make_players(no=0):
        # Makes the specified number of players and returns them
        players = []

        # Make players with random names
        for k in range(no):
            players.append(Player(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))))

        return players

    def test_divide_players1(self):
        # Tests divide_players with too few players
        p1, = ManagerTests.__make_players(1)
        manager = Manager([p1, ])

        self.assertEqual(manager._Manager__divide_players(),
                         [])

    def test_divide_players2(self):
        # Tests a 6 = 4 + 2 player divide
        p1, p2, p3, p4, p5, p6 = ManagerTests.__make_players(6)
        manager = Manager([p1, p2, p3, p4, p5, p6])

        self.assertEqual(manager._Manager__divide_players(),
                         [[p1, p2, p3, p4],
                          [p5, p6]])

    def test_divide_players3(self):
        # Tests a 5 = 3 + 2 player divide
        p1, p2, p3, p4, p5 = ManagerTests.__make_players(5)
        manager = Manager([p1, p2, p3, p4, p5])

        self.assertEqual(manager._Manager__divide_players(),
                         [[p1, p2, p3],
                          [p4, p5]])

    def test_divide_players4(self):
        # Tests a 17 = 4 + 4 + 4 + 3 + 2 player divide
        p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15,\
            p16, p17 = ManagerTests.__make_players(17)
        manager = Manager([p1, p2, p3, p4, p5, p6, p7,
                           p8, p9, p10, p11, p12, p13, p14,
                           p15, p16, p17])

        self.assertEqual(manager._Manager__divide_players(),
                         [[p1, p2, p3, p4],
                          [p5, p6, p7, p8],
                          [p9, p10, p11, p12],
                          [p13, p14, p15],
                          [p16, p17]])

    @patch("constants.MIN_PLAYERS", 3)
    def test_divide_players5(self):
        # Tests a 17 = 4 + 4 + 3 + 3 + 3 player divide with MIN_PLAYERS mocked to 3
        p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15,\
            p16, p17 = ManagerTests.__make_players(17)

        manager = Manager([p1, p2, p3, p4, p5, p6, p7,
                           p8, p9, p10, p11, p12, p13, p14,
                           p15, p16, p17])

        self.assertEqual(manager._Manager__divide_players(),
                         [[p1, p2, p3, p4],
                          [p5, p6, p7, p8],
                          [p9, p10, p11],
                          [p13, p14, p15],
                          [p12, p16, p17]])

    def test_make_round_games1(self):
        # Tests the making of a 1-game round
        p1, p2, p3, p4 = ManagerTests.__make_players(4)

        manager = Manager([p1, p2, p3, p4])

        round_games, _ = manager._Manager__make_round_games()

        # Make sure we have the right number of games
        self.assertEqual(len(round_games), 1)

        # Make sure each game has the right players in it
        self.assertEqual(round_games[0]._Referee__players, [p1, p2, p3, p4])

    def test_make_round_games2(self):
        # Tests the making of a 2-game round
        p1, p2, p3, p4, p5, p6, p7, p8 = ManagerTests.__make_players(8)

        manager = Manager([p1, p2, p3, p4, p5,
                           p6, p7, p8])

        round_games, _ = manager._Manager__make_round_games()

        # Make sure we have the right number of games
        self.assertEqual(len(round_games), 2)

        # Make sure each game has the right players in it
        self.assertEqual(round_games[0]._Referee__players, [p1, p2, p3, p4])
        self.assertEqual(round_games[1]._Referee__players, [p5, p6, p7, p8])

    def test_make_round_games3(self):
        # Tests the making of a 5-game round
        p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15,\
            p16, p17 = ManagerTests.__make_players(17)

        manager = Manager([p1, p2, p3, p4, p5, p6, p7,
                           p8, p9, p10, p11, p12, p13, p14,
                           p15, p16, p17])

        round_games, _ = manager._Manager__make_round_games()

        # Make sure we have the right number of games
        self.assertEqual(len(round_games), 5)

        # Make sure each game has the right players in it
        self.assertEqual(round_games[0]._Referee__players, [p1, p2, p3, p4])
        self.assertEqual(round_games[1]._Referee__players, [p5, p6, p7, p8])
        self.assertEqual(round_games[2]._Referee__players, [p9, p10, p11, p12])
        self.assertEqual(round_games[3]._Referee__players, [p13, p14, p15])
        self.assertEqual(round_games[4]._Referee__players, [p16, p17])

    def test_run_round1(self):
        # Tests the running of a round when there's too few players
        random.seed(900)
        p1, = ManagerTests.__make_players(1)

        manager = Manager([p1])

        winners, losers = manager._Manager__run_round()

        # Assert expectations
        self.assertCountEqual(winners, [])
        self.assertCountEqual(losers, [])

    def test_run_round2(self):
        # Tests the running of a 1-game round
        random.seed(900)
        p1, p2, p3, p4 = ManagerTests.__make_players(4)

        manager = Manager([p1, p2, p3, p4])

        winners, losers = manager._Manager__run_round()

        # Assert expectations
        self.assertEqual(len(winners), 2)
        self.assertCountEqual(winners, [p1, p4])
        self.assertCountEqual(losers, [p2, p3])

    def test_run_round3(self):
        # Tests the running of a 2-game round
        p1, p2, p3, p4, p5, p6, p7, p8 = ManagerTests.__make_players(8)
        random.seed(900)

        manager = Manager([p1, p2, p3, p4, p5,
                           p6, p7, p8])

        winners, losers = manager._Manager__run_round()

        # Assert expectations
        self.assertEqual(len(winners), 2)

        self.assertCountEqual(winners, [p1, p7])
        self.assertCountEqual(losers, [p2, p3, p4, p5, p6, p8])

    def test_run1(self):
        # Tests a 4-player tournament in which only winner emerges after 2 rounds (one with 4 players and the
        # second with 2 players).
        random.seed(32321)
        p1, p2, p3, p4, _ = ManagerTests.__make_players(5)

        # Initialize counter to keep track of the # of updates & payload to expect
        count = 0

        def tournament_update(payload):
            nonlocal count
            if count == 0:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.NEW_ROUND)
                self.assertCountEqual(payload['games'][0], ['5ONLNC2NIJ', 'CGMI071DFB', 'BD9UBXLEG5', 'BX0EZWL7S9'])
            elif count == 1:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.NEW_ROUND)
                self.assertCountEqual(payload['games'][0], ['CGMI071DFB', '5ONLNC2NIJ'])
            else:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.TOURNAMENT_END)
                self.assertCountEqual(payload['winners'], ['5ONLNC2NIJ'])

            count += 1

            # Make sure payload coincides with tournament statistics
            self.assertEqual(manager.get_tournament_statistics(), payload)

        manager = Manager([p1, p2, p3, p4], 6, 6)

        manager.subscribe_tournament_updates(tournament_update)
        manager.run()

        self.assertEqual(manager.tournament_winners, [p1])

    def test_run2(self):
        # Tests a 2-player tournament in which only winner emerges (ends because too few players
        # remain to form another round)
        random.seed(900)
        p1, = ManagerTests.__make_players(1)

        manager = Manager([p1, self.__far_sight1], 4, 4)

        # Initialize counter to keep track of the # of updates & payload to expect
        count = 0

        def tournament_update(payload):
            nonlocal count
            if count < 1:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.NEW_ROUND)
                self.assertCountEqual(payload['games'][0], ['OXGFPVDK2O', 'Bob'])
            else:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.TOURNAMENT_END)
                self.assertCountEqual(payload['winners'], ['Bob'])

            count += 1

            # Make sure payload coincides with tournament statistics
            self.assertEqual(manager.get_tournament_statistics(), payload)

        manager.subscribe_tournament_updates(tournament_update)
        manager.run()

        self.assertEqual(manager.tournament_winners, [self.__far_sight1])

    def test_run3(self):
        # Tests a 2-player tournament which ends because two consecutive rounds
        # have produced the same winner
        random.seed(12312)
        p1, p2, p3 = ManagerTests.__make_players(3)

        # Initialize counter to keep track of the # of updates & payload to expect
        count = 0

        def tournament_update(payload):
            nonlocal count
            if count < 2:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.NEW_ROUND)
                self.assertCountEqual(payload['games'][0], ['A6V797EW9W', 'AYU1SUOBVW', '2ISVDETAGZ'])
            else:
                # Used to validate tournament update sent to observers
                self.assertEqual(payload['type'], TournamentUpdateType.TOURNAMENT_END)
                self.assertCountEqual(payload['winners'], ['A6V797EW9W', 'AYU1SUOBVW', '2ISVDETAGZ'])

            count += 1

            # Make sure payload coincides with tournament statistics
            self.assertEqual(manager.get_tournament_statistics(), payload)

        manager = Manager([p1, p2, p3], 5, 5)
        manager.subscribe_tournament_updates(tournament_update)

        manager.run()

        # Make sure we got the right winners
        self.assertCountEqual(manager.tournament_winners, [p1, p2, p3])

    def test_run4(self):
        # Tests a 2-player tournament with no winners because winner fails to acknowledge
        # that they've won by throwing an exception
        random.seed(12312)
        p1, = ManagerTests.__make_players(1)

        manager = Manager([self.__failing_winner1, p1], 3, 4)
        manager.run()

        # Make sure we got the right winners
        self.assertCountEqual(manager.tournament_winners, [])

    def test_run5(self):
        # Tests a 2-player tournament with no winners because winner fails to acknowledge
        # that they've won by entering an infinite loop
        random.seed(12312)
        p1, = ManagerTests.__make_players(1)

        manager = Manager([self.__failing_winner2, p1], 3, 4)
        manager.run()

        # Make sure we got the right winners
        self.assertCountEqual(manager.tournament_winners, [])

    def test_run_one_player(self):
        # Tests a tournament with a single player
        p1, = ManagerTests.__make_players(1)

        m = Manager([p1])
        m.run()

        # There should not be any winners / losers as no games can be made with one player
        self.assertEqual(m.tournament_winners, [])
        self.assertEqual(m.tournament_losers, [])

    def test_run_player_missing_tournament(self):
        # Tests a tournament wherein a player fails to acknowledge its start
        p1, p2 = ManagerTests.__make_players(2)

        m = Manager([p1, p2, TournamentMissingPlayer('Barney')])
        m.run()

        # Make sure both collections exclude sleepy player :)
        self.assertEqual(m.tournament_winners, [p1, p2])
        self.assertEqual(m.tournament_losers, [])
