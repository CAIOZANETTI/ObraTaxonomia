---
skill_name: "ObraTaxonomia - Uso em Engenharia"
agent: engenheiro_planejamento
category: "Orçamentação e Classificação"
difficulty: intermediate
version: 1.0.0
---

# Skill: ObraTaxonomia - Sistema de Classificação de Orçamentos

## Objetivo

Fornecer conhecimento sobre o sistema ObraTaxonomia v4 para uso em orçamentação, classificação automática de itens e análise de custos de obras.

## 1. Visão Geral do Sistema

**ObraTaxonomia** é um sistema de classificação automática de itens de orçamento de obras baseado em:
- **Taxonomia hierárquica** definida em arquivos YAML
- **Normalização de texto** para padronização de descrições
- **Matching fuzzy** para identificação de itens
- **Interface Streamlit** para processamento interativo

### Arquitetura do Fluxo

```
Excel/CSV → Upload → Mapeamento → Normalização → Classificação → Validação → Export
    ↓          ↓          ↓              ↓              ↓             ↓          ↓
  Dados    Colunas   Limpeza      tax_tipo        Apelidos      Revisão    CSV Final
  Brutos   Padrão    Texto        tax_grupo       Finais        Manual     Validado
```

## 2. Estrutura da Taxonomia

### Hierarquia

```
tax_tipo (Domínio)
  └─ tax_grupo (Categoria)
      └─ apelido (Item Específico)
```

**Exemplo:**
```
estrutura (tipo)
  └─ concreto (grupo)
      ├─ concreto_fck20
      ├─ concreto_fck25
      └─ concreto_fck30
```

### Tipos Principais

| tax_tipo | Descrição | Exemplos de Grupos |
|----------|-----------|-------------------|
| **estrutura** | Elementos estruturais | concreto, aco, forma |
| **fundacao** | Fundações | estaca, bloco, tubulao |
| **alvenaria** | Vedações | bloco_ceramico, bloco_concreto |
| **revestimento** | Acabamentos | argamassa, gesso, ceramica |
| **instalacao** | Instalações prediais | hidraulica, eletrica, gas |
| **cobertura** | Telhados e coberturas | telha, estrutura_madeira |

## 3. Uso do Sistema - Fluxo Completo

### Passo 1: Upload de Orçamento

```python
# O sistema aceita:
# - Excel (.xlsx, .xls) com múltiplas planilhas
# - CSV (.csv) com encoding UTF-8

# Estrutura mínima esperada:
# - Coluna de descrição (ex: "DESCRIÇÃO", "ITEM", "SERVIÇO")
# - Coluna de quantidade (ex: "QUANT", "QTD")
# - Coluna de unidade (ex: "UN", "UNID")
# - Coluna de preço unitário (ex: "P.UNIT", "PREÇO")
```

### Passo 2: Mapeamento de Colunas

O sistema identifica automaticamente colunas, mas permite ajuste manual:

```python
mapeamento_padrao = {
    'descricao': 'DESCRIÇÃO DO SERVIÇO',
    'quantidade': 'QUANT.',
    'unidade': 'UN.',
    'preco_unitario': 'PREÇO UNITÁRIO'
}
```

### Passo 3: Normalização

**Processo automático:**
1. Remoção de acentos
2. Conversão para minúsculas
3. Remoção de caracteres especiais
4. Padronização de espaços

**Exemplo:**
```
Original: "CONCRETO FCK=25MPa P/ ESTRUTURA"
Normalizado: "concreto fck 25 mpa estrutura"
```

### Passo 4: Classificação Automática

O sistema classifica cada item em:

```python
resultado_classificacao = {
    'tax_tipo': 'estrutura',           # Domínio
    'tax_grupo': 'concreto',           # Categoria
    'apelido_sugerido': 'concreto_fck25',  # Item específico
    'similaridade': 0.92,              # Score de confiança
    'status': 'ok',                    # ok | revisar | desconhecido
    'tax_desconhecido': False          # Flag de item não identificado
}
```

**Status:**
- **`ok`**: Classificação com alta confiança (similaridade > 0.8)
- **`revisar`**: Classificação incerta (0.6 < similaridade ≤ 0.8)
- **`desconhecido`**: Não identificado (similaridade ≤ 0.6)

### Passo 5: Validação e Ajustes

Interface permite:
- ✅ Validar classificações automáticas
- ✏️ Editar apelidos manualmente
- 🔍 Filtrar por status, tipo, validado
- 📥 Exportar itens para revisão

### Passo 6: Gestão de Desconhecidos

Itens não identificados são exportados para análise:

```csv
descricao_norm,frequencia,sugestao_tipo,sugestao_grupo
"argamassa especial tipo x",5,revestimento,argamassa
"concreto protendido fck45",2,estrutura,concreto
```

**Ação recomendada:**
1. Analisar padrões nos desconhecidos
2. Adicionar novos apelidos no YAML correspondente
3. Re-processar orçamento

## 4. Arquivos YAML - Estrutura

### Formato Padrão

```yaml
apelido: concreto_fck25
unit: m³
contem:
  - fck 25
  - fck25
  - fck=25
  - 25 mpa
ignorar:
  - bombeado
  - lancado
  - vibrado
```

**Campos:**
- **`apelido`**: Identificador único do item
- **`unit`**: Unidade de medida esperada
- **`contem`**: Lista de palavras-chave que identificam o item
- **`ignorar`**: Palavras irrelevantes para classificação

### Exemplo Completo: `yaml/estrutura/concreto.yaml`

```yaml
- apelido: concreto_fck20
  unit: m³
  contem:
    - fck 20
    - fck20
    - fck=20
    - 20 mpa
  ignorar:
    - bombeado
    - usinado

- apelido: concreto_fck25
  unit: m³
  contem:
    - fck 25
    - fck25
    - fck=25
    - 25 mpa
  ignorar:
    - bombeado
    - usinado

- apelido: concreto_fck30
  unit: m³
  contem:
    - fck 30
    - fck30
    - fck=30
    - 30 mpa
  ignorar:
    - bombeado
    - usinado
```

## 5. Aplicações Práticas

### 5.1 Padronização de Orçamentos

**Problema:** Orçamentos de diferentes fornecedores com nomenclaturas variadas

**Solução:**
```
Fornecedor A: "CONC. FCK=25 USINADO BOMBEADO"
Fornecedor B: "Concreto estrutural 25MPa"
Fornecedor C: "CONCRETO FCK25"

→ Todos classificados como: concreto_fck25
```

**Benefício:** Comparação direta de preços entre fornecedores

### 5.2 Análise de Composição de Custos

```python
# Após classificação, agrupar por tax_tipo
resumo = df.groupby('tax_tipo').agg({
    'custo_total': 'sum',
    'item': 'count'
}).sort_values('custo_total', ascending=False)

# Resultado:
# tax_tipo       custo_total    count
# estrutura      R$ 850.000     45
# fundacao       R$ 320.000     12
# revestimento   R$ 280.000     68
# ...
```

### 5.3 Benchmarking de Custos

```python
# Comparar custo/m² por apelido entre obras
benchmark = df.groupby('apelido_final').agg({
    'preco_unitario': ['mean', 'std', 'min', 'max']
})

# Identificar outliers (preços fora da faixa típica)
outliers = df[
    (df['preco_unitario'] > benchmark['mean'] + 2*benchmark['std']) |
    (df['preco_unitario'] < benchmark['mean'] - 2*benchmark['std'])
]
```

### 5.4 Curva ABC de Custos

```python
# Classificar itens por impacto no custo total
df_sorted = df.sort_values('custo_total', ascending=False)
df_sorted['custo_acumulado_%'] = (
    df_sorted['custo_total'].cumsum() / df_sorted['custo_total'].sum() * 100
)

# Classificação ABC
df_sorted['classe_abc'] = pd.cut(
    df_sorted['custo_acumulado_%'],
    bins=[0, 80, 95, 100],
    labels=['A', 'B', 'C']
)

# Classe A: 80% do custo (focar negociação)
# Classe B: 15% do custo (monitorar)
# Classe C: 5% do custo (controle simplificado)
```

## 6. Boas Práticas

### 6.1 Preparação de Planilhas

✅ **Fazer:**
- Usar colunas com nomes claros e consistentes
- Incluir unidades de medida
- Manter descrições detalhadas (não apenas códigos)
- Remover linhas de totais/subtotais

❌ **Evitar:**
- Células mescladas
- Fórmulas complexas
- Múltiplos cabeçalhos
- Formatação excessiva

### 6.2 Validação de Resultados

**Checklist pós-classificação:**
- [ ] Taxa de desconhecidos < 10%
- [ ] Taxa de "revisar" < 20%
- [ ] Apelidos fazem sentido técnico
- [ ] Unidades estão corretas
- [ ] Custos totais conferem com original

### 6.3 Manutenção da Taxonomia

**Quando adicionar novos apelidos:**
1. Item aparece frequentemente como desconhecido
2. Item tem características técnicas distintas (ex: concreto protendido)
3. Item requer tratamento diferenciado em análises

**Onde adicionar:**
```
yaml/
  ├── estrutura/
  │   ├── concreto.yaml      ← Adicionar aqui variações de concreto
  │   ├── aco.yaml           ← Adicionar aqui variações de aço
  │   └── forma.yaml
  ├── fundacao/
  │   ├── estaca.yaml        ← Adicionar aqui tipos de estacas
  │   └── bloco.yaml
  └── ...
```

## 7. Integração com Outras Ferramentas

### 7.1 Export para Análise

```python
# Após validação, exportar para análise detalhada
df_validado = pd.read_csv('data/output/validados/orcamento_validado.csv')

# Análise de produtividade (RUP)
df_validado['rup_hh_unidade'] = df_validado['mao_obra_hh'] / df_validado['quantidade']

# Análise de BDI
df_validado['preco_com_bdi'] = df_validado['custo_direto'] * 1.28

# Export para Power BI / Excel
df_validado.to_excel('analise_completa.xlsx', index=False)
```

### 7.2 Integração com ERP

```python
# Mapear apelidos para códigos do ERP
mapeamento_erp = {
    'concreto_fck25': 'MAT-001-025',
    'aco_ca50': 'MAT-002-050',
    # ...
}

df_validado['codigo_erp'] = df_validado['apelido_final'].map(mapeamento_erp)
```

## 8. Troubleshooting

### Problema: Taxa alta de desconhecidos (>20%)

**Causas:**
- Descrições muito genéricas ou códigos sem texto
- Nomenclatura regional/específica não coberta
- Itens de obra especial (industrial, infraestrutura)

**Solução:**
1. Exportar desconhecidos
2. Analisar padrões
3. Adicionar keywords nos YAMLs
4. Re-processar

### Problema: Classificações incorretas

**Causas:**
- Keywords ambíguas (ex: "forma" pode ser fôrma ou formato)
- Falta de context (ex: "tubo" sem especificar material)

**Solução:**
1. Refinar keywords no YAML
2. Adicionar palavras em `ignorar`
3. Usar validação manual para casos ambíguos

## 9. Outputs Esperados

Ao usar ObraTaxonomia, o engenheiro deve obter:

1. **Orçamento Classificado**
   - Todos os itens com tax_tipo, tax_grupo, apelido
   - Status de validação
   - Flags de qualidade

2. **Relatório de Desconhecidos**
   - Itens não identificados
   - Frequência de ocorrência
   - Sugestões de classificação

3. **Análise de Custos**
   - Distribuição por tipo/grupo
   - Curva ABC
   - Comparativos

## Referências

- **Documentação ObraTaxonomia**: `readme/` (arquitetura, update, taxonomia)
- **Scripts Backend**: `scripts/` (builder, classify, unknowns)
- **Interface Streamlit**: `app/pages/` (fluxo completo)
