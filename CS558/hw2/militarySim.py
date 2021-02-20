import math
import matplotlib.pyplot as plt


def main():
    x, y, alpha, beta, timestep, verbose = get_user_input()
    lanchestersLaw(x, y, alpha, beta, timestep, verbose)


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

    # Pad graph to look better
    for i in range(5):
        values['X'].append(x)
        values['Y'].append(y)
        values['t'].append(values['t'][-1] + timestep)
    # Plot X And Y Type and setup legend
    plt.plot(values['t'], values['X'], label='X - Type [X0: {}, alpha: {}]'.format(values['X'][0], alpha))
    plt.plot(values['t'], values['Y'], label='Y - Type [Y0: {}: beta: {}]'.format(values['Y'][0], beta))
    plot_helper(timestep)


# Handles beautification of graph output
def plot_helper(timestep:str):
    plt.legend()
    plt.grid(True)
    plt.title("Survivors vs Time")
    plt.xlabel("Time (Time Step: {})".format(timestep))
    plt.ylabel("Survivors")
    plt.show()

def get_user_input():
    print("Please Enter Starting Amount for Troop Levels and their Lethality Coefficients")
    x = y = alpha = beta = timestep = verbose = -1
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
    while timestep <= 0:
        try:
            tempInput = input("Time Step for Simulation (0, inf): ")
            try:
                timestep = float(tempInput)
            except ValueError:
                timestep = int(tempInput)
            if timestep <= 0:
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
    return x, y, alpha, beta, timestep, verbose == "TRUE" or verbose == "T"
if __name__ == '__main__':
    main()
