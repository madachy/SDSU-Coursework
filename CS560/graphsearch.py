from state import State
import bisect


def graph_search(initial: State, debug=False):
    frontier = PriorityQueue()
    frontier.append(initial)
    # Hash Table that Mirrors PQ for faster lookups
    frontier_hash = dict()
    frontier_hash[initial] = True
    done = False
    explored = dict()

    while not done:
        # Lol @ typing in Python
        node: State = frontier.pop()
        explored[node] = True

        if node.is_solved():
            if debug:
                print("Found a Solution")
            solution_path, solution_cost = node.solution()
            done = True
            if debug:
                print("Costing: {}, Path: {}".format(solution_cost, solution_path))
            return solution_path, solution_cost
        else:
            for child in node.get_actions():
                # Avoid Cycles
                if child in node.path:
                    continue
                # Need to create a new state to check first
                child_state = node.move(child)
                # Add new children state to frontier
                if child_state not in explored and child_state not in frontier_hash:
                    frontier.append(child_state)
                    frontier_hash[child_state] = True
                elif debug:
                    # Todo: Add __repr__ for state if not working
                    pass
            done = len(frontier) == 0
    if debug:
        print("No solution found, check https://www.youtube.com/watch?v=_asNhzXq72w")
    return None


class PriorityQueue:
    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order=min, f=lambda x: x):
        self.A = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))

    def __len__(self):
        return len(self.A)

    def pop(self):
        if self.order == min:
            return self.A.pop(0)[1]
        else:
            return self.A.pop()[1]

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)
