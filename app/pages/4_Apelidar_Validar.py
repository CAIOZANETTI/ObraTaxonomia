import streamlit as st
import pandas as pd
import io
import os
import time
import sys

# Adicionar root ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine
from scripts.unknowns import aggregate_unknowns

st.set_page_config(page_title="4. Apelidar e Validar", layout="wide")

# --- Inicialização da Engine (Cache) ---
@st.cache_resource
def get_engine():
    # Caminho relativo para yaml
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'yaml')
    builder = TaxonomyBuilder(base_dir).load_all()
    classifier = ClassifierEngine(builder)
    return classifier

    return classifier

if st.button("🔄 Recarregar Regras (Limpar Cache)"):
    st.cache_resource.clear()
    
    # Forçar reclassificação dos dados
    if 'df_working' in st.session_state:
        del st.session_state['df_working']
        
    st.success("Cache e Dados limpos! O classificador rodará novamente.")
    st.rerun()

classifier = get_engine()

st.header("4. Classificação e Validação")
st.markdown("O sistema sugere apelidos baseados na taxonomia. Você valida ou corrige.")

# --- Verificações de Sessão ---
if 'csv_norm' not in st.session_state:
    st.error("Dados normalizados não encontrados. Volte para a página 3.")
    if st.button("Voltar"):
        st.switch_page("pages/3_Normalizar.py")
    st.stop()

# --- Carregar Dados ---
if 'df_working' not in st.session_state:
    try:
        df_norm = pd.read_csv(io.StringIO(st.session_state['csv_norm']))
        # Inicializar colunas de trabalho se não existirem
        if 'apelido_sugerido' not in df_norm.columns:
            # Ainda não rodou classificador
            # Vamos rodar automaticamente na primeira vez
            with st.spinner("Classificando pela primeira vez..."):
                result_df = classifier.process_dataframe(df_norm, col_desc='descricao_norm', col_unit='unidade')
                # Merge
                # O process_dataframe retorna um df com mesmo index, então concat axis=1 funciona se index alinhado
                # Mas para garantir, vamos fazer concat e remover duplicatas se tiver
                df_combined = pd.concat([df_norm, result_df], axis=1)
                
                # Inicializar coluna de revisão
                df_combined['revisar'] = False
                
            st.session_state['df_working'] = df_combined
        else:
            st.session_state['df_working'] = df_norm
            
    except Exception as e:
        st.error(f"Erro ao preparar dados: {e}")
        st.stop()
else:
    # Recarregar do session state (pode ter edições anteriores)
    df_combined = st.session_state['df_working']

# --- Métricas ---
df = df_combined # Alias curto

total = len(df)
marcados_revisar = df['revisar'].sum()
ok = len(df[df['query_status']=='ok']) if 'query_status' in df.columns else len(df[df['status'] == 'ok']) # fallback compatibility
status_revisar = len(df[df['status'] == 'revisar'])
desconhecidos = len(df[df['status'] == 'desconhecido'])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total de Itens", total)
m2.metric("Sugestão Certa (OK)", ok)
m3.metric("Status: Revisar", status_revisar)
m4.metric("Desconhecidos", desconhecidos)
st.metric("Marcados para Revisão", f"{marcados_revisar} itens")

# --- Filtros e Controles ---
st.divider()

with st.expander("🔍 Filtros Avançados", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtro por Status
        status_filter = st.multiselect(
            "Status",
            options=['ok', 'revisar', 'desconhecido'],
            default=['ok', 'revisar', 'desconhecido']
        )
    
    with col2:
        # Filtro por Revisar
        revisar_filter = st.multiselect(
            "Revisar",
            options=['Marcado', 'Não Marcado'],
            default=['Marcado', 'Não Marcado']
        )
    
    with col3:
        # Filtro por Tipo (Domínio)
        tipos_disponiveis = ['Todos'] + sorted(df['tax_tipo'].dropna().unique().tolist())
        tipo_filter = st.selectbox(
            "Tipo (Domínio)",
            options=tipos_disponiveis,
            index=0
        )
    
    # Segunda linha de filtros
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Filtro por Apelido
        apelidos_disponiveis = ['Todos'] + sorted(df['apelido_sugerido'].dropna().unique().tolist())
        apelido_filter = st.selectbox(
            "Apelido Sugerido",
            options=apelidos_disponiveis,
            index=0
        )
    
    with col5:
        # Toggle para mostrar semelhantes
        show_similares = st.toggle("Mostrar Semelhantes", value=False)
    
    with col6:
        # Filtro de busca por texto na descrição
        search_text = st.text_input("Buscar na descrição", placeholder="Digite para filtrar...")

# Filtragem do DataFrame para Exibição
mask = df['status'].isin(status_filter)

# Aplicar filtro de revisar
if 'Marcado' in revisar_filter and 'Não Marcado' not in revisar_filter:
    mask = mask & (df['revisar'] == True)
elif 'Não Marcado' in revisar_filter and 'Marcado' not in revisar_filter:
    mask = mask & (df['revisar'] == False)
# Se ambos ou nenhum estiver selecionado, não filtra por revisar

# Aplicar filtro de tipo
if tipo_filter != 'Todos':
    mask = mask & (df['tax_tipo'] == tipo_filter)

# Aplicar filtro de apelido
if apelido_filter != 'Todos':
    mask = mask & (df['apelido_sugerido'] == apelido_filter)

# Aplicar filtro de busca por texto
if search_text:
    mask = mask & df['descricao_norm'].str.contains(search_text.lower(), case=False, na=False)

df_view = df[mask].copy()

# --- Configuração de Colunas Disponíveis (Mapeamento Interno -> Label) ---
COL_LABELS = {
    "revisar": "Revisar?",
    "descricao_norm": "Descrição (Norm)",
    "unidade": "Und",
    "quantidade": "Qtd",
    "apelido_sugerido": "Sugestão",
    "status": "Status",
    "motivo": "Motivo",
    "codigo": "Código",
    "preco_unit": "Preço Unit.",
    "preco_total": "Preço Total"
}

# Defaults visíveis
DEFAULT_VISIBLE = ["revisar", "descricao_norm", "status", "apelido_sugerido", "motivo"]

with st.expander("👁️ Configurar Colunas Visíveis", expanded=False):
    visible_cols = st.multiselect(
        "Selecione as colunas para exibir:",
        options=list(COL_LABELS.keys()),
        default=DEFAULT_VISIBLE,
        format_func=lambda x: COL_LABELS[x]
    )

# --- Tabela Editável ---
# Definir configuração base das colunas
col_config = {
    "revisar": st.column_config.CheckboxColumn("Revisar?", width="small", help="Marque os itens que precisam revisão"),
    "descricao_norm": st.column_config.TextColumn("Descrição (Norm)", disabled=True, width="large"),
    "unidade": st.column_config.TextColumn("Und", disabled=True, width="small"),
    "quantidade": st.column_config.NumberColumn("Qtd", disabled=True, format="%.2f"),
    "apelido_sugerido": st.column_config.TextColumn("Sugestão", disabled=True),
    "status": st.column_config.TextColumn("Status", disabled=True, width="small"),
    "motivo": st.column_config.TextColumn("Motivo", disabled=True),
    "codigo": st.column_config.TextColumn("Código", disabled=True, width="small"),
    "preco_unit": st.column_config.NumberColumn("Preço Unit.", disabled=True, format="%.2f"),
    "preco_total": st.column_config.NumberColumn("Preço Total", disabled=True, format="%.2f"),
    # Esconder colunas técnicas sempre
    "id_linha": None, "linha_origem": None, "aba_origem": None, 
    "alternativa": None, "score": None, "tax_tipo": None, "tax_desconhecido": None,
    "unidade_sugerida": None, "tax_incerto": None, "tax_confianca": None, "tax_apelido": None,
    "apelido_final": None  # Esconder apelido_final
}

# Aplicar filtro de visibilidade
# Para cada coluna que NÃO está em visible_cols, setar como None (esconder)
for col_key in COL_LABELS.keys():
    if col_key not in visible_cols:
        col_config[col_key] = None

# Lógica Dinâmica para Semelhantes (Toggle soberano)
if show_similares:
    col_config["semelhantes"] = st.column_config.TextColumn("Semelhantes", disabled=True)
else:
    col_config["semelhantes"] = None

st.caption("Marque os itens que precisam revisão. Baixe o CSV de itens marcados para aprendizado.")

edited_df_view = st.data_editor(
    df_view,
    column_config=col_config,
    use_container_width=True,
    hide_index=True,
    key="editor_validation" # Key fixa para não resetar em rerun parcial
)

# --- Sincronização de Edições ---
# O st.data_editor retorna apenas as linhas que estavam visíveis (df_view) com as edições.
# Precisamos atualizar o df principal (st.session_state['df_working']) com essas edições.
# Usamos o index original que foi preservado no df_view.

if st.button("💾 Salvar Alterações na Sessão"):
    # Atualizar o DataFrame mestre com as edições do view
    # Pandas update é eficiente com índices alinhados
    st.session_state['df_working'].update(edited_df_view)
    
    st.success("Alterações salvas!")
    st.rerun() # Refresh nas métricas

# --- Exportação ---
st.divider()
st.subheader("Finalizar e Exportar")

# Primeira linha de botões
c1, c2, c3, c4 = st.columns(4)

if c1.button("Voltar"):
    st.switch_page("pages/3_Normalizar.py")

# Botão Download Validado (Completo)
csv_validado = st.session_state['df_working'].to_csv(index=False).encode('utf-8')
c2.download_button(
    label="📥 Baixar Completo",
    data=csv_validado,
    file_name="orcamento_validado.csv",
    mime="text/csv",
    help="Baixa todos os dados processados (completo)."
)

# Botão Download Marcados para Revisar (Aprendizado)
marcados_revisar_df = st.session_state['df_working'][
    st.session_state['df_working']['revisar'] == True
]
csv_marcados = marcados_revisar_df.to_csv(index=False).encode('utf-8')
c3.download_button(
    label="📥 Marcados Revisar",
    data=csv_marcados,
    file_name="aprendizado_revisar.csv",
    mime="text/csv",
    help=f"Baixa {len(marcados_revisar_df)} itens marcados para revisão → data/aprendizado/revisar/"
)

# Botão Download Desconhecidos (Aprendizado)
unknowns_df = st.session_state['df_working'][
    st.session_state['df_working']['tax_desconhecido'] == True
]
csv_unknowns = unknowns_df.to_csv(index=False).encode('utf-8')
c4.download_button(
    label="📥 Desconhecidos",
    data=csv_unknowns,
    file_name="aprendizado_desconhecidos.csv",
    mime="text/csv",
    help=f"Baixa {len(unknowns_df)} itens desconhecidos → data/aprendizado/desconhecidos/"
)

# Segunda linha - Botão de continuar
st.markdown("")  # Espaçamento

# Botão Continuar para Unknowns (Gestão)
# Salva unknowns na sessão antes de ir
if st.button("Gerir Desconhecidos >", type="primary"):
    # Salvar estado final
    st.session_state['csv_validated'] = st.session_state['df_working'].to_csv(index=False)
    
    # Gerar Unknowns
    # Consideramos unknown aquilo que ainda está marked as unknown OU não foi validado/preenchido
    # Mas para o report de unknowns puro, usamos tax_desconhecido original da classificação?
    # Ou o residual?
    # Arquitetura diz: "Unknowns não são erro; são fila de melhoria".
    # Então exportamos o que o sistema NÃO conseguiu resolver sozinho ou o usuário confirmou que não existe.
    # Vamos usar a flag tax_desconhecido atualizada
    
    st.switch_page("pages/5_Desconhecidos.py")
