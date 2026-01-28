---
skill_name: "Proposta Comercial"
agent: engenheiro_custo
category: "Licitações e Propostas"
difficulty: intermediate
version: 1.0.0
---

# Skill: Proposta Comercial

## Objetivo

Fornecer estrutura e metodologia para elaboração de propostas comerciais competitivas e conformes para licitações e contratações privadas.

## Estrutura da Proposta

### 1. Carta de Apresentação

**Elementos:**
- Identificação da empresa
- Referência ao edital/convite
- Declaração de conformidade
- Validade da proposta (60-90 dias)
- Assinatura do representante legal

### 2. Planilha Orçamentária

**Formato:**
```
┌──────┬─────────────────┬──────┬──────┬────────┬────────┐
│ Item │ Descrição       │ Und  │ Qtd  │ P.Unit │ Total  │
├──────┼─────────────────┼──────┼──────┼────────┼────────┤
│ 1.0  │ FUNDAÇÕES       │      │      │        │        │
│ 1.1  │ Escavação       │ m³   │ 500  │ 45.00  │22.500  │
│ 1.2  │ Concreto fck25  │ m³   │ 120  │ 450.00 │54.000  │
└──────┴─────────────────┴──────┴──────┴────────┴────────┘

VALOR TOTAL: R$ 1.500.000,00
```

### 3. Cronograma Físico-Financeiro

**Formato:**
```
Mês 1: 10% - R$ 150.000
Mês 2: 15% - R$ 225.000
Mês 3: 20% - R$ 300.000
...
```

### 4. Composição de BDI

**Detalhamento:**
```python
def calcular_bdi_proposta(
    administracao_central_pct: float = 5.0,
    seguro_garantia_pct: float = 0.5,
    risco_pct: float = 1.5,
    despesas_financeiras_pct: float = 1.2,
    lucro_pct: float = 8.0,
    tributos_pct: float = 5.93  # ISS 5% + PIS/COFINS
) -> dict:
    """
    Calcula BDI conforme Acórdão TCU 2622/2013.
    
    Fórmula:
    BDI = [(1 + AC + S + R + G) / (1 - T)] - 1
    """
    ac = administracao_central_pct / 100
    s = seguro_garantia_pct / 100
    r = risco_pct / 100
    g = despesas_financeiras_pct / 100
    t = tributos_pct / 100
    
    bdi = ((1 + ac + s + r + g) / (1 - t)) - 1
    bdi_pct = bdi * 100
    
    return {
        'administracao_central_pct': administracao_central_pct,
        'seguro_garantia_pct': seguro_garantia_pct,
        'risco_pct': risco_pct,
        'despesas_financeiras_pct': despesas_financeiras_pct,
        'lucro_pct': lucro_pct,
        'tributos_pct': tributos_pct,
        'bdi_total_pct': round(bdi_pct, 2)
    }
```

### 5. Condições Comerciais

**Itens a incluir:**
- Prazo de execução
- Forma de pagamento
- Reajuste (índice, periodicidade)
- Garantias exigidas
- Seguros
- Responsabilidades

## Estratégia de Precificação

### 1. Análise de Competitividade

```python
def analisar_competitividade(
    custo_direto: float,
    bdi_desejado_pct: float,
    preco_referencia: float,
    num_concorrentes_estimado: int = 5
) -> dict:
    """
    Analisa competitividade da proposta.
    """
    preco_desejado = custo_direto * (1 + bdi_desejado_pct / 100)
    desconto_necessario_pct = ((preco_desejado - preco_referencia) / preco_desejado) * 100
    
    # Estimativa de posição competitiva
    if desconto_necessario_pct <= 0:
        posicao = 'Competitiva'
        probabilidade_ganho = 70
    elif desconto_necessario_pct <= 5:
        posicao = 'Moderadamente competitiva'
        probabilidade_ganho = 50
    elif desconto_necessario_pct <= 10:
        posicao = 'Pouco competitiva'
        probabilidade_ganho = 30
    else:
        posicao = 'Não competitiva'
        probabilidade_ganho = 10
    
    # Ajuste por número de concorrentes
    probabilidade_ganho = probabilidade_ganho / (1 + (num_concorrentes_estimado - 3) * 0.1)
    
    return {
        'custo_direto': custo_direto,
        'preco_desejado': round(preco_desejado, 2),
        'preco_referencia': preco_referencia,
        'desconto_necessario_pct': round(desconto_necessario_pct, 2),
        'posicao_competitiva': posicao,
        'probabilidade_ganho_pct': round(probabilidade_ganho, 1),
        'recomendacao': 'Participar' if probabilidade_ganho >= 30 else 'Avaliar'
    }
```

## Outputs Esperados

1. **Proposta Comercial Completa**
   - Carta de apresentação
   - Planilha orçamentária
   - Cronograma
   - Composição de BDI
   - Condições comerciais

2. **Análise de Competitividade**
   - Posicionamento de preço
   - Probabilidade de ganho
   - Recomendação

## Referências

- **Lei 8.666/1993** - Licitações
- **Acórdão TCU 2622/2013** - BDI
