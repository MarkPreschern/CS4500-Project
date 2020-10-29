import copy
import pickle
import tkinter as tk
from collections import deque

import constants as ct
from action import Action
from board import Board
from color import Color
from exceptions.InvalidActionException import InvalidActionException
from exceptions.InvalidPositionException import InvalidPositionException
from exceptions.MoveOutOfTurnException import MoveOutOfTurnException
from exceptions.NonExistentPlayerException import NonExistentPlayerException
from exceptions.UnclearPathException import UnclearPathException
from player import Player
from position import Position
from sprite_manager import SpriteManager


class State(object):
    """
    State represents the current state of a game: the state of the board,
    the current list of players along with their id, name, color and penguin
    placements, and the order in which they play. More generally speaking,
    a game state represents a complete snapshot of a game in time.
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

        # Check player list length
        if len(players) == 0:
            raise ValueError(f'Players list cannot be empty')

        # Make sure list consists of only player objects
        if not all(isinstance(x, Player) for x in players):
            raise TypeError('All player list objects have to of type Player!')

        # Make sure we weren't given too many players
        if len(players) < ct.MIN_PLAYERS or len(players) > ct.MAX_PLAYERS:
            raise ValueError(f'Invalid player length; length has to be between {ct.MIN_PLAYERS} and'
                             f' {ct.MAX_PLAYERS}')

        # Initialize players to array of players arranged in the order they go
        self.__players = players

        # Set board
        self.__board = board

        # Initialize cache for all possible actions as a list of Action objects
        self.__all_possible_actions_cache = []

        # Determine # no avatars per player
        self.__avatars_per_player = 6 - len(players)

        # Make up log of moves that have been made since the beginning
        # of the game
        self.__move_log = []

        # Make up cache of stuck player ids
        self.__player_stuck_cache = []

    def deepcopy(self) -> 'State':
        """
        Returns a 'deep-copy' of the state.
        """
        # Copy board
        board = pickle.loads(pickle.dumps(self.__board))
        # Copy players
        players = pickle.loads(pickle.dumps(self.__players))

        # Return new copy of state
        return State(board, players)

    @property
    def stuck_players(self) -> [int]:
        """
        Returns a list of ids who belong to players that are stuck (or
        cannot move any of their penguins). This list is actualized at the
        very least at end of each turn.
        """
        return self.__player_stuck_cache.copy()

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
        return pickle.loads(pickle.dumps(self.__board))

    @property
    def placements(self) -> []:
        """
        Returns an immutable copy of placements.
        """
        # Initialize dict of player id to Position object
        placements = {}

        # Cycles over players and add their placements to the list
        for p in self.__players:
            placements.update({p.id: p.places})

        return placements

    @property
    def current_player(self) -> int:
        """
        Returns the id of the player whose turn it is.
        """
        return self.__players[0].id

    def get_possible_actions(self) -> []:
        """
        Returns a list of all possible moves for the current
        player.

        :return: list of Action objects
        """
        # Initialize collection of possible moves
        possible_moves = []

        # Get player's placements
        player_placements = self.get_player_by_id(self.current_player).places

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

    def __trigger_next_turn(self, initial_shift=1):
        """
        Triggers next turn by giving the next player in the
        player order a turn.

        :param initial_shift: number of times to shift player order
                             to the left from the get-go. A value of
                             one means that the current player goes to
                             the end of the order.
        :return: None
        """
        # Do not change turn if no one can move
        if not self.can_anyone_move():
            return

        # Shift players collection in a deque
        players_deque = deque(self.__players)
        players_deque.rotate(-initial_shift)

        # Initialize actual shift amount
        shift_amount = 0

        # Find next player whose turn it is
        for player in players_deque:
            # If player is stuck, skip 'em over
            if self.__is_player_stuck(player.id):
                shift_amount += 1
                continue
            break

        # Rotate as needed to get to the next player that can move
        players_deque.rotate(-shift_amount)
        # Update actual players collection
        self.__players = list(players_deque)

    @property
    def player_order(self):
        """
        Returns list of ids of all players in the game in the order
        they go starting with the current player's id.
        """
        return [p.id for p in self.__players]

    def get_player_by_id(self, player_id: int) -> Player:
        """
        Retrieves player object by the provided id if it exists.
        Otherwise it returns throws NonExistentPlayerException.

        :param: id of player to retrieve
        :return: Player object
        """
        # Validate params
        if not isinstance(player_id, int):
            raise TypeError('Expected int for player_id!')

        # Cycle over players in search for the one with the
        # provided id
        for p in self.__players:
            if p.id == player_id:
                return p

        raise NonExistentPlayerException()

    def get_player_score(self, player_id: int) -> int:
        """
        Gets provided player's score or throws
        NonExistentPlayerException() if player does not exist.

        :param player_id: id of player whose score
                          to retrieve
        :return: score
        """
        # Validate player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        return self.get_player_by_id(player_id).score

    def get_player_positions(self, player_id: int) -> [Position]:
        """
        Gets provided player's positions or throws
        NonExistentPlayerException() if player does not exist.

        :param player_id: id of player whose positions
                          to retrieve
        :return: player's position
        """
        # Validate player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        return self.get_player_by_id(player_id).places

    def get_player_color(self, player_id: int) -> Color:
        """
        Gets provided player's color or throws
        NonExistentPlayerException() if player does not exist.

        :param player_id: id of player whose color
                          to retrieve
        :return: player's color
        """
        # Validate player id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive integer for player_id!')

        return self.get_player_by_id(player_id).color

    def place_avatar(self, player_id: int, position: Position) -> None:
        """
        Places an avatar on behalf of the given player id at
        the specified location if it is not a hole.

        :param player_id: id of player to place avatar for
        :param position: position to place avatar
        :return: None
        """
        # Validate type of player_id
        if not isinstance(player_id, int):
            raise TypeError('Expected int for player id!')

        # Validate type of position
        if not isinstance(position, Position):
            raise TypeError('Expected Position for position id!')

        # Make sure target position is not occupied by another player or
        # a hole
        if not self.is_position_open(position):
            raise InvalidPositionException("Position already occupied or hole!")

        # Make sure there are still avatars to place
        if self.has_everyone_placed():
            raise InvalidActionException()

        # Make sure player exists
        if player_id not in self.player_order:
            raise NonExistentPlayerException()

        # Update placement to reflect updated avatar's position
        self.get_player_by_id(player_id).add_place(position)

        # Make sure a player that can move is up
        self.__trigger_next_turn(0)

    def is_position_open(self, position: Position) -> bool:
        """
        Returns false if given position is either a hole or occupied
        by another avatar. Otherwise, it returns true.

        :param position: position to check
        :return: boolean indicating if condition above is fulfilled
        """
        if not isinstance(position, Position):
            raise TypeError('Expected Position for position!')

        # Check if position is within bounds
        if position.x >= self.__board.rows or position.y >= self.__board.cols:
            raise InvalidPositionException('Outside the bounds of the board!')

        # Check if tile is a hole
        if self.__board.get_tile(position).is_hole:
            return False

        # Check if an avatar is at position
        for placement_arr in self.placements.values():
            if position in placement_arr:
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

        # Get player id for src
        player_id = self.__whose_avatar(src)

        # Make sure there is an avatar at src
        if player_id == -1:
            raise InvalidActionException()

        # Make sure it is the current player
        if self.current_player != player_id:
            raise MoveOutOfTurnException(f'avatar belongs to player id {player_id} '
                                         f'current player id: {self.current_player}')

        # Adjust player score
        self.get_player_by_id(player_id).score += self.__board.get_tile(src).fish_no

        # Swap out old avatar position for new
        self.get_player_by_id(player_id).swap_places(src, dst)

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

        # Get player id whose avatar exists at src
        for player in self.__players:
            # If src is among this player's placements, return id
            if pos in player.places:
                return player.id

        return -1

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
            # Cycle over placements of each player
            for player_placements in self.placements.values():
                # Check if an avatar has been placed on current position
                if pos in player_placements:
                    return False

        return True

    def has_everyone_placed(self) -> bool:
        """
        Returns boolean indicating if everyone has placed their
        avatars.
        :return: resulting boolean
        """
        # Initialize counter
        placement_count = 0

        # Cycle over player placements and add to count
        for player_placements in self.placements.values():
            placement_count += len(player_placements)

        return placement_count == self.__avatars_per_player \
               * len(self.__players)

    def can_anyone_move(self) -> bool:
        """
        Tells if any player can move any of their avatars.

        :return: boolean indicating whether anyone can move
        """
        # Cycle over players and return true if any of them
        # can move
        for player_id in self.player_order:
            if not self.__is_player_stuck(player_id):
                return True

        return False

    def __is_player_stuck(self, player_id: int) -> bool:
        """
        Tells if player with given player_id can go anywhere. It does
        not check for turn. Can only be called after everyone has
        finished placing their avatars.

        :param player_id: id of player for whom to check
        :return: boolean indicating whether player
                 can move (not necessarily this turn)
        """
        # Validate player_id
        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expected positive int for player_id!')

        # Make sure player_id is in player collection
        if player_id not in self.player_order:
            raise NonExistentPlayerException()

        # See if player is in "forever-stuck" cache
        if player_id in self.__player_stuck_cache:
            return True

        # Retrieve player's positions
        player_positions = self.get_player_by_id(player_id).places

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
        for player_obj in self.__players:
            # Retrieve sprite's name based on avatar color
            player_sprite_name = player_obj.color.name.lower()
            player_id = player_obj.id

            # Cycle over player's positions
            for pos in player_obj.places:
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
                                   text=f'{player_obj.name}[{player_id}]')
