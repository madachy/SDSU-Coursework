"""
ai - search & strategy module

implement a concrete Strategy class and AlphaBetaSearch
"""
import sys
import random

import abstractstrategy
from checkerboard import *


class Strategy(abstractstrategy.Strategy):

    def play(self, board: CheckerBoard) -> (CheckerBoard, tuple):
        actions = board.get_actions(self.maxplayer)
        if len(actions) is 0:
            return board, None
        action = actions[random.randint(0, len(actions) - 1)]
        return board.move(action), action

    def utility(self, board: CheckerBoard) -> int:
        pass
