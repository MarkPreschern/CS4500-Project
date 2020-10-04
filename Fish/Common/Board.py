from random import random
import constants as ct


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


    def build_min_one_fish_tiles_with_holes(self,
                                            min_one_fish_tile_no: int,
                                            holes_no: int):
        """
        Builds a board with at least min_one_fish_tiles one-fish tiles and holes_no
        holes.
        :param min_one_fish_tiles: 
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
        tile_lst.extend([Tile(random(ct.MIN_FISH_PER_TILE, ct.MAX_FISH_PER_TILE)) for _ in range(self.__tiles_no - holes_no - min_one_fish_tile_no)])

        # Shuffle list
        random.shuffle(tile_lst)

        # Disseminate list onto dictionary
        for row in self.__rows:
            for col in self.__cols:
                self.__tiles.update({ Point(row, col):  tile_lst.pop(0)})

        return self

    def build_homogeneous(self, tile_fish_no: int):
        self.__holes = []
        self.__tiles = []
        return self

    def get_reachable_positions(self):
        pass

    def remove_tile(coord):
        pass

    def render_tile(coord):
        pass
