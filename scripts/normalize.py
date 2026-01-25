"""
Módulo de Normalização de Texto e Números

Implementa normalização configurável de descrições de itens de orçamento
com auditoria completa de alterações.
"""

import re
import pandas as pd
from typing import Dict, List, Tuple
from scripts.utils import normalize_text


# Stopwords PT-BR comuns em descrições de orçamento
STOPWORDS_PT = {
    'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 'nos', 'nas',
    'a', 'o', 'e', 'para', 'com', 'sem', 'por', 'ao', 'aos', 'à', 'às',
    'um', 'uma', 'uns', 'umas', 'ou', 'como', 'mais', 'menos'
}


def normalize_sticky_numbers(text: str) -> str:
    """
    Separa números colados a letras, preservando traços de argamassa.
    
    Exemplos:
        'fck30' → 'fck 30'
        'dn100' → 'dn 100'
        'ø20' → 'ø 20'
        '1:3' → '1:3' (preservado)
        '1:2:3' → '1:2:3' (preservado)
    
    Args:
        text: Texto a normalizar
        
    Returns:
        Texto com números separados
    """
    # Preservar traços de argamassa (padrão: número:número ou número:número:número)
    # Substituir temporariamente por placeholder
    trace_pattern = r'(\d+:\d+(?::\d+)?)'
    traces = re.findall(trace_pattern, text)
    
    for i, trace in enumerate(traces):
        text = text.replace(trace, f'__TRACE{i}__')
    
    # Separar números colados a letras
    # Padrão: letra seguida de número (ex: fck30 → fck 30)
    text = re.sub(r'([a-záàâãéèêíïóôõöúçñ])(\d+)', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Padrão: número seguido de letra (ex: 30mpa → 30 mpa)
    text = re.sub(r'(\d+)([a-záàâãéèêíïóôõöúçñ])', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Restaurar traços de argamassa
    for i, trace in enumerate(traces):
        text = text.replace(f'__TRACE{i}__', trace)
    
    return text


def remove_stopwords(text: str, stopwords: set = STOPWORDS_PT) -> str:
    """
    Remove stopwords do texto.
    
    Args:
        text: Texto a processar
        stopwords: Conjunto de stopwords
        
    Returns:
        Texto sem stopwords
    """
    words = text.split()
    filtered = [w for w in words if w.lower() not in stopwords]
    return ' '.join(filtered)


def normalize_decimal(text: str) -> Tuple[str, bool]:
    """
    Detecta e normaliza decimais (vírgula → ponto).
    
    Args:
        text: Texto a normalizar
        
    Returns:
        (texto_normalizado, tem_decimal_virgula)
    """
    has_comma_decimal = False
    
    # Detectar padrão de decimal com vírgula (ex: 3,5 ou 12,75)
    comma_decimal_pattern = r'\b(\d+),(\d+)\b'
    
    if re.search(comma_decimal_pattern, text):
        has_comma_decimal = True
        # Substituir vírgula por ponto
        text = re.sub(comma_decimal_pattern, r'\1.\2', text)
    
    return text, has_comma_decimal


def normalize_dataframe(
    df: pd.DataFrame,
    config: Dict[str, bool],
    col_desc: str = 'descricao'
) -> Tuple[pd.DataFrame, List[Dict]]:
    """
    Normaliza DataFrame com auditoria de alterações.
    
    Args:
        df: DataFrame a normalizar
        config: Configuração de normalização:
            - remove_accents: bool
            - remove_punctuation: bool
            - remove_stopwords: bool
            - collapse_spaces: bool
            - normalize_numbers: bool
        col_desc: Nome da coluna de descrição
        
    Returns:
        (df_normalizado, audit_log)
    """
    if col_desc not in df.columns:
        raise ValueError(f"Coluna '{col_desc}' não encontrada no DataFrame")
    
    df_norm = df.copy()
    audit_log = []
    
    # Criar coluna de descrição normalizada
    df_norm['descricao_norm'] = df_norm[col_desc].astype(str)
    
    # Contador de alterações por regra
    stats = {
        'sticky_numbers': 0,
        'stopwords': 0,
        'decimals': 0,
        'accents': 0,
        'punctuation': 0,
        'spaces': 0,
        'zeroed': 0,
        'removed_empty': 0,
        'duplicates_removed': 0
    }
    }
    
    # Lista de linhas zeradas (para reverter)
    zeroed_rows = []
    
    # 0. Remover linhas vazias (Strict Cleaning)
    # Remove NaN, None, string "None", string vazia ou só espaços NA COLUNA DE DESCRIÇÃO
    if config.get('remove_empty_rows', True): # Default True
        initial_count = len(df_norm)
        
        # Converter para string e normalizar para check
        # 'coerce' transforma dtypes não str em str, mas NaN vira 'nan'
        temp_desc = df_norm[col_desc].astype(str).str.strip().str.lower()
        
        # Critérios de INVALIDADE (Se der True, a linha cai fora)
        mask_invalid = (
            (df_norm[col_desc].isna()) |          # NaN real
            (temp_desc == 'nan') |                # String 'nan'
            (temp_desc == 'none') |               # String 'none'
            (temp_desc == '') |                   # Vazio
            (temp_desc == '0') |                  # As vezes 0 é lixo
            (temp_desc == 'item')                 # Títulos perdidos
        )
        
        df_norm = df_norm[~mask_invalid].reset_index(drop=True)
        removed_count = initial_count - len(df_norm)
        
        if removed_count > 0:
            stats['removed_empty'] = removed_count
            audit_log.append({
                'tipo': 'rows_removed',
                'quantidade': removed_count,
                 'msg': f"{removed_count} linhas removidas (Descrição vazia ou 'None')."
            })

    for idx, row in df_norm.iterrows():
        original = str(row[col_desc])
        current = original
        
        # 1. Separar números colados
        if config.get('normalize_numbers', True):
            before = current
            current = normalize_sticky_numbers(current)
            if current != before:
                stats['sticky_numbers'] += 1
        
        # 2. Normalizar decimais
        if config.get('normalize_numbers', True):
            before = current
            current, has_comma = normalize_decimal(current)
            if has_comma:
                stats['decimals'] += 1
                audit_log.append({
                    'linha': idx,
                    'tipo': 'decimal_comma',
                    'original': before,
                    'normalizado': current
                })
        
        # 3. Remover acentos e converter para minúsculo
        if config.get('remove_accents', True):
            before = current
            current = normalize_text(current)  # Usa função de utils.py
            if current != before.lower():
                stats['accents'] += 1
        
        # 4. Remover pontuação (exceto traços de argamassa)
        if config.get('remove_punctuation', True):
            before = current
            # Preservar traços de argamassa
            trace_pattern = r'(\d+:\d+(?::\d+)?)'
            traces = re.findall(trace_pattern, current)
            
            for i, trace in enumerate(traces):
                current = current.replace(trace, f'__TRACE{i}__')
            
            # Remover pontuação
            current = re.sub(r'[^\w\s]', ' ', current)
            
            # Restaurar traços
            for i, trace in enumerate(traces):
                current = current.replace(f'__TRACE{i}__', trace)
            
            if current != before:
                stats['punctuation'] += 1
        
        # 5. Remover stopwords
        if config.get('remove_stopwords', False):
            before = current
            current = remove_stopwords(current)
            if current != before:
                stats['stopwords'] += 1
        
        # 6. Colapsar espaços
        if config.get('collapse_spaces', True):
            before = current
            current = re.sub(r'\s+', ' ', current).strip()
            if current != before:
                stats['spaces'] += 1
        
        # 7. Verificar se zerou
        if not current or current.isspace():
            zeroed_rows.append(idx)
            stats['zeroed'] += 1
            # Reverter para original normalizado básico
            current = normalize_text(original)
            audit_log.append({
                'linha': idx,
                'tipo': 'zeroed_reverted',
                'original': original,
                'tentativa': '',
                'revertido': current,
                'warning': 'Descrição zerada após normalização, revertido para normalização básica'
            })
        
        df_norm.at[idx, 'descricao_norm'] = current
    
    # 8. Deduplicação (Opção 1: Keep First)
    if config.get('remove_duplicates', False):
        before_dedup = len(df_norm)
        # Considerar Unidade se existir, senão só descrição
        subset_cols = ['descricao_norm']
        if 'unidade' in df_norm.columns:
            subset_cols.append('unidade')
            
        df_norm = df_norm.drop_duplicates(subset=subset_cols, keep='first').reset_index(drop=True)
        dedup_count = before_dedup - len(df_norm)
        
        if dedup_count > 0:
            stats['duplicates_removed'] = dedup_count
            audit_log.append({
                'tipo': 'duplicates_removed',
                'quantidade': dedup_count,
                'msg': f"{dedup_count} itens duplicados removidos (mantida a 1ª ocorrência)."
            })
    
    # Adicionar estatísticas ao log
    audit_log.insert(0, {
        'tipo': 'summary',
        'total_linhas': len(df_norm),
        'alteracoes': stats,
        'linhas_zeradas_revertidas': len(zeroed_rows)
    })
    
    return df_norm, audit_log


def get_normalization_report(audit_log: List[Dict]) -> str:
    """
    Gera relatório legível do audit log.
    
    Args:
        audit_log: Log de auditoria
        
    Returns:
        Relatório em texto
    """
    if not audit_log:
        return "Nenhuma alteração registrada"
    
    summary = audit_log[0]
    if summary.get('tipo') != 'summary':
        return "Log inválido"
    
    stats = summary.get('alteracoes', {})
    
    report = "=== Relatório de Normalização ===\n\n"
    report += f"Total de linhas processadas: {summary.get('total_linhas', 0)}\n\n"
    report += "Alterações por regra:\n"
    report += f"  - Números colados separados: {stats.get('sticky_numbers', 0)}\n"
    report += f"  - Decimais normalizados (vírgula → ponto): {stats.get('decimals', 0)}\n"
    report += f"  - Acentos removidos: {stats.get('accents', 0)}\n"
    report += f"  - Pontuação removida: {stats.get('punctuation', 0)}\n"
    report += f"  - Stopwords removidas: {stats.get('stopwords', 0)}\n"
    report += f"  - Espaços colapsados: {stats.get('spaces', 0)}\n"
    report += f"  - Descrições zeradas (revertidas): {stats.get('zeroed', 0)}\n"
    if stats.get('removed_empty', 0) > 0:
        report += f"  - Linhas removidas (vazias): {stats.get('removed_empty', 0)}\n"
    if stats.get('duplicates_removed', 0) > 0:
        report += f"  - Duplicatas removidas: {stats.get('duplicates_removed', 0)}\n"
    
    # Avisos de decimais
    decimal_warnings = [log for log in audit_log if log.get('tipo') == 'decimal_comma']
    if decimal_warnings:
        report += f"\n⚠️  {len(decimal_warnings)} linhas tinham decimais com vírgula (convertidos para ponto)\n"
    
    # Avisos de reversões
    zeroed_warnings = [log for log in audit_log if log.get('tipo') == 'zeroed_reverted']
    if zeroed_warnings:
        report += f"\n⚠️  {len(zeroed_warnings)} linhas foram revertidas (normalização zerou descrição)\n"
    
    return report


if __name__ == '__main__':
    # Teste básico
    test_df = pd.DataFrame({
        'descricao': [
            'Concreto fck30 bombeável',
            'Armação CA-50 ø20mm',
            'Argamassa traço 1:3',
            'Cimento Portland CP-II',
            'Tubo DN100 PVC'
        ],
        'unidade': ['m3', 'kg', 'm3', 'kg', 'm']
    })
    
    config = {
        'remove_accents': True,
        'remove_punctuation': True,
        'remove_stopwords': False,
        'collapse_spaces': True,
        'normalize_numbers': True
    }
    
    df_norm, log = normalize_dataframe(test_df, config)
    
    print("=== Teste de Normalização ===\n")
    print("Original vs Normalizado:")
    for idx, row in df_norm.iterrows():
        print(f"{row['descricao']} → {row['descricao_norm']}")
    
    print("\n" + get_normalization_report(log))
