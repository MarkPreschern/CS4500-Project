## Self-Evaluation Form for Milestone 2

A fundamental guideline of Fundamentals I, II, and OOD is to design
methods and functions systematically, starting with a signature, a
clear purpose statement (possibly illustrated with examples), and
unit tests.

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of tiles, including an interpretation:  
  - `AbstractTile:` https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/AbstractTile.py#L1-L4  
  - `Tile:` https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Tile.py#L5-L8  
  - `Hole:` https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Hole.py#L4-L7  
  - These snippets satisfy the request because for each type of tile, we have a class definition to serve as the data description and a comment describing how the class ought to be interpreted.

- the data description of boards, include an interpretation:  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L14-L17

  - This snippet satisfies the request because we have a class definition to serve as the data description and a comment describing how the class ought to be interpreted.

- the functionality for removing a tile: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L220-L238  
  - purpose:  
  https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L222-L223
  
  - signature:  
  https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L220-L226
  
  - unit tests:  
  https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/tests/BoardTests.py#L190-L206
  
  - These snippets satisfy the request because this functionality has a clear purpose statement, signature, and unit test that are all accessible via the links above.
  
- the functionality for reaching other tiles on the board:  
`get_reachable_positions`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L303-L333  
`__compute_reachable_edge_list`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L335-L393  
`__find_straight_path`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L395-L443  
  - purpose:  
    - `get_reachable_positions`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L305  
    - `__compute_reachable_edge_list`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L337-L339  
    - `__find_straight_path`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L397-L398  
  - signature:  
    - `get_reachable_positions`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L303-L309
    - `__compute_reachable_edge_list`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L335-L349
    - `__find_straight_path`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/Board.py#L395-L405
  - unit tests:  
    - `get_reachable_positions`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/tests/BoardTests.py#L237-L345  
    - `__compute_reachable_edge_list`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/tests/BoardTests.py#L347-L400  
    - `__find_straight_path`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/49e10b0060f9941d1df046c6f5d3c664e0152cf6/Fish/Common/tests/BoardTests.py#L402-L444  
  - These snippets satisfy the request because this functionality has a clear purpose statement, signature, and unit test that are all accessible via the links above. The helper methods used by `get_reachable_positions` also have clear purpose statements, signatures, and unit tests. 
  
The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "d0527d2c92e89d16484bd70d5f708bcc68d00826".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/wellman/tree/d0527d2c92e89d16484bd70d5f708bcc68d00826/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.
