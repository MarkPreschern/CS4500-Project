# Game

### Data representation

To represent entire games, we will construct a network of interconnected nodes, where each node corresponds to a position in the game. A node will feature up to 6 edges to other nodes in directions enabled by the game rules, namely across tile sides that run parallel to each other. When a move is made that renders previously reachable positions inaccessible or vice-versa, edges between the affected nodes are appropriately removed or added. 

Edges to nodes corresponding to holes or tiles occupied by avatars will be automatically pruned, as they are inherently out of reach for players. For other tiles, edges are only formed between tiles that lie in a straight line path in a valid direction. Players can use this map-like representation to determine the possible moves from a given position and plan their next move. Moreover, the referee will be able to leverage this representation to validate players' moves.

The representation will be constructed from a game state after all players have placed their avatars.

A potential game representation in JSON (or Python) could look like this:

```json
{
  [0, 0]: {"SE": [[1, 0], [2, 1], [3, 1]], "S": [[2, 0], [4, 0]]},
  [1, 0]: {"SE": [[2, 1], [3, 1]], "S": [[3, 0]], "NE": [[0, 1]], "NW": [[0, 0]], "SW": [[2, 0]]}
  ..
}
```

Each entry in the dictionary above is a position that is associated with a dictionary keyed with the directions in which moves are possibles from that position. Each direction in the dictionary (denoted using stringified shorthands for north (N), south (S), etc. ) is in turn an array containing all the positions that are accessible in that direction from the position key.

### External interface

> make_game(state: State) -> Game

This method builds a game representation from a given game State and returns it. The game state will be used to source information about the board, as well as about avatar placements.

>  is_move_valid(pos1: (int, int), pos2: (int, int)) -> bool

This method returns a boolean indicating whether a move from pos1 to pos2 would be valid. 

- pos1 and pos2 are both tuples of the form (x, y), where x represents a row, and col represents a column.

>  get_all_reachable_pos(pos: (int, int)) -> []

This method returns a list of all reachable positions from the given position.

- pos is a tuple of the form (x, y), where x represents a row, and col represents a column.

>  get_map() -> {}

This method returns a dictionary of the entire game representation. Each entry in the representation is a start position that corresponds to a dictionary of directions and positions that are accessible from that start direction. See above for an example of what this may look like.

The referee may use get_map() to periodically retrieve a master copy of the game to ensure game rules (i.e. that the moves being are valid).

### 