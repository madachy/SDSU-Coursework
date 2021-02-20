"""
Driver for graph search problem
Created on Feb 12, 2018

@author: Tom Paulus
@author: William Fox
"""

import re
import time
from statistics import (mean, stdev)

from basicsearch_lib02.tileboard import TileBoard
from basicsearch_lib02.utilsdontneed import print_table
from npuzzle import NPuzzle
from problemsearch import graph_search
from searchstrategies import (BreadthFirst, DepthFirst, Manhattan)

TRIAL_SIZE = 31
TRIAL_BOARD_SIZE = 8
SOLUTION_METHODS = [BreadthFirst, DepthFirst, Manhattan]

# Output Configuration
DEBUG = False
INFO = True
VERBOSE = False


def tic():
    """Return current time representation"""
    return time.time()


def tock(t):
    """Return time elapsed in sec since t where t is the output of tic()"""
    return time.time() - t


def driver():
    length_of_plan = dict()
    number_of_nodes = dict()
    elapsed_time = dict()

    for method in SOLUTION_METHODS:
        length_of_plan[method] = list()
        number_of_nodes[method] = list()
        elapsed_time[method] = list()

    for i in range(TRIAL_SIZE):
        if INFO:
            print('Starting Trial #%d' % (i + 1))

        # Standard Config
        board_layout = TileBoard(TRIAL_BOARD_SIZE).state_tuple()

        # Random Board - For testing
        # board_layout = TileBoard(TRIAL_BOARD_SIZE, force_state=[8, None, 6, 5, 4, 7, 2, 3, 1]).state_tuple()
        # board_layout = TileBoard(TRIAL_BOARD_SIZE, force_state=[7, 3, None, 5, 1, 2, 4, 8, 6]).state_tuple()

        # Solvable in 1 move
        # board_layout = TileBoard(TRIAL_BOARD_SIZE, force_state=[1, None, 3, 4, 2, 5, 6, 7, 8]).state_tuple()

        # Solvable in ~5 moves
        # board_layout = TileBoard(TRIAL_BOARD_SIZE, force_state=[4, 1, 2, None, 5, 3, 6, 7, 8]).state_tuple()
        # board_layout = TileBoard(TRIAL_BOARD_SIZE, force_state=[1, None, 3, 7, 2, 5, 4, 6, 8]).state_tuple()

        # Solvable in ~15 moves
        # board_layout = TileBoard(TRIAL_BOARD_SIZE, force_state=[5, 3, 7, None, 1, 2, 4, 6, 8]).state_tuple()

        for method in SOLUTION_METHODS:
            if INFO:
                print('Solving puzzle via %s' % method.__name__)

            puzzle = NPuzzle(TRIAL_BOARD_SIZE, g=method.g, h=method.h, force_state=board_layout)

            start_time = tic()
            path, nodes_explored = graph_search(puzzle, debug=DEBUG, verbose=VERBOSE)
            duration = tock(start_time)
            assert path is not None

            length_of_plan[method].append(len(path))
            number_of_nodes[method].append(nodes_explored)
            elapsed_time[method].append(duration)

            if INFO:
                print('Solved puzzle via %s in %d seconds' % (method.__name__, duration))

        print('Finished Trial #%d' % (i + 1))

    if INFO or DEBUG or VERBOSE:
        print("\n\n==================================================\n\n\n")

    header = ["Method / Result   ",
              "Length of Plan (Mean/STDEV)",
              "Number of Nodes (Mean/STDEV)",
              "Elapsed Time (Mean/STDEV)"]
    rows = list()

    # Header Separator
    rows.append(['-' * (len(header[i]) + 1) for i in range(len(header))])

    # Table Values
    for method in SOLUTION_METHODS:
        rows.append([' '.join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', method.__name__).split()),
                     '{:.3f} / {:.3f}'.format(mean(length_of_plan[method]), stdev(length_of_plan[method])),
                     '{:.3f} / {:.3f}'.format(mean(number_of_nodes[method]), stdev(number_of_nodes[method])),
                     '{:.3f} / {:.3f}'.format(mean(elapsed_time[method]), stdev(elapsed_time[method]))])

    print_table(rows, header=header, sep="\t| ")


if __name__ == '__main__':
    driver()
