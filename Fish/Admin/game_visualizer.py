import sys
from tkinter import Tk, Frame
import time

from player_interface import IPlayer
from referee import Referee
from state import State
from constants import DEFAULT_BOARD_ROWS, DEFAULT_BOARD_COLS, MIN_PLAYERS, MAX_PLAYERS


class GameVisualizer(object):
    """
    PURPOSE:        The purpose of this class is to visualize the run through of an entire Fish game. The set of players
                    is assumed to be in order of increasing age and may consist of any player implementing IPlayer.

    INTERPRETATION: A game visualization creates a window and frame for the graphical interpretation to be
                    displayed on. The visualization is updated every every 'RENDER_TIMEOUT' seconds after a player
                    makes a move. At the end of the visualization, the graphical user interface is removed.

                    A game visualization takes in a list of players, a number of rows, and a number of columns. A
                    referee is created with the program arguments to facilitate the game being played. An
                    '__update_gameboard' callback method is subscribed to the referee's game updates to render an update
                    visually whenever the game board is modified in the game. Once the Referee's game is started,
                    the visual state is updated according to the placements, actions, and resulting referee decisions
                    via the aforementioned callback.

                    The game visualization ends when the game being facilitated by the referee ends. Upon the game's
                    completion (when referee.run() completes), the graphical user interface is removed.

    DEFINITION(s):  A game is represented by a Referee object overseeing that game's players.
                    A window is a TK instance which can hold frames and images
                    A frame is a container in which images can be placed and displayed
    """

    def __init__(self, players: [IPlayer], board_row_no: int = DEFAULT_BOARD_ROWS, board_col_no: int = DEFAULT_BOARD_COLS, render_timeout: int = 1, num_fish: int = None):
        """
        Initializes the game visualizer with the list of IPlayer objects, board rows, and board columns.
        
        :param players: list of IPlayer
        :param board_row_no: number of rows to game board used in the tournament
        :param board_col_no: number of cols to game board used in the tournament
        :param render_timeout: the number of seconds to wait before re-rendering game after a change
        :param num_fish: the number of fish per tile
        :return: None
        """
        # Validate params
        if not isinstance(players, list):
            raise TypeError('Expected list of IPlayer for players!')

        if not isinstance(board_row_no, int):
            raise TypeError('Expected int for board_row_no')

        if not isinstance(board_col_no, int):
            raise TypeError('Expected int for board_col_no')

        if not isinstance(render_timeout, int):
            raise TypeError('Expected int for render_timeout')

        # Make sure we weren't given too many players
        if len(players) < MIN_PLAYERS or len(players) > MAX_PLAYERS:
            raise ValueError(f'Invalid player length; length has to be between {MIN_PLAYERS} and'
                             f' {MAX_PLAYERS}')

        self.__players = players

        self.__board_row_no = board_row_no
        self.__board_col_no = board_col_no
        self.__render_timeout = render_timeout
        self.__num_fish = num_fish

        # Creates frame for visualization
        self.__window, self.__frame = self.__setup_gui()

    def __setup_gui(self) -> [Tk, Frame]:
        """
        Creates a window and frame for the graphical interpretation to be displayed on. The window is an instance of TK
        and holds a frame which is a container for the rendered game state.

        :return: returns the window and frame created to display the game state
        """

        # Make up window
        window = Tk()
        window.wm_title('Fish Game')

        # Make up frame within window
        frame = Frame(window, width=505, height=400)
        # Set window to use gridview
        frame.grid(row=0, column=0)

        return window, frame

    def run(self):
        """
        Runs the game visualization, effectively playing through an entire game and visually displaying the game state
        every time it is updated in the game. A referee is created to facilitate the game being played and an
        __update_gameboard function is used as a callback to update the GUI every time the game state is updated by
        the referee. Upon completion of the game, the GUI's window is destroyed, effectively removing it.

        :return: None
        """

        # creates referee
        referee: Referee = Referee(self.__board_row_no, self.__board_col_no, self.__players, self.__num_fish)

        # Displays initial game board
        referee.state.render(self.__frame)
        self.__window.update()

        # subscribe referee game updates to update the game board in real time
        referee.subscribe_game_updates(self.__update_gameboard)

        # subscribe to game outcome from referee (for testing)
        referee.subscribe_final_game_report(self.__handle_final_game_report)

        # start game
        referee.start()

        # Destroys the GUI window effectively removing it
        self.__window.destroy()

        # return final game results
        return self.final_game_report

    def __update_gameboard(self, state: State):
        """
        Updates the graphical user interface by rendering the updated state onto the frame. The update occurs
        'RENDER_TIMEOUT' seconds after being called to give the user time to visually process the change.

        :param state: the updated game state to display on the GUI
        :return: None
        """

        # wait RENDER_TIMEOUT to display update
        time.sleep(self.__render_timeout)

        # update frame and window with the new state
        state.render(self.__frame)
        
        self.__window.update()

    
    def __handle_final_game_report(self, game_report):
        self.final_game_report = game_report
