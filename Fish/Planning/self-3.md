## Self-Evaluation Form for Milestone 3

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of states, including an interpretation:
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/State.py#L24-L29
  - The referenced snippet includes a description of what a state is. It lacks a thorough interpretation, however.

- a signature/purpose statement of functionality that creates states 
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/State.py#L31-L37
  - The referenced snippet includes a constructor of State with type-annotated parameters, as well as a brief purpose statement beneath it.

- unit tests for functionality of taking a turn
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L207-L458
  - The tests referenced above test a player's successful and unsuccessful attempts at taking a turn by moving their avatar.

  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L690-L710
  - The snippet referenced above is a test of player trying to take a turn (make a move) out of turn.

  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L741-L792
  - The snippet above tests a series of players taking turns and ensures that the state correctly assigns the next player to go.

- unit tests for functionality of placing an avatar
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L103-L205

  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L678-L688
  - The two snippets above test a series of erroneous and valid avatar placements.

- unit tests for functionality of final-state test
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L540
  - The above code performs a final-state test to ascertain whether anyone can move after a player has made a move.
  - https://github.ccs.neu.edu/CS4500-F20/wellman/blob/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish/Common/tests/StateTests.py#L828-L855
  - The test referenced above tests a game-over scenario where no more moves are possible. Internally, can_anyone_move() is leveraged to throw the *NoMoreTurnsException* exception, which is telling of the "final state".

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "4b53e5a0aa2f4d3cea2909980670791909cc48c9".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/wellman/tree/4b53e5a0aa2f4d3cea2909980670791909cc48c9/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.

## Partnership Eval 

Select ONE of the following choices by deleting the other two options.

B) My partner and I contributed not *exactly* equally, but *roughly*
   equally to this assignment.


If you chose C, please give some further explanation below describing
the state of your partnership and whether and how you have been or are
addressing this disparity. Describe the overall trajectory of your
partnership from the beginning until now. Be honest with your answer
here, and with each other. Even if it's uncomfortable reading this
together right now.

If you chose one of the other two options, you should feel free to
also add some explanation if you wish. 
