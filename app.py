import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np
from rapidfuzz import fuzz
import unidecode

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

def normalizar_nome(nome):
    return unidecode.unidecode(str(nome)).lower().replace('.', '').replace(' ', '')

# --- Uploads ---
col1, col2 = st.columns(2)

with col1:
    st.header("📁 Arquivo Financeiro")
    arquivo_fin = st.file_uploader("Selecione o arquivo financeiro", type="xlsx", key="fin")

with col2:
    st.header("📁 Arquivo Contábil")
    arquivo_con = st.file_uploader("Selecione o arquivo contábil", type="xlsx", key="con")

if arquivo_fin and arquivo_con:
    xls_fin = pd.ExcelFile(arquivo_fin)
    xls_con = pd.ExcelFile(arquivo_con)

    st.markdown("<style>div[data-testid='stSelectbox'] label, div[data-testid='stRadio'] label, div[data-testid='stTextInput'] label { font-size: 0.85rem !important; }</style>", unsafe_allow_html=True)

    with st.expander("⚙️ Parâmetros de Conciliação", expanded=True):
        col5, col6 = st.columns(2)

        with col5:
            st.write("**Financeiro**")
            aba_fin = st.selectbox("Escolha a aba (financeiro):", xls_fin.sheet_names, key="aba_fin")
            df_fin = pd.read_excel(xls_fin, sheet_name=aba_fin)
            st.dataframe(df_fin.head(5), height=150)
            colunas_fin = df_fin.columns.tolist()

            modo_fin = st.radio("Formato de valor:", ["Campo único de valor", "Crédito e Débito"], key="modo_fin")
            campo_data_fin = st.selectbox("Data:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'data')), key="data_fin")
            campo_doc_fin = st.selectbox("Documento:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'documento')), key="doc_fin")
            campo_parceiro_fin = st.selectbox("Parceiro:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'parceiro')), key="parceiro_fin")

            if modo_fin == "Campo único de valor":
                campo_valor_fin = st.selectbox("Campo de Valor:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'valor')), key="valor_fin")
                df_fin["VALOR_CONSOLIDADO"] = pd.to_numeric(df_fin[campo_valor_fin], errors='coerce')
            else:
                campo_credito_fin = st.selectbox("Crédito:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'credito')), key="credito_fin")
                campo_debito_fin = st.selectbox("Débito:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'debito')), key="debito_fin")
                df_fin["VALOR_CONSOLIDADO"] = pd.to_numeric(df_fin[campo_credito_fin], errors='coerce').fillna(0) - pd.to_numeric(df_fin[campo_debito_fin], errors='coerce').fillna(0)
            df_fin[campo_data_fin] = pd.to_datetime(df_fin[campo_data_fin], errors='coerce')

        with col6:
            st.write("**Contábil**")
            aba_con = st.selectbox("Escolha a aba (contábil):", xls_con.sheet_names, key="aba_con")
            df_con = pd.read_excel(xls_con, sheet_name=aba_con)
            st.dataframe(df_con.head(5), height=150)
            colunas_con = df_con.columns.tolist()

            modo_con = st.radio("Formato de valor:", ["Campo único de valor", "Crédito e Débito"], key="modo_con")
            sugestao_data_con = sugerir_coluna(df_con, 'data')
            campo_data_con = st.selectbox("Data:", colunas_con, index=colunas_con.index(sugestao_data_con) if sugestao_data_con in colunas_con else 0, key="data_con")
            sugestao_doc_con = sugerir_coluna(df_con, 'documento')
            campo_doc_con = st.selectbox("Documento:", colunas_con, index=colunas_con.index(sugestao_doc_con) if sugestao_doc_con in colunas_con else 0, key="doc_con")
            sugestao_parceiro_con = sugerir_coluna(df_con, 'parceiro')
            campo_parceiro_con = st.selectbox("Parceiro:", colunas_con, index=colunas_con.index(sugestao_parceiro_con) if sugestao_parceiro_con in colunas_con else 0, key="parceiro_con")

            if modo_con == "Campo único de valor":
                sugestao_valor_con = sugerir_coluna(df_con, 'valor')
                campo_valor_con = st.selectbox("Campo de Valor:", colunas_con, index=colunas_con.index(sugestao_valor_con) if sugestao_valor_con in colunas_con else 0, key="valor_con")
                df_con["VALOR_CONSOLIDADO"] = pd.to_numeric(df_con[campo_valor_con], errors='coerce')
            else:
                sugestao_credito_con = sugerir_coluna(df_con, 'credito')
                campo_credito_con = st.selectbox("Crédito:", colunas_con, index=colunas_con.index(sugestao_credito_con) if sugestao_credito_con in colunas_con else 0, key="credito_con")
                sugestao_debito_con = sugerir_coluna(df_con, 'debito')
                campo_debito_con = st.selectbox("Débito:", colunas_con, index=colunas_con.index(sugestao_debito_con) if sugestao_debito_con in colunas_con else 0, key="debito_con")
                df_con["VALOR_CONSOLIDADO"] = pd.to_numeric(df_con[campo_credito_con], errors='coerce').fillna(0) - pd.to_numeric(df_con[campo_debito_con], errors='coerce').fillna(0)
            df_con[campo_data_con] = pd.to_datetime(df_con[campo_data_con], errors='coerce')

    # Conciliação
    if st.button("🔍 Executar Conciliação"):
        with st.spinner("Conciliando registros..."):
            df_fin['STATUS'] = 'Não Encontrado'
            df_fin['PARCEIRO_NORMALIZADO'] = df_fin[campo_parceiro_fin].apply(normalizar_nome)
            df_con['PARCEIRO_NORMALIZADO'] = df_con[campo_parceiro_con].apply(normalizar_nome)

            for i, row_fin in df_fin.iterrows():
                for j, row_con in df_con.iterrows():
                    if abs(row_fin['VALOR_CONSOLIDADO'] - row_con['VALOR_CONSOLIDADO']) <= 0.05:
                        if str(row_fin[campo_doc_fin]).strip() == str(row_con[campo_doc_con]).strip():
                            df_fin.at[i, 'STATUS'] = 'Conciliado'
                            break
                        elif fuzz.partial_ratio(row_fin['PARCEIRO_NORMALIZADO'], row_con['PARCEIRO_NORMALIZADO']) >= 85:
                            df_fin.at[i, 'STATUS'] = 'Parcial'

            # Filtros
            status_filtrado = st.selectbox("Filtrar por status:", ["Todos", "Conciliado", "Parcial", "Não Encontrado"])
            parceiro_filtrado = st.text_input("Filtrar por parceiro:").lower().strip()
            doc_filtrado = st.text_input("Filtrar por documento:").lower().strip()

            df_visual = df_fin[[campo_data_fin, campo_doc_fin, campo_parceiro_fin, 'VALOR_CONSOLIDADO', 'STATUS']].copy()

            if status_filtrado != "Todos":
                df_visual = df_visual[df_visual['STATUS'] == status_filtrado]
            if parceiro_filtrado:
                df_visual = df_visual[df_visual[campo_parceiro_fin].astype(str).str.lower().str.contains(parceiro_filtrado)]
            if doc_filtrado:
                df_visual = df_visual[df_visual[campo_doc_fin].astype(str).str.lower().str.contains(doc_filtrado)]

            def colorir_linhas(val):
                if val == 'Conciliado':
                    return 'background-color: #d4edda; color: black'  # verde claro
                elif val == 'Parcial':
                    return 'background-color: #fff3cd; color: black'  # amarelo claro
                else:
                    return 'background-color: #f8d7da; color: black'  # vermelho claro

            styled_df = df_visual.style.applymap(colorir_linhas, subset=['STATUS'])
            st.dataframe(styled_df, use_container_width=True)

            resumo = pd.DataFrame({
                'Fonte': ['Financeiro'],
                'Total de Linhas': [len(df_fin)],
                'Conciliados': [len(df_fin[df_fin['STATUS'] == 'Conciliado'])],
                'Parciais': [len(df_fin[df_fin['STATUS'] == 'Parcial'])],
                'Não Encontrados': [len(df_fin[df_fin['STATUS'] == 'Não Encontrado'])]
            })
            st.markdown("### 📌 Resumo")
            st.dataframe(resumo)

            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_visual.to_excel(writer, index=False, sheet_name='Resultado Filtrado')
            st.download_button("📥 Baixar resultado filtrado", buffer.getvalue(), file_name="consolidado_filtrado.xlsx")
