import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

#------------------------------------------------------------------------------------------------------------------------------------------------------
# Logo + título lado a lado
st.markdown(
    """
    <div style="background-color: white; padding: 20px 30px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=304,fit=crop,q=95/Aq2B471lDpFnv1BK/logo---trescon-30-anos-mv0jg6Lo2EiV7yLp.png" style="height: 60px;">
            <h1 style="margin: 0; font-size: 2.4em;">Conciliador Financeiro x Contábil</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#------------------------------------------------------------------------------------------------------------------------------------------------------

# --- Uploads ---
col1, col2 = st.columns(2)

with col1:
    st.header("📁 Arquivo Financeiro")
    arquivo_fin = st.file_uploader("Selecione o arquivo financeiro", type="xlsx", key="fin")

with col2:
    st.header("📁 Arquivo Contábil")
    arquivo_con = st.file_uploader("Selecione o arquivo contábil", type="xlsx", key="con")

# --- Mapeamento de campos com sugestão ---
def sugerir_coluna(df, tipo):
    nomes = [col.lower() for col in df.columns]
    sugestoes = {
        'valor': ['valor', 'vlr_total', 'vlr', 'total'],
        'credito': ['credito', 'crédito', 'vlr_cred'],
        'debito': ['debito', 'débito', 'vlr_deb'],
        'data': ['data', 'dt_pagamento', 'dt_baixa', 'dt_lancamento'],
        'documento': ['documento', 'doc', 'nf', 'nota', 'numero'],
        'parceiro': ['parceiro', 'cliente', 'fornecedor', 'cnpj', 'razao']
    }
    for sugestao in sugestoes[tipo]:
        for i, nome in enumerate(nomes):
            if sugestao in nome:
                return df.columns[i]
    return None

# --- Processamento e preview ---
df_fin = df_con = None
if arquivo_fin:
    xls_fin = pd.ExcelFile(arquivo_fin)
    aba_fin = st.selectbox("Escolha a aba (financeiro):", xls_fin.sheet_names, key="aba_fin")
    df_fin = pd.read_excel(xls_fin, sheet_name=aba_fin)

if arquivo_con:
    xls_con = pd.ExcelFile(arquivo_con)
    aba_con = st.selectbox("Escolha a aba (contábil):", xls_con.sheet_names, key="aba_con")
    df_con = pd.read_excel(xls_con, sheet_name=aba_con)

if df_fin is not None:
    st.subheader("🔹 Arquivo Financeiro")
    st.dataframe(df_fin.head(5))
    colunas_fin = df_fin.columns.tolist()
    modo_fin = st.radio("Formato de valor:", ["Campo único de valor", "Crédito e Débito"], key="modo_fin")
    if modo_fin == "Campo único de valor":
        campo_valor_fin = st.selectbox("Valor:", colunas_fin, key="valor_fin")
        df_fin["VALOR_CONSOLIDADO"] = pd.to_numeric(df_fin[campo_valor_fin], errors="coerce").fillna(0)
    else:
        campo_credito_fin = st.selectbox("Crédito:", colunas_fin, key="credito_fin")
        campo_debito_fin = st.selectbox("Débito:", colunas_fin, key="debito_fin")
        credito = pd.to_numeric(df_fin[campo_credito_fin], errors="coerce").fillna(0)
        debito = pd.to_numeric(df_fin[campo_debito_fin], errors="coerce").fillna(0)
        df_fin["VALOR_CONSOLIDADO"] = credito - debito

if df_con is not None:
    st.subheader("🔶 Arquivo Contábil")
    st.dataframe(df_con.head(5))
    colunas_con = df_con.columns.tolist()
    modo_con = st.radio("Formato de valor:", ["Campo único de valor", "Crédito e Débito"], key="modo_con")
    if modo_con == "Campo único de valor":
        campo_valor_con = st.selectbox("Valor:", colunas_con, key="valor_con")
        df_con["VALOR_CONSOLIDADO"] = pd.to_numeric(df_con[campo_valor_con], errors="coerce").fillna(0)
    else:
        campo_credito_con = st.selectbox("Crédito:", colunas_con, key="credito_con")
        campo_debito_con = st.selectbox("Débito:", colunas_con, key="debito_con")
        credito = pd.to_numeric(df_con[campo_credito_con], errors="coerce").fillna(0)
        debito = pd.to_numeric(df_con[campo_debito_con], errors="coerce").fillna(0)
        df_con["VALOR_CONSOLIDADO"] = credito - debito
