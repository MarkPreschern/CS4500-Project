This file should explain the file organization of the folder. At this point you have seen how the code for this project is organized according to concepts (not artificial language constraints), and you should be able to match this kind of organization.

Also, if you modify other pieces of code, describe these modifications in a separate section in this README file.

1. Added set_color to player_interface, as it is needed for any player to know what color they are in a given game
2. Added notify_opponent_colors to player interface, as we need to be able to inform players who they are playing against
(according to the protocol given to us)
3. [BUG] tournament manager did not __notify_players after first round is played, resulting in losers not knowing to exit.

TODOS:
[ ] Fix take-turn JSON message to include [Action, ..., Action] as per spec (not sure what we would use these for)
[ ] Ensure board type is correct (make fish constant, no holes, 5x5, etc)
[ ] Ensure that failed players are counted in the final output
[ ] RPP must handle abnormal conditions from network (i.e. a 1 sec timeout needs to implemented on all of its calls, and
    must be declared a failed player)
[ ] Add argument parsing to xserver and xclients according to specification.
[ ] Fix player allocation method to prefer games of 3 until must move on to 2
[ ] Ensure that we can deal with both ill-formed and invalid JSON (on client and RPP side)
[ ] Fix that server sign up rounds works according to specification, need to deal with not enough players
[ ] Ensure that allocations to games are happening according to age
[ ] Ensure that turns are being taken according to age
[ ] Handle case where client connects but doesn't send their name (drop this connection)

[ ] Sanity check that both remote and logical interactions follow the protocol diagrams
[ ] Testing (manual and unit testing)
[ ] Finish filling out this README