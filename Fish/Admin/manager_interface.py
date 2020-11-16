from abc import abstractmethod, ABC
from typing import Callable


class IManager(ABC):
    """
    PURPOSE:        This class is meant to define the interface for a tournament manager. It defines the base
                    functionality that the tournament manager is required to have in order to successfully facilitate a
                    tournament.

    INTERPRETATION: A tournament manager has several pieces of functionality it must implement. These pieces of
                    functionality are as follows:
                        * Accepting new player sign-ups for a tournament
                        * Allocating players to games within tournaments
                        * Creating referees to run games
                        * Running tournaments
                        * Collecting tournament statistics
                        * Advertising tournament information to tournament observers


                    The tournament manager is initialized with an list of IPlayer objects in increasing order of age.

                    The tournament is begun via the run_tournament method, which runs each round of the tournament
                    until completion.

                    The tournament manager runs a tournament using a knock-out elimination style. Knock-out elimination
                    entails that the losers in each game of the tournament are eliminated, whereas the winner gets
                    to proceed onto the next round. The winner of a game is determined to be the player who collects
                    the largest number of fish. There may be multiple winners if multiple players achieve the same
                    highest number of fish in the game.

                    In the case of cheating/failing players, the tournament manager will remove them from the tournament
                    and not allow them to proceed in future rounds (i.e. they will be treated like other losing players
                    in each game). If every player in the tournament cheats, the tournament will have no winner.

                    A round of a tournament consists of several games being played at the same time. A round will end
                    once all games in the round end.

                    A Game is represented by a collection of Player objects and a single referee that is created by the
                    tournament manager to run the game.

                    A tournament observer is a third party that subscribes to tournament updates by way of
                    subscribe_tournament_updates. They can also obtain tournament statistics at any time by invoking
                    get_tournament_statistics.
    """

    @abstractmethod
    def run_tournament(self) -> None:
        """
        This method kicks off the tournament by running rounds of games. It first notifies the players that the
        tournament is about to start. It then creates the first round by dividing the initial set of players the manager
        was initialized with into games with the maximal number of players. If any outstanding players remain that can
        not maximally fill a game, previous fully-formed games are revisited and reduced in size one at a time until
        enough players remain to form the last game in the round.

        At the end of each game in a round, the players are notified whether they have won or lost.

        A round ends when all games in a round have finished. A new round is formed if enough players remain to warrant
        one. If too few players remain or if two consecutive rounds have produced the same winners, then the
        tournament ends. At this point, the finalists are notified whether they have lost or won the tournament.
        Otherwise, a new round is automatically started.

        :return: None
        """
        pass

    @abstractmethod
    def subscribe_tournament_updates(self, callback: Callable) -> None:
        """
        Subscribes a tournament observer to relevant tournament updates that the tournament manager will send
        by invoking the callback function provided by the observer. Tournament updates will be sent when a new round
        begins or when the tournament ends. Updates sent at the beginning of a round will be delivered in a dictionary
        containing  the current round number and a list of the games taking place in the round. Games will be
        represented by a list  containing the names of all participating players. The update will also contain a "type"
        field indicating what type of update is being sent (in this case, the type will be something like "new_round")
        The update sent at the end of a round will look something like this:

        {
            "round_num": num,
            "games": [
                [p_name1, ..., p_nameN],
                ...
                [p_name, ..., p_name]
            ],
            "type": new_round
        }

        Round numbers will be determined by the tournament manager throughout the course of the tournament, and they
        will be  1-indexed (i.e. they will begin at 1 and be incremented by 1 for each new round in the tournament).

        Updates that are sent at the end of a tournament will be delivered in a dictionary that contains a list of the 
        names of cheating players throughout the tournament, a list of the names of failing players throughout the 
        tournament, the total number of players who signed up for the tournament, and the final game standings 
        which will indicate the winner of the tournament. The update will also contain a "type" field indicating 
        what type of update is being sent (in this case, the type will be something like "tournament_end")

        The update sent at the end of a round will look something like this:
        {
            "cheating_players": [p_name, ..., p_name],
            "failing_players": [p_name, ..., p_name],
            "total_players": num_players_in_tournament,
            "final_game_standings": [
                            {"name": "Winner", "color": Color.BLACK, "score": 99},
                            {"name": "Runner-up", "color": Color.WHITE, "score": 40}
            ]
            "type": tournament_end
        }

        Please note that we considered adding a top five players field to indicate who had the highest scores in the
        tournament. However, given that the tournament manager is not responsible for determining the layout of the 
        board, it is entirely possible that not all players will be in games with as many fish as other players.
        Thus, the total score of each player throughout the tournament does not provide any significant information.

        :param callback: the callback function that will be invoked by the tournament manager to provide updates
        :return: None
        """
        pass

    @abstractmethod
    def get_tournament_statistics(self) -> dict:
        """
        Allow a tournament observer to get tournament statistics at any point during the tournament.
        Tournament statistics will include a list of the names of cheating/failing players,
        the total number of fish collected by all rule-abiding players, and the total number of 
        players who signed up for the tournament.

        The dictionary returned by this function will look something like the following:
        {
            "cheating_players": [p_name, ..., p_name],
            "failing_players": [p_name, ..., p_name],
            "total_players": num_players_in_tournament,
            "total_fish_collected": num_fish_collected_by_rule_abiding_players
        }

        :return: a dictionary containing the relevant tournament statistics described above
        """
        pass
