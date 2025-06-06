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
            st.dataframe(df_fin.head(10))

with col4:
    if arquivo_con:
        xls_con = pd.ExcelFile(arquivo_con)
        aba_con = st.selectbox("Escolha a aba (contábil):", xls_con.sheet_names, key="aba_con")
        if aba_con:
            df_con = pd.read_excel(xls_con, sheet_name=aba_con)
            st.write("Prévia (5 linhas):")
            st.dataframe(df_con.head(10))

# --- Mapeamento de campos com sugestão ---
def sugerir_coluna(df, tipo):
    nomes = [col.lower() for col in df.columns]

    sugestoes = {
        'valor': ['valor', 'vlr_total', 'vlr', 'total'],
        'data': ['data', 'dt_pagamento', 'dt_baixa', 'dt_lancamento'],
        'documento': ['documento', 'doc', 'nf', 'nota', 'numero'],
        'parceiro': ['parceiro', 'cliente', 'fornecedor', 'cnpj', 'razao']
    }

    for sugestao in sugestoes[tipo]:
        for i, nome in enumerate(nomes):
            if sugestao in nome:
                return df.columns[i]
    return None

if df_fin is not None and df_con is not None:
    st.markdown("### 🧹 Mapeamento dos campos para conciliação")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔹 Arquivo Financeiro")
        colunas_fin = df_fin.columns.tolist()
        campo_valor_fin = st.selectbox("Campo de Valor:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'valor')) if sugerir_coluna(df_fin, 'valor') in colunas_fin else 0)
        campo_data_fin = st.selectbox("Campo de Data:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'data')) if sugerir_coluna(df_fin, 'data') in colunas_fin else 0)
        campo_doc_fin = st.selectbox("Campo de Documento:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'documento')) if sugerir_coluna(df_fin, 'documento') in colunas_fin else 0)
        campo_parceiro_fin = st.selectbox("Campo de Parceiro:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'parceiro')) if sugerir_coluna(df_fin, 'parceiro') in colunas_fin else 0)

    with col2:
        st.subheader("🔶 Arquivo Contábil")
        colunas_con = df_con.columns.tolist()
        campo_valor_con = st.selectbox("Campo de Valor:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'valor')) if sugerir_coluna(df_con, 'valor') in colunas_con else 0)
        campo_data_con = st.selectbox("Campo de Data:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'data')) if sugerir_coluna(df_con, 'data') in colunas_con else 0)
        campo_doc_con = st.selectbox("Campo de Documento:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'documento')) if sugerir_coluna(df_con, 'documento') in colunas_con else 0)
        campo_parceiro_con = st.selectbox("Campo de Parceiro:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'parceiro')) if sugerir_coluna(df_con, 'parceiro') in colunas_con else 0)
