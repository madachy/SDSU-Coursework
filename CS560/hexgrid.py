from hexagon import Hexagon


class HexagonList(object):
    """List Representation of Weighted Rectangle 16x8 Hexagonal Lattice """

    top = [x for x in range(1, 9)]
    right = [x for x in range(8, 234, 15)]
    left = [x for x in range(1, 227, 15)]
    bottom = [x for x in range(226, 234)]

    def __init__(self, weights: list, blockedhex=-1):
        self.blockedhex = blockedhex
        self.hexagons = [None]
        index = 0
        # Remove Leading None
        weights.pop(0)
        while weights:
            index += 1
            self.hexagons.append(Hexagon(index, weights.pop(0)))
        self.__cleanNeighbors__()

    def __cleanNeighbors__(self):
        """Removes any wrap arounds left from initial neighbor list in Hexagon constructor"""
        for hexagon in self.left:
            self.hexagons[hexagon].neighbors = list(set(self.hexagons[hexagon].neighbors) - set(self.right))
        for hexagon in self.right:
            self.hexagons[hexagon].neighbors = list(set(self.hexagons[hexagon].neighbors) - set(self.left))
