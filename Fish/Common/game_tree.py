import pickle

from action import Action
from exceptions.GameNotRunningException import GameNotRunningException
from exceptions.InvalidActionException import InvalidActionException
from game_status import GameStatus
from state import State


class GameTree(object):
    """
    INTERPRETATION: Represents an entire game starting from a given state wherein no more
    avatars will be placed. It is generated from a state and can maintain connections to
    subsequent game states by way of other GameTree(s).

    PURPOSE: The representation can be used by the players and the referee to check rules and
    plan their next moves.

    DEFINITION(S): A a GameTree node is simply a GameTree with child GameTrees attached to it.

    The structure follows a lazy, generative design meaning that adjacent trees are not connected
    until there is an explicit "need".
    """
    DEBUG = False

    def __init__(self, state: State):
        """
        Initializes a barren GameTree with the given state. A complete
        tree is not generated until flesh_out() is called, however. This
        constructor solely returns a new GameTree that incorporates
        a reference to the given game state.

        :param state: State object to based game tree off of
        :return: resulting GameTree object
        """
        # Validate state
        if not isinstance(state, State):
            raise TypeError('Expected State object for state!')

        # Initialize state
        self.__state = state

        # Make sure the state is one in which everyone has finished
        # placing their penguins
        if self.__state.game_status == GameStatus.PLACING:
            raise GameNotRunningException()

        # Initialize dictionary of Action objects to GameTree objects (nodes).
        # to hold subsequent game trees.
        self.__children = {}

        # Set flag to indicate whether game tree has been fleshed out
        self.__fleshed_out = False

        # Get all possible actions for this tree's underlying state. It only includes
        # actions that can be performed by the current player and that are legal
        # under the rules of Fish.
        self.__all_possible_moves = self.__state.get_possible_actions()

    @property
    def children(self):
        """
        Returns a list of all GameTrees that derive from this GameTree.
        """
        return self.__children

    @property
    def state(self) -> State:
        """
        Returns a copy of the GameState that the tree is based off of.
        """
        return pickle.loads(pickle.dumps(self.__state))

    def get_next(self):
        """
        Lazily returns the node's next child node by generating it
        when the returned iterable is iterated over. If no more children exist,
        None is returned.

        :return: child GameTree object or None
        """

        # Cycle over all possible moves from this node
        for move in self.__all_possible_moves:
            # Make a copy of the state
            subsequent_state: State = pickle.loads(pickle.dumps(self.__state))

            current_player_id = subsequent_state.current_player

            if GameTree.DEBUG:
                print(
                    f'[avatar: {current_player_id}] [score:'
                    f' {subsequent_state.get_player_score(current_player_id)}]'
                    f' [move: {[move.src.x, move.src.y, move.dst.x, move.dst.y]}]')

            # Get move to make
            src, dst = move
            # Make move
            subsequent_state.move_avatar(src, dst)

            score = subsequent_state.get_player_score(current_player_id)

            if GameTree.DEBUG:
                print(f'after moving avatar {current_player_id} with score of {score}')

                if score >= 10:
                    print(subsequent_state.move_log)

            # Yield next node
            yield move, GameTree(subsequent_state)

    def flesh_out(self):
        """
        Fleshes out the GameTree by connecting it to game trees for
        all the subsequent game states that can be derived from this
        tree's game state.

        :return: resulting GameTree object
        """
        # Make sure it hasn't been already fleshed out
        if self.__fleshed_out:
            return

        # Set children
        for action in self.__all_possible_moves:
            # De-multiplex action into position tuples
            src, dst = action

            # Create subsequent game state after this move is made
            subsequent_state: State = pickle.loads(pickle.dumps(self.__state))
            subsequent_state.move_avatar(src, dst)

            self.__children.update({action: GameTree(subsequent_state)})

        # Set flag
        self.__fleshed_out = True

    @classmethod
    def try_action(cls, node: 'GameTree', action: Action) -> State:
        """
        Tries to perform the given action or fails on the provided GameTree
        node. If successful, the function returns the resulting state from
        performing provided action, otherwise it throws an InvalidActionException().

        :param node: game tree node to try action on
        :param action: Action object representing move to make
        :return: resulting game state
        """
        # Validate parameters
        if not isinstance(node, GameTree):
            raise TypeError('Expected GameTree object for node!')

        if not isinstance(action, Action):
            raise TypeError('Expected a Action object for action!')

        # Flesh out said game tree
        node.flesh_out()

        # Check if given action is among those possible
        # for said game tree
        if action in node.children.keys():
            # Retrieve game tree that can be arrived at
            # by performing the given move
            tree: GameTree = node.children.get(action)

            # Return state of resulting game state
            return tree.state

        raise InvalidActionException()

    @classmethod
    def apply_to_child_states(cls, node: 'GameTree', fn):
        """
        Applies given function to all child states that are
        reachable from the provided state.

        :param node: GameTree object whose child nodes to apply function to
        :param fn: function to apply
        :return: list of results of applying given function to all reachable
                 states
        """
        # Validate parameters
        if not isinstance(node, GameTree):
            raise TypeError('Expected GameTree object for node!')

        if not callable(fn):
            raise TypeError('Expected function for fn!')

        # Flesh out node
        node.flesh_out()

        # For each child, apply the function to child's underlying state and
        # append result to array
        return [fn(child_node.state) for child_node in node.children.values()]
