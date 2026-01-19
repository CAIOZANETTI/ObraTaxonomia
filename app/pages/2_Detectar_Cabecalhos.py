import streamlit as st
import pandas as pd
import unidecode

st.set_page_config(
    page_title="Detectar Cabeçalhos",
    page_icon="🕵️",
    layout="wide"
)

# --- 1. CONFIG & DICTIONARY ---

st.title("🕵️ Detecção de Cabeçalhos e Mapeamento de Colunas")

# Dicionário de Sinônimos (Fixo/Editável via código por enquanto)
CANDIDATOS = {
    "descricao": [
        "descricao", "descrição", "item", "itens", "servico", "serviço",
        "produto", "nome", "especificacao", "especificação", "material", "insumo",
        "discriminacao", "discriminação"
    ],
    "unidade": [
        "un", "und", "unid", "unidade", "u.m", "um", "un. med", "un_med", "medida"
    ],
    "quantidade": [
        "qtd", "qtde", "quantidade", "quantidades", "quant", "qnt", "qte", "volume"
    ],
    "preco_unitario": [
        "preco unit", "preço unit", "preco unitario", "preço unitário",
        "p.u", "pu", "valor unit", "vl unit", "unitario", "unitário"
    ],
    "preco_total": [
        "preco total", "preço total", "total", "valor total", "vl total",
        "subtotal", "parcial", "valor", "montante"
    ]
}

# --- Sidebar Controls ---
st.sidebar.header("Configurações de Detecção")
max_scan_lines = st.sidebar.slider("Máx. linhas para varrer", 20, 300, 80)
score_threshold = st.sidebar.slider("Score mínimo para aceitar", 0.0, 1.0, 0.55, step=0.05)
strategy = st.sidebar.selectbox("Estratégia", [
    "Somente palavras-chave",
    "Palavras-chave + validação por tipo (número/moeda)", # Placeholder logic
])


# --- IMPORTS ---
import sys
import os

# Add scripts to path if needed (though running from root usually works, Streamlit pages are weird)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

try:
    from header_utils import detect_header, CANDIDATOS
except ImportError:
    # Fallback to local import if structure differs (e.g. deployed)
    # or simple hacky import
    sys.path.append('scripts')
    from header_utils import detect_header, CANDIDATOS

# --- UI LOGIC ---

# --- UI LOGIC ---

if 'df_all' not in st.session_state:
    st.warning("Por favor, faça o upload do arquivo na Página 1.")
    st.stop()

df_all = st.session_state['df_all']
sheets = df_all['aba'].unique().tolist()
grouped = df_all.groupby('aba')

st.header(f"Processando {len(sheets)} abas...")

# Sidebar Config
with st.sidebar:
    st.header("Configurações de Detecção")
    max_scan = st.slider("Máx. linhas para varrer", 10, 100, 50)
    score_thresh = st.slider("Score minimo para aceitar", 0.0, 1.0, 0.55)
    strategy = st.selectbox("Estratégia", ["Híbrida (Keywords + Conteúdo)", "Somente palavras-chave"])

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
            
        # Re-inject 'aba'
        df_struct['aba'] = sheet
        structured_dfs.append(df_struct)
        
        progress_bar.progress((i + 1) / len(sheets))
        
    st.session_state['detection_results'] = results
    st.session_state['df_structured'] = pd.concat(structured_dfs, ignore_index=True)
    st.success("Detecção concluída!")

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
        
        with st.expander(f"{icon} Aba: {sheet} (Linha {res['header_row_idx']}, Score {score:.2f}, Método: {method})"):
            c1, c2 = st.columns([1, 2])
            
            c1.write(f"**Status:** {'Detectado' if is_success else 'Falha'}")
            c1.write(f"**Linha Cabeçalho:** {res['header_row_idx']}")
            c1.metric("Score", f"{score:.2f}")
            
            c2.write("**Mapeamento Encontrado:**")
            c2.json(res['mapping'])
            
            st.write("Preview (5 primeiras linhas de dados):")
            # Show preview from df_structured filtered
            if 'df_structured' in st.session_state:
                df_s = st.session_state['df_structured']
                st.dataframe(df_s[df_s['aba'] == sheet].head(5))
                
        # Summary row
        mapping = res['mapping']
        summary_data.append({
            "Aba": sheet,
            "Header Row": res['header_row_idx'],
            "Method": method,
            "Score": round(score, 2),
            "Descricao": next((k for k,v in mapping.items() if v=='descricao'), None),
            "Unidade": next((k for k,v in mapping.items() if v=='unidade'), None),
            "Qtd": next((k for k,v in mapping.items() if v=='quantidade'), None),
            "PrecoResult": next((k for k,v in mapping.items() if v=='preco_unitario'), None),
        })

    st.divider()
    st.subheader("Resumo Geral")
    st.dataframe(pd.DataFrame(summary_data))
    
    if st.button("Confirmar e Avançar para ETL"):
        st.switch_page("pages/3_Normalizacao_ETL.py")
