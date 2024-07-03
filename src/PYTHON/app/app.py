import streamlit as st
from data_loader import carregar_e_tratar_dados
from database_handler import inserir_dados
import yaml

# ---  Configuração de Cores ---

st.set_page_config(
    page_title="Carga de Dados",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="src\\PYTHON\\app\\image\\Green_Logo.png",
    menu_items=None
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #98FB98;
        color: white;
    }
    .stButton button {
        background-color: #FFFFE0;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("src\\PYTHON\\app\\image\\Green_Logo.png", width=64)
st.sidebar.title("Instruções para o uso do Aplicativo")
st.sidebar.write("Bem-vindo ao nosso aplicativo de upload de dados!")
st.sidebar.markdown("Instruções:")
st.sidebar.markdown("- Selecione a estação desejada.")
st.sidebar.markdown("- Carregue o arquivo CSV com os dados.")
st.sidebar.markdown("- Clique em 'Inserir Dados' para adicionar os dados ao banco.")
st.sidebar.markdown("- Confirme a inserção para finalizar o processo.")

mysql_config = {
    'user': 'root',
    'password': '75221139',
    'host': 'localhost',
    'database': 'DW_ESTACOES_GREEN'
}

def pagina_upload():
    estacoes = ["GIRASSOL", "COLMEIA"]
    estacao_selecionada = st.selectbox("Selecione a estação:", estacoes, key="estacao_selectbox_upload")
    uploaded_file = st.file_uploader("Carregue seu arquivo CSV", type=["csv"], key="file_uploader_upload")



    if st.button("Inserir Dados", key="inserir_dados_button"):
        if uploaded_file is not None:
            try:
                df, erro = carregar_e_tratar_dados(uploaded_file, estacao_selecionada)

                if erro is None:
                    st.dataframe(df)

                    inserir_dados(df, mysql_config)
                    st.success(f"Dados da estação {estacao_selecionada} inseridos com sucesso!")
                    
                else:
                    st.error(erro)
            except Exception as e:
                st.error(f"Erro ao carregar os dados: {e}")
        else:
            st.warning("Por favor, carregue um arquivo CSV antes de inserir os dados.")

st.title("Carga de Dados")

with open("src\\PYTHON\\app\\config.yaml") as file:
    config = yaml.safe_load(file)

pagina_upload()
