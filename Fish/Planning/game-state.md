## Game states

Things to keep track of:
- players (color, name, age, position, status = ACTIVE/IDLE/KICKED)
- board state (tiles, gaps)
- timestamp / time-elapsed



tile {  
    "type": 0,1,2  
    "fish_no": 0,1,2..
}

### Game state ####
{  
   "players": {  
        "id" : {  
            "name": ''   
            "color": ''
            "position": [122, 323]  
            "status": ''  
        },
        ...
   },  
   
   "board": {
        "tiles": [
           [x, y, tile_obj],
           [x, y, tile_obj]
           ...
        ]
   },
   
   "timestamp": 12321424.14
}  

  