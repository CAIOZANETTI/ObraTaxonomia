"""
Módulo de Gerenciamento de Unknowns (Itens Desconhecidos)

Responsável por agregar, contabilizar e exportar itens que não foram classificados
corretamente ou que possuem unidades incompatíveis, para posterior curadoria ou
treinamento de modelos.
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

def aggregate_unknowns(df: pd.DataFrame, 
                      col_desc_norm: str = 'descricao_norm',
                      col_unit: str = 'unidade',
                      col_unknown: str = 'tax_desconhecido') -> pd.DataFrame:
    """
    Agrega itens desconhecidos por descrição normalizada e unidade.
    
    Args:
        df: DataFrame contendo os dados processados
        col_desc_norm: Nome da coluna de descrição normalizada
        col_unit: Nome da coluna de unidade
        col_unknown: Nome da coluna booleana que indica se é desconhecido
        
    Returns:
        DataFrame agregado com colunas:
        - descricao_norm
        - unidade
        - ocorrencias
        - exemplos (lista de descrições originais, limitado a 3)
    """
    if col_unknown not in df.columns:
        return pd.DataFrame()
        
    # Filtrar apenas desconhecidos
    unknowns = df[df[col_unknown] == True].copy()
    
    if unknowns.empty:
        return pd.DataFrame(columns=['descricao_norm', 'unidade', 'ocorrencias', 'exemplos'])
    
    # Garantir que colunas existam
    if col_desc_norm not in unknowns.columns:
        # Tentar fallback para 'descricao' se normalizado não existir
        if 'descricao' in unknowns.columns:
            col_desc_norm = 'descricao'
        else:
            raise ValueError(f"Coluna {col_desc_norm} não encontrada")
            
    # Agrupamento
    # Vamos agrupar por (descricao_norm, unidade)
    # E agregar: contagem, e lista de exemplos originais
    
    # Função auxiliar para pegar exemplos únicos
    def get_examples(series):
        return list(series.unique())[:3]
    
    col_orig_desc = 'descricao' if 'descricao' in df.columns else col_desc_norm
    
    aggregated = unknowns.groupby([col_desc_norm, col_unit]).agg(
        ocorrencias=(col_desc_norm, 'count'),
        exemplos=(col_orig_desc, get_examples)
    ).reset_index()
    
    # Ordenar por ocorrências (decrescente)
    aggregated = aggregated.sort_values('ocorrencias', ascending=False)
    
    return aggregated

def save_unknowns_jsonl(aggregated_df: pd.DataFrame, 
                       output_dir: str = 'data/unknowns/inbox') -> Optional[str]:
    """
    Salva o DataFrame de unknowns agregados em arquivo JSONL com timestamp.
    
    Args:
        aggregated_df: DataFrame retornado por aggregate_unknowns
        output_dir: Diretório onde salvar
        
    Returns:
        Caminho do arquivo salvo ou None se dataframe vazio
    """
    if aggregated_df.empty:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"unknowns_{timestamp}.jsonl"
    filepath = os.path.join(output_dir, filename)
    
    # Converter para formato de registros orientado a linhas
    records = aggregated_df.to_dict(orient='records')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            # Adicionar metadados extras se necessário
            record['timestamp'] = datetime.now().isoformat()
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
            
    return filepath

if __name__ == '__main__':
    # Teste simples
    df_test = pd.DataFrame({
        'descricao': ['Cimento CP-II', 'Cimento CP-II', 'Areia', 'Tijolo 8 furos'],
        'descricao_norm': ['cimento cp ii', 'cimento cp ii', 'areia', 'tijolo 8 furos'],
        'unidade': ['kg', 'kg', 'm3', 'un'],
        'tax_desconhecido': [True, True, True, False]
    })
    
    agg = aggregate_unknowns(df_test)
    print("Agregado:")
    print(agg)
    
    path = save_unknowns_jsonl(agg, output_dir='tmp_unknowns_test')
    if path:
        print(f"Salvo em: {path}")
