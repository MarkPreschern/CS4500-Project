# xstate

> A testing harness that ensures JSON input that represents a game state produces the correct execution of a potential
move for the first player's first avatar. In other words, the testing harness takes a JSON representation of a game state, attempts to move the first player's first avatar in the proper order of directions (North, Northeast, Southeast, South, Southwest, Northwest), and either returns the game state produced from this execution or returns false.

## Project structure

- *xstate* (program entry point)
- **Other/**
	- contains program logic, unit tests, and extra json test files
- **Test/**
    - contains JSON test files

## Usage
- General usage: 
	- `./xstate`
    - Running xstate will accept JSON input and produce the corresponding JSON output once program execution is ended.

- To run unit tests:
    - Run `./xstate --unit`. This will display the output of all unit tests instead of the json file test results.

- To alter program logic:
	- Edit `xstate.py` in **Other**
