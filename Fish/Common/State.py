from Board import Board
from Player import Player
import constants as ct
from collections import OrderedDict

from exceptions.AvatarAlreadyPlacedException import AvatarAlreadyPlacedException
from exceptions.AvatarNotPlacedException import AvatarNotPlacedException
from exceptions.InvalidPosition import InvalidPosition


class State(object):
    """
    State represents the current state of a game: the state of the board,
    the current placements of the penguins, knowledge about the players,
    and the order in which they play.
    """

    def __init__(self, board: Board, players: [Player]):
        """
        Initializes a State object with the given parameters.
        :param board: Board object
        :param players: list of Player objects
        :return: new State object designed to spec
        """
        # Validate params
        if not isinstance(board, Board):
            raise TypeError('Expected Board object for board!')

        # Make sure players is a list
        if not isinstance(players, list):
            raise TypeError('Expected list for players!')

        # Make sure list consists of only player objects
        if not all(isinstance(x, Player) for x in players):
            raise TypeError('All player list objects have to of type Player!')

        # Check player list length
        if len(players) < ct.MIN_PLAYERS or len(players) > ct.MAX_PLAYERS:
            raise ValueError(f'Expected list of length <= {ct.MAX_PLAYERS} and >= {ct.MIN_PLAYERS}')

        self.__board = board

        # Create player dictionary keyed by player ids
        self.__players = OrderedDict()

        # Sort player list in increasing order of age
        players.sort(key=lambda p: p.age)

        # Insert players in the order they go
        for player in players:
            self.__players.update({player.id: player})

        # Initialize placements
        self.__placements = {}  # keys = ids, values = position tuples

    def place_avatar(self, player_id: int, position: tuple) -> None:
        """
        Places an avatar on behalf of the player with the specified
        id at the specified location if it is not a hole.

        :param player_id: id of player whose avatar to place
        :param position: tuple position to place avatar
        :return: None
        """
        # Validate type of player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player id!')
            
        # Validate type of position
        if not isinstance(position, tuple):
            raise TypeError('Expected tuple for position!')
            
        # Make sure player id is in player list
        if player_id not in self.__players.keys():
            raise ValueError('Player id not in player list!')

        # Make sure player has not already placed avatar
        if player_id in self.__placements.keys():
            raise AvatarAlreadyPlacedException()
            
        # Make sure a player cannot place an avatar where another player has
        if position in self.__placements.values():
            raise InvalidPosition()
    
        # Validate position (throws InvalidPosition if it's not)
        tile = self.__board.get_tile(position)

        # Make sure it is not a hole
        if tile.is_hole:
            raise InvalidPosition('Cannot place avatar on a Hole!')
            
        # Place avatar to desired position
        self.__placements.update({player_id: position})

    def move_avatar(self, player_id: int, position: tuple) -> None:
        """
        Moves an avatar on behalf of the player with the specified
        id to the specified location if said location is reachable
        and not a hole.

        :param player_id: id of player whose avatar to move
        :param position: tuple position to move avatar
        :return: None
        """
        # Validate type of player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player id!')

        # Make sure player id is in player list
        if player_id not in self.__players.keys():
            raise ValueError('Player id not in player list!')

        # Make sure player has already placed their avatar
        if player_id not in self.__placements:
            raise AvatarNotPlacedException()

        # Validate type of position
        if not isinstance(position, tuple):
            raise TypeError('Expected tuple for position!')

        # Validate position (throws InvalidPosition if it's not)
        tile = self.__board.get_tile(position)

        # Make sure it is not a hole
        if tile.is_hole:
            raise InvalidPosition('Cannot place avatar on a Hole!')

        # Make sure target position is reachable from current position
        current_pos = self.__placements.get(player_id)
        reachable_pos = self.__board.get_reachable_positions(current_pos)

        if position not in reachable_pos:
            raise InvalidPosition('Target position is not reachable from'
                                  ' player\'s current position!')

        # Update position
        self.__placements.update({player_id: position})

    def can_anyone_move(self) -> bool:
        """
        Tells if any player can perform a move.
        :return: boolean indicating whether anyone
                 can move
        """
        # Cycle over placements see if any move is possible
        # from current position
        for _, position in self.__placements.items():
            if len(self.__board.get_reachable_positions(position)) > 0:
                return True
        # If we haven't returned thus far, no positions are reachable
        # for anyone
        return False
