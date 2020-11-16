# xref

> A testing harness that tests the functionality of `referee.py`. The harness consumes JSON input from STDIN in the form of a JSON object. The JSON object contains a row number, a columns number, a player object containing a list of players arranged in ascending order of age with their corresponding depth, and a fish number. The harness will then compute the result of running the specified game as an array of strings representing players that shared first place. It will output the array to STDOUT.

## Project structure

- *xref* (program entry point)
- **Other/**
	- contains program logic, unit tests
- **Test/**
    - contains JSON test files

## Usage
- General usage: 
	- `./xref`
    - Running xref will accept JSON input and produce the corresponding JSON output once program execution is ended.

- To run unit tests:
    - Run `./xref --unit`. This will display the output of all unit tests instead of the json file test results.

- To alter program logic:
	- Edit `xref.py` in **Other**
