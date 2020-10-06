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
The game state will be represented in its own unique format via a Python object/class. The game state class will contain three fields:  
- Players: this will be a dictionary of all of the players that are currently participating in the game. Each entry of the dictionary will use the player_id as a key and a dictionary of relevant player information as the value.
- Board: this will be a dictionary that keeps track of all of the tiles and player positions on the board. This includes tile objects and their coordinates, as well as player ids and their positions.
- Timestamp: this will be a double that represents the current system timestamp of the game.
  
The **game state** representation as a Python dictionary / JSON object will look something like the following:  

{  
   "players": {  
        "id" : {  
            "name": ''   
            "color": ''  
            "status": ''  
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
   
   "timestamp": 12321424.14  
}  

## External Interface ##
Our interface will consist of the following functionality:  
- Pong / Heartbeat: