# xtcp

> A small TCP server that takes a series of JSON values and returns a formatted output

## Project structure

- *xtcp* (program entry point)
- **Other/**
	- contains program logic and helpers
- **Test/**
    - contains tests

## Usage
- General usage: 
	- `xtcp [port_no]`
    - The server default to port 4567 if one is not provided.
    - The server exits within 3 seconds of starting if no client connects.
- Example:
	- `xtcp 1234` → runs on port 1234

- To run tests:
    - Pick a test to run (X=1-3).
    - Start server on a port (say 3433).
	- In a new terminal in the **Test/** directory run (within 3 seconds of starting the server):
        - `cat testX-in.json | nc localhost 3433`, where X is the test number
	- The response you get back in the new terminal should match up with the contents of the
      `testX-out.json` file.

- To alter program logic:
	- Edit `xtcp.py` in **Other**
