"""
Script para reconstruir o master JSON a partir dos YAMLs.
"""
import sys
import os
import json

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.builder import TaxonomyBuilder

def rebuild_master():
    """Reconstrói o master JSON a partir dos YAMLs."""
    yaml_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'yaml')
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'master.json')
    
    print(f"Carregando YAMLs de: {yaml_dir}")
    builder = TaxonomyBuilder(yaml_dir)
    builder.load_all()
    
    # Salvar regras em JSON
    master_data = {
        'rules': builder.rules_cache,
        'units_map': builder.units_map
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    
    print(f"Master JSON salvo em: {output_file}")
    print(f"Total de regras: {len(builder.rules_cache)}")
    print(f"Total de unidades mapeadas: {len(builder.units_map)}")
    
    return builder

if __name__ == '__main__':
    rebuild_master()
