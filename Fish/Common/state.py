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
from player_entity import PlayerEntity
from position import Position
from sprite_manager import SpriteManager


class State(object):
    """
    PURPOSE:        State represents the current state of a game: the state of the board,
                    the current list of players along with their name, color and penguin
                    placements, and the order in which they play. More generally speaking,
                    a game state represents a complete snapshot of a game in time.

    INTERPRETATION: State consists of a Board object, list of Player objects and information
                    about placements, moves and turns. The players' avatars are tracked
                    by way of the 'places' member of a Player object, which contains Position
                    objects describing where each of the player's avatars are located. These
                    locations along with the information provided by the Board determine the
                    placements and moves that can be performed.

                    The State expects a list of players sorted by age in the beginning, which it
                    then rotates throughout the game to allow the next movable player to go. A
                    player is movable if it can move any of its penguins. When a player becomes stuck
                    (or unmovable), it is skipped over meaning that no such state can exist wherein the
                    current player is stuck (with the exception of a state in which all players are stuck).
                    Upon a valid move being made, the state rotates the list of players to allow the next
                    eligible player to go.

                    On a different note, the state provides the tooling necessary to query whose turn it is,
                    whether any moves are possibles or if all avatars have been placed. This allows for a
                    referee to properly run a game and end it when needed.
    """

    def __init__(self, board: Board, players: [PlayerEntity]):
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
        if not all(isinstance(x, PlayerEntity) for x in players):
            raise TypeError('All player list objects have to of type Participant!')

        # Make up list of all player colors
        player_colors = [p.color for p in players]
        # Make sure there are no duplicate player colors
        if any(player_colors.count(color) > 1 for color in player_colors):
            raise ValueError('Player colors must unique!')

        # Initialize players to list of players arranged in the order they go. This list encompasses
        # the players along with their name, color and penguin placements (expressed using Position objects).
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

        # Make up cache of stuck player colors
        self.__player_stuck_cache = []

    def deepcopy(self) -> 'State':
        """
        Returns a 'deep-copy' of the state.

        Note: move_log contents are lost in the copy process and
        the resulting copy will not have the contents of the original.
        """
        # Copy board
        board: Board = pickle.loads(pickle.dumps(self.__board))
        # Copy players
        players: [PlayerEntity] = pickle.loads(pickle.dumps(self.__players))

        # Return new copy of state
        return State(board, players)

    @property
    def stuck_players(self) -> [int]:
        """
        Returns a list of colors who belong to players that are stuck (or
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
    def players(self) -> [PlayerEntity]:
        """
        Returns a copy of the state's list of PlayerEntity objects.
        """
        return pickle.loads(pickle.dumps(self.__players))

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
        Returns an immutable dictionary of player colors to places. Each
        value (a.k.a places) is a list of Position objects indicating
        where each player's avatar is placed on the board.
        """
        # Initialize dict of player color to Position object
        placements = {}

        # Cycles over players and add their placements to the list
        for p in self.__players:
            placements.update({p.color: p.places})

        return placements

    @property
    def current_player(self) -> Color:
        """
        Returns the color of the player whose turn it is.
        """
        return self.__players[0].color

    def remove_player(self, color: Color) -> None:
        """
        Removes player with given color from the game.
        """
        # Validate params
        if not isinstance(color, Color):
            raise TypeError('Expected Color for color!')

        # Cycle over players until one matching color is found
        for player in self.__players:
            if player.color == color:
                # Remove player
                self.__players.remove(player)
                # Recompute stuck players
                self.can_anyone_move()
                return

        # Could not find player to remove
        raise NonExistentPlayerException()

    def get_possible_actions(self) -> []:
        """
        Returns a list of all possible moves for the current
        player.

        :return: list of Action objects
        """
        # if there are no more players
        if len(self.__players) == 0:
            return []

        # Initialize collection of possible moves
        possible_moves = []

        # Get player's placements
        player_placements = self.get_player_by_color(self.current_player).places

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
            if self.__is_player_stuck(player.color):
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
        Returns list of colors of all players in the game in the order
        they go starting with the current player's color.
        """
        return [p.color for p in self.__players]

    def get_player_by_color(self, color: Color) -> PlayerEntity:
        """
        Retrieves PlayerEntity object by the provided color if it exists.
        Otherwise it returns throws NonExistentPlayerException.

        :param: color of player to retrieve
        :return: PlayerEntity object
        """
        # Validate params
        if not isinstance(color, Color):
            raise TypeError('Expected Color for color!')

        # Cycle over players in search for the one with the
        # provided color
        for p in self.__players:
            if p.color == color:
                return p

        raise NonExistentPlayerException()

    def get_player_score(self, color: Color) -> int:
        """
        Gets provided player's score or throws
        NonExistentPlayerException() if player does not exist.

        :param color: color of player whose score
                          to retrieve
        :return: score
        """
        # Validate player color
        if not isinstance(color, Color):
            raise TypeError('Expected Color for color!')

        return self.get_player_by_color(color).score

    def get_player_positions(self, color: Color) -> [Position]:
        """
        Gets provided player's positions or throws
        NonExistentPlayerException() if player does not exist.

        :param color: color of player whose positions
                          to retrieve
        :return: player's position
        """
        # Validate player color
        if not isinstance(color, Color):
            raise TypeError('Expected Color for color!')

        return self.get_player_by_color(color).places

    def place_avatar(self, color: Color, position: Position) -> None:
        """
        Places an avatar on behalf of the given player color at
        the specified location if it is not a hole.

        :param color: color of player to place avatar for
        :param position: position to place avatar
        :return: None
        """
        # Validate type of color
        if not isinstance(color, Color):
            raise TypeError('Expected Color for player color!')

        # Validate type of position
        if not isinstance(position, Position):
            raise TypeError('Expected Position for position!')

        # Make sure target position is not occupied by another player or
        # a hole
        if not self.is_position_open(position):
            raise InvalidPositionException(f"Position {position} already occupied or hole!")

        # Make sure player exists
        if color not in self.player_order:
            raise NonExistentPlayerException()

        # Update placement to reflect updated avatar's position
        self.get_player_by_color(color).add_place(position)

        if self.__all_avatars_have_been_placed:
            # Proceed to the next unstuck player
            self.__trigger_next_turn(0)

    @property
    def __all_avatars_have_been_placed(self) -> bool:
        """
        Tells whether all avatars have been placed.
        """
        placed_avatars_no = sum([len(p.places) for p in self.__players])

        return placed_avatars_no == len(self.__players) * self.__avatars_per_player

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
            raise InvalidPositionException(f'{position} is outside the bounds of the board!')

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

        # Get player color for src
        player_color = self.__whose_avatar(src)

        # Make sure there is an avatar at src
        if player_color is None:
            raise InvalidActionException()

        # Make sure it is the current player
        if self.current_player != player_color:
            raise MoveOutOfTurnException(f'avatar belongs to player color {player_color} '
                                         f'current player color: {self.current_player}')

        # Adjust player score
        self.get_player_by_color(player_color).score += self.__board.get_tile(src).fish_no

        # Swap out old avatar position for new
        self.get_player_by_color(player_color).swap_places(src, dst)

        # Clear cache for all possible actions
        self.__all_possible_actions_cache.clear()

        # Remove board tile
        self.__board.remove_tile(src)
        # Record move
        self.__move_log.append(Action(src, dst))
        # Trigger next turn
        self.__trigger_next_turn()

    def __whose_avatar(self, pos: Position) -> Color:
        """
        Returns the color of the player to whom the avatar
        on the given position belongs.

        :param pos: position avatar is one
        :return: returns player color or None to indicate that nobody
                 has an avatar placed at that position
        """
        # Validate position
        if not isinstance(pos, Position):
            raise TypeError('Expected Position for pos!')

        # Get player color whose avatar exists at src
        for player in self.__players:
            # If src is among this player's placements, return color
            if pos in player.places:
                return player.color

        return None

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

    def can_anyone_move(self) -> bool:
        """
        Tells if any player can move any of their avatars.

        :return: boolean indicating whether anyone can move
        """
        # Set flag to indicate at least player can move
        at_least_one_can_move = False

        # Cycle over players and return true if any of them
        # can move
        for player_color in self.player_order:
            if not self.__is_player_stuck(player_color):
                at_least_one_can_move = True
                # don't break as we want to check if anybody
                # else is stuck

        return at_least_one_can_move

    def __is_player_stuck(self, player_color: Color) -> bool:
        """
        Tells if player with given player_color can go anywhere. It does
        not check for turn. Can only be called after everyone has
        finished placing their avatars.

        :param player_color: color of player for whom to check
        :return: boolean indicating whether player
                 can move (not necessarily this turn)
        """
        # Validate player_color
        if not isinstance(player_color, Color):
            raise TypeError('Expected positive Color for player_color!')

        # Make sure player_color is in player collection
        if player_color not in self.player_order:
            raise NonExistentPlayerException()

        # Retrieve player's positions
        player_positions = self.get_player_by_color(player_color).places

        # Cycle over player's positions
        for position in player_positions:
            # Retrieve all reachable positions from this position
            reachable_pos: [Position] = self.__board.get_reachable_positions(position)
            # Make sure at least one path is clear
            for pos in reachable_pos:
                if self.__is_path_clear(position, pos, reachable_pos):
                    # Remove them from player stuck cache if they're in there
                    if player_color in self.__player_stuck_cache:
                        self.__player_stuck_cache.remove(player_color)
                    return False

        # Add them to cache if they're not already there
        if player_color not in self.__player_stuck_cache:
            # Cache that player is indefinitely stuck
            self.__player_stuck_cache.append(player_color)

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
            player_color = player_obj.color.name

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
                                   text=f'{player_obj.name}[{player_color}]')
