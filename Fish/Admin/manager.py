import sys
import pickle

sys.path.append('../Fish/Common')
sys.path.append('../Fish/Admin/Other/')

from player_interface import IPlayer
from manager_interface import IManager
from player_status import PlayerStatus
from player_kick_reason import PlayerKickReason
from tournament_update_type import TournamentUpdateType
from referee import Referee
import constants as ct
import threading
from typing import Callable
import utils


class Manager(IManager, threading.Thread):
    """
    PURPOSE:        The purpose of this class is to implement IManager to run a tournament of games of Fish
                    (IPlayer objects) and determine the winner(s) for a given set of players. The set of players is
                    assumed to be in order of increasing age and may consist of any player implementing IPlayer.

    INTERPRETATION: The manager uses a knock-out elimination system to determine which players may proceed to the
                    next round. A round is simply a set of Fish games that start simultaneously and end with the
                    players that qualify to the next round. To make up a game, the tournament creates a referee
                    and provides it with the list of players and the board size of that game. The board size is
                    configurable at the initialization of the manager.

                    The manager starts off by notifying players that the tournament has begun by calling
                    tournament_has_started() on them. If the manager does not receive a response from a player within
                    PLAYER_TIMEOUT that they acknowledge the start of the tournament, the manager removes the player
                    from the game. After notifying all players (and removing unresponsive ones), the manager proceeds
                    to allocate players to games.

                    To allocate players to the games in a round, the manager determines the minimum number of games
                    needed to fit all the players. If any outstanding players remain that are too few to form a game,
                    the manager backtracks to the previous games one one at a time, reducing their size by one to
                    come up with enough players to form the last game.

                    At the beginning of each round, subscribed observers are notified that the round is about to
                    start and they are provided with an update packet. Similarly, at the end of the tournament, a final
                    update is issued to all observers notifying them of the tournament winners.

                    At the end of each game, the players are notified whether they have lost or won. Players win
                    and qualify onto the next round if they have collected the largest number of fish at game end
                    (the manager leverages the referee's end-of-game information, namely .winners, to determine this).
                    Players that refuse to accept a win via status_update() within PLAYER_TIMEOUT seconds are
                    automatically disqualified from the next round (if there is one). If multiple players in the same
                    game have collected the same highest number of fish, they all proceed onto the next round. It is
                    also conceivable that no players proceed to the next round if all players have been eliminate in
                    the course of a game (by cheating or failing). Moreover, a player that loses a game, loses the
                    tournament.

                    The tournament ends when two rounds produce the exact same winners in a row, there are too few
                    players for a single game or when the final game of all outstanding players has been played. At
                    this point, the manager informs the remaining active players whether they won or lost. Failure on
                    the part of a player to accept this information within PLAYER_TIMEOUT seconds will result in the
                    player becoming a "loser".

    DEFINITION(s):  A game is represented by a Referee object overseeing that game's players.
                    A (player) divide is a low-level representation of a game in the form of a list of list of IPlayer
                    , where each inner-list represents a game in the form of the players of that game.
    """
    DEBUG = False

    # Initialize player timeout (int no. of seconds a player is allowed to take to acknowledge either a status update
    # or that the tournament has begun).
    PLAYER_TIMEOUT = 1

    # the number of fish on each tile of each game board in the server's tournament. Random by default.
    FISH_NUMBER = None

    def __init__(self, players: [IPlayer], board_row_no: int = 5, board_col_no: int = 5):
        """
        Initializes the tournament manager with the list of IPlayer objects.

        :param players: list of IPlayer
        :param board_row_no: number of rows to game board used in the tournament
        :param board_col_no: number of cols to game board used in the tournament
        :return: None
        """
        # Validate params
        if not isinstance(players, list):
            raise TypeError('Expected list of IPlayer for players!')

        if not isinstance(board_row_no, int):
            raise TypeError('Expected int for board_row_no')

        if not isinstance(board_col_no, int):
            raise TypeError('Expected int for board_col_no')

        self.__board_row_no = board_row_no
        self.__board_col_no = board_col_no

        self.__players = players

        # Initialize list to hold tournament winners
        self.__tournament_winners = []
        # Initialize list to hold tournament losers, which includes kicked players
        self.__tournament_losers = []
        # Initialize list to hold tournament players who were kicked for cheating or failing
        self.__tournament_kicked = []
        # Initialize list to hold the callback methods of subscribed observers
        self.__update_callbacks = []
        # Initialize counter to keep track of round no.
        self.__round_no = 1
        # Initialize placeholder to hold last update that was dispatched to observers
        self.__last_update = {}

    @property
    def tournament_winners(self):
        """
        Returns a list of IPlayer objects representing the tournament winners.
        """
        return self.__tournament_winners

    @property
    def tournament_losers(self):
        """
        Returns a list of IPlayer objects representing the tournament losers.
        """
        return self.__tournament_losers

    @property
    def tournament_kicked(self):
        """
        Returns a list of IPlayer objects representing the tournament players who were kicked for cheating or failing.
        """
        return self.__tournament_kicked

    def subscribe_tournament_updates(self, callback: Callable) -> None:
        """
        Implements IManager.subscribe_tournament_updates(Callable).
        """
        # Validate params
        if not callable(callback):
            raise TypeError('Expected callable for callback!')

        self.__update_callbacks.append(callback)

    def get_tournament_statistics(self) -> dict:
        """
        Implements IManager.get_tournament_statistics().
        """
        return self.__last_update.copy()

    def __broadcast_tournament_start(self) -> None:
        """
        This methods calls tournament_has_started() on each IPlayer partaking in the tournament
        to let it know that the tournament has begun. Failure on the part of any player to acknowledge
        this in a timely fashion will result in their disconnection.

        :return: None
        """

        # Trim down player list to players that have acknowledged that the tournament has started
        present_players = []
        for p in self.__players:
            if utils.timed_call(Manager.PLAYER_TIMEOUT, p, 'tournament_has_started', ()):
                present_players.append(p)
            else:
                self.__tournament_kicked.append(p)
                p.kick(PlayerKickReason.FAILING.name)
        self.__players = present_players

    def __broadcast_tournament_end(self) -> None:
        """
        This methods calls tournament_has_ended() on each IPlayer partaking in the tournament
        to let it know that the tournament has ended. Failure on the part of any player to acknowledge
        this in a timely fashion will result in their disconnection.

        :return: None
        """

        # Trim down player list of winning players to those that ack the notification
        present_players = []
        for p in self.__players:
            if utils.timed_call(Manager.PLAYER_TIMEOUT, p, 'tournament_has_ended', tuple([True])):
                present_players.append(p)
            else:
                self.__tournament_losers.append(p)
                self.__tournament_kicked.append(p)
                p.kick(PlayerKickReason.FAILING.name)
        self.__players = present_players
        self.__tournament_winners = present_players

        # Notify loser players that they lost
        for loser in self.__tournament_losers:
            loser.tournament_has_ended(False)

    def run(self):
        """
        Implements IManager.run()
        """
        # Inform players tournament has started
        self.__broadcast_tournament_start()

        # Run first round & get players qualified to next
        winners, losers, kicked = self.__run_round()
        winners, losers, kicked = self.__notify_players(losers, winners, kicked)

        # Trim down player list to winners
        self.__players = winners

        # Run tournament so long as enough players remain to warrant another round or until two consecutive
        # rounds have produced the same winners.
        while len(winners) > 1:
            self.__round_no += 1
            # Get this round's winners & losers
            winners, losers, kicked = self.__run_round()
            # Notify players & transfer failing winners to losers if they refuse to accept notification
            winners, losers, kicked = self.__notify_players(losers, winners, kicked)

            # See if the previous & current round have produced the same winners
            if set(self.__players) == set(winners):
                if Manager.DEBUG:
                    print(f'produced same winners x2: {[winner.name for winner in winners]}')
                # Tournament is over.
                break

            # Trim down set of players to winners
            self.__players = winners

        # set tournament winners
        self.__tournament_winners = winners

        # Notified subscribed parties of tournament results
        self.__notify_tournament_end()
        self.__broadcast_tournament_end()

    def __notify_players(self, losers: [IPlayer], winners: [IPlayer], kicked: [IPlayer]) -> [[IPlayer], [IPlayer], [IPlayer]]:
        """
        Notifies the given collection of winning and losing players that they have either
        won the game (a game, not necessarily the tournament) or that they lost the tournament
        (if you lose a game, you lose the tournament). A failure on the part of the winning players
        to accept the notification will result in them being moved to the losers collection.

        :param losers: list of IPlayer representing losing players
        :param winners: list of IPlayer representing winning players
        :param kicked: list of IPlayer representing kicked players
        :return: resulting losers: [IPlayer], winners: [IPlayer], kicked: [IPlayer]
        """
        # Initialize list to hold IPlayer objects that fail to acknowledge that they won
        failing_winners = []
        # Notify this round's winners that they won
        for winner in winners:
            try:
                result = utils.timed_call(Manager.PLAYER_TIMEOUT, winner, 'status_update', (PlayerStatus.WON_GAME, ))

                # Make sure we get back True
                if not isinstance(result, bool) or not result:
                    raise TypeError()

            except Exception:
                # If an exception was thrown the winner becomes a loser.
                failing_winners.append(winner)

        # Remove failing winners from winners and add them to collections of losers
        for failing_winner in failing_winners:
            # A failing winner is not a winner
            winners.remove(failing_winner)
            # A failing winner is a game loser
            losers.append(failing_winner)
            # A failing winner is a kicked players
            kicked.append(failing_winner)
            # A failing winner is a tournament loser
            self.__tournament_losers.append(failing_winner)

        # Notify this rounds kicked players that they've been kicked
        for kick in kicked:
            # append tournament kicked players
            self.__tournament_kicked.append(kick)
            try:
                kick.status_update(PlayerStatus.DISCONTINUED)
            except Exception:
                # Nothing to do.
                pass

        # Notify this round's losers that they've lost, only if they haven't already been kicked
        for loser in losers:
            # append tournament losers
            self.__tournament_losers.append(loser)
            if loser not in kicked:
                try:
                    loser.status_update(PlayerStatus.LOST_GAME)
                except Exception:
                    # Nothing to do.
                    pass

        # Return updated winners & losers
        return winners, losers, kicked

    def __notify_tournament_end(self) -> None:
        """
        Notifies all subscribed observers that the tournament has come to end. It dispatches
        an update packet as described in IManager.subscribe_tournament_updates(Callable).

        :return: None
        """
        # Make up payload
        update = {
            "type": TournamentUpdateType.TOURNAMENT_END,
            "winners": [player.name for player in self.__tournament_winners]
        }

        # Update last update
        self.__last_update = update

        # Notify subscribers & remove those that fail to accept callback
        self.__update_callbacks = [callback for callback in self.__update_callbacks
                                   if Manager.__try_callback(callback, update)]

    @staticmethod
    def __try_callback(callback: Callable, payload: dict) -> bool:
        """
        Attempts to call callback with payload on it. In case an Exception occurs in the process
        False is returned. Otherwise, True is returned indicating successful callback.
        """
        try:
            callback(payload)
        except AssertionError as e:
            # Raise assertion exceptions are these are used for testing
            raise e
        except Exception as e:
            if Manager.DEBUG:
                print(f'Error in callback: {e}')
            return False
        return True

    def __notify_round_start(self, player_divide: [[IPlayer]]) -> None:
        """
        This method updates the subscribed tournament observers that a new round is about to start.
        It dispatches a dict as described in IManager.subscribe_tournament_updates().

        :param player_divide: list of list of IPlayer representing the allocation of players into games
        :return: None
        """
        # Validate params
        if not isinstance(player_divide, list):
            raise TypeError('Expected list of list of IPlayer for player_divide!')

        # Initialize list to hold the names of players as they are organized into games
        named_player_divide = []

        # Map player divide to a list of list of str (player name)
        for game in player_divide:
            named_player_divide.append([player.name for player in game])

        # Make up payload
        update = {
            "round_num": self.__round_no,
            "games": named_player_divide,
            "type": TournamentUpdateType.NEW_ROUND
        }

        # Update last update
        self.__last_update = update

        # Notify subscribers & remove those that fail to accept callback
        self.__update_callbacks = [callback for callback in self.__update_callbacks
                                   if Manager.__try_callback(callback, update)]

    def __run_round(self) -> [IPlayer]:
        """
        Runs a round of the tournament and returns list of
        IPlayer objects qualified to the next round of the tournament.

        :return: resulting IPlayer lists of winning and losing players
        """
        # Make round (list of Referee)
        games, divide = self.__make_round_games()

        # Dispatch update about the round about to start
        self.__notify_round_start(divide)

        # Initialize list to contain IPlayer objects that won
        winners = []
        # Initialize list to contain IPlayer objects that lost
        losers = []
        # Initialize list to contain IPlayer objects that were kicked
        kicked = []

        games_in_progress = len(games)

        while games_in_progress > 0:
            # Cycle over games
            for k in range(len(games) - 1, -1, -1):
                # Start game if needed
                if not games[k].started:
                    games[k].start()

                # Check if game over
                if games[k].game_over:
                    # Extend list of qualified players to include this game's winners
                    winners.extend(games[k].winners)
                    # Extend list of losers to include this game's losers
                    losers.extend(games[k].losers)
                    # Extend list of kicked players to include cheating players
                    kicked.extend(games[k].cheating_players)
                    # Extend list of kicked players to include failing players
                    kicked.extend(games[k].failing_players)
                    # Remove game from list
                    games.remove(games[k])

            games_in_progress = len(games)

        if Manager.DEBUG:
            print(f'this rounds winners: {[winner.name for winner in winners]}')

        return winners, losers, kicked

    def __make_round_games(self):
        """
        Makes a round by creating games (Referee objects) with players.

        :return: resulting list of Referee (representing games) and list of list of IPlayer as returned by
                 __divide_players()
        """
        divide: [[IPlayer]] = self.__divide_players()
        games: [Referee] = []

        # For each list of players (game), make up a referee
        for player_list in divide:
            referee: Referee = Referee(self.__board_row_no, self.__board_col_no, player_list, Manager.FISH_NUMBER)
            # referee.subscribe_final_game_report(blah)
            games.append(referee)

        return games, divide

    def __divide_players(self):
        """
        Divides outstanding players into the smallest number of lists of IPlayer possible considering
        the minimum and and maximum # of players that can be allocated to a game. After packing as many IPlayer objects
        in as few such lists as possible, if N < MIN_PLAYERS players remain, previous well-formed lists of IPlayer are
        revisited in reverse order (starting from the last complete one) and the last player from each such
        lists is popped off and inserted into the right location of a new list so the order of age is preserved. When
        the new list reaches a length = MIN_PLAYERS, the algorithm stops and the resulting list of lists of IPlayer
        is returned.

        :return: returns a player divide (list of lists of IPlayer representing the games that are about to be formed)
        """
        divide: [[IPlayer]] = []

        if len(self.__players) < ct.MIN_PLAYERS:
            return []

        # Make games with the highest number of players possible
        for i in range(0, len(self.__players), ct.MAX_PLAYERS):
            divide.append(self.__players[i:i + ct.MAX_PLAYERS])

        last_index = len(divide) - 1

        # Initialize variable to keep track of the number of times the entire set of games
        # has been swept end to end
        sweep_no = 0

        # Transfer one player at a time from previous games (in reverse order) to the last game
        # until last game has minimum players
        while len(divide[last_index]) < ct.MIN_PLAYERS:
            # Cycle from second to last game to first game
            for k in range(last_index - 1, -1, -1):
                # Pop last player from the current game off and add it to the last game at the right
                # index so order is preserved
                divide[last_index].insert(sweep_no * k, divide[k].pop())

                # If last game has valid number of players break
                if len(divide[last_index]) >= ct.MIN_PLAYERS:
                    break
            # Increment sweep
            sweep_no += 1

        return divide
