import sys

from color import Color
from game_tree import GameTree

sys.path.append('../Common')

from state import State
from exceptions.InvalidGameStatus import InvalidGameStatus
from game_status import GameStatus
from action import Action
from position import Position


class Strategy(object):
    """
    Purpose: This class is purported to provide a player with a strategy for placing avatars
             and one for determining the best move by looking ahead a number of turns. The latter
             is achieved through a min-max algorithm that maximizes the player's score for the
             worst possible moves (for the player) played by their opponent(s).

    Interpretation: The strategy is the logic employed by a player to determine their moves in an
                    attempt to win the game by collecting the largest number of fish.
    """

    @staticmethod
    def place_penguin(state: State) -> None:
        """
        This method places a penguin for the current player by scanning down columns
        starting in the top-left row until a free spot is found. If all columns on one
        row are exhausted and no spot has been found, the search is resumed on the next
        row from the first (left-most) column. Once a spot has been found, an avatar is
        placed in that location on behalf of the current player.

        :param state: current state of the game
        :return: None
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        # Make sure state is in placing phase
        if state.game_status != GameStatus.PLACING:
            raise InvalidGameStatus('Game status is not PLACING!')

        # Find a place to pitch avatar according to strategy by cycling over
        # rows and columns
        for row in range(state.board.rows):
            for col in range(state.board.cols):
                # Make up position from row and column
                pos = Position(row, col)
                # Pitch avatar if said position is open
                if state.is_position_open(pos):
                    state.place_avatar(pos)

    @staticmethod
    def get_best_action(state: State, depth: int) -> Action:
        """
        This method determines the best action for the current player by looking ahead depth
        number of turns and considering the most detrimental move an opponent can make in each
        of them. It then returns the action tied to the maximum score for the provided state's
        current player based on those worst case scenarios.

        :param state: state which to determine best move for current player for
        :param depth: how many turns to look ahead (must be > 0)
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State object for state!')

        if not isinstance(depth, int) or depth <= 0:
            raise TypeError('Expected integer >= 0 for depth!')

        # Make up game tree from state
        game_tree = GameTree(state)
        # Flesh game tree out (determine its subsequent states)
        game_tree.flesh_out()

        # Initialize variable to hold best action
        best_action = None
        # Initialize variable to hold maximum score
        max_score = 0

        # Calculate true depth (we want current player to play depth rounds)
        # depth = depth * state.players_no

        # Cycle over every possible action and resulting state in game tree
        for action, next_tree_node in game_tree.children.items():
            # Determine min-max score for current child state
            score = Strategy.__minmax(next_tree_node, state.current_player, depth, -1000, 1000)

            # If score is better than running max score, record both score and action
            if score > max_score:
                max_score = score
                best_action = action

        print(f'max score: {max_score}')
        # Return "best" action associated with the best score
        return best_action

    @staticmethod
    def __minmax(node: GameTree, player_id_to_max: int, depth: int, alpha: int, beta: int):
        """
        Implements min-max algorithm with alpha-beta pruning.
        """
        # Validate params
        if not isinstance(node, GameTree):
            raise TypeError('Expected GameTree for node!')

        if depth == 0:
            return node.state.get_player_score(player_id_to_max)

        node.flesh_out()

        # If current player is maximizer, maximize
        if node.state.current_player == player_id_to_max:
            # Cycle over all possibles moves and their associated states
            for action, child_node in node.children.items():
                score = Strategy.__minmax(child_node, player_id_to_max, depth - 1, alpha, beta)
                # maximize player_id_to_max's score
                if score > alpha:
                    # found a better move for ourselves
                    alpha = score
                if alpha >= beta:
                    # cut off
                    return alpha
                # player's best move
            return alpha
        else:
            # Minimize, otherwise
            for action, child_node in node.children.items():
                score = Strategy.__minmax(child_node, player_id_to_max, depth - 1, alpha, beta)
                # minimize player_id_to_max's score
                if score < beta:
                    # opponent found a better worse move (worse for us)
                    beta = score
                if alpha >= beta:
                    # cut off
                    return beta
            # opponent's best move
            return beta
