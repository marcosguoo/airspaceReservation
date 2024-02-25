import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

transactions_file = 'dailyTransactions3.csv'
network_utilization_file = 'export-NetworkUtilization3.csv'

transactions_data = pd.read_csv(transactions_file)
network_utilization_data = pd.read_csv(network_utilization_file)

transactions_data['Date(UTC)'] = pd.to_datetime(transactions_data['Date(UTC)'])
network_utilization_data['Date(UTC)'] = pd.to_datetime(network_utilization_data['Date(UTC)'])

merged_data = pd.merge(transactions_data, network_utilization_data, on='Date(UTC)', suffixes=('_tx', '_nu'))

merged_data.rename(columns={'Value_tx': 'Daily Transaction Count', 'Value_nu': 'Network Utilization'}, inplace=True)

merged_data['Network Utilization'] = merged_data['Network Utilization'].replace(0, 0.0001) 

merged_data['Max TPS'] = merged_data['Daily Transaction Count'] / (86400 * merged_data['Network Utilization'])

mean_tps = merged_data['Max TPS'].mean()

print(f"A média do TPS para todo o período dos dados é: {mean_tps}")