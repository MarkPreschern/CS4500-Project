import sys
import unittest

sys.path.append('Player/')
sys.path.append('../../Common')

from strategy import Strategy
from action import Action
from board import Board
from color import Color
from player import Player
from position import Position
from state import State
from tile import Tile


class StrategyTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(StrategyTests, self).__init__(*args, **kwargs)

        # Initialize boards
        self.__board1 = Board.homogeneous(5, 10, 3)
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

        # Initialize some players for testing
        self.__p1 = Player(1, "John", 20, Color.RED)
        self.__p2 = Player(2, "George", 21, Color.WHITE)
        self.__p3 = Player(3, "Gary", 22, Color.BLACK)
        self.__p4 = Player(4, "Jeanine", 23, Color.BROWN)
        self.__p5 = Player(5, "Obama", 24, Color.RED)
        self.__p6 = Player(6, "Fred", 32, Color.BROWN)
        self.__p7 = Player(7, "Stewart", 33, Color.WHITE)
        self.__p8 = Player(8, "Bobby Mon", 42, Color.BLACK)
        self.__p9 = Player(9, "Bob Ross", 48, Color.RED)
        self.__p10 = Player(10, "Eric Khart", 52, Color.BROWN)
        self.__p11 = Player(11, "Ionut", 54, Color.RED)

        # ========================== STATE 1 ==========================

        # Initialize a premature state
        self.__state1 = State(self.__board1, [self.__p1, self.__p2, self.__p3, self.__p4])

        # ========================== STATE 2 ==========================

        # Initialize a finalized state where at least two more rounds are possible
        self.__state2 = State(self.__board1, [self.__p1, self.__p2, self.__p3])
        # Place all avatars
        # Player 1 place
        self.__state2.place_avatar(Position(6, 0))
        # Player 2 place
        self.__state2.place_avatar(Position(0, 1))
        # Player 3 place
        self.__state2.place_avatar(Position(2, 2))
        # Player 1 place
        self.__state2.place_avatar(Position(1, 0))
        # Player 2 place
        self.__state2.place_avatar(Position(2, 0))
        # Player 3 place
        self.__state2.place_avatar(Position(3, 2))
        # Player 1 place
        self.__state2.place_avatar(Position(1, 1))
        # Player 2 place
        self.__state2.place_avatar(Position(4, 1))
        # Player 3 place
        self.__state2.place_avatar(Position(3, 0))

    def test_get_best_action_success1(self):
        # Tests successful get_best_action
        self.assertEqual(Strategy.get_best_action(self.__state2, 8),
                         Action(Position(0, 0), Position(1, 0)))
