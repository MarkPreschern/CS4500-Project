# xboard

> A testing harness that ensures json input files that represent Fish game boards produce the correct number of reachable positions according to json output files.

## Project structure

- *xboard* (program entry point)
- **Other/**
	- contains program logic and unit tests
- **Test/**
    - contains JSON test files

## Usage
- General usage: 
	- `xboard`
    - Runs testing for all input/output json file pairs (i.e. runs for 1-in.json and 1-out.json, 2-in.json and 2-out.json, etc.)

- To run unit tests:
    - Run `./xboard --unit`. This will display the output of all unit tests instead of the json file test results.

- To alter program logic:
	- Edit `xboard.py` in **Other**
