"""
ETL Pipeline Module - ObraTaxonomia

Skill: Extract, Transform, Load (ETL)
Agent: tech_lead_data
Category: Data Engineering
Version: 1.0.0

Este módulo fornece funções genéricas para pipeline ETL de dados de engenharia,
com suporte a múltiplos formatos (CSV, Excel) e transformações padronizadas.

Padrões seguidos:
- PEP8 (Style Guide for Python Code)
- Google-style docstrings
- Type hints obrigatórios
- Logging estruturado
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Optional, Dict, Any
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_etl_pipeline(
    source_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    column_mapping: Optional[Dict[str, str]] = None,
    drop_duplicates: bool = True,
    fill_na_strategy: str = 'drop'
) -> pd.DataFrame:
    """
    Executa pipeline ETL completo: detecta formato, extrai, transforma e carrega dados.
    
    Este é o ponto de entrada principal para processamento de dados de engenharia.
    Suporta arquivos CSV e Excel (.xlsx, .xls), aplica transformações padronizadas
    e retorna DataFrame limpo e normalizado.
    
    Args:
        source_path: Caminho do arquivo de origem (CSV ou Excel).
        output_path: Caminho opcional para salvar DataFrame processado.
            Se None, não salva arquivo.
        column_mapping: Dicionário de mapeamento {nome_antigo: nome_novo}.
            Exemplo: {'Descrição': 'descricao', 'Qtd': 'quantidade'}
        drop_duplicates: Se True, remove linhas duplicadas.
        fill_na_strategy: Estratégia para valores nulos:
            - 'drop': Remove linhas com nulos
            - 'zero': Preenche com 0
            - 'forward': Forward fill (propaga último valor válido)
            - 'mean': Preenche com média da coluna (apenas numérico)
    
    Returns:
        pd.DataFrame: DataFrame processado e limpo.
    
    Raises:
        FileNotFoundError: Se arquivo não existe.
        ValueError: Se formato de arquivo não suportado.
        pd.errors.EmptyDataError: Se arquivo está vazio.
    
    Example:
        >>> df = run_etl_pipeline(
        ...     source_path='data/excel/orcamento.xlsx',
        ...     column_mapping={'Descrição': 'descricao', 'Qtd': 'quantidade'},
        ...     fill_na_strategy='zero'
        ... )
        >>> print(df.head())
    
    Notes:
        - Colunas são automaticamente normalizadas (lowercase, sem espaços)
        - Tipos de dados são inferidos automaticamente
        - Processo é idempotente (pode ser executado múltiplas vezes)
    """
    logger.info(f"Iniciando ETL pipeline para: {source_path}")
    
    # EXTRACT
    df = extract_data(source_path)
    logger.info(f"Extraídos {len(df)} registros de {source_path}")
    
    # TRANSFORM
    df = transform_data(
        df,
        column_mapping=column_mapping,
        drop_duplicates=drop_duplicates,
        fill_na_strategy=fill_na_strategy
    )
    logger.info(f"Transformação concluída: {len(df)} registros após limpeza")
    
    # LOAD
    if output_path:
        load_data(df, output_path)
        logger.info(f"Dados salvos em: {output_path}")
    
    return df


def extract_data(source_path: Union[str, Path]) -> pd.DataFrame:
    """
    Extrai dados de arquivo CSV ou Excel.
    
    Detecta automaticamente o formato do arquivo pela extensão e aplica
    o parser apropriado. Suporta múltiplas abas em arquivos Excel.
    
    Args:
        source_path: Caminho do arquivo de origem.
    
    Returns:
        pd.DataFrame: Dados extraídos.
    
    Raises:
        FileNotFoundError: Se arquivo não existe.
        ValueError: Se formato não suportado.
    
    Example:
        >>> df = extract_data('data/excel/orcamento.xlsx')
    """
    source_path = Path(source_path)
    
    if not source_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")
    
    extension = source_path.suffix.lower()
    
    if extension == '.csv':
        logger.debug(f"Detectado formato CSV: {source_path}")
        df = pd.read_csv(
            source_path,
            encoding='utf-8-sig',  # Suporta BOM
            sep=None,  # Detecta separador automaticamente
            engine='python'
        )
    
    elif extension in ['.xlsx', '.xls']:
        logger.debug(f"Detectado formato Excel: {source_path}")
        
        # Ler todas as abas
        excel_file = pd.ExcelFile(source_path)
        
        if len(excel_file.sheet_names) == 1:
            # Uma única aba
            df = pd.read_excel(source_path, sheet_name=0)
        else:
            # Múltiplas abas: concatenar com identificador de origem
            dfs = []
            for sheet_name in excel_file.sheet_names:
                df_sheet = pd.read_excel(source_path, sheet_name=sheet_name)
                df_sheet['aba_origem'] = sheet_name
                dfs.append(df_sheet)
            df = pd.concat(dfs, ignore_index=True)
            logger.info(f"Concatenadas {len(excel_file.sheet_names)} abas")
    
    else:
        raise ValueError(
            f"Formato não suportado: {extension}. "
            f"Suportados: .csv, .xlsx, .xls"
        )
    
    return df


def transform_data(
    df: pd.DataFrame,
    column_mapping: Optional[Dict[str, str]] = None,
    drop_duplicates: bool = True,
    fill_na_strategy: str = 'drop'
) -> pd.DataFrame:
    """
    Aplica transformações padronizadas ao DataFrame.
    
    Sequência de transformações:
    1. Normalizar nomes de colunas
    2. Aplicar mapeamento customizado
    3. Remover duplicatas
    4. Tratar valores nulos
    5. Inferir e converter tipos de dados
    
    Args:
        df: DataFrame de entrada.
        column_mapping: Mapeamento de nomes de colunas.
        drop_duplicates: Se True, remove duplicatas.
        fill_na_strategy: Estratégia para nulos ('drop', 'zero', 'forward', 'mean').
    
    Returns:
        pd.DataFrame: DataFrame transformado.
    
    Example:
        >>> df_clean = transform_data(
        ...     df,
        ...     column_mapping={'Descrição': 'descricao'},
        ...     fill_na_strategy='zero'
        ... )
    """
    df = df.copy()
    
    # 1. Normalizar nomes de colunas
    df = normalize_column_names(df)
    
    # 2. Aplicar mapeamento customizado
    if column_mapping:
        df = df.rename(columns=column_mapping)
        logger.debug(f"Aplicado mapeamento de colunas: {column_mapping}")
    
    # 3. Remover duplicatas
    if drop_duplicates:
        original_len = len(df)
        df = df.drop_duplicates()
        removed = original_len - len(df)
        if removed > 0:
            logger.info(f"Removidas {removed} linhas duplicadas")
    
    # 4. Tratar valores nulos
    df = handle_missing_values(df, strategy=fill_na_strategy)
    
    # 5. Inferir tipos de dados
    df = infer_data_types(df)
    
    return df


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nomes de colunas: lowercase, sem espaços, sem acentos.
    
    Transformações aplicadas:
    - Converte para minúsculas
    - Substitui espaços por underscore
    - Remove acentos
    - Remove caracteres especiais
    
    Args:
        df: DataFrame de entrada.
    
    Returns:
        pd.DataFrame: DataFrame com colunas normalizadas.
    
    Example:
        >>> df = pd.DataFrame({'Descrição Item': [1, 2], 'Qtd.': [10, 20]})
        >>> df_norm = normalize_column_names(df)
        >>> print(df_norm.columns.tolist())
        ['descricao_item', 'qtd']
    """
    import unicodedata
    import re
    
    def normalize_name(name: str) -> str:
        # Remover acentos
        name = unicodedata.normalize('NFKD', name)
        name = name.encode('ASCII', 'ignore').decode('ASCII')
        
        # Lowercase e substituir espaços
        name = name.lower().strip()
        name = re.sub(r'\s+', '_', name)
        
        # Remover caracteres especiais (manter apenas letras, números, underscore)
        name = re.sub(r'[^a-z0-9_]', '', name)
        
        return name
    
    df = df.copy()
    df.columns = [normalize_name(col) for col in df.columns]
    
    return df


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = 'drop'
) -> pd.DataFrame:
    """
    Trata valores nulos conforme estratégia especificada.
    
    Args:
        df: DataFrame de entrada.
        strategy: Estratégia ('drop', 'zero', 'forward', 'mean').
    
    Returns:
        pd.DataFrame: DataFrame com nulos tratados.
    
    Raises:
        ValueError: Se estratégia não reconhecida.
    """
    df = df.copy()
    
    if strategy == 'drop':
        df = df.dropna()
        logger.debug("Removidas linhas com valores nulos")
    
    elif strategy == 'zero':
        df = df.fillna(0)
        logger.debug("Valores nulos preenchidos com 0")
    
    elif strategy == 'forward':
        df = df.fillna(method='ffill')
        logger.debug("Aplicado forward fill para valores nulos")
    
    elif strategy == 'mean':
        # Preencher apenas colunas numéricas com média
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        logger.debug(f"Valores nulos preenchidos com média em {len(numeric_cols)} colunas")
    
    else:
        raise ValueError(
            f"Estratégia '{strategy}' não reconhecida. "
            f"Opções: 'drop', 'zero', 'forward', 'mean'"
        )
    
    return df


def infer_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Infere e converte tipos de dados automaticamente.
    
    Conversões aplicadas:
    - Strings numéricas → float/int
    - Datas em formato ISO → datetime
    - Booleanos ('sim'/'não', 'true'/'false') → bool
    
    Args:
        df: DataFrame de entrada.
    
    Returns:
        pd.DataFrame: DataFrame com tipos otimizados.
    """
    df = df.copy()
    
    for col in df.columns:
        # Tentar converter para numérico
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
        
        # Tentar converter para datetime
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except:
                pass
    
    logger.debug(f"Tipos de dados inferidos: {df.dtypes.to_dict()}")
    
    return df


def load_data(
    df: pd.DataFrame,
    output_path: Union[str, Path],
    format: str = 'auto'
) -> None:
    """
    Salva DataFrame em arquivo CSV ou Excel.
    
    Args:
        df: DataFrame a salvar.
        output_path: Caminho do arquivo de saída.
        format: Formato ('auto', 'csv', 'excel').
            Se 'auto', detecta pela extensão.
    
    Example:
        >>> load_data(df, 'data/output/processado.csv')
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'auto':
        extension = output_path.suffix.lower()
        format = 'csv' if extension == '.csv' else 'excel'
    
    if format == 'csv':
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    elif format == 'excel':
        df.to_excel(output_path, index=False, engine='openpyxl')
    
    else:
        raise ValueError(f"Formato '{format}' não suportado")
    
    logger.info(f"Dados salvos em: {output_path}")


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[List[str]] = None,
    min_rows: int = 1
) -> Dict[str, Any]:
    """
    Valida DataFrame conforme critérios especificados.
    
    Args:
        df: DataFrame a validar.
        required_columns: Lista de colunas obrigatórias.
        min_rows: Número mínimo de linhas.
    
    Returns:
        dict: Resultado da validação com status e mensagens.
    
    Example:
        >>> result = validate_dataframe(
        ...     df,
        ...     required_columns=['descricao', 'quantidade'],
        ...     min_rows=10
        ... )
        >>> if not result['valid']:
        ...     print(result['errors'])
    """
    errors = []
    warnings = []
    
    # Verificar número de linhas
    if len(df) < min_rows:
        errors.append(f"DataFrame tem {len(df)} linhas, mínimo requerido: {min_rows}")
    
    # Verificar colunas obrigatórias
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            errors.append(f"Colunas faltando: {missing_cols}")
    
    # Verificar valores nulos
    null_counts = df.isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if len(cols_with_nulls) > 0:
        warnings.append(f"Colunas com nulos: {cols_with_nulls.to_dict()}")
    
    # Verificar duplicatas
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        warnings.append(f"Encontradas {duplicates} linhas duplicadas")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'stats': {
            'num_rows': len(df),
            'num_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        }
    }


if __name__ == '__main__':
    # Exemplo de uso
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python etl.py <caminho_arquivo>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    output_file = source_file.replace('.xlsx', '_processado.csv').replace('.xls', '_processado.csv')
    
    try:
        df = run_etl_pipeline(
            source_path=source_file,
            output_path=output_file,
            fill_na_strategy='zero'
        )
        
        print(f"\n✅ ETL concluído com sucesso!")
        print(f"Registros processados: {len(df)}")
        print(f"Colunas: {list(df.columns)}")
        print(f"Arquivo salvo em: {output_file}")
        
    except Exception as e:
        logger.error(f"Erro no pipeline ETL: {e}", exc_info=True)
        sys.exit(1)
