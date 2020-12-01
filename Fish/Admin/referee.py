import operator
import sys
from random import randrange

sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

import constants as ct
from player_interface import IPlayer
from board import Board
from state import State
from action import Action
from player_entity import PlayerEntity
from player_kick_reason import PlayerKickReason
from exceptions.InvalidPositionException import InvalidPositionException
from exceptions.InvalidActionException import InvalidActionException
from position import Position
from color import Color
from exceptions.NonExistentPlayerException import NonExistentPlayerException
import pickle
from game_tree import GameTree
import utils


class Referee(object):
    """
    PURPOSE:        This class implements a Referee for the game fish. It is purported to provide all the
                    functionality required for running a game from placements to moves and game end. It
                    reports game updates and the final report (at game end) to observers. The latter includes a list
                    of cheating and failing players, as well as a leader board of all rule-abiding players.

                    A cheating player is one that attempts to perform either an illegal placement (placing on an already
                    occupied tile or outside the bounds of the board) or an illegal move (moving via a path that
                    is unclear of holes or avatars, moving to an occupied tile, moving across corners or tiles that
                    are not accessible in a straight line across parallel hexagon edges, moving in-place, and moving
                    outside the bounds of the board). This determination is for placements is made using the State and
                    whereas the one for moves (or actions) is made using the GameTree. Both State and GameTree will
                    raise appropriate exceptions to indicate abnormal conditions should any occur.

                    A failing player is one that fails to return either a placement or an action. More specifically,
                    if a player returns an object of the wrong type (something that is not a Position for
                    get_placement or something that is not an Action for get_action), it is marked as failing.
                    Similarly, if a player takes takes more than PLAYER_TIMEOUT seconds to respond to the referee or
                    throws any exception(s), it is marked out as failing.

                    The referee will prompt the players for moves and placements by passing a deep copy of its
                    game state. This means that exogenous players will not be able to affect the state maintained
                    by the referee.

                    The referee will remove the cheating and failing players' avatars from the game and prevent them
                    from taking any more turns (that includes placing and moving).

    INTERPRETATION: The referee could best be described as the engine that runs a game of Fish. It receives
                    a list of IPlayer objects that is sorted by age and row and column dimensions of the board from
                    the tournament manager, sets up a homogeneous game board of the specified size and assigns each
                    player a color. The board the referee creates is homogeneous (has the same random number of fish on
                    each tile) and may have holes in it (see paragraph on "difficulty factor"). When signaled to kick
                    off the game (via start()) it then prompts each player for a placement by having them return a
                    Position object containing the row and column number they wish to place their avatar. After it
                    finishes prompting users for placements it prompts each movable player for an Action object
                    (made up of a Position describing the place on the board the move is made from and another
                    describing the place the move is made to).

                    To setup the game board, the referee applies a "difficulty factor" - a Natural number that speaks to
                    the maximum number of Tiles the referee will try to remove. This factor is adjustable and can be
                    leveraged to make a game more challenging or less so. The referee will randomly pick the tiles to
                    remove and may even end up removing 0 tiles for a difficulty factor D > 0.

                    The referee also maintains a master copy of the game State which it updates throughout the course of
                    the game to reflect the players' positions, score etc.. Given the state's design, the current player
                    in it will always be unstuck (stuck players are automatically skipped) unless all players are stuck,
                    in which case the referee ends the game.

                    It also provides functionality that external observers can employ to follow the game. An
                    observer or tournament manager subscribe via `subscribe_game_updates` to receive an update with
                    the latest game state every time it changes (this happens whenever a player makes a placement or
                    move, or is kicked). They can also subscribe to an end game report via `subscribe_final_game_report`
                    to receive a copy of the final game report.

                    The final game report encompasses a list of the cheating players, a list of the failing
                    players and a list of dictionary objects sorted in decreasing order of score,
                    each object containing a rule-abiding player's name, color and score.

                    Here's an example of what the report may look like:

                    {
                        'cheating_players': [IPlayer],
                        'failing_players': [IPlayer],
                        'leaderboard': [
                            {'name': 'Winner', 'color': Color.BLACK, 'score': 99},
                            {'name': 'Runner-up', 'color': Color.WHITE, 'score': 40}
                        ]

                    }

                    Upon determining that no more moves can be made (by calling can_anyone_move() on the internal state)
                    , the referee ends the game and provides all players and subscribed observers with the final game
                    report.

                    At initialization, the referee is given a list of IPlayer objects with undefined colors (.color =
                    Color.UNDEFINED). After assigning colors, the referee creates a PlayerEntity for each object,
                    which contains the essential information needed for identification in the game (namely name,
                    color and placements). All other information pertaining to a player is scrapped. The referee
                    starts running the game (from the placement phase onwards) when start() is called on it (presumably
                    the tournament manager would call it to kick off the game).

                    Throughout the game, every time the internal game state is altered, the game tree is updated,
                    players are synchronized (by calling sync on them with the game state) and observers are notified
                    with a version of the latest one. This keeps all parties informed and the game tree up to date for
                    rule-checking.

    DEFINITIONS:    A losing player is one that does not obtain the largest number of fish in the game, or is one that
                    cheats or fails.

                    A winning player is one that obtains the largest number of fish in the game (and does not cheat).
                    There can be multiple winning players if multiple players obtain the same largest number of fish
                    in the game.
    """
    DEBUG = False

    # Initialize difficulty factor
    DIFFICULTY_FACTOR = 2
    # Initialize player timeout (number of seconds a player is allowd to take to make a move/placement)
    PLAYER_TIMEOUT = 1

    def __init__(self, rows: int, cols: int, players: [IPlayer], fish_no: int = None) -> None:
        """
        Initializes a referee for a game with a board of size row x col and a given (ordered) list of IPlayer
        objects.

        :param rows: row dimension of the board
        :param cols: column dimension of the board
        :param players: list of IPlayer objects sorted in increasing order of age
        :param fish_no: Number of fish to be placed on each tile on the board
        :return: None
        """
        # Validate params
        if not isinstance(rows, int) or rows <= 0:
            raise TypeError('Expected positive int for rows!')

        if not isinstance(cols, int) or cols <= 0:
            raise TypeError('Expected positive int for cols!')

        if not isinstance(players, list):
            raise TypeError('Expected list for players!')

        # Make sure list consists of only IPlayer objects
        if not all(isinstance(x, IPlayer) for x in players):
            raise TypeError('All player list objects have to of type IPlayer!')

        # Make sure we weren't given too many players
        if len(players) < ct.MIN_PLAYERS or len(players) > ct.MAX_PLAYERS:
            raise ValueError(f'Invalid player length; length has to be between {ct.MIN_PLAYERS} and'
                             f' {ct.MAX_PLAYERS}')

        # Make sure dimensions are large enough to accommodate all players
        if cols * rows < len(players):
            raise ValueError('Board dimensions are too small to accomodate all players!')

        # Make sure fish is between 1 and 5 or is equal to None (default value, means that the user didn't specify a
        # fish number.
        if fish_no is not None and \
                (not isinstance(fish_no, int) or fish_no < ct.MIN_FISH_PER_TILE or fish_no > ct.MAX_FISH_PER_TILE):
            raise ValueError('Expected positive int between 1 and 5 inclusive for fish!')

        # Set properties
        self.__players: [IPlayer] = players
        self.__avatars_per_player = 6 - len(players)

        # Make up list of IPlayer holding failing players
        self.__failing_players: [IPlayer] = []
        # Make up list of IPlayer holding cheating players
        self.__cheating_players: [IPlayer] = []

        # Initialize game update callbacks as a list of callable items called every time
        # the state of the game changes
        self.__game_update_callbacks = []

        # Initializes game over callbacks as a list of callable items called at the end
        # of the game together with the game report
        self.__game_over_callbacks = []

        # Make up a board
        self.__board = self.__make_board(cols, rows, fish_no)

        # Send player's color information
        self.__notify_player_colors()

        # Make up state from board & list of PlayerEntity objects
        self.__state = State(self.__board, [PlayerEntity(p.name, p.color) for p in players])
        # Initialize game tree placeholder
        self.__game_tree = None

        # Make up flag to indicate whether the game has started
        self.__started = False
        # Make up flag to indicate whether the game has ended
        self.__game_over = False
        # Initialize empty game report that will be fleshed out at game end
        self.__report = {}
        # Initialize empty list of IPlayer to hold winners (player(s) with the highest score in the game)
        self.__winners = []
        # Initialize empty list of IPlayer to hold losers
        self.__losers = []

    @property
    def game_over(self) -> bool:
        """
        Tells whether the game run by this referee has ended.
        """
        return self.__game_over

    @property
    def game_report(self) -> dict:
        """
        Retrieves game report for the game.
        """
        return self.__report.copy()

    @property
    def winners(self) -> [IPlayer]:
        """
        Retrieves the winners in this game.
        """
        return self.__winners

    @property
    def losers(self) -> [IPlayer]:
        """
        Retrieves the losers in this game.
        """
        return self.__losers

    @property
    def state(self) -> State:
        """
        Retrieves the current game state in this game.
        """
        return self.__state

    def start(self) -> None:
        """
        This method starts the game by first running a series of placement rounds and then
        prompting each player to make a move until game end. At game end, it provides all pertinent
        parties with a copy of the game report.

        :return: None
        """
        # Return if we already started
        if self.__started:
            return

        # RUN ON A SEPARATE THREAD
        # Indicate that game has started
        self.__started = True
        # Run placement rounds
        if self.__run_placements():
            # Initialize game tree for rule checking
            self.__game_tree = GameTree(self.__state)
            # Run game
            self.__run_game()

        # End game
        self.__fire_game_over()

    @property
    def players(self) -> [IPlayer]:
        """
        Returns (copy) collection of players referee oversees.
        """
        return pickle.loads(pickle.dumps(self.__players))

    @property
    def cheating_players(self) -> [IPlayer]:
        """
        Returns collection of IPlayer objects corresponding to cheating
        players.

        :return: resulting list of Color
        """
        return self.__cheating_players

    @property
    def failing_players(self) -> [IPlayer]:
        """
        Returns collection of IPlayer objects corresponding to failing
        players.

        :return: resulting list of Color
        """
        return self.__failing_players

    @property
    def started(self) -> bool:
        """
        Returns boolean flag indicating whether the referee has started
        the game. A game is started when the referee prompts the first player to
        make a placement.

        :return: boolean flag indicating the above
        """
        return self.__started

    def __notify_player_colors(self):
        """
        Assign each player the color that correspond to their position in the player list and notify
        each player which colors they will be playing against. If player's fail to acknowledge the color
        messages, their are marked as failing players.
        :return: None
        """
        # Assign each player the color that correspond to their position in the player list
        game_colors = []
        for index, p in enumerate(self.__players):
            ack = utils.timed_call(Referee.PLAYER_TIMEOUT, p, 'set_color', args=(Color(index),))
            game_colors.append(Color(index))
            # if the player doesn't ack, they are a failing player
            if ack is None or not ack:
                self.__failing_players.append(p)

        # Notify each player which colors they will be playing against
        for player in self.__players:
            colors = [color for color in game_colors if color != player.color]
            ack = utils.timed_call(Referee.PLAYER_TIMEOUT, player, 'notify_opponent_colors', args=tuple([colors]))
            # if the player doesn't ack, they are a failing player
            if ack is None or not ack:
                self.__failing_players.append(player)

    def __make_board(self, cols: int, rows: int, fish_no: int) -> Board:
        """
        Makes a board with the given dimensions. It also applies a difficulty factor to
        the board by removing at most DIFFICULTY_FACTOR tiles. What and how many tiles
        is something determined randomly.

        :param cols: number of columns for the board
        :param rows: number of rows for the board
        :param fish: number of fish to be placed on each tile on the board
        :return: resulting Board object
        """

        # number of fish as a range or set number
        fish_no = randrange(ct.MIN_FISH_PER_TILE, ct.MAX_FISH_PER_TILE) if fish_no is None else fish_no

        # Make up board
        board = Board.homogeneous(fish_no, rows, cols)
        # Determine number of tiles to remove given difficulty factor
        tiles_to_remove = min(Referee.DIFFICULTY_FACTOR,
                              rows * cols - len(self.__players) * self.__avatars_per_player)

        for k in range(tiles_to_remove):
            # Generate random row of tile to remove
            random_row = randrange(0, rows - 1)
            # Generate random col of tile to remove
            random_col = randrange(0, cols - 1)
            # Make up location of tile to remove
            tile_location = Position(random_row, random_col)

            # If it's a hole, skip
            if board.get_tile(tile_location).is_hole:
                continue

            # Remove tile
            board.remove_tile(tile_location)

        # Return resulting board
        return board

    def __run_placements(self) -> bool:
        """
        Runs placements rounds until everyone has placed their avatars. Players may
        get removed in the process for either failing or cheating. If all players
        get removed then the function returns False to indicate there is no point
        in pressing forward with the game. Otherwise, it returns True.

        :return: boolean indicating whether any players remain
        """

        # Determine how many avatars there are to place
        avatars_to_place = self.__avatars_per_player * len(self.__players)

        # Prompt players to place until we've exhausted all avatars
        while avatars_to_place > 0:
            # Cycle over players and have them provide a Position object describing where they
            # wish to place their avatars
            for p in self.__players:
                # Check if player has either failed or cheated; if they have, skip 'em over
                if p in self.__failing_players or p in self.__cheating_players:
                    avatars_to_place -= 1
                    continue

                # Get placement for player using a deep copy of state
                placement = utils.timed_call(Referee.PLAYER_TIMEOUT, p, 'get_placement',
                                             args=(self.__state.deepcopy(),))

                # Validate placement received
                if not isinstance(placement, Position):
                    # If it's not a Position, mark out player as failing & remove player from
                    # state
                    self.__kick_player(p, PlayerKickReason.FAILING)
                    # Decrement avatars needed to be placed
                    avatars_to_place -= 1
                    continue

                try:
                    # Try to place on board
                    self.__state.place_avatar(p.color, placement)
                except InvalidPositionException:
                    # Position is out-of-bounds, already occupied or a hole. Mark player
                    # as cheating & remove player from state.
                    self.__kick_player(p, PlayerKickReason.CHEATING)
                    # Decrement avatars needed to be placed
                    avatars_to_place -= 1
                    continue

                if Referee.DEBUG:
                    print(f'got placement of {placement} from player {p.color}')

                self.__fire_game_state_changed()
                # Decrement avatars needed to be placed
                avatars_to_place -= 1

        # Check if any players remain after placement (everyone might have gotten kicked)
        return self.__state.players_no != 0

    def __kick_player(self, player_obj: IPlayer, reason: PlayerKickReason):
        """
        Kicks provided Player from the game.

        :param player_obj: IPlayer object to kick
        :param reason: reason (str) they're being kicked
        """
        # Validate params
        if not isinstance(player_obj, IPlayer):
            raise TypeError('Expected IPlayer object for player_obj!')

        if not isinstance(reason, PlayerKickReason):
            raise TypeError('Expected PlayerKickReason for reason!')

        if Referee.DEBUG:
            print(f'Kicking {player_obj.color} for reason {reason}')

        if reason == PlayerKickReason.CHEATING:
            self.__cheating_players.append(player_obj)
        else:
            self.__failing_players.append(player_obj)

        # Notify player WHY they're being kicked
        player_obj.kick(reason.name)
        # Remove player from state
        self.__state.remove_player(player_obj.color)
        # Trigger event
        self.__fire_game_state_changed()

    def __run_game(self) -> None:
        """
        This method runs the game after placement by prompting each active player
        for an action. A player is active if they can move and have not been removed from
        the game.

        :return: None
        """
        # Run game by prompting players for actions until nobody can move
        while self.__state.can_anyone_move():
            self.__run_turn()

    def __run_turn(self):
        """
        This method runs a single turn by prompting the current player in the internal state
        to make a move.
        """
        current_player_obj = self.__get_player_by_color(self.__state.current_player)
        try:
            # Get action from player using a deep copy of state
            action = utils.timed_call(Referee.PLAYER_TIMEOUT, current_player_obj, 'get_action',
                                       args=(self.__state.deepcopy(),))

            # If call was not successful or anything but an Action object was returned, the player failed
            if not isinstance(action, Action):
                self.__kick_player(current_player_obj, PlayerKickReason.FAILING)
            else:
                # Use game tree to validate action (will throw InvalidPositionException if
                # action is illegal)
                self.__state = self.__game_tree.try_action(action)

                if Referee.DEBUG:
                    print(f'{current_player_obj.color} just moved from {action.src} to {action.dst}')
                self.__fire_game_state_changed()
        except AssertionError as e:
            # Raise assertion errors are these are used for testing
            raise e
        except InvalidActionException:
            self.__kick_player(current_player_obj, PlayerKickReason.CHEATING)

    def __get_player_by_color(self, color: Color) -> IPlayer:
        """
        Retrieves IPlayer object with provided color.

        :param color: Color of player to retrieve
        :return: associated IPlayer object
        """
        # Validate params
        if not isinstance(color, Color):
            raise TypeError('Expected Color for color!')

        for p in self.__players:
            if p.color == color:
                return p

        raise NonExistentPlayerException()

    def __fire_game_state_changed(self):
        """
        Signals that the game state has changed and it is time to update the game tree, sync all the players and
        notify all subscribed observers about the new state. It notifies observers so by calling their provided
        callbacks on a copy of the latest game state.
        """
        # Update game tree
        self.__game_tree = GameTree(self.__state)

        # Notify all parties subscribed for game updates
        state_to_broadcast = self.__state.deepcopy()

        # Cycle over players and sync them
        for p in self.__players:
            p.sync(state_to_broadcast)

        # Cycle over game update callbacks and call each one
        # with a copy of the latest state
        for callback in self.__game_update_callbacks:
            try:
                callback(state_to_broadcast)
            except AssertionError as e:
                # Raise assertion exceptions are these are used for testing
                raise e
            except Exception as e:
                print(f'Exception occurred, removing observer: {e}')

    def __get_game_report(self) -> dict:
        """
        Retrieves the final game report. It encompasses a list of the cheating players' colors,
        a list of the failing players' colors and a list of dictionary objects sorted in decreasing
        order of score, each object containing the respective player's name, color and score.

        Here's an example of what the report may look like:

        {
            'cheating_players': [Color.BROWN],
            'failing_players': [Color.RED],
            'leaderboard': [
                {'name': 'Winner', 'color': Color.BLACK, 'score': 99},
                {'name': 'Runner-up', 'color': Color.WHITE, 'score': 40}
            ]

        }

        :return: resulting dict object
        """
        # Make up array to hold leaderboard
        leaderboard = []

        # Cycle over rule-abiding players and collect their name, color & score
        for p in self.__state.players:
            # Only add player to leaderboard if they were rule-abiding
            if p not in self.__failing_players and p not in self.__cheating_players:
                leaderboard.append({'name': p.name, 'color': p.color, 'score': p.score})

        # Sort leader board in decreasing order of score
        leaderboard.sort(key=operator.itemgetter('score'), reverse=True)

        # Return report
        return {
            'cheating_players': self.__cheating_players,
            'failing_players': self.__failing_players,
            'leaderboard': leaderboard
        }

    def __get_player_by_name(self, name: str) -> IPlayer:
        for p in self.__players:
            if p.name == name:
                return p

    def __fire_game_over(self) -> None:
        """
        Signals the game is over and dispatches the final game report to all subscribed
        observers.
        """
        # Retrieve report
        self.__report = self.__get_game_report()

        # Set flag
        self.__game_over = True

        # Determine highest score in the game
        max_score = max([p['score'] for p in self.__report['leaderboard']]) \
            if len(self.__report['leaderboard']) > 0 else 0

        # Determine names of winners
        winner_names = [p['name'] for p in self.__report['leaderboard'] if p['score'] == max_score]
        loser_names = [p['name'] for p in self.__report['leaderboard'] if p['score'] < max_score]

        # Determine winners with the highest scores by name
        self.__winners = [self.__get_player_by_name(name) for name in winner_names]
        # Determine losers by adding players with scores < highest_score, failing & cheating players
        self.__losers = [self.__get_player_by_name(name) for name in loser_names]

        self.__losers.extend(self.__report['failing_players'])
        self.__losers.extend(self.__report['cheating_players'])

        if Referee.DEBUG:
            print(f'Game over report: {self.__report}')

        # Give each player a copy of the report
        for player in self.__players:
            player.game_over(self.__report['leaderboard'], self.__report['cheating_players'],
                             self.__report['failing_players'])

        # Cycle over game update callbacks and call each observer with the report
        for callback in self.__game_over_callbacks:
            try:
                callback(self.__report)
            except AssertionError as e:
                # Raise assertion exceptions are these are used for testing
                raise e
            except Exception as e:
                # Callback has failed
                if Referee.DEBUG:
                    print(f'Game over callback has failed: {e}')

    def subscribe_game_updates(self, callback: 'Callable') -> None:
        """
        Subscribes caller for game state updates by way of a callable
        object that is called with a copy of the internal game state
        every time said game state changes. i.e. callback(state)

        :param callback: callback function call state on
        :return: None
        """
        # Validate params
        if not callable(callback):
            raise TypeError('Expected callable for callback!')

        # Add to list of callbacks
        self.__game_update_callbacks.append(callback)

    def subscribe_final_game_report(self, callback: 'Callable'):
        """
        Subscribes observers for the final game report by way of a callable
        object that is called with a copy of the final game report
        when the game ends. i.e. callback(report).

        :param callback: callback function call report on
        :return: None
        """
        # Validate params
        if not callable(callback):
            raise TypeError('Expected callable for callback!')

        # Add to list of callbacks
        self.__game_over_callbacks.append(callback)
