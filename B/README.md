# xyes

> A generalized *yes* with a print limit option

## Project structure

- **xyes** (program entry point)
- **Other**
	- contains program logic and tests

## Usage
- General usage: 
	- `xyes [-limit] [arg1 arg2 .. ]`
- Examples:
	- `xyes hello` → prints *hello* on a new line forever
	- `xyes` → prints *hello world* on a new line forever
	- `xyes -limit around the world` → prints *around the world* on a new line 20x times

- To run tests:
	- In **Other /** run:
		- `./run_tests` to run ALL tests
		- `python3 TestB.py` to run test suite for solution B

- To alter program logic:
	- Edit `xyes.py` in **Other**