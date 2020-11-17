import sys

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player_interface import IPlayer
from manager_interface import IManager
from player_status import PlayerStatus
from referee import Referee
import constants as ct
from typing import Callable


class Manager(IManager):
    """
    PURPOSE:        The purpose of this class is to implement IManager to run a tournament of games of Fish
                    (IPlayer objects) and determine the winner(s) for a given set of players. The set of players is
                    assumed to be in order of increasing age and may consist of any player implementing IPlayer.

    INTERPRETATION: The manager uses a knock-out elimination system to determine which players may proceed to the
                    next round. A round is simply a set of Fish games that start simultaneously and end with the
                    players that qualify to the next round. To make up a game, the tournament creates a referee
                    and provides it with the list of players and the board size of that game. The board size is
                    configurable at the initialization of the manager.

                    To allocate players to the games in a round, the manager determines the minimum number of games
                    needed to fit all the players. If any outstanding players remain that are too few to form a game,
                    the last formed game is revisited and reduced in size so that another game could be formed to
                    fit all remaining players.

                    At the end of each game, the players are notified whether they have lost or won. Players that
                    refuse to accept a win are automatically disqualified from the next round (if there is one). In
                    each game, the player that proceeds onto the next round is the player that has collected the
                    most fish. If multiple players have collected the same highest number of fish, they all proceed
                    onto the next round. It is also conceivable that no players proceed to the next round if all players
                    have been eliminate in the course of a game (by cheating or failing). Moreover, a player that loses
                    a game, loses the tournament.

                    The tournament ends when two rounds produce the exact same winners in a row, there are too few
                    players for a single game or when the final game of all outstanding players has been played. At
                    this point, the manager informs the remaining active players whether they won or lost. Failure on
                    the part of a player to accept this information will result in the player becoming a "loser".
    """
    def __init__(self, players: [IPlayer], board_row_no:int = 5, board_col_no:int = 5):
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
        # Initialize list to hold tournament losers
        self.__tournament_losers = []

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

    def subscribe_tournament_updates(self, callback: Callable) -> None:
        pass

    def get_tournament_statistics(self) -> dict:
        pass

    def run_tournament(self):
        """
        Implements IManager.run_tournament()
        """
        # Run first round & get players qualified to next
        winners, losers = self.__run_round()
        # Trim down player list to winners
        self.__players = winners

        print(f'1st rounds winners: {[winner.name for winner in winners]} losers: {[loser.name for loser in losers]}')
        # Run tournament so long as enough players remain to warrant another round or until two consecutive
        # rounds have produced the same winners.
        while len(winners) > 1:
            # Get this round's winners & losers
            winners, losers = self.__run_round()

            print(f'this rounds winners: {[winner.name for winner in winners]} losers: {[loser.name for loser in losers]}')
            # Initialize list to hold IPlayer objects that fail to acknowledge that they won
            failing_winners = []

            # Notify this round's winners that they won
            for winner in winners:
                try:
                    winner.status_update(PlayerStatus.WON_GAME)
                except:
                    # If an exception was thrown the winner becomes a loser.
                    failing_winners.append(winner)

            # Remove failing winners from winners and add them to losers
            for failing_winner in failing_winners:
                winners.remove(failing_winner)
                losers.append(failing_winner)

            # Notify this round's losers that they've lost
            for loser in losers:
                try:
                    loser.status_update(PlayerStatus.LOST_GAME)
                except:
                    # Nothing to do.
                    pass

            # See if the previous & current round have produced the same winners
            if set(self.__players) == set(winners):
                print('produced same winners x2')
                # Tournament is over.
                # Trim down set of players to winners
                self.__players = winners
                break

            # Trim down set of players to winners
            self.__players = winners

        # Outstanding players have won the tournament
        for player in self.__players:
            try:
                player.status_update(PlayerStatus.WON_TOURNAMENT)
            except:
                # If a winning player throws an exception, they become a loser
                player.status_update(PlayerStatus.LOST_GAME)
                self.__tournament_losers.append(player)
            else:
                self.__tournament_winners.append(player)

    def __run_round(self) -> [IPlayer]:
        """
        Runs a round of the tournament and returns list of
        IPlayer objects qualified to the next round of the tournament.

        :return: resulting IPlayer lists of winning and losing players
        """
        # Make round (list of Referee)
        games = self.__make_round_games()

        # Initialize list to contain IPlayer objects that won
        winners = []
        # Initialize list to contain IPlayer objects that lost
        losers = []

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
                    # Remove game from list
                    games.remove(games[k])

            games_in_progress = len(games)

        return winners, losers

    def __make_round_games(self):
        """
        Makes a round by creating games (Referee objects) with players.

        :return: resulting games (list of Referee)
        """
        divide: [[IPlayer]] = self.__divide_players()
        games: [Referee] = []

        # For each list of players (game), make up a referee
        for player_list in divide:
            referee: Referee = Referee(self.__board_row_no, self.__board_col_no, player_list)
            # referee.subscribe_final_game_report(blah)
            games.append(referee)

        return games

    def __divide_players(self):
        """
        Divides outstanding players into the smallest number of lists of IPlayer possible considering
        the minimum and and maximum # of players that can be allocated to a game. After packing as many IPlayer objects
        in as few such lists as possible, if N < MIN_PLAYERS players remain, previous well-formed lists of IPlayer are
        revisited in reverse order (starting from the last complete one) and the last player from each such
        lists is popped off and inserted into the right location of a new list so the order of age is preserved. When
        the new list reaches a length = MIN_PLAYERS, the algorithm stops and the resulting list of lists of IPlayer
        is returned.

        :return: list of lists of IPlayer representing the games that are about to be formed
        """
        games: [[IPlayer]] = []

        # Make games with the highest number of players possible
        for i in range(0, len(self.__players), ct.MAX_PLAYERS):
            games.append(self.__players[i:i + ct.MAX_PLAYERS])

        last_index = len(games) - 1

        # Initialize variable to keep track of the number of times the entire set of games
        # has been swept end to end
        sweep_no = 0

        # Transfer one player at a time from previous games (in reverse order) to the last game
        # until last game has minimum players
        while len(games[last_index]) < ct.MIN_PLAYERS:
            # Cycle from second to last game to first game
            for k in range(last_index - 1, -1, -1):
                # Pop last player from the current game off and add it to the last game at the right
                # index so order is preserved
                games[last_index].insert(sweep_no * k, games[k].pop())

                # If last game has valid number of players break
                if len(games[last_index]) >= ct.MIN_PLAYERS:
                    break
            # Increment sweep
            sweep_no += 1

        return games
