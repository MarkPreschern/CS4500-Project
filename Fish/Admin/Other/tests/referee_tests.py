import unittest
import sys
import random

sys.path.append('Player/')
sys.path.append('Admin/')
sys.path.append('Admin/Other')
sys.path.append('Admin/Other/mocks')
sys.path.append('../../../Common')

from referee import Referee
from player import Player
from color import Color
from position import Position
from state import State
from cheating_player1 import CheatingPlayer1
from cheating_player2 import CheatingPlayer2
from cheating_player3 import CheatingPlayer3
from cheating_player4 import CheatingPlayer4
from failing_player1 import FailingPlayer1
from failing_player2 import FailingPlayer2
from failing_player3 import FailingPlayer3
from failing_player4 import FailingPlayer4
from failing_player5 import FailingPlayer5
from failing_player6 import FailingPlayer6
from unittest.mock import patch


class RefereeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RefereeTests, self).__init__(*args, **kwargs)
        # Make depth one to keep run time to a minimum
        Player.SEARCH_DEPTH = 1

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

        # Make up player that cheats in placing
        self.__cheating_player1 = CheatingPlayer1('iCrack :P')
        # Make up player that cheats by moving outside the bounds of the board
        self.__cheating_player2 = CheatingPlayer2('iCrack v2')
        # Make up player that cheats by moving in place
        self.__cheating_player3 = CheatingPlayer3('iCrack v3')
        # Make up another player that cheats by moving in place
        self.__cheating_player4 = CheatingPlayer3('iCrack v3')
        # Make up another player that cheats by moving its first avatar
        # to one of its other avatars
        self.__cheating_player5 = CheatingPlayer4('iCrack v4')

        # Make up plaer that fails in placing
        self.__failing_player1 = FailingPlayer1('iFail v1')
        # Make up player that fails in making a move / action
        self.__failing_player2 = FailingPlayer2('iFail v2')
        # Make up another player that fails in making a move / action
        self.__failing_player3 = FailingPlayer2('iFail v2')
        # Make up another player that enters an infinite loop in making a move / action
        self.__failing_player4 = FailingPlayer3('iFail v3')
        # Make up another player throws an exception in making a move / action
        self.__failing_player5 = FailingPlayer4('iFail v4')
        # Make up another player that enters an infinite loop in making a placement
        self.__failing_player6 = FailingPlayer5('iFail v5')
        # Make up another player throws an exception in making a placement
        self.__failing_player7 = FailingPlayer6('iFail v6')

        # Set seed to add some predictability as to what kind of board
        # the referee is gonna setup
        random.seed(900)

        Referee.DIFFICULTY_FACTOR = 1

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

    def test_init_fail8(self):
        # Tests failing init due to improper fish number 0
        with self.assertRaises(ValueError):
            Referee(5, 5, [self.__p1, self.__p2, self.__p3, self.__p4], 0)

    def test_init_fail10(self):
        # Tests failing init due to improper fish number 6
        with self.assertRaises(ValueError):
            Referee(5, 5, [self.__p1, self.__p2, self.__p3, self.__p4], 6)


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
        # Tests successful 2-player game in which everybody plays by
        # the rules and uses the strategy laid out in Strategy
        referee = Referee(4, 3, [self.__p1, self.__p2])

        # Make up observer callback to validate game report
        def game_report_observer(report: dict):
            self.assertEqual(report['cheating_players'], [])
            self.assertEqual(report['failing_players'], [])

            # All players should have the same score
            self.assertEqual(report['leaderboard'],
                             [
                                 {
                                     'name': 'Jim',
                                     'color': Color.WHITE,
                                     'score': 4
                                 },
                                 {
                                     'name': 'Bob',
                                     'color': Color.RED,
                                     'score': 2
                                 }
                             ])

        expected_placements = [
            {
                Color.RED: [Position(0, 0)],
                Color.WHITE: []
            },
            {
                Color.RED: [Position(0, 0)],
                Color.WHITE: [Position(0, 1)]
            },
            {
                Color.RED: [Position(0, 0), Position(0, 2)],
                Color.WHITE: [Position(0, 1)]
            },
            {
                Color.RED: [Position(0, 0), Position(0, 2)],
                Color.WHITE: [Position(0, 1), Position(1, 0)]
            },
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(1, 1)],
                Color.WHITE: [Position(0, 1), Position(1, 0)]
            },
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(1, 1)],
                Color.WHITE: [Position(0, 1), Position(1, 0), Position(1, 2)]
            },
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0)],
                Color.WHITE: [Position(0, 1), Position(1, 0), Position(1, 2)]
            },
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(1, 1), Position(2, 0)],
                Color.WHITE: [Position(0, 1), Position(1, 0), Position(1, 2), Position(2, 2)]
            },
            # (1 1) -> (3 1)
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(3, 1), Position(2, 0)],
                Color.WHITE: [Position(0, 1), Position(1, 0), Position(1, 2), Position(2, 2)]
            },
            # (1 0) -> (3 0)
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(3, 1), Position(2, 0)],
                Color.WHITE: [Position(0, 1), Position(3, 0), Position(1, 2), Position(2, 2)]
            },
            # (1 2) -> (3 2)
            {
                Color.RED: [Position(0, 0), Position(0, 2), Position(3, 1), Position(2, 0)],
                Color.WHITE: [Position(0, 1), Position(3, 0), Position(3, 2), Position(2, 2)]
            }
        ]

        # Initialize running counter to keep track of where we are in the expected
        # placement array
        count = 0

        def game_update_observer(state: State):
            nonlocal count

            self.assertEqual(state.placements, expected_placements[count])
            count += 1

        referee.subscribe_final_game_report(game_report_observer)
        referee.subscribe_game_updates(game_update_observer)
        referee.start()

        self.assertTrue(referee.started)
        self.assertCountEqual(referee.winners, [self.__p2])

    def test_start_success2(self):
        # Tests a game in which a player cheats by making an illegal placement
        referee = Referee(4, 4, [self.__p3, self.__p4, self.__cheating_player1])

        # Make up observer callback to validate game report
        def game_report_observer(report: dict):
            self.assertEqual(report['cheating_players'], [
                self.__cheating_player1
            ])
            self.assertEqual(report['failing_players'], [])

            # All players should have the same score
            self.assertEqual(report['leaderboard'],
                             [
                                 {
                                     'name': 'Elon',
                                     'color': Color.WHITE,
                                     'score': 15
                                 },
                                 {
                                     'name': 'Marley',
                                     'color': Color.RED,
                                     'score': 12
                                 }
                             ])

        referee.subscribe_final_game_report(game_report_observer)
        referee.start()
        self.assertEqual(referee.winners, [self.__p4])

    def test_start_success3(self):
        # Tests a game in which a player cheats by making an illegal action (moving in place)
        referee = Referee(3, 4, [self.__p6, self.__cheating_player3])

        # Make up observer callback to validate game report
        def game_report_observer(report: dict):
            self.assertEqual(report['cheating_players'], [
                self.__cheating_player3
            ])
            self.assertEqual(report['failing_players'], [])

            self.assertEqual(report['leaderboard'],
                             [
                                 {
                                     'name': 'Roger Dodger',
                                     'color': Color.RED,
                                     'score': 12
                                 }
                             ])

        referee.subscribe_final_game_report(game_report_observer)
        referee.start()
        self.assertEqual(referee.winners, [self.__p6])

    def test_start_success4(self):
        # Tests a game in which a player cheats by making an illegal action
        # (moving outside the bounds of the board) and another player cheats
        # by moving in place
        referee = Referee(3, 4, [self.__p7, self.__p8, self.__cheating_player4,
                                 self.__cheating_player2])

        # Make up observer callback to validate game report
        def game_report_observer(report: dict):
            self.assertEqual(report['cheating_players'], [
                self.__cheating_player4, self.__cheating_player2
            ])
            self.assertEqual(report['failing_players'], [])

            # All players should have the same score
            self.assertEqual(report['leaderboard'],
                             [
                                 {
                                     'name': 'Sam',
                                     'color': Color.WHITE,
                                     'score': 6
                                 },
                                 {
                                     'name': 'Nathan',
                                     'color': Color.RED,
                                     'score': 6
                                 }
                             ])

        referee.subscribe_final_game_report(game_report_observer)
        referee.start()
        self.assertCountEqual(referee.winners, [self.__p7, self.__p8])

    def test_start_success5(self):
        # Tests a game in which a player fails to make a placement

        referee = Referee(3, 4, [self.__p9, self.__p10, self.__failing_player1])

        # Make up observer callback to validate game report
        def game_report_observer(report: dict):
            self.assertEqual(report['cheating_players'], [])
            self.assertEqual(report['failing_players'], [
                self.__failing_player1
            ])

            # All players should have the same score
            self.assertEqual(report['leaderboard'],
                             [
                                 {
                                     'name': 'Doug',
                                     'color': Color.RED,
                                     'score': 6
                                 },
                                 {
                                     'name': 'Sebastian',
                                     'color': Color.WHITE,
                                     'score': 4
                                 }
                             ])

        referee.subscribe_final_game_report(game_report_observer)
        referee.start()
        self.assertCountEqual(referee.winners, [self.__p9])

    def test_start_success6(self):
        # Tests a game in which a player fails to make a move
        referee = Referee(3, 4, [self.__p11, self.__failing_player2, self.__p12])

        # Make up observer callback to validate game report
        def game_report_observer(report: dict):
            self.assertEqual(report['cheating_players'], [])
            self.assertEqual(report['failing_players'], [
                self.__failing_player2
            ])

            # All players should have the same score
            self.assertEqual(report['leaderboard'],
                             [
                                 {
                                     'name': 'iHaxor',
                                     'color': Color.RED,
                                     'score': 12
                                 },
                                 {
                                     'name': 'Razorsharp',
                                     'color': Color.BROWN,
                                     'score': 8
                                 }
                             ])

        referee.subscribe_final_game_report(game_report_observer)
        referee.start()
        self.assertCountEqual(referee.winners, [self.__p11])

    def test_start_success7(self):
        # Tests a game in which a player cheats (by trying to move its first avatar to its second
        # avatar) and another player fails to make a move
        referee = Referee(3, 4, [self.__p13, self.__failing_player3, self.__cheating_player5])

        with patch.object(self.__p13, 'game_over') as mock:
            # Make up observer callback to validate game report
            def game_report_observer(report: dict):
                self.assertEqual(report['cheating_players'], [
                    self.__cheating_player5
                ])
                self.assertEqual(report['failing_players'], [
                    self.__failing_player3
                ])

                # All players should have the same score
                self.assertEqual(report['leaderboard'],
                                 [
                                     {
                                         'name': 'Sony',
                                         'color': Color.RED,
                                         'score': 12
                                     }
                                 ])

                # Make sure game_over was called on the players
                mock.assert_called_with(report['leaderboard'], report['cheating_players'],
                                        report['failing_players'])

            referee.subscribe_final_game_report(game_report_observer)
            referee.start()
            self.assertCountEqual(referee.winners, [self.__p13])

    def test_start_success_move_timeout(self):
        # Tests a game in which a player times out in making a move
        referee = Referee(3, 4, [self.__p14, self.__failing_player4])

        with patch.object(self.__p14, 'game_over') as mock:
            # Make up observer callback to validate game report
            def game_report_observer(report: dict):
                self.assertEqual(report['cheating_players'], [
                ])
                self.assertEqual(report['failing_players'], [
                    self.__failing_player4
                ])

                # All players should have the same score
                self.assertEqual(report['leaderboard'],
                                 [
                                     {
                                         'name': 'Sony 2',
                                         'color': Color.RED,
                                         'score': 24
                                     }
                                 ])

                # Make sure game_over was called on the players
                mock.assert_called_with(report['leaderboard'], report['cheating_players'],
                                        report['failing_players'])

            referee.subscribe_final_game_report(game_report_observer)
            referee.start()
            self.assertCountEqual(referee.winners, [self.__p14])

    def test_start_success_move_exception(self):
        # Tests a game in which a player throws an Exception in making a move
        referee = Referee(3, 4, [self.__p15, self.__failing_player5])

        with patch.object(self.__p15, 'game_over') as mock:
            # Make up observer callback to validate game report
            def game_report_observer(report: dict):
                self.assertEqual(report['cheating_players'], [
                ])
                self.assertEqual(report['failing_players'], [
                    self.__failing_player5
                ])

                # All players should have the same score
                self.assertEqual(report['leaderboard'],
                                 [
                                     {
                                         'name': 'Sony 3',
                                         'color': Color.RED,
                                         'score': 28
                                     }
                                 ])

                # Make sure game_over was called on the players
                mock.assert_called_with(report['leaderboard'], report['cheating_players'],
                                        report['failing_players'])

            referee.subscribe_final_game_report(game_report_observer)
            referee.start()
            self.assertCountEqual(referee.winners, [self.__p15])

    def test_start_success_placement_timeout(self):
        # Tests a game in which a player times out in making a placement
        referee = Referee(3, 4, [self.__p16, self.__failing_player6])

        with patch.object(self.__p16, 'game_over') as mock:
            # Make up observer callback to validate game report
            def game_report_observer(report: dict):
                self.assertEqual(report['cheating_players'], [
                ])
                self.assertEqual(report['failing_players'], [
                    self.__failing_player6
                ])

                # All players should have the same score
                self.assertEqual(report['leaderboard'],
                                 [
                                     {
                                         'name': 'Sony 4',
                                         'color': Color.RED,
                                         'score': 28
                                     }
                                 ])

                # Make sure game_over was called on the players
                mock.assert_called_with(report['leaderboard'], report['cheating_players'],
                                        report['failing_players'])

            referee.subscribe_final_game_report(game_report_observer)
            referee.start()
            self.assertCountEqual(referee.winners, [self.__p16])

    def test_start_success_placement_exception(self):
        # Tests a game in which a player throws an Exception in making a placement
        referee = Referee(3, 4, [self.__p17, self.__failing_player7])

        with patch.object(self.__p17, 'game_over') as mock:
            # Make up observer callback to validate game report
            def game_report_observer(report: dict):
                self.assertEqual(report['cheating_players'], [
                ])
                self.assertEqual(report['failing_players'], [
                    self.__failing_player7
                ])

                # All players should have the same score
                self.assertEqual(report['leaderboard'],
                                 [
                                     {
                                         'name': 'Sony 5',
                                         'color': Color.RED,
                                         'score': 7
                                     }
                                 ])

                # Make sure game_over was called on the players
                mock.assert_called_with(report['leaderboard'], report['cheating_players'],
                                        report['failing_players'])

            referee.subscribe_final_game_report(game_report_observer)
            referee.start()
            self.assertCountEqual(referee.winners, [self.__p17])
