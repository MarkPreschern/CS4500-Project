from random import randint
import constants as ct
from hole import Hole
from position import Position
from tile import Tile
from abstract_tile import AbstractTile
import tkinter as tk
import itertools
from movement_direction import MovementDirection
from exceptions.InvalidPositionException import InvalidPositionException
from sprite_manager import SpriteManager


class Board(object):
    """
    PURPOSE:        The purpose of the board is to aggregate the staple board pieces
                    (tiles and holes) in a matrix-like setup where each tile can hold a
                    number of fish. The arrangement of tiles and holes determines what straight
                    line paths can be traversed from any arbitrary position. A straight line path
                    is one that traverses tiles across their parallel edges (as opposed to corners).

    INTERPRETATION: The tiles and holes (collectively denoted using AbstractTile(s)) and their
                    respective locations on the board are stored in the "tiles" member of the
                    class. Locations of the aforementioned game pieces are described using Position objects,
                    which tell the x (row value) and y (column value) of the associated object.
                    The coordinate system employed has its origin in the upper left corner (denoted using
                    Position(0,0)) with row numbers (Position.x) increasing in value as the player moves
                    to the right of the board, and with column numbers (Position.y) increasing in value
                    as the player moves toward the bottom of the board.

                    The board spreads out consecutive columns by the length of a tile's top side on each row and
                    offsets every 2nd row (from the top) on the board to the right and fits it into the row above it
                    to create an interlaced board layout where adjacent hexagons "lock" into each other. For a graphical
                    representation of this, please see the pictures in sprites/example_board.png.

                    To determine which tiles are reachable from where, the board computes an edge list (a list of all
                    the adjacent tiles each tile on the board can access across its 6 sides). The edge list is then
                    used to determine all the Position(s) (and therefore, tiles) that can be accessed in any given
                    direction for a given Position.

    """
    DISABLE_SPRITE_MANAGER = True
    RENDER_TILE_COORDINATES = True

    def __init__(self, tiles: dict):
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

        # Compute edge list for determining reachable positions.
        self.__edge_list = self.__compute_reachable_edge_list()

        if not Board.DISABLE_SPRITE_MANAGER:
            # Loads sprites
            SpriteManager.load_sprites()

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

    @classmethod
    def min_oft_and_holes(cls, min_one_fish_tile_no: int, holes: [Position]):
        """
        Builds a board with at least min_one_fish_tiles one-fish tiles and given
        holes.
        :param min_one_fish_tile_no: minimum number of one-fish tiles
        :param holes: holes in the form of a list of Position objects
        :return: instance of Board configured to spec
        """
        # Check params
        if not isinstance(min_one_fish_tile_no, int) or min_one_fish_tile_no < 0:
            raise ValueError('Expected integer >= 0 for min_one_fish_tile_no!')

        if not isinstance(holes, list):
            raise ValueError('Expected list for holes!')

        # Remove duplicate holes (if any)
        holes = list(set([k for k in holes]))

        # Determine maximum hole coordinates (if any)
        if len(holes) > 0:
            # Extract hole coordinates
            xs, ys = zip(*holes)

            # Determine max coordinates
            max_x = max(xs)
            max_y = max(ys)
        else:
            # Set them if no holes
            max_x = 1
            max_y = 1

        # Set tentative rows and cols
        rows, cols = max_x + 1, max_y + 1

        # Determine remaining open slots after adding holes and one-fish tiles
        remaining_slots = rows * cols - min_one_fish_tile_no - len(holes)

        # Continue adding columns and rows until both holes and the minimum number of
        # one-fish tiles can be accommodated
        while remaining_slots < 0:
            # Randomly determine whether to add row or column, with more
            # weight being assigned to row
            if randint(0, ct.ROW_TO_COLUMN_PROBABILITY) == 0:
                cols += 1
            else:
                rows += 1
            # Recalculate remaining_slots
            remaining_slots = rows * cols - min_one_fish_tile_no - len(holes)

        # Initialize empty tile container
        tiles = {}
        # Initialize one-fish tile count
        one_fish_tile_cnt = 0
        # Disseminate list onto dictionary
        for row in range(rows):
            for col in range(cols):
                # Check if it's a hole
                if (row, col) in holes:
                    tiles.update({Position(row, col): Hole()})
                elif one_fish_tile_cnt < min_one_fish_tile_no:
                    # Add one-fish tile
                    tiles.update({Position(row, col): Tile(1)})
                    one_fish_tile_cnt += 1
                else:
                    # Generate an arbitrary number of fish
                    fish_no = randint(ct.MIN_FISH_PER_TILE, ct.MAX_FISH_PER_TILE)
                    # Add random fish-tile
                    tiles.update({Position(row, col): Tile(fish_no)})

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
        if not isinstance(tile_fish_no, int) or tile_fish_no < ct.MIN_FISH_PER_TILE \
                or tile_fish_no > ct.MAX_FISH_PER_TILE:
            raise ValueError('Expected int >=0 for tile_fish_no')

        if not isinstance(rows, int) or rows < 0:
            raise ValueError('Expected int >=0 for rows')

        if not isinstance(cols, int) or cols < 0:
            raise ValueError('Expected int >=0 for rows')

        # Initialize empty tiles container
        tiles = {}

        # Add x-fish tiles to each pointer
        for r in range(rows):
            for c in range(cols):
                tiles.update({Position(r, c): Tile(tile_fish_no)})

        # Return resulting board
        return cls(tiles)

    def remove_tile(self, pt: Position) -> None:
        """
        Removes a tile at the given position (if one exists) by
        replacing it with a Hole instead.
        :param pt: position to remove tile
        :return: None
        """
        # Validate point
        if not isinstance(pt, Position):
            raise ValueError('Expected Position object for pt!')

        # Retrieve tile at point
        tile = self.get_tile(pt)

        # Check tile type
        if tile.is_tile:
            self.__tiles.update({pt: Hole()})
        else:
            raise ValueError('No tile at given location!')

    def get_tile(self, pt: Position) -> AbstractTile:
        """
        Returns the tile at the given point.

        :param pt: position the tile lives
        :return: AbstractTile object
        """
        # Validate point
        if not isinstance(pt, Position):
            raise TypeError('Expected Position object for pt!')

        if pt not in self.__tiles.keys():
            raise InvalidPositionException('No tile exists at given position!')

        return self.__tiles.get(pt)

    def render(self, parent_frame: tk.Frame):
        """
        Renders board to provided frame.
        :param parent_frame: frame to render board on
        :return: resulting Canvas object
        """
        # Validate params
        if not isinstance(parent_frame, tk.Frame):
            raise TypeError('Expected Frame for parent_frame!')

        # Determine total frame size
        total_width = self.__cols * ct.DELTA * 2 + ct.DELTA / 2
        total_height = (self.__rows + 1) * ct.TILE_HEIGHT / 2 + ct.MARGIN_OFFSET

        # Load sprites
        SpriteManager.load_sprites()
        
        # Set geometry
        canvas = tk.Canvas(parent_frame, bd=0, highlightthickness=0,
                           height=total_height, width=total_width)
        canvas.place(x=0, y=0)
        # Render one tile at a time
        for pt, tile in self.__tiles.items():
            # Determine x
            x = (0 if pt[0] % 2 == 0 else ct.DELTA) + (2 * ct.DELTA * pt[1])
            # Determine y
            y = pt[0] * ct.TILE_HEIGHT / 2
            # Check if tile is a full tile
            if tile.is_tile:
                # Add tile
                tile_sprite = canvas.create_image(3, 3, image=SpriteManager.get_sprite('tile'), anchor=tk.NW)
                # Move tile to corresponding position
                canvas.move(tile_sprite, x, y)
                # Add correct fish sprite
                fish_sprite = canvas.create_image(24, 20, image=SpriteManager.get_sprite(f'fish-{tile.fish_no}'),
                                                  anchor=tk.NW)
                # Move fish to corresponding position
                canvas.move(fish_sprite, x, y)
            else:
                # Add hole
                hole_sprite = canvas.create_image(3, 3, image=SpriteManager.get_sprite('hole'), anchor=tk.NW)
                canvas.move(hole_sprite, x, y)

            if Board.RENDER_TILE_COORDINATES:
                # Add tile x, y
                canvas.create_text(x + ct.TILE_WIDTH / 2 + ct.MARGIN_OFFSET,
                                   y + ct.TILE_HEIGHT - ct.MARGIN_OFFSET,
                                   fill="black", font="Arial 10",
                                   text=f'{pt[0]},{pt[1]}')

        return canvas

    def get_reachable_positions(self, pos: Position) -> [Position]:
        """
        Create a list of all tiles that are reachable within a straight line path of the given position.

        :param pos: the starting position for which reachable positions will be computed
        :return: a list of Position that contains all reachable positions
        """
        # Validate params
        if not isinstance(pos, Position):
            raise TypeError('Expected Position for pos.')
        if pos not in self.tiles.keys():
            raise ValueError('Expected pos to be a position on the game board.')

        # Store reachable positions
        reachable_positions = []

        # Use out-edges from the tile at the given pos
        edges_to_adj_tiles = self.__edge_list[pos]

        # Look at all adjacent tiles for straight line paths
        for movement_dir in edges_to_adj_tiles:
            # Find all of the tiles in the same direction as the current direction
            tiles_in_path = self.__find_straight_path(pos, movement_dir)

            # Add all tiles above to the overall list of reachable positions
            reachable_positions.extend(tiles_in_path)

        return reachable_positions

    def get_connecting_positions(self, pos1: Position, pos2: Position) -> [Position]:
        """
        Retrieves a list of all Position objects connecting
        the provided positions.

        :param pos1: first position
        :param pos2: second position
        :return: resulting list
        """
        if not isinstance(pos1, Position):
            raise TypeError('Expected Position for pos1')

        if not isinstance(pos2, Position):
            raise TypeError('Expected Position for pos2')

        # De-multiplex positions into x,y coordinates
        x1, y1 = pos1
        x2, y2 = pos2

        # No connecting points if the two are equal
        if pos1 == pos2:
            return []

        # Determine direction
        if y1 == y2:
            if x2 > x1:
                direction = MovementDirection.Bottom
            else:
                direction = MovementDirection.Top
        elif y1 > y2:
            if x1 == x2:
                return []  # cannot move across corners
            elif x1 > x2:
                direction = MovementDirection.TopLeft
            else:
                direction = MovementDirection.BottomLeft
        else:
            if x2 > x1:
                direction = MovementDirection.BottomRight
            elif x1 > x2:
                direction = MovementDirection.TopRight
            else:
                return []  # cannot move across corners

        # Retrieves all positions in said direction from pos1
        positions = self.__find_straight_path(pos1, direction)

        # Check if pos2 is among the points in direct line path
        if pos2 in positions:
            return positions[:positions.index(pos2)]
        else:
            return []

    def __compute_reachable_edge_list(self) -> dict:
        """
        Return an edge dict for all of the tiles on the board. The graph in question
        is directed. Edges exist between all adjacent tiles, and each edge has a weight
        that represents the direction of said edge (i.e each weight is a MovementDirection)

        Note that edges cannot be created between a hole and a tile, nor can they be created
        between two holes.

        As an example, an edge between a starting tile A and its neighboring tile to the
        top left will have a weight of MovementDirection.TopLeft, or 0.
        
        :return: a dict whose keys are Position objects representing positions
                 and whose values are dicts containing adjacent tiles with weights
        """
        # Store the edges
        edges = {}

        # Compute a list of edges for all tiles on the board
        for pos in self.tiles:
            # Store the edges to adjacent tiles with directions as weights 
            adjacent_tiles_dict = {}

            # Current row/col position
            row = pos[0]
            col = pos[1]

            # Locations of surrounding tiles
            top_left = Position(row - 1, col - 1) if row % 2 == 0 else Position(row - 1, col)
            top = Position(row - 2, col)
            top_right = Position(row - 1, col) if row % 2 == 0 else Position(row - 1, col + 1)
            bottom_right = Position(row + 1, col) if row % 2 == 0 else Position(row + 1, col + 1)
            bottom = Position(row + 2, col)
            bottom_left = Position(row + 1, col - 1) if row % 2 == 0 else Position(row + 1, col)

            # For all possible directions, check if the computed position exists on the board
            # and add to the current adjacent tiles dict with 
            if top_left in self.tiles.keys():
                adjacent_tiles_dict[MovementDirection.TopLeft] = top_left

            if top in self.tiles.keys():
                adjacent_tiles_dict[MovementDirection.Top] = top

            if top_right in self.tiles.keys():
                adjacent_tiles_dict[MovementDirection.TopRight] = top_right

            if bottom_right in self.tiles.keys():
                adjacent_tiles_dict[MovementDirection.BottomRight] = bottom_right

            if bottom in self.tiles.keys():
                adjacent_tiles_dict[MovementDirection.Bottom] = bottom

            if bottom_left in self.tiles.keys():
                adjacent_tiles_dict[MovementDirection.BottomLeft] = bottom_left

            # Set the edges list for the current position
            edges[pos] = adjacent_tiles_dict

        return edges

    def __find_straight_path(self, start_pos, direction) -> [Position]:
        """
        Find the positions of all tiles in the straight line path starting from the
        given position and moving in the given direction.

        :param start_pos: starting position of the straight line path
        :param direction: direction of the straight line path
        :return: a list of Position objects representing the positions of tiles that are in
                 the straight line path
        """

        # Validate params
        if not isinstance(start_pos, Position):
            raise TypeError('Expected Position for start_pos.')
        if not isinstance(direction, MovementDirection):
            raise TypeError('Expected MovementDirection for direction.')

        # Store tiles in the current straight line path
        tiles_in_path = []

        # Keep track of the current position and the next position in the path
        current_pos = start_pos

        # Iterate until the end of the path is reached or a hole is encountered
        while current_pos is not None:
            # Get the position of the next tile in the path
            next_pos = self.__edge_list.get(current_pos, {}).get(direction, None)

            # If the next tile in the path is a hole, break
            if next_pos and self.tiles[next_pos].is_hole:
                break

            # If there is a next position, append that position to the list
            if next_pos:
                tiles_in_path.append(next_pos)

                # Update current pos and proceed down the straight line path or
            # break out of loop
            current_pos = next_pos

        return tiles_in_path
