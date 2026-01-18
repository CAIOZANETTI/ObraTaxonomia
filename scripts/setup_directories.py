"""
Script para criar e configurar a estrutura de diretórios do projeto ObraTaxonomia.

Este script garante que todos os diretórios necessários existam antes de executar
a aplicação, evitando erros de "diretório não encontrado".

Uso:
    python scripts/setup_directories.py
"""
import os
from pathlib import Path


def setup_project_directories(base_dir=None):
    """
    Cria estrutura de diretórios do projeto.
    
    Args:
        base_dir: Diretório base do projeto (padrão: diretório atual)
    
    Returns:
        List[str]: Lista de diretórios criados
    """
    if base_dir is None:
        base_dir = os.getcwd()
    
    # Diretórios necessários
    directories = [
        'data/input',                # Arquivos Excel de entrada
        'data/output',               # Saídas gerais
        'data/output/csv_extracted', # CSVs extraídos de XLSX
        'data/unknowns',             # Itens não reconhecidos (para aprendizado)
        'data/processed',            # Itens já processados/arquivados
    ]
    
    created = []
    
    print("=" * 60)
    print("CONFIGURAÇÃO DE DIRETÓRIOS - ObraTaxonomia")
    print("=" * 60)
    print(f"\nDiretório base: {base_dir}\n")
    
    for dir_path in directories:
        full_path = os.path.join(base_dir, dir_path)
        
        if os.path.exists(full_path):
            print(f"[OK] {dir_path:30s} (já existe)")
        else:
            os.makedirs(full_path, exist_ok=True)
            created.append(dir_path)
            print(f"[+]  {dir_path:30s} (criado)")
        
        # Criar .gitkeep para diretórios vazios importantes
        if dir_path in ['data/unknowns', 'data/processed']:
            gitkeep_path = os.path.join(full_path, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                Path(gitkeep_path).touch()
                print(f"     +- .gitkeep criado")

    
    print("\n" + "=" * 60)
    
    if created:
        print(f"[OK] {len(created)} diretorio(s) criado(s) com sucesso!")
    else:
        print("[OK] Todos os diretorios ja existem!")
    
    print("=" * 60)
    
    return created


def verify_structure(base_dir=None):
    """
    Verifica se a estrutura de diretórios está completa.
    
    Args:
        base_dir: Diretório base do projeto (padrão: diretório atual)
    
    Returns:
        bool: True se todos os diretórios existem, False caso contrário
    """
    if base_dir is None:
        base_dir = os.getcwd()
    
    required_dirs = [
        'data/input',
        'data/output',
        'data/output/csv_extracted',
        'data/unknowns',
        'data/processed',
    ]
    
    missing = []
    
    for dir_path in required_dirs:
        full_path = os.path.join(base_dir, dir_path)
        if not os.path.exists(full_path):
            missing.append(dir_path)
    
    if missing:
        print(f"[!] Diretorios faltando: {', '.join(missing)}")
        return False
    
    print("[OK] Estrutura de diretorios completa!")
    return True


if __name__ == "__main__":
    import sys
    
    # Permite especificar diretório base como argumento
    base = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Criar estrutura
    setup_project_directories(base)
    
    # Verificar
    print("\nVerificando estrutura...")
    verify_structure(base)
