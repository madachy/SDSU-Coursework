# William Fox 2019/04/06

from typing import List, Tuple

import matplotlib.pyplot as plot
import numpy


def random_move() -> (int, int):
    # (dx, xy) SW, S, SE, E, NE, N, NW, W
    off_sets = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    return off_sets[numpy.random.randint(len(off_sets))]


class Board:
    def __init__(self, team_names: List[str], x_limit: int, y_limit: int):
        self.team_names = team_names
        self.x_limit = x_limit
        self.y_limit = y_limit


class Player:
    def __init__(self, color: str, x_pos: int, y_pos: int):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_alive = True
        self.is_dead = False

    def at(self, other_agent: 'Player'):
        # Is the other agent alive at our position?
        return other_agent.is_alive and self.x_pos == other_agent.x_pos and self.y_pos == other_agent.y_pos

    def kill(self):
        self.is_alive = False
        self.is_dead = True

    def friendly(self, other_agent: 'Player'):
        return self.color == other_agent.color

    # Move player to random adjacent position if able to
    def move(self, players: List[List['Player']], board: Board):
        if self.is_locked_in(players, board):
            print("No Valid Move for {} @ {}".format(self.color, self.position()))
            return
        # Go Until a valid move is found
        move = random_move()
        while self.is_not_valid_move(move, players, board):
            move = random_move()
        # Add (dx, dy) to current position
        prev_position_helper = Player("", self.x_pos, self.y_pos)
        self.x_pos += move[0]
        self.y_pos += move[1]
        print("{} @ {} Moved to {}".format(self.color, prev_position_helper.position(), self.position()))
        # Check to see if we got a rival piece
        for team in players:
            if self in team:
                continue
            for other_agent in team:
                if self.at(other_agent):
                    print("{} killed {} @ {}".format(self.color, other_agent.color, self.position()))
                    other_agent.kill()
                    return

    # Returns true if the move is invalid for our self
    def is_not_valid_move(self, move: (int, int), players: List[List['Player']], board: Board) -> bool:
        # -1 to account for 0 indexing of board
        if self.x_pos + move[0] < 0 or self.x_pos + move[0] > board.x_limit - 1:
            return True
        elif self.y_pos + move[1] < 0 or self.y_pos + move[1] > board.y_limit - 1:
            return True
        # Check to see if ally occupies that spot
        for team in players:
            if self not in team:
                continue
            for friendly_agent in team:
                if Player("", self.x_pos + move[0], self.y_pos + move[1]).at(friendly_agent):
                    return True
        return False

    # Returns true if there is no valid moves for self
    def is_locked_in(self, players: List[List['Player']], board: Board) -> bool:
        # (dx, xy) SW, S, SE, E, NE, N, NW, W
        off_sets = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        return sum([self.is_not_valid_move(move, players, board) for move in off_sets]) == len(off_sets)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        status = "{} @ ({}, {})".format(self.color, self.x_pos, self.y_pos)
        if self.is_alive:
            return status + " Alive"
        else:
            return status + " Dead "

    def position(self) -> str:
        return "({}, {})".format(self.x_pos, self.y_pos)


def main():
    move_limit = 1000
    input_lines = list()
    with open("boardGameInputs.csv") as input_file:
        for line in input_file:
            input_lines.append(line.split(','))
    # Trash header line
    input_lines = input_lines[1:]
    x_limit, y_limit = int(input_lines[0][0]), int(input_lines[0][1])
    # Trash Board Input and Next Header
    input_lines = input_lines[2:]
    input_lines = [[line[0], int(line[1])] for line in input_lines]
    board = Board([line[0] for line in input_lines], x_limit, x_limit)
    teams = list()
    taken_starting_positions = list()
    # Place teams from input on the board
    for line in input_lines:
        team, taken_starting_positions = plot_player(line[0], line[1], x_limit, y_limit, taken_starting_positions)
        teams.append(team)
    verbose = False
    if verbose:
        verbose_helper("---Starting State", teams)
    move_count = 0
    move_limit_reached = False
    # Keep going until one team wins or move limit reached
    while is_more_than_one_team_remaining(teams) and not move_limit_reached:
        for team in teams:
            # Skip team if all players are dead
            if len(team) == count_dead(team):
                continue
            # Find random alive player to move
            agent_idx = numpy.random.randint(0, len(team))
            while team[agent_idx].is_dead:
                agent_idx = numpy.random.randint(0, len(team))
            # Move found player
            team[agent_idx].move(teams, board)
        move_count += 1
        move_limit_reached = move_limit == move_count

    if move_limit_reached:
        print("Move Limit of {} Hit".format(move_limit))
    else:
        for team in teams:
            if len(team) != count_dead(team):
                print("Team {} is last standing".format(team[0].color))
    if verbose:
        verbose_helper("---Ending State", teams)

    plot_helper(teams, board)


def plot_player(color: str, n: int, x_limit: int, y_limit: int, taken_starting_positions) -> Tuple[List[Player], List]:
    players = list()
    for i in range(n):
        x_pos = numpy.random.randint(x_limit)
        y_pos = numpy.random.randint(y_limit)
        while (x_pos, y_pos) in taken_starting_positions:
            if len(taken_starting_positions) == x_limit * y_limit:
                print("Team Counts too Large for Board of {} x {}".format(x_limit, y_limit))
                exit()
            x_pos = numpy.random.randint(x_limit)
            y_pos = numpy.random.randint(y_limit)
        taken_starting_positions.append((x_pos, y_pos))
        players.append(Player(color, x_pos, y_pos))
    return players, taken_starting_positions


def count_dead(team: List[Player]) -> int:
    count = 0
    for agent in team:
        if not agent.is_alive:
            count += 1
    return count


def is_more_than_one_team_remaining(teams: List[List[Player]]) -> bool:
    return sum([len(team) == count_dead(team) for team in teams]) < len(teams) - 1


def plot_helper(teams: List[List[Player]], board: Board):
    for team in teams:
        plot.scatter([agent.x_pos for agent in team if agent.is_alive],
                     [agent.y_pos for agent in team if agent.is_alive], c=team[0].color, s=1000)
        plot.scatter([agent.x_pos for agent in team if not agent.is_alive],
                     [agent.y_pos for agent in team if not agent.is_alive], c=team[0].color, marker="x", s=1000)
    plot.axis([-1, board.x_limit, -1, board.y_limit])
    plot.grid()
    plot.xlabel("X Position")
    plot.ylabel("Y Position")
    plot.title("Ending State For Random Board Game\n")
    plot.show()


def verbose_helper(message: str, teams: List[List[Player]]):
    print(message)
    for team in teams:
        print(team, " Dead: {}".format(count_dead(team)))
    print()


if __name__ == '__main__':
    main()
