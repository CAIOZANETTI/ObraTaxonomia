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
        # para ver se 'quantidade' é numero, etc.
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    # Validar threshold
    status = "ok"
    if best_score < threshold:
        status = "nao_detectado"
        if best_score < 0.1: # Muito ruim
             best_idx = 0 # Fallback para primeira linha ou None
        # Mesmo não detectado, retornamos o "melhor" palpite marcando status
        
    # Fazer mapeamento usando a linha vencedora
    if best_idx is not None:
        header_vals = df.iloc[best_idx].astype(str).tolist()
        mapping = map_columns(header_vals)
    else:
        mapping = {}
        
    return {
        "header_row": best_idx,
        "score": best_score,
        "map": mapping,
        "status": status
    }


# --- 3. MAIN LOGIC ---

if 'df_all' not in st.session_state or st.session_state['df_all'] is None:
    st.warning("⚠️ Nenhum arquivo carregado. Por favor, vá para a Página 1 e faça o upload.")
    st.stop()

df_all = st.session_state['df_all']
unique_sheets = df_all['aba'].unique()

st.info(f"Processando {len(unique_sheets)} abas...")

# Store results
if 'header_detection' not in st.session_state:
    st.session_state['header_detection'] = {}

detection_results = {}
structured_dfs = []

# Botão para (re)detectar
if st.button("🔄 Executar Detecção Automática", type="primary"):
    with st.spinner("Analisando abas..."):
        for aba in unique_sheets:
            df_sheet = df_all[df_all['aba'] == aba].copy()
            # Reset index para garantir que iloc bata com "varias linhas"
            df_sheet.reset_index(drop=True, inplace=True)
            
            res = detect_header(df_sheet, max_scan_lines, score_threshold)
            detection_results[aba] = res
        
        st.session_state['header_detection'] = detection_results
        st.success("Detecção concluída!")

# Se nao tiver resultados ainda, tenta rodar ou pede
if not st.session_state['header_detection']:
    st.write("Clique acima para iniciar.")
else:
    # Exibir result em Expanders
    
    full_clean_data = [] # Para gerar o df_structured final
    
    for aba in unique_sheets:
        res = st.session_state['header_detection'].get(aba, {})
        status = res.get('status', 'n/a')
        score = res.get('score', 0)
        h_row = res.get('header_row', -1)
        
        icon = "✅" if status == 'ok' else "❌"
        title = f"{icon} Aba: {aba} (Linha {h_row}, Score {score:.2f})"
        
        with st.expander(title):
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.write(f"**Status:** {status}")
                st.write(f"**Linha Cabeçalho:** {h_row}")
                st.metric("Score", f"{score:.2f}")
                
            with c2:
                st.write("**Mapeamento Encontrado:**")
                st.json(res.get('map', {}))
                
            # Preview (Data interpreted)
            if h_row is not None and h_row >= 0:
                df_sheet_raw = df_all[df_all['aba'] == aba].reset_index(drop=True)
                
                # Create "structured" view for this sheet
                # Use row at h_row as columns
                # Only keep rows > h_row
                
                try:
                    cols = df_sheet_raw.iloc[h_row].astype(str).tolist()
                    # De-duplicate cols
                    seen = {}
                    final_cols = []
                    for c in cols:
                        if c not in seen:
                            seen[c] = 0
                            final_cols.append(c)
                        else:
                            seen[c] += 1
                            final_cols.append(f"{c}_{seen[c]}")
                            
                    df_view = df_sheet_raw.iloc[h_row+1:].copy()
                    df_view.columns = final_cols
                    
                    st.write("Preview (5 primeiras linhas de dados):")
                    st.dataframe(df_view.head(5), hide_index=True)
                
                    # Add to full structure
                    # Create normalized columns based on map
                    mapping = res.get('map', {})
                    # Add standard columns
                    # We need to map from 'Original Name' -> 'Standard Field'
                    # The dict is {Standard: Original}
                    
                    # Invert mapping (assuming 1-to-1 in map logic mostly, but check duplicates)
                    inv_map = {v: k for k, v in mapping.items() if v is not None}
                    
                    # Select only mapped cols and rename
                    # Note: cols in df_view are the strings found in row h_row.
                    
                    # Filter columns that are in the map
                    cols_to_keep = []
                    rename_dict = {}
                    
                    for col in df_view.columns:
                        if col in inv_map:
                            field_name = inv_map[col]
                            rename_dict[col] = field_name
                            cols_to_keep.append(col)
                    
                    df_std = df_view[cols_to_keep].rename(columns=rename_dict).copy()
                    df_std['aba'] = aba # Keep aba
                    
                    # Ensure all 5 keys exist
                    for k in CANDIDATOS.keys():
                        if k not in df_std.columns:
                            df_std[k] = None
                            
                    # Reorder
                    df_std = df_std[['aba', 'descricao', 'unidade', 'quantidade', 'preco_unitario', 'preco_total']]
                    full_clean_data.append(df_std)

                except Exception as e:
                    st.error(f"Erro ao gerar preview: {e}")

    # Summary Table
    st.divider()
    st.subheader("Resumo Final")
    
    summary_data = []
    for aba, res in st.session_state['header_detection'].items():
        m = res.get('map', {})
        row = {
            'Aba': aba,
            'Header Row': res.get('header_row'),
            'Score': f"{res.get('score', 0):.2f}",
            'Descricao': m.get('descricao'),
            'Unidade': m.get('unidade'),
            'Qtd': m.get('quantidade'),
            'PrecoResult': m.get('preco_total')
        }
        summary_data.append(row)
    
    st.dataframe(pd.DataFrame(summary_data))
    
    # Save Structured DF
    if full_clean_data:
        df_structured_final = pd.concat(full_clean_data, ignore_index=True)
        st.session_state["df_structured"] = df_structured_final
        st.write(f"Total de linhas extraídas: {len(df_structured_final)}")
        
        if not df_structured_final.empty:
            csv = df_structured_final.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Baixar Dados Estruturados (CSV)", csv, "dados_estruturados.csv", "text/csv")
