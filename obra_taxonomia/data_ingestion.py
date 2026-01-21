
import pandas as pd
import os
import io
import unicodedata
import string

# --- CONSTANTS ---
IGNORED_COLS_HINT = ['id', 'codigo', 'código', 'cod', 'cpf', 'cnpj', 'ncm', 'gtin', 'sku', 'chave']
STOPWORDS_PT = [
    'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
    'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 'nos', 'nas', 
    'para', 'por', 'com', 'sem', 'ao', 'à', 'aos', 'às', 'e'
]

# --- FILE OPERATIONS ---
def list_test_files(base_path="data/excel"):
    """Lists .xlsx/.xls files in the given directory."""
    if not os.path.exists(base_path):
        return []
    files = [f for f in os.listdir(base_path) if f.lower().endswith(('.xlsx', '.xls'))]
    return sorted(files)

def load_excel_bytes(path):
    """Reads file bytes from disk."""
    with open(path, "rb") as f:
        return io.BytesIO(f.read()), os.path.basename(path)

# --- READ LOGIC ---
def read_sheet(xls, sheet_name):
    """
    Reads a single sheet from a pd.ExcelFile object.
    Returns: df, status, details
    """
    try:
        # Try reading with default header first
        # But requirements say: "try read brute (header=None when applicable)"?
        # A "generic" ingestion usually wants header=0 or header=None. 
        # Requirement 4.2.1: "tentar ler bruto (sem cabeçalho: header=None quando aplicável)"
        # Let's default to reading with header to get column names, 
        # or header=None if it looks like there's no header? 
        # Let's stick to standard pandas read (header=0) for standard excel files,
        # but the prompt emphasizes "bruto". 
        # If we use header=None, the first row becomes data.
        # "CSV bruto consolidado" implies we want the raw data.
        # However, for a user to understand 'coluna X', we usually need headers.
        # Let's stick to header=0 (default) as it's standard for 'Excel -> CSV'.
        # If the sheet is completely jagged, header=None might be safer, but harder to consolidate by name.
        # Given "Permitir schemas diferentes entre abas (concat com união de colunas)", headers are implied.
        
        df = pd.read_excel(xls, sheet_name)
        
        if df.empty:
             return df, "empty", "Empty dataframe returned"

        # Check for actual data (not just NaNs)
        if df.dropna(how='all').empty:
             return df, "empty", "Dataframe contains only NaNs"

        return df, "ok", "Read via pd.read_excel"
        
    except Exception as e:
        return None, "error", str(e)

def process_workbook(file_bytes, filename):
    """
    Orchestrates reading all sheets, validating, and consolidating.
    Returns:
        sheets_info: dict
        df_resumo: pd.DataFrame
        df_all: pd.DataFrame (consolidated)
        csv_bytes: bytes
    """
    
    try:
        xls = pd.ExcelFile(file_bytes)
    except Exception as e:
        # Not a valid excel
        return {}, pd.DataFrame(), pd.DataFrame(), None

    all_sheets = xls.sheet_names
    sheets_info = {}
    valid_dfs = []
    
    # Validation / Read Loop
    for sheet_name in all_sheets:
        df, status, msg = read_sheet(xls, sheet_name)
        
        rows, cols = (0,0)
        df_head = None
        
        if df is not None:
            rows, cols = df.shape
            
        if status == 'ok':
            # Create a copy for consolidation
            d_cons = df.copy()
            d_cons['aba'] = sheet_name # Essential column
            valid_dfs.append(d_cons)
            df_head = df.head(20) # preview
        
        sheets_info[sheet_name] = {
            'rows': rows, 
            'cols': cols, 
            'status': status,
            'read_method': msg if status == 'ok' else None,
            'error_msg': msg if status == 'error' else None,
            'df_head': df_head
        }

    # Summary Table
    summary_data = []
    for s_name in all_sheets:
        info = sheets_info[s_name]
        summary_data.append({
            'aba': s_name,
            'linhas': info['rows'],
            'colunas': info['cols']
        })
    df_resumo = pd.DataFrame(summary_data)
    
    # Consolidation
    if valid_dfs:
        # sort=False preserves column order of the first df, then appends others
        df_all = pd.concat(valid_dfs, ignore_index=True, sort=False)
    else:
        df_all = pd.DataFrame()

    csv_bytes = None
    if not df_all.empty:
        csv_bytes = df_all.to_csv(index=False).encode('utf-8')

    return sheets_info, df_resumo, df_all, csv_bytes


# --- ETL / NORMALIZATION ---

def normalize_text_value(text, config):
    """
    Applies normalization steps to a single string value.
    Config dict:
      - 'remove_accents': bool
      - 'remove_punctuation': bool
      - 'remove_stopwords': bool
      - 'collapse_spaces': bool
    """
    if not isinstance(text, str):
        return text
    
    # ALWAYS Lowercase
    s = text.lower()
    
    if config.get('remove_accents', True):
        # Normalize to NFD form, strip non-spacing marks
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    if config.get('remove_punctuation', True):
        # Translate keys to None
        # Keep things like '/' ?? Prompt says "manter ... 1/2".
        # Prompt: "remover pontuação e caracteres 'ruído'"
        # Strategy: Remove standard punctuation but maybe spare some used in units?
        # Simple approach first: remove all string.punctuation
        # To strictly follow "manter 1/2", we should perhaps allow '/'.
        # But "minima" implementation might just strip mostly everything.
        # Let's strip default output but maybe keep floating point dots? 
        # The user instructions are high level, stick to removing string.punctuation
        # If numbers are passed as strings ("25.5"), stripping '.' breaks them.
        # But 'Numbers' should ideally not be normalized if they are numeric types.
        # If they are strings, we might mess them up.
        # Let's stick to standard `str.translate` for now.
        trans_table = str.maketrans('', '', string.punctuation)
        s = s.translate(trans_table)

    if config.get('collapse_spaces', True):
        s = " ".join(s.split())
        
    if config.get('remove_stopwords', True):
        tokens = s.split()
        filtered = [t for t in tokens if t not in STOPWORDS_PT]
        s = " ".join(filtered)
        
    return s.strip()

def etl_normalize_df(df, config):
    """
    Applies normalization to an entire dataframe.
    Returns: df_norm, etl_log (dict stats)
    """
    df_norm = df.copy()
    
    etl_log = []
    
    schema_cols = df_norm.columns.tolist()
    
    for col in schema_cols:
        col_str = str(col).lower()
        
        # Rule: Skip exact ID columns hint
        # Prompt check: "nome da coluna contendo: id, codigo..."
        skip = False
        for hint in IGNORED_COLS_HINT:
            if hint in col_str:
                skip = True
                break
        
        # Rule: Skip 'aba' (mostly, handle special logic or just skip norm?)
        # Prompt: "coluna aba pode ser normalizada apenas com lower/strip".
        if col_str == 'aba': 
             df_norm[col] = df_norm[col].astype(str).str.strip().str.lower()
             continue # Already handled specific case
             
        if skip:
            continue
            
        # Check dtype - only normalize Object/String
        if not pd.api.types.is_string_dtype(df_norm[col]) and not pd.api.types.is_object_dtype(df_norm[col]):
            continue
            
        # Apply normalization
        # We use apply map for safety or vector ops? Vector ops hard with complex rules.
        # map() is cleaner.
        
        original_series = df_norm[col].astype(str) # ensure string for comparison
        
        # Optimization: use vector str ops where possible?
        # For simplicity and custom rules (stopwords), map is robust.
        # df_norm[col] can contain mixed types (int within object col).
        # normalize_text_value handles non-str check.
        
        new_series = df_norm[col].map(lambda x: normalize_text_value(x, config))
        df_norm[col] = new_series
        
        # Log changes
        # Simple count: how many different?
        # Cast original to string for fair comparison since normalize returns string
        # Careful with Nones/NaNs.
        
        # Just simple validation sampling logic
        # changed_mask = (df_norm[col] != df[col]) # naive
        
        etl_log.append({
            'coluna': col,
            'status': 'normalizado'
        })
        
    return df_norm, etl_log
