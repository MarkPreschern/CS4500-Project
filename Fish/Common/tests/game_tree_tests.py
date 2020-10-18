import unittest
import sys

from action import Action
from board import Board
from color import Color
from game_status import GameStatus
from player import Player
from position import Position
from state import State
from exceptions.GameNotRunningException import GameNotRunningException

sys.path.append('Common/')

from game_tree import GameTree


class GameTreeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTreeTests, self).__init__(*args, **kwargs)

        # Initialize boards
        self.__board1 = Board.homogeneous(2, 5, 3)
        self.__board2 = Board.homogeneous(3, 5, 2)

        # Initialize some players for testing
        self.__p1 = Player(1, "John", 20, Color.RED)
        self.__p2 = Player(2, "George", 21, Color.WHITE)
        self.__p3 = Player(3, "Gary", 22, Color.BLACK)
        self.__p4 = Player(4, "Jeanine", 23, Color.BROWN)
        self.__p5 = Player(5, "Jen", 22, Color.RED)

        # Initialize a premature state
        self.__state1 = State(self.__board1, [self.__p1, self.__p2, self.__p3, self.__p4])
        # Initialize a finalized state where at least two more rounds are possible
        self.__state2 = State(self.__board1, [self.__p1, self.__p2, self.__p3])
        # Place all avatars
        # Player 1 place
        self.__state2.place_avatar(Position(4, 0))
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

        # Setup state that is one move away from game over
        self.__state3 = State(self.__board2, players=[
            self.__p1,
            self.__p2,
            self.__p3,
            self.__p4])

        # Set up the board with placements s.t. only 2 moves can be made
        # Player 1
        self.__state3.place_avatar(Position(3, 0))
        # Player 2
        self.__state3.place_avatar(Position(0, 0))
        # Player 3
        self.__state3.place_avatar(Position(1, 0))
        # Player 4
        self.__state3.place_avatar(Position(2, 0))
        # Player 1
        self.__state3.place_avatar(Position(3, 1))
        # Player 2
        self.__state3.place_avatar(Position(0, 1))
        # Player 3
        self.__state3.place_avatar(Position(1, 1))
        # Player 4
        self.__state3.place_avatar(Position(2, 1))
        # Make move 1 for p1
        self.__state3.move_avatar(Position(3, 1), Position(4, 1))

    def test_init_fail1(self):
        # Tests failing constructor due to an invalid state
        with self.assertRaises(TypeError):
            GameTree("mickey mouse")

    def test_init_fail2(self):
        # Tests failing constructor due to state not being 'started' (or due
        # to not everyone having placed their avatars).
        with self.assertRaises(GameNotRunningException):
            GameTree(self.__state1)

    def test_init_success(self):
        # Tests successful game tree constructor
        game_tree = GameTree(self.__state2)

        # Tests properties
        self.assertEqual(game_tree.state, self.__state2)
        self.assertEqual(game_tree.children, {})

    def test_flesh_out1(self):
        # Tests the fleshing out of a GameTree where at least two more rounds
        # are possible.
        game_tree = GameTree(self.__state2)
        # Flesh out tree
        game_tree.flesh_out()
        # It's player 1's turn in the state corresponding to this tree
        self.assertEqual(game_tree.state.current_player, 1)

        # Make sure it has generated all possible connecting trees
        self.assertSequenceEqual(self.__state2.get_possible_actions(),
                                 list(game_tree.children.keys()))

        # Cycle over child trees, check current player, and check move log to make sure
        # move has been made for the state.
        for action, tree in game_tree.children.items():
            # Make sure it's player 2's turn in the state corresponding to this tree
            self.assertEqual(tree.state.current_player, 2)

            # Make sure action was the last action that happened
            self.assertEqual(action, tree.state.move_log[-1])

    def test_flesh_out2(self):
        # Tests the fleshing out of a GameTree where no more rounds are possible
        game_tree = GameTree(self.__state3)
        # Flesh out tree
        game_tree.flesh_out()
        # It's player 4's turn in the state corresponding to this tree
        self.assertEqual(game_tree.state.current_player, 4)

        # Make sure it has generated all possible connecting trees
        self.assertSequenceEqual(self.__state3.get_possible_actions(),
                                 [Action(Position(2, 0), Position(4, 0))])

        # Cycle over child trees, check current player, and check move log to make sure
        # move has been made for the state.
        for action, tree in game_tree.children.items():
            # Make sure it's player 4's turn in the state corresponding to this tree
            self.assertEqual(tree.state.current_player, 4)

            # Make sure action was the last action that happened
            self.assertEqual(action, tree.state.move_log[-1])

            # Make sure it's game over
            self.assertEqual(tree.state.game_status, GameStatus.OVER)

            # Flesh out child tree
            tree.flesh_out()

            # Make sure no more child states are possible for it is game
            # over
            self.assertSequenceEqual(tree.children, [])
