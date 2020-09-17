# xjson

> A program that can consume a sequence of well-formed JSON values and deliver JSON in return

## Project structure

- **xjson** (program entry point + program logic)
- **Test**
	- contains test files
    - `1-in.json`: contains mock input
    - `1-out.json`: contains expected output

## Usage
- General usage: 
	- `xjson` + any JSON input to stdin after execution + `ctrl-D`

- To run tests:
	- `./xjson < Test/1-in.json | diff - Test/1-out.json`
    
- To alter program logic:
	- Edit `xjson`