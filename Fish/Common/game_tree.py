import pickle

from action import Action
from exceptions.GameNotRunningException import GameNotRunningException
from exceptions.InvalidActionException import InvalidActionException
from state import State


class GameTree(object):
    """
    INTERPRETATION: Represents an entire game starting from a given state wherein no more
    avatars will be placed. It is generated from a state and can maintain connections to
    subsequent game states by way of other GameTree(s). A game tree can only represent states
    wherein the current player can move or no one can move (game over). The game tree cannot
    represent states in which the current player is stuck as that is prevented by default by
    the game state by skipping players that cannot move over.

    PURPOSE: The representation can be used by the players and the referee to check rules and
    plan their next moves.

    DEFINITION(S): A a GameTree node is simply a GameTree with child GameTrees attached to it.

    The structure follows a lazy, generative design meaning that adjacent trees are not computed
    until there is an explicit "need".
    """

    def __init__(self, state: State):
        """
        Initializes a barren GameTree with the given state. The tree's child
        nodes are not computed until get_next() is called. This constructor solely
        returns a new GameTree that incorporates
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
        if not self.__state.has_everyone_placed():
            raise GameNotRunningException()

        # Initialize dictionary of Action objects to GameTree objects (nodes).
        # to hold subsequent game trees.
        self.__children = {}

        # Get all possible actions for this tree's underlying state. It only includes
        # actions that can be performed by the current player and that are legal
        # under the rules of Fish.
        self.__all_possible_actions = self.__state.get_possible_actions()

    @property
    def all_possible_actions(self):
        """
        Returns a copy of all possible actions (list of Action).
        """
        return self.__all_possible_actions.copy()

    @property
    def state(self) -> State:
        """
        Returns a copy of the GameState that the tree is based off of.
        """
        return pickle.loads(pickle.dumps(self.__state))

    def __get_node(self, move: Action):
        """
        Gets node from performing specified move on this game tree's
        underlying state. If the node does not exist, it is created
        (assuming the move is valid).

        :param move: Action object to perform
        :return: game tree node or None
        """
        # Validate param
        if not isinstance(move, Action):
            raise TypeError('Expected Action for move!')

        # Make sure move is possible
        if move not in self.__all_possible_actions:
            raise InvalidActionException()

        # Crate child node for move if not in cache
        if move not in self.__children:
            # Make a copy of the state
            subsequent_state: State = self.__state.deepcopy()
            # Get move to make
            src, dst = move
            # Make move
            subsequent_state.move_avatar(src, dst)
            # Make up game tree for this child state
            subsequent_gt = GameTree(subsequent_state)
            # Cache child node
            self.__children.update({move: subsequent_gt})

        # Return from cache
        return self.__children[move]

    def get_next(self):
        """
        Returns a generator that lazily yields the tree's next child nodes.

        :return: a tuple made of an Action object and the GameTree node said action
                 results in when applied to the underlying state of the tree.
        """

        # Cycle over all possible moves from this node
        for move in self.__all_possible_actions:
            # Yield move along with resulting node
            yield move, self.__get_node(move)

    def try_action(self, action: Action) -> State:
        """
        Tries to perform the given action or fails on the underlying state
        of the game tree. If successful, the function returns the resulting state from
        performing provided action, otherwise it throws an InvalidActionException().

        :param action: Action object representing move to make
        :return: resulting game state
        """
        # Validate parameters
        if not isinstance(action, Action):
            raise TypeError('Expected a Action object for action!')

        # __get_node throws InvalidActionException() upon failure
        return self.__get_node(action).state

    def apply_to_child_states(self, fn):
        """
        Applies given function to all child states that are
        reachable from this game tree.

        :param fn: function to apply
        :return: list of results of applying given function to all reachable
                 states
        """
        # Validate parameters
        if not callable(fn):
            raise TypeError('Expected function for fn!')

        # For each child, apply the function to child's underlying state and
        # append result to array
        return [fn(child_node.state) for move, child_node in self.get_next()]
