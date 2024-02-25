import csv
import random
import os
import matplotlib.pyplot as plt
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

detour_logs = []

class Drone:
    def __init__(self, id, start, end, departure_time):
        self.id = id
        self.start = start
        self.end = end
        self.departure_time = departure_time
        self.path = self.calculate_path()
        self.position = start
        self.completed = False
        self.distance_traveled = 0
        self.collided = False
        self.time_steps = []
        self.collision_time_step = None

    def find_alternative_path(self, matrix, start, end, blocked_positions):
        """
        Finds an alternative path using the A* algorithm, avoiding the blocked positions.
        :param matrix: The grid matrix representing the map.
        :param start: The starting tuple coordinates (x, y).
        :param end: The ending tuple coordinates (x, y).
        :param blocked_positions: A set of tuples representing blocked coordinates.
        :return: A tuple containing the new path as a list of tuples and the additional distance as an integer.
        """

        for pos in blocked_positions:
            matrix[pos[1]][pos[0]] = 1

        grid = Grid(matrix=matrix)
        start_node = grid.node(start[0], start[1])
        end_node = grid.node(end[0], end[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

        path, _ = finder.find_path(start_node, end_node, grid)
        
        path_tuples = [(node.x, node.y) for node in path]

        additional_distance = len(path_tuples) - (abs(end[0] - start[0]) + abs(end[1] - start[1]))

        return path_tuples, additional_distance

    def get_data(self):
        return {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'completed': self.completed,
            'collided': self.collided,
            'distance_traveled': self.distance_traveled,
            'time_steps': self.time_steps
        }

    def calculate_path(self):
        path = [self.start]
        x, y = self.start
        x_end, y_end = self.end

        while (x, y) != (x_end, y_end):
            if x < x_end:
                x += 1
            elif x > x_end:
                x -= 1

            if y < y_end:
                y += 1
            elif y > y_end:
                y -= 1

            path.append((x, y))

        return path

    def calculate_next_position(self):
        current_index = self.path.index(self.position)
        if current_index < len(self.path) - 1:
            return self.path[current_index + 1]
        return self.position
    
    def need_to_detour(self, next_position, grid, other_drones):
        if next_position in grid: 
            blocking_drone = next((d for d in other_drones if d.position == next_position and d.id != self.id), None)
            if blocking_drone and blocking_drone.departure_time < self.departure_time:
                return True
        return False

    def move(self, simulation_time, grid, other_drones):
        global detour_logs
        if self.collided or self.completed:
            return

        if simulation_time < self.departure_time:
            return

        next_position = self.calculate_next_position()
        if grid[next_position[1]][next_position[0]] != '.':
            blocking_drone = next((d for d in other_drones if d.position == next_position and d.id != self.id), None)
            if blocking_drone and blocking_drone.departure_time <= simulation_time:
                matrix = [[0 if cell == '.' else 1 for cell in row] for row in grid]
                blocked_positions = {(d.position[1], d.position[0]) for d in other_drones if d.id != self.id}
                new_path, additional_distance = self.find_alternative_path(matrix, self.position, self.end, blocked_positions)
                if new_path:
                    self.path = new_path
                    self.distance_traveled += additional_distance
                    detour_logs.append({
                        'drone_id': self.id,
                        'time_step': simulation_time,
                        'additional_blocks': additional_distance
                    })
                else:
                    self.collided = True
        else:
            self.position = next_position
            self.distance_traveled += 1
            self.time_steps.append(simulation_time)
            if self.position == self.end:
                self.completed = True
        
def is_peak_hour(time_step, steps_per_hour):
    hour = time_step // steps_per_hour
    if (11.5 <= hour < 14.5) or (18 <= hour < 21):
        return True
    return False

def get_normal_departure_time(total_time_steps, steps_per_hour, n_drones):
    departure_times = []

    peak_hours = [(11.5, 14.5), (18, 21)]
    peak_hours_in_steps = [(int(start * steps_per_hour), int(end * steps_per_hour)) for start, end in peak_hours]

    std_dev = steps_per_hour * 2

    while len(departure_times) < n_drones:
        peak_start, peak_end = random.choice(peak_hours_in_steps)
        peak_mean = (peak_start + peak_end) / 2

        time_step = int(np.random.normal(peak_mean, std_dev))

        time_step = max(0, min(time_step, total_time_steps - 1))

        if time_step not in departure_times:
            departure_times.append(time_step)

    return departure_times

def initialize_drones(grid_size, n_drones, total_time_steps, steps_per_hour):
    drones = []
    departure_times = get_normal_departure_time(total_time_steps, steps_per_hour, n_drones)
    
    for i in range(n_drones):
        start = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        end = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        
        if i < len(departure_times):
            departure_time = departure_times[i]
        else:
            break

        drone = Drone(i+1, start, end, departure_time)
        drones.append(drone)

    return drones

def simulate_step(drones, time_step, grid_size):
    global detour_logs
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    for drone in drones:
        if drone.departure_time <= time_step and not drone.collided:
            x, y = drone.position
            grid[y][x] = drone.id

    for drone in drones:
        if drone.departure_time <= time_step and not drone.completed and not drone.collided:
            next_position = drone.calculate_next_position()
            x, y = next_position
            if grid[y][x] != '.':
                other_drone_id = grid[y][x]
                if drones[other_drone_id - 1].departure_time <= time_step:
                    drone.collided = True
                    drones[other_drone_id - 1].collided = True
                    drone.collision_time_step = time_step
                else:
                    additional_distance = drone.find_alternative_path(grid, {d.position for d in drones if d.departure_time <= time_step})
                    detour_logs.append({
                        'drone_id': drone.id,
                        'time_step': time_step,
                        'additional_blocks': additional_distance
                    })
            else:
                drone.position = next_position
                drone.time_steps.append(time_step)
                drone.distance_traveled += 1
                if drone.position == drone.end:
                    drone.completed = True

max_simulation_step = 0
max_simulation_steps = []

max_steps_across_all_simulations = 0

def run_simulation(grid_size, n_drones, total_time_steps, percentage):
    global max_simulation_step
    total_departures_for_grid_size = 0
    simulation_time = 0
    steps_per_hour = 120
    lambda_peak = 0.5
    lambda_off_peak = 0.1

    drones = initialize_drones(grid_size, n_drones, total_time_steps, steps_per_hour)

    while not all(drone.completed or drone.collided for drone in drones):
        total_departures_for_grid_size = simulate_step(drones, simulation_time, grid_size)
        simulation_time += 1
    print(f"Total departures for grid size {grid_size} with {percentage}% drones: {n_drones}")
    max_simulation_step = simulation_time
    max_simulation_steps.append(max_simulation_step)
    
    successful_flights = len([d for d in drones if d.completed and not d.collided])
    failed_flights = len([d for d in drones if not d.completed or d.collided])
    total_distance = sum(d.distance_traveled for d in drones if d.completed and not d.collided)

    return drones, successful_flights, failed_flights, total_distance, max_simulation_step

each_total_steps = []

def export_detour_logs():
    global detour_logs
    filename = 'detours.csv'
    fieldnames = ['drone_id', 'time_step', 'additional_blocks']
    
    file_exists = os.path.exists(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(detour_logs)

def run_simulations_and_collect_data():
    global max_simulation_step, max_steps_across_all_simulations, max_simulation_steps, detour_logs

    grid_sizes = [10, 20, 34, 102, 205]
    drone_percentages = [i for i in range(50, 100, 10)]
    time_steps_per_grid_size = {10: 24 * 60, 20: 48 * 60, 34: 72 * 60, 102: 96 * 60, 205: 108 * 60}

    results = []
    all_drones = [] 

    for grid_size in grid_sizes:
        total_time_steps = time_steps_per_grid_size[grid_size]
        for percentage in drone_percentages:
            n_drones = int(grid_size * (percentage / 100))
            drones, successful_flights, failed_flights, total_distance, max_step_this_simulation = run_simulation(grid_size, n_drones, total_time_steps, percentage)
            all_drones.extend(drones)
            max_steps_across_all_simulations = max(max_steps_across_all_simulations, max_step_this_simulation)
            ts_hour = max_step_this_simulation / 24

            results.append([
                grid_size,
                percentage,
                n_drones,
                successful_flights / n_drones * 100 if n_drones > 0 else 0, 
                failed_flights / n_drones * 100 if n_drones > 0 else 0,
                total_distance,
                max_step_this_simulation,
                ts_hour
            ])

        each_total_steps.append(max_simulation_step)
        if detour_logs:
            export_detour_logs()
            detour_logs = []

    with open('simulation_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Grid Size', 'Ratio', 'Number of Drones', 'Percentage of Successful Flights', 'Percentage of Failed Flights', 'Total Distance Combined', 'Max Time Steps'])
        writer.writerows(results)

    return all_drones

def calculate_steps_per_hour(each_total_steps):
    steps_hour = []
    for steps in each_total_steps:
        steps_hour.append(steps / 24)

def count_drones_in_peak(departure_times, steps_per_hour):
    peak_start_1 = int(11.5 * steps_per_hour)
    peak_end_1 = int(14.5 * steps_per_hour)
    peak_start_2 = int(18 * steps_per_hour)
    peak_end_2 = int(21 * steps_per_hour)

    peak_departures = sum(peak_start_1 <= time_step < peak_end_1 or peak_start_2 <= time_step < peak_end_2 for time_step in departure_times)
    
    off_peak_departures = len(departure_times) - peak_departures

    return peak_departures, off_peak_departures

def create_histogram(hourly_successful, hourly_failed):
    calculate_steps_per_hour(each_total_steps)
    plt.figure(figsize=(12, 6))
    bins = np.arange(24)
    plt.bar(bins - 0.2, hourly_successful, width=0.4, color='green', label='Successful')
    plt.bar(bins + 0.2, hourly_failed, width=0.4, color='red', label='Failed')
    plt.xticks(bins, range(24))
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Flights')
    plt.legend()
    plt.show()

def plot_drones_departure(drones, steps_per_hour):
    departure_times = [drone.departure_time for drone in drones]
    drone_ids = [drone.id for drone in drones]
    departure_hours = [(time_step / steps_per_hour) % 24 for time_step in departure_times]

    sorted_drones = sorted(zip(departure_hours, drone_ids))
    departure_hours, drone_ids = zip(*sorted_drones)

    plt.figure(figsize=(12, 6))
    plt.scatter(departure_hours, drone_ids, alpha=0.6, marker='o')

    plt.xticks(np.arange(0, 24, 1), [f"{hour:02d}:00" for hour in range(24)], rotation=45)
    plt.xlabel('Horário')
    plt.ylabel('ID do Drone')
    plt.title('Horário de partida pelo ID do Drone')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

all_drones_from_simulations = run_simulations_and_collect_data()

def export_drones_data(drones):
    fieldnames = ['id', 'start', 'end', 'completed', 'collided', 'distance_traveled']
    with open('drones.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for drone in drones:
            drone_data = {
                'id': drone.id,
                'start': drone.start,
                'end': drone.end,
                'completed': drone.completed,
                'collided': drone.collided,
                'distance_traveled': drone.distance_traveled
            }
            writer.writerow(drone_data)

export_drones_data(all_drones_from_simulations)

steps_per_hour = 120
all_departure_times = [drone.departure_time for drone in all_drones_from_simulations]
peak_departures, off_peak_departures = count_drones_in_peak(all_departure_times, steps_per_hour)

print(f"Total drones departing during peak hours: {peak_departures}")
print(f"Total drones departing outside peak hours: {off_peak_departures}")

plot_drones_departure(all_drones_from_simulations, steps_per_hour=120)