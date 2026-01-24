import streamlit as st
import pandas as pd
import io
import os
from scripts.unknowns import aggregate_unknowns, save_unknowns_jsonl

st.set_page_config(page_title="5. Desconhecidos", layout="wide")

st.header("5. Gestão de Desconhecidos")
st.markdown("Itens não identificados são oportunidades de aprendizado para a IA. Exporte-os para alimentar o ciclo de melhoria.")

if 'csv_validated' not in st.session_state:
    st.error("Dados validados não encontrados. Volte para a página 4.")
    if st.button("Voltar"):
        st.switch_page("pages/4_Apelidar_Validar.py")
    st.stop()

# --- Carregar Dados ---
try:
    df_final = pd.read_csv(io.StringIO(st.session_state['csv_validated']))
except Exception as e:
    st.error(f"Erro ao ler CSV da sessão: {e}")
    st.stop()
    
# --- Agregar Unknowns ---
# Unknowns são aqueles onde tax_desconhecido=True (mesmo após validação humana, se o humano marcou que manteve desconhecido?)
# Ou aquilo que o humano NÃO validou?
# Vamos assumir que unknowns são aqueles explicitamente não resolvidos ou marcados como desconhecidos.
# A função aggregate_unknowns usa 'tax_desconhecido' column.

with st.spinner("Agregando desconhecidos..."):
    agg_df = aggregate_unknowns(df_final)

# --- Métricas e Visualização ---
total_unknown_lines = df_final['tax_desconhecido'].sum()
unique_unknowns = len(agg_df)

c1, c2 = st.columns(2)
c1.metric("Linhas Desconhecidas", total_unknown_lines)
c2.metric("Itens Únicos (Agregados)", unique_unknowns)

st.divider()

if unique_unknowns > 0:
    st.subheader("Top Unknowns")
    st.dataframe(
        agg_df, 
        use_container_width=True,
        column_config={
            "descricao_norm": st.column_config.TextColumn("Descrição (Norm)"),
            "unidade": st.column_config.TextColumn("Und"),
            "ocorrencias": st.column_config.ProgressColumn("Frequência", format="%d", min_value=0, max_value=int(agg_df['ocorrencias'].max())),
            "exemplos": st.column_config.ListColumn("Exemplos Originais")
        }
    )
    
    st.divider()
    st.subheader("Exportação para IA")
    st.info("O arquivo JSONL contém metadados ricos para treinamento e deve ser enviado para curadoria.")
    
    b1, b2 = st.columns(2)
    
    # Gerar JSONL em memória para download
    jsonl_str = agg_df.to_dict(orient='records')
    import json
    jsonl_output = ""
    for record in jsonl_str:
        jsonl_output += json.dumps(record, ensure_ascii=False) + '\n'
        
    b1.download_button(
        "📥 Baixar JSONL (Treinamento IA)",
        data=jsonl_output,
        file_name="unknowns_training.jsonl",
        mime="application/x-jsonlines"
    )
    
    # CSV Simples
    csv_output = agg_df.to_csv(index=False).encode('utf-8')
    b2.download_button(
        "📥 Baixar Tabela Agregada (CSV)",
        data=csv_output,
        file_name="unknowns_aggregated.csv",
        mime="text/csv"
    )
    
    # --- Auto Save (Simulado) ---
    # Salvar localmente na pasta data/unknowns/inbox
    if st.button("💾 Persistir na Inbox do Projeto"):
        path = save_unknowns_jsonl(agg_df)
        if path:
            st.success(f"Salvo em: {path}")
        else:
            st.warning("Nada para salvar.")

else:
    st.success("🎉 Parabéns! Não há itens desconhecidos neste lote.")
    st.balloons()

# --- Ações Finais ---
st.divider()
if st.button("🏠 Voltar para Início (Nova Sessão)"):
    st.switch_page("streamlit_app.py")
