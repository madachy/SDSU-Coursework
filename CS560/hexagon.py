class Hexagon(object):
    offsets = [-15, -8, -7, 7, 8, 15]

    def __init__(self, index: int, weight: int):
        self.index = index
        self.weight = weight
        self.neighbors = list()
        for offset in self.offsets:
            if index + offset < 1 or index + offset > 233:
                continue
            self.neighbors.append(index + offset)

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)

    def __repr__(self):
        return str(self.index)
