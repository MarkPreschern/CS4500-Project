from Board import Board
from Player import Player
from Avatar import Avatar
from Color import Color
import constants as ct
from collections import OrderedDict
import tkinter as tk
from itertools import cycle

from Position import Position
from exceptions.AvatarAlreadyPlacedException import AvatarAlreadyPlacedException
from exceptions.AvatarNotPlacedException import AvatarNotPlacedException
from exceptions.GameNotStartedException import GameNotStartedException
from exceptions.InvalidPositionException import InvalidPositionException
from SpriteManager import SpriteManager
from exceptions.MoveOutOfTurnException import MoveOutOfTurnException
from exceptions.NoMoreTurnsException import NoMoreTurnsException
from exceptions.NonExistentAvatarException import NonExistentAvatarException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.PlaceOutOfTurnException import PlaceOutOfTurnException
from exceptions.UnclearPathException import UnclearPathException


class State(object):
    """
    State represents the current state of a game: the state of the board,
    the current placements of the penguins, knowledge about the players,
    and the order in which they play. More generally speaking, a game state
    represents a complete snapshot of a game in time.
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
        self.__placements = {}  # key = avatar id, value = Position obj

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

        # Create a circular list of player ids in order in which they go
        self.__player_order = cycle(list(self.__players.keys()))

        # Define variable to keep track of whose turn it is by player_id.
        # It is initialized to be the first player in the collection's id
        # as the collection is sorted in increasing order of age.
        self.__current_player_id = next(self.__player_order)

        # Indicates whether everyone has finished placing their avatar
        # and the game has started
        self.__game_started = False

    @property
    def current_player(self) -> int:
        """
        Returns the id of the player whose turn it is.
        """
        return self.__current_player_id

    @property
    def game_started(self) -> bool:
        """
        Returns a boolean indicating if game has started.
        """
        return self.__game_started

    def get_possible_actions(self) -> []:
        """
        Returns a list of all possible moves for the current
        player.

        :return: list of Position tuples, where each tuple is made up of
                 an origin and a destination Position object.
        """
        # Retrieve current players' avatars' ids
        avatar_ids = self.__get_avatar_ids_by_player_id(self.__current_player_id)

        # Initialize collection of possible moves
        possible_moves = []

        # Cycle over player's avatar ids
        for avatar_id in avatar_ids:
            # Get current avatar's position
            avatar_pos = self.__placements.get(avatar_id)

            # Determine all reachable positions for avatar_pos
            reachable_positions = self.__board.get_reachable_positions(avatar_pos)

            # Create possible move for position reachable from avatar's
            # current position
            for pos in reachable_positions:
                possible_moves.extend((avatar_pos, pos))

        return possible_moves

    def __trigger_next_turn(self):
        """
        Triggers next turn by giving the next player
        a turn.
        """
        # Check if game over
        if not self.can_anyone_move() and self.__game_started:
            raise NoMoreTurnsException()

        # Cycle over ordered circular list until a player who
        # can move or is still placing has been found
        for player_id in self.__player_order:
            if not self.__game_started:
                self.__current_player_id = player_id
                break
            elif self.__game_started and self.can_player_move(player_id):
                self.__current_player_id = player_id
                break

    def get_player_order(self) -> []:
        """
        Returns the order in which the players go in
        a sorted collection of player ids.
        """
        return list(self.__players.keys())

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

    def place_avatar(self, position: Position) -> None:
        """
        Places an avatar on behalf of the current player with at
        the specified location if it is not a hole.

        :param position: position to place avatar
        :return: None
        """
        # Validate type of position
        if not isinstance(position, Position):
            raise TypeError('Expected Position for position id!')

        # Make sure target position is not occupied by another player or
        # a hole
        if self.__is_position_occupied_or_hole(position):
            raise InvalidPositionException("Position already occupied or hole!")

        # Get current player's avatar ids
        avatar_ids = self.__get_avatar_ids_by_player_id(self.__current_player_id)

        # Initialize place holder for id of avatar to place
        avatar_id_to_place = None

        # Find current player the next available avatar they can place
        for avatar_id in avatar_ids:
            # If this avatar has not been placed, use it
            if avatar_id not in self.__placements.keys():
                avatar_id_to_place = avatar_id
                break

        # If not avatar can be placed, throw error
        if avatar_id_to_place is None:
            raise NonExistentAvatarException()

        # Update placement to reflect updated avatar's position
        self.__placements.update({avatar_id_to_place: position})

        # If everyone has placed, start game
        if self.__has_everyone_placed():
            self.__game_started = True

        # Trigger next turn
        self.__trigger_next_turn()

    def __is_position_occupied_or_hole(self, position: Position) -> bool:
        """
        Returns true if given position is either a hole or occupied
        by another avatar.
        :param position: position to check
        :return: boolean indicating if condition above is fulfilled
        """
        if not isinstance(position, Position):
            raise TypeError('Expected Position for position!')

        # Check if tile is a hole
        if self.__board.get_tile(position).is_hole:
            return True

        # Check if an avatar is at position
        if position in self.__placements.values():
            return True

        return False

    def move_avatar(self, src: Position, dst: Position) -> None:
        """
        Moves an avatar on behalf of the current player from src to dst.
        If the player does not have an avatar at src, an error occurs.

        :param src: position from which to move player's avatar
        :param dst: position to which to move player's avatar
        :return: None
        """
        # Validate src
        if not isinstance(src, Position):
            raise TypeError('Expected Position for src!')

        # Validate dst
        if not isinstance(dst, Position):
            raise TypeError('Expected Position for dst!')

        # Check if path to target position is clear
        if not self.__is_path_clear(src, dst):
            raise UnclearPathException('Target position cannot be reached!')

        # Retrieve current player's avatar ids
        avatar_ids = self.__get_avatar_ids_by_player_id(self.__current_player_id)

        # Initialize flag to indicate whether avatar has been found
        found_avatar = False

        # Cycle over player's avatar ids
        for avatar_id in avatar_ids:
            # Check if current avatar is positioned at src
            if self.__placements.get(avatar_id) == src:
                # Update position
                self.__placements.update({avatar_id: dst})
                # Replace previous position on the board with a hole
                self.__board.remove_tile(src)
                # Set flag to indicate that an avatar has been found
                found_avatar = True

                # Trigger next turn
                self.__trigger_next_turn()

        # If we have not found an avatar that belongs to the player
        # at that position, throw an error
        if not found_avatar:
            raise NonExistentAvatarException()

    def __is_path_clear(self, pos1: Position, pos2: Position) -> bool:
        """
        Checks if the path is clear of holes and avatars
        from pos1 to pos2.

        :param pos1: start position
        :param pos2: end position
        :return: boolean indicating if condition is fulfilled
        """
        if not isinstance(pos1, Position):
            raise TypeError('Expected Position for pos1!')

        if not isinstance(pos2, Position):
            raise TypeError('Expected Position for pos2!')

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

    def __has_everyone_placed(self) -> bool:
        """
        Returns boolean indicating if everyone has placed their
        avatars.
        :return: resulting boolean
        """

        return len(self.__placements) == self.__avatars_per_player * len(self.__players)

    def can_anyone_move(self) -> bool:
        """
        Tells if any player can move any of their avatars.
        :return: boolean indicating whether anyone can move
        """
        # If the game hasn't started, no one can move
        if not self.__game_started:
            return False

        # Cycle over players and return true if any of them
        # can move
        for player_id in self.__players.keys():
            if self.can_player_move(player_id):
                return True

        return False

    def can_player_move(self, player_id: int) -> bool:
        """
        Tells if player with given player_id can perform a move.
        :param player_id: id of player for whom to check
        :return: boolean indicating whether player
                 can move
        """
        # Validate player_id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive int for player_id!')

        # Make sure player_id is in player collection
        if player_id not in self.__players.keys():
            raise NonExistentPlayerException()

        # If the game hasn't started, no one can move
        if not self.__game_started:
            return False

        # Get avatar ids for this player
        avatar_ids = self.__get_avatar_ids_by_player_id(player_id)

        # Cycle over avatar ids
        for avatar_id in avatar_ids:
            # Make sure player has already placed their avatar
            if avatar_id not in self.__placements:
                # Cannot move until player has placed all their
                # avatars
                return False

            # Retrieve avatar position for this avatar
            avatar_pos = self.__placements.get(avatar_id)

            # Retrieve all reachable positions from this position
            reachable_pos: [Position] = self.__board.get_reachable_positions(avatar_pos)

            # Make sure at least one path is clear
            for pos in reachable_pos:
                if self.__is_path_clear(avatar_pos, pos):
                    return True

        # If we haven't returned thus far, no positions are reachable
        # for anyone
        return False

    def __get_avatar_ids_by_player_id(self, player_id: int) -> [int]:
        """
        Returns a list of avatar ids owned by the player with provided
        id.

        :param player_id: id of player for whom to retrieve
                          avatar
        :return: list of avatar ids
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

    def __get_player_by_avatar_id(self, avatar_id: int) -> Player:
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

    def render(self, parent_frame: tk.Frame):
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

            # De-multiplex avatar position into x & y
            avatar_x, avatar_y = pos

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
