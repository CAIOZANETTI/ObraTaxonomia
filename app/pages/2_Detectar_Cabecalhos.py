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

# --- IMPORTS ---
import sys
import os
import pandas as pd
import streamlit as st

# Add scripts to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

# --- UI LOGIC ---

st.title("🕵️ Mapeamento Manual de Colunas")
st.markdown("Selecione as abas, indique a linha do cabeçalho e mapeie as colunas manualmente.")

if 'df_all' not in st.session_state:
    st.warning("Por favor, faça o upload do arquivo na Página 1.")
    st.stop()

df_all = st.session_state['df_all']
sheets = df_all['aba'].unique().tolist()
grouped = df_all.groupby('aba')

# 1. Sheet Selection (Pills)
st.subheader("1. Selecione as Abas para Processar")

# Default select all? Or clean start? Let's select all by default so user can remove.
selected_sheets = st.pills(
    "Abas:",
    options=sheets,
    selection_mode="multi",
    default=sheets,
    key="manual_sheet_selection"
)

if not selected_sheets:
    st.warning("Selecione pelo menos uma aba para configurar.")
    st.stop()

st.divider()

# 2. Manual Configuration Loop
st.subheader("2. Configuração de Mapeamento")

manual_configs = {} # Store user config {sheet: {header_row, mapping}}
structured_dfs = []

# To persist configs across reruns, we might need st.session_state
# But for now, let's rely on widget keys.

for sheet in selected_sheets:
    with st.expander(f"📝 Configurar Aba: {sheet}", expanded=False):
        df_sheet = grouped.get_group(sheet).reset_index(drop=True)
        # Drop internal 'aba' col for display
        df_display = df_sheet.drop(columns=['aba'], errors='ignore')
        
        # A. Preview Raw Data to help find Header Row
        st.write("Visualização dos Dados Brutos (Topo):")
        st.dataframe(df_display.head(10))
        
        # B. Header Row Selection
        # Default 0
        header_row_idx = st.number_input(
            f"Linha do Cabeçalho ({sheet})", 
            min_value=0, 
            max_value=len(df_display)-1, 
            value=0, 
            key=f"hr_{sheet}"
        )
        
        # C. Get Columns based on Header Row
        # If Row 0, cols are df columns. 
        # If Row > 0, we treat that row as header.
        
        current_cols = []
        if header_row_idx == 0:
            current_cols = list(df_display.columns)
        else:
            # Emulate reading header from that row
            # We rename generic columns to values in that row
            vals = df_display.iloc[header_row_idx].astype(str).tolist()
            # Handle duplicates
            seen = {}
            for v in vals:
                seen[v] = seen.get(v, 0) + 1
                
            final_cols = []
            seen_counts = {}
            for v in vals:
                if seen[v] > 1:
                    seen_counts[v] = seen_counts.get(v, 0) + 1
                    final_cols.append(f"{v}_{seen_counts[v]}")
                else:
                    final_cols.append(v)
            current_cols = final_cols
            
        # Options for dropdowns match these columns
        col_options = ["(Ignorar)"] + current_cols
        
        # D. Mapping Dropdowns
        c1, c2, c3 = st.columns(3)
        c4, c5 = st.columns(2)
        
        # Helper to find default index if column name matches simple keywords
        def find_default(options, keyword):
            for i, opt in enumerate(options):
                if keyword in str(opt).lower():
                    return i
            return 0
            
        # Mappings
        with c1:
            desc_col = st.selectbox(f"Descrição ({sheet})", col_options, index=find_default(col_options, "desc"), key=f"map_desc_{sheet}")
        with c2:
            unit_col = st.selectbox(f"Unidade ({sheet})", col_options, index=find_default(col_options, "unid"), key=f"map_unit_{sheet}")
        with c3:
            qty_col = st.selectbox(f"Quantidade ({sheet})", col_options, index=find_default(col_options, "qtd"), key=f"map_qty_{sheet}")
        with c4:
            price_col = st.selectbox(f"Preço Unit. ({sheet})", col_options, index=find_default(col_options, "unit"), key=f"map_prc_{sheet}")
        with c5:
            total_col = st.selectbox(f"Preço Total ({sheet})", col_options, index=find_default(col_options, "total"), key=f"map_tot_{sheet}")
            
        # E. Process Sheet Button (Real-time Preview?)
        # Let's show a preview of the *RESULT*
        
        # Logic to build structured DF for this sheet
        # header_row_idx implies data starts at idx + 1
        data_start = header_row_idx + 1
        
        # Slice data
        df_sliced = df_sheet.iloc[data_start:].copy()
        
        # Use the "virtual" column names (current_cols) to reference data?
        # NO. df_sliced still has original columns (0, 1, 2 or A, B, C...).
        # We need to map: Chosen Name -> Original Column ID.
        
        # Let's rebuild the map: "Chosen Name" -> Index in current_cols -> Original Column Name in df_sheet
        
        # Map: Standard Field -> User Selected Option
        user_map = {
            'descricao': desc_col,
            'unidade': unit_col,
            'quantidade': qty_col,
            'preco_unitario': price_col,
            'preco_total': total_col
        }
        
        # Filter out ignored
        active_map = {k: v for k, v in user_map.items() if v != "(Ignorar)"}
        
        if not active_map:
            st.warning("Nenhuma coluna mapeada.")
        else:
            # Rename logic
            # We need to find which ACTUAL column in df_sheet corresponds to the selected name
            # header_vals (current_cols) map 1:1 to df_sheet.columns (by index)
            
            rename_dict = {} # OldColName -> NewStandardName
            
            # Create lookup: DisplayName -> OriginalColName
            # current_cols [i] corresponds to df_sheet.columns [i] (minus 'aba' if we dropped it, wait.
            # df_display was used for current_cols. df_display matches df_sheet minus 'aba'.
            
            orig_cols = df_display.columns.tolist()
            
            for field, selected_name in active_map.items():
                # Find index of selected_name in current_cols
                try:
                    idx = current_cols.index(selected_name)
                    # Get original col name
                    orig_name = orig_cols[idx]
                    rename_dict[orig_name] = field
                except ValueError:
                    pass # Should not happen
            
            # Filter columns - keep only text cols + 'aba'
            # But we must act on df_sheet (which has 'aba') or df_sliced (has 'aba'?)
            # df_sliced comes from df_sheet, so it has 'aba'.
            
            # Select only mapped columns + aba
            cols_to_keep = list(rename_dict.keys())
            
            # Rename
            df_final = df_sliced.rename(columns=rename_dict)
            
            # Keep only standard fields + aba
            final_cols_standard = list(rename_dict.values())
            
            # Ensure we keep 'aba'
            if 'aba' in df_final.columns:
                 df_final = df_final[['aba'] + final_cols_standard]
            else:
                 # Re-inject?
                 df_final = df_final[final_cols_standard]
                 df_final['aba'] = sheet
                 
            st.write("Preview Resultado:")
            st.dataframe(df_final.head(5))
            
            structured_dfs.append(df_final)

st.divider()
if st.button("Confirmar e Avançar para ETL ➡️", type="primary"):
    if not structured_dfs:
        st.error("Nenhum dado estruturado gerado. Configure pelo menos uma aba.")
    else:
        # Concatenate
        try:
            full_df = pd.concat(structured_dfs, ignore_index=True)
            st.session_state['df_structured'] = full_df
            st.success("Dados estruturados com sucesso!")
            st.switch_page("pages/3_Normalizacao_ETL.py")
        except Exception as e:
            st.error(f"Erro ao consolidar: {e}")
            
if st.button("⬅️ Voltar para Upload"):
    st.switch_page("pages/1_Processar_Orcamento.py")
