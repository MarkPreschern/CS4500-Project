# TODO List

TODOS:
Main
- [X] Create unit tests for JSON serializer
- [X] Ensure that we can deal with both ill-formed and invalid JSON (on client and RPP side, receive_messages)
- [X] Ensure that allocations to games are happening according to age
- [X] Add documentation to json_serialization (after dealing with ill-formed and invalid JSON)
- [X] Write the server's interpretation
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
- [x] Create unit tests for server
- [x] Create unit tests for client
- [x] Create unit tests for remote_player_proxy

Cleanup
- [x] Sanity check specification vs. implementation
- [x] Test xclients and xserver on the Khoury Machines
- [x] Finish filling out this README


