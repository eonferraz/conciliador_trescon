import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# -----------------------------------------------------------------------------
# Logo + Título com faixa branca e alinhamento centralizado do título
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
        <img src="logo.png" style="height: 60px;">
        <h1 style="margin: 0; font-size: 2.2em;">Conciliador Financeiro x Contábil</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------

# Tradução visual dos elementos do file_uploader
st.markdown("""
<style>
    .stFileUploader > div:first-child {
        display: none !important;
    }
    .stFileUploader label div[data-testid="stFileDropzone"]::before {
        content: "Arraste e solte o arquivo aqui";
        display: block;
        color: #666;
        font-size: 0.9em;
        text-align: center;
        margin-bottom: 10px;
    }
    .stFileUploader button {
        visibility: hidden;
        position: relative;
    }
    .stFileUploader button::after {
        content: "Buscar arquivo";
        visibility: visible;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f2f6;
        border: 1px solid #ccc;
        border-radius: 0.5rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# --- Uploads ---
col1, col2 = st.columns(2)

with col1:
    st.header("📁 Arquivo Financeiro")
    arquivo_fin = st.file_uploader("Selecione o arquivo financeiro", type="xlsx", key="fin")
    aba_fin = None
    df_fin = None

with col2:
    st.header("📁 Arquivo Contábil")
    arquivo_con = st.file_uploader("Selecione o arquivo contábil", type="xlsx", key="con")
    aba_con = None
    df_con = None

# --- Processamento e preview ---
col3, col4 = st.columns(2)

with col3:
    if arquivo_fin:
        xls_fin = pd.ExcelFile(arquivo_fin)
        aba_fin = st.selectbox("Escolha a aba (financeiro):", xls_fin.sheet_names, key="aba_fin")
        if aba_fin:
            df_fin = pd.read_excel(xls_fin, sheet_name=aba_fin)
            st.write("Prévia (5 linhas):")
            st.dataframe(df_fin.head(5))

with col4:
    if arquivo_con:
        xls_con = pd.ExcelFile(arquivo_con)
        aba_con = st.selectbox("Escolha a aba (contábil):", xls_con.sheet_names, key="aba_con")
        if aba_con:
            df_con = pd.read_excel(xls_con, sheet_name=aba_con)
            st.write("Prévia (5 linhas):")
            st.dataframe(df_con.head(5))
