import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('simulation_results_ratios.csv')

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(data['Ratio'], data['Successful Bids Percentage'], alpha=0.5, c='black')
plt.title('Porcentagem de lances com sucesso vs. Razão de Agentes/Blocos')
plt.xlabel('Razão (Agentes/Blocos)')
plt.ylabel('Porcentagem de lances com sucesso')
plt.grid(True)
plt.show()
