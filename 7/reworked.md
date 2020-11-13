 - >insufficient interpretation of the board
(it should be clear what all components of the data definition mean,
 how the data definition represents a real game board,
 what coordinates mean (there are 2+ possible coordinate systems), etc. 
 How does a user of your Board know what hexagonal tile the coordinate (2,3) 
 corresponds to? What does the edge list mean? And so on.)
    - We completed the Board interpretation by explaining our coordinate system,
      edge list and all other definitions we were missing.
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39/Fish/Common/board.py#L15-L41
 
 - >insufficient interpretation of the game state
(it should be clear
 how players are related to penguins and how penguins' locations are tracked,
 what is the order of players and how they take turns,
 etc.)
    - We completed the interpretation to explain the components mentioned in the feedback.
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39/Fish/Common/state.py#L21-L45
    
 - >The game tree node implementation cannot represent all three kinds of nodes:
game-is-over, current-player-is-stuck, and current-player-can-move.
only current-player-can-move is obvious
    - We completed the interpretation to say that the current player could not be stuck and to mention support for game-over states.
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/3744c1375e3b654b8b854e01b2eeb5e3fe90ea39/Fish/Common/game_tree.py#L10-L25

 - >The assignment specified some required functionality for game trees, using the language "for a given tree node and [other inputs]". For methods on a class, it is implied that the method is "given" the instance of the class where it's located, and in Python, the `self` parameter actually makes this explicit. It is not necessary to take another GameTree as a parameter.
    - We removed the `@staticmethod` attribute from previously static members `try_action` and `apply_to_child_states` and made them dynamic.
    - fix:  https://github.ccs.neu.edu/CS4500-F20/quintana/blob/7ee74748d64fc43e78cdde18b462f1778dec6478/Fish/Common/game_tree.py#L116-L147
    
    
 - >README does not explain how project is organized (file/folder structure)
(README is not up to date)
    - We added `Admin/` and `Player/` to our README and explained what they are.
    - fix 1: https://github.ccs.neu.edu/CS4500-F20/quintana/commit/b8ce0ef4e2a7d8baa00f9e1dc698e1e4686edeec#diff-f4923aab63564278027a266fe91df7a4
    - fix 2: https://github.ccs.neu.edu/CS4500-F20/quintana/commit/d88770effa24d23414620c61946d42a90fd4917a#diff-f4923aab63564278027a266fe91df7a4

 - >choosing turn action: purpose statement doesn't specify what happens
when the current player does not have valid moves
    - We completed the purpose statement of two of the methods employed in minimax to mention that the current player can never be stuck.
    - fix 1: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/master/Fish/Player/strategy.py#L76-L78
    - fix 2: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/master/Fish/Player/strategy.py#L116-L117

 - >no separate function to handle a single turn (1 player making 1 move)
    - We refactored the single-turn logic into an individual function to handle individual player turns.
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/4c61de7e9c8cb445edf3561023b10543457d73f7/Fish/Admin/referee.py#L404-L428
 
 -   > Referee documentation does not address all abnormal player conditions
    (note that even failing to respond can already happen
     without remote communication, e.g. if the player goes into an infinite loop)
    What is missing:
      >  * calls to player methods that result in exceptions  
      >  
      >  * player possibly mutates referee's trusted data structures
      >-- no deduction for that
      >(e.g. when self.__state is passed to the player
      > in current_player_obj.get_action(self.__state));
      >if mutation of referee's data is impossible, document why that is the case
        - We documented the abnormal conditions we were missing.
        - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/4c61de7e9c8cb445edf3561023b10543457d73f7/Fish/Admin/referee.py#L44-L49

- >no separate method/function that implements protection of calls to player
    - Created a method to handle the timed & isolated execution of calls to IPlayer objects. 
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/4c61de7e9c8cb445edf3561023b10543457d73f7/Fish/Admin/referee.py#L379-L402

- >unit tests only cover one abnormal condition (players failing in one way,
but e.g. no exceptions)
    - Added tests to test players failing in placement & moving by entering an infinite loop and/or throwing an Exception.
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/4c61de7e9c8cb445edf3561023b10543457d73f7/Fish/Admin/Other/tests/referee_tests.py#L423-L541
