import streamlit as st
import pandas as pd
import unidecode

st.set_page_config(
    page_title="Detectar Cabeçalhos",
    page_icon="🕵️",
    layout="wide"
)

# --- IMPORTS ---
import sys
import os

# Add scripts to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

try:
    from header_utils import detect_header, CANDIDATOS
except ImportError:
    sys.path.append('scripts')
    from header_utils import detect_header, CANDIDATOS

# --- UI LOGIC ---

st.title("🕵️ Detecção de Cabeçalhos e Mapeamento de Colunas")

# Dicionário (Legacy/Ref for now)
if 'CANDIDATOS' not in locals():
    # Only if not imported
    CANDIDATOS = {}

if 'df_all' not in st.session_state:
    st.warning("Por favor, faça o upload do arquivo na Página 1.")
    st.stop()

df_all = st.session_state['df_all']
sheets = df_all['aba'].unique().tolist()
grouped = df_all.groupby('aba')

st.header(f"Processando {len(sheets)} abas...")

# Configuração Simplificada (Expander)
with st.expander("⚙️ Configurações Avançadas (Opcional)"):
    max_scan = st.slider("Máx. linhas para varrer", 10, 100, 50)
    score_thresh = st.slider("Score minimo para aceitar", 0.0, 1.0, 0.55)
    # Strategy is implicit now (Hybrid fallback)
    # strategy = st.selectbox("Estratégia", ["Híbrida (Keywords + Conteúdo)", "Somente palavras-chave"])

if st.button("🚀 Executar Detecção Automática", type="primary"):
    results = {}
    structured_dfs = []
    
    progress_bar = st.progress(0)
    
    for i, sheet in enumerate(sheets):
        df_sheet = grouped.get_group(sheet)
        
        # Reset index
        df_sheet = df_sheet.reset_index(drop=True)
        # Drop 'aba' col for detection
        df_det = df_sheet.drop(columns=['aba'], errors='ignore')
        
        # Detect
        det_result = detect_header(df_det, max_scan_lines=max_scan, score_threshold=score_thresh)
        results[sheet] = det_result
        
        # Process and Store
        header_idx = det_result['header_row_idx']
        mapping = det_result['mapping']
        
        # Use header_idx + 1 for data start, unless it's -1 (inference mode)
        if header_idx == -1:
            data_start = 0
            # Rename columns based on mapping directly
            # mapping keys are current column names
            df_struct = df_det.iloc[data_start:].copy()
            # Normalize column names?
            # We want to rename matched cols to std, others leave as is
            rename_dict = {k: v for k, v in mapping.items()}
            df_struct.rename(columns=rename_dict, inplace=True)
            
        else:
            data_start = header_idx + 1
            df_struct = df_det.iloc[data_start:].copy()
            
            # Rename columns based on Header Row Values
            header_vals = df_det.iloc[header_idx].astype(str).tolist()
            current_cols = df_det.columns.tolist()
            
            # Create a rename dict: { CurrentColName: StandardName }
            # Mapping is { HeaderValue: StandardName }
            # Need to map CurrentCol -> HeaderValue -> StandardName
            
            final_rename = {}
            for col_idx, col_name in enumerate(current_cols):
                if col_idx < len(header_vals):
                    h_val = header_vals[col_idx]
                    if h_val in mapping:
                        final_rename[col_name] = mapping[h_val]
                    else:
                        final_rename[col_name] = h_val # Use header value as name
            
            df_struct.rename(columns=final_rename, inplace=True)
            
        # Deduplicate columns to avoid InvalidIndexError in pd.concat
        # (If header row had duplicate values, or if we ignored some columns)
        cols = pd.Series(df_struct.columns)
        for dup in cols[cols.duplicated()].unique(): 
            cols[cols == dup] = [f"{dup}_{i}" for i in range(sum(cols == dup))]
        df_struct.columns = cols
        
        # Re-inject 'aba' at start
        df_struct.insert(0, 'aba', sheet)
        structured_dfs.append(df_struct)
        
        progress_bar.progress((i + 1) / len(sheets))
        
    st.session_state['detection_results'] = results
    
    # Safe Concat
    if structured_dfs:
        try:
            st.session_state['df_structured'] = pd.concat(structured_dfs, ignore_index=True)
            st.success("Detecção concluída!")
        except Exception as e:
            st.error(f"Erro ao consolidar dados: {e}")
            st.session_state['df_structured'] = None
    else:
        st.warning("Nenhum dado estruturado gerado.")

# --- RESULTS DISPLAY ---
if 'detection_results' in st.session_state:
    results = st.session_state['detection_results']
    
    summary_data = []
    
    for sheet in sheets:
        res = results.get(sheet)
        if not res: continue
        
        score = res['score']
        method = res.get('method', 'keyword_scan')
        is_success = score >= score_thresh or method == 'content_inference'
        icon = "✅" if is_success else "❌"
        
        # UI Tweak: Removed Score as requested
        with st.expander(f"{icon} Aba: {sheet} (Linha Cab: {res['header_row_idx']}, Método: {method})"):
            c1, c2 = st.columns([1, 2])
            
            c1.write(f"**Status:** {'Detectado' if is_success else 'Falha'}")
            c1.write(f"**Linha Cabeçalho:** {res['header_row_idx']}")
            # c1.metric("Score", f"{score:.2f}") # Removed
            
            c2.write("**Mapeamento Encontrado:**")
            c2.json(res['mapping'])
            
            st.write("Preview (5 primeiras linhas de dados):")
            # Show preview from df_structured filtered
            if 'df_structured' in st.session_state and st.session_state['df_structured'] is not None:
                df_s = st.session_state['df_structured']
                # Safeguard against string/int type mismatch in 'aba'
                try:
                    df_preview = df_s[df_s['aba'] == sheet].head(5)
                    st.dataframe(df_preview)
                except:
                    st.warning("Não foi possível filtrar o preview.")
            else:
                st.warning("Preview indisponível (Erro na consolidação).")
                
        # Summary row
        mapping = res['mapping']
        summary_data.append({
            "Aba": sheet,
            "Header Row": res['header_row_idx'],
            "Method": method,
            # "Score": round(score, 2), # Removed
            "Descricao": next((k for k,v in mapping.items() if v=='descricao'), None),
            "Unidade": next((k for k,v in mapping.items() if v=='unidade'), None),
            "Qtd": next((k for k,v in mapping.items() if v=='quantidade'), None),
            "PrecoResult": next((k for k,v in mapping.items() if v=='preco_unitario'), None),
        })

    st.divider()
    st.subheader("Resumo Geral")
    st.dataframe(pd.DataFrame(summary_data))
    
    if st.button("Confirmar e Avançar para ETL ➡️", type="primary"):
        st.switch_page("pages/3_Normalizacao_ETL.py")
        
    if st.button("⬅️ Voltar para Upload"):
        st.switch_page("pages/1_Processar_Orcamento.py")
