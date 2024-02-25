import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Função para calcular métricas de dispersão
def calcular_metricas(df, x, y):
    media_x = np.mean(df[x])
    media_y = np.mean(df[y])
    desvio_padrao_x = np.std(df[x])
    desvio_padrao_y = np.std(df[y])
    variancia_x = np.var(df[x])
    variancia_y = np.var(df[y])
    coef_variacao_x = np.std(df[x]) / np.mean(df[x])
    coef_variacao_y = np.std(df[y]) / np.mean(df[y])
    iqr_x = np.subtract(*np.percentile(df[x], [75, 25]))
    iqr_y = np.subtract(*np.percentile(df[y], [75, 25]))
    
    return {
        'media_x': media_x,
        'media_y': media_y,
        'desvio_padrao_x': desvio_padrao_x,
        'desvio_padrao_y': desvio_padrao_y,
        'variancia_x': variancia_x,
        'variancia_y': variancia_y,
        'coef_variacao_x': coef_variacao_x,
        'coef_variacao_y': coef_variacao_y,
        'iqr_x': iqr_x,
        'iqr_y': iqr_y
    }

# Caminho dos arquivos CSV
file_path_gas_price = 'export-AvgGasPrice3.csv'
file_path_block_time = 'export-BlockTime3.csv'

# Leitura dos dados
data_gas_price = pd.read_csv(file_path_gas_price)
data_block_time = pd.read_csv(file_path_block_time)

# Fusão dos datasets utilizando 'UnixTimeStamp' como chave
merged_data = pd.merge(data_gas_price, data_block_time, on='UnixTimeStamp', suffixes=('_gas', '_block'))

# Renomeando as colunas para clareza
merged_data.rename(columns={'Value (Wei)': 'AvgGasPrice', 'Value': 'BlockTime'}, inplace=True)

# Calculando as métricas
metricas = calcular_metricas(merged_data, 'AvgGasPrice', 'BlockTime')

# Saída das métricas
for metrica, valor in metricas.items():
    print(f"{metrica}: {valor}")

# Plotagem
plt.figure(figsize=(10, 6))
sns.scatterplot(x='AvgGasPrice', y='BlockTime', data=merged_data, color='black')
plt.xlabel('Preço médio de Gas Fee (Wei)')
plt.ylabel('Tempo de inclusão de um bloco na rede (segundos)')

# Calculando e plotando a linha de regressão
m, b = np.polyfit(merged_data['AvgGasPrice'], merged_data['BlockTime'], 1)
plt.plot(merged_data['AvgGasPrice'], m * merged_data['AvgGasPrice'] + b, color='black')

plt.show()