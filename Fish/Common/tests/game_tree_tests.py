import copy
import sys
import unittest

from action import Action
from board import Board
from color import Color
from exceptions.GameNotRunningException import GameNotRunningException
from exceptions.InvalidActionException import InvalidActionException
from player import Player
from position import Position
from state import State
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
        self.__p11 = Player(11, "Ionut", Color.RED)

        # ========================== STATE 1 ==========================

        # Initialize a premature state
        self.__state1 = State(self.__board1, [self.__p1, self.__p2, self.__p3, self.__p4])

        # ========================== STATE 2 ==========================

        # Initialize a finalized state where at least two more rounds are possible
        self.__state2 = State(self.__board1, [self.__p1, self.__p2, self.__p3])
        # Place all avatars
        # Player 1 place
        self.__state2.place_avatar(1, Position(4, 0))
        # Player 2 place
        self.__state2.place_avatar(2, Position(0, 1))
        # Player 3 place
        self.__state2.place_avatar(3, Position(2, 2))
        # Player 1 place
        self.__state2.place_avatar(1, Position(1, 0))
        # Player 2 place
        self.__state2.place_avatar(2, Position(2, 0))
        # Player 3 place
        self.__state2.place_avatar(3, Position(3, 2))
        # Player 1 place
        self.__state2.place_avatar(1, Position(1, 1))
        # Player 2 place
        self.__state2.place_avatar(2, Position(4, 1))
        # Player 3 place
        self.__state2.place_avatar(3, Position(3, 0))

        # Make up tree for this state
        self.__tree2 = GameTree(self.__state2)

        # ========================== STATE 3 ==========================
        # Setup state that is one move away from game over
        self.__state3 = State(self.__board2, players=[
            self.__p5,
            self.__p6,
            self.__p7,
            self.__p8])

        # Set up the board with placements s.t. only 2 moves can be made
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

        # Make up tree for this state
        self.__tree3 = GameTree(self.__state3)

        # ========================== STATE 4 ==========================
        # Setup state that is game over
        self.__state4 = copy.deepcopy(self.__state3)

        # Make final move
        self.__state4.move_avatar(Position(2, 0), Position(4, 0))

        # Make up tree for this state
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

        # Make up tree for this state
        self.__tree5 = GameTree(self.__state5)

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
        GameTree(self.__state2)

    def test_get_next1(self):
        # Tests the get_next() of a GameTree where at least two more rounds
        # are possible.
        # It's player 1's turn in the state corresponding to this tree
        self.assertEqual(self.__tree2.state.current_player, 1)

        # Make sure it has generated all possible connecting trees
        self.assertSequenceEqual(self.__state2.get_possible_actions(),
                                 self.__tree2.all_possible_actions)

        # Cycle over child trees, check current player, and check move log to make sure
        # move has been made for the state.
        for action, tree in self.__tree2.get_next():
            # Make sure it's player 2's turn in the state corresponding to this tree
            self.assertEqual(tree.state.current_player, 2)

            # Make sure action was the last action that happened
            self.assertEqual(action, tree.state.move_log[-1])

    def test_get_next2(self):
        # Tests the get_next() out of a GameTree where one more round is possible
        # It's player 4's turn in the state corresponding to this tree
        self.assertEqual(self.__tree3.state.current_player, 8)

        # Make sure it has generated all possible connecting trees
        self.assertSequenceEqual(self.__tree3.all_possible_actions,
                                 [Action(Position(2, 0), Position(4, 0))])

        # Cycle over child trees, check current player, and check move log to make sure
        # move has been made for the state.
        for action, tree in self.__tree3.get_next():
            # Make sure it's player 11's turn in the state corresponding to this tree
            self.assertEqual(tree.state.current_player, 8)

            # Make sure action was the last action that happened
            self.assertEqual(action, tree.state.move_log[-1])

            # Make sure it's game over
            self.assertFalse(tree.state.can_anyone_move())

            # Make sure no more child states are possible for it is game
            # over
            self.assertSequenceEqual(tree.all_possible_actions, [])

    def test_get_next3(self):
        # Tests the get_next() of a GameTree where no more rounds is possible (aka
        # game over state).
        for _, _ in self.__tree4.get_next():
            self.assertTrue(False)

        # Make sure is has not generated any more trees (as there are no more
        # possible moves)
        self.assertSequenceEqual(self.__tree4.all_possible_actions, [])

    def test_get_next4(self):
        # Tests the get_next() out of a GameTree and that of its children
        # It's player 1's turn in the state corresponding to this tree
        self.assertEqual(self.__tree2.state.current_player, 1)

        # Cycle over child trees, check current player, and check move log to make sure
        # move has been made for the state.
        for action1, tree1 in self.__tree2.get_next():
            # Make sure it has generated all possible connecting edges
            self.assertSequenceEqual(tree1.state.get_possible_actions(),
                                     tree1.all_possible_actions)

            for action2, tree2 in self.__tree2.get_next():
                # Make sure it has generated all possible connecting edges for current
                # child tree
                self.assertSequenceEqual(tree2.state.get_possible_actions(),
                                         tree2.all_possible_actions)

                # Make sure it's player 2's turn in the state corresponding to this tree
                self.assertEqual(tree2.state.current_player, 2)

                # Make sure action was the last action that happened
                self.assertEqual(action2, tree2.state.move_log[-1])

    def test_try_action_fail1(self):
        # Tests a failing try_action due to action being invalid (type-wise)
        with self.assertRaises(TypeError):
            self.__tree2.try_action(Position(0, 0), Position(1, 0))

    def test_try_action_fail2(self):
        # Tests a failing try_action due to action being invalid (not accessible via a straight
        # line path)
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(3, 0), Position(0, 0)))

    def test_try_action_fail3(self):
        # Tests a failing try_action due to action being out of turn (it involves moving someone
        # else but the current player's avatar, despite otherwise being legal)
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(0, 1), Position(2, 1)))

    def test_try_action_fail4(self):
        # Tests a failing try_action due to action involves moving thru another character
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(4, 0), Position(2, 1)))

    def test_try_action_fail5(self):
        # Tests a failing try_action due to action involves moving to an already occupied tile
        with self.assertRaises(InvalidActionException):
            GameTree.try_action(GameTree(self.__state2), Action(Position(4, 0), Position(3, 0)))

    def test_try_action_success(self):
        # Tests a successful try_action where a valid action gets executed
        valid_action = Action(Position(1, 0), Position(4, 2))
        new_state = self.__tree2.try_action(valid_action)

        # Make sure the valid action we gave it got executed and is at the top
        # of the move log
        self.assertEqual(valid_action, new_state.move_log[-1])
        # Make sure it's second player's turn now
        self.assertEqual(new_state.current_player, 2)

    def test_apply_to_child_states_fail1(self):
        # Tests apply_to_child_states failing due to invalid function (type-wise)
        with self.assertRaises(TypeError):
            self.__tree2.apply_to_child_states(lambda state, _: state)

    def test_apply_to_child_states_success1(self):
        # Tests successful apply_to_child_states where each child state maps to
        # that state's current player
        result = GameTree.apply_to_child_states(GameTree(self.__state2), lambda state: state.current_player)

        # Resulting array should consist of the next player's id the same number of times
        # as there are reachable states
        self.assertSequenceEqual(result, [2, 2, 2, 2, 2, 2, 2])

    def test_apply_to_child_states_success2(self):
        # Tests successful apply_to_child_states where each child state maps to
        # that a given player's score (homogeneous board)
        result = GameTree.apply_to_child_states(GameTree(self.__state2), lambda state: state.get_player_score(1))

        # Score should be the same (5) all around since this is a homogeneous board with
        # 5 fish to each tile
        self.assertSequenceEqual(result, 7 * [5])

    def test_apply_to_child_states_success3(self):
        # Tests successful apply_to_child_states where each child state maps to
        # that a given player's score (heterogeneous board)
        result = GameTree.apply_to_child_states(GameTree(self.__state5), lambda state: state.get_player_score(9))

        self.assertSequenceEqual(result, [3, 3, 3, 2, 1, 1, 1, 1])
