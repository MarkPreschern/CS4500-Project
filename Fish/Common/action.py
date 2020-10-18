from collections import namedtuple

# Define named tuple called Action to represent a
# move on the board. An action object is described
# by two Position, namely src and dst, where dst represents
# the position the move was made from and dst represents
# the position the move was made to.
Action = namedtuple('Action', ['src', 'dst'])
