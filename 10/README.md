# xclients & xserver

> A testing harness that tests the functionality of `clients.py` and `server.py`. xserver connects with n clients spawned by xclients (using multiple threads) on a specified port. The server will then run a tournament with the clients where each client employs a standard player using a zig-zag placement pattern and a best-score-at-depth-2 strategy for moving penguins. Each game on the server is on a 5x5 board (no holes) with each tile populated by 2 fish. When the tournament is over, the server prints a JSON array with two natural numbers to STDOUT: [w, cf] where w is the number of tournament winners and cf is the number of players that were caught cheating or that failed during the tournament run. 

## Project structure

- *xclients* (program entry point#1)
- *xserver* (program entry point#2)
- **Other/**
	- contains program logic

## Usage
- General usage: 
	- `./xclients <n> <port> <ip>`
	- `./xserver <port>`
	- Running xclients will accept the number of clients to run, which all connect on the server on a specified port at a specified ip address. If the ip address is ommited, the client connects to "local host" (127.0.0.1).
    - Running xserver will accept a single integer as a program argument (the port number).

- To alter program logic:
	- Edit `xclients.py` and `xserver` in **Other**