import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="2. Mapear Colunas", layout="wide")

# --- Interface Principal (Full Screen) ---
st.title("2. Mapeamento de Colunas")

# --- Validação Inicial ---
if 'csv_raw' not in st.session_state:
    st.error("Nenhum arquivo carregado. Volte para a página 1.")
    if st.button("Voltar"):
        st.switch_page("pages/1_Upload_Excel.py")
    st.stop()

# --- Definição dos Campos ---
MANDATORY_FIELDS = {
    'descricao': 'Descrição do Item *',
    'unidade': 'Unidade de Medida *',
    'quantidade': 'Quantidade *'
}
OPTIONAL_FIELDS = {
    'codigo': 'Código / Item',
    'preco_unit': 'Preço Unitário',
    'preco_total': 'Preço Total'
}

# --- Sidebar: Controles de Mapeamento ---
with st.sidebar:
    st.header("🔧 Configuração")
    
    # --- Ajuste de Cabeçalho ---
    st.markdown("### 1. Ajuste de Tabela")
    # Default 0, mas permite pular linhas de "lixo" no topo
    header_row = st.number_input(
        "Linha do Cabeçalho", 
        min_value=0, 
        value=0, 
        help="Se a planilha tem títulos ou logos no topo, aumente este número até a linha azul (cabeçalho) ficar correta."
    )
    
    # Recarregar com novo header (Otimização: cachear ou apenas ler de novo é rápido com StringIO)
    try:
        # header=header_row define qual linha é o header (0-indexed)
        df_raw = pd.read_csv(io.StringIO(st.session_state['csv_raw']), header=header_row)
        cols_originais = df_raw.columns.tolist()
    except Exception as e:
        st.error(f"Erro ao ler cabeçalho na linha {header_row}: {e}")
        st.stop()
        
    st.markdown("### 2. Mapeamento")

    st.divider()
    
    # Inicializar mapa na sessão se não existir
    if 'colmap' not in st.session_state:
        st.session_state['colmap'] = {}
    
    current_map = st.session_state['colmap'].copy()
    
    # Função Auxiliar de AutoMap
    def try_automap(field, columns, used):
        if field in current_map and current_map[field] in columns:
            return current_map[field]
        
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

    # Excluir colunas já selecionadas (Mutual Exclusivity)
    # Mas precisamos permitir que o próprio campo mantenha sua seleção
    # Estratégia: Calcular 'used_globally' mas subtrair o valor atual do campo loop
    
    # Primeiro, obter todos os valores atualmente selecionados (exceto None)
    # Isso é difícil fazer dinamicamente dentro do loop do streamlit pois a seleção acontece sequencialmente
    # Vamos simplificar: O usuario pode ver todas, mas se selecionar duplicado a validação avisa.
    # OU: filtrar options. Vamos tentar filtrar options para uma UX melhor.
    
    # Passo 1: Recuperar seleções atuais do session state (se houver widget state) ou do current_map
    # Como st.selectbox write diretamente na key, podemos usar st.session_state
    
    # Loop Obrigatórios
    st.subheader("Obrigatórios")
    
    # Para garantir exclusividade interativa, precisamos saber o que JÁ foi escolhido nos outros selects.
    # O Streamlit rerun a cada select change.
    
    # Coletar valores usados em OUTROS campos
    def get_used_in_others(current_field):
        used = []
        for f, v in current_map.items():
            if f != current_field and v:
                used.append(v)
        return used

    warnings = []
    
    for field, label in MANDATORY_FIELDS.items():
        used_others = get_used_in_others(field)
        available = [""] + [c for c in cols_originais if c not in used_others]
        
        # Determinar default/index index
        val = try_automap(field, cols_originais, used_others)
        
        # Se o valor atual (no mapa) não está nas disponíveis, reseta
        if val and val not in available:
            val = "" # ou None
            
        index_val = available.index(val) if val in available else 0
        
        selection = st.selectbox(
            label,
            options=available,
            index=index_val,
            key=f"sel_{field}",
            help=f"Coluna correspondente a {field}"
        )
        
        if selection:
            current_map[field] = selection
        else:
            if field in current_map: del current_map[field]
            warnings.append(field)
            
    st.divider()
    
    # Expander Opcionais
    with st.expander("⚙️ Opcionais", expanded=False):
        for field, label in OPTIONAL_FIELDS.items():
            used_others = get_used_in_others(field)
            available = [""] + [c for c in cols_originais if c not in used_others]
            
            val = try_automap(field, cols_originais, used_others)
            # Opcionais não precisam de automap agressivo, mas ajuda
            
            index_val = available.index(val) if val in available else 0
            
            selection = st.selectbox(
                label,
                options=available,
                index=index_val,
                key=f"sel_{field}"
            )
            
            if selection:
                current_map[field] = selection
            elif field in current_map:
                del current_map[field]
                
    # Salvar mapa
    st.session_state['colmap'] = current_map
    
    st.divider()
    
    # Botão de Ação no Sidebar
    can_proceed = len(warnings) == 0
    if not can_proceed:
        st.error(f"Pesquise: {', '.join(warnings)}")
        
    if st.button("✅ Aplicar e Continuar", type="primary", disabled=not can_proceed):
         try:
            # Construir csv_struct
            df_struct = df_raw.copy()
            rename_map = {v: k for k, v in current_map.items()}
            
            cols_to_keep = list(rename_map.keys())
            if 'aba_origem' in df_struct.columns:
                cols_to_keep.append('aba_origem')
                
            df_struct = df_struct[cols_to_keep].rename(columns=rename_map)
            df_struct['id_linha'] = range(1, len(df_struct) + 1)
            
            for opt in OPTIONAL_FIELDS:
                if opt not in df_struct.columns:
                    df_struct[opt] = None
                    
            if 'quantidade' in df_struct.columns:
                df_struct['quantidade'] = pd.to_numeric(df_struct['quantidade'], errors='coerce')
                
            st.session_state['csv_struct'] = df_struct.to_csv(index=False)
            st.success("Salvo!")
            st.switch_page("pages/3_Normalizar.py")
            
         except Exception as e:
            st.error(f"Erro: {e}")
            
    if st.button("Voltar"):
        st.switch_page("pages/1_Upload_Excel.py")


# --- Main Area: Tabela Visual ---
st.markdown("### 📋 Visualização dos Dados")
st.caption("Esta visualização ajuda a identificar as colunas. Use o **menu lateral (Sidebar)** à esquerda para fazer o mapeamento.")

# Highlight das colunas selecionadas
# Vamos criar um style function para colorir os headers ou as celulas das colunas mapeadas
# Pandas Styler é pesado no Streamlit se a tabela for grande.
# Alternativa: Apenas mostrar a tabela limpa. O usuário vê o nome da coluna no header.

# Uma feature legal: Filtrar para mostrar apenas as colunas que AINDA NÃO FORAM USADAS?
# Não, o usuário quer ver o contexto inteiro.

st.dataframe(
    df_raw,
    use_container_width=True,
    height=800 # Altura fixa grande para preencher a tela
)
