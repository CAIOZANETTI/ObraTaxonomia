---
skill_name: "Caminho Crítico (CPM/PERT)"
agent: engenheiro_planejamento
category: "Gestão de Projetos"
difficulty: advanced
version: 1.0.0
---

# Skill: Caminho Crítico - Método CPM/PERT

## Objetivo

Fornecer metodologia rigorosa para aplicação dos métodos CPM (Critical Path Method) e PERT (Program Evaluation and Review Technique) na identificação do caminho crítico, cálculo de folgas e análise de riscos de prazo.

## Fundamentos Teóricos

### 1. Método CPM (Critical Path Method)

**Definição:**
- Técnica de análise de rede que identifica a sequência de atividades com menor folga
- Caminho Crítico = sequência de atividades que determina a duração mínima do projeto
- Qualquer atraso em atividade crítica → atraso no projeto

**Conceitos-Chave:**
```
ES (Early Start): Início mais cedo possível
EF (Early Finish): Término mais cedo possível
LS (Late Start): Início mais tarde permitido
LF (Late Finish): Término mais tarde permitido
TF (Total Float): Folga total = LS - ES = LF - EF
FF (Free Float): Folga livre = ES(sucessora) - EF(atividade)
```

### 2. Algoritmo CPM

#### Passo 1: Forward Pass (Cálculo de Datas Cedo)

```
Para cada atividade (em ordem topológica):
   ES = max(EF de todas as predecessoras)
   EF = ES + Duração

Início do projeto: ES = 0
```

#### Passo 2: Backward Pass (Cálculo de Datas Tarde)

```
Para cada atividade (em ordem reversa):
   LF = min(LS de todas as sucessoras)
   LS = LF - Duração

Final do projeto: LF = EF_máximo
```

#### Passo 3: Cálculo de Folgas

```
Folga Total (TF) = LS - ES = LF - EF
Folga Livre (FF) = ES_sucessora - EF

Atividade Crítica: TF = 0
Caminho Crítico: Sequência de atividades com TF = 0
```

### 3. Implementação Completa em Python

```python
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class AtividadeCPM:
    def __init__(self, id, descricao, duracao, predecessoras=None):
        self.id = id
        self.descricao = descricao
        self.duracao = duracao
        self.predecessoras = predecessoras or []
        
        # Datas cedo
        self.ES = 0
        self.EF = 0
        
        # Datas tarde
        self.LS = 0
        self.LF = 0
        
        # Folgas
        self.TF = 0  # Total Float
        self.FF = 0  # Free Float
        
        self.critica = False

def calcular_cpm(atividades):
    """
    Calcula CPM completo: datas cedo, tarde, folgas e caminho crítico.
    
    Args:
        atividades: Lista de objetos AtividadeCPM
    
    Returns:
        tuple: (atividades atualizadas, duração total, caminho crítico)
    """
    # Criar mapa de atividades
    ativ_map = {a.id: a for a in atividades}
    
    # FORWARD PASS
    for ativ in atividades:
        if not ativ.predecessoras:
            ativ.ES = 0
        else:
            ativ.ES = max(ativ_map[pred].EF for pred in ativ.predecessoras)
        
        ativ.EF = ativ.ES + ativ.duracao
    
    # Duração total do projeto
    duracao_total = max(a.EF for a in atividades)
    
    # BACKWARD PASS
    for ativ in reversed(atividades):
        # Encontrar sucessoras
        sucessoras = [a for a in atividades if ativ.id in a.predecessoras]
        
        if not sucessoras:
            ativ.LF = duracao_total
        else:
            ativ.LF = min(s.LS for s in sucessoras)
        
        ativ.LS = ativ.LF - ativ.duracao
    
    # CÁLCULO DE FOLGAS
    for ativ in atividades:
        ativ.TF = ativ.LS - ativ.ES
        
        # Folga livre
        sucessoras = [a for a in atividades if ativ.id in a.predecessoras]
        if sucessoras:
            ativ.FF = min(s.ES for s in sucessoras) - ativ.EF
        else:
            ativ.FF = ativ.TF
        
        # Identificar atividades críticas
        ativ.critica = (ativ.TF == 0)
    
    # IDENTIFICAR CAMINHO CRÍTICO
    caminho_critico = [a.id for a in atividades if a.critica]
    
    return atividades, duracao_total, caminho_critico

def gerar_relatorio_cpm(atividades, duracao_total, caminho_critico):
    """
    Gera relatório formatado do CPM.
    """
    df = pd.DataFrame([{
        'ID': a.id,
        'Descrição': a.descricao,
        'Duração': a.duracao,
        'ES': a.ES,
        'EF': a.EF,
        'LS': a.LS,
        'LF': a.LF,
        'TF': a.TF,
        'FF': a.FF,
        'Crítica': '★' if a.critica else ''
    } for a in atividades])
    
    print("=" * 100)
    print(f"ANÁLISE CPM - Duração Total: {duracao_total} dias")
    print("=" * 100)
    print(df.to_string(index=False))
    print("\n" + "=" * 100)
    print(f"CAMINHO CRÍTICO: {' → '.join(caminho_critico)}")
    print("=" * 100)
    
    return df

# EXEMPLO DE USO
atividades = [
    AtividadeCPM('A', 'Mobilização', 5, []),
    AtividadeCPM('B', 'Fundações', 30, ['A']),
    AtividadeCPM('C', 'Estrutura Térreo', 15, ['B']),
    AtividadeCPM('D', 'Estrutura 1º Pav', 15, ['C']),
    AtividadeCPM('E', 'Estrutura 2º Pav', 15, ['D']),
    AtividadeCPM('F', 'Alvenaria Térreo', 20, ['C']),
    AtividadeCPM('G', 'Alvenaria 1º Pav', 20, ['D']),
    AtividadeCPM('H', 'Alvenaria 2º Pav', 20, ['E']),
    AtividadeCPM('I', 'Instalações', 45, ['F', 'G', 'H']),
    AtividadeCPM('J', 'Revestimentos', 60, ['I']),
    AtividadeCPM('K', 'Acabamentos', 40, ['J']),
    AtividadeCPM('L', 'Limpeza Final', 5, ['K'])
]

atividades, duracao, caminho = calcular_cpm(atividades)
relatorio = gerar_relatorio_cpm(atividades, duracao, caminho)
```

### 4. Método PERT (Program Evaluation and Review Technique)

**Diferença do CPM:**
- CPM: Durações determinísticas (fixas)
- PERT: Durações probabilísticas (incertas)

#### Estimativa Três Pontos

```
Duração Esperada (te) = (to + 4tm + tp) / 6

Onde:
to = Duração otimista (melhor cenário)
tm = Duração mais provável (cenário realista)
tp = Duração pessimista (pior cenário)

Desvio Padrão (σ) = (tp - to) / 6

Variância (σ²) = [(tp - to) / 6]²
```

#### Análise de Probabilidade

```
Variância do Caminho Crítico = Σ σ²(atividades críticas)

Desvio Padrão do Projeto = √(Variância Total)

Probabilidade de Conclusão:
Z = (T_desejado - T_esperado) / σ_projeto

P(conclusão em T_desejado) = Φ(Z)  [Tabela Normal Padrão]
```

### 5. Implementação PERT

```python
import numpy as np
from scipy.stats import norm

class AtividadePERT(AtividadeCPM):
    def __init__(self, id, descricao, otimista, mais_provavel, pessimista, predecessoras=None):
        self.otimista = otimista
        self.mais_provavel = mais_provavel
        self.pessimista = pessimista
        
        # Calcular duração esperada
        duracao_esperada = (otimista + 4*mais_provavel + pessimista) / 6
        
        # Calcular desvio padrão
        self.desvio_padrao = (pessimista - otimista) / 6
        self.variancia = self.desvio_padrao ** 2
        
        super().__init__(id, descricao, duracao_esperada, predecessoras)

def calcular_probabilidade_conclusao(atividades, caminho_critico, prazo_desejado):
    """
    Calcula probabilidade de conclusão do projeto em prazo desejado.
    
    Args:
        atividades: Lista de AtividadePERT
        caminho_critico: Lista de IDs do caminho crítico
        prazo_desejado: Prazo desejado em dias
    
    Returns:
        dict com análise probabilística
    """
    ativ_map = {a.id: a for a in atividades}
    
    # Duração esperada do projeto
    duracao_esperada = max(a.EF for a in atividades)
    
    # Variância do caminho crítico
    variancia_total = sum(ativ_map[id].variancia for id in caminho_critico)
    desvio_padrao_projeto = np.sqrt(variancia_total)
    
    # Cálculo de Z-score
    z_score = (prazo_desejado - duracao_esperada) / desvio_padrao_projeto
    
    # Probabilidade (distribuição normal)
    probabilidade = norm.cdf(z_score)
    
    return {
        'duracao_esperada_dias': round(duracao_esperada, 2),
        'desvio_padrao_dias': round(desvio_padrao_projeto, 2),
        'prazo_desejado_dias': prazo_desejado,
        'z_score': round(z_score, 2),
        'probabilidade_%': round(probabilidade * 100, 2),
        'interpretacao': interpretar_probabilidade(probabilidade)
    }

def interpretar_probabilidade(prob):
    if prob >= 0.90:
        return "Alta probabilidade de conclusão no prazo"
    elif prob >= 0.70:
        return "Probabilidade moderada de conclusão no prazo"
    elif prob >= 0.50:
        return "Probabilidade baixa de conclusão no prazo"
    else:
        return "Improvável conclusão no prazo - revisar cronograma"
```

### 6. Compressão de Cronograma (Crashing)

**Técnicas:**

1. **Fast Tracking:** Paralelizar atividades sequenciais
   - Risco: Retrabalho
   - Custo: Baixo

2. **Crashing:** Adicionar recursos para reduzir duração
   - Risco: Médio
   - Custo: Alto

```python
def analisar_crashing(atividade, custo_normal, custo_crash, duracao_crash):
    """
    Analisa custo-benefício de compressão de atividade.
    
    Returns:
        dict com análise de crashing
    """
    reducao_maxima = atividade.duracao - duracao_crash
    custo_adicional = custo_crash - custo_normal
    custo_por_dia = custo_adicional / reducao_maxima if reducao_maxima > 0 else float('inf')
    
    return {
        'atividade': atividade.id,
        'reducao_maxima_dias': reducao_maxima,
        'custo_adicional_R$': custo_adicional,
        'custo_por_dia_R$': round(custo_por_dia, 2),
        'recomendacao': 'Priorizar' if atividade.critica and custo_por_dia < 5000 else 'Avaliar'
    }
```

### 7. Checklist de Análise CPM/PERT

Ao aplicar CPM/PERT:

- [ ] Todas as dependências estão corretas?
- [ ] Durações foram estimadas realisticamente?
- [ ] Forward e Backward Pass foram calculados?
- [ ] Folgas (TF e FF) foram determinadas?
- [ ] Caminho crítico foi identificado?
- [ ] Há mais de um caminho crítico? (risco!)
- [ ] Análise PERT foi feita para atividades incertas?
- [ ] Probabilidade de conclusão foi calculada?

### 8. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Tabela CPM Completa**
   - ES, EF, LS, LF para todas as atividades
   - Folgas totais e livres
   - Identificação de atividades críticas

2. **Diagrama de Rede**
   - Caminho crítico destacado
   - Folgas visualizadas

3. **Análise PERT (se aplicável)**
   - Durações esperadas
   - Desvios padrão
   - Probabilidade de conclusão

4. **Recomendações**
   - Atividades a monitorar
   - Oportunidades de compressão
   - Riscos de prazo

## Referências

- **PMI - PMBOK Guide** (Project Management Body of Knowledge)
- **Practice Standard for Scheduling** (PMI, 2019)
- **Critical Path Method (CPM)** - Kelley & Walker, 1959
- **PERT** - US Navy, 1958
