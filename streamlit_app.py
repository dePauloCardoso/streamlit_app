import streamlit as st
import requests
import pandas as pd

# URL da sua API FastAPI
API_URL = "https://api-streamlit-7h4o.onrender.com"

# Função para consultar a API
def consultar_api(**kwargs):
    params = {key: value for key, value in kwargs.items() if value}
    response = requests.get(f"{API_URL}/produtos", params=params, verify=False)
    return response.json() if response.status_code == 200 else None

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Define a cor de fundo
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

st.sidebar.title("Consulta de Produtos")

# Inicializa os estados da sessão para filtros
if "segmento" not in st.session_state:
    st.session_state.segmento = ""
if "serie" not in st.session_state:
    st.session_state.serie = ""
if "cod_insersao" not in st.session_state:
    st.session_state.cod_insersao = ""
if "cod_sku" not in st.session_state:
    st.session_state.cod_sku = ""
if "envio" not in st.session_state:
    st.session_state.envio = ""
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "personalizacao" not in st.session_state:
    st.session_state.personalizacao = ""

# Opções de segmento
segmento_options = ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"]

# Mapeamento de séries por segmento
serie_dict = {
    "": [""],
    "INF": ["", "INF I", "INF II", "INF III", "INF IV", "INF V"],
    "FUND AI": ["", "1O ANO", "2O ANO", "3O ANO", "4O ANO", "5O ANO"],
    "FUND AF": ["", "6O ANO", "7O ANO", "8O ANO", "9O ANO"],
    "EM": ["", "1A SERIE", "2A SERIE", "3A SERIE"],
    "PV": ["", "APROVA +", "ELETIVAS", "SEMI"],
    "VÁRIOS": ["", "VARIOS"]
}

# Campos de entrada para os filtros
st.session_state.cod_insersao = st.sidebar.text_input("Código de Inserção", st.session_state.cod_insersao)
st.session_state.cod_sku = st.sidebar.text_input("Código SKU", st.session_state.cod_sku)

# Filtros dropdowns
tmp_segmento = st.sidebar.selectbox("Segmento", segmento_options, index=segmento_options.index(st.session_state.segmento))
st.session_state.segmento = tmp_segmento

serie_options = serie_dict.get(st.session_state.segmento, [""])
tmp_serie = st.sidebar.selectbox("Série", serie_options, index=serie_options.index(st.session_state.serie))
st.session_state.serie = tmp_serie

st.session_state.envio = st.sidebar.selectbox("Envio", ["", "V1", "V2", "V3", "V4"], index=["", "V1", "V2", "V3", "V4"].index(st.session_state.envio))
st.session_state.usuario = st.sidebar.selectbox("Usuário", ["", "Aluno", "Professor"], index=["", "Aluno", "Professor"].index(st.session_state.usuario))
st.session_state.personalizacao = st.sidebar.selectbox("Personalização", ["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER", "DOM BOSCO", "DOM BOSCO BALSAS", "ELO", "FATO", "FILOMENA", "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR", "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", "ROSALVO", "SAE", "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"], index=["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER", "DOM BOSCO", "DOM BOSCO BALSAS", "ELO", "FATO", "FILOMENA", "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR", "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", "ROSALVO", "SAE", "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"].index(st.session_state.personalizacao))

# Botão para limpar filtros
if st.sidebar.button("Limpar Filtros"):
    for key in ["segmento", "serie", "cod_insersao", "cod_sku", "envio", "usuario", "personalizacao"]:
        st.session_state[key] = ""
    st.rerun()

# Botão para consultar
df = None
if st.sidebar.button("Consultar"):
    produtos = consultar_api(
        cod_insersao=st.session_state.cod_insersao,
        cod_sku=st.session_state.cod_sku,
        segmento=st.session_state.segmento,
        serie=st.session_state.serie,
        envio=st.session_state.envio,
        usuario=st.session_state.usuario,
        personalizacao=st.session_state.personalizacao
    )
    if produtos:
        df = pd.DataFrame(produtos)
        colunas_desejadas = ['cod_insersao', 'descricao_kit', 'cod_sku',
                              'descricao_sku', 'segmento', 'serie', 'volume', 'envio',
                              'frequencia', 'usuario', 'info_produto', 'tipo_material',
                              'classificacao_produto', 'personalizacao']
        df = df[colunas_desejadas]

if df is not None:
    st.dataframe(df, use_container_width=True)
else:
    st.write("Nenhum produto encontrado para estes filtros.")
