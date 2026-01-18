import streamlit as st
import os

st.set_page_config(
    page_title="ObraTaxonomia - Home",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ ObraTaxonomia")

st.markdown("""
### Bem-vindo ao Sistema de Padronização de Orçamentos

Este sistema utiliza inteligência de regras (Taxonomia) para transformar planilhas orçamentárias "sujas" em dados estruturados e auditáveis.

#### Funcionalidades Principais:

1.  **Processador de Excel**: Carregue sua planilha, o sistema reconhece os itens automaticamente.
2.  **Gestão de Desconhecidos**: Itens não reconhecidos são isolados para aprendizado.
3.  **Feedback Loop**: O Agente Antigravity monitora os desconhecidos e atualiza as regras automaticamente.

---

#### Como usar:
*   Vá para **Processar Orçamento** no menu lateral para subir um arquivo.
*   Vá para **Análise de Desconhecidos** para ver o que o sistema anda aprendendo (ou falhando).

---
*Versão do Sistema: 0.1.0 MVP*
""")
