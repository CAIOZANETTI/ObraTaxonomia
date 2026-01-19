import pandas as pd
import numpy as np
import unidecode

# --- Helper Functions Copy (Simulated import due to Streamlit structure) ---
def normalize_text(text, remove_accents=False):
    if not isinstance(text, str):
        return str(text) if pd.notnull(text) else ""
    text = text.strip()
    text = text.replace('\u00A0', ' ').replace('\r', '').replace('\n', '')
    if remove_accents:
        text = unidecode.unidecode(text)
    text = " ".join(text.split())
    text = text.lower()
    return text

def normalize_colnames(df):
    new_cols = []
    seen = {}
    for col in df.columns:
        c_str = str(col).strip().lower()
        c_str = unidecode.unidecode(c_str)
        c_str = "_".join(c_str.split())
        c_str = c_str.replace('\u00A0', '').replace('\r', '').replace('\n', '')
        if c_str in seen:
            seen[c_str] += 1
            c_str = f"{c_str}__{seen[c_str] + 1}"
        else:
            seen[c_str] = 0
        new_cols.append(c_str)
    df_out = df.copy()
    df_out.columns = new_cols
    return df_out

def suggest_drop_columns(df):
    suggestions = []
    for col in df.columns:
        if df[col].isnull().all():
            suggestions.append(col)
        elif col != 'aba' and df[col].nunique(dropna=False) <= 1:
            suggestions.append(col)
        elif pd.Series([col]).astype(str).str.contains(r'^(unnamed|index|linha|row|coluna_vazia|sem_nome)', case=False, regex=True).any():
            suggestions.append(col)
    return suggestions

def parse_numbers(df):
    df_out = df.copy()
    target_keywords = ["qtd", "quant", "preco", "valor", "total", "unit", "parcial"]
    
    for col in df.columns:
        if df[col].dtype.kind in 'iuf': continue
        if any(k in col.lower() for k in target_keywords):
            def safe_parse(x):
                if not x or str(x).lower() == 'nan': return None
                val = str(x).strip().replace("R$", "").strip()
                # BR format fix
                if '.' in val and ',' in val:
                    val = val.replace('.', '').replace(',', '.')
                elif ',' in val:
                    val = val.replace(',', '.')
                return val
            
            parsed = df[col].apply(safe_parse)
            numeric = pd.to_numeric(parsed, errors='coerce')
            # Check valid ratio (simple check for test)
            if numeric.notnull().sum() > 0:
                df_out[col] = numeric
    return df_out

# --- Tests ---
def test_etl():
    print("--- Testing ETL Logic ---")
    
    # Data
    data = {
        "  Item Descrição  ": ["Concreto", "Aço CA-50", "  Tijolo  ", np.nan],
        "Unidade (Un)": ["m3", "kg", "unid", "m2"],
        "Qtd.": ["1.000,50", "500", "200,00", "invalid"],
        "Preco Unit": ["R$ 450,00", "10,50", "1.20", None],
        "Unnamed: 5": [None, None, None, None], # Empty
        "Constante": ["X", "X", "X", "X"] # Constant
    }
    df = pd.DataFrame(data)
    
    # 1. Colnames
    df_norm = normalize_colnames(df)
    print("Cols:", df_norm.columns.tolist())
    assert "item_descricao" in df_norm.columns
    assert "unidade_(un)" in df_norm.columns
    assert "unnamed:_5" in df_norm.columns
    
    # 2. Strings
    # Test normalization on item_descricao
    # "  Tijolo  " -> "tijolo"
    val = normalize_text(df['  Item Descrição  '][2])
    print(f"Norm String: '{val}'")
    assert val == "tijolo"
    
    # 3. Drop Suggestions
    drop_sug = suggest_drop_columns(df_norm)
    print("Drop suggestions:", drop_sug)
    # unnamed_5 is 100% null ? yes.
    # constante is unique? yes.
    assert "unnamed:_5" in drop_sug
    assert "constante" in drop_sug
    
    # 4. Parse Numbers
    # Qtd. -> "1.000,50" -> 1000.5
    df_parsed = parse_numbers(df_norm)
    print("Qtd parsed:", df_parsed['qtd.'].tolist())
    assert df_parsed['qtd.'][0] == 1000.5
    assert df_parsed['preco_unit'][0] == 450.0

if __name__ == "__main__":
    test_etl()
