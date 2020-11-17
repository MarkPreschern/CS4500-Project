import sys


sys.path.append('../Common')

from state import State
from exceptions.OutOfTilesException import OutOfTilesException
from action import Action
from position import Position
from constants import VERY_LARGE_NUMBER
from game_tree import GameTree
from color import Color


class Strategy(object):
    """
    Purpose: This class is purported to provide a player with a strategy for placing avatars
             and one for determining the best move by looking ahead a number of turns. The former
             is achieved by sequentially scanning down each row from left to right starting with the
             first row at the top of the board. If no suitable placement is found on the first row the
             sequential scanning is repeated on the second row starting from the first (left-most) column.
             The latter strategy is achieved through a min-max algorithm that maximizes the player's score
             for the worst possible moves (for the player) played by their opponent(s).

    Interpretation: The strategy is the logic employed by a player to determine their moves in an
                    attempt to win the game by collecting the largest number of fish.
    """
    # Initialize DEBUG flag (if enabled debug information may be written to stdout)
    DEBUG = False

    @staticmethod
    def place_penguin(player_color: Color, state: State) -> Position:
        """
        This method places a penguin for the given player color by scanning down columns
        starting in the top-left row until a free spot is found. If all columns on one
        row are exhausted and no spot has been found, the search is resumed on the next
        row from the first (left-most) column. Once a spot has been found, an avatar is
        placed in that location on behalf of the current player.

        :param player_color: color of player to place penguin for
        :param state: current state of the game
        :return: returns position at which the penguin was placed
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State for state!')

        if not isinstance(player_color, Color):
            raise TypeError('Expected int for player_color!')

        # Find a place to pitch avatar according to strategy by cycling over
        # rows and columns
        for row in range(state.board.rows):
            for col in range(state.board.cols):
                # Make up position from row and column
                pos = Position(row, col)
                # Pitch avatar if said position is open
                if state.is_position_open(pos):
                    if Strategy.DEBUG:
                        print(f'[{player_color}] placed avatar at {pos}')
                    state.place_avatar(player_color, pos)
                    return pos

        raise OutOfTilesException()

    @staticmethod
    def get_best_action(state: State, depth: int) -> Action:
        """
        This method determines the best action for the current player by looking ahead at most
        depth number of current-player turns and considering the most detrimental move an opponent
        can make in each of them. It then returns the action tied to the maximum score for the provided
        state's current player based on those scenarios in which its opponents make the "worst" (most
        score minimizing) moves for the player.

        If there are multiple best action leading to the same score, then the one with the smallest
        source row, source column, destination row or destination column is picked (in that order). If the current
        player gets stuck during the tree traversal and the provided depth has not been reached, the traversal is
        aborted and the best running move is returned.

        :param state: state which to determine best move for current player for
        :param depth: how many the current player in the provided states gets to go at most
        :return: best Action current player can make best on mini-max strategy
        """
        # Validate parameters
        if not isinstance(state, State):
            raise TypeError('Expected State object for state!')

        if not isinstance(depth, int) or depth <= 0:
            raise TypeError('Expected integer >= 0 for depth!')

        # Make up a game tree for the state
        tree = GameTree(state)

        # Determine min-max score for current child state
        score, best_move = Strategy.__mini_max_search(tree, state.current_player, depth)

        if Strategy.DEBUG:
            print(f'  [depth={depth}] max score: {score} {best_move}')
            print(f'  Score [before action]: {state.get_player_by_color(state.current_player).score}')
        # Return "best" action associated with the best score
        return best_move

    @staticmethod
    def __mini_max_search(node: GameTree, player_color_to_max: Color, depth: int,
                          alpha: int = -VERY_LARGE_NUMBER, beta: int = VERY_LARGE_NUMBER):
        """
        Implements min-max algorithm with alpha-beta pruning. It computes the best worst
        score of the current player in the provided GameTree node by picking
        the best moves the player can make during their turn and the "best" worst moves its
        opponents can make during their turns that most minimize the player's score. It utilizes
        alpha-beta pruning to trim away edges of the tree (or player moves) that are known to
        yield a worse score than previously computed same-level branches. Two branches are at
        on same level if they descend from a common node.

        If there are multiple best moves leading to the same score, then the one with the smallest
        source row, source column, destination row or destination column is picked (in that order).
        If the maximizing player becomes stuck at any point in the tree traversal, the search is aborted and
        its current score is returned.

        :param node: game tree node for which to run
        :param player_color_to_max: color of player whose score to maximize (maximizer)
        :param depth: the number of times maximizing player is evaluated
        :param alpha: the best score of the maximizer
        :param beta: the best worst score of the minimizer (one of the player's opponents)
        :return: tuple of integer best score and corresponding best Action object.
        """
        # Validate params
        if not isinstance(node, GameTree):
            raise TypeError('Expected GameTree for node!')

        if not isinstance(player_color_to_max, Color):
            raise TypeError('Expected Color for player_color_to_max!')

        if not isinstance(depth, int) or depth < 0:
            raise TypeError('Expected integer >= 0 for depth!')

        if not isinstance(alpha, int):
            raise TypeError('Expected integer for alpha!')

        if not isinstance(beta, int):
            raise TypeError('Expected integer for beta!')

        # If we have reached our depth, maximizer is stuck or game is over, return player score
        if depth == 0 or (not node.state.can_anyone_move()) \
                or player_color_to_max in node.state.stuck_players:
            return node.state.get_player_score(player_color_to_max), None

        # If current player is maximizer, maximize
        if node.state.current_player == player_color_to_max:
            if Strategy.DEBUG:
                print(f'==== PLAYER {node.state.current_player} ========')
            # Initialize best value to something very negative
            best_val = -VERY_LARGE_NUMBER
            # Initialize best_move to anything (won't be compared to assuming we can always achieve
            # a positive score)
            best_move: Action = Action(Position(VERY_LARGE_NUMBER, VERY_LARGE_NUMBER),
                                       Position(VERY_LARGE_NUMBER, VERY_LARGE_NUMBER))
            # Cycle over all possibles moves and their associated states
            for move, child_node in node.get_next():
                # Get best score of subsequent node
                score, _ = Strategy.__mini_max_search(child_node, player_color_to_max, depth - 1, alpha, beta)

                # If our best move leads to the same score, pick the move with
                # the lowest src x, dst y, dst x, dst y (in that order)
                if score == best_val:
                    best_move = min(best_move, move)
                elif score > best_val:
                    # If it leads to a better score, update best val and best move
                    best_val = score
                    best_move = move

                # Determine if this beats our alpha, and if so set our alpha
                alpha = max(alpha, best_val)

                # If player's best beats opponents best worst move, cut off
                if alpha >= beta:
                    break

            # Return our best move
            return best_val, best_move
        else:
            if Strategy.DEBUG:
                print(f'==== PLAYER {node.state.current_player} ========')
            # Initialize opponent's best value to something very positive
            best_val = VERY_LARGE_NUMBER
            # Minimize, otherwise
            for move, child_node in node.get_next():
                # Get best score of subsequent node
                score, _ = Strategy.__mini_max_search(child_node, player_color_to_max, depth, alpha, beta)
                # Minimize player_id_to_max's score
                best_val = min(score, best_val)

                # See if we have come up with a better "worst" move
                beta = min(beta, best_val)

                # If player's best beats opponents best worst move, cut off
                if alpha >= beta:
                    break

            # Return opponent's best move
            return best_val, None
