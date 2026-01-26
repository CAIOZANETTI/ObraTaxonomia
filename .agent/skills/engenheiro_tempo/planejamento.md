---
skill_name: "Planejamento de Obra"
agent: engenheiro_planejamento
category: "Gestão de Projetos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Planejamento de Obra (Sequenciamento Lógico)

## Objetivo

Fornecer metodologia para criar sequenciamento lógico de atividades, definir dependências, estimar durações e estabelecer marcos de controle para execução de obras.

## Fundamentos Teóricos

### 1. Tipos de Dependências

#### Relações de Precedência

```
FS (Finish-to-Start): Término → Início
   A ────┐
         └──→ B ────

SS (Start-to-Start): Início → Início
   A ────┐
         └──→ B ────

FF (Finish-to-Finish): Término → Término
   A ────┐
         └──→ B ────

SF (Start-to-Finish): Início → Término [raro]
   A ────┐
         └──→ B ────
```

**Mais Comum:** FS (Finish-to-Start) - 90% dos casos

#### Leads e Lags

```
Lead (Antecipação): Sucessora inicia ANTES do término da predecessora
   A ────────┐
         B ──────── (Lead = -2 dias)

Lag (Espera): Sucessora inicia DEPOIS do término da predecessora
   A ────┐
         └─── (Lag = +3 dias) ──→ B ────
```

### 2. Sequenciamento Típico de Obra

#### Macro-Sequência

```
1. SERVIÇOS PRELIMINARES
   ├─ Mobilização
   ├─ Instalação de Canteiro
   └─ Terraplenagem
        │
        ↓ (FS)
2. FUNDAÇÕES
   ├─ Locação
   ├─ Escavação
   ├─ Estacas
   └─ Blocos de Coroamento
        │
        ↓ (FS)
3. ESTRUTURA
   ├─ Pilares Térreo
   ├─ Vigas e Lajes Térreo
   ├─ Pilares 1º Pav (SS com Vigas Térreo + Lag 7 dias)
   └─ Ciclo repetitivo por pavimento
        │
        ↓ (SS + Lag 30 dias)
4. ALVENARIA
   ├─ Elevação (por pavimento)
   └─ Vergas e Contravergas
        │
        ↓ (SS + Lag 45 dias)
5. INSTALAÇÕES
   ├─ Hidráulica
   ├─ Elétrica
   └─ Especiais
        │
        ↓ (FS)
6. REVESTIMENTOS
   ├─ Chapisco/Emboço
   ├─ Reboco/Gesso
   └─ Impermeabilizações
        │
        ↓ (FS)
7. ACABAMENTOS
   ├─ Pisos
   ├─ Pintura
   ├─ Esquadrias
   └─ Louças e Metais
        │
        ↓ (FS)
8. FINALIZAÇÃO
   ├─ Limpeza
   ├─ Paisagismo
   └─ Desmobilização
```

### 3. Estimativa de Duração

#### Método 1: Produtividade (RUP)

```
Duração = Quantidade / (Produtividade × Equipe × Jornada)

Exemplo: Concretagem de Laje
Quantidade: 120 m³
Produtividade: 15 m³/h (bomba)
Equipe: 1 bomba
Jornada: 8h/dia

Duração = 120 / (15 × 1 × 8) = 1 dia
```

#### Método 2: Estimativa Três Pontos (PERT)

```
Duração Esperada = (Otimista + 4×Mais Provável + Pessimista) / 6

Exemplo: Fundações
Otimista: 20 dias
Mais Provável: 25 dias
Pessimista: 35 dias

Duração = (20 + 4×25 + 35) / 6 = 25.8 dias ≈ 26 dias
```

### 4. Implementação em Python

```python
import pandas as pd
from datetime import datetime, timedelta

class AtividadeObra:
    def __init__(self, codigo, descricao, duracao_dias, predecessoras=None):
        self.codigo = codigo
        self.descricao = descricao
        self.duracao = duracao_dias
        self.predecessoras = predecessoras or []
        self.inicio_cedo = None
        self.termino_cedo = None
        self.inicio_tarde = None
        self.termino_tarde = None
        self.folga_total = None
        self.critica = False

def criar_cronograma_basico():
    """
    Cria cronograma básico de obra residencial.
    """
    atividades = [
        AtividadeObra('A', 'Mobilização', 5, []),
        AtividadeObra('B', 'Fundações', 30, ['A']),
        AtividadeObra('C', 'Estrutura Térreo', 15, ['B']),
        AtividadeObra('D', 'Estrutura 1º Pav', 15, ['C']),
        AtividadeObra('E', 'Estrutura 2º Pav', 15, ['D']),
        AtividadeObra('F', 'Alvenaria Térreo', 20, ['C']),
        AtividadeObra('G', 'Alvenaria 1º Pav', 20, ['D', 'F']),
        AtividadeObra('H', 'Alvenaria 2º Pav', 20, ['E', 'G']),
        AtividadeObra('I', 'Instalações', 45, ['H']),
        AtividadeObra('J', 'Revestimentos', 60, ['I']),
        AtividadeObra('K', 'Acabamentos', 40, ['J']),
        AtividadeObra('L', 'Limpeza Final', 5, ['K'])
    ]
    
    return atividades

def calcular_cronograma(atividades):
    """
    Calcula datas cedo, tarde e folgas (método CPM simplificado).
    """
    # Mapa de atividades
    ativ_map = {a.codigo: a for a in atividades}
    
    # Forward pass (cálculo de datas cedo)
    for ativ in atividades:
        if not ativ.predecessoras:
            ativ.inicio_cedo = 0
        else:
            max_termino = max(ativ_map[pred].termino_cedo for pred in ativ.predecessoras)
            ativ.inicio_cedo = max_termino
        
        ativ.termino_cedo = ativ.inicio_cedo + ativ.duracao
    
    # Duração total do projeto
    duracao_total = max(a.termino_cedo for a in atividades)
    
    # Backward pass (cálculo de datas tarde)
    for ativ in reversed(atividades):
        sucessoras = [a for a in atividades if ativ.codigo in a.predecessoras]
        
        if not sucessoras:
            ativ.termino_tarde = duracao_total
        else:
            min_inicio = min(s.inicio_tarde for s in sucessoras)
            ativ.termino_tarde = min_inicio
        
        ativ.inicio_tarde = ativ.termino_tarde - ativ.duracao
        ativ.folga_total = ativ.inicio_tarde - ativ.inicio_cedo
        ativ.critica = (ativ.folga_total == 0)
    
    return atividades, duracao_total

# Uso
atividades = criar_cronograma_basico()
atividades, prazo_total = calcular_cronograma(atividades)

print(f"Prazo Total: {prazo_total} dias")
print("\nCaminho Crítico:")
for ativ in atividades:
    if ativ.critica:
        print(f"  {ativ.codigo} - {ativ.descricao}")
```

### 5. Marcos de Controle (Milestones)

**Definição:** Eventos importantes com duração zero, usados para controle gerencial

**Marcos Típicos:**
```
M1: Início da Obra (Data: 01/03/2026)
M2: Fundações Concluídas (Data: 15/04/2026)
M3: Estrutura Concluída (Data: 30/06/2026)
M4: Fechamento Concluído (Data: 31/08/2026)
M5: Instalações Concluídas (Data: 30/10/2026)
M6: Entrega da Obra (Data: 31/12/2026)
```

### 6. Linha de Balanço (Line of Balance)

**Aplicação:** Obras repetitivas (edifícios, casas geminadas)

```
Conceito: Manter equipes trabalhando continuamente, pavimento após pavimento

Exemplo: Estrutura de 10 Pavimentos
- Ciclo por pavimento: 15 dias
- Equipes: 2 (trabalham alternadamente)
- Ritmo: 1 pavimento a cada 7.5 dias
- Duração total: 10 × 7.5 = 75 dias (vs 10 × 15 = 150 dias sequencial)
```

### 7. Checklist de Planejamento

Ao criar sequenciamento lógico:

- [ ] Todas as atividades da EAP estão no cronograma?
- [ ] Dependências lógicas estão corretas (FS, SS, FF)?
- [ ] Durações foram estimadas com base em produtividades reais?
- [ ] Recursos (equipes, equipamentos) estão disponíveis?
- [ ] Marcos de controle estão definidos?
- [ ] Caminho crítico foi identificado?
- [ ] Folgas foram calculadas?
- [ ] Cronograma foi validado com equipe de execução?

### 8. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Diagrama de Rede (Network Diagram)**
   - Atividades e dependências
   - Caminho crítico destacado

2. **Gráfico de Gantt**
   - Barras de atividades
   - Marcos de controle
   - Linha de base

3. **Relatório de Análise**
   - Duração total
   - Atividades críticas
   - Folgas disponíveis

## Referências

- **PMI - PMBOK Guide** (Project Management Body of Knowledge)
- **NBR ISO 21500** - Orientações sobre gerenciamento de projetos
- **Practice Standard for Scheduling** (PMI, 2019)
