---
skill_name: "Produtividade de Mão de Obra"
agent: engenheiro_tempo
category: "Planejamento e Produtividade"
difficulty: intermediate
version: 1.0.0
---

# Skill: Produtividade de Mão de Obra

## Objetivo

Calcular e analisar índices de produtividade de mão de obra (RUP - Razão Unitária de Produção) para estimativa de prazos e custos.

## RUP - Razão Unitária de Produção

```
RUP = Horas-homem / Quantidade produzida

Unidade: Hh/m³, Hh/m², Hh/kg, etc.

Exemplo:
10 pedreiros × 8h = 80 Hh
Produção: 100m² de alvenaria
RUP = 80 / 100 = 0.8 Hh/m²
```

## Índices Referenciais

### Estrutura de Concreto

| Atividade | RUP (Hh/m³) | Equipe Típica |
|-----------|-------------|---------------|
| Forma de madeira | 8-12 | 4 carpinteiros |
| Armação | 15-25 | 3 armadores |
| Concretagem | 2-4 | 2 pedreiros + 4 serventes |

### Alvenaria

| Tipo | RUP (Hh/m²) | Produtividade (m²/dia) |
|------|-------------|------------------------|
| Bloco cerâmico | 0.8-1.2 | 6-10 m²/pedreiro |
| Bloco concreto | 1.0-1.5 | 5-8 m²/pedreiro |

### Revestimentos

| Tipo | RUP (Hh/m²) | Produtividade (m²/dia) |
|------|-------------|------------------------|
| Reboco | 0.5-0.8 | 10-16 m²/pedreiro |
| Cerâmica parede | 0.8-1.2 | 6-10 m²/azulejista |
| Cerâmica piso | 0.6-1.0 | 8-13 m²/azulejista |

## Fatores que Afetam Produtividade

1. **Qualificação da equipe** (±20%)
2. **Condições climáticas** (±15%)
3. **Acesso e logística** (±25%)
4. **Complexidade do projeto** (±30%)

## Outputs Esperados

1. **Tabela de RUPs**
2. **Curva de Aprendizado**
3. **Análise de Desvios**

## Referências
- **TCPO** - Tabelas de Composições de Preços
- **SINAPI** - Produtividades de referência
