"""
Script de teste para extração de XLSX para CSV usando múltiplos métodos.
"""
import sys
import os

# Adicionar o diretório scripts ao path
sys.path.insert(0, os.path.dirname(__file__))

from utils import convert_xlsx_to_csv_all_methods

def main():
    # Arquivo de teste
    xlsx_path = r"d:\github\ObraTaxonomia\data\input\orcamento_tunel-submerso_santos.xlsx"
    output_dir = r"d:\github\ObraTaxonomia\data\output\csv_extracted"
    
    print("=" * 80)
    print("TESTE DE EXTRAÇÃO XLSX -> CSV")
    print("=" * 80)
    print(f"\nArquivo de entrada: {xlsx_path}")
    print(f"Diretório de saída: {output_dir}")
    print("\n" + "-" * 80)
    
    # Tentar converter
    result = convert_xlsx_to_csv_all_methods(xlsx_path, output_dir)
    
    print("\nRESULTADO:")
    print("-" * 80)
    print(f"Sucesso: {result['success']}")
    print(f"Método usado: {result['method']}")
    print(f"Mensagem: {result['message']}")
    print(f"\nArquivos gerados: {len(result['output_files'])}")
    
    if result['output_files']:
        print("\nArquivos CSV criados:")
        for i, file_path in enumerate(result['output_files'], 1):
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            print(f"  {i}. {os.path.basename(file_path)} ({file_size:,} bytes)")
    
    print("\n" + "-" * 80)
    print("HISTORICO DE TENTATIVAS:")
    print("-" * 80)
    
    for i, attempt in enumerate(result['attempts'], 1):
        status = "[OK] SUCESSO" if attempt['success'] else "[X] FALHOU"
        print(f"{i}. {attempt['method']:12s} - {status}")
        print(f"   {attempt['message']}")
    
    print("\n" + "=" * 80)
    
    if result['success']:
        print("[OK] Extracao concluida com sucesso!")
        return 0
    else:
        print("[X] Todas as tentativas falharam. Verifique as dependencias.")
        print("\nDependencias sugeridas:")
        print("  pip install openpyxl pandas xlsx2csv polars pywin32 xlwings pyexcel pyexcel-xlsx python-calamine")
        return 1


if __name__ == "__main__":
    sys.exit(main())
