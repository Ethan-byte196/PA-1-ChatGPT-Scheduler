import sys
import os

# Class representing a process with necessary attributes
class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.start_time = -1
        self.completion_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1

# Function to read and parse the input file
def read_input_file(filename):
    processes = []
    scheduling_algorithm = None
    quantum = None
    total_time = None
    
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            
            for line in lines:
                tokens = line.split()
                if tokens[0] == 'processcount':
                    process_count = int(tokens[1])
                elif tokens[0] == 'runfor':
                    total_time = int(tokens[1])
                elif tokens[0] == 'use':
                    scheduling_algorithm = tokens[1]
                elif tokens[0] == 'quantum':
                    quantum = int(tokens[1])
                elif tokens[0] == 'process':
                    name = tokens[2]
                    arrival = int(tokens[4])
                    burst = int(tokens[6])
                    processes.append(Process(name, arrival, burst))
                elif tokens[0] == 'end':
                    break
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid numeric value in input file.")
        sys.exit(1)
    
    if scheduling_algorithm == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)
    
    return processes, scheduling_algorithm, quantum, total_time

# First-Come, First-Served (FCFS) scheduling algorithm
def fcfs_scheduler(processes, total_time):
    time = 0
    log = []
    queue = sorted(processes, key=lambda p: p.arrival)
    
    for process in queue:
        if time < process.arrival:
            log.append(f"Time {time} : Idle")
            time = process.arrival
        log.append(f"Time {time} : {process.name} selected (burst {process.burst})")
        process.start_time = time
        process.response_time = time - process.arrival
        time += process.burst
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival
        process.waiting_time = process.turnaround_time - process.burst
        log.append(f"Time {time} : {process.name} finished")
    
    return log, processes

# Preemptive Shortest Job First (SJF) scheduling algorithm
def sjf_scheduler(processes, total_time):
    time = 0
    log = []
    ready_queue = []
    processes = sorted(processes, key=lambda p: (p.arrival, p.burst))
    
    while time < total_time:
        for process in processes:
            if process.arrival == time:
                log.append(f"Time {time} : {process.name} arrived")
                ready_queue.append(process)
                ready_queue.sort(key=lambda p: p.remaining_time)
        
        if ready_queue:
            current_process = ready_queue.pop(0)
            if current_process.start_time == -1:
                current_process.start_time = time
                current_process.response_time = time - current_process.arrival
            
            log.append(f"Time {time} : {current_process.name} selected (burst {current_process.remaining_time})")
            current_process.remaining_time -= 1
            time += 1
            
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
                ready_queue.sort(key=lambda p: p.remaining_time)
            else:
                log.append(f"Time {time} : {current_process.name} finished")
                current_process.completion_time = time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival
                current_process.waiting_time = current_process.turnaround_time - current_process.burst
        else:
            log.append(f"Time {time} : Idle")
            time += 1
    
    return log, processes

# Round Robin scheduling algorithm
def rr_scheduler(processes, total_time, quantum):
    time = 0
    log = []
    queue = sorted(processes, key=lambda p: p.arrival)
    ready_queue = []
    
    while time < total_time:
        for process in queue:
            if process.arrival == time:
                log.append(f"Time {time} : {process.name} arrived")
                ready_queue.append(process)
        
        if ready_queue:
            current_process = ready_queue.pop(0)
            if current_process.start_time == -1:
                current_process.start_time = time
                current_process.response_time = time - current_process.arrival
            
            execute_time = min(quantum, current_process.remaining_time)
            log.append(f"Time {time} : {current_process.name} selected (burst {current_process.remaining_time})")
            current_process.remaining_time -= execute_time
            time += execute_time
            
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            else:
                log.append(f"Time {time} : {current_process.name} finished")
                current_process.completion_time = time
                current_process.turnaround_time = time - current_process.arrival
                current_process.waiting_time = current_process.turnaround_time - current_process.burst
        else:
            log.append(f"Time {time} : Idle")
            time += 1
    
    return log, processes

# Function to write output to file
def write_output_file(filename, log, processes, scheduling_algorithm, quantum=None):
    output_filename = filename.replace('.in', '.out')
    with open(output_filename, 'w') as file:
        file.write(f"  {len(processes)} processes\n")
        file.write(f"Using {scheduling_algorithm.replace('rr', 'Round-Robin').replace('sjf', 'preemptive Shortest Job First')}\n")
        if quantum:
            file.write(f"Quantum   {quantum}\n\n")
        for entry in log:
            file.write(entry.replace("Time", "Time   ") + "\n")
        file.write(f"Finished at time  {log[-1].split()[1]}\n\n")
        for p in processes:
            file.write(f"{p.name} wait   {p.waiting_time} turnaround  {p.turnaround_time} response   {p.response_time}\n")

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    processes, scheduling_algorithm, quantum, total_time = read_input_file(filename)
    
    if scheduling_algorithm == 'fcfs':
        log, processes = fcfs_scheduler(processes, total_time)
    elif scheduling_algorithm == 'sjf':
        log, processes = sjf_scheduler(processes, total_time)
    elif scheduling_algorithm == 'rr':
        log, processes = rr_scheduler(processes, total_time, quantum)
    else:
        print("Error: Unsupported scheduling algorithm")
        sys.exit(1)
    
    write_output_file(filename, log, processes, scheduling_algorithm, quantum)

if __name__ == "__main__":
    main()