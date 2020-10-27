import copy
import tkinter as tk
from collections import OrderedDict, deque
from itertools import cycle

import constants as ct
from action import Action
from board import Board
from color import Color
from exceptions.GameNotRunningException import GameNotRunningException
from exceptions.InvalidActionException import InvalidActionException
from exceptions.InvalidPositionException import InvalidPositionException
from exceptions.MoveOutOfTurnException import MoveOutOfTurnException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.UnclearPathException import UnclearPathException
from game_status import GameStatus
from player import Player
from position import Position
from sprite_manager import SpriteManager


class State(object):
    """
    State represents the current state of a game: the state of the board,
    the current placements of the penguins, knowledge about the players,
    and the order in which they play. More generally speaking, a game state
    represents a complete snapshot of a game in time.
    """

    def __init__(self, board: Board, players: [Player]):
        """
        Initializes a State object with the given board and player list.

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

        # Initialize placements as a dictionary that maps player ids to a array
        # of avatar positions
        self.__placements = {}

        # Initialize cache for all possible actions as a list of Action objects
        self.__all_possible_actions_cache = []

        # Create player dictionary keyed by player ids w/ Player values
        self.__players = OrderedDict()

        # Sort player list in increasing order of age
        players.sort(key=lambda p: p.age)

        # Determine # no avatars per player
        self.__avatars_per_player = 6 - len(players)

        # Insert players in the order they go
        for player in players:
            # Add player to collection
            self.__players.update({player.id: player})
            # Initialize player's placements
            self.__placements.update({player.id: []})

        # Create a circular list of player ids in order in which they go
        self.__player_order = cycle(list(self.__players.keys()))

        # Define variable to keep track of whose turn it is by player_id.
        # It is initialized to be the first player in the collection's id
        # as the collection is sorted in increasing order of age.
        self.__current_player_id = next(self.__player_order)

        # Indicates the status of the game (placing / running / over)
        self.__game_status = GameStatus.PLACING

        # Make up log of moves that have been made since the beginning
        # of the game
        self.__move_log = []

        # Make up cache of stuck player ids
        self.__player_stuck_cache = []

    @property
    def stuck_players(self) -> [int]:
        return self.__player_stuck_cache

    @property
    def avatars_per_player(self) -> int:
        """
        Returns the number of avatars each player
        started with.
        """
        return self.__avatars_per_player

    @property
    def players_no(self) -> int:
        """
        Returns the number of players currently in the game.
        """
        return len(self.__players)

    @property
    def move_log(self) -> []:
        """
        Returns immutable list of actions that have been made since the beginning
        of the game.
        """
        return copy.copy(self.__move_log)

    @property
    def board(self) -> []:
        """
        Returns an immutable copy of the board.
        """
        return copy.deepcopy(self.__board)

    @property
    def placements(self) -> []:
        """
        Returns an immutable copy of placements.
        """
        return copy.copy(self.__placements)

    @property
    def current_player(self) -> int:
        """
        Returns the id of the player whose turn it is.
        """
        return self.__current_player_id

    @property
    def game_status(self) -> GameStatus:
        """
        Returns the status of the game (whether it is in a
        placing, running or over state).
        """
        return self.__game_status

    def get_possible_actions(self) -> []:
        """
        Returns a list of all possible moves for the current
        player assuming that the game is running.

        :return: list of Action objects
        """
        if self.__game_status != GameStatus.RUNNING:
            return []

        # Initialize collection of possible moves
        possible_moves = []

        # Get player's placements
        player_placements = self.__placements.get(self.__current_player_id)

        # Cycle over each avatar position
        for position in player_placements:
            # Determine all reachable positions for avatar_pos
            reachable_positions = self.__board.get_reachable_positions(position)

            # Create possible move for position reachable from avatar's
            # current position
            for pos in reachable_positions:
                # Check if path is clear
                if not self.__is_path_clear(position, pos, reachable_positions):
                    continue

                possible_moves.append(Action(position, pos))

        # Set cache
        self.__all_possible_actions_cache = possible_moves

        return possible_moves

    def __trigger_next_turn(self):
        """
        Triggers next turn by giving the next player
        a turn.
        """
        # Check if game over
        if self.__game_status == GameStatus.OVER:
            return

        # Check if another turn is warranted, otherwise call it a game.
        if not self.can_anyone_move() and self.__game_status == GameStatus.RUNNING:
            self.__game_status = GameStatus.OVER
            return

        # Cycle over ordered circular list until a player who
        # can move or is still placing has been found
        for player_id in self.__player_order:
            if self.__game_status == GameStatus.PLACING:
                self.__current_player_id = player_id
                break
            elif not self.__is_player_stuck(player_id):
                self.__current_player_id = player_id
                break

    def get_player_order(self) -> []:
        """
        Returns the order in which the players go in
        a sorted collection of player ids.
        """
        # Come up with original sorting of player ids
        original_sorting = list(self.__players.keys())

        # Find the current player id in the original sorting
        n = original_sorting.index(self.__current_player_id)

        # Rotate original sorting to get current sorting
        # based on the current player
        dl = deque(original_sorting)
        # Rotate left
        dl.rotate(-n)

        return list(dl)

    def get_player_score(self, player_id: int) -> int:
        """
        Gets provided player's score.

        :param player_id: id of player whose score
                          to retrieve
        :return: score
        """
        # Validate player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        if player_id not in self.__players.keys():
            raise NonExistentPlayerException()

        return self.__players.get(player_id).score

    def get_player_positions(self, player_id: int) -> [Position]:
        """
        Gets provided player's positions.

        :param player_id: id of player whose positions
                          to retrieve
        :return: player's position
        """
        # Validate player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        # Make sure this player is actually in the game
        if player_id not in self.__placements.keys():
            raise NonExistentPlayerException()

        return self.__placements.get(player_id)

    def get_player_color(self, player_id: int) -> Color:
        """
        Gets provided player's color.

        :param player_id: id of player whose color
                          to retrieve
        :return: player's color
        """
        # Validate player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        # Make sure this player is actually in the game
        if player_id not in self.__players.keys():
            raise NonExistentPlayerException()

        return self.__players.get(player_id).color

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
        if not self.is_position_open(position):
            raise InvalidPositionException("Position already occupied or hole!")

        # Make sure there are still avatars to place
        if self.__has_everyone_placed():
            raise InvalidActionException()

        # Update placement to reflect updated avatar's position
        self.__placements[self.__current_player_id].append(position)

        # If everyone has placed, start game
        if self.__has_everyone_placed():
            self.__game_status = GameStatus.RUNNING

        # Trigger next turn
        self.__trigger_next_turn()

    def is_position_open(self, position: Position) -> bool:
        """
        Returns false if given position is either a hole or occupied
        by another avatar.
        :param position: position to check
        :return: boolean indicating if condition above is fulfilled
        """
        if not isinstance(position, Position):
            raise TypeError('Expected Position for position!')

        # Check if tile is a hole
        if self.__board.get_tile(position).is_hole:
            return False

        # Check if an avatar is at position
        for placements in self.__placements.values():
            if position in placements:
                return False

        return True

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

        # If action is not cache as valid, validate
        if Action(src, dst) not in self.__all_possible_actions_cache:
            # Check if path to target position is clear
            if not self.__is_path_clear(src, dst):
                raise UnclearPathException('Target position cannot be reached!')

            # Make sure everyone has placed their avatars
            if self.__game_status != GameStatus.RUNNING:
                raise GameNotRunningException()

        # Get player id for src
        player_id = self.__whose_avatar(src)

        # Make sure there is an avatar at src
        if player_id == -1:
            raise InvalidActionException()

        # Make sure it is the current player
        if self.__current_player_id != player_id:
            raise MoveOutOfTurnException(f'avatar belongs to player id {player_id} '
                                         f'current player id: {self.__current_player_id}')

        # Adjust player score
        self.__players[self.__current_player_id].score += self.__board.get_tile(src).fish_no

        # Swap out old avatar position for new
        self.__placements[player_id][self.__placements[player_id].index(src)] = dst
        # Clear cache for all possible actions
        self.__all_possible_actions_cache.clear()

        # Remove board tile
        self.__board.remove_tile(src)
        # Record move
        self.__move_log.append(Action(src, dst))
        # Trigger next turn
        self.__trigger_next_turn()

    def __whose_avatar(self, pos: Position) -> int:
        """
        Returns the id of the player to whom the avatar
        on the given position belongs.

        :param pos: position avatar is one
        :return: returns player id or -1 to indicate that nobody
                 has an avatar placed at that position
        """
        # Validate position
        if not isinstance(pos, Position):
            raise TypeError('Expected Position for pos!')

        # Initialize player id at place holder
        player_id = -1
        # Get player id whose avatar exists at src
        for pid, placements in self.__placements.items():
            # If src is among this player's placements, set id
            if pos in placements:
                player_id = pid
                break

        return player_id

    def __is_path_clear(self, pos1: Position, pos2: Position, reachable_pos=None) -> bool:
        """
        Checks if the path is clear of holes and avatars
        from pos1 to pos2.

        :param pos1: start position
        :param pos2: end position
        :param reachable_pos: optional list of all reachables positions from pos1
        :return: boolean indicating if condition is fulfilled
        """
        if not isinstance(pos1, Position):
            raise TypeError('Expected Position for pos1!')

        if not isinstance(pos2, Position):
            raise TypeError('Expected Position for pos2!')

        if reachable_pos is not None and not isinstance(reachable_pos, list):
            raise TypeError('Expected list of Position for reachable_pos or None!')

        # Check if reachable pos is provided
        if not reachable_pos:
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
            if pos in self.__get_all_avatar_positions():
                return False

        return True

    def __get_all_avatar_positions(self) -> []:
        """
        Returns a list of all avatar Position objects.
        """
        positions = []

        for placements in self.__placements.values():
            positions.extend(placements)

        return positions

    def __has_everyone_placed(self) -> bool:
        """
        Returns boolean indicating if everyone has placed their
        avatars.
        :return: resulting boolean
        """

        return len(self.__get_all_avatar_positions()) == self.__avatars_per_player \
               * len(self.__players)

    def can_anyone_move(self) -> bool:
        """
        Tells if any player can move any of their avatars.
        :return: boolean indicating whether anyone can move
        """
        # If the game hasn't started, no one can move
        if self.__game_status != GameStatus.RUNNING:
            return False

        # Cycle over players and return true if any of them
        # can move
        for player_id in self.__players.keys():
            if not self.__is_player_stuck(player_id):
                return True

        return False

    def __is_player_stuck(self, player_id: int) -> bool:
        """
        Tells if player with given player_id can go anywhere. It does
        not check for turn.

        :param player_id: id of player for whom to check
        :return: boolean indicating whether player
                 can move (not necessarily this turn)
        """
        # Validate player_id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive int for player_id!')

        # Make sure player_id is in player collection
        if player_id not in self.__players.keys():
            raise NonExistentPlayerException()

        # If the game hasn't started, no one can move
        if self.__game_status != GameStatus.RUNNING:
            return True

        # See if player is in "forever-stuck" cache
        if player_id in self.__player_stuck_cache:
            return True

        # Retrieve player's positions
        player_positions = self.__placements.get(player_id)

        # Cycle over player's positions
        for position in player_positions:
            # Retrieve all reachable positions from this position
            reachable_pos: [Position] = self.__board.get_reachable_positions(position)
            # Make sure at least one path is clear

            for pos in reachable_pos:
                if self.__is_path_clear(position, pos, reachable_pos):
                    return False

        # Cache that player is indefinitely stuck
        self.__player_stuck_cache.append(player_id)

        # If we haven't returned thus far, no positions are reachable
        return True

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
        for player_id, positions in self.__placements.items():
            # Retrieve player
            player = self.__players.get(player_id)
            # Retrieve sprite's name based on avatar color
            player_sprite_name = player.color.name.lower()

            # Cycle over player's positions
            for pos in positions:
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
                                   text=f'{player.name}[{player_id}]')
