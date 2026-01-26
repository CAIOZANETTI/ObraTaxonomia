---
skill_name: "Planilha EAP (WBS)"
agent: engenheiro_planejamento
category: "Gestão de Projetos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Planilha EAP - Estrutura Analítica do Projeto (WBS)

## Objetivo

Fornecer diretrizes para criar e gerenciar a Estrutura Analítica do Projeto (EAP/WBS), decompondo o escopo total da obra em pacotes de trabalho gerenciáveis, mensuráveis e controláveis.

## Fundamentos Teóricos

### 1. Definição de EAP/WBS

**EAP (Estrutura Analítica do Projeto)** ou **WBS (Work Breakdown Structure)**:
- Decomposição hierárquica orientada a entregas do trabalho a ser executado
- Organiza e define o escopo total do projeto
- Cada nível descendente representa uma definição mais detalhada do trabalho

**Regra dos 100%:**
- A EAP inclui 100% do trabalho definido pelo escopo do projeto
- Nada fora da EAP faz parte do projeto

### 2. Níveis Hierárquicos Típicos em Obras

```
Nível 0: Projeto (Obra Completa)
│
├─ Nível 1: Fases Principais (Fundações, Estrutura, Acabamento)
│  │
│  ├─ Nível 2: Subsistemas (Superestrutura, Infraestrutura)
│  │  │
│  │  ├─ Nível 3: Elementos (Pilares, Vigas, Lajes)
│  │  │  │
│  │  │  └─ Nível 4: Pacotes de Trabalho (Pilar P1, Pilar P2)
│  │  │     │
│  │  │     └─ Nível 5: Atividades (Forma, Armação, Concretagem)
```

### 3. Estrutura Padrão para Obras Civis

```
1.0 OBRA RESIDENCIAL MULTIFAMILIAR
│
├─ 1.1 SERVIÇOS PRELIMINARES
│  ├─ 1.1.1 Mobilização e Instalações Provisórias
│  ├─ 1.1.2 Terraplenagem e Movimento de Terra
│  └─ 1.1.3 Locação da Obra
│
├─ 1.2 INFRAESTRUTURA
│  ├─ 1.2.1 Fundações Profundas
│  │  ├─ 1.2.1.1 Estacas Hélice Contínua
│  │  └─ 1.2.1.2 Blocos de Coroamento
│  └─ 1.2.2 Contenções
│
├─ 1.3 SUPERESTRUTURA
│  ├─ 1.3.1 Estrutura de Concreto Armado
│  │  ├─ 1.3.1.1 Pilares
│  │  ├─ 1.3.1.2 Vigas
│  │  └─ 1.3.1.3 Lajes
│  └─ 1.3.2 Escadas e Rampas
│
├─ 1.4 ALVENARIA E VEDAÇÕES
│  ├─ 1.4.1 Alvenaria de Blocos Cerâmicos
│  └─ 1.4.2 Divisórias Leves
│
├─ 1.5 INSTALAÇÕES
│  ├─ 1.5.1 Instalações Hidrossanitárias
│  ├─ 1.5.2 Instalações Elétricas
│  ├─ 1.5.3 Instalações de Gás
│  └─ 1.5.4 Instalações Especiais (SPDA, CFTV)
│
├─ 1.6 REVESTIMENTOS
│  ├─ 1.6.1 Revestimentos Internos
│  ├─ 1.6.2 Revestimentos Externos (Fachada)
│  └─ 1.6.3 Impermeabilizações
│
├─ 1.7 ACABAMENTOS
│  ├─ 1.7.1 Pisos e Rodapés
│  ├─ 1.7.2 Pintura
│  ├─ 1.7.3 Esquadrias
│  └─ 1.7.4 Louças e Metais
│
└─ 1.8 SERVIÇOS COMPLEMENTARES
   ├─ 1.8.1 Limpeza Final
   ├─ 1.8.2 Paisagismo
   └─ 1.8.3 Desmobilização
```

### 4. Codificação (Numbering System)

**Sistema Decimal Hierárquico:**
```
1.0       → Projeto
1.1       → Fase
1.1.1     → Subsistema
1.1.1.1   → Elemento
1.1.1.1.1 → Pacote de Trabalho
```

**Exemplo Prático:**
```
1.3.1.1.2 = Pilares do 2º Pavimento
│ │ │ │ │
│ │ │ │ └─ Pavimento específico
│ │ │ └─── Pilares
│ │ └───── Estrutura de Concreto
│ └─────── Superestrutura
└───────── Projeto
```

### 5. Atributos de Cada Pacote de Trabalho

Cada elemento da EAP deve conter:

| Atributo | Descrição | Exemplo |
|----------|-----------|---------|
| **Código WBS** | Identificador único | 1.3.1.1.2 |
| **Descrição** | Nome do pacote | Pilares 2º Pavimento |
| **Responsável** | Equipe/Empresa | Equipe Estrutura |
| **Duração** | Tempo estimado | 5 dias |
| **Custo** | Orçamento alocado | R$ 45.000,00 |
| **Predecessoras** | Dependências | 1.3.1.1.1 (Pilares 1º Pav) |
| **Critério de Aceitação** | Como validar conclusão | Prova de carga, inspeção |

### 6. Implementação em Planilha

#### Template Excel/Google Sheets

```python
import pandas as pd

def criar_eap_template():
    """
    Cria template de EAP em DataFrame pandas.
    """
    eap_data = {
        'Código WBS': [],
        'Nível': [],
        'Descrição': [],
        'Responsável': [],
        'Duração (dias)': [],
        'Custo (R$)': [],
        'Predecessoras': [],
        'Status': [],
        '% Concluído': []
    }
    
    # Exemplo de estrutura
    exemplos = [
        ('1.0', 0, 'OBRA RESIDENCIAL', 'Gerente de Obra', 365, 5000000, '', 'Em andamento', 45),
        ('1.1', 1, 'SERVIÇOS PRELIMINARES', 'Eng. Civil', 30, 150000, '', 'Concluído', 100),
        ('1.1.1', 2, 'Mobilização', 'Mestre de Obras', 5, 25000, '', 'Concluído', 100),
        ('1.2', 1, 'INFRAESTRUTURA', 'Eng. Fundações', 45, 800000, '1.1', 'Concluído', 100),
        ('1.2.1', 2, 'Fundações Profundas', 'Eng. Fundações', 30, 600000, '1.1.1', 'Concluído', 100),
        ('1.3', 1, 'SUPERESTRUTURA', 'Eng. Estruturas', 120, 1800000, '1.2', 'Em andamento', 60),
        ('1.3.1', 2, 'Estrutura de Concreto', 'Eng. Estruturas', 100, 1500000, '1.2.1', 'Em andamento', 60),
        ('1.3.1.1', 3, 'Pilares', 'Equipe Estrutura', 40, 500000, '1.2.1', 'Em andamento', 75),
    ]
    
    for exemplo in exemplos:
        eap_data['Código WBS'].append(exemplo[0])
        eap_data['Nível'].append(exemplo[1])
        eap_data['Descrição'].append(exemplo[2])
        eap_data['Responsável'].append(exemplo[3])
        eap_data['Duração (dias)'].append(exemplo[4])
        eap_data['Custo (R$)'].append(exemplo[5])
        eap_data['Predecessoras'].append(exemplo[6])
        eap_data['Status'].append(exemplo[7])
        eap_data['% Concluído'].append(exemplo[8])
    
    df = pd.DataFrame(eap_data)
    return df

# Uso
eap_df = criar_eap_template()
eap_df.to_excel('EAP_Obra.xlsx', index=False)
```

### 7. Boas Práticas

#### Regra 8/80

- **Pacotes de trabalho** devem ter duração entre **8 e 80 horas** de esforço
- Menor que 8h → muito granular, dificulta controle
- Maior que 80h → muito agregado, perde visibilidade

#### Orientação a Entregas (Deliverable-Oriented)

✅ **Correto:** "Estrutura do 3º Pavimento Concretada"
❌ **Incorreto:** "Trabalhar na Estrutura"

#### Decomposição Adequada

**Critérios para parar a decomposição:**
- Pode-se estimar custo e duração com confiança (±10%)
- Pode-se atribuir responsabilidade clara
- Pode-se definir critério de aceitação objetivo
- Pode-se monitorar progresso semanalmente

### 8. Integração com Outras Ferramentas

#### EAP → Orçamento
```
Cada pacote de trabalho → Composição de custos (CPU)
Soma dos pacotes → Custo total do projeto
```

#### EAP → Cronograma
```
Pacotes de trabalho → Atividades no MS Project/Primavera
Dependências → Sequenciamento lógico (CPM)
```

#### EAP → Controle de Qualidade
```
Pacotes de trabalho → Pontos de inspeção
Critérios de aceitação → Checklists de qualidade
```

### 9. Exemplo Completo: Estrutura de Concreto

```
1.3.1 ESTRUTURA DE CONCRETO ARMADO
│
├─ 1.3.1.1 PILARES
│  ├─ 1.3.1.1.1 Pilares Térreo
│  │  ├─ 1.3.1.1.1.1 Formas
│  │  ├─ 1.3.1.1.1.2 Armação
│  │  └─ 1.3.1.1.1.3 Concretagem
│  ├─ 1.3.1.1.2 Pilares 1º Pavimento
│  └─ 1.3.1.1.3 Pilares 2º Pavimento
│
├─ 1.3.1.2 VIGAS
│  ├─ 1.3.1.2.1 Vigas Térreo
│  └─ 1.3.1.2.2 Vigas 1º Pavimento
│
└─ 1.3.1.3 LAJES
   ├─ 1.3.1.3.1 Lajes Térreo
   └─ 1.3.1.3.2 Lajes 1º Pavimento
```

### 10. Checklist de Validação

Ao criar uma EAP, verificar:

- [ ] Todos os pacotes têm código WBS único?
- [ ] A regra dos 100% está sendo respeitada?
- [ ] Pacotes de trabalho têm duração entre 8-80h?
- [ ] Cada pacote tem responsável definido?
- [ ] Critérios de aceitação estão claros?
- [ ] Dependências estão mapeadas?
- [ ] Custos estão estimados para cada pacote?
- [ ] Estrutura está orientada a entregas (não a atividades)?

### 11. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Planilha EAP Completa**
   - Todos os níveis hierárquicos
   - Codificação WBS consistente
   - Atributos preenchidos

2. **Dicionário da EAP**
   - Descrição detalhada de cada pacote
   - Critérios de aceitação
   - Premissas e restrições

3. **Diagrama Visual (Opcional)**
   - Organograma da EAP
   - Visualização hierárquica

## Referências

- **PMI - PMBOK Guide** (Project Management Body of Knowledge)
- **NBR ISO 21500** - Orientações sobre gerenciamento de projetos
- **Practice Standard for Work Breakdown Structures** (PMI, 2019)
