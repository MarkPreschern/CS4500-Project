from action import Action
from position import Position
from state import State


class PlayerInterface(object):
    """
    PURPOSE: The purpose of the interface is to provide participating
    parties with the required functionality that must be implemented by a player to enable
    the referee and the players to communicate.

    INTERPRETATION: The interface is the collection of mutually agreed upon rules (protocol) the referee
    and the players subscribe to for a game of Fish to be properly carried out.
    """
    def setup(self, player_id: int, state: State) -> None:
        """
        This method is used to inform the player about the initial setup of the game before
        any placements are made. More specifically it provides it with its id, and the initial
        state of the game, which includes the board layout, player order, and a complete list of
        players.

        :param player_id:   player's id
        :param state:       a State object that includes the state of the board,
                            the current placements of the penguins, knowledge about the players,
                            and the order in which they play
        :return: None
        """
        pass

    def place_request(self, state: State) -> Position:
        """
        This method is used to prompt the user to place their avatar. It is solely used in the
        incipient or "placing" stage of the game during which there are still avatars to be
        placed. It is called with the latest state of the game, which is meant to provide
        the player with a latest snapshot of the game. This is required as the player needs
        to know the places on the board that have been occupied, as well as the players they
        have been occupied by to be able to visualize the game as they are about to place. The
        function returns a Position object where the player wishes to place an avatar.

        :param state: a copy of the latest State object
        :return: Position object the player wishes to place an avatar
        """
        pass

    def kick_player(self, reason: str) -> None:
        """
        This method is used to kick a player for a given reason. The referee may choose to use
        this on a player who has violated the rules of the game (i.e. making an invalid move or
        placement). A reason may also be supplied to inform the player why they are being kicked.
        The player is likely to be removed shortly after this message is dispatched.

        :param reason: reason why the player is being kicked
        :return: None
        """
        pass

    def sync(self, state: State) -> None:
        """
        This method is purported to ensure that all players have the current-most game state.

        :param state: State object to provide
        :return: None
        """
        pass

    def action_req(self, state: State) -> Action:
        """
        This method is used to prompt the user to perform an action (move). It is issued upon each
        change of turn, when the current player is expected to make a move. A copy of the latest
        state is supplied to ensure that the player is acting upon the most-current version of the
        game. Upon receiving the request, the player is expected to return an Action object
        representing the action it would like to make.

        :param state: latest copy of state to supply player
        :return: action object that player wishes to make
        """
        pass

    def game_over(self, leaderboard: dict, cheating_players: list, failing_players: list) -> None:
        """
        This method is meant to notify the player that the game is over. It also provides information
        about the leaderboard, namely the ids and respective scores of players, the ids of cheating players
        as well as those of failing players.

        :param leaderboard:         dictionary of player ids mapped to their respective scores
        :param cheating_players:    list of cheating players' ids (if any)
        :param failing_players:     list of failing players' ids (if any)
        :return: None
        """
        pass
