import operator
import sys
from random import randrange


sys.path.append('../Common/')
sys.path.append('../')
sys.path.append('../Admin/Other/')

from player import Player
import constants as ct
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
                    Similarly, in the version of the game involving remote communication, a player that takes takes more
                    than ten seconds to respond to the referee with either action or placement is marked out as failing.

                    The referee will remove the cheating and failing players' avatars from the game and prevent them
                    from taking any more turns (that includes placing and moving).

    INTERPRETATION: The referee could best be described as the engine that runs a game of Fish. It receives
                    a list of Player objects that is sorted by age and a row and column dimensions of the board from
                    the tournament manager, sets up a game board (based on the dimensions received) and assigns each
                    player a color. It then prompts each player for a placement by having them return a Position
                    object containing the row and column number they wish to place their avatar. After it finishes
                    prompting users for placements, it prompts each movable player for an Action object (made up
                    of a Position describing the place on the board the move is made from and another describing the
                    place the move is made to).

                    To setup the game board, the referee applies a "difficulty factor" - a Natural number that speaks to
                    the maximum number of Tiles the referee will try to remove. This factor is adjustable and can be
                    leveraged to make a game more challenging or less so. The referee will randomly pick the tiles to
                    remove and may even end up removing 0 tiles for a difficulty factor D > 0.

                    It also provides functionality that external observers can employ to follow the game. An
                    observer or tournament manager subscribe via `subscribe_game_updates` to receive an update with
                    the latest game state every time it changes (this happens whenever a player makes a placement or
                    move, or is kicked). They can also subscribe to an end game report via `subscribe_final_game_report`
                    to receive a copy of the final game report.

                    The final game report encompasses a list of the cheating players' colors, a list of the failing
                    players' colors and a list of dictionary objects sorted in decreasing order of score,
                    each object containing a rule-abiding player's name, color and score.

                    Here's an example of what the report may look like:

                    {
                        'cheating_players': [Color.BROWN],
                        'failing_players': [Color.RED],
                        'leaderboard': [
                            {'name': 'Winner', 'color': Color.BLACK, 'score': 99},
                            {'name': 'Runner-up', 'color': Color.WHITE, 'score': 40}
                        ]

                    }

                    Upon determining that no more moves can be made, the referee ends the game and provides all players
                    and subscribed observers with the final game report.

                    At initialization, the referee is given a list of Player objects with undefined colors (.color =
                    Color.UNDEFINED). After assigning colors, the referee creates a PlayerEntity for each object,
                    which contains the essential information needed for identification in the game (namely name,
                    color and placements). All other information pertaining to a player is scrapped. The referee
                    starts running the game (from the placement phase onwards) when start() is called.

                    Throughout the game, every time the internal game state is altered, the game tree is updated,
                    players are synchronized (by calling sync on them with the game state) and observers are notified
                    with a version of the latest one. This keeps all parties informed and the game tree up to date for
                    rule-checking.
    """
    DEBUG = False

    # Initialize difficulty factor
    DIFFICULTY_FACTOR = 2

    def __init__(self, rows: int, cols: int, players: [Player]) -> None:
        """
        Initializes a referee for a game with a board of size row x col and a given (ordered) list of Player
        objects.

        :param rows: row dimension of the board
        :param cols: column dimension of the board
        :param players: list of Player objects sorted in increasing order of age
        :return: None
        """
        # Validate params
        if not isinstance(rows, int) or rows <= 0:
            raise TypeError('Expected positive int for rows!')

        if not isinstance(cols, int) or cols <= 0:
            raise TypeError('Expected positive int for cols!')

        if not isinstance(players, list):
            raise TypeError('Expected list for players!')

        # Make sure list consists of only player objects
        if not all(isinstance(x, Player) for x in players):
            raise TypeError('All player list objects have to of type Player!')

        # Make sure we weren't given too many players
        if len(players) < ct.MIN_PLAYERS or len(players) > ct.MAX_PLAYERS:
            raise ValueError(f'Invalid player length; length has to be between {ct.MIN_PLAYERS} and'
                             f' {ct.MAX_PLAYERS}')

        # Make sure dimensions are large enough to accommodate all players
        if cols * rows < len(players):
            raise ValueError('Board dimensions are too small to accomodate all players!')

        # Assign each player the color that correspond to their position in the player list
        for k in range(len(players)):
            players[k].color = Color(k)

        # Set properties
        self.__players: [Player] = players
        self.__avatars_per_player = 6 - len(players)

        # Make up list of Color holding the colors of failing players
        self.__failing_players = []
        # Make up list of Color holding the colors of cheating players
        self.__cheating_players = []

        # Initialize game update callbacks as a list of callable items called every time
        # the state of the game changes
        self.__game_update_callbacks = []

        # Initializes game over callbacks as a list of callable items called at the end
        # of the game together with the game report
        self.__game_over_callbacks = []

        # Make up a board
        self.__board = self.__make_board(cols, rows)

        # Make up state from board & list of PlayerEntity objects
        self.__state = State(self.__board, [PlayerEntity(p.name, p.color) for p in players])
        # Initialize game tree placeholder
        self.__game_tree = None

        # Make up flag to indicate whether the game has started
        self.__started = False

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
    def players(self) -> [Player]:
        """
        Returns (copy) collection of players referee oversees.
        """
        return pickle.loads(pickle.dumps(self.__players))

    @property
    def cheating_players(self) -> [Color]:
        """
        Returns collection of Color objects corresponding to cheating
        players.

        :return: resulting list of Color
        """
        return self.__cheating_players

    @property
    def failing_players(self) -> [Color]:
        """
        Returns collection of Color objects corresponding to failing
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

    def __make_board(self, cols, rows) -> Board:
        """
        Makes a board with the given dimensions. It also applies a difficulty factor to
        the board by removing at most DIFFICULTY_FACTOR tiles. What and how many tiles
        is something determined randomly.

        :param cols: number of columns for the board
        :param rows: number of rows for the board
        :return: resulting Board object
        """
        # Make up board
        board = Board.homogeneous(randrange(ct.MIN_FISH_PER_TILE, ct.MAX_FISH_PER_TILE), rows, cols)
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
                if p.color in self.__failing_players or p.color in self.__cheating_players:
                    avatars_to_place -= 1
                    continue

                # Get placement for player
                placement = p.get_placement(self.__state.deepcopy())

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

                if Referee.DEBUG:
                    print(f'got placement of {placement} from player {p.color}')

                self.__fire_game_state_changed()
                # Decrement avatars needed to be placed
                avatars_to_place -= 1

        # Check if any players remain after placement (everyone might have gotten kicked)
        return self.__state.players_no != 0

    def __kick_player(self, player_obj: Player, reason: PlayerKickReason):
        """
        Kicks provided Player from the game.

        :param player_obj: Player object to kick
        :param reason: reason (str) they're being kicked
        """
        # Validate params
        if not isinstance(player_obj, Player):
            raise TypeError('Expected Player object for player_obj!')

        if not isinstance(reason, PlayerKickReason):
            raise TypeError('Expected PlayerKickReason for reason!')

        if Referee.DEBUG:
            print(f'Kicking {player_obj.color} for reason {reason}')

        if reason == PlayerKickReason.CHEATING:
            self.__cheating_players.append(player_obj.color)
        else:
            self.__failing_players.append(player_obj.color)

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
            current_player_obj = self.__get_player_by_color(self.__state.current_player)

            try:
                # Get action from player
                action: Action = current_player_obj.get_action(self.__state)

                if not isinstance(action, Action):
                    # If anything but an Action object was returned Player failed
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

    def __get_player_by_color(self, color: Color) -> Player:
        """
        Retrieves Player object with provided color.

        :param color: Color of player to retrieve
        :return: associated Player object
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
            if p.color not in self.__failing_players and p.color not in self.__cheating_players:
                leaderboard.append({'name': p.name, 'color': p.color, 'score': p.score})

        # Sort leader board in decreasing order of score
        leaderboard.sort(key=operator.itemgetter('score'), reverse=True)

        # Return report
        return {
            'cheating_players': self.__cheating_players,
            'failing_players': self.__failing_players,
            'leaderboard': leaderboard
        }

    def __fire_game_over(self) -> None:
        """
        Signals the game is over and dispatches the final game report to all subscribed
        observers.
        """
        # Retrieve report
        report = self.__get_game_report()

        if Referee.DEBUG:
            print(f'Game over report: {report}')

        # Give each player a copy of the report
        for player in self.__players:
            player.game_over(report['leaderboard'], report['cheating_players'], report['failing_players'])

        # Cycle over game update callbacks and call each observer with the report
        for callback in self.__game_over_callbacks:
            try:
                callback(report)
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
