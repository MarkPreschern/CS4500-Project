This file should explain the file organization of the folder. At this point you have seen how the code for this project is organized according to concepts (not artificial language constraints), and you should be able to match this kind of organization.

Also, if you modify other pieces of code, describe these modifications in a separate section in this README file.

1. Added set_color to player_interface, as it is needed for any player to know what color they are in a given game
2. Added notify_opponent_colors to player interface, as we need to be able to inform players who they are playing against
(according to the protocol given to us)
3. [BUG] tournament manager did not __notify_players after first round is played, resulting in losers not knowing to exit.