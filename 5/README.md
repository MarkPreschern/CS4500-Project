# xtree

> A testing harness that tests the functionality of game tree. The harness accepts a JSON object from STDIN. This object contains a state object, a from position, and a to position. The test harness attempts to move one of the first player's avatars from the from position to the to position. If the action is illegal, the input object is considered invalid input. Otherwise, the harness will attempt to find an action that the second player can take to move to a tile that is adjacent to the one that the first player just conquered. If there is a possible action, a list of [Position, Position] is printed to STDOUT. If there is no such action, it prints false to STDOUT.

## Project structure

- *xtree* (program entry point)
- **Other/**
	- contains program logic, unit tests
- **Test/**
    - contains JSON test files

## Usage
- General usage: 
	- `./xtree`
    - Running xstate will accept JSON input and produce the corresponding JSON output once program execution is ended.

- To run unit tests:
    - Run `./xtree --unit`. This will display the output of all unit tests instead of the json file test results.

- To alter program logic:
	- Edit `xtree.py` in **Other**
