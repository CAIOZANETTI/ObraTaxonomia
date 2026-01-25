import streamlit as st
import pandas as pd
import os
import io
import sys

# Adicionar diretório raiz ao path para importar scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.utils import convert_xlsx_to_csv_all_methods

st.set_page_config(page_title="1. Upload Excel", layout="wide")

st.header("1. Upload de Arquivo")
st.markdown("Carregue seu arquivo Excel (.xlsx) para iniciar o processamento.")

# --- Inicialização do Session State ---
if 'sheet_mode' not in st.session_state:
    st.session_state['sheet_mode'] = 'Uma Aba'
if 'sheet_selected' not in st.session_state:
    st.session_state['sheet_selected'] = None

# --- Abas: Upload vs Teste ---
tab_upload, tab_test = st.tabs(["📂 Upload Arquivo", "🧪 Arquivos de Teste"])

uploaded_file = None
file_source = None # 'upload' or 'test'

with tab_upload:
    uploaded_file_obj = st.file_uploader("Selecione o arquivo Excel", type=['xlsx', 'xls', 'csv'])
    if uploaded_file_obj:
        uploaded_file = uploaded_file_obj
        file_source = 'upload'

with tab_test:
    st.info("Selecione um arquivo da pasta `data/excel` para testar o sistema.")
    
    # Listar arquivos em data/excel
    # Caminho relativo ou absoluto
    # Assumindo estrutura do projeto: app/pages/1_Upload.py -> ../../data/excel
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    test_dir = os.path.join(base_dir, 'data', 'excel')
    
    if os.path.exists(test_dir):
        files = [f for f in os.listdir(test_dir) if f.endswith(('.xlsx', '.xls', '.csv'))]
        if files:
            # Change from selectbox to pills per user request
            selected_test_file = st.pills(
                "Escolha um arquivo:", 
                files, 
                selection_mode="single"
            )
            
            if selected_test_file:
                file_path = os.path.join(test_dir, selected_test_file)
                # Ler arquivo como bytes para simular upload
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    uploaded_file = io.BytesIO(file_bytes)
                    uploaded_file.name = selected_test_file
                    file_source = 'test'
        else:
            st.warning("Nenhum arquivo encontrado em `data/excel`.")
    else:
        st.error(f"Diretório de testes não encontrado: {test_dir}")

# --- Processamento ---
if uploaded_file:
    # Salvar bytes no session state para persistência
    # Se mudou o arquivo, reseta o processamento anterior?
    # Vamos verificar se mudou o arquivo pelo nome/tamanho ou apenas processar sempre
    
    st.session_state['excel_bytes'] = uploaded_file.getvalue()
    
    # Mostrar banner
    if file_source == 'test':
        st.toast(f"Usando arquivo de teste: {uploaded_file.name}", icon="🧪")
    
    # Salvar temporariamente para conversão
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    try:
        st.divider()
        st.subheader("Configuração de Leitura")
        
        # --- Modo de Processamento ---
        mode_options = ["Uma Aba", "Concatenar Abas"]
        st.session_state['sheet_mode'] = st.radio(
            "Modo de Leitura", 
            mode_options, 
            index=mode_options.index(st.session_state.get('sheet_mode', 'Uma Aba')),
            horizontal=True
        )
        
        # --- Conversão ---
        with st.spinner("Lendo estrutura do arquivo..."):
            result = convert_xlsx_to_csv_all_methods(temp_path, output_dir="temp_csvs")
        
        if not result['success']:
            st.error(f"Erro na conversão: {result['message']}")
        else:
            files_generated = result['output_files']
            sheet_map = {os.path.basename(f): f for f in files_generated}
            sheet_names = list(sheet_map.keys())
            
            selected_csv_path = None
            
            if st.session_state['sheet_mode'] == "Uma Aba":
                if len(sheet_names) > 8:
                    selected_sheet_name = st.selectbox("Selecione a Aba", sheet_names)
                else:
                    if hasattr(st, 'pills'):
                        selected_sheet_name = st.pills("Selecione a Aba", sheet_names, selection_mode="single")
                    else:
                        selected_sheet_name = st.radio("Selecione a Aba", sheet_names, horizontal=True)
                
                st.session_state['sheet_selected'] = selected_sheet_name
                if selected_sheet_name:
                    selected_csv_path = sheet_map[selected_sheet_name]
                    
            else: # Concatenar
                st.info(f"Concatenando {len(files_generated)} abas...")
                dfs = []
                for fname in files_generated:
                    try:
                        d = pd.read_csv(fname)
                        d['aba_origem'] = os.path.basename(fname)
                        dfs.append(d)
                    except Exception as e:
                        st.warning(f"Ignorando {fname}: {e}")
                
                if dfs:
                    df_concat = pd.concat(dfs, ignore_index=True)
                    concat_path = "temp_csvs/concatenado.csv"
                    df_concat.to_csv(concat_path, index=False)
                    selected_csv_path = concat_path
            
            # --- Carregar e Exibir CSV Raw ---
            if selected_csv_path and os.path.exists(selected_csv_path):
                df_raw = pd.read_csv(selected_csv_path)
                st.session_state['csv_raw'] = df_raw.to_csv(index=False)
                
                # Resumo
                st.divider()
                st.markdown("### Resumo do Arquivo")
                m1, m2, m3 = st.columns(3)
                m1.metric("Linhas", len(df_raw))
                m2.metric("Colunas", len(df_raw.columns))
                m3.metric("Abas", len(sheet_names) if st.session_state['sheet_mode'] == 'Concatenar Abas' else 1)
                
                # Preview
                st.markdown("### 🔍 Visualização dos Dados")
                
                with st.expander("🟦 Início do Arquivo (Primeiras 10 linhas)", expanded=True):
                    st.dataframe(df_raw.head(10), use_container_width=True)
                
                with st.expander("🟧 Fim do Arquivo (Últimas 10 linhas)", expanded=True):
                    st.dataframe(df_raw.tail(10), use_container_width=True)
                
                # Ações
                st.divider()
                c1, c2 = st.columns([1, 5])
                if c1.button("Resetar Sessão", type="primary"):
                    st.session_state.clear()
                    st.rerun()
                
                if c2.button("Continuar para Mapeamento >"):
                    st.switch_page("pages/2_Mapear_Colunas.py")

    except Exception as e:
        st.error(f"Erro inesperado: {e}")
    finally:
        # Limpar temporário principal
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
