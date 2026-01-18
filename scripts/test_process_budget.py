import pandas as pd
import os
import sys

# Add root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine

def test_processing(file_path):
    print(f"--- Iniciando teste com: {os.path.basename(file_path)} ---")
    
    # 1. Carregar Motor
    print("1. Carregando Regras...")
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'yaml')
    builder = TaxonomyBuilder(base_dir).load_all()
    engine = ClassifierEngine(builder)
    print(f"   Motor carregado com {len(engine.rules)} regras.")

    # 2. Leitura e Smart Detection (Lógica idêntica ao Streamlit)
    print("2. Lendo Arquivo Excel e Detectando Colunas...")
    try:
        sheets_dict = pd.read_excel(file_path, sheet_name=None, header=None)
        all_sheets = []
        
        desc_keywords = ['descricao', 'descrição', 'discriminacao', 'discriminação', 'especificacao', 'servico', 'item']
        unit_keywords = ['unid', 'unidade', 'und', 'un.', 'un']

        for sheet_name, raw_df in sheets_dict.items():
            print(f"   Processando aba: {sheet_name}")
            header_idx = -1
            
            for r_idx in range(min(len(raw_df), 20)):
                row_vals = raw_df.iloc[r_idx].astype(str).str.lower().tolist()
                has_desc = any(k in " ".join(row_vals) for k in desc_keywords)
                has_unit = any(k in " ".join(row_vals) for k in unit_keywords)
                
                if has_desc and has_unit:
                    header_idx = r_idx
                    break
            
            if header_idx != -1:
                # Deduplicação de colunas
                cols_raw = raw_df.iloc[header_idx].fillna('Unnamed').astype(str).tolist()
                seen = {}
                cols_dedup = []
                for c in cols_raw:
                    if c not in seen:
                        seen[c] = 0
                        cols_dedup.append(c)
                    else:
                        seen[c] += 1
                        cols_dedup.append(f"{c}_{seen[c]}")
                
                raw_df.columns = cols_dedup
                sheet_df = raw_df.iloc[header_idx+1:].copy()
                sheet_df.reset_index(drop=True, inplace=True)
                
                # Mapping
                new_map = {}
                for col in sheet_df.columns:
                    c_str = str(col).lower()
                    if any(k in c_str for k in desc_keywords) and 'System_Descricao' not in new_map.values():
                        new_map[col] = 'System_Descricao'
                    elif any(k == c_str.strip() or k + '.' in c_str for k in unit_keywords) and 'System_Unidade' not in new_map.values():
                        new_map[col] = 'System_Unidade'
                
                sheet_df.rename(columns=new_map, inplace=True)
            else:
                sheet_df = raw_df
                
            sheet_df['sheet_name'] = sheet_name
            
            if 'System_Descricao' not in sheet_df.columns: sheet_df['System_Descricao'] = None
            if 'System_Unidade' not in sheet_df.columns: sheet_df['System_Unidade'] = None
            
            all_sheets.append(sheet_df)

        df = pd.concat(all_sheets, ignore_index=True)
        print(f"   Consolidado: {len(df)} linhas de {len(sheets_dict)} abas.")
        
    except Exception as e:
        print(f"❌ Erro crítico na leitura do Excel: {e}")
        return

    # 3. Classificação
    if 'System_Descricao' in df.columns and 'System_Unidade' in df.columns:
        print("3. Classificando Itens...")
        
        # Filtra linhas vazias
        df_clean = df.dropna(subset=['System_Descricao']).copy()
        
        results_df = engine.process_dataframe(df_clean, col_desc='System_Descricao', col_unit='System_Unidade')
        final_df = pd.concat([df_clean.reset_index(drop=True), results_df], axis=1)
        
        total = len(final_df)
        unknowns = final_df[final_df['tax_desconhecido'] == True]
        count_unknown = len(unknowns)
        success_rate = ((total - count_unknown) / total) * 100 if total > 0 else 0
        
        print(f"\n=== RESULTADOS ===")
        print(f"Total Processado: {total}")
        print(f"Reconhecidos: {total - count_unknown}")
        print(f"Desconhecidos: {count_unknown}")
        print(f"Taxa de Sucesso: {success_rate:.2f}%")
        
        if count_unknown > 0:
            print("\nExemplos de Desconhecidos:")
            print(unknowns[['System_Descricao', 'System_Unidade', 'sheet_name']].head(5).to_string(index=False))
            
    else:
        print("⚠️ Colunas 'System_Descricao' e 'System_Unidade' não foram detectadas automaticamente.")

if __name__ == "__main__":
    target_file = r"d:\github\ObraTaxonomia\data\input\orcamento_tunel-submerso_santos.xlsx"
    if os.path.exists(target_file):
        test_processing(target_file)
    else:
        print(f"Arquivo não encontrado: {target_file}")
