---
skill_name: "Python Best Practices"
agent: tech_lead_data
category: "Development"
difficulty: intermediate
version: 1.0.0
---

# Skill: Python - Guia de Estilo e Boas Práticas (PEP8)

## Objetivo

Fornecer diretrizes de codificação Python seguindo PEP8 e boas práticas de engenharia de software para garantir código limpo, manutenível e profissional.

## Fundamentos - PEP8

### 1. Nomenclatura (Naming Conventions)

```python
# Módulos e pacotes: lowercase_com_underscores
import orcamento_builder
from scripts.taxonomy import TaxonomyEngine

# Classes: PascalCase
class TaxonomyBuilder:
    pass

class OrcamentoValidator:
    pass

# Funções e variáveis: snake_case
def calcular_custo_total(itens: list) -> float:
    custo_unitario = 10.50
    quantidade_total = sum(item.qtd for item in itens)
    return custo_unitario * quantidade_total

# Constantes: UPPER_CASE_COM_UNDERSCORES
MAX_TENTATIVAS = 3
TAXA_BDI_PADRAO = 0.28
CAMINHO_DADOS = "data/master/"

# Variáveis privadas: _prefixo_underscore
class Orcamento:
    def __init__(self):
        self._cache_interno = {}
        self.__valor_secreto = 0  # Name mangling (muito privado)
```

### 2. Indentação e Formatação

```python
# Indentação: 4 espaços (NUNCA tabs)
def processar_orcamento(
    arquivo_csv: str,
    aplicar_bdi: bool = True,
    taxa_bdi: float = 0.28
) -> pd.DataFrame:
    """
    Processa orçamento de arquivo CSV.
    
    Args:
        arquivo_csv: Caminho do arquivo
        aplicar_bdi: Se deve aplicar BDI
        taxa_bdi: Taxa de BDI a aplicar
    
    Returns:
        DataFrame processado
    """
    # Linha máxima: 79-100 caracteres
    df = pd.read_csv(arquivo_csv)
    
    if aplicar_bdi:
        df['preco_final'] = df['custo_direto'] * (1 + taxa_bdi)
    
    return df

# Quebra de linha em listas longas
itens_estrutura = [
    'pilares',
    'vigas',
    'lajes',
    'escadas',
    'fundacoes'
]

# Quebra de linha em dicionários
config_taxonomia = {
    'versao': '4.0',
    'modo': 'producao',
    'cache_habilitado': True,
    'timeout_segundos': 30
}
```

### 3. Imports

```python
# Ordem dos imports:
# 1. Biblioteca padrão
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# 2. Bibliotecas de terceiros
import pandas as pd
import numpy as np
import streamlit as st

# 3. Módulos locais
from scripts.builder import TaxonomyBuilder
from scripts.classify import ClassifierEngine

# Evitar: from module import *
# Preferir: import específico ou alias
from scripts.utils import normalizar_texto, calcular_similaridade
```

### 4. Docstrings (PEP 257)

```python
def calcular_capacidade_estaca(
    tipo_estaca: str,
    diametro_m: float,
    comprimento_m: float,
    N_SPT: float
) -> Dict[str, float]:
    """
    Calcula capacidade de carga de estaca pelo método Aoki-Velloso.
    
    Esta função implementa o método semi-empírico brasileiro para
    determinação da capacidade de carga de fundações profundas.
    
    Args:
        tipo_estaca: Tipo da estaca ('helice_continua', 'escavada', etc.)
        diametro_m: Diâmetro da estaca em metros
        comprimento_m: Comprimento embutido em metros
        N_SPT: Valor médio do SPT ao longo do fuste
    
    Returns:
        Dicionário contendo:
            - 'Q_ponta_kN': Resistência de ponta (kN)
            - 'Q_lateral_kN': Resistência lateral (kN)
            - 'Q_ult_kN': Capacidade última (kN)
            - 'Q_adm_kN': Capacidade admissível (kN)
    
    Raises:
        ValueError: Se tipo_estaca não for reconhecido
        ValueError: Se diametro_m ou comprimento_m forem negativos
    
    Examples:
        >>> calcular_capacidade_estaca('helice_continua', 0.4, 12.0, 15)
        {'Q_ponta_kN': 245.2, 'Q_lateral_kN': 380.5, ...}
    
    References:
        Aoki, N.; Velloso, D. A. (1975). "An approximate method to estimate
        the bearing capacity of piles". Proceedings of the 5th Pan-American
        Conference on Soil Mechanics and Foundation Engineering.
    """
    # Implementação...
    pass
```

### 5. Type Hints (PEP 484)

```python
from typing import List, Dict, Optional, Union, Tuple

def processar_itens(
    itens: List[Dict[str, Union[str, float]]],
    filtro: Optional[str] = None
) -> Tuple[pd.DataFrame, int]:
    """
    Processa lista de itens de orçamento.
    
    Args:
        itens: Lista de dicionários com dados dos itens
        filtro: Filtro opcional a aplicar
    
    Returns:
        Tupla (DataFrame processado, número de itens filtrados)
    """
    df = pd.DataFrame(itens)
    
    if filtro:
        df = df[df['categoria'] == filtro]
    
    return df, len(df)

# Type hints para classes
class Orcamento:
    def __init__(self, nome: str, valor: float) -> None:
        self.nome: str = nome
        self.valor: float = valor
    
    def aplicar_desconto(self, percentual: float) -> float:
        return self.valor * (1 - percentual)
```

### 6. Tratamento de Erros

```python
# Específico, não genérico
try:
    df = pd.read_csv(arquivo)
except FileNotFoundError:
    logger.error(f"Arquivo não encontrado: {arquivo}")
    raise
except pd.errors.EmptyDataError:
    logger.warning(f"Arquivo vazio: {arquivo}")
    return pd.DataFrame()

# Usar context managers
with open('orcamento.csv', 'r', encoding='utf-8') as f:
    dados = f.read()

# Validação de entrada
def calcular_bdi(lucro: float, tributos: float) -> float:
    if not (0 <= lucro <= 1):
        raise ValueError(f"Lucro deve estar entre 0 e 1, recebido: {lucro}")
    
    if not (0 <= tributos < 1):
        raise ValueError(f"Tributos deve estar entre 0 e 1, recebido: {tributos}")
    
    return ((1 + lucro) / (1 - tributos)) - 1
```

### 7. List Comprehensions e Generators

```python
# List comprehension (quando resultado cabe na memória)
quadrados = [x**2 for x in range(10)]

# Com filtro
pares = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
mapeamento = {item['id']: item['nome'] for item in itens}

# Generator (para grandes volumes)
def ler_linhas_grandes_arquivo(caminho: str):
    with open(caminho, 'r') as f:
        for linha in f:
            yield linha.strip()

# Generator expression
soma_quadrados = sum(x**2 for x in range(1000000))  # Eficiente em memória
```

### 8. Logging

```python
import logging

# Configuração
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Uso
def processar_taxonomia(arquivo_yaml: str) -> dict:
    logger.info(f"Iniciando processamento de {arquivo_yaml}")
    
    try:
        with open(arquivo_yaml, 'r') as f:
            dados = yaml.safe_load(f)
        
        logger.debug(f"Carregados {len(dados)} itens")
        return dados
    
    except Exception as e:
        logger.error(f"Erro ao processar {arquivo_yaml}: {e}", exc_info=True)
        raise
```

### 9. Testes Unitários

```python
import unittest
import pandas as pd

class TestOrcamentoProcessor(unittest.TestCase):
    def setUp(self):
        """Executado antes de cada teste."""
        self.df_teste = pd.DataFrame({
            'item': ['Concreto', 'Aço'],
            'custo': [100.0, 200.0]
        })
    
    def test_aplicar_bdi(self):
        """Testa aplicação de BDI."""
        resultado = aplicar_bdi(self.df_teste, taxa=0.28)
        
        self.assertAlmostEqual(resultado.loc[0, 'preco_final'], 128.0)
        self.assertAlmostEqual(resultado.loc[1, 'preco_final'], 256.0)
    
    def test_validacao_taxa_negativa(self):
        """Testa que taxa negativa levanta erro."""
        with self.assertRaises(ValueError):
            aplicar_bdi(self.df_teste, taxa=-0.1)
    
    def tearDown(self):
        """Executado após cada teste."""
        pass

if __name__ == '__main__':
    unittest.main()
```

### 10. Checklist de Qualidade

Antes de commitar código Python:

- [ ] Código segue PEP8 (usar `flake8` ou `black`)
- [ ] Funções têm docstrings completas
- [ ] Type hints estão presentes
- [ ] Imports estão organizados
- [ ] Nomes de variáveis são descritivos
- [ ] Não há código comentado (deletar)
- [ ] Testes unitários foram escritos
- [ ] Logging adequado está presente
- [ ] Tratamento de erros é específico
- [ ] Código foi revisado (code review)

### 11. Ferramentas Recomendadas

```bash
# Formatação automática
pip install black
black scripts/

# Linting
pip install flake8
flake8 scripts/ --max-line-length=100

# Type checking
pip install mypy
mypy scripts/

# Ordenação de imports
pip install isort
isort scripts/

# Tudo junto (pre-commit hook)
pip install pre-commit
```

## Outputs Esperados

Ao aplicar esta skill, o código deve:

1. **Passar em Linters**
   - `flake8` sem erros
   - `mypy` sem erros de tipo

2. **Ser Legível**
   - Nomes descritivos
   - Funções pequenas (< 50 linhas)
   - Complexidade ciclomática < 10

3. **Estar Documentado**
   - Docstrings em todas as funções públicas
   - README.md atualizado
   - Comentários apenas onde necessário

## Referências

- **PEP 8** - Style Guide for Python Code
- **PEP 257** - Docstring Conventions
- **PEP 484** - Type Hints
- **Google Python Style Guide**
- **The Hitchhiker's Guide to Python**
