"""
searchstrategies

Module to provide implementations of g and h for various search strategies.
In each case, the functions are class methods as we don't need an instance
of the class.  

If you are unfamiliar with Python class methods, Python uses a function
decorator (indicated by an @ to indicate that the next method is a class
method).  Example:

class SomeClass:
    @classmethod
    def foobar(cls, arg1, arg2):
        "foobar(arg1, arg2) - does ..."
        
        code... class variables are accessed as cls.var (if needed)
        return computed value

A caller would import SomeClass and then call, e.g. :  
    SomeClass.foobar("hola","amigos")

Contains g and h functions for:
BreadFirst - breadth first search
DepthFirst - depth first search
Manhattan - city block heuristic search.  To restrict the complexity of
    this, you only need handle heuristics for puzzles of an odd length
    with solutions that contain the blank in the middle and numbers going
    from left to right in each row, e.g.:
        123
        4 5
        678
    When multiple solutions are allowed, the heuristic becomes a little more
    complex as the city block distance must be estimated to each possible solution
    state.

@author: Tom Paulus
@author: William Fox
"""

# For each of the following classes, create classmethods g and h
# with the following signatures
#       @classmethod
#       def g(cls, parentnode, action, childnode):
#               return appropriate g value
#       @classmethod
#        def h(cls, state):
#               return appropriate h value
from basicsearch_lib02.searchrep import Node
from basicsearch_lib02.tileboard import TileBoard


class BreadthFirst:
    """BredthFirst - breadthfirst search"""

    k = 0

    @classmethod
    def g(cls, parentnode: Node, action, childnode: Node):
        # Return Depth
        return len(childnode.path())

    @classmethod
    def h(cls, state):
        # Return Constant K (eg 0)
        return cls.k


class DepthFirst:
    """"DepthFirst - depth first search"""

    @classmethod
    def g(cls, parentnode: Node, action, childnode: Node):
        return (parentnode.depth + 1) * -1

    @classmethod
    def h(cls, state: TileBoard):
        return 0


class Manhattan:
    """"Manhattan Block Distance heuristic"""

    @classmethod
    def g(cls, parentnode, action, childnode: Node):
        return childnode.depth * 2

    @classmethod
    def h(cls, state: TileBoard):
        manhattan_sum = 0

        # Populates Solved State
        solved = [[None for c in range(state.cols)] for r in range(state.rows)]
        index = 1
        for row in range(state.boardsize):
            for col in range(state.boardsize):
                if row == state.rows // 2 and col == state.cols // 2:
                    solved[row][col] = None
                else:
                    solved[row][col] = index
                    index += 1

        # Calculate Displacements
        for row in range(state.boardsize):
            for col in range(state.boardsize):
                item = state.get(row, col)
                # Find location for solved state
                for solved_row in range(len(solved)):
                    if item in solved[solved_row]:
                        # Adds manhattan distance to manhattan_sum
                        # If item is at [1, 2] in state and [0, 0] in solved then distance is 1 + 2 = 3
                        manhattan_sum += abs(solved_row - row) + abs(solved[solved_row].index(item) - col)
        return manhattan_sum
