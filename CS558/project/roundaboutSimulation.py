import json
from collections import defaultdict, Counter
from math import ceil, floor
from statistics import mean
from typing import List, Dict

from matplotlib import pyplot
from numpy import random, cumsum

global verbose
verbose = False
low_entry_flow = 0
high_entry_flow = 1200


def main():
    with open("roundaboutInput.json", "r") as read_file:
        data = json.load(read_file)
    if verbose:
        print(data)
    is_random = data["random"] is not None
    number_of_runs = data["number_of_runs"]
    is_single_run = number_of_runs == 1
    if number_of_runs < 1:
        exit()
    elif not is_random and data["static"] is None:
        exit()
    multi_run_info = defaultdict(list)
    for i in range(number_of_runs):
        if is_random:
            dist = data["random"]["distribution"]
            entry_flow = floor(get_entry_flow(dist, data["random"]))
        else:
            entry_flow = data["static"]["entry_flow"]
        initial_level = data["initial_level"]
        avg_delay = get_average_delay(entry_flow)
        parking_lot_history, roundabout_history, delay_history, ending_time = simulate(initial_level, entry_flow,
                                                                                       avg_delay, is_single_run)
        multi_run_info["parking_lot_history"].append(parking_lot_history)
        multi_run_info["roundabout_history"].append(roundabout_history)
        multi_run_info["delay_history"].append(delay_history)
        multi_run_info["ending_time"].append(ending_time)
        multi_run_info["entry_flow"].append(entry_flow)
        if verbose:
            print("Avg Delay: {}, Entry Flow: {}, Capacity: {}".format(avg_delay, entry_flow,
                                                                       get_capacity_of_movement(entry_flow)))
    if is_single_run:
        single_run_plot_helper(multi_run_info["parking_lot_history"], multi_run_info["roundabout_history"],
                               multi_run_info["delay_history"], entry_flow)
    else:
        multi_run_plot_helper(multi_run_info["roundabout_history"], multi_run_info["delay_history"],
                              multi_run_info["ending_time"], data["initial_level"], number_of_runs,
                              mean(multi_run_info["entry_flow"]))


def get_entry_flow(dist: str, data: Dict) -> float:
    entry_flow = -1
    if dist == "normal":
        location = data["loc"]
        scale = data["scale"]
        while not is_valid_entry_flow(entry_flow):
            entry_flow = random.normal(location, scale)
    elif dist == "uniform":
        low = data["low"]
        high = data["high"]
        while not is_valid_entry_flow(entry_flow):
            entry_flow = random.uniform(low, high)
    elif dist == "triangle":
        left = data["left"]
        right = data["right"]
        mode = data["mode"]
        while not is_valid_entry_flow(entry_flow):
            entry_flow = random.triangular(left, mode, right)

    return entry_flow


def simulate(initial_level: int, entry_flow: float, avg_delay: int, is_single_run=False):
    time = 0
    parking_lot_count = initial_level
    roundabout_waiting = 0
    parking_lot_history = [(0, parking_lot_count)]
    if is_single_run:
        roundabout_history = [(0, 0)]
    else:
        roundabout_history = [0]
    delay_history = list()
    while parking_lot_count > 0 or roundabout_waiting > 0:
        roundabout_estimate_delay = get_estimate_delay(parking_lot_count, initial_level - parking_lot_count,
                                                       initial_level, avg_delay)
        if is_single_run:
            delay_history.append((time / 60, roundabout_estimate_delay))
        else:
            delay_history.append(roundabout_estimate_delay)
        if time % (3600 // entry_flow) == 0:
            if parking_lot_count > 0:
                parking_lot_count -= 1
                roundabout_waiting += 1
                if is_single_run:
                    parking_lot_history.append((time / 60, parking_lot_count))
                    roundabout_history.append((time / 60, roundabout_waiting))
                else:
                    roundabout_history.append(roundabout_waiting)
        if time % roundabout_estimate_delay == 0:
            if roundabout_waiting > 0:
                roundabout_waiting -= 1
                if is_single_run:
                    roundabout_history.append((time / 60, roundabout_waiting))
                else:
                    roundabout_history.append(roundabout_waiting)
        time += 1
    return parking_lot_history, roundabout_history, delay_history, time


# Estimates current delay based on the amount of cars left in starting level
# Returns between minimum_delay and max_multiplier * average_delay
def get_estimate_delay(cars_in_lot: int, cars_left_lot: int, total_cars: int, avg_delay: int) -> int:
    min_delay = 1
    max_multiplier = 1.8
    return floor(
        (max_multiplier - max_multiplier * abs(cars_left_lot - cars_in_lot) / total_cars) * avg_delay) + min_delay


# Returns the average delay for the entry flow passed in
def get_average_delay(entry_flow: float) -> int:
    capacity = get_capacity_of_movement(entry_flow)
    if capacity == 0:
        capacity = 1
    time_step = 1 / 60
    free = (entry_flow / capacity - 1)
    under_root = free ** 2 + (3600 * entry_flow) / (450 * time_step * capacity ** 2)
    return ceil(3600 / capacity + 900 * time_step * (free + under_root ** 0.5))


# Returns the capacity of movement for a single lane roundabout for the entry flow
def get_capacity_of_movement(entry_flow: float) -> float:
    if not is_valid_entry_flow(entry_flow):
        print("Invalid Entry Flow For Single Lane Roundabout")
        exit(1)
    elif entry_flow <= 500:
        return 1800 - entry_flow
    elif entry_flow <= high_entry_flow:
        return 15600 / 7 - entry_flow * 13 / 7


# Checks to see if entry_flow is valid for single lane roundabout
def is_valid_entry_flow(entry_flow: float) -> float:
    return low_entry_flow <= entry_flow <= high_entry_flow


# easier plot helper for list of tuples
def zip_plot_helper(history: List, message: str):
    x, y = zip(*history)
    if verbose:
        print(message, mean(y))
    pyplot.plot(x, y, label=message)


# Prints information relevant to a single run of the simulation
def single_run_plot_helper(parking_lot_history: List, roundabout_history: List, delay_history: List, entry_flow: int):
    # Turns list of list into single list
    parking_lot_history = parking_lot_history[0]
    roundabout_history = roundabout_history[0]
    delay_history = delay_history[0]
    pyplot.title("Parking Lot Egress (Flow of {} Veh/Hr) to a Roundabout Controlled Road".format(entry_flow))
    pyplot.ylabel("Cars")
    pyplot.xlabel("Time (minutes)")
    pyplot.grid()
    zip_plot_helper(parking_lot_history, "Parking Lot Level")
    zip_plot_helper(roundabout_history, "Roundabout Level")
    zip_plot_helper(delay_history, "Estimated Roundabout Delay")
    pyplot.legend()
    pyplot.show()


def pdf_cdf_plot_helper(data: List):
    variate_counts = Counter(data)
    variates = list()
    probability = list()
    for variate in sorted(variate_counts.items(), key=lambda tup: tup[0]):
        variates.append(variate[0])
        probability.append(variate[1] / len(data))

    pyplot.ylabel("Probability")
    pyplot.plot(variates, probability, label="PDF")
    pyplot.plot(variates, cumsum(probability), c="Red", label="CDF")
    pyplot.legend()


def multi_run_plot_helper(roundabout_history: List[List], delay_history: List[List], ending_time: List, cars: int,
                          runs: int, average_entry_flow:float):
    roundabout_max_queue = [max(roundabout_hist) for roundabout_hist in roundabout_history]
    average_delay = [mean(delay_hist) for delay_hist in delay_history]
    # Convert to minutes
    ending_time = [time / 60 for time in ending_time]
    pyplot.subplot(3, 1, 1)
    pyplot.title("Parking Lot Egress of {} Cars, n={}, mean entry flow={:.2f}".format(cars, runs, average_entry_flow))
    pyplot.xlabel("Maximum Roundabout Stock Level (Cars), mean: {:.2f}".format(mean(roundabout_max_queue)))
    pdf_cdf_plot_helper(roundabout_max_queue)
    pyplot.subplot(3, 1, 2)
    pdf_cdf_plot_helper(average_delay)
    pyplot.xlabel("Average Delay (Seconds), mean: {:.2f}".format(mean(average_delay)))
    pyplot.subplot(3, 1, 3)
    pdf_cdf_plot_helper(ending_time)
    pyplot.xlabel("Ending Time (Minutes), mean: {:.2f}".format(mean(ending_time)))
    pyplot.show()


if __name__ == '__main__':
    main()
