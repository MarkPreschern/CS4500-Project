import copy

from Position import Position
from State import State
from exceptions.InvalidActionException import InvalidActionException


class GameTree(object):
    """
    Represents a game tree representation. The representation can be used to represent
    entire games and enables parties to check rules and plan their next moves. It
    is generated from a state and can maintain connections to subsequent game states
    by way of other GameTree(s).
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

        # Initialize state
        self.__state = state

        # Initialize dictionary of "actions to GameTree objects"
        # to hold subsequent game trees
        self.__children = {}

    @property
    def children(self):
        """
        Returns a list of all GameTrees that derive from this GameTree.
        """
        return copy.deepcopy(self.__children)

    @property
    def state(self) -> State:
        """
        Returns a copy of the GameState that the tree is based off of.
        """
        return copy.deepcopy(self.__state)

    def flesh_out(self):
        """
        Fleshes out the GameTree by connecting it to game trees for
        all the subsequent game states that can be derived from this
        tree's game state.

        :return: resulting GameTree object
        """

        # Get all possible actions for this tree's underlying state
        actions: [(Position, Position)] = self.__state.get_possible_actions()

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
    def try_action(cls, state: State, action: (Position, Position)):
        """
        Tries to perform the given action or fails. If successful, the
        function returns the resulting state from performing provided
        action, otherwise it throws an InvalidActionException().

        :param state: State object to perform action on
        :param action: tuple of Positions representing move to make
        :return: resulting game state
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State object for state!')

        if not isinstance(action, ((int, int), (int, int))):
            raise TypeError('Expected a tuple of two positions for'
                            'action!')

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
    def apply_function_to_child_states(cls, state: State, fn):
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
        return [fn(child.state) for child in tree.children]

