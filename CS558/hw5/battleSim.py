# William Fox 2019/04/06
import random
import sys
from typing import List

import matplotlib.pyplot as plot
import numpy


class Board:
    def __init__(self, team_names: List[str], x_limit: int, y_limit: int):
        self.team_names = team_names
        self.x_limit = x_limit
        self.y_limit = y_limit


class Soldier:
    def __init__(self, color: str, x_pos: int, y_pos: int, low_lethality: int, high_lethality: int):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.low_lethality = low_lethality
        self.high_lethality = high_lethality
        self.is_alive = True
        self.is_dead = False

    def kill(self):
        self.is_alive = False
        self.is_dead = True

    def is_friendly(self, other_agent: 'Soldier'):
        return self.color == other_agent.color

    def get_position(self) -> str:
        return "({}, {})".format(self.x_pos, self.y_pos)

    # Finds Closest Enemy to self using manhattan distance
    def find_closest_alive_enemy(self, armies: List[List['Soldier']]):
        lowest_distance = 2**32
        army_index = -1
        soldier_index = -1
        for army_i in range(len(armies)):
            if self in armies[army_i]:
                continue
            for soldier_i in range(len(armies[army_i])):
                if armies[army_i][soldier_i].is_alive:
                    if self.manhattan_distance(armies[army_i][soldier_i]) <= lowest_distance:
                        lowest_distance = self.manhattan_distance(armies[army_i][soldier_i])
                        army_index = army_i
                        soldier_index = soldier_i
                else:
                    # Is Dead
                    continue
        return army_index, soldier_index

    # Kills nearest alive enemy if self does not miss
    def shoot_nearest_alive_enemy(self, armies: List[List['Soldier']]):
        percent_to_hit = random.uniform(self.low_lethality, self.high_lethality)
        if random.uniform(0, 1) <= percent_to_hit:
            army_index, soldier_index = self.find_closest_alive_enemy(armies)
            armies[army_index][soldier_index].kill()
            verbose_helper(self.color, self.get_position(), armies[army_index][soldier_index].color,
                           armies[army_index][soldier_index].get_position(), "Killed")
        else:
            print("{} @ {} Missed".format(self.color, self.get_position()))

    def manhattan_distance(self, other_solder: 'Soldier'):
        return abs(self.x_pos - other_solder.x_pos) + abs(self.y_pos - other_solder.y_pos)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        status = "{} @ ({}, {})".format(self.color, self.x_pos, self.y_pos)
        if self.is_alive:
            return status + " Alive"
        else:
            return status + " Dead "


def main():
    global verbose
    verbose = True
    turn_limit = 100000
    input_lines = list()
    with open("battleSimInputs.csv") as input_file:
        for line in input_file:
            input_lines.append(line.split(','))
    # Trash CSV's header line
    input_lines = input_lines[1:]
    input_lines = [[line[0], int(line[1]), float(line[2]), float(line[3])] for line in input_lines]
    board = Board([line[0] for line in input_lines], 2**31, 2**31)
    armies = [plot_soldiers(line[0], line[1], board.x_limit, board.y_limit, (line[2], line[3])) for line in input_lines]

    turn_count = 0
    reached_limit = False
    # Go until all but one army is dead or turn limit reached
    while is_more_than_one_army_remaining(armies) and not reached_limit:
        for army in armies:
            # Skip army if all soldiers are dead
            if count_dead(army) != len(army):
            # Find random alive soldier from army who's turn it is
                random_shooter_index = numpy.random.randint(0, len(army))
                while army[random_shooter_index].is_dead:
                    random_shooter_index = numpy.random.randint(0, len(army))
                # Have that soldier shoot nearest alive enemy
                army[random_shooter_index].shoot_nearest_alive_enemy(armies)
        turn_count += 1
        reached_limit = turn_limit == turn_count

    if reached_limit:
        print("Move Limit of {} Hit".format(turn_limit))
    else:
        for army in armies:
            if count_dead(army) != len(army):
                print("Team {} is last standing".format(army[0].color))
                break
    plot_helper(armies, board)


def plot_soldiers(color: str, n: int, x_limit: int, y_limit: int, lethality_range: (int, int)) -> List[Soldier]:
    solders = list()
    taken_positions = list()
    for i in range(n):
        x_pos = numpy.random.randint(x_limit)
        y_pos = numpy.random.randint(y_limit)
        while (x_pos, y_pos) in taken_positions:
            if len(taken_positions) == x_limit * y_limit:
                print("Starting Troop Value of {} for Team {} is too Large for a Board of {} x {} ".format(n, color,
                                                                                                           x_limit,
                                                                                                           y_limit))
                exit()
            x_pos = numpy.random.randint(x_limit)
            y_pos = numpy.random.randint(y_limit)
        taken_positions.append((x_pos, y_pos))
        solders.append(Soldier(color, x_pos, y_pos, lethality_range[0], lethality_range[1]))
    return solders


# Counts all the dead soldiers in an army
def count_dead(army: List[Soldier]) -> int:
    count = 0
    for soldier in army:
        if soldier.is_dead:
            count += 1
    return count


def is_more_than_one_army_remaining(armies: List[List[Soldier]]) -> bool:
    return sum([count_dead(army) == len(army) for army in armies]) < len(armies) - 1


def verbose_helper(shooter: str, shooter_pos: str, shot: str, shot_pos: str, action: str):
    print("{} @ {} {} {} @ {}".format(shooter, shooter_pos, action, shot, shot_pos))


def plot_helper(armies: List[List['Soldier']], board: Board):
    for army in armies:
        plot.scatter([soldier.x_pos for soldier in army if soldier.is_alive],
                     [soldier.y_pos for soldier in army if soldier.is_alive], c=army[0].color, s=100)
        plot.scatter([soldier.x_pos for soldier in army if soldier.is_dead],
                     [soldier.y_pos for soldier in army if soldier.is_dead], c=army[0].color, marker="X", alpha=0.5,
                     s=100)
    plot.axis([0, board.x_limit, 0, board.y_limit])
    plot.xlabel("X Position")
    plot.ylabel("Y Position")
    plot.title("Ending State For Agent Based Battle Simulation Using Lanchester’s Law\n")
    plot.show()


if __name__ == '__main__':
    main()
