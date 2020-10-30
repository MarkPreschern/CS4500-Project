## Self-Evaluation Form for Milestone 5

Under each of the following elements below, indicate below where your
TAs can find:

- the data definition, including interpretation, of penguin placements for setups  
`Position`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/Fish/Common/position.py#L3-L7

- the data definition, including interpretation, of penguin movements for turns  
`Action`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/Fish/Common/action.py#L3-L8

- the unit tests for the penguin placement strategy  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/Fish/Player/Other/tests/strategy_tests.py#L286-L349

- the unit tests for the penguin movement strategy; 
  given that the exploration depth is a parameter `N`, there should be at least two unit tests for different depths  
  https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/Fish/Player/Other/tests/strategy_tests.py#L196-L284
  
- any game-tree functionality you had to add to create the `xtree` test harness:
  - where the functionality is defined in `game-tree.PP`
  - where the functionality is used in `xtree`
  - you may wish to submit a `git-diff` for `game-tree` and any auxiliary modules  
  
  We added some functionality to game_tree.py, but we did it for the sake of efficiency and not to make our test harness work. We used our `try_action` method inside `game_tree.py`, which we refactored from last milestone.  
  
  Here is where the functionality is defined in `game_tree.py`: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/Fish/Common/game_tree.py#L118-L132
  
  Here is where the functionality is used in `xtree`:
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/5/Other/xtree.py#L114
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/8c314af6f3ecd73c6ea9cb332e5936191911f05c/5/Other/xtree.py#L166

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "8c314af6f3ecd73c6ea9cb332e5936191911f05c".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/wellman/tree/8c314af6f3ecd73c6ea9cb332e5936191911f05c/Fish>

