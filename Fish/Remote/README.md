# Remote

Implements the server-and-client architecture of Fish.com, a Plan.

The client TCP-connects a player to a server according to [Remote Interactions](https://www.ccs.neu.edu/home/matthias/4500-f20/remote.html). The server awaits TCP connections according to [Remote Interactions](https://www.ccs.neu.edu/home/matthias/4500-f20/remote.html).

When a sufficient number of clients are connected, the server signs them up with the manager and asks the latter to run a complete tournament; when the manager’s work is done, your server shuts down. If there aren’t a sufficient number of clients signed up at the end of the waiting period, the server shuts down without running a tournament.

## Project Structure

- *client.py* Fish.com server
- *server.py* Fish.com clients
- *remote_player_proxy.py* Player proxy used to establish connection between server and clients
- **Other/** All other files
	- **tests/** contains unit tests for py files in the Remote/ directory
	- *json_serializer.py* utility encodes and decodes Fish.com related logic to/from json

## Modifications

Modifications to pieces of code outside of the Remote/ directory

## Modifications
1. Added set_color to player_interface, as it is needed for any player to know what color they are in a given game.
2. Added notify_opponent_colors to player interface, as we need to be able to inform players who they are playing against (according to the protocol given to us)
3. Implemented set_color and notify_opponent_colors in player.py to conform to the player_interface changes
4. Fixed bug in tournament manager, previously did not __notify_players after first round is played, resulting in losers not knowing to exit.
5. Added 'DISCONTINUED' to PlayerStatus enum which represents players that have been discontinued from a tournament due to a business logic, safety, or DoS bug.
6. Refactored manager.py to include a list a players in the tournament who have been kicked for cheating or failing.
7. Refactored manager.py to include a fish number, which if modified makes every tile of every game have the modified number of fish.
8. Refactored manager.py to kick player's who did not respond to a tournament start or end notification
9. Refactored referee.py to have players set their color and acknowledge other player's colors
10. Modified state.py's deepcopy method to include the move_log in the copy
11. Added a test to strategy_tests.py showing applying the minimax algorithm on a 5x5 board with no holes and 4 players directly after placement always takes more than 1 second to compute.

## TODO List

TODOS:
Main
- [ ] Ensure that we can deal with both ill-formed and invalid JSON (on client and RPP side, receive_messages)
- [ ] Add documentation to json_serialization (after dealing with ill-formed and invalid JSON)
- [ ] Create unit tests for server
- [ ] Create unit tests for client
- [ ] Create unit tests for remote_player_proxy

Cleanup
- [ ] Sanity check specification vs. implementation
- [ ] Testing (manual and unit testing)
- [ ] Test xclients and xserver on the Khoury Machines
- [ ] Finish filling out this README

Done
- [x] RPP must handle abnormal conditions from network (i.e. a 1 sec timeout needs to implemented on all of its calls, and must be declared a failed player)
- [x] Ensure we are failing players that don't return string "void" when no response is expected
- [x] Check on RPP for "void" message
- [x] Timeout of 1 second isn't enough for some players because minimax takes too long, look into this. Verdict: This is expected.
- [x] Fix take-turn JSON message to include [Action, ..., Action] as per spec (not sure what we would use these for)
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
- [x] update repo level readme with 10/ info
- [x] Write the server's interpretation
- [x] Ensure that allocations to games are happening according to age
