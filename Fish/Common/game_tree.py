import copy

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

    The structure follows a lazy, generative design meaning that adjacent trees are not connected
    until there is an explicit "need".
    """

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

        # Initialize dictionary of actions to GameTree objects.
        # to hold subsequent game trees. An action is defined as
        # a tuple of Position(s) to denote a move from the former
        # position to the latter.
        self.__children = {}

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
        return self.__state

    def flesh_out(self):
        """
        Fleshes out the GameTree by connecting it to game trees for
        all the subsequent game states that can be derived from this
        tree's game state.

        :return: resulting GameTree object
        """

        # Get all possible actions for this tree's underlying state
        actions: [Action] = self.__state.get_possible_actions()

        # For each possible action
        for action in actions:
            # De-multiplex action into position tuples
            src, dst = action

            # Create subsequent game state after this move is made
            subsequent_state: State = copy.deepcopy(self.__state)
            subsequent_state.move_avatar(src, dst)

            # Insert mapping of action to resulting GameTree
            self.__children.update({action: GameTree(subsequent_state)})

    @classmethod
    def try_action(cls, state: State, action: Action):
        """
        Tries to perform the given action or fails. If successful, the
        function returns the resulting state from performing provided
        action, otherwise it throws an InvalidActionException().

        :param state: State object to perform action on
        :param action: Action object representing move to make
        :return: resulting game state
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State object for state!')

        if not isinstance(action, Action):
            raise TypeError('Expected a Action object for action!')

        # Create game tree for given state
        tree = cls(state)
        # Flesh out said game tree
        tree.flesh_out()

        # Check if given action is among those possible
        # for said game tree
        if action in tree.children.keys():
            # Retrieve game tree that can be arrived at
            # by performing the given move
            tree: GameTree = tree.children.get(action)

            # Return state of resulting game state
            return tree.state

        raise InvalidActionException()

    @classmethod
    def apply_to_child_states(cls, state: State, fn):
        """
        Applies given function to all child states that are
        reachable from the provided state.

        :param state: State object whose children to apply function to
        :param fn: function to apply
        :return: list of results of applying given function to child
                 states
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State object for state!')

        if not callable(fn):
            raise TypeError('Expected function for fn!')

        # Create game tree for given state
        tree = cls(state)
        # Flesh out said game tree
        tree.flesh_out()

        # For each child tree, apply function to child's underlying
        # state and return the results for all children in an array
        return [fn(child.state) for child in tree.children.values()]

