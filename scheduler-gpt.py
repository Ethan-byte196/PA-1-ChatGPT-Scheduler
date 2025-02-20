# Group 45:
# Valentina Terry
# Gabriel Martin
# Xander Levine
# Ethan Fuller

import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def fcfs_scheduling(processes, run_for):
    time = 0
    output = []
    queue = sorted(processes, key=lambda p: p.arrival)
    arrived = set()
    
    output.append(f"{len(processes)} processes")
    output.append("Using FCFS")
    while time < run_for:
        # Check and log all arrivals at the current time
        for p in processes:
            if p.arrival == time and p.name not in arrived:
                output.append(f"Time {time} : {p.name} arrived")
                arrived.add(p.name)
        
        available = [p for p in queue if p.arrival <= time]
        if available:
            current = available[0]
            if current.response_time == -1:
                current.response_time = time - current.arrival
            output.append(f"Time {time} : {current.name} selected (burst {current.burst})")
            for _ in range(current.burst):
                time += 1
                # Check and log any new arrivals during execution
                for p in processes:
                    if p.arrival == time and p.name not in arrived:
                        output.append(f"Time {time} : {p.name} arrived")
                        arrived.add(p.name)
            current.turnaround_time = time - current.arrival
            current.wait_time = current.turnaround_time - current.burst
            output.append(f"Time {time} : {current.name} finished")
            queue.remove(current)
        else:
            output.append(f"Time {time} : Idle")
            time += 1
    output.append(f"Finished at time {run_for}")
    for p in processes:
        output.append(f"{p.name} wait {p.wait_time} turnaround {p.turnaround_time} response {p.response_time}")
    return output

def rr_scheduling(processes, run_for, quantum):
    time = 0
    output = []
    queue = sorted(processes, key=lambda p: p.arrival)
    ready_queue = []
    arrived = set()

    output.append(f"{len(processes)} processes")
    output.append("Using Round-Robin")
    output.append(f"Quantum {quantum}")

    while time < run_for:
        # Check and log all arrivals at the current time
        for p in processes:
            if p.arrival == time and p.name not in arrived:
                output.append(f"Time {time} : {p.name} arrived")
                arrived.add(p.name)

        while queue and queue[0].arrival <= time:
            ready_queue.append(queue.pop(0))
        
        if ready_queue:
            current = ready_queue.pop(0)
            if current.response_time == -1:
                current.response_time = time - current.arrival
            burst_time = min(quantum, current.remaining_burst)
            output.append(f"Time {time} : {current.name} selected (burst {current.remaining_burst})")

            for _ in range(burst_time):
                time += 1
                # Check and log any new arrivals during execution
                for p in processes:
                    if p.arrival == time and p.name not in arrived:
                        output.append(f"Time {time} : {p.name} arrived")
                        arrived.add(p.name)

            current.remaining_burst -= burst_time
            if current.remaining_burst > 0:
                while queue and queue[0].arrival <= time:
                    ready_queue.append(queue.pop(0))
                ready_queue.append(current)
            else:
                current.turnaround_time = time - current.arrival
                current.wait_time = current.turnaround_time - current.burst
                output.append(f"Time {time} : {current.name} finished")
        else:
            output.append(f"Time {time} : Idle")
            time += 1

    output.append(f"Finished at time {run_for}")
    for p in processes:
        output.append(f"{p.name} wait {p.wait_time} turnaround {p.turnaround_time} response {p.response_time}")
    return output

def sjf_scheduling(processes, run_for):
    time = 0
    output = []
    queue = sorted(processes, key=lambda p: (p.arrival, p.burst))
    arrived = set()
    current_process = None  # Track the currently running process

    output.append(f"{len(processes)} processes")
    output.append("Using preemptive Shortest Job First")

    while time < run_for:
        # Check and log all arrivals at the current time
        for p in processes:
            if p.arrival == time and p.name not in arrived:
                output.append(f"Time {time} : {p.name} arrived")
                arrived.add(p.name)

        # Get available processes
        available = [p for p in queue if p.arrival <= time and p.remaining_burst > 0]
        
        if available:
            # Select the process with the shortest remaining burst
            selected = min(available, key=lambda p: p.remaining_burst)

            # Only log selection and set response time on the first burst
            if selected != current_process:
                output.append(f"Time {time} : {selected.name} selected (burst {selected.remaining_burst})")
                current_process = selected
                
                # Set response time only if it hasn't been set before
                if selected.response_time == -1:
                    selected.response_time = time - selected.arrival

            # Execute the process for one time unit
            selected.remaining_burst -= 1
            time += 1

            # Check and log any new arrivals during execution
            for p in processes:
                if p.arrival == time and p.name not in arrived:
                    output.append(f"Time {time} : {p.name} arrived")
                    arrived.add(p.name)

            # If the process finishes, log it and clear the current process
            if selected.remaining_burst == 0:
                selected.turnaround_time = time - selected.arrival
                selected.wait_time = selected.turnaround_time - selected.burst
                output.append(f"Time {time} : {selected.name} finished")
                current_process = None  # Clear to allow new selection
        else:
            output.append(f"Time {time} : Idle")
            time += 1

    output.append(f"Finished at time {run_for}")
    for p in processes:
        output.append(f"{p.name} wait {p.wait_time} turnaround {p.turnaround_time} response {p.response_time}")
    
    return output

def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler.py <input file>")
        return

    input_file = sys.argv[1]
    
    # Ensure the input file has a .in extension
    if not input_file.endswith(".in"):
        print("Error: Input file must have a .in extension")
        return

    # Replace .in with .out for output filename
    output_file = input_file.replace(".in", ".out")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    processes = []
    run_for = 0
    algorithm = ""
    quantum = 0
    
    for line in lines:
        parts = line.split()
        if parts[0] == "processcount":
            pass
        elif parts[0] == "runfor":
            run_for = int(parts[1])
        elif parts[0] == "use":
            algorithm = parts[1]
        elif parts[0] == "quantum":
            quantum = int(parts[1])
        elif parts[0] == "process":
            name = parts[2]
            arrival = int(parts[4])
            burst = int(parts[6])
            processes.append(Process(name, arrival, burst))
    
    if algorithm == "fcfs":
        output = fcfs_scheduling(processes, run_for)
    elif algorithm == "rr":
        if quantum == 0:
            print("Error: Quantum must be specified for Round-Robin scheduling")
            return
        output = rr_scheduling(processes, run_for, quantum)
    elif algorithm == "sjf":
        output = sjf_scheduling(processes, run_for)
    else:
        print("Error: Unsupported scheduling algorithm")
        return

    # Write output to .out file
    with open(output_file, 'w') as f:
        for line in output:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
