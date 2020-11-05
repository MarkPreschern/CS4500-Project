# xstrategy

> A testing harness that tests the functionality of `strategy.py`. The harness consumes JSON input from STDIN in the form of a JSON list. The JSON list has a depth and a state. The harness will then compute the best action that the first player in the state can take (using either avatar). It will output the best action to STDOUT, where an Action can either be a list of Positions or false.

## Project structure

- *xstrategy* (program entry point)
- **Other/**
	- contains program logic, unit tests
- **Test/**
    - contains JSON test files

## Usage
- General usage: 
	- `./xstrategy`
    - Running xstate will accept JSON input and produce the corresponding JSON output once program execution is ended.

- To run unit tests:
    - Run `./xstrategy --unit`. This will display the output of all unit tests instead of the json file test results.

- To alter program logic:
	- Edit `xstrategy.py` in **Other**
