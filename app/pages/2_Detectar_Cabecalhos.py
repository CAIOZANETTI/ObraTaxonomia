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


# --- 2. HELPER FUNCTIONS ---

def normalize_text(text):
    if not isinstance(text, str):
        return str(text).lower().strip()
    # Lowercase, remove accents, collapse spaces
    text = text.lower().strip()
    text = unidecode.unidecode(text)
    text = " ".join(text.split())
    return text

def calculate_row_score(row_values):
    """
    Calcula score de uma linha baseado nos matches com CANDIDATOS.
    """
    row_strs = [normalize_text(v) for v in row_values]
    
    score = 0.0
    found_fields = set()
    
    # Matches
    for cell in row_strs:
        for field, keywords in CANDIDATOS.items():
            # Check for tokens or substrings
            # Logic: keyword in cell OR cell in keyword (if cell is not empty/too short)
            if not cell:
                continue
            
            match = False
            for k in keywords:
                # Caso exato ou substring significativa
                if k == cell: 
                    match = True
                elif k in cell or cell in k: 
                    # Evitar falso positivos com strings muito curtas in longas
                    # mas o prompt pede substring "preco unit" em "Preço Unitário (R$)"
                    match = True
                
                if match:
                    # Pontuação
                    if field == 'descricao': points = 1.0
                    elif field == 'quantidade': points = 1.0
                    else: points = 0.7
                    
                    if field not in found_fields:
                        score += points
                        found_fields.add(field)
                    break # Next cell
            if match: break # Next cell (cell assigned to one field)

    # Max Score theoretico = 1+1+0.7+0.7+0.7 = 4.1
    # Normalize
    max_possible = 4.1
    normalized = min(score / max_possible, 1.0)
    
    return normalized

def map_columns(header_row_values):
    """
    Mapeia colunas para os 5 campos alvo.
    Retorna dict {target_field: original_col_name}
    """
    mapping = {k: None for k in CANDIDATOS.keys()}
    
    # Prioridade de resolução de conflitos
    priority = ['descricao', 'quantidade', 'unidade', 'preco_unitario', 'preco_total']
    
    # Para cada coluna original, ver qual campo ela melhor representa
    # Se houver conflito (coluna serve para varios), ou duplicidade (varias colunas para mesmo campo)
    # Aqui faremos uma passagem gananciosa simples mas respeitando prioridade de campo se conflito.
    
    # Mas o problema comum é: varias colunas podem parecer "quantidade".
    # Vamos pontuar cada coluna para cada campo.
    
    col_scores = [] # list of {col_idx, field, score} (simples match bool)
    
    for idx, val in enumerate(header_row_values):
        val_norm = normalize_text(val)
        if not val_norm: continue
        
        for field, keywords in CANDIDATOS.items():
            for k in keywords:
                if k in val_norm or val_norm in k:
                    col_scores.append({'idx': idx, 'field': field, 'val': val})
                    break
    
    # Resolver
    used_cols = set()
    res_map = {}
    
    # Itera na ordem de prioridade dos CAMPOS
    for target in priority:
        # Pega candidatos para esse campo
        candidates = [c for c in col_scores if c['field'] == target and c['idx'] not in used_cols]
        if candidates:
            # Pega o primeiro (ou melhor lógica se tivesse score detalhado por coluna)
            chosen = candidates[0]
            res_map[target] = header_row_values[chosen['idx']] # Nome original da coluna (pode ser int se não tiver header real no excel, mas aqui pegamos valores da linha)
            used_cols.add(chosen['idx'])
            
    return res_map

def detect_header(df, max_lines, threshold):
    """
    Varre df e retorna (header_idx, score, mapping_dict)
    """
    best_idx = None
    best_score = -1.0
    
    # Varredura
    scan_limit = min(len(df), max_lines)
    
    for i in range(scan_limit):
        row_vals = df.iloc[i].astype(str).tolist()
        score = calculate_row_score(row_vals)
        
        # Bônus ou penalidade de tipo (placeholder simplificado)
        # Se selecionado na UI, poderiamos inspecionar linhas abaixo (i+1 a i+5) 
    best_mapping = {}
    
    # 1. Explicit Header Scan
    limit = min(max_scan_lines, len(df))
    
    for i in range(limit):
        row = df.iloc[i]
        score = calculate_row_score(row)
        
        if score > best_score:
            best_score = score
            best_row_idx = i
            
    # 2. Decision Logic
    final_output = {
        "header_row_idx": best_row_idx,
        "score": best_score,
        "mapping": {},
        "method": "keyword_scan"
    }

    if best_score >= score_threshold:
        # Keyword Success
        header_row = df.iloc[best_row_idx]
        best_mapping = map_columns(header_row)
        final_output["mapping"] = best_mapping
    else:
        # Fallback: Inference from Data Patterns
        # Assuming no header row, so data starts at 0
        inferred_map = infer_columns_from_data(df)
        
        # Requirements for acceptance: Must have at least Description found
        if 'descricao' in inferred_map:
            # Construct a "virtual" mapping
            # The map_columns expects { "Header Name": "Standard" }
            # But here we have { ColumnIndex/Name: "Standard" }
            # Since we assume NO header row, we map the Column Name directly.
            
            # Check if we should use row 0 or None? 
            # If we say header_row_idx = -1, it means "No Header, use default cols".
            
            final_output["header_row_idx"] = 0 # Data starts at 0 (or strictly speaking -1 but lets use 0 as "first row of block")
            # Wait, if data starts at 0, header is theoretical.
            # Page logic uses df.iloc[header_row_idx+1:].
            # If we want to include row 0 in data, we should set header_row_idx = -1.
            final_output["header_row_idx"] = -1 
            final_output["score"] = 0.6 # Synthetic confidence
            final_output["method"] = "content_inference"
            
            # Invert mapping for consistency: { "Col Name": "Standard" }
            # The inferred_map is already { "Col Name": "Standard" }.
            # But the UI expects mapping keys to be values of a header row.
            # If header is -1, keys are the column names (0, 1... or 'A', 'B'...).
            final_output["mapping"] = inferred_map

    return final_output

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
