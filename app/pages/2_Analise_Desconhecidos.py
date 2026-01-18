import streamlit as st
import pandas as pd
import os
import glob
import sys

# Adiciona raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

st.set_page_config(page_title="Análise de Desconhecidos", page_icon="🕵️", layout="wide")

st.title("🕵️ Gestão de Itens Desconhecidos")

unknowns_dir = os.path.join(os.getcwd(), 'data', 'unknowns')

if not os.path.exists(unknowns_dir):
    st.info("A pasta `data/unknowns` ainda não existe ou está vazia.")
    st.stop()

files = glob.glob(os.path.join(unknowns_dir, "*.csv"))

if not files:
    st.success("🎉 Nenhuma pendência encontrada! O sistema reconheceu tudo até agora.", icon="🙌")
    st.stop()
    
# Seleção de Arquivo
selected_file = st.selectbox("Selecione um arquivo de pendências:", files, format_func=lambda x: os.path.basename(x))

if selected_file:
    df = pd.read_csv(selected_file)
    st.markdown(f"**Total de itens desconhecidos neste lote:** `{len(df)}`")
    
    st.dataframe(df, use_container_width=True)
    
    # Botão de download
    csv_data = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="⬇️ Baixar CSV de Desconhecidos",
        data=csv_data,
        file_name=os.path.basename(selected_file),
        mime="text/csv",
        help="Baixar este arquivo CSV para análise offline",
        use_container_width=True
    )
    
    st.markdown("### Ação Requerida")
    st.info("""
    Este arquivo deve ser processado pelo **Agente Antigravity**.
    
    1. O Agente lerá este CSV.
    2. Consultar o repositório YAML atual.
    3. Propor novas regras ou sinônimos.
    """)
    
    if st.button("🗑️ Marcar como Resolvido (Arquivar)"):
        # Mover para processados (simulação)
        processed_dir = os.path.join(os.getcwd(), 'data', 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        new_path = os.path.join(processed_dir, os.path.basename(selected_file))
        os.rename(selected_file, new_path)
        st.success("Arquivo movido para processados!")
        st.rerun()
