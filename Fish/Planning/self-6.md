## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*, 
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- the functionality for "place all penguins"  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L276-L330

- a unit test for the "place all penguins" funtionality  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/Other/tests/referee_tests.py#L141-L230  
**Note:** our "place all penguins" functionality is in the form of a private method in our referee class. Therefore, we don't have direct unit tests for it. However, by including this first test that checks for correct player placements, we inherently verify that our "place all penguins" functionality works

- the "loop till final game state"  function  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L361-L392


- this function must initialize the game tree for the players that survived the start-up phase  
Function Definition: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L179-L202  
Line where game tree is initialized: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L197


- a unit test for the "loop till final game state"  function  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/Other/tests/referee_tests.py#L141-L230  
**Note:** our "loop till final game state" functionality is in the form of a private method in our referee class. Therefore, we don't have direct unit tests for it. However, by including tests that check the final game report in the unit tests linked above, we are inherently showing that our referee successfully loops the game until the final game state is reached.


- the "one-round loop" function  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L361-L392    
**Note:** our `__run_game` method that we referenced above has the capability to run one round. However, this functionality is nested in a while-loop that runs all rounds in the game.


- a unit test for the "one-round loop" function  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/Other/tests/referee_tests.py#L232-L259  
**Note:** our "one-round loop" functionality is in the form of a private method in our referee class. Therefore, we don't have direct unit tests for it. However, by including tests that check the execution of the full game, we are inherently showing that our referee can successfully run one round of the game

- the "one-turn" per player function  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L361-L392  
**Note:** our `__run_game` method that we referenced above has the capability to run a single player turn. However, this functionality is nested in a while-loop that runs all player turns in order for the duration of the game.


- a unit test for the "one-turn per player" function with a well-behaved player 
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/Other/tests/referee_tests.py#L141-L230    
**Note:** our "one-turn per player" functionality is in the form of a private method in our referee class. Therefore, we don't have direct unit tests for it. However, by including tests that check the execution of the full game for a game where all players follow the rules, we are inherently showing that our referee can run one turn per player successfully.


- a unit test for the "one-turn" function with a cheating player  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/Other/tests/referee_tests.py#L232-L259    
**Note:** our "one-turn per player" functionality is in the form of a private method in our referee class. Therefore, we don't have direct unit tests for it. However, by including tests that check the execution of the full game for a game where a player cheated , we are inherently showing that our referee can run a single turn successfully and remove players who cheat on their turn.


- a unit test for the "one-turn" function with an failing player  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/Other/tests/referee_tests.py#L346-L373    
**Note:** our "one-turn per player" functionality is in the form of a private method in our referee class. Therefore, we don't have direct unit tests for it. However, by including tests that check the execution of the full game for a game where a player cheated , we are inherently showing that our referee can run a single turn successfully and remove players who fail on their turn


- for documenting which abnormal conditions the referee addresses  
https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L33-L48


- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing  
  - When the referee kicks a player, they invoke `__kick_player` here: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L379  
  - After invoking `__kick_player`, the `__fire_game_state_changed` function is invoked here: https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L359  
  - **The game state is updated at this line in __fire_game_state_changed:** https://github.ccs.neu.edu/CS4500-F20/wellman/blob/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish/Admin/referee.py#L418  



**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/wellman/tree/ad69dab4fcd1f23eb39751b10d3320ccdeb02bc2/Fish>

