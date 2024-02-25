import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the CSV files
transactions_file = 'dailyTransactions3.csv'  # Update with the actual file path
network_utilization_file = 'export-NetworkUtilization3.csv'  # Update with the actual file path

# Read the data
transactions_data = pd.read_csv(transactions_file)
network_utilization_data = pd.read_csv(network_utilization_file)

# Convert 'Date(UTC)' to datetime for easy merging
transactions_data['Date(UTC)'] = pd.to_datetime(transactions_data['Date(UTC)'])
network_utilization_data['Date(UTC)'] = pd.to_datetime(network_utilization_data['Date(UTC)'])

# Merge the two datasets on 'Date(UTC)'
merged_data = pd.merge(transactions_data, network_utilization_data, on='Date(UTC)', suffixes=('_tx', '_nu'))

# Rename columns for clarity
merged_data.rename(columns={'Value_tx': 'Daily Transaction Count', 'Value_nu': 'Network Utilization'}, inplace=True)

merged_data['Network Utilization'] = merged_data['Network Utilization'].replace(0, 0.0001) 

# Calculate the maximum TPS
merged_data['Max TPS'] = merged_data['Daily Transaction Count'] / (86400 * merged_data['Network Utilization'])

mean_tps = merged_data['Max TPS'].mean()

print(f"A média do TPS para todo o período dos dados é: {mean_tps}")