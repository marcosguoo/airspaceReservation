import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('simulation_results_ratios.csv')

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(data['Ratio'], data['Total Blocks Traveled'], alpha=0.5, c='black')
plt.title('Total Blocks Traveled vs. Ratio')
plt.xlabel('Ratio (Agent-to-Segment)')
plt.ylabel('Total Blocks Traveled')
plt.grid(True)
plt.show()
