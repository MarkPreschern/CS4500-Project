from abc import abstractmethod, ABC
import sys

class IManager(ABC):
    """
    PURPOSE: This class is meant to define the interface for a tournament manager. It defines the base functionality that the tournament
            manager is required to have in order to successfully facilitate a tournament.

    INTERPRETATION: A tournament manager has several pieces of functionality it must implement. These pieces of functionality are as follows:
        * Accepting new player signups for a tournament
        * Allocating players to games within tournaments
        * Creating referees to run games
        * Running tournaments
        * Collecting tournament statistics
        * Advertising tournament information to tournament observers

        The tournament is begun via the run_tournament method, which accepts player signups and runs each round of the tournament until completion.

        The tournament manager runs a tournament using a single elimination style. Single elimination entails that each game in a round of a tournament
        will have a single winner that moves on to the next round. All other players in the game will be removed from the tournament. The tournament manager will
        fill each game in the tournament with the same number of players (either human or house AI). For example, in a tournament with 20 players, the tournament manager 
        will assign 5 players to each game for round 1. For round 2, the tournament manager will take the 5 winners from round 1, assign 3 of them to one game, and
        assign the remaining 2 to another game. It will then add a house AI to the second game, making sure both games in the round have 3 players.
        In round 3, the tournament manager will take the 2 winners from round 2 and assign them to a game with 2 players.
        The winner of the tournament will be the player who wins the game in the final round.

        In the case of cheating/failing players, the tournament manager will remove them from the tournament and not allow them to proceed in future rounds
        (i.e. they will be treated like other losing players in each game). If every player in the tournament cheats, the tournament will have no winner.

        A round of a tournament consists of several games being played at the same time. A round will end once all games in the round end.

        A Game is represented by a collection of Player objects and a single referee that is created by the tournament manager to run the game.

        A tournament observer is a third party that subscribes to tournament updates by way of subscribe_tournament_updates. They can also obtain
        tournament statistics at any time by invoking get_tournament_statistics.
    """

    @abstractmethod
    def run_tournament(players: [Player]) -> None:
        """
        This method is responsible for running the tournament.

        It accepts new player signups after receiving a list of Player objects (presumably from a sign-up server).
        It is assumed that this sign-up server has already sorted the players in order of age,
        meaning reverse order of when they signed up.

        It will then create games with a uniform number of players (or as close to uniform as possible) and a referee to
        run the game. It will then run the tournament one round at a time as described in our interpretation.
        Before moving onto the next round of the tournament, this method will wait until all games in the current round
        have finished. At that point, it will repeat the process of creating games, assigning players, and assigning referees.

        This method will rely on helper methods, of course, but they will not be public facing.

        :param players: The list of players who have signed up for the tournament.
        :return: None
        """
        pass

    @abstractmethod
    def subscribe_tournament_updates(callback: 'Callable') -> None:
        """
        Subscribes a tournament observer to relevant tournament updates that the tournament manager will send
        by invoking the callback function provided by the observer. Tournament updates will be sent when a new round begins
        or when the tournament ends. Updates sent at the beginning of a round will be delivered in a dictionary containing 
        the current round number and a list of the games taking place in the round. Games will be represented by a list 
        containing the names of all participating players. The update will also contain a "type" field indicating what type
        of update is being sent (in this case, the type will be something like "new_round")
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

        Round numbers will be determined by the tournament manager throughout the course of the tournament, and they will be 
        1-indexed (i.e. they will begin at 1 and be incremented by 1 for each new round in the tournament).

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
    def get_tournament_statistics() -> dict:
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
