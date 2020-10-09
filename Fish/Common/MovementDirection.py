from enum import Enum

class MovementDirection(Enum):
        """
        Represents the potential movement directions between tiles.
        """
        TopLeft = 0
        Top = 1
        TopRight = 2
        BottomRight = 3
        Bottom = 4
        BottomLeft = 5