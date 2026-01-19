import unidecode

# --- Copied Logic from Page 2 ---
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
    return min(score / 4.1, 1.0)

def map_columns(header_row_values):
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

# --- Tests ---
def test_heuristics():
    # Case 1: Ideal Header
    row1 = ["Item", "Descrição", "Unid.", "Qtd", "Preço Unit.", "Total"]
    score1 = calculate_row_score(row1)
    print(f"Row 1 Score: {score1:.2f}")
    assert score1 > 0.8
    
    mapping1 = map_columns(row1)
    print(f"Row 1 Map: {mapping1}")
    assert mapping1['descricao'] == 'Descrição' or mapping1['descricao'] == 'Item'
    assert mapping1['quantidade'] == 'Qtd'
    assert mapping1['preco_total'] == 'Total'
    
    # Case 2: Messy Header
    row2 = ["", "Discriminação dos Serviços", "UN", "QUANT.", "P. UNITARIO (R$)", "VL. TOTAL"]
    score2 = calculate_row_score(row2)
    print(f"Row 2 Score: {score2:.2f}")
    assert score2 > 0.6
    
    mapping2 = map_columns(row2)
    print(f"Row 2 Map: {mapping2}")
    assert mapping2['descricao'] == 'Discriminação dos Serviços'
    assert mapping2['preco_unitario'] == 'P. UNITARIO (R$)'

    # Case 3: Random text (should be low score)
    row3 = ["Engenheiro Responsável", "Data: 2023", "Obra 123", "", ""]
    score3 = calculate_row_score(row3)
    print(f"Row 3 Score: {score3:.2f}")
    assert score3 < 0.3

if __name__ == "__main__":
    test_heuristics()
