import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Adiciona raiz ao path para importar scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine

st.set_page_config(page_title="Processar Orçamento", page_icon="📂", layout="wide")

st.title("📂 Processar Orçamento (Excel)")

# --- Sidebar: Config ---
st.sidebar.header("Configurações")
force_reload = st.sidebar.button("Recarregar Regras YAML")

# --- Cache do Builder ---
@st.cache_resource
def get_engine():
    base_dir = os.path.join(os.getcwd(), 'yaml')
    builder = TaxonomyBuilder(base_dir).load_all()
    engine = ClassifierEngine(builder)
    return engine

if force_reload:
    st.cache_resource.clear()
    st.toast("Cache limpo! Regras recarregadas.", icon="🔄")

try:
    engine = get_engine()
    st.success(f"Motor carregado com {len(engine.rules)} regras de classificação.", icon="✅")
except Exception as e:
    st.error(f"Erro ao carregar motor de regras: {e}")
    st.stop()

# --- Upload ---
with st.expander("ℹ️ Instruções e Modelo de Planilha"):
    st.markdown("""
    Para o melhor funcionamento, sua planilha deve conter pelo menos duas colunas principais:
    1.  **Descrição**: O texto principal do item (Ex: `Conc. Est. fck 30 mpa`).
    2.  **Unidade**: A unidade de medida (Ex: `m3`, `un`, `kg`).
    
    *A ordem das colunas não importa, você poderá selecioná-las após o upload.*
    """)
    
    # Exemplo visual
    example_df = pd.DataFrame([
        {"Codigo": "001", "Descricao": "Concreto FCK 30MPa Bombeado", "Unidade": "m3", "Preco": 450.00},
        {"Codigo": "002", "Descricao": "Armação CA-50 10mm", "Unidade": "kg", "Preco": 12.50},
    ])
    st.table(example_df)

uploaded_file = st.file_uploader("Carregue seu arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:

        # Lê todas as abas (sheet_name=None retorna um dict: 'NomeAba': DataFrame)
        sheets_dict = pd.read_excel(uploaded_file, sheet_name=None)
        
        all_sheets = []
        for sheet_name, sheet_df in sheets_dict.items():
            # Adiciona coluna identificadora da aba
            sheet_df['sheet_name'] = sheet_name
            all_sheets.append(sheet_df)
            
        # Consolida tudo num único DataFrame
        df = pd.concat(all_sheets, ignore_index=True)
        
        st.write(f"Arquivo carregado com sucesso! Encontradas {len(sheets_dict)} abas: {list(sheets_dict.keys())}")
        st.write("Prévia do Arquivo Consolidado:", df.head())
        
        # Seleção de Colunas
        cols = df.columns.tolist()
        c1, c2 = st.columns(2)
        col_desc = c1.selectbox("Selecione a coluna de DESCRIÇÃO", cols, index=0 if len(cols)>0 else None)
        col_unit = c2.selectbox("Selecione a coluna de UNIDADE", cols, index=1 if len(cols)>1 else None)
        
        if st.button("🚀 Iniciar Classificação"):
            with st.spinner("Classificando itens..."):
                # Processamento
                results_df = engine.process_dataframe(df, col_desc=col_desc, col_unit=col_unit)
                
                # Merge
                final_df = pd.concat([df, results_df], axis=1)
                
                # Métricas
                total = len(final_df)
                unknowns = final_df[final_df['tax_desconhecido'] == True]
                count_unknown = len(unknowns)
                success_rate = ((total - count_unknown) / total) * 100
                
                # Exibição
                m1, m2, m3 = st.columns(3)
                m1.metric("Total de Itens", total)
                m2.metric("Itens Reconhecidos", total - count_unknown)
                m3.metric("Taxa de Sucesso", f"{success_rate:.1f}%")
                
                # Destaque visual
                def highlight_unknown(row):
                    if row['tax_desconhecido']:
                        return ['background-color: #ffcccc'] * len(row)
                    else:
                        return [''] * len(row)

                st.subheader("Resultado")
                st.dataframe(final_df.style.apply(highlight_unknown, axis=1), use_container_width=True)
                
                # --- Exportação de Desconhecidos (Sistema) ---
                if count_unknown > 0:
                    unknowns_dir = os.path.join(os.getcwd(), 'data', 'unknowns')
                    os.makedirs(unknowns_dir, exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_unknowns.csv"
                    filepath = os.path.join(unknowns_dir, filename)
                    
                    # Salva colunas relevantes para o agente
                    cols_to_export = [col_desc, col_unit]
                    if 'sheet_name' in unknowns.columns:
                        cols_to_export.append('sheet_name')
                        
                    export_df = unknowns[cols_to_export].copy()
                    export_df['arquivo_origem'] = uploaded_file.name
                    export_df.to_csv(filepath, index=False)
                    
                    st.warning(f"⚠️ {count_unknown} itens não reconhecidos foram exportados para aprendizado em `{filename}`.")
                
                # --- Download User ---
                # to excel buffer
                # (simplificado para CSV aqui, mas ideal seria Excel com formatação)
                csv = final_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Baixar Resultado (CSV)",
                    data=csv,
                    file_name="orcamento_classificado.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
