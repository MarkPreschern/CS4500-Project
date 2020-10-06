## Game State Representation ##

We decided to represent our gamestate via Python objects. We will use these objects to keep track of the game during the local development phase of the project. Once we implement the networking features of our project, we will be able to serialize these Python objects to JSON objects so that we can send relevant gamestate fields to all players via a TCP connection. 

Things to keep track of:
- players (color, name, age, position, status = ACTIVE/IDLE/KICKED)
- board state (tiles, gaps)
- timestamp / time-elapsed

### Tiles ###
Tiles will be represented in their own unique format via a Python object/class. The tile class will contain two fields:  
- Type: represents the type of tile; stored as an enum; will either be regular tile or hole
- Fish_no: represents the number of fish currently on that tile

The **tile** representation as a Python dictionary / JSON object will look something like this:

{  
    "type": 0
    "fish_no": 2  
}

Please note that the current version of our project already has a Tile class that keeps track of the above information.

### Game state ####  
The game state will be represented in its own unique format via a Python object/class. The game state class will contain four fields:  
- Players: this will be a dictionary of all of the players that are currently participating in the game. Each entry of the dictionary will use the player_id as a key and a dictionary of relevant player information as the value.
- Board: this will be a dictionary that keeps track of all of the tiles and player positions on the board. This includes tile objects and their coordinates, as well as player ids and their positions.
- Game Status: this will be an enum that represent the current status of the game (i.e. is the game still accepting players, is the game active, is the game over)
- Timestamp: this will be a double that represents the current system timestamp of the game.
  
The **game state** representation as a Python dictionary / JSON object will look something like the following:  

{  
   "players": {  
        "id" : {  
            "name": '',   
            "color": '',  
            "status": '',  
            "score": ''  
        },  
        ...  
   },  
   
   "board": {  
        "tiles": [  
           [x, y, tile_obj],  
           [x, y, tile_obj]  
           ...  
        ],  
        "player_pos": {  
            "player_id": [x, y],  
            "player_id2": [x, y],  
            ...  
        }  
   },  

   "gameStatus": 0,    
   "timestamp": 12321424.14  
}  

## External Interface ##
Our interface will consist of the following functionality:  
- `get_gamestate`: allow players to get the current gamestate (will be rate limited to prevent players from abusing the network)
  - Args: *none*
  - Returns: gamestate object
- `place_player`: allow players to make their initial placements and execute moves
  - Args: `x: int, y: int` to represent desired position
  - Returns: boolean flag to indicate a successful placement or a failue (e.g. if another player has already placed their penguin in the specified position, if the move is invalid, etc.)
- `send_heartbeat`: sends a hash that corresponds to a gamestate; if the client gamestate does not match the server's gamestate, then the server will send a gamestate that matches the current one; will be sent intermittently; will be mandatory by having the server expect a heartbeat from each client and removing clients that do not send a heartbeat after a given timeout; will also remove clients that refuse to accept the current gamestate
  - Args: *none*
  - Returns: *none*
- `get_tournamentstate`: allows players to receive information on the current tournament
  - Args: *none*
  - Returns: relevant information on the tournament (i.e. player ranks, current round, other information that will likely be defined in a future assignment)

In terms of the required functionality of our external interface, the `get_gamestate` method will let players take turns by allowing players to check if their status is "active" or "inactive". The `get_gamestate` method will also allow players to receive information about the end of the game via the "gameStatus" field in the gamestate object. The `place_player` method will allow players to make their initial placements on the board and will let them replace their penguins if another player has already placed in the spot that they selected. 