import pandas as pd
import unidecode
import re

# Dicionário de Sinônimos
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

def normalize_text(text):
    if not isinstance(text, str):
        return str(text).lower().strip()
    text = text.lower().strip()
    text = unidecode.unidecode(text)
    text = " ".join(text.split())
    return text

def calculate_row_score(row_values):
    row_strs = [normalize_text(v) for v in row_values]
    score = 0.0
    found_fields = set()
    
    for cell in row_strs:
        for field, keywords in CANDIDATOS.items():
            if not cell: continue
            match = False
            for k in keywords:
                if k == cell: match = True
                elif k in cell or cell in k: match = True
                
                if match:
                    if field == 'descricao': points = 1.0
                    elif field == 'quantidade': points = 1.0
                    else: points = 0.7
                    
                    if field not in found_fields:
                        score += points
                        found_fields.add(field)
                    break
            if match: break
            
    max_possible = 4.1
    normalized = min(score / max_possible, 1.0)
    return normalized

def map_columns(header_row_values):
    mapping = {k: None for k in CANDIDATOS.keys()}
    priority = ['descricao', 'quantidade', 'unidade', 'preco_unitario', 'preco_total']
    col_scores = []
    
    for idx, val in enumerate(header_row_values):
        val_norm = normalize_text(val)
        if not val_norm: continue
        
        for field, keywords in CANDIDATOS.items():
            for k in keywords:
                if k in val_norm or val_norm in k:
                    col_scores.append({'idx': idx, 'field': field, 'val': val})
                    break
    
    used_cols = set()
    res_map = {}
    for target in priority:
        candidates = [c for c in col_scores if c['field'] == target and c['idx'] not in used_cols]
        if candidates:
            chosen = candidates[0]
            res_map[target] = header_row_values[chosen['idx']]
            used_cols.add(chosen['idx'])
            
    return res_map

# --- INFERENCE HELPERS ---

def is_potential_code(series):
    s_strs = series.astype(str).str.strip()
    valid = s_strs[s_strs != 'nan'][s_strs != '']
    if len(valid) == 0: return 0.0
    mean_len = valid.str.len().mean()
    if mean_len > 25: return 0.0
    pattern_matches = valid.str.match(r'^[A-Z0-9.\-/]+$', case=False).mean()
    return pattern_matches

def infer_columns_from_data(df):
    sample = df.head(50)
    mapping = {}
    used_cols = set()
    
    # 1. DESCRIÇÃO
    text_cols = []
    for col in sample.columns:
        s = sample[col].astype(str)
        # Check non-numeric and length
        is_numeric = pd.to_numeric(sample[col], errors='coerce').notnull().mean() > 0.8
        mean_len = s.str.len().mean()
        
        if not is_numeric and mean_len > 15:
            text_cols.append((col, mean_len))
            
    if text_cols:
        best_desc = sorted(text_cols, key=lambda x: x[1], reverse=True)[0][0]
        # Map: ColName -> 'descricao'
        mapping[best_desc] = 'descricao'
        used_cols.add(best_desc)
        
    # 2. UNIDADE
    known_units = {'m', 'm2', 'm3', 'kg', 'un', 'h', 'h.a', 'vb', 'cj', 'l', 'par', 'pç', 'sc', 'gl'}
    best_unit = None
    best_unit_score = 0
    
    for col in sample.columns:
        if col in used_cols: continue
        s = sample[col].astype(str).str.strip().str.lower()
        valid = s[s != 'nan'][s != '']
        if len(valid) == 0: continue
        
        match_rate = valid.apply(lambda x: x in known_units).mean()
        mean_len = valid.str.len().mean()
        
        score = match_rate * 2.0
        if mean_len < 6: score += 0.5
        
        if score > best_unit_score and score > 0.5:
            best_unit_score = score
            best_unit = col
            
    if best_unit:
        mapping[best_unit] = 'unidade'
        used_cols.add(best_unit)
        
    # 3. CODIGO (Optional/Stored only if useful)
    best_code = None
    best_code_score = 0
    for col in sample.columns:
        if col in used_cols: continue
        score = is_potential_code(sample[col])
        if score > best_code_score and score > 0.7:
            best_code_score = score
            best_code = col
    
    # 4. QUANTIDADE / PRECO
    numeric_cols = []
    for col in sample.columns:
        if col in used_cols: continue
        is_num = pd.to_numeric(sample[col], errors='coerce').notnull().mean() > 0.7
        if is_num:
            numeric_cols.append(col)
            
    if numeric_cols:
        mapping[numeric_cols[0]] = 'quantidade'
        used_cols.add(numeric_cols[0])
    
    if len(numeric_cols) > 1:
        mapping[numeric_cols[1]] = 'preco_unitario'
        used_cols.add(numeric_cols[1])
        
    return mapping

def detect_header(df, max_scan_lines=50, score_threshold=0.5):
    best_row_idx = None
    best_score = -1.0
    best_mapping = {}
    
    limit = min(max_scan_lines, len(df))
    
    for i in range(limit):
        row = df.iloc[i]
        score = calculate_row_score(row)
        if score > best_score:
            best_score = score
            best_row_idx = i
            
    final_output = {
        "header_row_idx": best_row_idx,
        "score": best_score,
        "mapping": {},
        "method": "keyword_scan"
    }

    if best_score >= score_threshold:
        header_row = df.iloc[best_row_idx]
        best_mapping = map_columns(header_row)
        final_output["mapping"] = best_mapping
    else:
        # Fallback Inference
        inferred_map = infer_columns_from_data(df)
        if 'descricao' in inferred_map.values():
            final_output["header_row_idx"] = -1 
            final_output["score"] = 0.6 
            final_output["method"] = "content_inference"
            final_output["mapping"] = inferred_map

    return final_output
