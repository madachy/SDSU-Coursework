from hexagon import Hexagon
from hexgrid import HexagonList
from copy import deepcopy


class State(object):
    """Search State for Hexagon Weighted Lattice"""

    def __init__(self, hexagons: HexagonList, initialpath: list, head: Hexagon, cost: int):
        self.hexagonlist = hexagons
        self.head = head
        self.path = initialpath
        self.g = self.cost = cost
        self.depth = len(self.path)

    def statetuple(self):
        return tuple(self.path)

    def get_actions(self):
        """Returns List of Adjacent Hexagon objects to the Head Hexagon"""
        actions = list()
        for index in self.head.neighbors:
            hex_object = self.hexagonlist.hexagons[index]
            if hex_object.weight is not self.hexagonlist.blockedhex:
                actions.append(hex_object)
        return actions

    def actions(self):
        return self.actions()

    def move(self, hexagon: Hexagon):
        """Returns new state after moving to next Hexagon"""
        new_path = deepcopy(self.path)
        new_path.append(hexagon)
        return State(self.hexagonlist, new_path, hexagon, self.cost + hexagon.weight)

    def is_solved(self):
        return self.head.index is 8

    def solution(self):
        """Returns a tuple with the first element being the solution path and the second being the cost"""
        # Throw error if state is not a solution
        assert self.is_solved() is True
        return self.path[::-1], self.cost

    def goal_test(self):
        return self.is_solved()

    def h(self):
        """Returns Manhattan Distance to Goal"""
        distance = 0
        position = self.head.index
        # At Goal
        if position is 8:
            return 0
        # Traverse Upper Right Diagonal
        while position not in self.hexagonlist.right or position not in self.hexagonlist.top:
            position -= 7
            distance += 1
        if position is 8:
            return distance
        # If on top edge of lattice calculate distance to far right
        elif position in self.hexagonlist.top:
            distance += 8 - position
        # If on right edge of lattice calculate distance to top right
        elif position in self.hexagonlist.right:
            distance += position / 15
        return distance

    def g(self):
        return self.g

    def __eq__(self, other):
        return isinstance(other, State) and self.statetuple() is other.statetuple

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __hash__(self):
        return hash(self.statetuple())
