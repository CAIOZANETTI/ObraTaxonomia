"""
Script de teste completo para verificar todos os novos apelidos do aprendizado.
Testa com o arquivo do túnel submerso.
"""
import sys
import os
import pandas as pd

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine

def test_all_learning_nicknames():
    """Testa todos os novos apelidos do aprendizado com o arquivo do túnel."""
    
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
    
    # Procurar colunas
    desc_col = None
    for col in df.columns:
        if 'descri' in col.lower() or 'item' in col.lower():
            desc_col = col
            break
    
    unit_col = None
    for col in df.columns:
        if 'unid' in col.lower() or 'un' in col.lower():
            unit_col = col
            break
    
    print(f"\nUsando coluna de descricao: {desc_col}")
    print(f"Usando coluna de unidade: {unit_col}")
    
    # Classificar todos os itens
    print("\n" + "="*80)
    print("CLASSIFICANDO TODOS OS ITENS")
    print("="*80)
    
    all_items = []
    for idx, row in df.iterrows():
        desc = str(row[desc_col])
        unit = str(row[unit_col]) if unit_col else ''
        
        apelido, tipo, desconhecido, score = classifier.classify_row(desc, unit)
        
        all_items.append({
            'descricao': desc,
            'unidade': unit,
            'apelido': apelido if apelido else 'DESCONHECIDO',
            'tipo': tipo if tipo else 'N/A',
            'score': score
        })
    
    # Resumo de apelidos
    print("\n" + "="*80)
    print("RESUMO DE APELIDOS UTILIZADOS")
    print("="*80)
    
    apelidos_count = {}
    for item in all_items:
        apelido = item['apelido']
        apelidos_count[apelido] = apelidos_count.get(apelido, 0) + 1
    
    for apelido, count in sorted(apelidos_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{apelido}: {count} ocorrencias")
    
    # Verificar novos apelidos do CSV aprendizado_revisar.csv
    novos_apelidos_demolicao = [
        'demolicao_concreto_armado_m3',
        'demolicao_concreto_m3'
    ]
    
    novos_apelidos_asfalto = [
        'concreto_asfaltico_binder_m3',
        'concreto_asfaltico_m3',
        'calcada_concreto_m3',
        'sarjeta_m3'
    ]
    
    novos_apelidos_aco = [
        'aco_estrutural_kg'
    ]
    
    novos_apelidos_eletrica = [
        'tomada_eletrica_32a_unid'
    ]
    
    novos_apelidos_alvenaria = [
        'alvenaria_bloco_concreto_m2',
        'piso_elevado_m2'
    ]
    
    print("\n" + "="*80)
    print("VERIFICACAO DOS NOVOS APELIDOS - DEMOLICAO")
    print("="*80)
    for novo in novos_apelidos_demolicao:
        if novo in apelidos_count:
            print(f"[OK] {novo}: ENCONTRADO ({apelidos_count[novo]} vezes)")
        else:
            print(f"[X] {novo}: NAO ENCONTRADO")
    
    print("\n" + "="*80)
    print("VERIFICACAO DOS NOVOS APELIDOS - ASFALTO/PAVIMENTACAO")
    print("="*80)
    for novo in novos_apelidos_asfalto:
        if novo in apelidos_count:
            print(f"[OK] {novo}: ENCONTRADO ({apelidos_count[novo]} vezes)")
        else:
            print(f"[X] {novo}: NAO ENCONTRADO")
    
    print("\n" + "="*80)
    print("VERIFICACAO DOS NOVOS APELIDOS - ACO ESTRUTURAL")
    print("="*80)
    for novo in novos_apelidos_aco:
        if novo in apelidos_count:
            print(f"[OK] {novo}: ENCONTRADO ({apelidos_count[novo]} vezes)")
        else:
            print(f"[X] {novo}: NAO ENCONTRADO")
    
    print("\n" + "="*80)
    print("VERIFICACAO DOS NOVOS APELIDOS - ELETRICA")
    print("="*80)
    for novo in novos_apelidos_eletrica:
        if novo in apelidos_count:
            print(f"[OK] {novo}: ENCONTRADO ({apelidos_count[novo]} vezes)")
        else:
            print(f"[X] {novo}: NAO ENCONTRADO")
    
    print("\n" + "="*80)
    print("VERIFICACAO DOS NOVOS APELIDOS - ALVENARIA/PISO")
    print("="*80)
    for novo in novos_apelidos_alvenaria:
        if novo in apelidos_count:
            print(f"[OK] {novo}: ENCONTRADO ({apelidos_count[novo]} vezes)")
        else:
            print(f"[X] {novo}: NAO ENCONTRADO")
    
    # Estatísticas gerais
    total_classificados = len([i for i in all_items if i['apelido'] != 'DESCONHECIDO'])
    total_desconhecidos = len([i for i in all_items if i['apelido'] == 'DESCONHECIDO'])
    
    print("\n" + "="*80)
    print("ESTATISTICAS GERAIS")
    print("="*80)
    print(f"Total de itens: {len(all_items)}")
    print(f"Classificados: {total_classificados} ({100*total_classificados/len(all_items):.1f}%)")
    print(f"Desconhecidos: {total_desconhecidos} ({100*total_desconhecidos/len(all_items):.1f}%)")
    print(f"Total de apelidos unicos: {len(apelidos_count)}")
    
    return all_items

if __name__ == '__main__':
    test_all_learning_nicknames()
