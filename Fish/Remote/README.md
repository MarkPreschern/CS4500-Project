This file should explain the file organization of the folder. At this point you have seen how the code for this project is organized according to concepts (not artificial language constraints), and you should be able to match this kind of organization.

Also, if you modify other pieces of code, describe these modifications in a separate section in this README file.

1. Added set_color to player_interface, as it is needed for any player to know what color they are in a given game.
2. Added notify_opponent_colors to player interface, as we need to be able to inform players who they are playing against (according to the protocol given to us)
3. Implemented set_color and notify_opponent_colors in player.py to conform to the player_interface changes
4. [BUG] tournament manager did not __notify_players after first round is played, resulting in losers not knowing to exit.
5. Added 'DISCONTINUED' to PlayerStatus enum which represents players that have been discontinued from a tournament due to a business logic, safety, or DoS bug.
6. Refactored manager.py to include a list a players in the tournament who have been kicked for cheating or failing.
7. Refactored manager.py to include a fish number, which if modified makes every tile of every game have the modified number of fish.
8. Refactored manager.py to kick player's who did not respond to a tournament start or end notification
9. Refactored referee.py to have players set their color and acknowledge other player's colors

TODOS:
Main
- [ ] Ensure that we can deal with both ill-formed and invalid JSON (on client and RPP side, receive_messages)
- [ ] Add documentation to json_serialization (after dealing with ill-formed and invalid JSON)
- [ ] 1/2 done: Fix take-turn JSON message to include [Action, ..., Action] as per spec (not sure what we would use these for)
- [ ] Fix player allocation method to prefer games of 3 until must move on to 2
- [ ] Ensure that allocations to games are happening according to age
- [ ] Timeout of 1 second isn't enough for some players because minimax takes too long, look into this. Remove time print statements in Client when done.
- [ ] Create unit tests for server
- [ ] Create unit tests for client
- [ ] Create unit tests for remote_player_proxy
- [ ] Write the server's interpretation

Cleanup
- [ ] Sanity check specification vs. implementation
- [ ] Testing (manual and unit testing)
- [ ] Finish filling out this README

Done
- [x] RPP must handle abnormal conditions from network (i.e. a 1 sec timeout needs to implemented on all of its calls, and must be declared a failed player)
- [x] Ensure we are failing players that don't return string "void" when no response is expected
- [x] Check on RPP for "void" message
- [x] Handle case where client connects but doesn't send their name (drop this connection)
- [x] Refactor tournament manager to have seperated cheaters and failed players (and losers)
- [x] Add DEBUG to logs (client and server)
- [x] Ensure board type is correct (make fish constant, no holes, 5x5, etc)
- [x] Add argument parsing to xserver and xclients according to specification.
- [x] Handle case where two players give the same name
- [x] Add README to Runnables Task
- [x] Fix that server sign up rounds works according to specification, need to deal with not enough players
- [x] abstract out code in run method of server
- [x] abstract out code in run method of client
- [x] Use 'ascii' encoding instead of 'utf-8'
- [x] Find out where 'timed out' message is coming from and add it to debug
- [x] clients don't close connection when kicked, fix this