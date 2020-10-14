from Color import Color


class Avatar(object):
    """
    Represents a player's avatar in the game.
    """
    def __init__(self, id: int, player_id: int, color: Color):
        """
        Initializes an Avatar with the given parameters.
        :param id: unique identifier for avatar
        :param player_id: id of player to which avatar belongs
        :param color: avatar color (Color)
        :return: resulting Avatar object
        """
        # Validate params
        if not isinstance(id, int) or player_id <= 0:
            raise TypeError('Expecting positive int for avatar id!')

        if not isinstance(player_id, int) or player_id <= 0:
            raise TypeError('Expecting positive int for player id!')

        if not isinstance(color, Color):
            raise TypeError('Expecting Color for color!')

        self.__player_id = player_id
        self.__color = color
        self.__id = id

    @property
    def id(self) -> int:
        """
        Returns avatar's unique identifier.
        """
        return self.__id

    @property
    def player_id(self) -> int:
        """
        Returns id of player avatar belongs to.
        """
        return self.__player_id

    @property
    def color(self) -> Color:
        """
        Returns avatar color.
        """
        return self.__color
