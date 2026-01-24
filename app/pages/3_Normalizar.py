import streamlit as st
import pandas as pd
import io
from scripts.normalize import normalize_dataframe, get_normalization_report

st.set_page_config(page_title="3. Normalizar", layout="wide")

st.header("3. Normalização")
st.markdown("Limpeza e padronização dos textos e números para garantir a qualidade da classificação.")

if 'csv_struct' not in st.session_state:
    st.error("Estrutura não definida. Volte para a página 2.")
    if st.button("Voltar"):
        st.switch_page("pages/2_Mapear_Colunas.py")
    st.stop()

# --- Carregar Dados ---
try:
    df_struct = pd.read_csv(io.StringIO(st.session_state['csv_struct']))
except Exception as e:
    st.error(f"Erro ao ler CSV estruturado: {e}")
    st.stop()

# --- Configuração das Regras ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Regras Ativas")
    config = {
        'remove_accents': st.checkbox("Remover acentos", value=True),
        'remove_punctuation': st.checkbox("Remover pontuação (exceto traços numéricos)", value=True),
        'remove_stopwords': st.checkbox("Remover stopwords (de, da, com...)", value=False),
        'collapse_spaces': st.checkbox("Remover espaços duplos", value=True),
        'normalize_numbers': st.checkbox("Normalizar números e decimais", value=True)
    }

# --- Preview Dinâmico (Amostra) ---
with col2:
    st.subheader("Amostra do Resultado")
    if st.button("Atualizar Preview"):
        # Pegar amostra de 5 linhas
        sample = df_struct.head(5).copy()
        sample_norm, _ = normalize_dataframe(sample, config, col_desc='descricao')
        
        # Comparar
        comparison = pd.DataFrame({
            'Original': sample['descricao'],
            'Normalizado': sample_norm['descricao_norm']
        })
        st.dataframe(comparison, use_container_width=True)

# --- Aplicação Final ---
st.divider()

c1, c2 = st.columns([1, 5])
if c1.button("Voltar"):
    st.switch_page("pages/2_Mapear_Colunas.py")

if c2.button("Aplicar Normalização em Tudo", type="primary"):
    with st.spinner("Normalizando..."):
        try:
            # Processar tudo
            df_norm, audit_log = normalize_dataframe(df_struct, config, col_desc='descricao')
            
            # Salvar sessão
            st.session_state['csv_norm'] = df_norm.to_csv(index=False)
            st.session_state['audit_log'] = audit_log
            
            # Mostrar Relatório
            report = get_normalization_report(audit_log)
            st.success("Normalização concluída!")
            
            with st.expander("Ver Relatório de Auditoria", expanded=True):
                st.text(report)
                
            # Botão para proximo
            st.button("Continuar para Classificação >", on_click=lambda: st.switch_page("pages/4_Apelidar_Validar.py"))
            
        except Exception as e:
            st.error(f"Erro na normalização: {e}")
