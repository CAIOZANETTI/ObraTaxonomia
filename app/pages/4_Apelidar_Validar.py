import streamlit as st
import pandas as pd
import io
import os
import time

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
                
                # Inicializar colunas de validação
                df_combined['validado'] = False
                df_combined['apelido_final'] = df_combined['apelido_sugerido']
                
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
validados = df['validado'].sum()
ok = len(df[df['query_status']=='ok']) if 'query_status' in df.columns else len(df[df['status'] == 'ok']) # fallback compatibility
revisar = len(df[df['status'] == 'revisar'])
desconhecidos = len(df[df['status'] == 'desconhecido'])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total de Itens", total)
m2.metric("Sugestão Certa (OK)", ok)
m3.metric("Para Revisar", revisar)
m4.metric("Desconhecidos", desconhecidos)
st.progress(int(validados / total * 100) if total > 0 else 0, text=f"Progresso da Validação: {validados}/{total}")

# --- Filtros e Controles ---
st.divider()
c_filter, c_toggle = st.columns([3, 1])

with c_filter:
    # Usando selectbox ou multiselect para filtros, pills ideal mas fallback
    status_filter = st.multiselect(
        "Filtrar por Status",
        options=['ok', 'revisar', 'desconhecido'],
        default=['ok', 'revisar', 'desconhecido']
    )
    
    # Checkbox para mostrar apenas não validados
    show_pending_only = st.checkbox("Mostrar apenas pendentes de validação", value=False)

with c_toggle:
    show_similares = st.toggle("Mostrar Semelhantes", value=False)

# Filtragem do DataFrame para Exibição
mask = df['status'].isin(status_filter)
if show_pending_only:
    mask = mask & (df['validado'] == False)

df_view = df[mask].copy()

# --- Tabela Editável ---
# Definir configuração das colunas
col_config = {
    "validado": st.column_config.CheckboxColumn("Validado?", width="small"),
    "descricao_norm": st.column_config.TextColumn("Descrição (Norm)", disabled=True, width="large"),
    "unidade": st.column_config.TextColumn("Und", disabled=True, width="small"),
    "apelido_sugerido": st.column_config.TextColumn("Sugestão", disabled=True),
    "apelido_final": st.column_config.TextColumn("Apelido Final (Editável)", required=True),
    "status": st.column_config.TextColumn("Status", disabled=True, width="small"),
    "motivo": st.column_config.TextColumn("Motivo", disabled=True),
    "semelhantes": st.column_config.TextColumn("Semelhantes", disabled=True, hidden=not show_similares),
    # Esconder colunas técnicas
    "id_linha": None, "linha_origem": None, "aba_origem": None, 
    "alternativa": None, "score": None, "tax_tipo": None, "tax_desconhecido": None,
    "unidade_sugerida": None, "tax_incerto": None, "tax_confianca": None, "tax_apelido": None
}

st.caption("Edite o 'Apelido Final' se necessário e marque 'Validado'. Suas alterações são salvas automaticamente na memória.")

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
    
    # Atualizar status de desconhecido baseado na edição
    # Se usuário preencheu apelido_final em um desconhecido, ele deixa de ser desconhecido para fins de unknown export?
    # Regra: Se validado=True e apelido_final != "", não é mais unknown
    
    # Re-calcular tax_desconhecido para consistência
    mask_resolved = (st.session_state['df_working']['validado'] == True) & (st.session_state['df_working']['apelido_final'].notna()) & (st.session_state['df_working']['apelido_final'] != "")
    st.session_state['df_working'].loc[mask_resolved, 'tax_desconhecido'] = False
    
    st.success("Alterações salvas!")
    st.rerun() # Refresh nas métricas

# --- Exportação ---
st.divider()
st.subheader("Finalizar e Exportar")

c1, c2, c3 = st.columns(3)

if c1.button("Voltar"):
    st.switch_page("pages/3_Normalizar.py")

# Botão Download Validado
csv_validado = st.session_state['df_working'].to_csv(index=False).encode('utf-8')
c2.download_button(
    label="📥 Baixar Resultado Validado (.csv)",
    data=csv_validado,
    file_name="orcamento_validado.csv",
    mime="text/csv"
)

# Botão Continuar para Unknowns
# Salva unknowns na sessão antes de ir
if c3.button("Ver Desconhecidos >"):
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
