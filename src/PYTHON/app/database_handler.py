# database_handler.py
import mysql.connector
import pandas as pd

# Função para inserir dados no banco de dados
def inserir_dados(df, mysql_config):
    # Conectar ao banco de dados MySQL
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()

    # Inserir dados na tabela FATO_GREEN
    for index, row in df.iterrows():
        # 1. Tabela TEMPO:
        datetime_obj = pd.to_datetime(row['TIMESTAMP'])
        ano = datetime_obj.year
        mes = datetime_obj.month
        dia = datetime_obj.day
        hora = datetime_obj.hour
        minuto = datetime_obj.minute

        # Verificar se o registro de tempo já existe
        cursor.execute("SELECT idTEMPO FROM DIM_TEMPO WHERE Ano = %s AND Mes = %s AND Dia = %s AND Hora = %s AND Minuto = %s", (ano, mes, dia, hora, minuto))
        result = cursor.fetchone()

        if result:
            tempo_id = result[0]
        else:
            # Inserir novo registro na tabela TEMPO
            cursor.execute("INSERT INTO DIM_TEMPO (Ano, Mes, Dia, Hora, Minuto) VALUES (%s, %s, %s, %s, %s)", (ano, mes, dia, hora, minuto))
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
        direcao_vento = row['WindDir']

        cursor.execute("SELECT idDIM_VENTO FROM DIM_VENTO WHERE WindDir = %s", (direcao_vento,))
        result = cursor.fetchone()

        if result:
            vento_id = result[0]
        else:
            cursor.execute("INSERT INTO DIM_VENTO (WindDir) VALUES (%s)", (direcao_vento,))
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
                    AirTC, Batt_Volt, BattV, Crnt_A, PTemp_C, piranometro_dif, Rain_mm, RH, Solar_KJ, Solar_Wm2, Tot24, WS_ms, TEMPO_idTEMPO, DIM_ESTACAO_idDIM_ESTACAO, DIM_VENTO_idDIM_VENTO
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['AirTC'], row['Batt_Volt'], row['BattV'], row['Crnt_A'],
                row['PTemp_C'], row['piranometro_dif'], row['Rain_mm'], row['RH'], row['Solar_KJ'], row['Solar_Wm2'], row['Tot24'], row['WS_ms'], tempo_id, estacao_id, vento_id
            ))

    # Commitar as mudanças no banco de dados
    cnx.commit()

    # Fechar a conexão
    cursor.close()
    cnx.close()