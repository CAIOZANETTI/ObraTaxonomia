import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="2. Mapear Colunas", layout="wide")

st.header("2. Mapeamento de Colunas")
st.markdown("Identifique quais colunas do seu arquivo correspondem aos campos padrões do sistema.")

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
MANDATORY_FIELDS = ['descricao', 'unidade', 'quantidade']
OPTIONAL_FIELDS = ['codigo', 'preco_unit', 'preco_total']
ALL_FIELDS = MANDATORY_FIELDS + OPTIONAL_FIELDS

# --- Interface de Mapeamento ---
st.subheader("Configuração de De/Para")

# Prepara DataFrame para o Data Editor
# Estrutura: [Campo Padrão, Coluna no Arquivo]
map_data = []

# Tentar automap (heurística simples)
used_cols = set()
for field in ALL_FIELDS:
    match = None
    # Procura por substring
    for col in cols_originais:
        if col in used_cols: continue
        
        # Heurísticas básicas
        if field == 'descricao' and any(x in col.lower() for x in ['desc', 'disc', 'nome', 'servico']):
            match = col
        elif field == 'unidade' and any(x in col.lower() for x in ['unid', 'und']):
            match = col
        elif field == 'quantidade' and any(x in col.lower() for x in ['quant', 'qtd', 'qtde']):
            match = col
        elif field == 'codigo' and any(x in col.lower() for x in ['cod', 'item', 'ref']):
            match = col
        elif field == 'preco_unit' and any(x in col.lower() for x in ['unit', 'p.u']):
            match = col
        elif field == 'preco_total' and any(x in col.lower() for x in ['total', 'vl', 'valor']):
            match = col
    
    if match:
        used_cols.add(match)
    
    # Se já tem mapeamento salvo na sessão, usa ele
    saved_map = st.session_state.get('colmap', {})
    current_val = saved_map.get(field, match)
    
    map_data.append({
        "Campo Sistema": field,
        "Obrigatório": "Sim" if field in MANDATORY_FIELDS else "Não",
        "Coluna no Arquivo": current_val
    })

df_map = pd.DataFrame(map_data)

# Editor de mapeamento
edited_df = st.data_editor(
    df_map,
    column_config={
        "Campo Sistema": st.column_config.TextColumn(disabled=True),
        "Obrigatório": st.column_config.TextColumn(disabled=True),
        "Coluna no Arquivo": st.column_config.SelectboxColumn(
            "Selecione a coluna",
            options=[""] + cols_originais,
            required=True
        )
    },
    use_container_width=True,
    hide_index=True,
    num_rows="fixed"
)

# --- Validação e Aplicação ---
st.divider()

colmap = {}
errors = []

for idx, row in edited_df.iterrows():
    field = row["Campo Sistema"]
    col_file = row["Coluna no Arquivo"]
    required = row["Obrigatório"] == "Sim"
    
    if required and (not col_file or col_file == ""):
        errors.append(f"O campo obrigatório **{field}** não foi mapeado.")
    
    if col_file and col_file != "":
        if col_file in colmap.values():
            errors.append(f"A coluna **{col_file}** foi mapeada mais de uma vez.")
        colmap[field] = col_file

if errors:
    for err in errors:
        st.error(err)
else:
    st.info("Mapeamento parece válido.")

c1, c2 = st.columns([1, 5])
if c1.button("Voltar"):
    st.switch_page("pages/1_Upload_Excel.py")

if c2.button("Aplicar Mapa e Continuar", type="primary", disabled=len(errors) > 0):
    try:
        # Construir csv_struct
        df_struct = df_raw.copy()
        
        # Manter apenas colunas mapeadas e renomear
        # Inverter o mapa para rename: {col_arquivo: campo_sistema}
        rename_map = {v: k for k, v in colmap.items()}
        
        # Selecionar apenas as colunas que estão no mapa (e colunas técnicas se existirem)
        cols_to_keep = list(rename_map.keys())
        
        # Garantir que aba_origem e outras técnicas sejam preservadas se existirem
        if 'aba_origem' in df_struct.columns:
            cols_to_keep.append('aba_origem')
        
        df_struct = df_struct[cols_to_keep].rename(columns=rename_map)
        
        # Adicionar id_linha sequencial
        df_struct['id_linha'] = range(1, len(df_struct) + 1)
        
        # Adicionar colunas faltantes opcionais como vazias
        for opt in OPTIONAL_FIELDS:
            if opt not in df_struct.columns:
                df_struct[opt] = None
                
        # Validações de dados
        # Quantidade deve ser numerica
        if 'quantidade' in df_struct.columns:
            # Tentar limpar e converter
            df_struct['quantidade'] = pd.to_numeric(df_struct['quantidade'], errors='coerce')
            qtd_invalidas = df_struct['quantidade'].isna().sum()
            if qtd_invalidas > 0:
                st.warning(f"{qtd_invalidas} linhas têm quantidade inválida (viraram NaN).")
        
        # Salvar na sessão
        st.session_state['colmap'] = colmap
        st.session_state['csv_struct'] = df_struct.to_csv(index=False)
        
        st.success("Estrutura criada com sucesso!")
        st.switch_page("pages/3_Normalizar.py")
        
    except Exception as e:
        st.error(f"Erro ao aplicar estrutura: {e}")

# Review
if 'csv_struct' in st.session_state:
    st.subheader("Preview Estruturado")
    try:
        df_show = pd.read_csv(io.StringIO(st.session_state['csv_struct']))
        st.dataframe(df_show.head(), use_container_width=True)
    except:
        pass
