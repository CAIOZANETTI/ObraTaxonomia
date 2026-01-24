import streamlit as st
import pandas as pd
import os
import time
from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine

st.set_page_config(
    page_title="ObraTaxonomia - Processador",
    page_icon="🏗️",
    layout="wide"
)

# --- Singleton Cache para Builder (evitar recarregar YAML a cada interação) ---
@st.cache_resource
def get_engine():
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'yaml')
    builder = TaxonomyBuilder(base_dir).load_all()
    classifier = ClassifierEngine(builder)
    return classifier

classifier = get_engine()

st.title("🏗️ ObraTaxonomia")

st.markdown("### Processador de Orçamentos e Memoriais")
st.info("O sistema aplica regras estritas de unidade. Itens com unidades incompatíveis serão marcados como desconhecidos.")

# --- Upload ---
uploaded_file = st.file_uploader("Carregar planilha (.xlsx, .csv)", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write(f"Arquivo carregado: **{len(df)} linhas**")
        
        # --- Seleção de Colunas ---
        cols = df.columns.tolist()
        col1, col2 = st.columns(2)
        
        # Tenta adivinhar colunas padrão
        default_desc = next((c for c in cols if 'desc' in c.lower()), cols[0])
        default_unit = next((c for c in cols if 'unid' in c.lower()), cols[1] if len(cols)>1 else cols[0])
        
        with col1:
            col_desc = st.selectbox("Coluna de Descrição", cols, index=cols.index(default_desc))
        with col2:
            col_unit = st.selectbox("Coluna de Unidade", cols, index=cols.index(default_unit))
            
        if st.button("🚀 Processar Classificação"):
            with st.spinner("Classificando itens..."):
                start_time = time.time()
                
                # Processamento
                result_df = classifier.process_dataframe(df, col_desc=col_desc, col_unit=col_unit)
                
                # Merge com original
                final_df = pd.concat([df, result_df], axis=1)
                
                elapsed = time.time() - start_time
                st.success(f"Processamento concluído em {elapsed:.2f}s")
                
                # --- Resultados ---
                st.divider()
                
                # Métricas
                total = len(final_df)
                unknowns = final_df['tax_desconhecido'].sum()
                found = total - unknowns
                accuracy = (found / total) * 100
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Itens Classificados", found)
                m2.metric("Desconhecidos / Erro Unidade", unknowns)
                m3.metric("Taxa de Sucesso", f"{accuracy:.1f}%")
                
                # Preview
                st.subheader("Preview dos Resultados")
                st.dataframe(final_df.head(50), use_container_width=True)
                
                # Filtro de Desconhecidos
                if unknowns > 0:
                    st.warning(f"Foram encontrados {unknowns} itens não classificados ou com unidade incompatível.")
                    st.dataframe(final_df[final_df['tax_desconhecido'] == True].head(20))
                
                # --- Downloads ---
                d1, d2 = st.columns(2)
                
                # CSV Completo
                csv = final_df.to_csv(index=False).encode('utf-8')
                d1.download_button(
                    "📥 Baixar Resultado Completo (CSV)",
                    csv,
                    "orcamento_classificado.csv",
                    "text/csv"
                )
                
                # CSV Unknowns (para curadoria)
                if unknowns > 0:
                    unknowns_df = final_df[final_df['tax_desconhecido'] == True]
                    csv_unknown = unknowns_df.to_csv(index=False).encode('utf-8')
                    d2.download_button(
                        "🧐 Baixar Apenas Desconhecidos (Curadoria)",
                        csv_unknown,
                        "unknowns_to_curate.csv",
                        "text/csv"
                    )
                
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
