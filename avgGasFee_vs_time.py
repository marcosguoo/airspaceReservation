import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('sepolias.csv')

df['date_time'] = pd.to_datetime(df['block_time'], unit='s')

df['average_gas_fee_ether'] = df['average_gas_price'] / 1e18

start_time = df['date_time'].dt.normalize() + pd.DateOffset(hours=11)

df = df[df['date_time'] >= start_time.iloc[0]]

plt.figure(figsize=(24, 12))
plt.plot(df['date_time'], df['average_gas_fee_ether'], marker='o', linestyle='-')

plt.title('Average Gas Fee Over Time')
plt.xlabel('Time (24h format)')
plt.ylabel('Average Gas Fee (in Wei)')
plt.grid(True)

plt.gca().xaxis.set_major_locator(mdates.HourLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Hh'))

plt.xlim(start_time.iloc[0], start_time.iloc[0] + pd.Timedelta(hours=24))

plt.show()
