
import streamlit as st
import pandas as pd
import os
import sys

# Add project root to path generic logic if needed (or rely on installed package)
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if base_path not in sys.path:
    sys.path.append(base_path)

from obra_taxonomia import data_ingestion as di

st.set_page_config(
    page_title="Excel -> CSV",
    page_icon="🏗️",
    layout="wide"
)

# --- SESSION STATE ---
if 'processed_data' not in st.session_state:
    st.session_state['processed_data'] = {} 
    # Structure: { 
    #   'excel_name': ..., 'excel_bytes': ..., 'sheets_info': ..., 
    #   'df_all': ..., 'csv_all_bytes': ... 
    #   'df_norm': ..., 'csv_norm_bytes': ..., 'etl_log': ...
    # }
    
# We will use st.session_state locals to hold the CURRENT file's state for display context.
if 'current_file_state' not in st.session_state:
    st.session_state['current_file_state'] = None


# --- UI ---

st.title("Excel → CSV (Ingestão Genérica)")
st.markdown("Converta planilhas para o formato padrão do sistema (CSV) com opção de normalização.")

# TABS
tab_upload, tab_test = st.tabs(["📤 Upload", "🧪 Modo Teste (Batch)"])

def set_current_state(filename, file_bytes, source):
    """Process triggers generic ingestion logic."""
    with st.spinner(f"Processando {filename}..."):
        sheets_info, df_resumo, df_all, csv_bytes = di.process_workbook(file_bytes, filename)
        
        st.session_state['current_file_state'] = {
            'filename': filename,
            'source': source,
            'sheets_info': sheets_info,
            'df_resumo': df_resumo,
            'df_all': df_all,
            'csv_all_bytes': csv_bytes,
            'df_norm': None,       # Reset norm on new process
            'csv_norm_bytes': None
        }
        
        # Persist specific globals (optional, dependendo do requisito de session state global)
        st.session_state['df_all'] = df_all
        st.session_state['df_resumo_abas'] = df_resumo
        st.session_state['sheets_info'] = sheets_info


# --- TAB 1: UPLOAD ---
with tab_upload:
    uploaded_file = st.file_uploader("Selecione Excel (.xlsx, .xls)", type=['xlsx', 'xls'])
    if uploaded_file:
        # Check if we need to process (if file changed)
        # Using name size check or just manual trigger? 
        # Streamlit re-runs, let's process if not already processed same file
        curr = st.session_state['current_file_state']
        if curr is None or curr.get('filename') != uploaded_file.name:
             set_current_state(uploaded_file.name, uploaded_file.getvalue(), "upload")

# --- TAB 2: TESTE ---
with tab_test:
    st.info("Arquivos em `data/excel/`")
    test_files = di.list_test_files()
    
    if test_files:
        selected_test = st.selectbox("Escolha um arquivo para teste", test_files)
        if st.button("Processar Arquivo de Teste"):
            path = os.path.join("data/excel", selected_test)
            try:
                f_bytes, f_name = di.load_excel_bytes(path)
                set_current_state(f_name, f_bytes, "test_file")
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
    else:
        st.warning("Nenhum arquivo encontrado em `data/excel/`.")


# --- DISPLAY RESULTS ---

state = st.session_state['current_file_state']

if state and state['df_all'] is not None:
    st.divider()
    st.subheader(f"Resultado: {state['filename']}")
    
    # 1. Summary Table
    st.markdown("### Resumo das Abas")
    st.dataframe(state['df_resumo'], hide_index=True)
    
    # Stats footer
    total_lines = len(state['df_all'])
    total_cols = len(state['df_all'].columns)
    counts = state['df_resumo']['linhas'].astype(bool).sum() # rough 'ok' check or use status logic? 
    # Better to iterate sheets_info for accurate status count
    s_info = state['sheets_info']
    n_ok = sum(1 for k,v in s_info.items() if v['status'] == 'ok')
    n_err = sum(1 for k,v in s_info.items() if v['status'] == 'error')
    n_emp = sum(1 for k,v in s_info.items() if v['status'] == 'empty')
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Linhas (Bruto)", total_lines)
    c2.metric("Colunas", total_cols)
    c3.metric("Abas OK", n_ok)
    c4.caption(f"Vazias: {n_emp} | Erros: {n_err}")
    
    # 2. Details (Expanders)
    with st.expander("Ver Detalhes por Aba"):
        for s_name, info in s_info.items():
            status_icon = "✅" if info['status'] == 'ok' else "⚠️" if info['status'] == 'empty' else "❌"
            st.markdown(f"**{status_icon} {s_name}** ({info['rows']}x{info['cols']})")
            if info['status'] == 'ok' and info['df_head'] is not None:
                st.dataframe(info['df_head'], use_container_width=True)
            elif info['status'] == 'error':
                st.error(info['error_msg'])
    
    # 3. CSV Bruto Download
    if state['csv_all_bytes']:
        st.download_button(
            "⬇️ Baixar CSV Bruto",
            state['csv_all_bytes'],
            f"{state['filename']}__consolidado_bruto.csv",
            "text/csv"
        )
    
    st.divider()
    
    # --- NORMALIZATION BLOCK ---
    st.header("Normalização de Texto (Opcional)")
    
    col_opts, col_action = st.columns([1, 2])
    
    with col_opts:
        st.markdown("**Configurações:**")
        do_accents = st.toggle("Remover Acentos", True)
        do_punct = st.toggle("Remover Pontuação", True)
        do_stopwords = st.toggle("Remover Stopwords (de, da, o...)", True)
        do_spaces = st.toggle("Colapsar Espaços", True)
        
        config = {
            'remove_accents': do_accents,
            'remove_punctuation': do_punct,
            'remove_stopwords': do_stopwords,
            'collapse_spaces': do_spaces
        }

    with col_action:
        if st.button("Gerar CSV Normalizado"):
            with st.spinner("Normalizando..."):
                df_norm, logs = di.etl_normalize_df(state['df_all'], config)
                
                state['df_norm'] = df_norm
                state['csv_norm_bytes'] = df_norm.to_csv(index=False).encode('utf-8')
                state['etl_log'] = logs
                st.success("Normalização concluída!")

    if state['df_norm'] is not None:
        st.markdown("#### Preview Normalizado")
        st.dataframe(state['df_norm'].head(20), use_container_width=True)
        
        st.download_button(
            "⬇️ Baixar CSV Normalizado",
            state['csv_norm_bytes'],
            f"{state['filename']}__consolidado_normalizado.csv",
            "text/csv",
            type="primary"
        )
        
        with st.expander("Log de Normalização"):
             st.write(state.get('etl_log'))

