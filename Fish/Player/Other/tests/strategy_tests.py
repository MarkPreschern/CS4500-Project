import sys
import unittest


sys.path.append('Player/')
sys.path.append('../../../Common')

from strategy import Strategy
from board import Board
from color import Color
from player import Player
from position import Position
from state import State
from tile import Tile
from constants import VERY_LARGE_NUMBER
from exceptions.GameNotRunningException import GameNotRunningException
from exceptions.InvalidGameStatus import InvalidGameStatus
from game_tree import GameTree
from hole import Hole


class StrategyTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StrategyTests, self).__init__(*args, **kwargs)

        # Initialize boards
        self.__board1 = Board.homogeneous(2, 5, 3)
        self.__board2 = Board.homogeneous(3, 5, 2)
        self.__board3 = Board({
            Position(0, 0): Tile(5),
            Position(0, 1): Tile(3),
            Position(0, 2): Tile(2),
            Position(1, 0): Tile(2),
            Position(1, 1): Tile(3),
            Position(1, 2): Tile(2),
            Position(2, 0): Tile(3),
            Position(2, 1): Tile(4),
            Position(2, 2): Tile(1),
            Position(3, 0): Tile(1),
            Position(3, 1): Tile(1),
            Position(3, 2): Tile(5),
            Position(4, 0): Tile(2),
            Position(4, 1): Tile(3),
            Position(4, 2): Tile(4)
        })

        self.__board4 = Board({
            Position(0, 0): Tile(5),
            Position(0, 1): Tile(3),
            Position(0, 2): Hole(),
            Position(1, 0): Tile(2),
            Position(1, 1): Tile(3),
            Position(1, 2): Hole(),
            Position(2, 0): Hole(),
            Position(2, 1): Tile(4),
            Position(2, 2): Hole(),
            Position(3, 0): Tile(1),
            Position(3, 1): Tile(1),
            Position(3, 2): Tile(5),
            Position(4, 0): Hole(),
            Position(4, 1): Tile(3),
            Position(4, 2): Tile(4)
        })

        # Initialize some players for testing
        self.__p1 = Player(1, "John", Color.RED)
        self.__p2 = Player(2, "George", Color.WHITE)
        self.__p3 = Player(3, "Gary", Color.BLACK)
        self.__p4 = Player(4, "Jeanine", Color.BROWN)
        self.__p5 = Player(5, "Obama", Color.RED)
        self.__p6 = Player(6, "Fred", Color.BROWN)
        self.__p7 = Player(7, "Stewart", Color.WHITE)
        self.__p8 = Player(8, "Bobby Mon", Color.BLACK)
        self.__p9 = Player(9, "Bob Ross", Color.RED)
        self.__p10 = Player(10, "Eric Khart", Color.BROWN)
        self.__p11 = Player(11, "Ionut", Color.BLACK)
        self.__p12 = Player(12, "Bot 1", Color.RED)
        self.__p13 = Player(13, "Bot 2", Color.BROWN)
        self.__p14 = Player(14, "Bot 3", Color.WHITE)
        self.__p15 = Player(15, "Bot X", Color.RED)
        self.__p16 = Player(16, "Bot Y", Color.BROWN)
        self.__p17 = Player(17, "Bot Z", Color.BLACK)
        self.__p18 = Player(18, "Bot W", Color.RED)

        # ========================== STATE 1 ==========================

        # Initialize a premature state
        self.__state1 = State(self.__board1, [self.__p15, self.__p16, self.__p17, self.__p18])

        # ========================== STATE 2 ==========================

        # Initialize a finalized state where at least two more rounds are possible
        self.__state2 = State(self.__board1, [self.__p1, self.__p2, self.__p3])
        # Place all avatars
        # Player 1 place
        self.__state2.place_avatar(1, Position(4, 2))
        # Player 2 place
        self.__state2.place_avatar(2, Position(0, 1))
        # Player 3 place
        self.__state2.place_avatar(3, Position(2, 1))
        # Player 1 place
        self.__state2.place_avatar(1, Position(1, 0))
        # Player 2 place
        self.__state2.place_avatar(2, Position(2, 0))
        # Player 3 place
        self.__state2.place_avatar(3, Position(3, 1))
        # Player 1 place
        self.__state2.place_avatar(1, Position(1, 1))
        # Player 2 place
        self.__state2.place_avatar(2, Position(4, 1))
        # Player 3 place
        self.__state2.place_avatar(3, Position(3, 0))

        # Make up game tree for state 2
        self.__tree2 = GameTree(self.__state2)

        # ========================== STATE 3 ==========================
        # Setup state that is one move away from game over
        self.__state3 = State(self.__board2, players=[
            self.__p5,
            self.__p6,
            self.__p7,
            self.__p8])

        # Player 1
        self.__state3.place_avatar(5, Position(3, 0))
        # Player 2
        self.__state3.place_avatar(6, Position(0, 0))
        # Player 3
        self.__state3.place_avatar(7, Position(1, 0))
        # Player 4
        self.__state3.place_avatar(8, Position(2, 0))
        # Player 1
        self.__state3.place_avatar(5, Position(3, 1))
        # Player 2
        self.__state3.place_avatar(6, Position(0, 1))
        # Player 3
        self.__state3.place_avatar(7, Position(1, 1))
        # Player 4
        self.__state3.place_avatar(8, Position(2, 1))
        # Make move 1 for p1
        self.__state3.move_avatar(Position(3, 1), Position(4, 1))

        # Player 1 has a score of 3 now
        # Make up tree for state 3
        self.__tree3 = GameTree(self.__state3)

        # ========================== STATE 4 ==========================
        # Setup state that is game over
        self.__state4 = self.__state3.deepcopy()

        # Make final move on behalf of Player 4
        self.__state4.move_avatar(Position(2, 0), Position(4, 0))
        # Player 4 has a score of 3 now

        # Make up tree for state 4
        self.__tree4 = GameTree(self.__state4)

        # ========================== STATE 5 ==========================
        # Setup state that includes heterogeneous board
        self.__state5 = State(self.__board3, players=[
            self.__p9,
            self.__p10,
            self.__p11])

        # Player 1
        self.__state5.place_avatar(9, Position(2, 0))
        # Player 2
        self.__state5.place_avatar(10, Position(0, 1))
        # Player 3
        self.__state5.place_avatar(11, Position(0, 2))
        # Player 1
        self.__state5.place_avatar(9, Position(1, 0))
        # Player 2
        self.__state5.place_avatar(10, Position(1, 2))
        # Player 3
        self.__state5.place_avatar(11, Position(0, 0))
        # Player 1
        self.__state5.place_avatar(9, Position(3, 1))
        # Player 2
        self.__state5.place_avatar(10, Position(2, 1))
        # Player 3
        self.__state5.place_avatar(11, Position(3, 2))

        # Make up tree for state 5
        self.__tree5 = GameTree(self.__state5)

        # ========================== STATE 6 ==========================
        # Setup state that includes heterogeneous board riddled with a lot of holes
        # and with no avatars on it
        self.__state6 = State(self.__board4, players=[
            self.__p12,
            self.__p13,
            self.__p14])

    def test_get_best_action_fail1(self):
        # Fails due to invalid state (type-wise)
        with self.assertRaises(TypeError):
            Strategy.get_best_action('', 10)

    def test_get_best_action_fail2(self):
        # Fails due to invalid state (still placing)
        with self.assertRaises(GameNotRunningException):
            Strategy.get_best_action(self.__state1, 10)

    def test_get_best_action_fail3(self):
        # Fails due to invalid depth
        with self.assertRaises(TypeError):
            Strategy.get_best_action(self.__state2, 0)

    def test_get_best_action_success1(self):
        # Tests successful get_best_action with a max depth of 2 (3 players)
        self.assertEqual(Strategy.get_best_action(self.__state2, 1), ((1, 0), (0, 0)))

    def test_get_best_action_success2(self):
        # Tests successful get_best_action with a max depth of 5 (3 players)
        self.assertEqual(Strategy.get_best_action(self.__state2, 5), ((1, 1), (2, 2)))

    def test_get_best_action_success3(self):
        # Tests minimax search on an incipient state and then on the state after a move has
        # been made
        # Get best move for player id 9
        self.assertEqual(Strategy.get_best_action(self.__state5, 2), ((1, 0), (3, 0)))

        self.__state5.move_avatar(Position(1, 0), Position(3, 0))

        # Get best move for player id 10
        self.assertEqual(Strategy.get_best_action(self.__state5, 2), ((0, 1), (2, 2)))

    def test_mini_max_search_fail1(self):
        # Tests failing mini_max_search due to invalid node
        with self.assertRaises(TypeError):
            Strategy._Strategy__mini_max_search('not a node', 1, 2, -VERY_LARGE_NUMBER, VERY_LARGE_NUMBER)

    def test_mini_max_search_fail2(self):
        # Tests failing mini_max_search due to invalid maximizer id
        with self.assertRaises(TypeError):
            Strategy._Strategy__mini_max_search(self.__tree2, -1, 2, -VERY_LARGE_NUMBER, VERY_LARGE_NUMBER)

    def test_mini_max_search_fail3(self):
        # Tests failing mini_max_search due to invalid depth
        with self.assertRaises(TypeError):
            Strategy._Strategy__mini_max_search(self.__tree2, 1, -2, -VERY_LARGE_NUMBER, VERY_LARGE_NUMBER)

    def test_mini_max_search_fail4(self):
        # Tests failing mini_max_search due to invalid alpha
        with self.assertRaises(TypeError):
            Strategy._Strategy__mini_max_search(self.__tree2, 1, 2, 'alpha', VERY_LARGE_NUMBER)

    def test_mini_max_search_fail5(self):
        # Tests failing mini_max_search due to invalid beta
        with self.assertRaises(TypeError):
            Strategy._Strategy__mini_max_search(self.__tree2, 1, 2, -VERY_LARGE_NUMBER, 'beta')

    def test_mini_max_search_success1(self):
        # Tests base case of minimax search with a depth of 0
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree3, 5, 0)[0], 3)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree3, 6, 0)[0], 0)

    def test_mini_max_search_success2(self):
        # Tests base case of minimax search with a positive depth where only one move is
        # possible by Player 4 (id = 8)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree3, 6, 1)[0], 0)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree3, 7, 1)[0], 0)

    def test_mini_max_search_success3(self):
        # Tests base case of minimax search with a positive depth on a game state wherein
        # no more moves are possible
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree4, 5, 1)[0], 3)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree4, 6, 2)[0], 0)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree4, 7, 2)[0], 0)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree4, 8, 2)[0], 3)

    def test_mini_max_search_success4(self):
        # Tests minimax search with a depth of 1 on a game at least 4 levels deep (homogeneous board)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree2, 1, 1), (2, ((1, 0), (0, 0))))

    def test_mini_max_search_success5(self):
        # Tests minimax search with a depth of 4 on a game at least 4 levels deep (homogeneous board)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree2, 1, 4), (8, ((1, 1), (2, 2))))

    def test_mini_max_search_success6(self):
        # Tests minimax search with a depth of 4 on a game at least 2 levels deep (heterogeneous board)
        self.assertEqual(Strategy._Strategy__mini_max_search(self.__tree5, 9, 2), (5, ((1, 0), (3, 0))))

    def test_place_penguin_fail1(self):
        # Tests failing place_penguin due to invalid player_id (type_wise)
        with self.assertRaises(TypeError):
            Strategy.place_penguin('ok', self.__state1)

    def test_place_penguin_fail2(self):
        # Tests failing place_penguin due to invalid state being provided (type-wise)
        with self.assertRaises(TypeError):
            Strategy.place_penguin(1, 'CS4500 is life!')

    def test_place_penguin_fail3(self):
        # Tests failing place_penguin due to invalid state (not in placing phase)
        with self.assertRaises(InvalidGameStatus):
            Strategy.place_penguin(1, self.__state2)

    def test_place_penguin_success1(self):
        # Tests a series of successful place_penguin calls
        self.assertEqual(Strategy.place_penguin(15, self.__state1), (0, 0))
        self.assertTrue((0, 0) in self.__state1.placements[15])

        self.assertEqual(Strategy.place_penguin(16, self.__state1), (0, 1))
        self.assertTrue((0, 1) in self.__state1.placements[16])

        # Place a bunch of avatars
        self.__state1.place_avatar(17, Position(0, 2))
        self.__state1.place_avatar(18, Position(1, 0))
        self.__state1.place_avatar(15, Position(1, 2))
        self.__state1.place_avatar(16, Position(2, 0))

        # Make sure place_penguin dodges the penguins we just manually
        # placed
        self.assertEqual(Strategy.place_penguin(17, self.__state1), (1, 1))
        self.assertTrue((1, 1) in self.__state1.placements[17])

        self.assertEqual(Strategy.place_penguin(18, self.__state1), (2, 1))
        self.assertTrue((2, 1) in self.__state1.placements[18])

    def test_place_penguin_success2(self):
        # Tests a series of successful place_penguin calls on a hole-riddled
        # heterogeneous board

        # p1 place
        self.assertEqual(Strategy.place_penguin(12, self.__state6), (0, 0))
        # p2 place
        self.assertEqual(Strategy.place_penguin(13, self.__state6), (0, 1))
        # p3 place
        self.assertEqual(Strategy.place_penguin(14, self.__state6), (1, 0))
        # p1 place
        self.assertEqual(Strategy.place_penguin(12, self.__state6), (1, 1))
        # p2 place
        self.assertEqual(Strategy.place_penguin(13, self.__state6), (2, 1))
        # p3 place
        self.assertEqual(Strategy.place_penguin(14, self.__state6), (3, 0))
        # p1 place
        self.assertEqual(Strategy.place_penguin(12, self.__state6), (3, 1))
        # p2 place
        self.assertEqual(Strategy.place_penguin(13, self.__state6), (3, 2))
        # p3 place
        self.assertEqual(Strategy.place_penguin(14, self.__state6), (4, 1))

        # Make sure penguins have been placed correctly on behalf of the right players
        self.assertTrue({(0, 0), (1, 1), (3, 1)}.issubset(set(self.__state6.placements[12])))
        self.assertTrue({(0, 1), (2, 1), (3, 2)}.issubset(set(self.__state6.placements[13])))
        self.assertTrue({(1, 0), (3, 0), (4, 1)}.issubset(set(self.__state6.placements[14])))
