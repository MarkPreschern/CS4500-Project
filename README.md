# CS4500 - Andrew Nedea and Mark Preschern

## Folders in this Repo
- B: the code in B is meant to provide a tool that can infinitely output any command line arguments that you provide. The output can also be limited to 20 lines. This folder contains Assignment B of the TAHBPL series of assignments.
- C: the code in C is meant to provide a tool that can accept an arbitrarily long sequence of well-formed JSON values from standard input and print JSON to standard out with helpful information regarding the input that was provided. This folder contains Assignment C of the TAHBPL series of assignments.
- D: project D is a small program that renders a hexagon of the provided size. The size is a a positive integer given as
a command line input. The program can be quit by clicking anywhere within the hexagon.
- E: the code in E is a small program that uses the same functionality provided in project C while allowing clients to interact with a server via TCP functionality.
- Fish: contains the code needed to implement the Fish game
- 3: contains test harness xboard, a small program that takes a JSON input describing a Fish board configuration and a start position, and outputs a JSON containing
the number of reachable positions for the given position. 
- 4: contains test harness xstate, which serves as integration tests for our State implementation. The harness takes in a complete
state and produces a new state if a move is possible on the current player's first avatar. Otherwise, it produces False. The directory also
includes unit tests for said harness, as well as a series of test input and output JSON files that can be used with the harness.
- 5: contains the test harness for milestone 5 (xtree), which checks the integrity of the GameTree by attempting to make
an action on behalf of the current player, and then determining the best move an opponent could make
to a tile neighboring the one the player just moved to. It determines the "best" such move by inspecting the
neighboring tiles clockwise from North to South West and picking the first action that could get an opponent's
avatar there. If multiple avatars can reach the same "best" tile, the avatar with the lowest source and destination
coordinates lis picked (in order of priority: source.x, source.y, destination.x, destination.y).
- 6: contains the test harness for milestone 6 (xstrategy), which checks the integrity of a player strategy that determines the best action a player can take. See the README in 6 for more information.
- 7: contains a series of markdown files documenting outstanding issues, bug fixes and reworked items.
- 8: contains the test harness for milestone 8 (xref), which checks the integrity of a referee running a full game and producing as output the winning player(s). See the README in 8 for more information.