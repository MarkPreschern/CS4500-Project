## Overview
Describe file organization and architecture here.

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