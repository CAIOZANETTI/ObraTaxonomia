
import os
import pandas as pd
import sys
import glob

# Ensure we can import from project root
sys.path.append(os.getcwd())
from obra_taxonomia.header_utils import detect_header

def run_test():
    files = glob.glob("data/excel/*.xls*")
    print(f"Encontrados {len(files)} arquivos em data/excel/")
    
    for f_path in files:
        f_name = os.path.basename(f_path)
        print(f"\n{'='*40}")
        print(f"ARQUIVO: {f_name}")
        print(f"{'='*40}")
        
        try:
            xls = pd.ExcelFile(f_path)
            for sheet in xls.sheet_names:
                print(f"\n--- Aba: {sheet} ---")
                try:
                    df = pd.read_excel(xls, sheet_name=sheet, header=None) # Read raw
                    
                    if df.empty:
                        print("  [Vazia]")
                        continue
                        
                    result = detect_header(df)
                    
                    print(f"  Método: {result['method']}")
                    print(f"  Score: {result['score']:.2f}")
                    print(f"  Linha Cabeçalho: {result['header_row_idx']}")
                    
                    if result['mapping']:
                        print("  Mapeamento Encontrado:")
                        for k, v in result['mapping'].items():
                            val_preview = k if len(str(k)) < 20 else str(k)[:20] + "..."
                            print(f"    '{val_preview}' -> {v}")
                    else:
                        print("  (Nenhum mapeamento confiável)")
                        
                except Exception as e:
                    print(f"  Erro ao ler aba: {e}")
                    
        except Exception as e:
            print(f"Falha ao abrir arquivo: {e}")

if __name__ == "__main__":
    run_test()
