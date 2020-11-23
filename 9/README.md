# xgui

> A testing harness that tests the functionality of `game_visualizer.py`. The harness consumes a single integer between 2 and 4 inclusive which specifies the number of AI players in a game. The program visualizes the progress of a game with the specified number of players on a graphical user interface and removes the GUI elements upon completion.

## Project structure

- *xgui* (program entry point)
- **Other/**
	- contains program logic

## Usage
- General usage: 
	- `./xgui <int>`
    - Running xgui will accept a single integer as a program argument and visually display the entire game on a GUI. 

- To alter program logic:
	- Edit `xgui.py` in **Other**