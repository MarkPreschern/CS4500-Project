## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.
    It is possible that you had "perfect" data definitions/interpretations
    (purpose statement, unit tests, etc) and/or responded to feedback in a 
    timely manner. In that case, explain why you didn't have to add this to
    your `todo` list.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites: 

These questions are taken from the rubric and represent some of the most
critical elements of the project, though by no means all of them.

(No, not even your sw arch. delivers perfect code.)

### Board

- a data definition and an interpretation for the game _board_
    - We had already fixed our definition and interpretation of the game board, and there was no need to revisit it. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39#diff-a2e5e9a5574dc815c4a99949d621cf78).

- a purpose statement for the "reachable tiles" functionality on the board representation
    - We had already amended our Board interpretation to explain how it computes "reachable tiles" by way of an edge list, and there was no need to revisit it. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39#diff-a2e5e9a5574dc815c4a99949d621cf78R36-R40) and [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39/Fish/Common/board.py#L396-L409). The snippet the latter link points to was never amended, as we "got it right" from the get-go.

- two unit tests for the "reachable tiles" functionality
    - We already had N >= 2 unit tests for said functionality, and there was no need to revisit it. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39/Fish/Common/tests/board_tests.py#L237-L427).


### Game States 


- a data definition and an interpretation for the game _state_
    - We had already amended our State's interpretation & purpose, and assumed that purpose also fullfiled the role of a definition, so we chose not to revisit it. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39#diff-3c0c742881289081d1c3cfb361c6da0eR22-R44).

- a purpose statement for the "take turn" functionality on states
    - Our "take turn" functionality is implicitly taken care of by our State by shifting the player list and allowing the next eligible player to `move_avatar`. We did not think it necessary to amend our purpose statement for `move_avatar` further as its intended use it had already been documented in both the interpretation of our State and in `move_avatar` itself. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39#diff-3c0c742881289081d1c3cfb361c6da0eR34-R40) and [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/d4cfe7e40a62c1aac09f70df53e1d6349f41b63e#diff-8b59c1ced5e1a2b96a91913cb360a99cR239-R242)

- two unit tests for the "take turn" functionality 
    - We already had sufficient unit tests for `move_avatar` (our implementation of the "take turn" functionality) and did not think it necessary to revisit it. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/52437902b5505416e36fa8af1d242477a6e557f5/Fish/Common/tests/state_tests.py#L279-L514) for `move_avatar` tests prior to Milestone 7 being published. 

### Trees and Strategies


- a data definition including an interpretation for _tree_ that represent entire games
    - We had already addressed the point of having a proper definition & interpretation for GameTree and did not see the need to revisit it. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39#diff-a2b85550c39cc14472cf741196ccb390R10-R19).

- a purpose statement for the "maximin strategy" functionality on trees
    - We already had a purpose statement for "maximin" and only saw the need to clarify what would happen if the maximizing player became stuck and the search depth had not been reached. We admittedly forgot to add this to our TODO list as it was a very small change. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/61981ac2ec08e44f119f4b0beb25817545bf3c0a#diff-8668b6307021688899b1d56141354730R73-R118) for fix. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/9981d988be3aa1b66594cae83d8beae39509b2b7/Fish/Player/strategy.py#L105-L119) and [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/9981d988be3aa1b66594cae83d8beae39509b2b7/Fish/Player/strategy.py#L69-L78) for the complete purpose statements for our "maximin strategy" implementation.

- two unit tests for the "maximin" functionality 
    - We already had unit tests for "maximin" and did not see the need to revisit them. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/9981d988be3aa1b66594cae83d8beae39509b2b7/Fish/Player/Other/tests/strategy_tests.py#L196-L285) for our tests.

### General Issues

Point to at least two of the following three points of remediation: 


- the replacement of `null` for the representation of holes with an actual representation 
    - We never represented holes using `null`, so there was no need to add this to our TODO list. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/master/Fish/Common/hole.py) for our latest Hole representation.

- one name refactoring that replaces a misleading name with a self-explanatory name
    - We never had any knowledge of a method / variable or otherwise with a misleading name. We made a best effort to name our variables and functions appropriately. As such, we did not have to add this to our TODO list.

- a "debugging session" starting from a failed integration test:
  - the failed integration test
  - its translation into a unit test (or several unit tests)
  - its fix
  - bonus: deriving additional unit tests from the initial ones 
  - *Answer:* We had already addressed the failing integration tests from previous milestones. As such, we decided to address the failing staff integration tests (namely 2 and 3) for Milestone 6. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blame/9981d988be3aa1b66594cae83d8beae39509b2b7/7/todo.md#L4) for entry in our README file for this item. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/8640d11096bace47f44a638e6416aa3ad84ec46f#diff-3c0c742881289081d1c3cfb361c6da0eR351-R362) for fix and [here](https://github.ccs.neu.edu/CS4500-F20/quintana/commit/8640d11096bace47f44a638e6416aa3ad84ec46f#diff-8c70528cbfd7d4467390cc3e36673746R826-R870) for unit test that was failing prior to the fix.


### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).

- Our favorite debt removal action was addressing the failing Staff integration tests from Milestone 6. It was not required for Milestone 7, but we decided to eliminate virtually all the technical debt we had left as we had no failing staff integration tests from previous milestones. It was an interesting bug because it pointed to an issue with our State that we thought we had fixed: shifting the player list to the next eligible player that can move. See [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blame/9981d988be3aa1b66594cae83d8beae39509b2b7/7/bugs.md#L1-L10) for more information.


