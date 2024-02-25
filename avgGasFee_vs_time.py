import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the dataset from the uploaded CSV file
df = pd.read_csv('sepolias.csv')

# Convert Unix timestamps to human-readable dates
df['date_time'] = pd.to_datetime(df['block_time'], unit='s')

# Convert Wei to Ether for average gas price (1 Ether = 1e18 Wei)
df['average_gas_fee_ether'] = df['average_gas_price'] / 1e18

# Set the start time for the plot - for example, start at 06:00 on the efirst date in the dataset
start_time = df['date_time'].dt.normalize() + pd.DateOffset(hours=11)

# Ensure the data starts from the defined start time
df = df[df['date_time'] >= start_time.iloc[0]]

# Plotting
plt.figure(figsize=(24, 12))
plt.plot(df['date_time'], df['average_gas_fee_ether'], marker='o', linestyle='-')

# Formatting the plot
plt.title('Average Gas Fee Over Time')
plt.xlabel('Time (24h format)')
plt.ylabel('Average Gas Fee (in Wei)')
plt.grid(True)

# Setting the x-axis major locator to hour locator and formatter to 24-hour format
plt.gca().xaxis.set_major_locator(mdates.HourLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Hh'))

# Limiting the x-axis to show only the 24 hours range from the start time
plt.xlim(start_time.iloc[0], start_time.iloc[0] + pd.Timedelta(hours=24))

# Show the plot
plt.show()
