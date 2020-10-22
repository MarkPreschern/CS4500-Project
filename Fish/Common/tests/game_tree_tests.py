import copy
import unittest
import sys

from action import Action
from board import Board
from color import Color
from exceptions.InvalidActionException import InvalidActionException
from game_status import GameStatus
from hole import Hole
from player import Player
from position import Position
from state import State
from exceptions.GameNotRunningException import GameNotRunningException
from tile import Tile

sys.path.append('Common/')

from game_tree import GameTree


class GameTreeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTreeTests, self).__init__(*args, **kwargs)

        # Initialize boards
        self.__board1 = Board.homogeneous(5, 5, 3)
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

        # ========================== STATE 3 ==========================
        # Setup state that is one move away from game over
        self.__state3 = State(self.__board2, players=[
            self.__p5,
            self.__p6,
            self.__p7,
            self.__p8])

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

        # ========================== STATE 4 ==========================
        # Setup state that is game over
        self.__state4 = copy.deepcopy(self.__state3)

        # Make final move
        self.__state4.move_avatar(Position(2, 0), Position(4, 0))

        # ========================== STATE 5 ==========================
        # Setup state that includes heterogeneous board
        self.__state5 = State(self.__board3, players=[
            self.__p9,
            self.__p10,
            self.__p11])

        # Player 1
        self.__state5.place_avatar(Position(2, 0))
        # Player 2
        self.__state5.place_avatar(Position(0, 1))
        # Player 3
        self.__state5.place_avatar(Position(0, 2))
        # Player 1
        self.__state5.place_avatar(Position(1, 0))
        # Player 2
        self.__state5.place_avatar(Position(1, 2))
        # Player 3
        self.__state5.place_avatar(Position(0, 0))
        # Player 1
        self.__state5.place_avatar(Position(3, 1))
        # Player 2
        self.__state5.place_avatar(Position(2, 1))
        # Player 3
        self.__state5.place_avatar(Position(3, 2))

        """
                self.__board3 = Board({
            Position(0, 0): Tile(5),
            Position(0, 1): Tile(3),
            Position(0, 2): Tile(2),
            Position(1, 0): Tile(2),
            Position(1, 1): Hole(),
            Position(1, 2): Tile(2),
            Position(2, 0): Tile(3),
            Position(2, 1): Tile(4),
            Position(2, 2): Hole(),
            Position(3, 0): Tile(1),
            Position(3, 1): Tile(1),
            Position(3, 2): Tile(5)
        })
        """

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
        # Tests the fleshing out of a GameTree where one more round is possible
        game_tree = GameTree(self.__state3)
        # Flesh out tree
        game_tree.flesh_out()
        # It's player 4's turn in the state corresponding to this tree
        self.assertEqual(game_tree.state.current_player, 8)

        # Make sure it has generated all possible connecting trees
        self.assertSequenceEqual(list(game_tree.children.keys()),
                                 [Action(Position(2, 0), Position(4, 0))])

        # Cycle over child trees, check current player, and check move log to make sure
        # move has been made for the state.
        for action, tree in game_tree.children.items():
            # Make sure it's player 11's turn in the state corresponding to this tree
            self.assertEqual(tree.state.current_player, 8)

            # Make sure action was the last action that happened
            self.assertEqual(action, tree.state.move_log[-1])

            # Make sure it's game over
            self.assertEqual(tree.state.game_status, GameStatus.OVER)

            # Flesh out child tree
            tree.flesh_out()

            # Make sure no more child states are possible for it is game
            # over
            self.assertSequenceEqual(tree.children, [])

    def test_flesh_out3(self):
        # Tests the fleshing out of a GameTree where no more rounds is possible (aka
        # game over state).
        game_tree = GameTree(self.__state4)
        # Flesh out tree
        game_tree.flesh_out()

        # Make sure is has not generated any more trees (as there are no more
        # possible moves)
        self.assertSequenceEqual(game_tree.children, {})

    def test_flesh_out4(self):
        # Tests the fleshing out of a GameTree and that of its children
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
            # Flesh out current child tree
            tree.flesh_out()

            # Make sure it has generated all possible connecting trees for current
            # child tree
            self.assertSequenceEqual(tree.state.get_possible_actions(),
                                     list(tree.children.keys()))

            # Make sure it's player 2's turn in the state corresponding to this tree
            self.assertEqual(tree.state.current_player, 2)

            # Make sure action was the last action that happened
            self.assertEqual(action, tree.state.move_log[-1])

    def test_try_action_fail1(self):
        # Tests a failing try_action due to state being invalid (type-wise)
        with self.assertRaises(TypeError):
            GameTree.try_action('not a real state', Action(Position(0, 0), Position(1, 0)))

    def test_try_action_fail2(self):
        # Tests a failing try_action due to action being invalid (type-wise)
        with self.assertRaises(TypeError):
            GameTree.try_action(self.__state2, (Position(0, 0), Position(1, 0)))

    def test_try_action_fail3(self):
        # Tests a failing try_action due to action being invalid (not accessible via a straight
        # line path)
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(3, 0), Position(0, 0)))

    def test_try_action_fail4(self):
        # Tests a failing try_action due to action being out of turn (it involves moving someone
        # else but the current player's avatar, despite otherwise being legal)
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(0, 1), Position(2, 1)))

    def test_try_action_fail5(self):
        # Tests a failing try_action due to action involves moving thru another character
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(4, 0), Position(2, 1)))

    def test_try_action_fail6(self):
        # Tests a failing try_action due to action involves moving to an already occupied tile
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(4, 0), Position(3, 0)))

    def test_try_action_success(self):
        # Tests a successful try_action where a valid action gets executed
        valid_action = Action(Position(1, 0), Position(4, 2))
        new_state = GameTree.try_action(GameTree(self.__state2), valid_action)

        # Make sure the valid action we gave it got executed and is at the top
        # of the move log
        self.assertEqual(valid_action, new_state.move_log[-1])
        # Make sure it's second player's turn now
        self.assertEqual(new_state.current_player, 2)

    def test_apply_to_child_states_fail1(self):
        # Tests apply_to_child_states failing due to invalid state (type-wise)
        with self.assertRaises(TypeError):
            GameTree.apply_to_child_states('not a real state', lambda _: 1)

    def test_apply_to_child_states_fail2(self):
        # Tests apply_to_child_states failing due to invalid underlying state (game is not running)
        with self.assertRaises(GameNotRunningException):
            GameTree.apply_to_child_states(GameTree(self.__state1), lambda _: 1)

    def test_apply_to_child_states_fail3(self):
        # Tests apply_to_child_states failing due to invalid function (type-wise)
        with self.assertRaises(TypeError):
            GameTree.apply_to_child_states(GameTree(self.__state2), lambda state, _: state)

    def test_apply_to_child_states_successful1(self):
        # Tests successful apply_to_child_states where each child state maps to
        # that state's current player
        result = GameTree.apply_to_child_states(GameTree(self.__state2), lambda state: state.current_player)

        # Resulting array should consist of the next player's id the same number of times
        # as there are reachable states
        self.assertSequenceEqual(result, [2, 2, 2, 2, 2, 2, 2])

    def test_apply_to_child_states_successful2(self):
        # Tests successful apply_to_child_states where each child state maps to
        # that a given player's score (homogeneous board)
        result = GameTree.apply_to_child_states(GameTree(self.__state2), lambda state: state.get_player_score(1))

        # Score should be the same (5) all around since this is a homogeneous board with
        # 5 fish to each tile
        self.assertSequenceEqual(result, 7 * [5])

    def test_apply_to_child_states_successful3(self):
        # Tests successful apply_to_child_states where each child state maps to
        # that a given player's score (heterogeneous board)
        result = GameTree.apply_to_child_states(GameTree(self.__state5), lambda state: state.get_player_score(9))

        self.assertSequenceEqual(result, [3, 3, 3, 2, 1, 1, 1, 1])
