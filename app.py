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

# --- Uploads ---
col1, col2 = st.columns(2)

with col1:
    st.header("📁 Arquivo Financeiro")
    arquivo_fin = st.file_uploader("Selecione o arquivo financeiro", type="xlsx", key="fin")

with col2:
    st.header("📁 Arquivo Contábil")
    arquivo_con = st.file_uploader("Selecione o arquivo contábil", type="xlsx", key="con")

# --- Função de sugestão de coluna ---
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

# --- Processamento ---
df_fin, df_con = None, None

if arquivo_fin:
    xls_fin = pd.ExcelFile(arquivo_fin)

if arquivo_con:
    xls_con = pd.ExcelFile(arquivo_con)

if arquivo_fin and arquivo_con:
    st.markdown("### 🧹 Mapeamento dos campos para conciliação")
    col5, col6 = st.columns(2)

    with col5:
        st.write("**Financeiro**")
        aba_fin = st.selectbox("Escolha a aba (financeiro):", xls_fin.sheet_names, key="aba_fin")
        if aba_fin:
            df_fin = pd.read_excel(xls_fin, sheet_name=aba_fin)
            colunas_fin = df_fin.columns.tolist()
            st.dataframe(df_fin.head(5))

            modo_fin = st.radio("Formato de valor:", ["Campo único de valor", "Crédito e Débito"], key="modo_fin")
            campo_data_fin = st.selectbox("Data:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'data')) if sugerir_coluna(df_fin, 'data') in colunas_fin else 0, key="data_fin")
            campo_doc_fin = st.selectbox("Documento:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'documento')) if sugerir_coluna(df_fin, 'documento') in colunas_fin else 0, key="doc_fin")
            campo_parceiro_fin = st.selectbox("Parceiro:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'parceiro')) if sugerir_coluna(df_fin, 'parceiro') in colunas_fin else 0, key="parceiro_fin")

            if modo_fin == "Campo único de valor":
                campo_valor_fin = st.selectbox("Campo de Valor:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'valor')) if sugerir_coluna(df_fin, 'valor') in colunas_fin else 0, key="valor_fin")
                df_fin["VALOR_CONSOLIDADO"] = pd.to_numeric(df_fin[campo_valor_fin], errors='coerce')
            else:
                campo_credito_fin = st.selectbox("Crédito:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'credito')) if sugerir_coluna(df_fin, 'credito') in colunas_fin else 0, key="credito_fin")
                campo_debito_fin = st.selectbox("Débito:", colunas_fin, index=colunas_fin.index(sugerir_coluna(df_fin, 'debito')) if sugerir_coluna(df_fin, 'debito') in colunas_fin else 0, key="debito_fin")
                df_fin["VALOR_CONSOLIDADO"] = pd.to_numeric(df_fin[campo_credito_fin], errors='coerce').fillna(0) - pd.to_numeric(df_fin[campo_debito_fin], errors='coerce').fillna(0)
            df_fin[campo_data_fin] = pd.to_datetime(df_fin[campo_data_fin], errors='coerce')

    with col6:
        st.write("**Contábil**")
        aba_con = st.selectbox("Escolha a aba (contábil):", xls_con.sheet_names, key="aba_con")
        if aba_con:
            df_con = pd.read_excel(xls_con, sheet_name=aba_con)
            colunas_con = df_con.columns.tolist()
            st.dataframe(df_con.head(5))

            modo_con = st.radio("Formato de valor:", ["Campo único de valor", "Crédito e Débito"], key="modo_con")
            campo_data_con = st.selectbox("Data:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'data')) if sugerir_coluna(df_con, 'data') in colunas_con else 0, key="data_con")
            campo_doc_con = st.selectbox("Documento:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'documento')) if sugerir_coluna(df_con, 'documento') in colunas_con else 0, key="doc_con")
            campo_parceiro_con = st.selectbox("Parceiro:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'parceiro')) if sugerir_coluna(df_con, 'parceiro') in colunas_con else 0, key="parceiro_con")

            if modo_con == "Campo único de valor":
                campo_valor_con = st.selectbox("Campo de Valor:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'valor')) if sugerir_coluna(df_con, 'valor') in colunas_con else 0, key="valor_con")
                df_con["VALOR_CONSOLIDADO"] = pd.to_numeric(df_con[campo_valor_con], errors='coerce')
            else:
                campo_credito_con = st.selectbox("Crédito:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'credito')) if sugerir_coluna(df_con, 'credito') in colunas_con else 0, key="credito_con")
                campo_debito_con = st.selectbox("Débito:", colunas_con, index=colunas_con.index(sugerir_coluna(df_con, 'debito')) if sugerir_coluna(df_con, 'debito') in colunas_con else 0, key="debito_con")
                df_con["VALOR_CONSOLIDADO"] = pd.to_numeric(df_con[campo_credito_con], errors='coerce').fillna(0) - pd.to_numeric(df_con[campo_debito_con], errors='coerce').fillna(0)
            df_con[campo_data_con] = pd.to_datetime(df_con[campo_data_con], errors='coerce')

    considerar_parceiro = st.checkbox("Considerar similaridade de parceiro na conciliação")

    if st.button("🔍 Iniciar Conciliação"):
        tolerancia = 0.05
        df_fin['STATUS'] = 'Não Encontrado'
        df_con['STATUS'] = 'Não Encontrado'

        for i, linha_fin in df_fin.iterrows():
            valor_fin = linha_fin['VALOR_CONSOLIDADO']
            doc_fin = str(linha_fin[campo_doc_fin]).strip()
            parceiro_fin = normalizar_nome(linha_fin[campo_parceiro_fin])

            candidatos = df_con[abs(df_con['VALOR_CONSOLIDADO'] - valor_fin) <= tolerancia].copy()

            if not candidatos.empty:
                candidatos['DOC_OK'] = candidatos[campo_doc_con].astype(str).str.strip() == doc_fin
                candidatos['SIMILARIDADE'] = candidatos[campo_parceiro_con].apply(lambda x: fuzz.partial_ratio(parceiro_fin, normalizar_nome(x)))

                if any(candidatos['DOC_OK']):
                    idx_match = candidatos[candidatos['DOC_OK']].index[0]
                    df_fin.at[i, 'STATUS'] = 'Conciliado'
                    df_con.at[idx_match, 'STATUS'] = 'Conciliado'
                elif considerar_parceiro and any(candidatos['SIMILARIDADE'] >= 85):
                    idx_parcial = candidatos[candidatos['SIMILARIDADE'] >= 85].index[0]
                    df_fin.at[i, 'STATUS'] = 'Parcial'
                    df_con.at[idx_parcial, 'STATUS'] = 'Parcial'

        resumo = pd.DataFrame({
            'Fonte': ['Financeiro', 'Contábil'],
            'Total de Linhas': [len(df_fin), len(df_con)],
            'Conciliados': [len(df_fin[df_fin['STATUS'] == 'Conciliado']), len(df_con[df_con['STATUS'] == 'Conciliado'])],
            'Parciais': [len(df_fin[df_fin['STATUS'] == 'Parcial']), len(df_con[df_con['STATUS'] == 'Parcial'])],
            'Não Encontrados': [len(df_fin[df_fin['STATUS'] == 'Não Encontrado']), len(df_con[df_con['STATUS'] == 'Não Encontrado'])]
        })

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_fin.to_excel(writer, sheet_name='Financeiro - Original', index=False)
            df_con.to_excel(writer, sheet_name='Contabil - Original', index=False)

            campos_export_fin = [campo_data_fin, campo_doc_fin, campo_parceiro_fin, 'VALOR_CONSOLIDADO', 'STATUS']
            campos_export_con = [campo_data_con, campo_doc_con, campo_parceiro_con, 'VALOR_CONSOLIDADO', 'STATUS']

            df_fin[campos_export_fin].to_excel(writer, sheet_name='Financeiro', index=False)
            df_con[campos_export_con].to_excel(writer, sheet_name='Contabil', index=False)

            for aba, df in [('Financeiro', df_fin[campos_export_fin]), ('Contabil', df_con[campos_export_con])]:
                ws = writer.sheets[aba]
                for i, status in enumerate(df['STATUS']):
                    cor = {
                        'Conciliado': '#C6EFCE',
                        'Parcial': '#FFEB9C',
                        'Não Encontrado': '#FFC7CE'
                    }.get(status, '#FFFFFF')
                    ws.set_row(i+1, None, writer.book.add_format({'bg_color': cor}))

            resumo.to_excel(writer, sheet_name='Resumo', index=False)

        st.download_button("📄 Baixar Resultado da Conciliação", output.getvalue(), file_name="resultado_conciliacao.xlsx")
