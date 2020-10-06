from random import randint
import random
import constants as ct
from Hole import Hole
from Tile import Tile
from AbstractTile import AbstractTile
import tkinter as tk
import pathlib
import inspect
import os
import itertools


class Board(object):
    """
    Represents the board on which the game is played.
    """

    def __init__(self, tiles):
        """
        Initializes board with given parameters.
        :param tiles: dictionary of tiles
        :return: None
        """
        # Validate params
        if not isinstance(tiles, dict):
            raise ValueError('Invalid tiles - expected dictionary!')

        # Make sure the values are of either Hole or Tile
        for val in tiles.values():
            if not isinstance(val, AbstractTile):
                raise ValueError(f'Invalid tile value: {type(val)}. Must be either'
                                 f'Hole or Tile!')

        # Validate tiles
        xs, ys = zip(*list(tiles.keys()))
        # Strip out duplicates
        xs = list(set(xs))
        ys = list(set(ys))

        # Infer rows and columns by inspect the largest element of either
        # array
        rows, cols = max(xs) + 1, max(ys) + 1

        # Generate cartesian product of [0..rows] x [0...cols]
        compl_coord = [k for k in itertools.product(list(range(rows)), list(range(cols)))]

        # Make sure all points are covered (completeness check)
        if list(tiles.keys()) != compl_coord:
            raise ValueError(f'Invalid tiles dict - cannot have missing points!')

        # Initialize tile container
        self.__tiles = tiles

        # Set fields
        self.__rows = rows
        self.__cols = cols
        self.__tile_no = self.__rows * self.__cols

        # Initialize empty sprite container to hold our sprites
        # as to prevent tkinter from garbage collecting them
        self.__sprites = {}

        # Set root path (path to this class' parent folder)
        self.__root_path = pathlib.Path(inspect.getfile(self.__class__)).parent

        # Set root path (path to this class' parent folder)
        self.__load_sprites()

    @property
    def rows(self) -> int:
        """
        Returns the number of rows on the board.
        """
        return self.__rows

    @property
    def cols(self) -> int:
        """
        Returns the number of cols on the board.
        """
        return self.__cols

    @property
    def tile_no(self) -> int:
        """
        Returns the number of tiles on the board.
        """
        return self.__tile_no

    @property
    def tiles(self) -> dict:
        """
        Returns immutable copy of tile collection.
        """
        return self.__tiles.copy()

    def __load_sprites(self) -> None:
        """
        Loads sprites from sprites folder.
        :return: None
        """
        for file_name in os.listdir(self.__root_path.joinpath(ct.SPRITE_PATH)):
            # Break up file name & extension (if it exists)
            file_name_tokens = os.path.splitext(file_name)

            # Validate file type if there is one
            if file_name_tokens[1] != f'.{ct.SPRITE_FORMAT}':
                continue

            # Add to sprite collection
            self.__sprites.update({file_name_tokens[0]: self.__get_sprite(file_name_tokens[0])})

    @classmethod
    def min_oft_and_holes(cls, min_one_fish_tile_no: int, holes_no: int):
        """
        Builds a board with at least min_one_fish_tiles one-fish tiles and holes_no
        holes.
        :param min_one_fish_tile_no: minimum number of one-fish tiles
        :param holes_no: number of holes
        :return: instance of Board configured to spec
        """
        # Check params
        if not isinstance(min_one_fish_tile_no, int) or min_one_fish_tile_no < 0:
            raise ValueError('Expected integer >= 0 for min_one_fish_tile_no!')

        if not isinstance(holes_no, int) or holes_no < 0:
            raise ValueError('Expected integer >= 0 for holes_no!')

        # Generate a board large enough to accommodate the given minimum
        # number of one fish tiles and number of holes
        rows, cols = (min_one_fish_tile_no + 1), (holes_no + 1)

        tile_lst = []
        # Add holes to tile list
        tile_lst.extend([Hole() for _ in range(holes_no)])
        # Add 1-fish tiles to tile list
        tile_lst.extend([Tile(1) for _ in range(min_one_fish_tile_no)])
        # Add random number-fish tiles to tile list
        rand_no_fish_tile_no = rows * cols - holes_no - min_one_fish_tile_no

        for _ in range(rand_no_fish_tile_no):
            # Generate an arbitrary number of fish
            fish_no = randint(ct.MIN_FISH_PER_TILE, ct.MAX_FISH_PER_TILE)
            # Create and append tile
            tile_lst.append(Tile(fish_no))

        # Shuffle list
        random.shuffle(tile_lst)

        # Initialize empty dict to disseminate list into
        tiles = {}

        # Disseminate list onto dictionary
        for row in range(rows):
            for col in range(cols):
                tiles.update({(row, col): tile_lst.pop(0)})

        # return new instance of Board with built board
        return cls(tiles)

    @classmethod
    def homogeneous(cls, tile_fish_no: int, rows: int = ct.DEFAULT_BOARD_ROWS,
                    cols: int = ct.DEFAULT_BOARD_COLS):
        """
        Builds a homogeneous board with tiles laden with
        the number of fish provided.
        :param tile_fish_no: number of fish to each tile
        :param rows: number of rows to board
        :param cols: number of cols to board
        :return: new homogeneous Board designed to spec
        """
        # Validate params
        if not isinstance(tile_fish_no, int) or tile_fish_no < ct.MIN_FISH_PER_TILE\
                or tile_fish_no > ct.MAX_FISH_PER_TILE:
            raise TypeError('Expected int >=0 for tile_fish_no')

        if not isinstance(rows, int) or rows < 0:
            raise TypeError('Expected int >=0 for rows')

        if not isinstance(cols, int) or cols < 0:
            raise TypeError('Expected int >=0 for rows')

        # Initialize empty tiles container
        tiles = {}

        # Add x-fish tiles to each pointer
        for r in range(rows):
            for c in range(cols):
                tiles.update({ (r, c): Tile(tile_fish_no)})

        # Return resulting board
        return cls(tiles)

    def get_reachable_positions(self):
        pass

    def remove_tile(self, pt) -> None:
        """
        Removes a tile at the given position (if one exists) by
        replacing it with a Hole instead.
        :param pt: point at to remove tile
        :return: None
        """
        # Validate point
        if not isinstance(pt, tuple):
            raise ValueError('Expected tuple object for pt!')

        # Retrieve tile at point
        tile = self.get_tile(pt)

        # Check tile type
        if tile.is_tile:
            self.__tiles.update({pt: Hole()})
        else:
            raise ValueError('No tile at given location!')

    def get_tile(self, pt) -> AbstractTile:
        """
        Returns the tile at the given point.

        :param pt: xy tuple the tile lives
        :return: AbstractTile object
        """
        # Validate point
        if not isinstance(pt, tuple):
            raise TypeError('Expected tuple object for pt!')

        if pt not in self.__tiles.keys():
            raise ValueError('No tile exists at given point!')

        return self.__tiles.get(pt)

    def __get_sprite(self, sprite_name: str) -> tk.PhotoImage:
        """
        Retrieves the PhotoImage object of the given sprite.
        :param sprite_name: sprite to retrieve
        :return: resulting PhotoImage object
        """
        return tk.PhotoImage(file=self.__root_path.joinpath(f'{ct.SPRITE_PATH}/{sprite_name}.{ct.SPRITE_FORMAT}'))

    def render_tile(self, parent_frame, pt) -> tk.Canvas:
        """
        Returns an image of the tile at the given point.

        :param parent_frame: frame to render it to
        :param pt: xy tuple the tile lives
        :return: Canvas object of the tile
        """
        # Validate params
        if not isinstance(pt, tuple):
            raise TypeError('Expected tuple object for pt!')

        if not isinstance(parent_frame, tk.Frame):
            raise TypeError('Expected Frame for parent_frame!')

        # Retrieve tile at point
        tile = self.get_tile(pt)
        # Create canvas in parent window unto which to render tile
        canvas = tk.Canvas(parent_frame, width=ct.TILE_WIDTH, height=ct.TILE_HEIGHT)
        # Set canvas to use grid
        canvas.grid(row=0, column=0)

        # Check if tile is a full tile
        if tile.is_tile:
            # Add tile
            canvas.create_image(3, 3, image=self.__sprites['tile'], anchor=tk.NW)
            # Add correct fish sprite
            canvas.create_image(24, 20, image=self.__sprites[f'fish-{tile.fish_no}'], anchor=tk.NW)
        else:
            # Add hole
            canvas.create_image(3, 3, image=self.__sprites['hole'], anchor=tk.NW)
        # Return resulting canvas
        return canvas
