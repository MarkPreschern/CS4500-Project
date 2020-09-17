# xjson

> A program that can consume a sequence of well-formed JSON values and deliver JSON in return

## Project structure

- **xjson** (program entry point)
- **Test**
	- contains program logic and tests

## Usage
- General usage: 
	- `xjson` + any JSON input to stdin after execution + `ctrl-D`

- To run tests:
	- In **Test /** run:
		- `./xjson < Test/1-in.json | diff - Test/1-out.json`