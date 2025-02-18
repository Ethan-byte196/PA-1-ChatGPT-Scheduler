import sys

# Class representing a process with necessary attributes
class Process:
    def __init__(self, name, arrival, burst):
        self.name = name  # Process name
        self.arrival = arrival  # Arrival time of the process
        self.burst = burst  # Total burst time needed
        self.remaining_time = burst  # Time left to complete execution
        self.start_time = -1  # When the process starts execution
        self.completion_time = -1  # When the process finishes execution
        self.waiting_time = 0  # Total waiting time before execution
        self.turnaround_time = 0  # Total turnaround time (completion - arrival)
        self.response_time = -1  # Time from arrival to first execution

# Function to read and parse the input file
def read_input_file(filename):
    processes = []  # List to store process objects
    scheduling_algorithm = None  # Type of scheduling algorithm
    quantum = None  # Time slice for Round Robin (if applicable)
    total_time = None  # Total time for simulation
    
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            
            for line in lines:
                tokens = line.split()
                if tokens[0] == 'processcount':
                    process_count = int(tokens[1])  # Number of processes
                elif tokens[0] == 'runfor':
                    total_time = int(tokens[1])  # Total execution time
                elif tokens[0] == 'use':
                    scheduling_algorithm = tokens[1]  # Scheduling algorithm
                elif tokens[0] == 'quantum':
                    quantum = int(tokens[1])  # Time quantum for Round Robin
                elif tokens[0] == 'process':
                    name = tokens[2]  # Process name
                    arrival = int(tokens[4])  # Arrival time
                    burst = int(tokens[6])  # Burst time
                    processes.append(Process(name, arrival, burst))
                elif tokens[0] == 'end':
                    break  # End of file processing
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid numeric value in input file.")
        sys.exit(1)
    
    # Validate Round Robin scheduling requires a quantum
    if scheduling_algorithm == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)
    
    return processes, scheduling_algorithm, quantum, total_time

# Round Robin scheduling algorithm
def rr_scheduler(processes, total_time, quantum):
    time = 0  # Current time in simulation
    log = []  # Store execution log
    queue = sorted(processes, key=lambda p: p.arrival)  # Sort by arrival time
    ready_queue = []  # Ready queue for RR
    completed_processes = []  # Track completed processes
    
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
            
            for process in queue:
                if process.arrival <= time and process not in ready_queue and process.remaining_time > 0:
                    ready_queue.append(process)
            
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            else:
                current_process.completion_time = time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival
                current_process.waiting_time = current_process.turnaround_time - current_process.burst
                completed_processes.append(current_process)
                log.append(f"Time {time} : {current_process.name} finished")
        else:
            log.append(f"Time {time} : Idle")
            time += 1
    
    return log, queue

# Function to write output to file with correct formatting
def write_output_file(filename, log, processes, scheduling_algorithm, quantum=None):
    output_filename = filename.replace('.in', '.out')  # Change extension to .out
    with open(output_filename, 'w') as file:
        file.write(f"  {len(processes)} processes\n")  # Indented number of processes
        file.write(f"Using {scheduling_algorithm.replace('rr', 'Round-Robin')}\n")  # Correct spacing and format
        if quantum:
            file.write(f"Quantum   {quantum}\n\n")  # Proper spacing for quantum
        for entry in log:
            file.write(entry.replace("Time", "Time   ") + "\n")  # Adjust spacing
        file.write(f"Finished at time  {log[-1].split()[1]}\n\n")  # Properly spaced finishing time
        for p in processes:
            file.write(f"{p.name} wait   {p.waiting_time} turnaround  {p.turnaround_time} response   {p.response_time}\n")  # Proper spacing

# Main function to handle program execution
def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not filename.endswith('.in'):
        print("Error: Input file must have a .in extension")
        sys.exit(1)
    
    processes, scheduling_algorithm, quantum, total_time = read_input_file(filename)
    
    if scheduling_algorithm == 'fcfs':
        log, processes = fcfs_scheduler(processes, total_time)
    elif scheduling_algorithm == 'rr':
        log, processes = rr_scheduler(processes, total_time, quantum)
    else:
        print("Error: Unsupported scheduling algorithm")
        sys.exit(1)
    
    write_output_file(filename, log, processes, scheduling_algorithm, quantum)  # Write results

if __name__ == "__main__":
    main()
