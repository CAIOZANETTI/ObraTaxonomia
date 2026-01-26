---
skill_name: "Cálculo de BDI"
agent: engenheiro_planejamento
category: "Orçamentação"
difficulty: advanced
version: 1.0.0
---

# Skill: Cálculo de BDI (Benefícios e Despesas Indiretas)

## Objetivo

Fornecer metodologia rigorosa para cálculo do BDI (Bonificações e Despesas Indiretas), garantindo que todas as despesas não incluídas nos custos diretos sejam adequadamente contempladas no preço de venda da obra.

## Fundamentos Teóricos

### 1. Definição de BDI

**BDI (Benefícios e Despesas Indiretas):**
- Taxa percentual aplicada sobre o custo direto para cobrir despesas indiretas e lucro
- Também chamado de LDI (Lucros e Despesas Indiretas)
- Varia conforme tipo de obra, porte, localização e regime de contratação

**Fórmula Básica:**
```
Preço de Venda = Custo Direto × (1 + BDI/100)

ou

BDI% = [(Preço de Venda - Custo Direto) / Custo Direto] × 100
```

### 2. Componentes do BDI

#### Estrutura Completa

```
BDI = AC + S + R + G + DF + L

Onde:
AC = Administração Central (%)
S  = Seguros e Garantias (%)
R  = Riscos (%)
G  = Despesas Financeiras (%)
DF = Tributos (%)
L  = Lucro (%)
```

#### Fórmula Detalhada (Acórdão TCU 2622/2013)

```
         (1 + AC + S + R + G) × (1 + L)
BDI = [ --------------------------------- - 1 ] × 100
                  (1 - DF)

Onde:
AC = Taxa de Administração Central
S  = Taxa de Seguros
R  = Taxa de Riscos
G  = Taxa de Despesas Financeiras
L  = Taxa de Lucro
DF = Taxa de Tributos (PIS + COFINS + ISS ou ICMS)
```

### 3. Detalhamento dos Componentes

#### 3.1 Administração Central (AC)

**Definição:** Custos da estrutura administrativa da empresa (não alocados diretamente à obra)

**Itens Incluídos:**
- Salários da diretoria e staff administrativo
- Aluguel de escritório central
- Despesas de marketing e comercial
- Sistemas de gestão (ERP, contabilidade)
- Assessorias jurídica, contábil, fiscal

**Faixas Típicas:**
- Pequenas empresas: 3% - 5%
- Médias empresas: 4% - 7%
- Grandes empresas: 5% - 8%

#### 3.2 Seguros e Garantias (S)

**Tipos de Seguros:**
- Seguro de Responsabilidade Civil (RC)
- Seguro de Riscos de Engenharia (All Risks)
- Seguro de Equipamentos
- Garantia de Execução (Performance Bond)
- Garantia de Adiantamento

**Faixas Típicas:**
- Obras privadas: 0.5% - 1.5%
- Obras públicas: 1.0% - 2.5% (garantias obrigatórias)

#### 3.3 Riscos (R)

**Definição:** Margem para cobrir imprevistos não seguráveis

**Riscos Cobertos:**
- Variações climáticas extremas
- Greves e paralisações
- Descobertas arqueológicas
- Interferências não mapeadas
- Variações cambiais (importações)

**Faixas Típicas:**
- Obras de baixa complexidade: 0.5% - 1.5%
- Obras de média complexidade: 1.0% - 3.0%
- Obras de alta complexidade: 2.0% - 5.0%

#### 3.4 Despesas Financeiras (G)

**Definição:** Custo do capital de giro necessário para financiar a obra

**Fórmula:**
```
G = (Taxa de Juros × Prazo Médio de Recebimento) / 12

Exemplo:
Taxa CDI + spread = 12% a.a.
Prazo médio de recebimento = 30 dias
G = (0.12 × 30) / 365 = 0.98% ≈ 1.0%
```

**Faixas Típicas:**
- Obras com pagamento à vista: 0.5% - 1.0%
- Obras com pagamento em 30 dias: 1.0% - 1.5%
- Obras com pagamento em 60 dias: 1.5% - 2.5%

#### 3.5 Tributos (DF)

**Tributos Federais:**
- PIS: 0.65% (regime não cumulativo) ou 1.65% (cumulativo)
- COFINS: 3.00% (regime não cumulativo) ou 7.60% (cumulativo)

**Tributos Municipais/Estaduais:**
- ISS (Imposto Sobre Serviços): 2% - 5% (varia por município)
- ICMS (apenas para fornecimento de materiais): 12% - 18%

**Cálculo Típico (Obras de Construção Civil):**
```
DF = PIS + COFINS + ISS
DF = 0.65% + 3.00% + 5.00% = 8.65%
```

**Importante:** Tributos incidem sobre o **preço de venda**, não sobre o custo direto.

#### 3.6 Lucro (L)

**Definição:** Remuneração do capital investido e risco empresarial

**Faixas Típicas:**
- Obras públicas (licitação competitiva): 6% - 10%
- Obras privadas (negociação direta): 8% - 15%
- Obras de alta complexidade/risco: 10% - 20%

**Fatores que Influenciam:**
- Porte da obra
- Complexidade técnica
- Prazo de execução
- Condições de pagamento
- Concorrência no mercado

### 4. Exemplos de Cálculo

#### Exemplo 1: Obra Pública (Acórdão TCU)

```python
def calcular_bdi_tcu(
    admin_central: float = 0.05,    # 5%
    seguros: float = 0.015,          # 1.5%
    riscos: float = 0.02,            # 2%
    desp_financeiras: float = 0.012, # 1.2%
    lucro: float = 0.08,             # 8%
    tributos: float = 0.0865         # 8.65% (PIS+COFINS+ISS)
) -> dict:
    """
    Calcula BDI conforme metodologia do TCU (Acórdão 2622/2013).
    
    Returns:
        dict com BDI total e componentes
    """
    numerador = (1 + admin_central + seguros + riscos + desp_financeiras) * (1 + lucro)
    denominador = (1 - tributos)
    
    bdi_decimal = (numerador / denominador) - 1
    bdi_percentual = bdi_decimal * 100
    
    return {
        'BDI_%': round(bdi_percentual, 2),
        'Componentes': {
            'Administração Central': f"{admin_central*100:.2f}%",
            'Seguros e Garantias': f"{seguros*100:.2f}%",
            'Riscos': f"{riscos*100:.2f}%",
            'Despesas Financeiras': f"{desp_financeiras*100:.2f}%",
            'Lucro': f"{lucro*100:.2f}%",
            'Tributos': f"{tributos*100:.2f}%"
        },
        'Fórmula': f"BDI = [({numerador:.4f}) / ({denominador:.4f}) - 1] × 100"
    }

# Exemplo de uso
resultado = calcular_bdi_tcu()
print(f"BDI Total: {resultado['BDI_%']}%")
# Resultado típico: ~25-30%
```

#### Exemplo 2: Aplicação no Orçamento

```python
def aplicar_bdi_orcamento(
    custo_direto: float,
    bdi_percentual: float
) -> dict:
    """
    Aplica BDI ao custo direto para obter preço de venda.
    
    Args:
        custo_direto: Custo direto total da obra (R$)
        bdi_percentual: BDI em percentual (ex: 28.5 para 28.5%)
    
    Returns:
        dict com preço de venda e margem
    """
    bdi_decimal = bdi_percentual / 100
    preco_venda = custo_direto * (1 + bdi_decimal)
    margem_reais = preco_venda - custo_direto
    
    return {
        'custo_direto_R$': f"R$ {custo_direto:,.2f}",
        'BDI_%': bdi_percentual,
        'margem_BDI_R$': f"R$ {margem_reais:,.2f}",
        'preco_venda_R$': f"R$ {preco_venda:,.2f}"
    }

# Exemplo: Obra de R$ 1.000.000,00 com BDI de 28%
resultado = aplicar_bdi_orcamento(1000000, 28.0)
# Preço de Venda: R$ 1.280.000,00
```

### 5. BDI por Tipo de Obra

| Tipo de Obra | BDI Típico | Observações |
|--------------|------------|-------------|
| Edificações residenciais | 25% - 30% | Obras privadas, menor complexidade |
| Edificações comerciais | 28% - 35% | Maior complexidade, prazos apertados |
| Obras públicas (licitação) | 20% - 28% | Competição acirrada, margens menores |
| Infraestrutura (rodovias) | 22% - 30% | Riscos geotécnicos, clima |
| Obras industriais | 30% - 40% | Alta complexidade, tecnologia |
| Reformas e manutenção | 35% - 50% | Alto risco, baixa previsibilidade |

### 6. Análise de Sensibilidade

```python
def analise_sensibilidade_bdi(
    custo_direto: float,
    bdi_base: float,
    variacao_percentual: float = 10
) -> pd.DataFrame:
    """
    Analisa impacto de variações no BDI sobre o preço final.
    
    Args:
        custo_direto: Custo direto da obra (R$)
        bdi_base: BDI base em percentual
        variacao_percentual: Variação a testar (±%)
    
    Returns:
        DataFrame com cenários
    """
    import pandas as pd
    
    cenarios = []
    
    for variacao in [-variacao_percentual, 0, variacao_percentual]:
        bdi_cenario = bdi_base * (1 + variacao/100)
        preco_venda = custo_direto * (1 + bdi_cenario/100)
        
        cenarios.append({
            'Cenário': f"BDI {'+' if variacao > 0 else ''}{variacao}%",
            'BDI (%)': round(bdi_cenario, 2),
            'Preço de Venda (R$)': round(preco_venda, 2),
            'Variação no Preço (%)': round((preco_venda / (custo_direto * (1 + bdi_base/100)) - 1) * 100, 2)
        })
    
    return pd.DataFrame(cenarios)
```

### 7. Checklist de Validação

Ao calcular BDI, verificar:

- [ ] Todos os componentes (AC, S, R, G, DF, L) foram considerados?
- [ ] Fórmula do TCU foi aplicada corretamente (tributos no denominador)?
- [ ] Tributos estão corretos para o regime tributário da empresa?
- [ ] Taxa de lucro está compatível com o mercado e tipo de obra?
- [ ] Despesas financeiras refletem prazo real de recebimento?
- [ ] BDI total está dentro da faixa típica para o tipo de obra?
- [ ] Há justificativa técnica para BDI fora da faixa usual?

### 8. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Planilha de Cálculo de BDI**
   - Detalhamento de todos os componentes
   - Fórmula aplicada
   - BDI total resultante

2. **Justificativa Técnica**
   - Explicação de cada taxa adotada
   - Comparação com referências de mercado
   - Análise de sensibilidade

3. **Aplicação no Orçamento**
   - Custo direto total
   - BDI aplicado
   - Preço de venda final

## Referências

- **Acórdão TCU 2622/2013** - Metodologia de cálculo de BDI para obras públicas
- **Lei 8.666/1993** - Licitações e contratos administrativos
- **Decreto 7.983/2013** - Regras de BDI para obras públicas federais
- **TCPO - Tabelas de Composições de Preços** (Editora PINI)
