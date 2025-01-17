## Self-Evaluation Form for Milestone 9

You must make an appointment with your grader during his or her office
hour to demo your project. See the end of the self-eval for the assigned
grader. 

Indicate below where your TA can find the following elements in your strategy 
and/or player-interface modules: 

1. for human players, point the TA to
   - the interface (signature) that an AI player implements
   - the interface that the human-GUI component implements
   - the implementation of the player GUI

2. for game observers, point the TA to
   - the `game-observer` interface that observers implement
   
   See [Here](https://github.ccs.neu.edu/CS4500-F20/buffalogap/blob/3b7a8e82376790e4b730a32712acb01cdc8247b4/Fish/Admin/game_visualizer.py).
   
   - the point where the `referee` consumes observers 
   
   Observers can subscribe to game state updates [Here](https://github.ccs.neu.edu/CS4500-F20/buffalogap/blob/3b7a8e82376790e4b730a32712acb01cdc8247b4/Fish/Admin/referee.py#L605-L619).

   - the callback from `referee` to observers concerning turns
   
   See the callback from referee to observers implemented [Here](https://github.ccs.neu.edu/CS4500-F20/buffalogap/blob/3b7a8e82376790e4b730a32712acb01cdc8247b4/Fish/Admin/referee.py#L487-L512)
   and the observer utilizing the callback [Here](https://github.ccs.neu.edu/CS4500-F20/buffalogap/blob/3b7a8e82376790e4b730a32712acb01cdc8247b4/Fish/Admin/game_visualizer.py#L110-L111).


3. for tournament observers, point the TA to
   - the `tournament-observer` interface that observers implement 
   - the point where the `manager` consumes observers 
   - the callback to observes concerning the results of rounds 


Do not forget to meet the assigned TA for a demo; see bottom.  If the
TA's office hour overlaps with other obligations, sign up for a 1-1.


**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "3b7a8e82376790e4b730a32712acb01cdc8247b4".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/buffalogap/tree/3b7a8e82376790e4b730a32712acb01cdc8247b4/Fish>

Assigned grader = Peter Abbondanzo (abbondanzo.p@northeastern.edu)

