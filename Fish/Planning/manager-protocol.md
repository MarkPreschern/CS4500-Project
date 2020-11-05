## Tournament Manager Protocol

The protocol for the tournament manager API can be described via the following diagram:

![](manager-protocol-diagram.png)

**Note: to see our diagram in more detail, please zoom in or click on the image.*

Below, we will explain the protocol in more detail.

### Beginning a Tournament
A tournament is begun by the Sign-Up Server. It will provide the TournamentManager with the list of Players who have signed up for the tournament (sorted by age) via a call to `run_tournament`.

### Tournament Observers
A TournamentObserver can receive tournament updates periodically by invoking the `subscribe_tournament_updates` method. Ideally, this will occur before the tournament begins, but it could occur at any point during the tournament's execution (i.e. until the tournament ends). See the interface for more details on what updates they can receive.

A TournamentObserver can receive tournament statistics at any time during the tournament by invoking `get_tournament_statistics`. 

### Running the Tournament
Once the tournament has begun, the TournamentManager will create some number of games N for each round of the tournament. In doing so, it will divide the non-eliminated players of the tournament into games with an equal number of people (see interface for more detail). It will then create N Referee objects, providing proper dimensions for the board and the subset of Players in the game that the Referee will run. The TournamentManager will invoke `subscribe_final_game_report` for each Referee so that it can be notified when each game ends. 

Prior to beginning the games in the round, the TournamentManager will alert each TournamentObserver that a new round is beginning and give details on the games that will be run by invoking the callback function the TournamentObservers provided in `subscribe_tournament_updates`. See the interface for a description of what the data format looks like for these updates.

The TournamentManager will invoke the `start` method for each Referee in order to begin the games in the round. Once a game has been finished, the Referee running that game will send the final game report back to the TournamentManager via the callback function that the TournamentManager provided in `subscribe_final_game_report`. Once all final game reports have been received, the TournamentManager will either begin a new round and repeat the process outlined above or it will end the tournament.

### Ending the Tournament
When the tournament has ended and there is a final winner, the TournamentManager will send a final update to all TournamentObservers indicating the winner of the tournament, the standings of the final game, and other tournament information (see the interface for more details on what the data format for this update looks like). It will do so by invoking the callback function provided by each TournamentObserver when they invoked `subscribe_tournament_updates`. 
