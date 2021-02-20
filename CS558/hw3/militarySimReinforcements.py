from typing import Dict
import matplotlib.pyplot as plt


def main():
    x, y, alpha, beta, time_step, reinforcements, verbose = get_user_input()
    lanchestersLaw(x, y, alpha, beta, time_step, reinforcements, verbose)


def lanchestersLaw(x: int = 1000, y: int = 800, alpha: float = 0.8, beta: float = 0.9, time_step: float = 0.1,
                   reinforcements: Dict[str, list] = None,
                   verbose=False):
    # Parallel Lists that Hold population counts for X and Y Types as well as current time
    values = {'X': [x], 'Y': [y], 't': [0.00]}
    # 0.01 as cutoff to prevent infinite looping if matching troops
    while x > 0.01 and y > 0.01:

        # Checks to see if reinforcements should be added for X Type
        for reinforcement in reinforcements['X']:
            # Check to see if used already
            if reinforcement[3]:
                # Check troop level for reinforcement
                if reinforcement[0] >= x / values['X'][0]:
                    # Number of reinforcements
                    reinforcement_level = reinforcement[1] * values['X'][0]
                    # Alpha being adjusted for new troops
                    alpha = alpha * x / (x + reinforcement_level) + reinforcement[2] * reinforcement_level / (
                            x + reinforcement_level)
                    x += reinforcement_level
                    # Mark reinforcement as being used
                    reinforcement[3] = False
                    if verbose:
                        print("X Reinforcement {} used Current Troop Level: {} Current Alpha: {} at time: {}".format(
                            reinforcement[:-1], x, alpha, values['t'][-1]))
            else:
                # already used as reinforcement
                pass
        # Checks to see if reinforcements should be added for X Type
        for reinforcement in reinforcements['Y']:
            # Check to see if used already
            if reinforcement[3]:
                # Check troop level for reinforcement
                if reinforcement[0] >= y / values['Y'][0]:
                    # Number of reinforcements
                    reinforcement_level = reinforcement[1] * values['Y'][0]
                    # Beta being adjusted for new troops
                    beta = beta * y / (y + reinforcement_level) + reinforcement[2] * reinforcement_level / (
                            y + reinforcement_level)
                    y += reinforcement_level
                    # Mark reinforcement as being used
                    reinforcement[3] = False
                    if verbose:
                        print("Y Reinforcement {} used Current Troop Level: {} Current Beta: {} at time: {}".format(
                            reinforcement[:-1], y, beta, values['t'][-1]))
            else:
                # already used as reinforcement
                pass
        values['X'].append(x - (beta * y * time_step))
        values['Y'].append(y - (alpha * x * time_step))
        values['t'].append(values['t'][-1] + time_step)
        x = values['X'][-1]
        y = values['Y'][-1]
    # Prevents Negative Population Values from Being Graphed
    if x <= 0:
        values['X'][-1] = 0
        x = 0
        if verbose:
            print("X - Type Depleted")
    if y <= 0:
        values['Y'][-1] = 0
        y = 0
        if verbose:
            print("Y - Type Depleted")
    if verbose:
        print(values)

    # Plot X And Y Type and setup legend
    plt.plot(values['t'], values['X'],
             label='X - Type [X0: {}, Reinforcements: {}]'.format(values['X'][0], len(reinforcements['X'])))
    plt.plot(values['t'], values['Y'],
             label='Y - Type [Y0: {}, Reinforcements: {}]'.format(values['Y'][0], len(reinforcements['Y'])))
    plot_helper(time_step)


# Handles beautification of graph output
def plot_helper(time_step):
    plt.legend()
    plt.grid(True)
    plt.title("Survivors vs Time")
    plt.xlabel("Time (Time Step: {})".format(time_step))
    plt.ylabel("Survivors")
    plt.show()


# Grabs user input from stdin only if in the right range and data type, other wise re-prompt
def get_user_input():
    print("Please Enter Starting Amount for Troop Levels and their Lethality Coefficients")
    x = y = alpha = beta = time_step = verbose = -1
    reinforcements = {'X': list(), 'Y': list()}
    reinforcement_count: int = -1
    while x < 0:
        try:
            x = int(input("Number of Starting Troops for X - Type: "))
            if x < 0:
                raise ValueError
        except ValueError:
            print("Please enter a Positive Integer for Troop Levels")
    while alpha <= 0 or alpha > 1:
        try:
            alpha = float(input("Lethality Coefficient for X - Type: "))
            if alpha <= 0 or alpha > 1:
                raise ValueError
        except ValueError:
            print("Please enter a decimal (0, 1] for Lethality Coefficient")
    while reinforcement_count < 0 or reinforcement_count > 3:
        try:
            reinforcement_count = int(input("Number of Reinforcement Events for X - Type: "))
            if reinforcement_count < 0:
                raise ValueError
        except ValueError:
            print("Please enter a Positive Integer [0, 3] for Reinforcement Events")
    for i in range(reinforcement_count):
        percent = troop_percent = lethality = -1
        while not (0.1 <= percent <= 0.8):
            try:
                percent = float(input("Percent Depletion for Reinforcements: "))
                if percent < 0.1 or percent > 0.8:
                    raise ValueError
            except ValueError:
                print("Please enter a decimal [0.1, 0.8] for Percent Depletion")
        while not (0.1 <= troop_percent <= 0.5):
            try:
                troop_percent = float(input("Percentage of Original Troops for Reinforcements: "))
                if troop_percent > 0.5 or troop_percent < 0.1:
                    raise ValueError
            except ValueError:
                print("Please enter a decimal [0.1, 0.5] for Original Troops for Reinforcements")
        while lethality <= 0 or lethality > 1:
            try:
                lethality = float(input("Lethality Coefficient for Reinforcements: "))
                if lethality <= 0 or lethality > 1:
                    raise ValueError
            except ValueError:
                print("Please enter a decimal (0, 1] for Lethality Coefficient")
        reinforcements['X'].append([percent, troop_percent, lethality, True])

    while y <= 0:
        try:
            y = int(input("Number of Starting Troops for Y - Type: "))
            if x < 0:
                raise ValueError
        except ValueError:
            print("Please enter a Positive Integer for Troop Levels")
    while beta <= 0 or beta > 1:
        try:
            beta = float(input("Lethality Coefficient for Y - Type: "))
            if beta <= 0 or beta > 1:
                raise ValueError
        except ValueError:
            print("Please enter a decimal (0, 1] for Lethality Coefficient")
    reinforcement_count = -1
    while reinforcement_count < 0 or reinforcement_count > 3:
        try:
            reinforcement_count = int(input("Number of Reinforcement Events for Y - Type: "))
            if reinforcement_count < 0:
                raise ValueError
        except ValueError:
            print("Please enter a Positive Integer [0, 3] for Reinforcement Events")
    while reinforcement_count < 0 or reinforcement_count > 3:
        try:
            x = int(input("Number of Reinforcement Events for X - Type: "))
            if reinforcement_count < 0:
                raise ValueError
        except ValueError:
            print("Please enter a Positive Integer [0, 3] for Reinforcement Events")
    for i in range(reinforcement_count):
        percent = troop_percent = lethality = -1
        while not (0.1 <= percent <= 0.8):
            try:
                percent = float(input("Percent Depletion for Reinforcements: "))
                if percent < 0.1 or percent > 0.8:
                    raise ValueError
            except ValueError:
                print("Please enter a decimal [0.1, 0.8] for Percent Depletion")
        while not (0.1 <= troop_percent <= 0.5):
            try:
                troop_percent = float(input("Percentage of Original Troops for Reinforcements: "))
                if troop_percent > 0.5 or troop_percent < 0.1:
                    raise ValueError
            except ValueError:
                print("Please enter a decimal [0.1, 0.5] for Original Troops for Reinforcements")
        while lethality <= 0 or lethality > 1:
            try:
                lethality = float(input("Lethality Coefficient for Reinforcements: "))
                if lethality <= 0 or lethality > 1:
                    raise ValueError
            except ValueError:
                print("Please enter a decimal (0, 1] for Lethality Coefficient")
        reinforcements['Y'].append([percent, troop_percent, lethality, True])
    while time_step <= 0:
        try:
            # Needed as a float or int entered is valid as long as it is within domain specified
            temp_input = input("Time Step for Simulation (0, inf): ")
            try:
                time_step = float(temp_input)
            except ValueError:
                time_step = int(temp_input)
            if time_step <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a number (0, inf) for Time Step")
    while str(verbose).upper() not in ["TRUE", "FALSE", "T", "F"]:
        try:
            verbose = input("Verbose Text Output (True/False): ")
            if str(verbose).upper() not in ["TRUE", "FALSE", "T", "F"]:
                raise ValueError
        except ValueError:
            print("Please enter True or False for Verbose Output")
        verbose = str(verbose).upper()
    return x, y, alpha, beta, time_step, reinforcements, verbose == "TRUE" or verbose == "T"


if __name__ == '__main__':
    main()
