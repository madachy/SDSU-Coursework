'''
Constraint propagation
'''
from csp_lib.csp import CSP


def AC3(csp: CSP, queue: list = None, removals: list = None):
    """AC3 constraint propagation
    
    """
    if queue is None:
        queue = [(i, j) for i in csp.curr_domains for j in csp.neighbors[i]]

    def revise(i, j):
        revised = False
        for r in csp.curr_domains[i]:
            if not any([csp.constraints(i, r, j, y) for y in csp.curr_domains[j]]):
                csp.prune(i, r, removals)
                revised = True
        return revised

    while queue:
        i, j = queue.pop()  # Cell in Puzzle, Set Neighbors of Cell
        if revise(i, j):
            if csp.domains[i] is None:
                return False
            for x in csp.neighbors[i]:
                if (x, i) not in queue:
                    queue.append((x, i))
    return True

    # Hints:
    # Remember that:
    #    csp.variables is a list of variables
    #    cps.j[x] is the j of variable x
