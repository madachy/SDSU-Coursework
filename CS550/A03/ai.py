"""
ai - search & strategy module

implement a concrete Strategy class and AlphaBetaSearch
"""
import math
import abstractstrategy
from checkerboard import *


class Strategy(abstractstrategy.Strategy):
    __utility_weights = [100, 10, 1]  # Pieces, Kings, Board Position

    def play(self, board: CheckerBoard) -> (CheckerBoard, tuple):
        search = AlphaBetaSearch(self, self.maxplayer, self.minplayer, self.maxplies)
        action = search.alphabeta(board)
        # Forfeit
        if action is None:
            return board, None
        return board.move(action), action

    def utility(self, board: CheckerBoard) -> int:
        player_pieces = 0
        player_kings = 0
        player_pos_sum = 0

        opponent_pieces = 0
        opponent_kings = 0
        opponent_pos_sum = 0

        for (_r, _c, piece) in board:
            # Find player index and piece type
            (playerId, kingP) = board.identifypiece(piece)
            if playerId == board.playeridx(self.maxplayer):
                # This Player
                player_pieces += 1
                if kingP:
                    player_kings += 1
                player_pos_sum += self.__evaluate_position(board, self.maxplayer, _r, _c)

            else:
                # Opponent
                opponent_pieces += 1
                if kingP:
                    opponent_kings += 1
                opponent_pos_sum += self.__evaluate_position(board, self.minplayer, _r, _c)

        player_features = [player_pieces, player_kings, player_pos_sum]
        player_score = sum(feature * weight for (feature, weight) in zip(player_features, self.__utility_weights))

        opponent_features = [opponent_pieces, opponent_kings, opponent_pos_sum]
        opponent_score = sum(feature * weight for (feature, weight) in zip(opponent_features, self.__utility_weights))

        # print("Utility Calculation - R: {}  B: {}".format(player_score, opponent_score))

        return player_score - opponent_score

    @staticmethod
    def __evaluate_position(board: CheckerBoard, player, x, y) -> int:
        edge_size = board.edgesize - 1
        is_edge = (x == 0 or x == edge_size or y == 0 or y == edge_size)

        return (5 if is_edge else 3) + board.disttoking(player, y)


class AlphaBetaSearch:
    """AlphaBetaSearch
    Conduct alpha beta searches from a given state.

    Example usage:
    # Given an instance of a class derived from AbstractStrategy, set up class
    # to determine next move, maximizing utility with respect to red player
    # and minimiizing with respect to black player. Search 3 plies.
    search = AlphaBetaSearch(strategy, 'r', 'b', 3)

    # To find the move, run the alphabeta method
    best_move = search.alphabeta(some_checker_board)
    """

    def __init__(self, strategy: Strategy, maxplayer, minplayer, maxplies=3,
                 verbose=False):
        """"AlphaBetaSearch - Initialize a class capable of alphabeta search
        strategy - implementation of AbstractStrategy class
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the utility function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.__strategy = strategy
        self.__maxplayer = maxplayer
        self.__minplayer = minplayer
        self.__maxplies = maxplies
        self.__verbose = verbose


    def alphabeta(self, state: CheckerBoard) -> tuple:
        """alphbeta(state) - Run an alphabeta search from the current
       state. Returns best action.
       """
        return self.max_value(state, -1 * math.inf, math.inf, 0)[1]

    def max_value(self, state: CheckerBoard, alpha: int, beta: int, depth: int) -> (int, tuple):
        # Negative Infinity
        value = -1 * math.inf
        best_option = None

        if state.is_terminal()[0] or depth > self.__maxplies:
            value = self.__strategy.utility(state)
        else:
            for action in state.get_actions(self.__maxplayer):
                minv, _ = self.min_value(state.move(action), alpha, beta, depth + 1)
                if minv > value:
                    # New Better Option
                    value = minv
                    best_option = action
                if value >= beta:
                    # Prune
                    break
                else:
                    alpha = max(alpha, value)

        return value, best_option

    def min_value(self, state: CheckerBoard, alpha: int, beta: int, depth: int) -> (int, tuple):
        # Infinity
        value = math.inf
        worst_option = None

        if state.is_terminal()[0] or depth > self.__maxplies:
            value = self.__strategy.utility(state)
        else:
            for action in state.get_actions(self.__minplayer):
                maxv, _ = self.max_value(state.move(action), alpha, beta, depth + 1)
                if maxv < value:
                    # New Worst Option
                    value = maxv
                    worst_option = action
                if value <= alpha:
                    # Prune
                    break
                else:
                    beta = min(beta, value)
        return value, worst_option
