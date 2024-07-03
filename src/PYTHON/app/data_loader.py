# data_loader.py
import pandas as pd

# Função para carregar e tratar os dados do CSV
def carregar_e_tratar_dados(arquivo_csv, nome_estacao):
    try:
        df = pd.read_csv(arquivo_csv, skiprows=1)
        df = df.iloc[2:]
        df['Nome_Estacao'] = nome_estacao
        return df, None  # Retorne None para a mensagem de erro se não houver erro
    except Exception as e:
        return None, f"Erro ao carregar os dados: {e}"  # Retorne None para o DataFrame se houver erro