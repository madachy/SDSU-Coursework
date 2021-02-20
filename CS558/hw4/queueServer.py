import re
import statistics
import sys

import simpy

from typing import List


def main():
    server_name, capacity, entity_name, interarrival_times, service_times, performance_measures = get_user_input()
    verbose = False
    environment = simpy.Environment()
    server = simpy.Resource(environment, capacity=capacity)

    global waiting_times, min_queue, max_queue, idle_time, last_served

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
    print("\nMinimum Queue Length: {}".format(min_queue))
    print("Maximum Queue Length: {}".format(max_queue))
    print("Total Idle Time For {}: {:.2f}".format(server_name, idle_time))
    try:
        print("Resource Utilization: {:.2f}%".format((environment.now - idle_time)/environment.now * 100))
    except ZeroDivisionError:
        print("Resource Utilization: 100%")
    print("Total Queue Time: {:.2f}".format(sum(waiting_times)))
    print("Mean Waiting Time: {:.2f}".format(statistics.mean(waiting_times)))
    try:
        print("Variance of Waiting Time: {:.2f}".format(statistics.variance(waiting_times)))
    except statistics.StatisticsError:
        print("Variance requires 2 or more data points")
    for i in range(len(performance_measures)):
        try:
            print("Performance Measure #{}: {}".format(i + 1, eval(performance_measures[i])))
        except:
            print(sys.exc_info()[0])
            print("Please Fix Error with Performance Measure #{}: {}".format(i + 1, performance_measures[i]))


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


def get_user_input() -> [str, int, str, List, List]:
    server_name = capacity = entity_name = interarrival_times = service_times = attribute_count = performance_count = None
    performance_measures = list()
    built_in_attributes = "min_queue:int, max_queue:int, waiting_times:list, capacity:int, service_times:list, "
    built_in_attributes += "interarrival_times:list, server:str, entity_name:str, idle_time:int, environment:Simpy.environment"
    print("Please Enter Information for Queue Server Simulation")
    while server_name is None:
        try:
            server_name = str(input("Server Name: "))
        except ValueError:
            server_name = None
            print("Please enter a String for Server Name")
    while capacity is None:
        try:
            capacity = int(input("Capacity: "))
            if capacity <= 0:
                raise ValueError
        except ValueError:
            capacity = None
            print("Please enter an Integer (0, inf) for Capacity")
    while entity_name is None:
        try:
            entity_name = str(input("Entity Name: "))
        except ValueError:
            entity_name = None
            print("Please enter a String for Server Name")
    while interarrival_times is None:
        try:
            interarrival_times = input("Please Enter Interarrival Times: ")
            interarrival_times = re.sub(r"[\[\],]", " ", interarrival_times).split()
            interarrival_times = [float(time) for time in interarrival_times]
            if any(time < 0 for time in interarrival_times):
                raise ValueError
            if len(interarrival_times) == 0:
                raise IndexError
        except ValueError:
            interarrival_times = None
            print("Please Enter Non Negative Floats Interarrival Times [f, f, f, f] ")
        except IndexError:
            interarrival_times = None
            print("Please Enter More Than 0 Interarrival Times: ")
    while service_times is None:
        try:
            service_times = input("Please Enter Service Times: ")
            service_times = re.sub(r"[\[\],]", " ", service_times).split()
            service_times = [float(time) for time in service_times]
            if any(time < 0 for time in service_times):
                raise ValueError
            if len(interarrival_times) != len(service_times):
                raise IndexError
        except ValueError:
            service_times = None
            print("Please Enter Non Negative Floats Service Times [f, f, f, f] ")
        except IndexError:
            service_times = None
            print("Service Time Input Length Does Not Match Length of Interarrival Times of {}".format(
                len(interarrival_times)))
    while attribute_count is None:
        try:
            attribute_count = int(input("Please enter number of attributes [0, inf): "))
            if attribute_count < 0:
                raise ValueError
        except ValueError:
            print("Number of Attributes should be within [0, inf)")
            attribute_count = None
    exec_helper(attribute_count, "Please enter attribute: ")
    while performance_count is None:
        try:
            performance_count = int(input("Please enter number of performance measures [0, inf): "))
            if performance_count < 0:
                raise ValueError
        except ValueError:
            print("Number of performance measures should be within [0, inf)")
            performance_count = None
    for i in range(performance_count):
        print("You have access to these built in attributes as well as your own customs: " + built_in_attributes)
        performance_measures.append(input("Please enter performance measure: "))

    return server_name, capacity, entity_name, interarrival_times, service_times, performance_measures

def exec_helper(count:int, prompt:str):
    for i in range(count):
        while True:
            try:
                exec(input(prompt), globals())
            except:
                print("Error, please fix: {}".format(sys.exc_info()[0]))
                continue
            break

if __name__ == "__main__":
    main()
