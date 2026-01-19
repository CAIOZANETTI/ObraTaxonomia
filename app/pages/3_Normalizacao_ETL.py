import streamlit as st
import pandas as pd
import unidecode
import json
import io
import datetime
import hashlib

st.set_page_config(
    page_title="Normalização / ETL",
    page_icon="🧹",
    layout="wide"
)

# --- CONFIG ---
VERSION = "p3_etl_v2"

# --- HELPER FUNCTIONS ---

def generate_hash(df):
    """Gera hash SHA1 do dataframe para auditoria."""
    return hashlib.sha1(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def normalize_text(text, remove_accents=False):
    if not isinstance(text, str):
        return str(text) if pd.notnull(text) else ""
    
    text = text.strip()
    # Remove chars invisíveis: \u00A0 (non-breaking space), \r, \n
    text = text.replace('\u00A0', ' ').replace('\r', '').replace('\n', '')
    
    if remove_accents:
        text = unidecode.unidecode(text)
    
    # Colapsar espaços
    text = " ".join(text.split())
    text = text.lower()
    return text

def normalize_colnames(df):
    """
    Passo 1: Normalização de colunas
    """
    step_log = {
        "step": "normalize_colnames",
        "renames": {},
        "count": 0
    }
    
    new_cols = []
    seen = {}
    
    for col in df.columns:
        # 1. String e strip
        c_str = str(col).strip()
        # 2. Lower
        c_str = c_str.lower()
        # 3. Unidecode (nomes de colunas sempre sem acento para facilitar código)
        c_str = unidecode.unidecode(c_str)
        # 4. Underscore
        c_str = "_".join(c_str.split())
        # 5. Remove invisibles
        c_str = c_str.replace('\u00A0', '').replace('\r', '').replace('\n', '')
        
        # Deduplicate
        if c_str in seen:
            seen[c_str] += 1
            c_str = f"{c_str}__{seen[c_str] + 1}"
        else:
            seen[c_str] = 0
            
        new_cols.append(c_str)
        if c_str != col:
            step_log["renames"][col] = c_str
            step_log["count"] += 1
            
    df_out = df.copy()
    df_out.columns = new_cols
    
    return df_out, step_log

def normalize_strings(df, remove_accents=False):
    """
    Passo 2: Normalização de valores string
    """
    step_log = {
        "step": "normalize_strings",
        "affected_cols": [],
        "cells_changed": 0,
        "sample_changes": []
    }
    
    df_out = df.copy()
    
    # Heurística para pular colunas de ID/Código
    skip_keywords = ["id", "codigo", "cod", "cpf", "cnpj", "ncm", "gtin", "sku", "hash"]
    
    cols_to_process = df.select_dtypes(include=['object', 'string']).columns
    
    for col in cols_to_process:
        # Check skip heuristics
        if any(k in col.lower() for k in skip_keywords):
            # Processamento mínimo para IDs (apenas strip e invisíveis)
            # Não fazemos lower nem remove accents obrigatoriamente
             df_out[col] = df_out[col].astype(str).str.strip().str.replace(r'[\r\n\u00A0]+', '', regex=True)
             continue
        
        # Processamento total
        before = df[col].astype(str).fillna('')
        
        # Aplica função customizada
        # Nota: pandas str accessor é vetorizado mas unidecode não.
        # map() pode ser lento para milhões de linhas, mas é seguro aqui.
        
        def clean_val(x):
            if pd.isna(x): return x
            return normalize_text(x, remove_accents=remove_accents)
            
        df_out[col] = df_out[col].apply(clean_val)
        
        # Métricas
        # Comparar (cuidado com NaN)
        # Vamos comparar string vs string
        mask_changed = (before != df_out[col])
        changed_count = mask_changed.sum()
        
        if changed_count > 0:
            step_log["affected_cols"].append(col)
            step_log["cells_changed"] += int(changed_count)
            
            # Amostra
            idx_changed = df_out[mask_changed].index[:2].tolist()
            for idx in idx_changed:
                step_log["sample_changes"].append({
                    "col": col,
                    "row": idx,
                    "before": str(df.at[idx, col]),
                    "after": str(df_out.at[idx, col])
                })
                
    return df_out, step_log

def suggest_drop_columns(df):
    """
    Analisa colunas e sugere remoção.
    """
    suggestions = []
    
    for col in df.columns:
        reason = None
        should_remove = False
        
        # 1. 100% nulo
        if df[col].isnull().all():
            reason = "100% Nulos"
            should_remove = True
            
        # 2. Constante única (exceto 'aba')
        elif col != 'aba' and df[col].nunique(dropna=False) <= 1:
            reason = "Valor Único (Constante)"
            should_remove = True
            
        # 3. Nome suspeito
        elif pd.Series([col]).astype(str).str.contains(r'^(unnamed|index|linha|row|coluna_vazia|sem_nome)', case=False, regex=True).any():
            reason = "Nome Genérico/Vazio"
            should_remove = True
            
        # Never remove protected columns
        is_protected = col in ['aba', 'descricao', 'unidade', 'quantidade', 'preco_unitario', 'preco_total']
        if is_protected:
            should_remove = False
            
        if reason:
            suggestions.append({
                "coluna": col,
                "motivo": reason,
                "nulos_pct": df[col].isnull().mean() * 100,
                "unicos": df[col].nunique(),
                "sugerido": should_remove
            })
            
    return pd.DataFrame(suggestions)

def parse_numbers(df):
    """
    Passo 4: Leve parsing numérico
    """
    step_log = {
        "step": "parse_numbers",
        "converted_cols": [],
        "warnings": []
    }
    
    df_out = df.copy()
    
    # Heurística de nomes
    target_keywords = ["qtd", "quant", "preco", "valor", "total", "unit", "parcial"]
    
    for col in df.columns:
        if df[col].dtype.kind in 'iuf': # Já é numérico
            continue
            
        if any(k in col.lower() for k in target_keywords):
            # Tentar converter
            series = df[col].astype(str)
            
            # Limpeza pré-parsing (PT-BR)
            # Remove separador milhar (.), troca decimal (,) por (.)
            # "1.000,50" -> "1000.50"
            # Cuidado: Se formato for US "1,000.50", isso quebra.
            # Assumindo BR preponderante no contexto de "ObraTaxonomia"
            
            def safe_parse(x):
                if not x or x.lower() == 'nan' or x.lower() == 'none' or x.strip() == '':
                    return None
                val = x.strip()
                # Remove sifrão ou texto
                val = val.replace("R$", "").replace("r$", "").strip()
                
                # Regras de sinal
                # Se tiver virgula e ponto:
                # 1.234,56 -> Ponto é milhar
                if '.' in val and ',' in val:
                    val = val.replace('.', '').replace(',', '.')
                elif ',' in val:
                    # Pode ser decimal ou milhar? Assumir decimal se único
                    val = val.replace(',', '.')
                # Se só ponto, já está OK (ou milhar sem decimal, mas pd.to_numeric lida se for float '1000.00' mas falha se '1.000' int? não, '1.000' vira 1.0)
                
                return val

            parsed = series.apply(safe_parse)
            
            # Tenta converter
            numeric_series = pd.to_numeric(parsed, errors='coerce')
            
            # Validar sucesso
            failures = numeric_series.isnull().sum() - series.apply(lambda x: not x or x=='' or x.lower()=='nan').sum()
            # Se failures (que não eram nulos antes) > 10% (tolerância), rejeita
            valid_count = len(series) - series.apply(lambda x: not x or x=='' or x.lower()=='nan').sum()
            
            if valid_count > 0:
                failure_rate = failures / valid_count
            else:
                failure_rate = 0
            
            if failure_rate < 0.20: # Aceita até 20% de falha
                df_out[col] = numeric_series
                step_log["converted_cols"].append(col)
            else:
                step_log["warnings"].append(f"Coluna '{col}' falhou parsing (taxa erro {failure_rate:.1%}). Mantida como string.")

    return df_out, step_log


# --- MAIN UI ---

st.title("🧹 Normalização e ETL")

# Recupera Entrada
# Preferencia: df_structured (Pag 2) > df_all (Pag 1)
if 'df_structured' in st.session_state and st.session_state['df_structured'] is not None:
    df_input = st.session_state['df_structured']
    source_name = "Dados Estruturados (Página 2)"
elif 'df_all' in st.session_state and st.session_state['df_all'] is not None:
    df_input = st.session_state['df_all']
    source_name = "Dados Brutos (Página 1)"
else:
    st.warning("⚠️ Nenhum dado encontrado. Processe a Página 1 ou 2 primeiro.")
    st.stop()

# --- 1. OVERVIEW ---
st.subheader(f"1. Visão Geral do Input ({source_name})")
st.write(f"Shape: {df_input.shape[0]} linhas x {df_input.shape[1]} colunas")

with st.expander("Ver amostra e tipos"):
    st.dataframe(df_input.head(10))
    st.write(df_input.dtypes.astype(str))

# --- 2. CONFIG ---
st.divider()
st.subheader("2. Configuração do Pipeline")

c1, c2, c3, c4 = st.columns(4)
do_norm_cols = c1.checkbox("Normalizar Colunas", value=True, help="Lower, strip, underscore")
do_norm_str = c2.checkbox("Normalizar Strings", value=True, help="Lower, cleanup")
do_parse_num = c3.checkbox("Parsing Numérico", value=False, help="Converter texto para números (Cuidado)")
remove_accents = c4.checkbox("Remover Acentos", value=False, help="Nas strings")

# Sugestões de Remoção
suggestions_df = suggest_drop_columns(df_input)
cols_to_drop = []

if not suggestions_df.empty:
    st.markdown("##### 🗑️ Sugestões de Limpeza")
    st.info("As seguintes colunas foram marcadas como potencialmente inúteis.")
    
    # Editor interativo para escolher o que deletar
    edited_suggestions = st.data_editor(
        suggestions_df,
        column_config={
            "sugerido": st.column_config.CheckboxColumn("Remover?", help="Marque para deletar", default=False)
        },
        disabled=["coluna", "motivo", "nulos_pct", "unicos"],
        hide_index=True,
        use_container_width=True,
        key="drop_editor"
    )
    
    # Filtrar marcados
    cols_to_drop = edited_suggestions[edited_suggestions['sugerido'] == True]['coluna'].tolist()
    if cols_to_drop:
        st.caption(f"Serão removidas {len(cols_to_drop)} colunas: {', '.join(cols_to_drop)}")
else:
    st.success("Nenhuma coluna inútil detectada automaticamente.")


# --- 3. EXECUTION ---
st.divider()
if st.button("🚀 Executar ETL", type="primary"):
    
    log_full = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": VERSION,
        "config": {
            "norm_cols": do_norm_cols,
            "norm_str": do_norm_str,
            "remove_accents": remove_accents,
            "parse_num": do_parse_num,
            "dropped_cols": cols_to_drop
        },
        "steps": [],
        "input_hash": generate_hash(df_input),
        "output_hash": None
    }
    
    steps_summary = []
    
    try:
        current_df = df_input.copy()
        
        # 3.1 Drop
        if cols_to_drop:
            current_df.drop(columns=cols_to_drop, inplace=True)
            step_info = {
                "step": "drop_columns",
                "count": len(cols_to_drop),
                "cols": cols_to_drop
            }
            log_full["steps"].append(step_info)
            steps_summary.append({"step": "1. Remoção Colunas", "detalhes": f"{len(cols_to_drop)} removidas"})
            
        # 3.2 Norm Cols
        if do_norm_cols:
            current_df, log_nc = normalize_colnames(current_df)
            log_full["steps"].append(log_nc)
            steps_summary.append({"step": "2. Norm. Colunas", "detalhes": f"{log_nc['count']} renomeadas"})
            
        # 3.3 Norm Strings
        if do_norm_str:
            current_df, log_ns = normalize_strings(current_df, remove_accents=remove_accents)
            log_full["steps"].append(log_ns)
            steps_summary.append({"step": "3. Norm. Strings", "detalhes": f"{log_ns['cells_changed']} células alteradas"})
            
        # 3.4 Parse Num
        if do_parse_num:
            current_df, log_pn = parse_numbers(current_df)
            log_full["steps"].append(log_pn)
            steps_summary.append({"step": "4. Parsing Numérico", "detalhes": f"{len(log_pn['converted_cols'])} convertidas"})
            
        
        # Finalize
        log_full["output_hash"] = generate_hash(current_df)
        
        # Session State Save
        st.session_state['df_norm'] = current_df
        st.session_state['etl_log'] = log_full
        st.session_state['etl_steps_summary'] = pd.DataFrame(steps_summary)
        
        st.success("ETL Concluído com Sucesso!")
        
    except Exception as e:
        st.error(f"Erro durante ETL: {e}")
        st.stop()


# --- 4. OUTPUTS & LOGS ---

if 'df_norm' in st.session_state:
    st.divider()
    st.subheader("4. Resultados e Log")
    
    # Summary
    if 'etl_steps_summary' in st.session_state:
        st.table(st.session_state['etl_steps_summary'])
        
    # Log Json
    with st.expander("📄 Log Completo (JSON)"):
        st.json(st.session_state['etl_log'])
        
    # Preview
    st.write("Preview Dados Normalizados:")
    st.dataframe(st.session_state['df_norm'].head(50))
    
    # Downloads
    csv = st.session_state['df_norm'].to_csv(index=False).encode('utf-8')
    log_json = json.dumps(st.session_state['etl_log'], indent=2).encode('utf-8')
    
    c1, c2 = st.columns(2)
    c1.download_button("⬇️ Baixar CSV Normalizado", csv, "master_normalizado.csv", "text/csv")
    c2.download_button("⬇️ Baixar Log de ETL (JSON)", log_json, "etl_log.json", "application/json")
    
    # Reset Button
    if st.button("↩️ Resetar (Descartar ETL)"):
        del st.session_state['df_norm']
        del st.session_state['etl_log']
        st.rerun()
