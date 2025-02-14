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
st.sidebar.image("https://github.com/dePauloCardoso/streamlit_app/blob/main/Logo_SAE.png")

# Interface Streamlit
st.sidebar.title("Consulta de Produtos")

# Campos de entrada para os filtros
cod_insersao = st.sidebar.text_input("Código de Inserção")
cod_sku = st.sidebar.text_input("Código SKU")

# Dropdowns para os filtros
segmento_options = ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"]  # Opções para o dropdown de segmento
segmento = st.sidebar.selectbox("Segmento", segmento_options)

serie_options = ["", "INF I", "INF II", "INF III", "INF IV", "INF V", "1o ANO", "2o ANO", "3o ANO", "4o ANO", "5o ANO",
                "6o ANO", "7o ANO", "8o ANO", "9o ANO", "1A SERIE", "2A SERIE", "3A SERIE", "APROVA +", "ELETIVAS", "SEMI", "VARIOS"]  # Opções para o dropdown de série
serie = st.sidebar.selectbox("Série", serie_options)

envio_options = ["", "V1", "V2", "V3", "V4"]  # Opções para o dropdown de envio
envio = st.sidebar.selectbox("Envio", envio_options)

usuario_options = ["", "Aluno", "Professor"]  # Opções para o dropdown de usuário
usuario = st.sidebar.selectbox("Usuário", usuario_options)

personalizacao_options = ["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER","DOM BOSCO", "DOM BOSCO BALSAS", "ELO", "FATO", "FILOMENA", 
                        "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR", "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", 
                        "ROSALVO", "SAE", "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"]  # Opções para o dropdown de personalizacao
personalizacao = st.sidebar.selectbox("Personalização", personalizacao_options)

# Botão para consultar
if st.sidebar.button("Consultar"):
    # Consulta a API com os filtros
    produtos = consultar_api(
        cod_insersao=cod_insersao,
        cod_sku=cod_sku,
        segmento=segmento,
        serie=serie,
        envio=envio,
        usuario=usuario,
        personalizacao=personalizacao
    )

    # Exibe os resultados em tabela
    if produtos:
        df = pd.DataFrame(produtos)

        # Reordena as colunas
        colunas_desejadas = ['cod_insersao', 'descricao_kit', 'cod_sku',
                             'descricao_sku', 'segmento', 'serie', 'volume', 'envio',
                             'frequencia', 'usuario', 'info_produto', 'tipo_material',
                             'classificacao_produto', 'personalizacao']
        df = df[colunas_desejadas]

        # Define a largura das colunas
        largura_colunas = {
            'cod_insersao': st.column_config.Column(width=125),
            'descricao_kit': st.column_config.Column(width=300),
            'cod_sku': st.column_config.Column(width=125),
            'descricao_sku': st.column_config.Column(width=300),
            'segmento': st.column_config.Column(width=70),
            'serie': st.column_config.Column(width=70),
            'volume': st.column_config.Column(width=100),
            'envio': st.column_config.Column(width=70),
            'frequencia': st.column_config.Column(width=100),
            'usuario': st.column_config.Column(width=80),
            'info_produto': st.column_config.Column(width=150),
            'tipo_material': st.column_config.Column(width=130),
            'classificacao_produto': st.column_config.Column(width=130),
            'personalizacao': st.column_config.Column(width=150)
        }

        # Exibe o DataFrame com column_config
        st.dataframe(df, column_config=largura_colunas, use_container_width=True)
    else:
        st.write("Nenhum produto encontrado para estes filtros.")