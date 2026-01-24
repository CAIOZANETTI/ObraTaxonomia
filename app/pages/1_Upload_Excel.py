import streamlit as st
import pandas as pd
import os
import io
from scripts.utils import convert_xlsx_to_csv_all_methods

st.set_page_config(page_title="1. Upload Excel", layout="wide")

st.header("1. Upload de Arquivo")
st.markdown("Carregue seu arquivo Excel (.xlsx) para iniciar o processamento.")

# --- Inicialização do Session State ---
if 'sheet_mode' not in st.session_state:
    st.session_state['sheet_mode'] = 'Uma Aba'
if 'sheet_selected' not in st.session_state:
    st.session_state['sheet_selected'] = None

# --- Upload ---
uploaded_file = st.file_uploader("Selecione o arquivo Excel", type=['xlsx'])

if uploaded_file:
    # Salvar bytes no session state para persistência
    st.session_state['excel_bytes'] = uploaded_file.getvalue()
    
    # Salvar temporariamente para conversão (a função de utils espera path)
    # TODO: Refatorar utils para aceitar bytes stream se possível, ou usar tempfile
    # Por enquanto, salvamos num temp
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    try:
        # --- Modo de Processamento ---
        mode_options = ["Uma Aba", "Concatenar Abas"]
        st.session_state['sheet_mode'] = st.radio(
            "Modo de Leitura", 
            mode_options, 
            index=mode_options.index(st.session_state.get('sheet_mode', 'Uma Aba')),
            horizontal=True
        )
        
        # --- Conversão ---
        # Convertemos TUDO primeiro para descobrir as abas
        with st.spinner("Lendo estrutura do arquivo..."):
            result = convert_xlsx_to_csv_all_methods(temp_path, output_dir="temp_csvs")
        
        if not result['success']:
            st.error(f"Erro na conversão: {result['message']}")
        else:
            files = result['output_files']
            # Extrair nomes das abas dos arquivos gerados
            # Assumindo que o conversor gera arquivos com nome da aba (ou similar)
            # O utils.py usa safe_name. Vamos mapear de volta ou usar o filename base
            
            sheet_map = {os.path.basename(f): f for f in files}
            sheet_names = list(sheet_map.keys())
            
            selected_csv_path = None
            
            if st.session_state['sheet_mode'] == "Uma Aba":
                if len(sheet_names) > 8:
                    selected_sheet_name = st.selectbox("Selecione a Aba", sheet_names)
                else:
                    # Usando radio como fallback se pills não existir em versoes antigas, 
                    # mas pills é recomendado na arquitetura.
                    # Verificando se st.pills existe (st.pills foi adicionado recentemente)
                    if hasattr(st, 'pills'):
                        selected_sheet_name = st.pills("Selecione a Aba", sheet_names, selection_mode="single")
                    else:
                        selected_sheet_name = st.radio("Selecione a Aba", sheet_names, horizontal=True)
                
                st.session_state['sheet_selected'] = selected_sheet_name
                if selected_sheet_name:
                    selected_csv_path = sheet_map[selected_sheet_name]
                    
            else: # Concatenar
                st.info("Concatenando todas as abas encontradas...")
                # Lógica de concatenação simples (assumindo mesma estrutura)
                dfs = []
                for fname in files:
                    try:
                        d = pd.read_csv(fname)
                        d['aba_origem'] = fname # Rastreabilidade
                        dfs.append(d)
                    except Exception as e:
                        st.warning(f"Ignorando arquivo {fname}: {e}")
                
                if dfs:
                    df_concat = pd.concat(dfs, ignore_index=True)
                    # Salvar concatenado
                    concat_path = "temp_csvs/concatenado.csv"
                    df_concat.to_csv(concat_path, index=False)
                    selected_csv_path = concat_path
            
            # --- Carregar e Exibir CSV Raw ---
            if selected_csv_path and os.path.exists(selected_csv_path):
                df_raw = pd.read_csv(selected_csv_path)
                st.session_state['csv_raw'] = df_raw.to_csv(index=False)
                
                # Resumo
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("Linhas", len(df_raw))
                m2.metric("Colunas", len(df_raw.columns))
                m3.metric("Abas", len(sheet_names) if st.session_state['sheet_mode'] == 'Concatenar Abas' else 1)
                
                # Preview
                st.subheader("Preview (Topo e Fim)")
                st.dataframe(df_raw.head(5), use_container_width=True)
                st.dataframe(df_raw.tail(5), use_container_width=True)
                
                # Ações
                st.divider()
                c1, c2 = st.columns([1, 5])
                if c1.button("Resetar Sessão", type="primary"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
                
                if c2.button("Continuar para Mapeamento >"):
                    st.switch_page("pages/2_Mapear_Colunas.py")

    except Exception as e:
        st.error(f"Erro inesperado: {e}")
    finally:
        # Limpar temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)

else:
    # Estado inicial ou resetado
    if st.button("Limpar Sessão Atual"):
        st.session_state.clear()
        st.rerun()
