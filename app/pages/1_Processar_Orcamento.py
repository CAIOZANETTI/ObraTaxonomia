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


        # Lê todas as abas sem assumir header (header=None) para podermos procurar a linha correta
        sheets_dict = pd.read_excel(uploaded_file, sheet_name=None, header=None)
        
        all_sheets = []
        found_standard_cols = False
        
        # Palavras-chave para detecção
        desc_keywords = ['descricao', 'descrição', 'discriminacao', 'discriminação', 'especificacao', 'servico', 'item']
        unit_keywords = ['unid', 'unidade', 'und', 'un.', 'un']

        progress_text = "Processando abas e detectando colunas..."
        my_bar = st.progress(0, text=progress_text)
        
        for i, (sheet_name, raw_df) in enumerate(sheets_dict.items()):
            # Atualiza barra de progresso
            my_bar.progress((i + 1) / len(sheets_dict), text=f"Lendo aba: {sheet_name}")

            # Heurística: Procurar linha de cabeçalho nas primeiras 20 linhas
            header_idx = -1
            
            # Percorre linhas para encontrar keywords
            for r_idx in range(min(len(raw_df), 20)):
                row_vals = raw_df.iloc[r_idx].astype(str).str.lower().tolist()
                
                has_desc = any(k in " ".join(row_vals) for k in desc_keywords)
                has_unit = any(k in " ".join(row_vals) for k in unit_keywords)
                
                # Se achou ambos na mesma linha, bingo! É o header.
                if has_desc and has_unit:
                    header_idx = r_idx
                    break
            
            if header_idx != -1:
                # Promove a linha a cabeçalho
                cols_raw = raw_df.iloc[header_idx].fillna('Unnamed').astype(str).tolist()
                
                # Deduplicar nomes de colunas (Ex: 'Data', 'Data' -> 'Data', 'Data_1')
                seen = {}
                cols_dedup = []
                for c in cols_raw:
                    if c not in seen:
                        seen[c] = 0
                        cols_dedup.append(c)
                    else:
                        seen[c] += 1
                        cols_dedup.append(f"{c}_{seen[c]}")
                
                raw_df.columns = cols_dedup # Define nomes das colunas limpos
                sheet_df = raw_df.iloc[header_idx+1:].copy() # Pega dados abaixo
                sheet_df.reset_index(drop=True, inplace=True)
                
                # Renomeia colunas para um padrão interno (facilita concatenação)
                new_map = {}
                for col in sheet_df.columns:
                    c_str = str(col).lower()
                    if any(k in c_str for k in desc_keywords) and 'System_Descricao' not in new_map.values():
                        new_map[col] = 'System_Descricao'
                    elif any(k == c_str.strip() or k + '.' in c_str for k in unit_keywords) and 'System_Unidade' not in new_map.values():
                        new_map[col] = 'System_Unidade'
                
                sheet_df.rename(columns=new_map, inplace=True)
                found_standard_cols = True
            else:
                # Se não achou header, mantém como está (será Unnamed: 0, etc)
                sheet_df = raw_df
            
            # Adiciona identificador da aba
            sheet_df['sheet_name'] = sheet_name
            
            # Garante que as colunas padrão existam (mesmo que vazias) para o concat não quebrar
            if 'System_Descricao' not in sheet_df.columns:
                sheet_df['System_Descricao'] = None 
            if 'System_Unidade' not in sheet_df.columns:
                sheet_df['System_Unidade'] = None

            all_sheets.append(sheet_df)
            
        my_bar.empty()

        # Consolida
        df = pd.concat(all_sheets, ignore_index=True)
        
        st.success(f"Arquivo carregado! {len(sheets_dict)} abas processadas.")
        
        # Pré-seleção inteligente nos dropdowns
        cols = df.columns.tolist()
        
        idx_desc = 0
        idx_unit = 1
        
        if 'System_Descricao' in cols:
            idx_desc = cols.index('System_Descricao')
        if 'System_Unidade' in cols:
            idx_unit = cols.index('System_Unidade')
        
        # Criar layout de colunas para os selectbox
        c1, c2 = st.columns(2)
        
        col_desc = c1.selectbox("Selecione a coluna de DESCRIÇÃO", cols, index=idx_desc)
        col_unit = c2.selectbox("Selecione a coluna de UNIDADE", cols, index=idx_unit)

        
        # Warning se a detecção falhou
        if not found_standard_cols:
            st.warning("⚠️ Não detectamos automaticamente os cabeçalhos 'Descrição' e 'Unidade'. Verifique se selecionou as colunas corretas acima.")
        else:
            st.info("ℹ️ Detectamos automaticamente as colunas de Descrição e Unidade nas abas.")
        
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
                
                # Verificar se o dataframe é pequeno o suficiente para aplicar estilo
                total_cells = final_df.shape[0] * final_df.shape[1]
                max_cells = 262144  # Limite padrão do Pandas Styler
                
                if total_cells <= max_cells:
                    # Aplicar estilo se o dataframe for pequeno
                    st.dataframe(final_df.style.apply(highlight_unknown, axis=1), use_container_width=True)
                else:
                    # Exibir sem estilo se for muito grande
                    st.warning(f"⚠️ Dataframe muito grande ({total_cells:,} células). Exibindo sem destaque visual para melhor performance.")
                    st.dataframe(final_df, use_container_width=True)

                
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
