import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Carregar o dataset
df = pd.read_csv('export-NetworkUtilization.csv')  # Substitua pelo caminho correto do arquivo CSV

# Converter 'Date (UTC)' para datetime
df['Date(UTC)'] = pd.to_datetime(df['Date(UTC)'])

# Plotting using matplotlib to create a line plot
plt.figure(figsize=(14, 7))

# Plot line for 'Value' which represents network utilization
plt.plot(df['Date(UTC)'], df['Value'], color='black', linewidth=0.8)

# Formatting the x-axis to display annual ticks
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
# Highlighting specific dates with different colors
plt.axvline(pd.to_datetime('2021-08-05'), color='green', linestyle='--', linewidth=2, label='London Fork')
plt.axvline(pd.to_datetime('2022-09-14'), color='blue', linestyle='--', linewidth=2, label='The Merge')

# Set the title and labels of the plot
plt.title('Utilização da Rede Ethereum ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Utilização da Rede')

# Improve readability of the plot
plt.gcf().autofmt_xdate()  # Auto-format the dates
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.5, color='gray')
plt.legend()  # Add a legend to highlight specific dates

# Show the plot
plt.show()
