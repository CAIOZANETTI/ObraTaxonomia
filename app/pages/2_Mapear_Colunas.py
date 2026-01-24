import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="2. Mapear Colunas", layout="wide")

st.header("2. Mapeamento de Colunas")
st.markdown("Identifique quais colunas do seu arquivo correspondem aos campos padrões do sistema.")

# --- Validação Inicial ---
if 'csv_raw' not in st.session_state:
    st.error("Nenhum arquivo carregado. Volte para a página 1.")
    if st.button("Voltar"):
        st.switch_page("pages/1_Upload_Excel.py")
    st.stop()

# --- Carregar Dados ---
try:
    df_raw = pd.read_csv(io.StringIO(st.session_state['csv_raw']))
    cols_originais = df_raw.columns.tolist()
except Exception as e:
    st.error(f"Erro ao ler CSV da sessão: {e}")
    st.stop()

# --- Definição dos Campos Padrão ---
MANDATORY_FIELDS = {
    'descricao': 'Descrição do Item (Obrigatório)',
    'unidade': 'Unidade de Medida (Obrigatório)',
    'quantidade': 'Quantidade (Obrigatório)'
}
OPTIONAL_FIELDS = {
    'codigo': 'Código / Item',
    'preco_unit': 'Preço Unitário',
    'preco_total': 'Preço Total'
}

ALL_FIELDS_ORDER = list(MANDATORY_FIELDS.keys()) + list(OPTIONAL_FIELDS.keys())

# --- Lógica de Mapa ---
# Inicializar mapa na sessão se não existir
if 'colmap' not in st.session_state:
    st.session_state['colmap'] = {}

# Copia para manipulação local
current_map = st.session_state['colmap'].copy()

# Heurística de Auto-Map (roda se o campo ainda não estiver mapeado)
def try_automap(field, columns, used):
    if field in current_map and current_map[field] in columns:
        return current_map[field]
    
    # Palavras-chave para heurística
    keywords = {
        'descricao': ['desc', 'disc', 'nome', 'servico', 'objeto'],
        'unidade': ['unid', 'und', 'med'],
        'quantidade': ['quant', 'qtd', 'qtde'],
        'codigo': ['cod', 'item', 'ref'],
        'preco_unit': ['unit', 'p.u', 'preco_unit'],
        'preco_total': ['total', 'vl', 'valor', 'preco_tot']
    }
    
    for col in columns:
        if col in used: continue
        if any(k in col.lower() for k in keywords.get(field, [])):
            return col
    return None

# --- Interface Sequencial ---
used_columns = []
warnings = []

st.divider()

# --- Global Preview (added per user request) ---
with st.expander("🔍 Visualizar Dados Originais (Contexto Geral)", expanded=True):
    col_slider, _ = st.columns([1, 3])
    with col_slider:
        n_rows = st.slider("Linhas para visualizar:", min_value=5, max_value=20, value=10)
    
    st.caption("Topo do Arquivo")
    st.dataframe(df_raw.head(n_rows), use_container_width=True)
    st.caption("Fim do Arquivo")
    st.dataframe(df_raw.tail(n_rows), use_container_width=True)

st.divider()

col_layout, preview_layout = st.columns([1, 1])

with col_layout:
    st.subheader("Seleção de Colunas")
    
    for field in ALL_FIELDS_ORDER:
        label = MANDATORY_FIELDS.get(field, OPTIONAL_FIELDS.get(field))
        is_mandatory = field in MANDATORY_FIELDS
        
        # Filtrar colunas disponíveis (excluir as já usadas em iterações anteriores neste loop)
        available_cols = [c for c in cols_originais if c not in used_columns or (field in current_map and current_map[field] == c)]
        
        # Determinar valor atual ou automap
        default_val = try_automap(field, cols_originais, used_columns)
        
        # Se o valor atual (do session ou automap) não estiver nas disponíveis, resetar
        if default_val and default_val not in available_cols:
            default_val = None

        # UI: Pills
        # Note: st.pills returns the selection interactively. 
        # Selection mode "single" returns value or None.
        selection = st.pills(
            f"{label} {'*' if is_mandatory else ''}",
            options=available_cols,
            selection_mode="single",
            default=default_val,
            key=f"pills_{field}"
        )
        
        if selection:
            current_map[field] = selection
            used_columns.append(selection)
            
            # Mostrar preview IMEDIATO (Snippet)
            st.caption(f"👁️ Preview: **{selection}**")
            # Pequeno dataframe preview logo abaixo do pill
            st.dataframe(df_raw[selection].head(10), height=150, use_container_width=True)
            st.markdown("---")
            
        else:
            # Se obrigatório e vazio, avisa
            if is_mandatory:
                st.warning(f"⚠️ O campo **{field}** é obrigatório.")
                warnings.append(field)
            # Remove do mapa se foi desmarcado
            if field in current_map:
                del current_map[field]

# --- Atualizar Session State ---
st.session_state['colmap'] = current_map

# --- Ações ---
st.divider()
c1, c2 = st.columns([1, 5])

if c1.button("Voltar"):
    st.switch_page("pages/1_Upload_Excel.py")

can_proceed = len(warnings) == 0

if c2.button("Aplicar Mapa e Continuar", type="primary", disabled=not can_proceed):
    try:
        # Construir csv_struct
        df_struct = df_raw.copy()
        
        # Inverter mapa
        rename_map = {v: k for k, v in current_map.items()}
        
        cols_to_keep = list(rename_map.keys())
        if 'aba_origem' in df_struct.columns:
            cols_to_keep.append('aba_origem')
            
        df_struct = df_struct[cols_to_keep].rename(columns=rename_map)
        df_struct['id_linha'] = range(1, len(df_struct) + 1)
        
        for opt in OPTIONAL_FIELDS:
            if opt not in df_struct.columns:
                df_struct[opt] = None
                
        # Validação Numérica Básica
        if 'quantidade' in df_struct.columns:
            df_struct['quantidade'] = pd.to_numeric(df_struct['quantidade'], errors='coerce')
            
        st.session_state['csv_struct'] = df_struct.to_csv(index=False)
        st.success("Estrutura definida!")
        st.switch_page("pages/3_Normalizar.py")
        
    except Exception as e:
        st.error(f"Erro ao estruturar: {e}")
