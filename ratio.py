import random
import csv

class Agent:
    def __init__(self, start, end, id):
        self.start = start
        self.end = end
        self.path = None
        self.id = id

def create_grid(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def generate_random_points(grid_size, n):
    points = []
    for _ in range(n):
        start = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        end = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        points.append((start, end))
    return points

def simple_pathfinding(start, end, grid):
    path = [start]
    x, y = start
    while x != end[0]:
        x += 1 if x < end[0] else -1
        if grid[x][y] == 0:
            path.append((x, y))
        else:
            return None
    while y != end[1]:
        y += 1 if y < end[1] else -1
        if grid[x][y] == 0:
            path.append((x, y))
        else:
            return None
    return path

def simulate_bidding(grid, agents):
    for agent in agents:
        path = simple_pathfinding(agent.start, agent.end, grid)
        if path:
            for point in path:
                grid[point[0]][point[1]] = agent.id
            agent.path = path

def run_simulation(grid_size, n_agents):
    grid = create_grid(grid_size)
    points = generate_random_points(grid_size, n_agents)
    agents = [Agent(start, end, id+1) for id, (start, end) in enumerate(points)]

    simulate_bidding(grid, agents)

    successful_bidders = [agent for agent in agents if agent.path is not None]
    failed_bidders = [agent for agent in agents if agent.path is None]

    total_blocks_traveled = sum(len(agent.path) for agent in successful_bidders)
    successful_bids = len(successful_bidders)  # Number of successful bids
    total_bids = n_agents  # Total number of bids is the same as the number of agents
    percentage_successful = round((successful_bids / total_bids) * 100, 2) if total_bids > 0 else 0.0


    return grid_size, n_agents, total_blocks_traveled, len(failed_bidders), successful_bids, total_bids, percentage_successful

def simulate_for_ratio(max_agent_to_segment_ratio, simulations_per_ratio):
    results = []
    for i in range(simulations_per_ratio):
        grid_size = random.randint(78, 390)  # 78 = 1km block size; 390 = 100m block size
        total_segments = grid_size ** 2
        # max_agents = int(total_segments * max_agent_to_segment_ratio)

        n_agents = int(grid_size * max_agent_to_segment_ratio) 

        result = run_simulation(grid_size, n_agents)
        results.append(result)

        # Print statement indicating completion of each simulation run
        print(f"Simulation {i + 1}/{simulations_per_ratio} completed (Ratio: {max_agent_to_segment_ratio}, Grid Size: {grid_size}, Agents: {n_agents})")

    return results

def main():
    ratio_range = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]  # Define a range of ratios to test
    simulations_per_ratio = 100  # Number of simulations to run for each ratio

    all_results = []
    for ratio in ratio_range:
        ratio_results = simulate_for_ratio(ratio, simulations_per_ratio)
        for result in ratio_results:
            all_results.append((ratio,) + result)  # Adding the ratio to the result tuple

    # Writing results to CSV
    with open('simulation_results_ratios.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ratio', 'Grid Size', 'Number of Agents', 'Total Blocks Traveled', 'Number of Failed Bids', 'Successful Number of Bids', 'Total Bids', 'Successful Bids Percentage'])
        writer.writerows(all_results)

if __name__ == "__main__":
    main()
