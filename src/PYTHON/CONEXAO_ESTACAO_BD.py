# %%
import pandas as pd
import mysql.connector

# %%
# Dados de conexão com o MySQL
mysql_config = {
    'user': 'root',
    'password': '75221139',
    'host': 'localhost',
    'database': 'DW_ESTACOES_GREEN'
}

# %%
# Dados de conexão com o MySQL
mysql_config = {
    'user': 'root',
    'password': '75221139',
    'host': 'localhost',
    'database': 'DW_ESTACOES_GREEN'
}

# %%
# Caminho para o arquivo CSV
dados_csv = 'degradação_Public.csv'

# %%
# Ler os dados do CSV com Pandas
df = pd.read_csv(dados_csv)

# %%
# Conectar ao banco de dados MySQL
cnx = mysql.connector.connect(**mysql_config)
cursor = cnx.cursor()

# %%
df.head()

# %%
df.dtypes

# %%
# Adicionar a coluna 'nome_estacao' ao DataFrame
df['Nome_Estacao'] = 'Colmeia'

# %%
for index, row in df.iterrows():
    # 1. Tabela TEMPO:
    # Extrair data e hora
    datetime_obj = pd.to_datetime(row['Datetime'])
    ano = datetime_obj.year
    mes = datetime_obj.month
    dia = datetime_obj.day
    hora = datetime_obj.hour
    minuto = datetime_obj.minute

    # Verificar se o registro de tempo já existe
    cursor.execute("SELECT idTEMPO FROM DIM_TEMPO WHERE Ano = %s AND Mes = %s AND dia = %s AND Hora = %s AND Minuto = %s", (ano, mes, dia, hora, minuto))
    result = cursor.fetchone()

    if result:
        tempo_id = result[0]
    else:
        # Inserir novo registro na tabela TEMPO
        cursor.execute("INSERT INTO DIM_TEMPO (Ano, Mes, dia, Hora, Minuto) VALUES (%s, %s, %s, %s, %s)", (ano, mes, dia, hora, minuto))
        tempo_id = cursor.lastrowid
    
    
    # 2. Tabela DIM_ESTACAO:
    nome_estacao = row['Nome_Estacao']
    cursor.execute("SELECT idDIM_ESTACAO FROM DIM_ESTACAO WHERE nome = %s", (nome_estacao,))
    result = cursor.fetchone()

    if result:
        estacao_id = result[0]
    else:
        cursor.execute("INSERT INTO DIM_ESTACAO (nome) VALUES (%s)", (nome_estacao,))
        estacao_id = cursor.lastrowid
    
    
    # 3. Tabela DIM_VENTO:
    direcao_vento = row['Direcao_do_vento']

    cursor.execute("SELECT idDIM_VENTO FROM DIM_VENTO WHERE Direca_do_vento = %s", (direcao_vento,))
    result = cursor.fetchone()

    if result:
        vento_id = result[0]
    else:
        cursor.execute("INSERT INTO DIM_VENTO (Direca_do_vento) VALUES (%s)", (direcao_vento,))
        vento_id = cursor.lastrowid
    
    
     # 4. Tabela FATO_GREEN:
    # Verificar se o registro já existe (usando a chave composta)
    cursor.execute("""
        SELECT 1 
        FROM FATO_GREEN 
        WHERE TEMPO_idTEMPO = %s 
          AND DIM_ESTACAO_idDIM_ESTACAO = %s 
          AND DIM_VENTO_idDIM_VENTO = %s
    """, (tempo_id, estacao_id, vento_id))
    result = cursor.fetchone()

    if not result:  # Inserir apenas se o registro não existir
        cursor.execute("""
            INSERT INTO FATO_GREEN (
                Temperatura, Pressao_do_ar, Velocidade_do_vento, Precipitacao, PTemp_C, Umidade, BattV, TEMPO_idTEMPO, DIM_ESTACAO_idDIM_ESTACAO, DIM_VENTO_idDIM_VENTO
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Temperatura'], row['Pressao_do_ar'], row['Velocidade_do_vento'], row['Precipitacao'], 
            row['PTemp_C'], row['Umidade'], row['BattV'], tempo_id, estacao_id, vento_id
        ))


# %%
# Commitar as mudanças no banco de dados
cnx.commit()

# Fechar a conexão
cursor.close()
cnx.close()


