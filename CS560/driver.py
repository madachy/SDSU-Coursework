from graphsearch import graph_search
from hexgrid import HexagonList
from state import State


def driver(verbose=False):
    # Pad with leading None to account for 1 indexing of Hexagons
    input_text = [None, ]
    with open("INPUT.txt") as file:
        file_contents = file.readlines()
    file_contents = [line.strip() for line in file_contents]
    file_contents = filter(None, file_contents)
    for line in file_contents:
        line = line.split()
        input_text.append(int(line[1]))
    if verbose:
        print(input_text)
    hex_list = HexagonList(input_text, blockedhex=999)
    # Starting Position
    initial_hex = hex_list.hexagons[226]
    initial_state = State(hex_list, [initial_hex], initial_hex, initial_hex.weight)
    solution, cost = graph_search(initial_state)
    for hexagon in solution:
        print()
        print(hexagon)
    print()
    print("MINIMAL-COST PATH COSTS: {}".format(cost))


if __name__ == '__main__':
    driver()
