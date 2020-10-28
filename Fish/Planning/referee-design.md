# Referee

### Game setup

The referee takes in a list of players (including their respective ids, ages and names) and a board dimension (specified as rows and columns). In creating the board, the referee will verify that the given board dimensions are large enough to accomodate the given players. If the board is not large enough, the referee will not proceed with board creation. The referee will also decide which tiles to remove to attain a configurable difficulty factor. The difficulty factor is a built-in number that speaks to the maximum number of holes that can be present on the board.

After setting up the board, the referee assigns each player a color. A new sorted player list is then created sorted in increasing order of their ages without any reference to their individual ages. The referee then creates a game state of the board and player list it just put together.

After the game has been setup, the referee will allow third party observers to "subscribe" for state updates. This way, every time a change (placement, move, player removal, game over etc.) is effected on the game state, subscribed observes will be updated with the latest game state. This will allow them to watch a game in "real-time" by rendering the game state supplied by the referee.

### Placement phase

As specified in the player-referee interface, the referee then repeatedly asks each player (in order of their ages) to place an avatar until all avatars have been placed<sup>1</sup>. The referee will send the current game state upon each request. Each placement response (position object) received from a player is checked against the state of the game to make sure it is valid. 

Upon receiving a valid placement response, the referee updates the game state, and informs the game observers and the other players of the placement<sup>2</sup>. To check whether a placement is valid, the referee will leverage the game state.

Upon receiving an erroneous or no response at all (after 10 seconds of waiting), the player is removed from the game<sup>3</sup> and the game observers and other players are notified of said removal<sup>2</sup>. An erroneous response can be a placement on a tile that is already occupied, is a hole, or is outside the bounds of the board. Any of these three responses will result in the referee marking the player as a cheating player and removing said player from the game<sup>3</sup>. Moreover, any response received from the player that is not a Position object (e.g. an Action) is considered a failure by the player to make a placement, and as a result, the referee will mark the player as a failing player and remove them from the game<sup>3</sup>. Similarly, if no response is received from a player after 10 seconds, the referee will mark the player as "failing" and remove them from the game<sup>3</sup>. 

If no players remain in the game or no player can make a placement, the referee shuts down the game (see  **End Phase** for more detail).

### Playing phase

As specified in the player-referee interface, after all avatars have been placed, the referee will start asking each player in order of increasing age to make a move<sup>4</sup> with the exception of stuck players, which are skipped over. A player is stuck if they can't move any of their avatars. The referee will then expect a response back from the player and will wait no longer than 10 seconds. If no response is received, it will remove the player from the game<sup>3</sup>, mark them as "failing", and notify the other parties involved<sup>2</sup> and proceed onto the next player (if there is one). Furthermore, if the referee receives a response that is not an Action object, it will mark the player as "failing", remove that player from the game<sup>3</sup>, and notify all relevant parties of the removal<sup>2</sup>. 

Upon receiving a move response, the referee will check the move the player wishes to make against the game tree to ensure its validity. If deemed valid, the referee updates the game state and sends out an update with the updated game state to all players<sup>2</sup> and game observers. If deemed invalid, the referee marks the player as "cheating", removes the player from the game<sup>3</sup> and notifies all parties (players & observers) of the removal<sup>2</sup>. 

If no players remain in the game or no player can make a move, the referee shuts down the game (see  **End Phase** for more detail).

### Game end

When no player can make a move or all players have been removed from the game, the referee will alert all game observers and players that the game has ended. Upon doing so, the referee will send a leaderboard to all players and game observers containing the score, color, and name of all players who did not cheat/fail throughout the course of the game<sup>5</sup>. It will also send a list of failing players and a list of cheating players<sup>5</sup> to all players and game observers.

The referee will determine that the game has ended by leveraging the game tree. It will use the game tree to check if any player is able to make a move. 

### Footnotes
<sup>1</sup> The referee will ask for placements via a `place_request`. Please see the player-referee interface for more details.  
<sup>2</sup> The referee will notify other players of successful placements/moves or player removals via a `sync`. Please see the player-referee interface for more details.  
<sup>3</sup> The referee will remove players from the game via a `kick_player`. Please see the player-referee interface for more details.  
<sup>4</sup> The referee will ask for moves from players via a `move_request`. Please see the player-referee interface for more details.  
<sup>5</sup> The referee will send all relevant information to other players when the game ends via a `game_over`. Please see the player-referee interface for more details.  

### API

* `subscribe_game_updates(callback: Callable)`: this method will be responsible for subscribing game observers to what is going on during the game. This function takes one parameter called `callback`, which will be a Callable (i.e. a function) invoked by the referee whenever the internal game state changes. A game observer will invoke the `subscribe_game_updates` function and provide their desired callback function as input. This callback function will accept a copy of the current game state in the form of a State object so that the given observer can stay up-to-date on any relevant game information.

* `subscribe_final_game_report(callback: Callable)`: this method will be responsible for subscribing game observers and the tournament manager to the final game report that the referee will send when the game ends. This update will contain the leaderboard of the game, the list of cheating players, and the list of failing players. A Game observer or tournament manager will invoke the `subscribe_final_game_report` function and provide their desired callback function as input. This callback function will accept a dictionary that contains the final game report (see an example of what this would look like below). 
  * Example of `callback` input:
    ```
    {
        "leaderboard": 
            {"player_id1": score1, ..., "player_idN": scoreN},
        "cheating_players": [pId1, ..., pIdN],
        "failing_players": [pId1, ..., pIdN]
    }
    ```  

* `setup_game(rows: int, cols: int, players: list, difficulty=default_num)`: this method will be responsible for carrying out the actions described in the **Game setup** portion of this document. It accepts the number of rows and columns on the board (i.e. board dimensions), a list of the players in the game, and an optional difficulty parameter that will be set to some default value (called `default_num` in the current stub) if no value is provided. This method will be invoked by a tournament manager when they wish to start a new game in the tournament.











