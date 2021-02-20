from backtrack import backtracking_search
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv, mac, forward_checking, lcv
from csp_lib.sudoku import (Sudoku, easy1, harder1)


def is_solved(sudoku: Sudoku):
    for var in sudoku.curr_domains:
        if len(sudoku.curr_domains[var]) is not 1:
            return False
    return True


if __name__ == "__main__":
    for puzzle in [easy1, harder1]:
        # for puzzle in [easy1]:
        s = Sudoku(puzzle)  # construct a Sudoku problem
        print("New Sudoku Puzzle")
        s.display(s.infer_assignment())
        AC3(s)
        if is_solved(s):
            print("Solved via AC3")
            s.display(s.infer_assignment())
        else:
            print("Could not solve via AC3: Current Puzzle")
            s.display(s.infer_assignment())
            print("Trying to solve via Back Track")
            backtracking_search(s, inference=forward_checking, order_domain_values=lcv, select_unassigned_variable=mrv)
            if is_solved(s):
                print("Solved via Back Track")
                s.display(s.infer_assignment())
            else:
                print("Puzzle could not be solved: Current State")
                s.display(s.infer_assignment())
