"""
Created on Feb 12, 2018

@author: Tom Paulus
@author: William Fox
"""
from collections import deque

from basicsearch_lib02.queues import PriorityQueue
from basicsearch_lib02.searchrep import (Node, Problem)
from explored import Explored


def graph_search(problem: Problem, verbose=False, debug=False):
    """graph_search(problem, verbose, debug) - Given a problem representation
    (instance of basicsearch_lib02.representation.Problem or derived class),
    attempt to solve the problem.
    
    If debug is True, debugging information will be displayed.
    
    if verbose is True, the following information will be displayed:
        
        Number of moves to solution
        List of moves and resulting puzzle states
        Example:
        
            Solution in 25 moves        
            Initial state
                  0        1        2    
            0     4        8        7    
            1     5        .        2    
            2     3        6        1    
            Move 1 -  [0, -1]
                  0        1        2    
            0     4        8        7    
            1     .        5        2    
            2     3        6        1    
            Move 2 -  [1, 0]
                  0        1        2    
            0     4        8        7    
            1     3        5        2    
            2     .        6        1    
            
            ... more moves ...
            
                  0        1        2    
            0     1        3        5    
            1     4        2        .    
            2     6        7        8    
            Move 22 -  [-1, 0]
                  0        1        2    
            0     1        3        .    
            1     4        2        5    
            2     6        7        8    
            Move 23 -  [0, -1]
                  0        1        2    
            0     1        .        3    
            1     4        2        5    
            2     6        7        8    
            Move 24 -  [1, 0]
                  0        1        2    
            0     1        2        3    
            1     4        .        5    
            2     6        7        8    
        
        If no solution were found (not possible with the puzzles we
        are using), we would display:
        
            No solution found
    
    Returns a tuple (path, nodes_explored) where:
    path - list of actions to solve the problem or None if no solution was found
    nodes_explored - Number of nodes explored (dequeued from frontier)
    """

    frontier = PriorityQueue()
    frontier.append(Node(problem, problem.initial))
    node = frontier.pop()
    right_pop = True
    if node.expand(node.problem)[0].g < 0:
        # DFS
        frontier = deque()
        frontier.append(Node(problem, problem.initial))
    elif node.expand(node.problem)[0].h < 2:
        # BFS
        right_pop = False
        frontier = deque()
        frontier.append(Node(problem, problem.initial))
    else:
        # Manhattan
        frontier.append(node)
    frontier_hash = Explored()
    frontier_hash.add(problem.initial.state_tuple())
    done = False
    nodes_explored = 0
    explored = Explored()
    while not done:
        if right_pop:
            node = frontier.pop()  # Manhattan and DFS
        else:
            node = frontier.popleft()  # BFS

        if debug:
            print("Popped Node:", str(node))

        explored.add(node.state.state_tuple())
        nodes_explored += 1

        if node.state.solved():
            if debug:
                print("A solution has been found!")
            solution_path = node.path()
            done = True
            if verbose:
                print_solution(solution_path)
            return solution_path, nodes_explored
        else:
            for child in node.expand(node.problem):
                # Add new children to frontier
                if not explored.exists(child.state.state_tuple()) and not frontier_hash.exists(
                        child.state.state_tuple()):
                    frontier.append(child)
                    frontier_hash.add(child)
                elif debug:
                    print("Skipping Node - not novel", child)
                    pass
            done = len(frontier) == 0
        if debug:
            print("")
    if verbose:
        print("No solution found")
    return None, nodes_explored


def print_solution(path: tuple):
    print("Solution in %d moves" % (len(path) - 1))
    print("Initial State")
    print(path[0])

    for i in range(1, len(path)):
        print("Move %d - %s" % (i, path[i].action))
        print(path[i].state)
        print("")
