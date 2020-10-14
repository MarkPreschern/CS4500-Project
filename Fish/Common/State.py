from Board import Board
from Player import Player
from Avatar import Avatar
from Color import Color
import constants as ct
from collections import OrderedDict
import tkinter as tk

from exceptions.AvatarAlreadyPlacedException import AvatarAlreadyPlacedException
from exceptions.AvatarNotPlacedException import AvatarNotPlacedException
from exceptions.InvalidPositionException import InvalidPositionException
from SpriteManager import SpriteManager
from exceptions.NonExistentAvatarException import NonExistentAvatarException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.UnclearPathException import UnclearPathException


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

        # Initialize placements
        self.__placements = {}  # key = avatar id, value = position tuple

        # Create player dictionary keyed by player ids w/ Player values
        self.__players = OrderedDict()

        # Create an avatar dictionary keyed by avatar ids w/ Avatar values
        self.__avatars = dict()

        # Sort player list in increasing order of age
        players.sort(key=lambda p: p.age)

        # Determine # no avatars per player
        self.__avatars_per_player = 6 - len(players)

        # Insert players in the order they go
        for player in players:
            # Add player to collection
            self.__players.update({player.id: player})
            # Create avatars for player
            self.__create_avatars(player_id=player.id, color=player.color)

    def __create_avatars(self, player_id: int, color: Color) -> None:
        """
        Generates avatars of provided color for given player id.
        :param player_id: player id to create avatars for
        :param color: color in which to render avatars
        :return: None
        """
        # Generate avatars to spec
        for _ in range(self.__avatars_per_player):
            # Come up with next available avatar id
            avatar_id = len(self.__avatars)
            # Create avatar
            avatar = Avatar(id=avatar_id, player_id=player_id, color=color)
            self.__avatars.update({avatar.id: avatar})

    def place_avatar(self, avatar_id: int, position: tuple) -> None:
        """
        Places an avatar on behalf of the player with the specified
        id at the specified location if it is not a hole.

        :param avatar_id: avatar id (unique with respect to the player)
        :param position: tuple position to place avatar
        :return: None
        """
        # Validate type of avatar_id
        if not isinstance(avatar_id, int) or avatar_id < 0:
            raise TypeError('Expected integer >= 0 for avatar id!')

        # Validate type of position
        if not isinstance(position, tuple):
            raise TypeError('Expected tuple for position id!')

        # Make sure player has not already placed avatar w/ id avatar_id
        if avatar_id in self.__placements:
            raise AvatarAlreadyPlacedException()

        if avatar_id not in self.__avatars.keys():
            raise NonExistentAvatarException()

        # Make sure target position is not occupied by another player or
        # a hole
        if self.__is_position_occupied_or_hole(position):
            raise InvalidPositionException("Position already occupied or hole!")

        # Update placement to reflect updated avatar's position
        self.__placements.update({avatar_id: position})

    def __is_position_occupied_or_hole(self, position: (int, int)) -> bool:
        """
        Returns true if given position is either a hole or occupied
        by another avatar.
        :param position: position to check
        :return: boolean indicating if condition above is fulfilled
        """
        if not isinstance(position, tuple):
            raise TypeError('Expected tuple for position!')

        # Check if tile is a hole
        if self.__board.get_tile(position).is_hole:
            return True

        # Check if an avatar is at position
        if position in self.__placements.values():
            return True

        return False

    def move_avatar(self, avatar_id: int, position: tuple) -> None:
        """
        Moves an avatar on behalf of the player with the specified
        id to the specified location if said location is reachable
        and not a hole.

        :param avatar_id: id of avatar to mvoe
        :param position: tuple position to move avatar
        :return: None
        """
        # Validate type of player id
        if not isinstance(avatar_id, int) or avatar_id < 0:
            raise TypeError('Expected integer for avatar id!')

        # Make sure player id is in player list
        if avatar_id not in self.__avatars.keys():
            raise ValueError('Avatar id not in avatar list!')

        # Make sure player has already placed their avatar
        if avatar_id not in self.__placements:
            raise AvatarNotPlacedException()

        # Validate type of position
        if not isinstance(position, tuple):
            raise TypeError('Expected tuple for position!')

        # Retrieve avatar's current position
        current_pos = self.__placements.get(avatar_id)

        # Check if path to target position is clear
        if not self.__is_path_clear(current_pos, position):
            raise UnclearPathException('Target position cannot be reached!')

        # Update position
        self.__placements.update({avatar_id: position})

    def __is_path_clear(self, pos1, pos2) -> bool:
        """
        Checks if the path is clear of holes and avatars
        from pos1 to pos2.
        :param pos1: start position
        :param pos2: end position
        :return: boolean indicating if condition is fulfilled
        """
        if not isinstance(pos1, tuple):
            raise TypeError('Expected tuple for pos1!')

        if not isinstance(pos2, tuple):
            raise TypeError('Expected tuple for pos2!')

        # Retrieve all reachable positions from pos1
        reachable_pos = self.__board.get_reachable_positions(pos1)

        # Check if pos2 is among said positions
        if pos2 not in reachable_pos:
            return False

        # Retrieve all in-between positions between pos1 and pos2, including
        # the latter
        positions_to_check = self.__board.get_connecting_positions(pos1, pos2)
        positions_to_check.append(pos2)

        # For each in-between position
        for pos in positions_to_check:
            # Check if an avatar has been placed on current position
            if pos in self.__placements.values():
                return False

        return True

    def can_player_move(self, player_id: int) -> bool:
        """
        Tells if player with given player_id can perform a move.
        :return: boolean indicating whether anyone
                 can move
        """
        # Validate player_id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive int for player_id!')

        # Make sure player_id is in player collection
        if player_id not in self.__players.keys():
            raise NonExistentPlayerException()

        # Get avatar ids for this player
        avatar_ids = self.get_avatars_by_player_id(player_id)

        # Cycle over avatar ids
        for avatar_id in avatar_ids:
            # Make sure player has already placed their avatar
            if avatar_id not in self.__placements:
                # Cannot move until player has placed all their
                # avatars
                return False

            # Retrieve avatar position for this avatar
            avatar_pos = self.__placements.get(avatar_id)

            # Retrieve all reachable positions for this position2
            reachable_pos = self.__board.get_reachable_positions(avatar_pos)

            # Make sure at least one path is clear
            for pos in reachable_pos:
                if self.__is_path_clear(avatar_pos, pos):
                    return True

        # If we haven't returned thus far, no positions are reachable
        # for anyone
        return False

    def get_avatars_by_player_id(self, player_id: int) -> [int]:
        """
        Returns a list of ids pertaining to
        avatars owned by the provided player.
        :param player_id: id of player for whom to retrieve
                          avatar
        """
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        # Create collection in which to store avatar ids
        avatar_ids = []

        # Cycle over avatar collection and store avatar ids
        # belonging to player to array
        for avatar_id, avatar in self.__avatars.items():
            if avatar.player_id == player_id:
                avatar_ids.append(avatar_id)

        return avatar_ids

    def __get_player_by_avatar_id(self, avatar_id) -> Player:
        """
        Retrieves player by way of provided avatar_id.
        :param avatar_id: avatar id used to retrieve player
        :return: Player object
        """
        if not isinstance(avatar_id, int) and avatar_id < 0:
            raise TypeError('Expected integer >= 0 for avatar_id!')

        # Make sure avatar id is registered
        if avatar_id not in self.__avatars:
            raise NonExistentAvatarException()

        player_id = self.__avatars.get(avatar_id).player_id

        # Make sure player id is registered
        if player_id not in self.__players:
            raise NonExistentPlayerException()

        return self.__players.get(player_id)

    def render(self, parent_frame):
        """
        Renders game state to provided Frame.
        :param parent_frame: frame to render board on
        :return: resulting Canvas object
        """
        # Validate params
        if not isinstance(parent_frame, tk.Frame):
            raise TypeError('Expected Frame for parent_frame!')

        # Calculate frame width and height based on board size
        frame_w = (self.__board.cols * 2 - 1) * ct.DELTA \
                  + ct.TILE_WIDTH + ct.MARGIN_OFFSET
        frame_h = (self.__board.rows - 1) * ct.TILE_HEIGHT / 2 \
                  + ct.TILE_HEIGHT + ct.MARGIN_OFFSET * 2

        # Make up frame
        frame = tk.Frame(parent_frame, width=frame_w, height=frame_h)
        # Set window to use grid view
        frame.grid(row=0, column=0)

        # Render board and retrieve canvas on which it was rendered
        canvas = self.__board.render(frame)

        # Render players to board
        for avatar_id, pos in self.__placements.items():
            # Retrieve player
            player = self.__get_player_by_avatar_id(avatar_id)
            # Retrieve sprite's name based on avatar color
            player_sprite_name = player.color.name.lower()

            # Demultiplex avatar position into x & y
            avatar_x, avatar_y = pos

            print(avatar_x, avatar_y)
            # Figure out avatar x y
            sprite_x_offset = ct.TILE_WIDTH / 2 - ct.AVATAR_WIDTH / 2 + ct.MARGIN_OFFSET

            sprite_x = (0 if avatar_x % 2 == 0 else ct.DELTA) + (2 * ct.DELTA * avatar_y) + sprite_x_offset
            sprite_y = avatar_x * ct.TILE_HEIGHT / 2 + ct.MARGIN_OFFSET

            # Figure out avatar's name x y
            avatar_name_x = sprite_x + ct.AVATAR_WIDTH / 2.0
            avatar_name_y = sprite_y + ct.AVATAR_HEIGHT + ct.MARGIN_OFFSET

            # Add avatar
            canvas.create_image(sprite_x, sprite_y, image=SpriteManager.get_sprite(player_sprite_name),
                                anchor=tk.NW)

            # Add avatar name
            canvas.create_text(avatar_name_x, avatar_name_y, fill="black", font="Arial 10",
                               text=f'{player.name}[{avatar_id}]')
