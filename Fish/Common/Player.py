from Color import Color


class Player(object):
    """
    Represents a player in the game and contains all
    pertaining player information.
    """

    def __init__(self, id: int, name: str, age: int, color: Color):
        """
        Initializes a Player object.
        :param id: unique positive integer identifying player
        :param age: positive integer representing player age
        :param color: Color object representing player color
        :return: new Player object
        """

        # Validate params
        if not isinstance(id, int) or id <= 0:
            raise TypeError('Expected positive int for id!')

        if not isinstance(name, str):
            raise TypeError('Expected string for name!')

        if not isinstance(age, int) or age <= 0:
            raise TypeError('Expected positive int for age!')

        if not isinstance(color, Color):
            raise TypeError('Expected Color object for color!')

        # Set properties
        self.__id = id
        self.__name = name
        self.__age = age
        self.__color = color
        self.__score = 0

    @property
    def id(self) -> int:
        """
        Returns player's id.
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        Returns player's name.
        """
        return self.__name

    @property
    def age(self) -> int:
        """
        Returns player's age.
        """
        return self.__age

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
