import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('export-NetworkUtilization.csv')

df['Date(UTC)'] = pd.to_datetime(df['Date(UTC)'])

plt.figure(figsize=(14, 7))

plt.plot(df['Date(UTC)'], df['Value'], color='black', linewidth=0.8)

plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
plt.axvline(pd.to_datetime('2021-08-05'), color='green', linestyle='--', linewidth=2, label='London Fork')
plt.axvline(pd.to_datetime('2022-09-14'), color='blue', linestyle='--', linewidth=2, label='The Merge')

plt.title('Utilização da Rede Ethereum ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Utilização da Rede')

plt.gcf().autofmt_xdate()
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.5, color='gray')
plt.legend()

plt.show()
