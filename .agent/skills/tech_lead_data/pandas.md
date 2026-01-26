---
skill_name: "Pandas - Manipulação de Dados"
agent: tech_lead_data
category: "Data Science"
difficulty: intermediate
version: 1.0.0
---

# Skill: Pandas - Manipulação de DataFrames e Séries

## Objetivo

Fornecer guia prático de Pandas para manipulação eficiente de dados tabulares, essencial para processamento de orçamentos, análise de custos e ETL.

## Fundamentos

### 1. Estruturas de Dados

```python
import pandas as pd
import numpy as np

# Series (1D)
precos = pd.Series([100, 200, 300], index=['item_a', 'item_b', 'item_c'])

# DataFrame (2D - tabela)
orcamento = pd.DataFrame({
    'item': ['Concreto', 'Aço', 'Forma'],
    'quantidade': [120, 5000, 300],
    'unidade': ['m³', 'kg', 'm²'],
    'preco_unitario': [450.0, 8.5, 25.0]
})
```

### 2. Leitura e Escrita de Dados

```python
# CSV
df = pd.read_csv('orcamento.csv', encoding='utf-8')
df.to_csv('orcamento_processado.csv', index=False)

# Excel
df = pd.read_excel('orcamento.xlsx', sheet_name='Planilha1')
df.to_excel('resultado.xlsx', sheet_name='Processado', index=False)

# JSON
df = pd.read_json('dados.json')
df.to_json('resultado.json', orient='records')

# Parquet (eficiente)
df.to_parquet('dados.parquet')
df = pd.read_parquet('dados.parquet')
```

### 3. Seleção e Filtros

```python
# Selecionar colunas
df['item']  # Uma coluna (Series)
df[['item', 'preco_unitario']]  # Múltiplas colunas (DataFrame)

# Selecionar linhas por índice
df.iloc[0]  # Primeira linha
df.iloc[0:3]  # Primeiras 3 linhas
df.iloc[:, 0:2]  # Todas as linhas, 2 primeiras colunas

# Selecionar por label
df.loc[0, 'item']  # Valor específico
df.loc[df['quantidade'] > 100]  # Filtro booleano

# Filtros múltiplos
itens_caros = df[(df['preco_unitario'] > 100) & (df['quantidade'] > 50)]

# Query (SQL-like)
df.query('preco_unitario > 100 and quantidade > 50')
```

### 4. Operações com Colunas

```python
# Criar nova coluna
df['custo_total'] = df['quantidade'] * df['preco_unitario']

# Aplicar BDI
df['preco_final'] = df['custo_total'] * 1.28

# Operações condicionais
df['categoria'] = np.where(df['custo_total'] > 10000, 'Alto', 'Baixo')

# Apply (função customizada)
def classificar_custo(valor):
    if valor < 1000:
        return 'Baixo'
    elif valor < 10000:
        return 'Médio'
    else:
        return 'Alto'

df['classificacao'] = df['custo_total'].apply(classificar_custo)

# Lambda
df['descricao_upper'] = df['item'].apply(lambda x: x.upper())
```

### 5. Agrupamento e Agregação

```python
# GroupBy
resumo_por_categoria = df.groupby('categoria').agg({
    'custo_total': ['sum', 'mean', 'count'],
    'quantidade': 'sum'
})

# Pivot Table
pivot = df.pivot_table(
    values='custo_total',
    index='categoria',
    columns='unidade',
    aggfunc='sum',
    fill_value=0
)

# Exemplo prático: Resumo de orçamento por fase
df_orcamento = pd.DataFrame({
    'fase': ['Fundação', 'Fundação', 'Estrutura', 'Estrutura', 'Acabamento'],
    'item': ['Estacas', 'Blocos', 'Pilares', 'Vigas', 'Pintura'],
    'custo': [50000, 30000, 80000, 60000, 40000]
})

resumo = df_orcamento.groupby('fase')['custo'].agg(['sum', 'mean', 'count'])
print(resumo)
```

### 6. Merge e Join

```python
# Inner join
df_itens = pd.DataFrame({
    'item_id': [1, 2, 3],
    'descricao': ['Concreto', 'Aço', 'Forma']
})

df_precos = pd.DataFrame({
    'item_id': [1, 2, 3],
    'preco': [450, 8.5, 25]
})

df_completo = pd.merge(df_itens, df_precos, on='item_id', how='inner')

# Left join (manter todos da esquerda)
df_left = pd.merge(df_itens, df_precos, on='item_id', how='left')

# Concatenar verticalmente
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
df_concat = pd.concat([df1, df2], ignore_index=True)
```

### 7. Limpeza de Dados

```python
# Valores faltantes
df.isnull().sum()  # Contar NaNs por coluna
df.dropna()  # Remover linhas com NaN
df.fillna(0)  # Preencher NaN com 0
df['coluna'].fillna(df['coluna'].mean())  # Preencher com média

# Duplicatas
df.duplicated().sum()  # Contar duplicatas
df.drop_duplicates(subset=['item'], keep='first')  # Remover duplicatas

# Renomear colunas
df.rename(columns={'old_name': 'new_name'}, inplace=True)

# Converter tipos
df['quantidade'] = df['quantidade'].astype(int)
df['data'] = pd.to_datetime(df['data'])

# Remover espaços
df['item'] = df['item'].str.strip()
df['item'] = df['item'].str.lower()
```

### 8. Operações de String

```python
# Métodos .str
df['item_upper'] = df['item'].str.upper()
df['item_lower'] = df['item'].str.lower()
df['item_title'] = df['item'].str.title()

# Contém
df_concreto = df[df['item'].str.contains('concreto', case=False)]

# Replace
df['item'] = df['item'].str.replace('aço', 'aco')

# Split
df[['tipo', 'subtipo']] = df['descricao'].str.split(' - ', expand=True)

# Extrair com regex
df['codigo'] = df['item'].str.extract(r'(\d+)')
```

### 9. Aplicação Prática: Pipeline de Orçamento

```python
def processar_orcamento_completo(arquivo_csv: str) -> pd.DataFrame:
    """
    Pipeline completo de processamento de orçamento.
    """
    # 1. Leitura
    df = pd.read_csv(arquivo_csv, encoding='utf-8')
    
    # 2. Limpeza
    df = df.dropna(subset=['item', 'quantidade', 'preco_unitario'])
    df = df.drop_duplicates(subset=['item'])
    df['item'] = df['item'].str.strip().str.lower()
    
    # 3. Cálculos
    df['custo_direto'] = df['quantidade'] * df['preco_unitario']
    df['bdi'] = 0.28
    df['preco_final'] = df['custo_direto'] * (1 + df['bdi'])
    
    # 4. Classificação
    df['categoria_custo'] = pd.cut(
        df['custo_direto'],
        bins=[0, 1000, 10000, np.inf],
        labels=['Baixo', 'Médio', 'Alto']
    )
    
    # 5. Ordenação
    df = df.sort_values('custo_direto', ascending=False)
    
    # 6. Resumo
    print(f"Total de itens: {len(df)}")
    print(f"Custo direto total: R$ {df['custo_direto'].sum():,.2f}")
    print(f"Preço final total: R$ {df['preco_final'].sum():,.2f}")
    
    return df

# Uso
df_processado = processar_orcamento_completo('orcamento_raw.csv')
```

### 10. Performance

```python
# Vetorização vs Apply vs Loop
import time

df = pd.DataFrame({'valor': np.random.rand(100000)})

# Loop (MUITO LENTO - EVITAR)
start = time.time()
resultado = []
for i in range(len(df)):
    resultado.append(df.loc[i, 'valor'] * 2)
tempo_loop = time.time() - start

# Apply (LENTO)
start = time.time()
resultado = df['valor'].apply(lambda x: x * 2)
tempo_apply = time.time() - start

# Vetorizado (RÁPIDO)
start = time.time()
resultado = df['valor'] * 2
tempo_vet = time.time() - start

print(f"Loop: {tempo_loop:.4f}s")
print(f"Apply: {tempo_apply:.4f}s")
print(f"Vetorizado: {tempo_vet:.4f}s")
# Vetorizado é 100-1000x mais rápido
```

### 11. Checklist

Ao usar Pandas:

- [ ] Usar operações vetorizadas (evitar loops)
- [ ] Limpar dados (NaN, duplicatas, tipos)
- [ ] Usar `inplace=False` (evitar mutações inesperadas)
- [ ] Especificar `dtype` ao ler CSVs grandes
- [ ] Usar `query()` para filtros complexos
- [ ] Preferir `loc/iloc` a indexação encadeada
- [ ] Usar `groupby` + `agg` para resumos
- [ ] Salvar em Parquet para grandes volumes

## Referências

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Pandas Cheat Sheet**: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
- **Python for Data Analysis** (Wes McKinney)
