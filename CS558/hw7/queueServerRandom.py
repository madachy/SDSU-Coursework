from statistics import mean, stdev, variance, StatisticsError
from collections import Counter
from matplotlib import pyplot as plt
from numpy import cumsum, random
from typing import List
import simpy


def main():
    global waiting_times, min_queue, max_queue, idle_time, last_served
    verbose = False
    singe_run_info = False
    server_name = "Server"
    entity_name = "Customer"
    monte_carlo_runs = 10000
    number_of_customers = 100
    server_capacity = 1
    avg_waiting_times = list()
    max_queue_lengths = list()
    idle_times = list()
    max_queue_times = list()
    for run in range(monte_carlo_runs):
        interarrival_times = list()
        service_times = list()
        last_arrival = 0
        for i in range(number_of_customers):
            interarrival_times.append(random.exponential(5))
            service_times.append(random.uniform(1, 5))

        environment = simpy.Environment()
        server = simpy.Resource(environment, capacity=server_capacity)
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
        avg_waiting_times.append(round(mean(waiting_times), 2))
        idle_times.append(idle_time)
        max_queue_lengths.append(max_queue)
        max_queue_times.append(sum(waiting_times))
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
            print("Mean Waiting Time: {:.2f}".format(mean(waiting_times)))
            try:
                print("Variance of Waiting Time: {:.2f}".format(variance(waiting_times)))
            except StatisticsError:
                print("Variance requires 2 or more data points")
    data = [avg_waiting_times, max_queue_times, idle_times]
    for i in range(len(data)):
        plt.subplot(len(data), 1, i+1)
        ci = get_CI(data[i], len(data[i]))
        if i == 0:
            plt.title("Queue Server Simulation n: {}".format(monte_carlo_runs))
            xlabel = "Avg Waiting Time (minutes), 95% CI: ({:.3f}, {:.3f})".format(ci[0], ci[1])
        elif i == 1:
            xlabel = "Total Waiting Time (minutes), 95% CI: ({:.3f}, {:.3f})".format(ci[0], ci[1])
        elif i == 2:
            xlabel = "Server Idle Time (minutes), 95% CI: ({:.3f}, {:.3f})".format(ci[0], ci[1])
        elif i == 3:
            xlabel = "Max Queue Length, 95% CI: ({:.3f}, {:.3f})".format(ci[0], ci[1])
        x_data = list()
        y_data = list()
        count = Counter([round(d, 2) for d in data[i]])
        for single_run in sorted(count.items(), key=lambda tup: tup[0]):
            x_data.append(single_run[0])
            y_data.append(single_run[1] / monte_carlo_runs)
        plt.xlabel(xlabel)
        plt.ylabel("Probability")
        plt.plot(x_data, y_data, label="PDF")
        plt.plot(x_data, cumsum(y_data), c="red", label="CDF")
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


def get_CI(data: List, n: int, z=1.96) -> (float, float):
    data_mean = mean(data)
    data_stdev = stdev(data)
    data_me = z * data_stdev / (n ** 0.5)
    return data_mean - data_me, data_mean + data_me


if __name__ == "__main__":
    main()
