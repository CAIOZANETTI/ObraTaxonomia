---
skill_name: "Planilha de Custo (EAP/WBS)"
agent: engenheiro_custo
category: "Orçamentação e Custos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Planilha de Custo (EAP/WBS)

## Objetivo

Estruturar planilha orçamentária seguindo metodologia de Estrutura Analítica do Projeto (EAP/WBS), organizando itens hierarquicamente por sistemas construtivos.

## Estrutura Hierárquica

```
1.0 SERVIÇOS PRELIMINARES
  1.1 Mobilização
  1.2 Canteiro de obras
  1.3 Locação da obra

2.0 INFRAESTRUTURA
  2.1 Escavação
  2.2 Fundações
    2.2.1 Estacas
    2.2.2 Blocos de coroamento

3.0 SUPERESTRUTURA
  3.1 Estrutura de concreto
    3.1.1 Pilares
    3.1.2 Vigas
    3.1.3 Lajes
  3.2 Armadura
  3.3 Formas

4.0 ALVENARIA E VEDAÇÕES
  4.1 Alvenaria de vedação
  4.2 Esquadrias

5.0 INSTALAÇÕES
  5.1 Instalações elétricas
  5.2 Instalações hidráulicas
  5.3 Instalações especiais

6.0 ACABAMENTOS
  6.1 Revestimentos
  6.2 Pisos
  6.3 Pintura

7.0 ADMINISTRAÇÃO LOCAL
  7.1 Equipe técnica
  7.2 Equipamentos

8.0 BDI
```

## Formato da Planilha

```
┌──────┬─────────────────┬──────┬──────┬────────┬────────┐
│ Item │ Descrição       │ Und  │ Qtd  │ P.Unit │ Total  │
├──────┼─────────────────┼──────┼──────┼────────┼────────┤
│ 1.0  │ PRELIMINARES    │      │      │        │ 50.000 │
│ 1.1  │ Mobilização     │ vb   │ 1    │ 20.000 │ 20.000 │
│ 1.2  │ Canteiro        │ mês  │ 12   │  2.500 │ 30.000 │
├──────┼─────────────────┼──────┼──────┼────────┼────────┤
│ 2.0  │ INFRAESTRUTURA  │      │      │        │300.000 │
│ 2.1  │ Escavação       │ m³   │ 500  │   45.00│ 22.500 │
│ 2.2  │ Fundações       │      │      │        │277.500 │
│ 2.2.1│ Estacas φ40cm   │ m    │ 600  │  250.00│150.000 │
│ 2.2.2│ Blocos coroam.  │ m³   │ 85   │1.500.00│127.500 │
└──────┴─────────────────┴──────┴──────┴────────┴────────┘
```

## Código Python para Geração

```python
import pandas as pd

def criar_planilha_eap(itens: list) -> pd.DataFrame:
    """
    Cria planilha orçamentária estruturada em EAP.
    
    Args:
        itens: Lista de dicts com estrutura:
               {'codigo': '1.1', 'descricao': '...', 
                'unidade': 'm³', 'quantidade': 100, 
                'preco_unitario': 50.00}
    """
    df = pd.DataFrame(itens)
    df['preco_total'] = df['quantidade'] * df['preco_unitario']
    
    # Calcular totais por nível
    df['nivel'] = df['codigo'].str.count(r'\.')
    
    return df
```

## Outputs Esperados

1. **Planilha Orçamentária Estruturada**
   - Hierarquia clara (EAP)
   - Totalizações por nível
   - Unidades padronizadas

2. **Curva ABC por Capítulo**
3. **Cronograma Físico-Financeiro**

## Referências
- **PMBOK** - WBS/EAP
- **NBR 12721** - Avaliação de custos
