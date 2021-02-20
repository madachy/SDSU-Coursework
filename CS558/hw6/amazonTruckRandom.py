import statistics
from collections import Counter
from matplotlib import pyplot as plt
from numpy import cumsum
import simpy
from numpy import random


def main():
    global waiting_times, min_queue, max_queue, idle_time, last_served
    verbose = False
    singe_run_info = False
    server_name = "Repair Facility"
    entity_name = "Amazon Truck"
    n = 10000
    total_costs = list()
    avg_waiting_times = list()
    avg_resc_util = list()

    input_lines = list()
    with open("amazonTruckRandom.csv") as input_file:
        for line in input_file:
            input_lines.append(line.split(','))
    capacity = int(input_lines[1][0])
    probability_of_service = float(input_lines[1][1])
    service_window = (float(input_lines[1][2]), float(input_lines[1][3]))
    days = int(input_lines[1][4])
    facility_cost = float(input_lines[1][5])
    downtime_cost = float(input_lines[1][6])

    for run in range(n):
        interarrival_times = list()
        service_times = list()
        last_arrival = 0
        for i in range(days + 1):
            if random.uniform(0, 1) <= probability_of_service:
                interarrival_times.append(i - last_arrival)
                last_arrival = i
                service_times.append(random.uniform(service_window[0], service_window[1]))

        environment = simpy.Environment()
        server = simpy.Resource(environment, capacity=capacity)
        waiting_times = list()
        min_queue = len(interarrival_times)
        max_queue = -1
        arrival_time = idle_time = last_served = 0
        for i in range(len(interarrival_times)):
            arrival_time += interarrival_times[i]
            service_time = service_times[i]
            environment.process(
                queue_server(environment, "{} {}".format(entity_name, i), server, arrival_time, service_time, verbose))

        environment.run()
        total_cost = round(
            environment.now * facility_cost * capacity + downtime_cost * sum(waiting_times + service_times), 2)
        total_costs.append(total_cost)
        avg_waiting_times.append(round(statistics.mean(waiting_times), 2))
        try:
            avg_resc_util.append(round((environment.now - idle_time) / environment.now, 2))
        except ZeroDivisionError:
            avg_resc_util.append(100)
        if singe_run_info:
            print("-----Single Run Information -----")
            print("Minimum Queue Length: {}".format(min_queue))
            print("Maximum Queue Length: {}".format(max_queue))
            print("Total Idle Time For {}: {:.2f}".format(server_name, idle_time))
            try:
                print("Resource Utilization: {:.2f}%".format((environment.now - idle_time) / environment.now * 100))
            except ZeroDivisionError:
                print("Resource Utilization: 100%")
            print("Total Queue Time: {:.2f}".format(sum(waiting_times)))
            print("Mean Waiting Time: {:.2f}".format(statistics.mean(waiting_times)))
            try:
                print("Variance of Waiting Time: {:.2f}".format(statistics.variance(waiting_times)))
            except statistics.StatisticsError:
                print("Variance requires 2 or more data points")
            print("Total Cost: {:.2f}".format(total_cost))
    data = [total_costs, avg_waiting_times, avg_resc_util]
    plt.title("Amazon Fright Simulation n: {}".format(n))
    for i in range(len(data)):
        plt.subplot(len(data), 1, i + 1)
        if i == 0:
            title = "Total Cost"
        elif i == 1:
            title = "Avg Waiting Days"
        else:
            title = "Resource Utilization"

        x_data = list()
        y_data = list()
        count = Counter([round(d, 2) for d in data[i]])
        for single_run in sorted(count.items(), key=lambda tup: tup[0]):
            x_data.append(single_run[0])
            y_data.append(single_run[1] / n)
        plt.title(title + ", mean: {:.2f}".format(statistics.mean(x_data)))
        plt.plot(x_data, y_data)
        plt.plot(x_data, cumsum(y_data), c="red")
    plt.show()


def queue_server(environment: simpy.Environment, entity: str, server: simpy.Resource, arrival_time: float,
                 service_time: float, verbose: bool):
    global waiting_times, min_queue, max_queue, idle_time, last_served
    last_served = 0
    yield environment.timeout(arrival_time)
    if verbose:
        print("{} arriving at {}".format(entity, environment.now))
    with server.request() as request:
        yield request
        queue = len(server.queue)
        min_queue = min(min_queue, queue)
        max_queue = max(max_queue, queue)
        waiting_time = environment.now - arrival_time
        if abs(0 - waiting_time) <= 0.001 and server.count == 1:
            idle_time += arrival_time - last_served
        if verbose:
            print("{} waiting time {:.2f}".format(entity, waiting_time))
            print("{} starting service at {}".format(entity, environment.now))
        yield environment.timeout(service_time)
        queue = len(server.queue)
        min_queue = min(min_queue, queue)
        max_queue = max(max_queue, queue)
        if verbose:
            print("{} served at {}".format(entity, environment.now))
        last_served = environment.now
        waiting_times.append(waiting_time)


if __name__ == "__main__":
    main()
