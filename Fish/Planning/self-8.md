## Self-Evaluation Form for Milestone 8

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

1. did you organize the main function/method for the manager around
the 3 parts of its specifications --- point to the main function

  - For the most part, yes. Our main method ([run()](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish/Admin/manager.py#L150-L186)), notifies the players that the tournament is about to start, runs the game via calls to `__run_round` (wherein players get allocated to games), and lastly notifies the winners that they have won the tournament. The notification of the losing players that they have lost the game (and therefore the tournament) is done from the main-loop via [`__notify_players()`](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish/Admin/manager.py#L164-L176).

2. did you factor out a function/method for informing players about
the beginning and the end of the tournament? Does this function catch
players that fail to communicate? --- point to the respective pieces

- We have a method for notifying players about the start of the tournament [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish/Admin/manager.py#L137-L148) that removes any players that fail to acknowledge the start of the tournament.

- We have a method for notifying winners that casts the winners that fail to accept the notification as losers [here](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish/Admin/manager.py#L188-L211). Players that lose the final game of the tournament are notified via [`__notify_players`](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish/Admin/manager.py#L213-L257). However, if a losing player refuses to accept a notification, nothing happens as they've already lost.

3. did you factor out the main loop for running the (possibly 10s of
thousands of) games until the tournament is over? --- point to this
function.

No, we have not factored out the main loop. The main loop lives in [`run()`](https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish/Admin/manager.py#L150-L186), but all other functionality in run() has been factored out into different methods.

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/quintana/tree/7ac2c59ebe52c8b60dfc54d20b0d3233b7dd6ef6/Fish>

