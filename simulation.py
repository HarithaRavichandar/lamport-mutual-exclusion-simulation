import simpy
from process import Process

def run_simulation(num_processes=3, sim_time=30):
    env = simpy.Environment()
    log = []

    processes = []
    for i in range(num_processes):
        p = Process(env, i + 1, [], log)
        processes.append(p)

    # Assign process list
    for p in processes:
        p.processes = processes

    # Start processes
    for p in processes:
        env.process(p.run())

    env.run(until=sim_time)

    return log