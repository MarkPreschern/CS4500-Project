from color import Color
from position import Position


class PlayerEntity(object):
    """
    PURPOSE:        The purpose of this class is to abstract away the sensitive information
                    associated with a Player and solely provide a means to keep track of its
                    name, color and avatar placements.

    INTERPRETATION: Represents a player in the game and contains the minimum information needed
                    to identify the player in the game without revealing any sensitive information.
                    It also holds information about the player's placement in the game via the 'places'
                    member, which is a list containing Position objects' describing the locations of the
                    player's avatars.
    """

    def __init__(self, name: str, color: Color):
        """
        Initializes a PlayerEntity object.
        :param color: Color object representing player color
                      that identifies player
        :return: new PlayerEntity object
        """
        if not isinstance(name, str):
            raise TypeError('Expected string for name!')

        if not isinstance(color, Color):
            raise TypeError('Expected Color object for color!')

        # Set properties
        self.__name = name
        self.__color = color
        self.__score = 0
        # Initialize a list of Position objects indicating where
        # the player's avatars live
        self.__places = []

    def add_place(self, pos: Position):
        """
        Adds an avatar position to player's places array.

        :param pos: Position object representing player's avatar's
                    location
        :return: None
        """
        if not isinstance(pos, Position):
            raise TypeError('Expected Position obj for pos!')

        self.__places.append(pos)

    def swap_places(self, src: Position, dst: Position):
        """
        Swaps Position object src for Position object dst in the
        places array.

        :param src: position object to swap out
        :param dst: position object to swap in
        :return: None
        """
        # Validate params
        if not isinstance(src, Position):
            raise TypeError('Expected Position obj for src!')

        if not isinstance(dst, Position):
            raise TypeError('Expected Position obj for dst!')

        # Make sure src exists
        if src not in self.__places:
            raise ValueError(f'Player does not have avatar at src = {src}')

        # Swap
        self.__places[self.__places.index(src)] = dst

    @property
    def places(self) -> [Position]:
        """
        Returns a list of Position objects indicating where
        the player's avatars are location w.r.t the board.
        """
        return self.__places.copy()

    @property
    def name(self) -> str:
        """
        Returns player's name.
        """
        return self.__name

    @property
    def color(self) -> Color:
        """
        Returns player's color.
        """
        return self.__color

    @property
    def score(self) -> int:
        """
        Returns player's score.
        """
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        """
        Sets a player's score to given value.
        """
        if not isinstance(score, int) or score < 0:
            raise TypeError('Expected positive int for score!')

        self.__score = score
