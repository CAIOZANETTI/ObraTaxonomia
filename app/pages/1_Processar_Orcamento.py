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

                # --- Interface de Validação Interativa ---
                st.subheader("📝 Validação de Classificações")
                
                # Obter lista de todos os apelidos disponíveis
                all_apelidos = sorted(list(set([rule['apelido'] for rule in engine.rules])))
                
                # Preparar dados para edição
                # Selecionar colunas relevantes para exibição
                display_cols = [col_desc, col_unit, 'tax_apelido', 'tax_tipo', 'tax_desconhecido']
                
                # Status visual e categorização
                def get_status_label(row):
                    if row.get('tax_desconhecido', True):
                        return '❌ Desconhecido'
                    elif row.get('tax_incerto', False):
                        return '⚠️ Incerto'
                    else:
                        return '✅ Conhecido'

                final_df['status_icon'] = final_df.apply(get_status_label, axis=1)

                # Tabs para organização
                tab_known, tab_uncertain, tab_unknown = st.tabs([
                    "✅ Conhecidos", 
                    "⚠️ Sugestões/Incertos", 
                    "❌ Desconhecidos"
                ])
                
                # Filtro global de busca
                st.markdown("#### 🔍 Filtros Globais")
                search_term = st.text_input("🔎 Buscar na descrição:", placeholder="Digite para filtrar em todas as abas...")
                
                # Configurar colunas editáveis (Comum a todas as abas)
                column_config = {
                    col_desc: st.column_config.TextColumn(
                        "Descrição",
                        disabled=True,
                        width="large",
                        help="Descrição original do item"
                    ),
                    col_unit: st.column_config.TextColumn(
                        "Unidade",
                        disabled=True,
                        width="small"
                    ),
                    'tax_apelido': st.column_config.SelectboxColumn(
                        "Apelido",
                        options=all_apelidos,
                        required=False,
                        help="Selecione o apelido correto",
                        width="medium"
                    ),
                    'tax_tipo': st.column_config.TextColumn(
                        "Tipo",
                        disabled=True,
                        width="small"
                    ),
                    'status_icon': st.column_config.TextColumn(
                        "Status",
                        disabled=True,
                        width="small"
                    ),
                    'tax_score': st.column_config.ProgressColumn(
                        "Confiança",
                        min_value=0,
                        max_value=100,
                        format="%.0f%%"
                    )
                }
                
                edit_cols = [col_desc, col_unit, 'tax_apelido', 'tax_tipo', 'status_icon', 'tax_score']
                
                # Função auxiliar para renderizar editor em cada aba
                def render_tab_editor(subset_df, key_suffix, help_text):
                    st.info(help_text)
                    
                    # Aplicar busca
                    if search_term:
                        mask = subset_df[col_desc].astype(str).str.contains(search_term, case=False, na=False)
                        current_df = subset_df[mask]
                    else:
                        current_df = subset_df

                    st.metric("Itens nesta categoria", len(current_df))
                    
                    if len(current_df) > 0:
                        return st.data_editor(
                            current_df[edit_cols],
                            column_config=column_config,
                            use_container_width=True,
                            num_rows="fixed",
                            hide_index=True,
                            key=f"editor_{key_suffix}",
                            disabled=[col_desc, col_unit, 'tax_tipo', 'status_icon', 'tax_score']
                        )
                    else:
                        st.success("Nenhum item nesta categoria! 🎉")
                        return pd.DataFrame() # Retorna vazio

                # --- Renderizar Abas ---
                
                all_editors = []
                
                # 1. Conhecidos
                with tab_known:
                    df_known = final_df[
                        (final_df['tax_desconhecido'] == False) & 
                        (final_df['tax_incerto'] == False)
                    ]
                    edited_known = render_tab_editor(
                        df_known, 
                        "known", 
                        "Itens identificados com alta confiança (Match Exato)."
                    )
                    if not edited_known.empty: all_editors.append(edited_known)

                # 2. Incertos
                with tab_uncertain:
                    df_uncertain = final_df[
                        (final_df['tax_desconhecido'] == False) & 
                        (final_df['tax_incerto'] == True)
                    ]
                    edited_uncertain = render_tab_editor(
                        df_uncertain, 
                        "uncertain", 
                        "💡 O sistema sugeriu apelidos similares. Por favor confirme ou corrija."
                    )
                    if not edited_uncertain.empty: all_editors.append(edited_uncertain)

                # 3. Desconhecidos
                with tab_unknown:
                    df_unknown = final_df[final_df['tax_desconhecido'] == True]
                    edited_unknown = render_tab_editor(
                        df_unknown, 
                        "unknown", 
                        "⚠️ Itens que não foram encontrados. Necessário classificar manualmente."
                    )
                    if not edited_unknown.empty: all_editors.append(edited_unknown)

                # Consolidar edições
                if all_editors:
                    # Juntar o que foi editado (apenas visualização das abas) com o resto do dataframe original
                    # Mas o st.data_editor retorna apenas as linhas que foram passadas para ele.
                    # Precisamos reconstruir um DF único de edições para comparar.
                    
                    edited_full = pd.concat(all_editors)

                
                # Detectar mudanças
                changes_made = False
                corrections = []
                
                if 'edited_full' in locals() and not edited_full.empty:
                    for idx in edited_full.index:
                        # Verificar se o índice existe no original (segurança)
                        if idx in final_df.index:
                            original_apelido = final_df.loc[idx, 'tax_apelido']
                            edited_apelido = edited_full.loc[idx, 'tax_apelido']
                            
                            # Tratar NaN misturados com None/Empty
                            if pd.isna(original_apelido): original_apelido = ""
                            if pd.isna(edited_apelido): edited_apelido = ""
                            
                            if str(original_apelido) != str(edited_apelido):
                                changes_made = True
                                corrections.append({
                                    'index': idx,
                                    'descricao': final_df.loc[idx, col_desc],
                                    'unidade': final_df.loc[idx, col_unit],
                                    'apelido_original': original_apelido,
                                    'apelido_corrigido': edited_apelido
                                })
                
                # Se houver mudanças, mostrar botão para aplicar
                if changes_made:
                    st.success(f"✓ {len(corrections)} alteração(ões) detectada(s)!")
                    
                    # Mostrar preview das correções
                    with st.expander("📋 Ver Correções"):
                        corrections_preview = pd.DataFrame(corrections)
                        st.dataframe(corrections_preview, use_container_width=True)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("💾 Aplicar Correções", type="primary", use_container_width=True):
                            # Aplicar correções ao dataframe original
                            for correction in corrections:
                                idx = correction['index']
                                new_apelido = correction['apelido_corrigido']
                                
                                # Atualizar apelido
                                final_df.loc[idx, 'tax_apelido'] = new_apelido
                                
                                # Atualizar tipo e status baseado no novo apelido
                                if new_apelido:
                                    matching_rule = next(
                                        (r for r in engine.rules if r['apelido'] == new_apelido),
                                        None
                                    )
                                    if matching_rule:
                                        final_df.loc[idx, 'tax_tipo'] = matching_rule['dominio']
                                        final_df.loc[idx, 'tax_desconhecido'] = False
                                        final_df.loc[idx, 'tax_incerto'] = False # Confirmado, não é mais incerto
                                        final_df.loc[idx, 'tax_score'] = 100 # Confirmed
                                        
                            
                            # Salvar correções para aprendizado
                            corrections_dir = os.path.join(os.getcwd(), 'data', 'corrections')
                            os.makedirs(corrections_dir, exist_ok=True)
                            
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            corrections_file = os.path.join(corrections_dir, f"{timestamp}_corrections.csv")
                            
                            corrections_df = pd.DataFrame(corrections)
                            corrections_df.to_csv(corrections_file, index=False, encoding='utf-8-sig')
                            
                            st.success(f"✓ Correções aplicadas com sucesso! Salvas em `{os.path.basename(corrections_file)}`")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("↩️ Descartar Alterações", use_container_width=True):
                            st.rerun()

                
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
