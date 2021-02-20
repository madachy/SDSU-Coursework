'''
Created on Feb 22, 2015

@author: mroch
'''

import time

# human - human player, prompts for input
import human
import ai
from checkerboard import *
import imp
import sys
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)

# If the tonto import fails remember that the compiled file is ignored by git


# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.5 and 3.6 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.


def elapsed(earlier, later):
    """elapsed - Convert elapsed time.time objects to duration string
    
    Useful for tracking move and game time.  Example pseudocode:
    
    gamestart = time.time()
    
    while game not over:
        movestart = time.time()
        ...  logic ...
        current = time.time() 
        print("Move time: {} Game time: {}".format(
            elapsed(movestart, current), elapsed(gamestart, current))
    
    
    """
    return time.strftime('%H:%M:%S', time.gmtime(later - earlier))


def Game(red=human.Strategy, black=ai.Strategy,
         maxplies=8, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """

    # Don't forget to create instances of your strategy,
    # e.g. black('b', checkerboard.CheckerBoard, maxplies)

    red_strategy = red('r', CheckerBoard, maxplies)
    black_strategy = black('b', CheckerBoard, maxplies)

    turn = firstmove
    board = CheckerBoard() if init is None else init
    winner = None
    while not board.is_terminal()[0]:
        if turn is 0:
            if verbose:
                print("Red Player's Turn")
                print("Calculated Utility: {}".format(red_strategy.utility(board)))

            board, action = red_strategy.play(board)
            if action is None:
                if verbose:
                    print("Red Player has Forfeited")
                winner = 'b'
                # Forfeit
                break
        else:
            if verbose:
                print("Black Player's Turn")
                print("Calculated Utility: {}".format(black_strategy.utility(board)))
            board, action = black_strategy.play(board)
            if action is None:
                if verbose:
                    print("Black Player has Forfeited")
                winner = 'r'
                # Forfeit
                break

        turn = (turn + 1) % 2
        if turn % 2 == 0:
            if verbose:
                print("End of Cycle")
                print(board)
                print("\n\n")

    if board.is_terminal()[0]:
        winner = board.is_terminal()[1]
        if winner is None:
            print("Game Over! It was a draw")
        else:
            print("Game Over! - {} wins".format(winner))
    else:
        print("The other player Forfeit - {} wins!".format(winner))


if __name__ == "__main__":
    Game()
