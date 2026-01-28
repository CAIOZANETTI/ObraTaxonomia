"""
Script de teste para verificar se os novos apelidos de escavação estão funcionando.
Testa com o arquivo do túnel submerso.
"""
import sys
import os
import pandas as pd

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine
from scripts.utils import normalize_text

def test_excavation_nicknames():
    """Testa os novos apelidos de escavação com o arquivo do túnel."""
    
    # Carregar taxonomia
    yaml_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'yaml')
    builder = TaxonomyBuilder(yaml_dir)
    builder.load_all()
    
    classifier = ClassifierEngine(builder)
    
    # Carregar arquivo do túnel
    excel_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'excel', '06_plan_tunel_submerso.xlsx')
    
    print(f"Carregando arquivo: {excel_file}")
    df = pd.read_excel(excel_file)
    
    print(f"\nTotal de linhas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    
    # Procurar por descrições de escavação
    desc_col = None
    for col in df.columns:
        if 'descri' in col.lower() or 'item' in col.lower():
            desc_col = col
            break
    
    if not desc_col:
        print("Coluna de descrição não encontrada!")
        return
    
    unit_col = None
    for col in df.columns:
        if 'unid' in col.lower() or 'un' in col.lower():
            unit_col = col
            break
    
    print(f"\nUsando coluna de descrição: {desc_col}")
    print(f"Usando coluna de unidade: {unit_col}")
    
    # Testar classificação de itens de escavação
    print("\n" + "="*80)
    print("TESTANDO CLASSIFICAÇÃO DE ESCAVAÇÃO")
    print("="*80)
    
    escavacao_items = []
    for idx, row in df.iterrows():
        desc = str(row[desc_col])
        unit = str(row[unit_col]) if unit_col else ''
        
        if 'escav' in desc.lower():
            apelido, tipo, desconhecido, score = classifier.classify_row(desc, unit)
            
            escavacao_items.append({
                'descricao_original': desc,
                'unidade': unit,
                'apelido': apelido,
                'score': score,
                'tipo': tipo,
                'desconhecido': desconhecido
            })
    
    print(f"\nEncontrados {len(escavacao_items)} itens de escavação")
    
    # Mostrar resultados
    for item in escavacao_items:
        print(f"\n{'-'*80}")
        print(f"Descrição: {item['descricao_original']}")
        print(f"Unidade: {item['unidade']}")
        print(f"Apelido: {item['apelido']}")
        print(f"Score: {item['score']}")
        print(f"Tipo: {item['tipo']}")
        print(f"Desconhecido: {item['desconhecido']}")
    
    # Verificar se os novos apelidos foram usados
    print("\n" + "="*80)
    print("RESUMO DE APELIDOS UTILIZADOS")
    print("="*80)
    
    apelidos_count = {}
    for item in escavacao_items:
        apelido = item['apelido'] if item['apelido'] else 'DESCONHECIDO'
        apelidos_count[apelido] = apelidos_count.get(apelido, 0) + 1
    
    for apelido, count in sorted(apelidos_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{apelido}: {count} ocorrências")
    
    # Verificar se os novos apelidos estão presentes
    novos_apelidos = [
        'escavacao_mec_solo_m3',
        'escavacao_mec_alterada_m3',
        'escavacao_mec_vala_solo_m3',
        'escavacao_mec_solo-mole_m3',
        'escavacao_manual_solo_m3'
    ]
    
    print("\n" + "="*80)
    print("VERIFICAÇÃO DOS NOVOS APELIDOS")
    print("="*80)
    
    for novo in novos_apelidos:
        if novo in apelidos_count:
            print(f"[OK] {novo}: ENCONTRADO ({apelidos_count[novo]} vezes)")
        else:
            print(f"[X] {novo}: NAO ENCONTRADO")
    
    return escavacao_items

if __name__ == '__main__':
    test_excavation_nicknames()
