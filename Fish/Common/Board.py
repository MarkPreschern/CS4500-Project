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


class Board(object):
    """
    Represents the board on which the game is played.
    """

    def __init__(self, rows, cols):
        """
        Initializes board with given parameters.
        :param rows:
        :param cols:
        :return: None
        """
        # Validate params
        if not isinstance(rows, int) or rows < 1:
            raise ValueError('Invalid row - expected positive integer!')

        if not isinstance(cols, int) or cols < 1:
            raise ValueError('Invalid col - expected positive integer!')

        # Set fields
        self.__rows = rows
        self.__cols = cols
        self.__tiles_no = self.__rows * self.__cols

        # Initialize empty tile container
        self.__tiles = {}

        # Initialize empty sprite container
        # Reason: prevent tkinter from garbage collecting our sprites
        self.__sprites = {}

        # Set root path (path to this class' parent folder)
        self.__root_path = pathlib.Path(inspect.getfile(self.__class__)).parent

        # Set root path (path to this class' parent folder)
        self.__load_sprites()

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

    def build_min_one_fish_tiles_with_holes(self,
                                            min_one_fish_tile_no: int,
                                            holes_no: int):
        """
        Builds a board with at least min_one_fish_tiles one-fish tiles and holes_no
        holes.
        :param min_one_fish_tile_no:
        :param holes_no:
        :return: None
        """
        # Check params
        if not isinstance(min_one_fish_tile_no, int) or min_one_fish_tile_no < 0:
            raise ValueError('Expected integer >= 0 for min_one_fish_tile_no!')

        if not isinstance(holes_no, int) or holes_no < 0:
            raise ValueError('Expected integer >= 0 for holes_no!')

        # Ensure that theyre not building a board that could not be fit within the boundaries
        # determined by rows and cols
        if self.__tiles_no < holes_no + min_one_fish_tile_no:
            raise ValueError('Given parameters exceed the maximum supported number of tiles for the board!')

        # Add holes to tile list
        tile_lst = [Hole() for _ in range(holes_no)]
        # Add 1-fish tiles to tile list
        tile_lst.extend([Tile(1) for _ in range(min_one_fish_tile_no)])
        # Add random number-fish tiles to tile list
        tile_lst.extend([Tile(randint(ct.MIN_FISH_PER_TILE, ct.MAX_FISH_PER_TILE))
                         for _ in range(self.__tiles_no - holes_no - min_one_fish_tile_no)])

        # Shuffle list
        random.shuffle(tile_lst)

        # Disseminate list onto dictionary
        for row in range(self.__rows):
            for col in range(self.__cols):
                self.__tiles.update({(row, col): tile_lst.pop(0)})

        return self

    def build_homogeneous(self, tile_fish_no: int):
        self.__holes = []
        self.__tiles = []
        return self

    def get_reachable_positions(self):
        pass

    def remove_tile(self, pt):
        pass

    def get_tile(self, pt) -> tk.PhotoImage:
        """
        Returns the tile at the given point.

        :param pt: xy tuple the tile lives
        :return: AbstractTile object
        """
        # Validate point
        if not isinstance(pt, tuple):
            raise ValueError('Expected tuple object for pt!')

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
            raise ValueError('Expected tuple object for pt!')

        if not isinstance(parent_frame, tk.Frame):
            raise TypeError('Expected Frame for parent_frame!')

        # Retrieve tile at point
        tile = self.get_tile(pt)

        if isinstance(tile, AbstractTile):
            # Create canvas in parent window unto which to render tile
            canvas = tk.Canvas(parent_frame, width=ct.TILE_WIDTH, height=ct.TILE_HEIGHT)
            # Set canvas to use grid
            canvas.grid(row=0, column=0)

            # Check if tile is a full tile
            if isinstance(tile, Tile):
                # Add tile
                canvas.create_image(3, 3, image=self.__sprites['tile'], anchor=tk.NW)
                # Add correct fish sprite
                canvas.create_image(24, 20, image=self.__sprites[f'fish-{tile.fish_no}'], anchor=tk.NW)
            else:
                # Add hole
                canvas.create_image(3, 3, image=self.__sprites['hole'], anchor=tk.NW)
            # Return resulting canvas
            return canvas
        else:
            raise TypeError(f'Tile is neither hole nor tile: {type(tile)}!')
