---
skill_name: "Custo Indireto"
agent: engenheiro_planejamento
category: "Orçamentação"
difficulty: intermediate
version: 1.0.0
---

# Skill: Custo Indireto (Administração Local e Canteiro)

## Objetivo

Fornecer metodologia para estimar e controlar custos indiretos de obra, incluindo administração local, instalações provisórias, mobilização/desmobilização e despesas de canteiro.

## Fundamentos Teóricos

### 1. Definição de Custos Indiretos

**Custos Indiretos:**
- Despesas necessárias para execução da obra, mas não incorporadas diretamente ao produto final
- Não podem ser alocados a um serviço específico
- Geralmente expressos como percentual do custo direto ou valor fixo mensal

**Diferença: Custo Indireto vs BDI:**
```
Custo Indireto → Despesas da OBRA (canteiro, engenheiro residente)
BDI → Despesas da EMPRESA (escritório central, lucro)
```

### 2. Componentes dos Custos Indiretos

#### 2.1 Administração Local

**Equipe Técnica:**
- Engenheiro Residente
- Mestre de Obras
- Encarregados
- Técnico de Segurança do Trabalho
- Estagiários

**Equipe Administrativa:**
- Almoxarife
- Apontador/Timekeeper
- Auxiliar Administrativo

**Fórmula de Custo Mensal:**
```
Custo_Admin_Mensal = Σ (Salário_i × Encargos_Sociais × Qtd_i)

Encargos Sociais típicos: 1.80 - 2.20 (180% - 220% sobre salário)
```

#### 2.2 Instalações Provisórias

**Estruturas:**
- Escritório de obra
- Almoxarifado
- Vestiários e sanitários
- Refeitório
- Guarita
- Depósitos

**Custos Incluídos:**
- Locação ou construção
- Mobiliário
- Equipamentos (computadores, impressoras)
- Manutenção

#### 2.3 Mobilização e Desmobilização

**Mobilização:**
- Transporte de equipamentos
- Montagem de gruas/elevadores
- Instalação de canteiro
- Ligações provisórias (água, luz, esgoto)

**Desmobilização:**
- Desmontagem de equipamentos
- Remoção de instalações
- Limpeza final do terreno
- Restauração de acessos

#### 2.4 Consumos e Despesas Mensais

**Utilidades:**
- Energia elétrica
- Água
- Telefone/Internet
- Combustíveis

**Materiais de Consumo:**
- Material de escritório
- EPI (Equipamentos de Proteção Individual)
- Ferramentas manuais
- Material de limpeza

**Serviços:**
- Segurança patrimonial
- Limpeza
- Topografia
- Ensaios tecnológicos

### 3. Métodos de Estimativa

#### Método 1: Percentual sobre Custo Direto

```
Custo Indireto = Custo Direto × Taxa_Indireto

Taxas Típicas:
- Obras pequenas (< R$ 1M): 8% - 12%
- Obras médias (R$ 1M - R$ 10M): 6% - 10%
- Obras grandes (> R$ 10M): 4% - 8%
```

#### Método 2: Custo Mensal × Prazo

```python
def calcular_custo_indireto_mensal(
    prazo_meses: int,
    equipe_tecnica: dict,
    equipe_admin: dict,
    instalacoes_mensais: float,
    consumos_mensais: float,
    mobilizacao: float,
    desmobilizacao: float
) -> dict:
    """
    Calcula custo indireto total pelo método de custo mensal.
    
    Args:
        prazo_meses: Duração da obra em meses
        equipe_tecnica: dict {'cargo': (salario, qtd, encargos)}
        equipe_admin: dict {'cargo': (salario, qtd, encargos)}
        instalacoes_mensais: Custo mensal de instalações (R$)
        consumos_mensais: Custo mensal de consumos (R$)
        mobilizacao: Custo único de mobilização (R$)
        desmobilizacao: Custo único de desmobilização (R$)
    
    Returns:
        dict com custo indireto total e detalhamento
    """
    # Custo mensal de pessoal
    custo_pessoal_mensal = 0
    
    for cargo, (salario, qtd, encargos) in {**equipe_tecnica, **equipe_admin}.items():
        custo_pessoal_mensal += salario * qtd * encargos
    
    # Custo mensal total
    custo_mensal_total = custo_pessoal_mensal + instalacoes_mensais + consumos_mensais
    
    # Custo indireto total
    custo_indireto_total = (custo_mensal_total * prazo_meses) + mobilizacao + desmobilizacao
    
    return {
        'custo_pessoal_mensal_R$': round(custo_pessoal_mensal, 2),
        'custo_mensal_total_R$': round(custo_mensal_total, 2),
        'custo_recorrente_R$': round(custo_mensal_total * prazo_meses, 2),
        'mobilizacao_R$': mobilizacao,
        'desmobilizacao_R$': desmobilizacao,
        'custo_indireto_total_R$': round(custo_indireto_total, 2),
        'custo_indireto_mensal_medio_R$': round(custo_indireto_total / prazo_meses, 2)
    }

# Exemplo de uso
equipe_tec = {
    'Engenheiro Residente': (12000, 1, 2.0),
    'Mestre de Obras': (6000, 2, 1.9),
    'Técnico Segurança': (5000, 1, 1.9)
}

equipe_adm = {
    'Almoxarife': (3500, 1, 1.8),
    'Apontador': (3000, 1, 1.8)
}

resultado = calcular_custo_indireto_mensal(
    prazo_meses=18,
    equipe_tecnica=equipe_tec,
    equipe_admin=equipe_adm,
    instalacoes_mensais=8000,
    consumos_mensais=5000,
    mobilizacao=80000,
    desmobilizacao=40000
)
```

### 4. Planilha de Custo Indireto Detalhada

#### Template de Planilha

```
┌─────────────────────────────────────────────────────────────┐
│ PLANILHA DE CUSTOS INDIRETOS                                │
├─────────────────────────────────────────────────────────────┤
│ 1. ADMINISTRAÇÃO LOCAL                                      │
│    1.1 Equipe Técnica                                       │
│        - Engenheiro Residente (1x) .......... R$ 24.000/mês │
│        - Mestre de Obras (2x) ............... R$ 22.800/mês │
│        - Técnico Segurança (1x) ............. R$  9.500/mês │
│    1.2 Equipe Administrativa                                │
│        - Almoxarife (1x) .................... R$  6.300/mês │
│        - Apontador (1x) ..................... R$  5.400/mês │
│    Subtotal Pessoal: ........................ R$ 68.000/mês │
│                                                              │
│ 2. INSTALAÇÕES PROVISÓRIAS                                  │
│    2.1 Locação/Construção ................... R$  5.000/mês │
│    2.2 Mobiliário e Equipamentos ............ R$  1.500/mês │
│    2.3 Manutenção ........................... R$  1.500/mês │
│    Subtotal Instalações: .................... R$  8.000/mês │
│                                                              │
│ 3. CONSUMOS MENSAIS                                         │
│    3.1 Energia Elétrica ..................... R$  2.000/mês │
│    3.2 Água ................................. R$    800/mês │
│    3.3 Telefone/Internet .................... R$    500/mês │
│    3.4 Material de Escritório ............... R$    300/mês │
│    3.5 EPI .................................. R$  1.000/mês │
│    3.6 Ferramentas Manuais .................. R$    400/mês │
│    Subtotal Consumos: ....................... R$  5.000/mês │
│                                                              │
│ 4. SERVIÇOS MENSAIS                                         │
│    4.1 Segurança Patrimonial ................ R$  3.500/mês │
│    4.2 Limpeza .............................. R$  1.500/mês │
│    4.3 Topografia ........................... R$  2.000/mês │
│    4.4 Ensaios Tecnológicos ................. R$  3.000/mês │
│    Subtotal Serviços: ....................... R$ 10.000/mês │
│                                                              │
│ TOTAL MENSAL: ............................... R$ 91.000/mês │
│                                                              │
│ 5. CUSTOS ÚNICOS                                            │
│    5.1 Mobilização .......................... R$ 80.000     │
│    5.2 Desmobilização ....................... R$ 40.000     │
│    Subtotal Únicos: ......................... R$ 120.000    │
│                                                              │
│ PRAZO DA OBRA: 18 meses                                     │
│                                                              │
│ CUSTO INDIRETO TOTAL:                                       │
│ = (R$ 91.000 × 18) + R$ 120.000 = R$ 1.758.000             │
└─────────────────────────────────────────────────────────────┘
```

### 5. Custos Indiretos por Tipo de Obra

| Tipo de Obra | % sobre Custo Direto | Observações |
|--------------|----------------------|-------------|
| Edificações residenciais | 6% - 10% | Canteiro padrão |
| Edificações comerciais | 8% - 12% | Maior equipe técnica |
| Obras industriais | 10% - 15% | Controles rigorosos, ensaios |
| Infraestrutura (rodovias) | 5% - 8% | Canteiro móvel |
| Reformas | 12% - 18% | Alto custo de logística |

### 6. Controle de Custos Indiretos

#### Indicadores de Desempenho

```python
def calcular_kpis_custo_indireto(
    custo_indireto_realizado: float,
    custo_indireto_orcado: float,
    custo_direto_realizado: float,
    prazo_decorrido_meses: int,
    prazo_total_meses: int
) -> dict:
    """
    Calcula KPIs de controle de custo indireto.
    
    Returns:
        dict com indicadores de desempenho
    """
    # Desvio orçamentário
    desvio_orcamentario = ((custo_indireto_realizado / custo_indireto_orcado) - 1) * 100
    
    # Taxa de custo indireto real
    taxa_indireto_real = (custo_indireto_realizado / custo_direto_realizado) * 100
    
    # Projeção de custo final
    taxa_realizacao = prazo_decorrido_meses / prazo_total_meses
    custo_indireto_projetado = custo_indireto_realizado / taxa_realizacao
    
    return {
        'desvio_orcamentario_%': round(desvio_orcamentario, 2),
        'taxa_indireto_real_%': round(taxa_indireto_real, 2),
        'custo_indireto_projetado_R$': round(custo_indireto_projetado, 2),
        'status': 'OK' if abs(desvio_orcamentario) < 10 else 'ATENÇÃO'
    }
```

### 7. Checklist de Estimativa

Ao estimar custos indiretos:

- [ ] Equipe técnica está dimensionada para o porte da obra?
- [ ] Encargos sociais estão corretos (CLT, horistas)?
- [ ] Instalações provisórias atendem NR-18 (segurança)?
- [ ] Custos de mobilização incluem todos os equipamentos?
- [ ] Consumos mensais foram estimados realisticamente?
- [ ] Serviços terceirizados têm cotações?
- [ ] Prazo da obra está correto para cálculo mensal?
- [ ] Custos únicos (mob/desmob) foram incluídos?

### 8. Otimização de Custos Indiretos

**Estratégias:**
1. **Dimensionamento adequado:** Equipe mínima necessária
2. **Compartilhamento:** Canteiro compartilhado (obras próximas)
3. **Tecnologia:** Automação de controles (reduz pessoal administrativo)
4. **Negociação:** Contratos de longo prazo (energia, segurança)
5. **Planejamento:** Redução de prazo → menos meses de custo fixo

### 9. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Planilha de Custo Indireto Detalhada**
   - Discriminação de todos os itens
   - Custos mensais e únicos
   - Total geral

2. **Memória de Cálculo**
   - Dimensionamento de equipe
   - Justificativa de taxas
   - Comparação com referências

3. **Cronograma de Desembolso**
   - Curva de custo indireto mensal
   - Picos de desembolso (mobilização)

## Referências

- **NBR 12721** - Avaliação de custos unitários
- **NR-18** - Condições de segurança no trabalho na indústria da construção
- **TCPO** - Tabelas de Composições de Preços (Editora PINI)
