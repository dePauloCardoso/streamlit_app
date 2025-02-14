import streamlit as st
import requests
import pandas as pd

# URL da sua API FastAPI
API_URL = "https://api-streamlit-7h4o.onrender.com"

# Função para consultar a API
def consultar_api(**kwargs):  # Aceita qualquer número de argumentos nomeados
    params = {}
    for key, value in kwargs.items():
        if value:
            params[key] = value
    response = requests.get(f"{API_URL}/produtos", params=params, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return None

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define a cor de fundo como '#282c34' (cinza escuro)
st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
        background-color: #161B33;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Exibe a imagem
st.sidebar.image("https://github.com/dePauloCardoso/streamlit_app/blob/main/Logo_SAE.png?raw=true")

# Interface Streamlit
st.sidebar.title("Consulta de Produtos")

# Inicializa session_state se não existir
if "filters" not in st.session_state:
    st.session_state["filters"] = {
        "cod_insersao": "",
        "cod_sku": "",
        "segmento": "",
        "serie": "",
        "envio": "",
        "usuario": "",
        "personalizacao": ""
    }

# Função para atualizar os filtros
def atualiza_filtros():
    st.session_state["filters"] = {
        "cod_insersao": st.session_state.cod_insersao,
        "cod_sku": st.session_state.cod_sku,
        "segmento": st.session_state.segmento,
        "serie": st.session_state.serie,
        "envio": st.session_state.envio,
        "usuario": st.session_state.usuario,
        "personalizacao": st.session_state.personalizacao
    }

# Campos de entrada para os filtros
cod_insersao = st.sidebar.text_input("Código de Inserção", key="cod_insersao", on_change=atualiza_filtros)
cod_sku = st.sidebar.text_input("Código SKU", key="cod_sku", on_change=atualiza_filtros)

# Dropdowns para os filtros
segmento_options = ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"]
segmento = st.sidebar.selectbox("Segmento", segmento_options, key="segmento", on_change=atualiza_filtros)

serie_options = ["", "INF I", "INF II", "INF III", "INF IV", "INF V", "1O ANO", "2O ANO", "3O ANO", "4O ANO", "5O ANO", "6O ANO", "7O ANO", "8O ANO", "9O ANO", "1A SERIE", "2A SERIE", "3A SERIE", "APROVA +", "ELETIVAS", "SEMI", "VARIOS"]
serie = st.sidebar.selectbox("Série", serie_options, key="serie", on_change=atualiza_filtros)

envio_options = ["", "V1", "V2", "V3", "V4"]
envio = st.sidebar.selectbox("Envio", envio_options, key="envio", on_change=atualiza_filtros)

usuario_options = ["", "Aluno", "Professor"]
usuario = st.sidebar.selectbox("Usuário", usuario_options, key="usuario", on_change=atualiza_filtros)

personalizacao_options = ["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER","DOM BOSCO", "DOM BOSCO BALSAS", "ELO", "FATO", "FILOMENA", "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR", "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", "ROSALVO", "SAE", "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"]
personalizacao = st.sidebar.selectbox("Personalização", personalizacao_options, key="personalizacao", on_change=atualiza_filtros)

# Botão para limpar os filtros
def limpar_filtros():
    for key in st.session_state["filters"]:
        st.session_state[key] = ""
    atualiza_filtros()

st.sidebar.button("Limpar Filtros", on_click=limpar_filtros)

# Consulta a API com os filtros
produtos = consultar_api(**st.session_state["filters"])

# Exibe os resultados em tabela
if produtos:
    df = pd.DataFrame(produtos)
    colunas_desejadas = ['cod_insersao', 'descricao_kit', 'cod_sku',
                         'descricao_sku', 'segmento', 'serie', 'volume', 'envio',
                         'frequencia', 'usuario', 'info_produto', 'tipo_material',
                         'classificacao_produto', 'personalizacao']
    df = df[colunas_desejadas]
    st.dataframe(df, use_container_width=True)
else:
    st.write("Nenhum produto encontrado para estes filtros.")
