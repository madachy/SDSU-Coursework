import math
from numpy import random
from numpy import cumsum
import matplotlib.pyplot as plt
from collections import Counter

def main():
    n = 10000
    input_lines = list()
    with open("battleSimRandomInputs.csv") as input_file:
        for line in input_file:
            input_lines.append(line.split(','))
    # Trash CSV's header line
    input_lines = input_lines[1:]
    for line in input_lines:
        line[1] = int(line[1])
        line[2] = float(line[2])
        line[3] = float(line[3])

    x = input_lines[0][1]
    y = input_lines[1][1]
    timestep = 0.1
    verbose = False
    results = list()
    for i in range(n):
        alpha = random.uniform(input_lines[0][2], input_lines[0][3])
        beta = random.uniform(input_lines[1][2], input_lines[1][3])
        results.append(lanchestersLaw(x, y, alpha, beta, timestep, verbose))
    troop_levels = Counter([result[0] for result in results])
    times = Counter([result[2] for result in results])
    level = list()
    per = list()
    for troop in sorted(troop_levels.items(), key=lambda tup: tup[0]):
        level.append(troop[0])
        per.append(troop[1]/n)
    plt.subplot(2, 1, 1)
    plt.plot(level, per)
    plt.plot(level, cumsum(per), c="red")
    plt.title("Troop Levels and Duration of Simulation n:{}".format(n))
    plt.ylabel("Troop Level Percent Probability")
    plt.subplot(2, 1, 2)
    level = list()
    per = list()
    for time in sorted(times.items(), key=lambda tup: tup[0]):
        level.append(time[0])
        per.append(time[1]/n)
    plt.plot(level, per)
    plt.plot(level, cumsum(per), c="red")
    plt.ylabel("Time Duration Probability")

    plt.show()
    print(troop_levels)


def lanchestersLaw(x: int = 1000, y: int = 800, alpha: float = 0.8, beta: float = 0.9, timestep: float = 0.1,
                   verbose=False):
    # Parallel Lists that Hold population counts for X and Y Types as well as current time
    values = {'X': [x], 'Y': [y], 't': [0.00]}
    while x > 0.5 and y > 0.5:
        values['X'].append(x - (beta * y * timestep))
        values['Y'].append(y - (alpha * x * timestep))
        values['t'].append(values['t'][-1] + timestep)
        x = values['X'][-1]
        y = values['Y'][-1]
    # Prevents Negative Population Values from Being Graphed
    if x <= 0.5:
        values['X'][-1] = 0
        x = 0
        if verbose:
            print("X - Type Depleted")
    if y <= 0.5:
        values['Y'][-1] = 0
        y = 0
        if verbose:
            print("Y - Type Depleted")
    if verbose:
        print(values)

    # Plot X And Y Type and setup legend
    # plt.plot(values['t'], values['X'], label='X - Type [X0: {}, alpha: {}]'.format(values['X'][0], alpha))
    # plt.plot(values['t'], values['Y'], label='Y - Type [Y0: {}: beta: {}]'.format(values['Y'][0], beta))
    # plot_helper(timestep)
    return int(x//10), int(y), round(values['t'][-1], 3)



# Handles beautification of graph output
def plot_helper(timestep: str):
    plt.legend()
    plt.grid(True)
    plt.title("Survivors vs Time")
    plt.xlabel("Time (Time Step: {})".format(timestep))
    plt.ylabel("Survivors")
    plt.show()


if __name__ == '__main__':
    main()
