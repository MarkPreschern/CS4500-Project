import sys

sys.path.append('../Common')

from player_interface import IPlayer
from strategy import Strategy
from color import Color
from position import Position
from state import State
from action import Action


class PlayerX(IPlayer):
    """
    PURPOSE:        This class implements the functionality of a player as laid out in the IPlayer. It leverages
                    a series of strategies for placing and moving avatars with the goal of collecting winning the game.

    INTERPRETATION: A Player is an entity that takes part in the Fish game and that is called upon by the referee
                    on its turn to either make a placement or a move. At the beginning of the game, the player is
                    initialized with an initial state (describing the board and other players) and its player id (to be
                    able to identify itself). A Player object may also be called upon with a State via the sync
                    method to be updated with the latest state of the game if an alteration to said state has occurred.
                    Finally, a Player object will be notified when a game is over about the leaderboard, cheating and
                    failing players.

                    It may also be removed from the game if the referee deems the player to be cheating (performing an
                    illegal placement or move) or fails to provide a valid return type for the functions laid out in the
                    Player interface.  When this happens the player' avatars are removed (the tiles upon which they
                    rested are not) and all communication with said player is terminated.
    """

    def __init__(self, color: Color, state: State) -> None:
        """
        This method is used to inform the player about the initial setup of the game before
        any placements are made. More specifically it provides it with its color and the initial
        state of the game, which includes the board layout, player order, and a complete list of
        players.

        :param color:       player's color
        :param state:       a State object that includes the state of the board,
                            the current placements of the penguins, knowledge about the players,
                            and the order in which they play
        :return: None
        """
        # Validate params
        if not isinstance(color, Color):
            raise TypeError('Expected Color for color!')

        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # Set properties
        self.__color = color
        self.__state = state
        # Initialize property to hold reason player was kicked
        self.__kicked_reason = ''
        # Set the depth for our strategy to find the next best move.
        self.__search_depth = 2

    @property
    def kicked_reason(self) -> str:
        """
        Returns the reason the player was kicked or
        an empty string if they have not been kicked.
        """
        return self.__kicked_reason

    def get_placement(self, state: State) -> Position:
        """
        Implements PlayerInterface.get_placement(State).

        Throws InvalidGameStatus if we're past placement stage.
        Throws OutOfTilesException if no position are open.
        """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # Update state
        self.__state = state

        # Figure out placement via strategy
        return Strategy.place_penguin(self.__color, state)

    def kick_player(self, reason: str) -> None:
        """
        Implements PlayerInterface.kick_player(str)
        """
        # Validate params
        if not isinstance(reason, str):
            raise TypeError('Expected str for state!')

        # Print reason why we got kicked.
        self.__kicked_reason = reason

    def sync(self, state: State) -> None:
        """
        Implements PlayerInterface.sync(State)
        """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # Update internal state
        self.__state = state

    def get_action(self, state: State) -> Action:
        """
        Implements PlayerInterface.get_action(State).

        Throws GameNotRunningException() if game is still in placement mode.
        """
        # Validate params
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        return Strategy.get_best_action(state, self.__search_depth)

    def game_over(self, leaderboard: dict, cheating_players: list, failing_players: list) -> None:
        """
        Implements PlayerInterface.game_over(dict, dict, list).
        """
        pass
