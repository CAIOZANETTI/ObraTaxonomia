import streamlit as st
import os

st.set_page_config(
    page_title="ObraTaxonomia Home",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ ObraTaxonomia v4")

st.markdown("""
### Bem-vindo ao Sistema de Taxonomia de Obras

Este sistema guia você através de 5 etapas para processar, normalizar e classificar itens de orçamento:

1.  **Upload**: Carregue seu arquivo Excel e converta para CSV.
2.  **Mapear**: Defina quais colunas correspondem ao padrão do sistema.
3.  **Normalizar**: Limpe e padronize textos e números.
4.  **Classificar**: Receba sugestões de apelidos e valide-as.
5.  **Desconhecidos**: Exporte itens não identificados para curadoria.

---
**Status da Sessão:**
""")

# Mostrar estado atual da sessão para debug/acompanhamento
if 'csv_raw' in st.session_state:
    st.success("✅ CSV Bruto carregado")
else:
    st.warning("⚠️ Nenhum arquivo carregado")

if 'colmap' in st.session_state:
    st.success("✅ Colunas mapeadas")

if 'csv_validated' in st.session_state:
    st.success("✅ Classificação validada")

st.divider()
st.caption("Antigravity Engineer - v4.0.0")
