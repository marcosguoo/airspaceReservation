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

# Carregando os arquivos CSV
file_path_gas_limit = 'export-GasLimit.csv'
file_path_transaction_count = 'export-TxGrowth.csv'

data_gas_limit = pd.read_csv(file_path_gas_limit)
data_transaction_count = pd.read_csv(file_path_transaction_count)

# Convertendo 'Date(UTC)' para o formato de data em ambos os DataFrames
data_gas_limit['Date(UTC)'] = pd.to_datetime(data_gas_limit['Date(UTC)'])
data_transaction_count['Date(UTC)'] = pd.to_datetime(data_transaction_count['Date(UTC)'])

# Renomeando as colunas para clareza
data_gas_limit.rename(columns={'Value': 'GasLimit'}, inplace=True)
data_transaction_count.rename(columns={'Value': 'DailyTransactionCount'}, inplace=True)

# Fusão dos datasets utilizando 'Date(UTC)' como chave
merged_data = pd.merge(data_gas_limit, data_transaction_count, on='Date(UTC)')

# Calculando as métricas
metricas = calcular_metricas(merged_data, 'GasLimit', 'DailyTransactionCount')

# Saída das métricas
for metrica, valor in metricas.items():
    print(f"{metrica}: {valor}")

# Plotagem
plt.figure(figsize=(10, 6))
sns.scatterplot(x='GasLimit', y='DailyTransactionCount', data=merged_data, color='black')
plt.xlabel('Gas Limit')
plt.ylabel('Contagem de Transações Diárias')

# Calculando e plotando a linha de regressão
m, b = np.polyfit(merged_data['GasLimit'], merged_data['DailyTransactionCount'], 1)
plt.plot(merged_data['GasLimit'], m * merged_data['GasLimit'] + b, color='black')

plt.show()
