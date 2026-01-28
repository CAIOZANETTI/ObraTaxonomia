---
skill_name: "Análise de Pareto (Curva ABC)"
agent: engenheiro_custo
category: "Orçamentação e Custos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Análise de Pareto (Curva ABC)

## Objetivo

Aplicar o princípio de Pareto (regra 80/20) para identificar itens críticos de custo em orçamentos de obras, permitindo foco em otimização e controle dos itens mais relevantes.

## Fundamentos

### 1. Princípio de Pareto

**Regra 80/20:**
```
Em orçamentos de construção:
- 20% dos itens representam 80% do custo total
- 80% dos itens representam 20% do custo total

Aplicação:
- Focar esforços de cotação nos itens A
- Controlar rigorosamente execução dos itens A
- Simplificar gestão dos itens C
```

### 2. Classificação ABC

**Critérios:**
```
Classe A: Itens que somam até 80% do valor acumulado
Classe B: Itens que somam de 80% a 95% do valor acumulado
Classe C: Itens que somam de 95% a 100% do valor acumulado

Características:
Classe A: ~20% dos itens, ~80% do valor → CRÍTICOS
Classe B: ~30% dos itens, ~15% do valor → IMPORTANTES
Classe C: ~50% dos itens, ~5% do valor → TRIVIAIS
```

### 3. Implementação em Python

```python
import pandas as pd
import matplotlib.pyplot as plt

def analise_pareto_orcamento(
    planilha: pd.DataFrame,
    coluna_descricao: str = 'descricao',
    coluna_valor: str = 'preco_total'
) -> dict:
    """
    Realiza análise de Pareto (Curva ABC) em planilha orçamentária.
    
    Args:
        planilha: DataFrame com itens do orçamento
        coluna_descricao: Nome da coluna com descrição dos itens
        coluna_valor: Nome da coluna com valor total dos itens
    
    Returns:
        dict com classificação ABC e estatísticas
    """
    # Ordenar por valor decrescente
    df = planilha.copy()
    df = df.sort_values(by=coluna_valor, ascending=False).reset_index(drop=True)
    
    # Calcular valor acumulado e percentual acumulado
    df['valor_acumulado'] = df[coluna_valor].cumsum()
    df['percentual_acumulado'] = (df['valor_acumulado'] / df[coluna_valor].sum()) * 100
    df['percentual_individual'] = (df[coluna_valor] / df[coluna_valor].sum()) * 100
    
    # Classificar ABC
    def classificar_abc(pct_acum):
        if pct_acum <= 80:
            return 'A'
        elif pct_acum <= 95:
            return 'B'
        else:
            return 'C'
    
    df['classe_abc'] = df['percentual_acumulado'].apply(classificar_abc)
    
    # Estatísticas por classe
    stats = df.groupby('classe_abc').agg({
        coluna_descricao: 'count',
        coluna_valor: 'sum'
    }).rename(columns={
        coluna_descricao: 'quantidade_itens',
        coluna_valor: 'valor_total'
    })
    
    total_itens = len(df)
    total_valor = df[coluna_valor].sum()
    
    stats['percentual_itens'] = (stats['quantidade_itens'] / total_itens) * 100
    stats['percentual_valor'] = (stats['valor_total'] / total_valor) * 100
    
    return {
        'planilha_classificada': df,
        'estatisticas': stats,
        'total_itens': total_itens,
        'total_valor': total_valor
    }

def gerar_grafico_pareto(resultado: dict, salvar_como: str = None):
    """
    Gera gráfico de Pareto (Curva ABC).
    
    Args:
        resultado: Resultado da função analise_pareto_orcamento
        salvar_como: Caminho para salvar o gráfico (opcional)
    """
    df = resultado['planilha_classificada']
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Gráfico de barras (valores individuais)
    ax1.bar(range(len(df)), df['percentual_individual'], 
            color=['red' if c == 'A' else 'yellow' if c == 'B' else 'green' 
                   for c in df['classe_abc']], alpha=0.7)
    ax1.set_xlabel('Itens do Orçamento')
    ax1.set_ylabel('Percentual Individual (%)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    
    # Linha de percentual acumulado
    ax2 = ax1.twinx()
    ax2.plot(range(len(df)), df['percentual_acumulado'], 
             color='blue', marker='o', linewidth=2, markersize=3)
    ax2.set_ylabel('Percentual Acumulado (%)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.axhline(y=80, color='red', linestyle='--', label='80%')
    ax2.axhline(y=95, color='orange', linestyle='--', label='95%')
    ax2.legend(loc='lower right')
    
    plt.title('Análise de Pareto (Curva ABC) - Orçamento de Obra')
    plt.tight_layout()
    
    if salvar_como:
        plt.savefig(salvar_como, dpi=300, bbox_inches='tight')
    
    plt.show()

# Exemplo de uso
import numpy as np

# Criar planilha exemplo
np.random.seed(42)
n_itens = 100

planilha_exemplo = pd.DataFrame({
    'codigo': [f'ITEM-{i:03d}' for i in range(1, n_itens + 1)],
    'descricao': [f'Serviço {i}' for i in range(1, n_itens + 1)],
    'unidade': np.random.choice(['m³', 'm²', 'kg', 'un'], n_itens),
    'quantidade': np.random.uniform(10, 1000, n_itens),
    'preco_unitario': np.random.uniform(10, 500, n_itens)
})

planilha_exemplo['preco_total'] = (planilha_exemplo['quantidade'] * 
                                     planilha_exemplo['preco_unitario'])

# Análise de Pareto
resultado = analise_pareto_orcamento(planilha_exemplo)

# Exibir estatísticas
print("Estatísticas por Classe ABC:")
print(resultado['estatisticas'])

# Exibir top 10 itens (Classe A)
print("\nTop 10 Itens Mais Caros (Classe A):")
print(resultado['planilha_classificada'].head(10)[
    ['codigo', 'descricao', 'preco_total', 'percentual_acumulado', 'classe_abc']
])

# Gerar gráfico
gerar_grafico_pareto(resultado, salvar_como='curva_abc.png')
```

### 4. Aplicações Práticas

#### 4.1 Cotação de Preços

**Estratégia:**
```
Classe A (20% dos itens, 80% do valor):
- Cotação com 5+ fornecedores
- Visita técnica aos fornecedores
- Negociação de condições especiais
- Análise detalhada de especificações

Classe B (30% dos itens, 15% do valor):
- Cotação com 3 fornecedores
- Negociação padrão
- Verificação de especificações

Classe C (50% dos itens, 5% do valor):
- Cotação com 1-2 fornecedores
- Preços tabelados
- Especificações genéricas
```

#### 4.2 Controle de Execução

**Monitoramento:**
```python
def definir_estrategia_controle(classe_abc: str) -> dict:
    """
    Define estratégia de controle por classe ABC.
    """
    estrategias = {
        'A': {
            'medicao': 'Semanal',
            'controle_qualidade': 'Rigoroso (100% dos lotes)',
            'controle_estoque': 'Just-in-time',
            'responsavel': 'Engenheiro residente',
            'documentacao': 'Completa (fotos, ensaios, relatórios)'
        },
        'B': {
            'medicao': 'Quinzenal',
            'controle_qualidade': 'Amostral (30% dos lotes)',
            'controle_estoque': 'Estoque mínimo',
            'responsavel': 'Mestre de obras',
            'documentacao': 'Parcial (relatórios mensais)'
        },
        'C': {
            'medicao': 'Mensal',
            'controle_qualidade': 'Visual',
            'controle_estoque': 'Estoque normal',
            'responsavel': 'Almoxarife',
            'documentacao': 'Simplificada'
        }
    }
    
    return estrategias.get(classe_abc, estrategias['C'])
```

### 5. Exemplo Real: Obra de Edificação

**Resultado Típico:**

| Classe | Qtd Itens | % Itens | Valor Total (R$) | % Valor | Principais Itens |
|--------|-----------|---------|------------------|---------|------------------|
| A | 15 | 18% | 1.200.000 | 80% | Estrutura, alvenaria, revestimentos |
| B | 25 | 30% | 225.000 | 15% | Esquadrias, pintura, instalações |
| C | 43 | 52% | 75.000 | 5% | Ferragens, louças, acabamentos |
| **Total** | **83** | **100%** | **1.500.000** | **100%** | - |

**Itens Classe A Típicos:**
1. Concreto estrutural (fck 25-30 MPa)
2. Aço CA-50 (armadura)
3. Alvenaria de vedação
4. Revestimento cerâmico
5. Forma e escoramento

## Outputs Esperados

1. **Planilha Classificada ABC**
   - Itens ordenados por valor
   - Classificação A/B/C
   - Percentuais acumulados

2. **Gráfico de Pareto**
   - Curva ABC visual
   - Identificação clara das classes

3. **Relatório de Recomendações**
   - Estratégias de cotação
   - Plano de controle
   - Oportunidades de otimização

## Referências

- **Vilfredo Pareto** - Princípio 80/20
- **Juran, J.M.** - Quality Control Handbook
- **PMBOK** - Project Management Body of Knowledge
