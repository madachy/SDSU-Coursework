import simpy
from matplotlib import pyplot as plt
from statistics import mean, stdev
from numpy import random


def main():
    global waiting_times, min_queue, max_queue, idle_time, last_served
    verbose = False
    entity_name = "Amazon Truck"
    n = 1000
    total_costs = list()

    input_lines = list()
    with open("amazonTruckRandom.csv") as input_file:
        for line in input_file:
            input_lines.append(line.split(','))
    capacity = int(input_lines[1][0])
    random_interarrival = input_lines[1][1].strip(" ") == 'True'
    service_window = (float(input_lines[1][2]), float(input_lines[1][3]))
    days = int(input_lines[1][4])
    facility_cost = float(input_lines[1][5])
    downtime_cost = float(input_lines[1][6])

    for run in range(n):
        interarrival_times = list()
        service_times = list()
        last_arrival = 0
        if not random_interarrival:
            for i in range(days + 1):
                interarrival_times.append(i - last_arrival)
                last_arrival = i
                service_times.append(random.uniform(service_window[0], service_window[1]))
        else:
            time_hr = 0
            while time_hr <= days * 24:
                interarrival_time = random.exponential(10)
                interarrival_times.append(interarrival_time / 24)
                service_times.append(random.uniform(service_window[0], service_window[1]))
                time_hr += interarrival_time

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

        environment.run(until=days)
        single_cost = environment.now * facility_cost * capacity + downtime_cost * sum(waiting_times + service_times)
        total_costs.append(single_cost / 1000000)

    plt.title("Amazon Fright Simulation, capacity: {},  n: {}".format(capacity, n))
    low_ci, high_ci = get_confidence_interval(total_costs, 1.645)
    plt.xlabel("Total Cost ($ Million), 90% CI: ({:.2f}, {:.2f})".format(low_ci, high_ci))
    plt.ylabel("Count")
    plt.hist(total_costs, rwidth=0.85)
    plt.show()
    print("Capacity: {}, Days: {}".format(capacity, days))
    print("Mean:", mean(total_costs), "Std. Dev:", stdev(total_costs))


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


def get_confidence_interval(data: list, z=1.95):
    sample_mean = mean(data)
    sample_stdev = stdev(data)
    sample_margin_of_error = z * sample_stdev / (len(data) ** 0.5)
    return sample_mean - sample_margin_of_error, sample_mean + sample_margin_of_error


if __name__ == "__main__":
    main()
