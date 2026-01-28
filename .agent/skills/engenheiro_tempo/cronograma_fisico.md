---
skill_name: "Cronograma Físico"
agent: engenheiro_tempo
category: "Planejamento e Controle"
difficulty: intermediate
version: 1.0.0
---

# Skill: Cronograma Físico

## Objetivo

Elaborar cronogramas físicos de obra utilizando metodologia CPM (Critical Path Method), identificando caminho crítico, folgas e sequenciamento lógico de atividades.

## Metodologia CPM

### 1. Estrutura Analítica (EAP)

```
1. MOBILIZAÇÃO (5 dias)
2. FUNDAÇÕES (30 dias)
   2.1 Escavação (10 dias)
   2.2 Estacas (15 dias)
   2.3 Blocos (10 dias)
3. ESTRUTURA (90 dias)
   3.1 Pilares 1º pav (15 dias)
   3.2 Vigas/lajes 1º pav (20 dias)
   ...
```

### 2. Sequenciamento Lógico

```
Tipos de dependência:
- TI (Término-Início): Mais comum
- II (Início-Início): Atividades simultâneas
- TT (Término-Término): Finalizam juntas
- IT (Início-Término): Raro
```

### 3. Caminho Crítico

```python
def calcular_caminho_critico(atividades: list) -> dict:
    """
    Calcula caminho crítico usando algoritmo CPM.
    
    Args:
        atividades: Lista de dicts com:
                   {'id': 'A', 'duracao': 10, 
                    'predecessoras': ['B', 'C']}
    """
    # Cálculo de PDI (Primeira Data de Início)
    # Cálculo de UDI (Última Data de Início)
    # Folga = UDI - PDI
    # Caminho crítico: atividades com folga = 0
    
    pass  # Implementação completa no código
```

## Gráfico de Gantt

```
Atividade       │ Mês 1 │ Mês 2 │ Mês 3 │ Mês 4 │
────────────────┼───────┼───────┼───────┼───────┤
Mobilização     │███    │       │       │       │
Fundações       │  █████│███    │       │       │
Estrutura       │       │  █████│███████│███    │
Alvenaria       │       │       │    ███│███████│
```

## Outputs Esperados

1. **Cronograma de Gantt**
2. **Lista de Caminho Crítico**
3. **Histograma de Recursos**

## Referências
- **PMBOK** - Gerenciamento de tempo
- **NBR 15575** - Desempenho de edificações
