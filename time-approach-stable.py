import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Drone:
    def __init__(self, id, start, end, departure_time):
        self.id = id
        self.start = start
        self.end = end
        self.departure_time = departure_time
        self.path = self.calculate_path()
        self.current_position = start

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
    
    def move(self, time_step):
        if time_step >= self.departure_time and (time_step - self.departure_time) < len(self.path):
            self.current_position = self.path[time_step - self.departure_time]

def initialize_drones(grid_size, n_drones, departure_interval):
    drones = []
    for i in range(n_drones):
        start = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        end = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        departure_time = i // departure_interval
        drone = Drone(i+1, start, end, departure_time)
        drones.append(drone)
        distance = len(drone.calculate_path())-1
        print(f"Drone {drone.id}: Starting point {start}, Ending point {end}, Blocks to travel: {distance}, Departure at time step {drone.departure_time}")
    return drones

def simulate_step_with_paths(drones, time_step, grid_size):
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    path_positions = {}

    for drone in drones:
        for pos in drone.path:
            if pos in path_positions:
                path_positions[pos].append(drone.id)
            else:
                path_positions[pos] = [drone.id]

    for (x, y), drone_ids in path_positions.items():
        if len(drone_ids) > 1:
            grid[y][x] = 'X'
        else:
            grid[y][x] = str(drone_ids[0])

    return grid

def run_simulation(grid_size, n_drones, total_time_steps, departure_rate):
    drones = initialize_drones(grid_size, n_drones, departure_rate)
    for time_step in range(total_time_steps):
        print(f"Time step {time_step}:")
        grid = simulate_step_with_paths(drones, time_step, grid_size)
    

def draw_drone_paths(drones, grid_size):
    fig, ax = plt.subplots()
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks(range(grid_size+1))
    ax.set_yticks(range(grid_size+1))
    ax.grid(True)

    for drone in drones:
        x_coords, y_coords = zip(*drone.path)

        ax.plot(x_coords, y_coords, marker='o', label=f"Drone {drone.id}")
        
        ax.scatter(*drone.start, color='green', zorder=5)
        ax.scatter(*drone.end, color='red', zorder=5)

    ax.legend()
    plt.show()

grid_size = 78
n_drones = 15
total_time_steps = 20
departure_rate = 3

run_simulation(grid_size, n_drones, total_time_steps, departure_rate)
drones = initialize_drones(grid_size, n_drones, departure_rate)
draw_drone_paths(drones, grid_size)