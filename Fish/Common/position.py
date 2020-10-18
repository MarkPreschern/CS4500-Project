from collections import namedtuple

# Define named tuple called Position to represent
# a position on the board. A position object is described
# by two coordinates, namely x and y, where x represents
# row and y represents column.
Position = namedtuple('Position', ['x', 'y'])
