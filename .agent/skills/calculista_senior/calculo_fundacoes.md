---
skill_name: "Cálculo de Fundações"
agent: calculista_senior
category: "Geotecnia e Fundações"
difficulty: advanced
version: 1.0.0
---

# Skill: Cálculo de Fundações

## Objetivo

Fornecer diretrizes técnicas para seleção, dimensionamento e verificação de fundações rasas e profundas, baseadas em investigação geotécnica (SPT) e normas brasileiras (NBR 6122:2019).

## Fundamentos Teóricos

### 1. Classificação de Fundações

#### Fundações Rasas (Diretas)
- **Definição:** Profundidade de assentamento (D) ≤ 2 × largura da base (B)
- **Tipos:** Sapatas isoladas, corridas, blocos, radier
- **Aplicação:** Solos competentes em profundidades acessíveis

#### Fundações Profundas
- **Definição:** D > 2B ou carga transmitida por atrito lateral e ponta
- **Tipos:** Estacas (pré-moldadas, escavadas, hélice contínua), tubulões
- **Aplicação:** Solos superficiais fracos, cargas elevadas

### 2. Árvore de Decisão (Baseada em N-SPT)

```
┌─────────────────────────────────────┐
│ Investigação Geotécnica (SPT)      │
└──────────────┬──────────────────────┘
               │
               ├─ N-SPT < 5 (Solo Muito Mole/Fofo)
               │  └─> Fundação Profunda OBRIGATÓRIA
               │
               ├─ 5 ≤ N-SPT < 8 (Solo Mole/Fofo)
               │  └─> Avaliar: Fundação Profunda ou Melhoria de Solo
               │
               ├─ 8 ≤ N-SPT < 15 (Solo Medianamente Compacto)
               │  └─> Fundação Rasa POSSÍVEL (verificar recalques)
               │
               └─ N-SPT ≥ 15 (Solo Compacto/Rijo)
                  └─> Fundação Rasa RECOMENDADA
```

**Critérios Adicionais:**
- Presença de nível d'água (NA): Se NA < 1.5m da cota de apoio → considerar fundação profunda
- Cargas > 1000 kN por pilar → preferir fundação profunda
- Recalque diferencial previsto > 20mm → fundação profunda

### 3. Capacidade de Carga - Fundações Rasas

#### Fórmula de Terzaghi (Sapatas Corridas)

```
q_ult = c·N_c + γ·D·N_q + 0.5·γ·B·N_γ

Onde:
q_ult = Capacidade de carga última (kPa)
c     = Coesão do solo (kPa)
γ     = Peso específico do solo (kN/m³)
D     = Profundidade de assentamento (m)
B     = Largura da sapata (m)
N_c, N_q, N_γ = Fatores de capacidade de carga (função do ângulo de atrito φ)
```

**Capacidade de Carga Admissível:**
```
q_adm = q_ult / FS

FS = Fator de Segurança
    = 3.0 (cargas permanentes)
    = 2.0 (cargas acidentais incluídas)
```

#### Verificação de Recalques (NBR 6122:2019)

```python
def verificar_recalque_sapata(carga_kN: float, area_m2: float, modulo_elastico_MPa: float) -> float:
    """
    Estima recalque elástico de sapata rígida em solo homogêneo.
    
    Args:
        carga_kN: Carga vertical total (kN)
        area_m2: Área da base da sapata (m²)
        modulo_elastico_MPa: Módulo de elasticidade do solo (MPa)
    
    Returns:
        Recalque estimado em mm
    
    Limites NBR 6122:
        - Recalque absoluto < 50mm (estruturas convencionais)
        - Recalque diferencial < 20mm
    """
    tensao_kPa = (carga_kN / area_m2)
    B = (area_m2) ** 0.5  # Largura equivalente (sapata quadrada)
    E_kPa = modulo_elastico_MPa * 1000
    
    # Fórmula simplificada (solo homogêneo, sapata rígida)
    recalque_m = (tensao_kPa * B * (1 - 0.3**2)) / E_kPa
    recalque_mm = recalque_m * 1000
    
    return recalque_mm
```

### 4. Capacidade de Carga - Fundações Profundas

#### Método de Aoki-Velloso (1975)

**Fórmula Geral:**
```
Q_ult = Q_ponta + Q_lateral

Q_ponta = (α · N_SPT · K · A_ponta) / F1

Q_lateral = (β · N_SPT · K · U · L) / F2

Onde:
Q_ult    = Capacidade de carga última (kN)
Q_ponta  = Resistência de ponta (kN)
Q_lateral= Resistência por atrito lateral (kN)
N_SPT    = Valor médio do SPT na camada
K        = Coeficiente de tipo de solo (tabela)
α, β     = Coeficientes de tipo de estaca (tabela)
A_ponta  = Área da seção transversal da ponta (m²)
U        = Perímetro da estaca (m)
L        = Comprimento da camada (m)
F1, F2   = Fatores de segurança parciais
```

**Tabela de Coeficientes K (kPa):**

| Tipo de Solo          | K (kPa) |
|-----------------------|---------|
| Areia                 | 1000    |
| Areia siltosa         | 800     |
| Areia silto-argilosa  | 700     |
| Argila arenosa        | 600     |
| Argila                | 500     |
| Silte                 | 400     |

**Tabela de Coeficientes α e β:**

| Tipo de Estaca        | α    | β     |
|-----------------------|------|-------|
| Franki                | 1.75 | 3.50  |
| Metálica              | 1.75 | 3.50  |
| Pré-moldada (concreto)| 1.75 | 3.50  |
| Escavada (bentonita)  | 1.00 | 2.80  |
| Hélice contínua       | 1.00 | 3.00  |
| Raiz                  | 1.00 | 3.50  |

**Fatores de Segurança (NBR 6122:2019):**
```
F1 = 4.0 (resistência de ponta)
F2 = 3.0 (resistência lateral)

Q_adm = Q_ult / FS_global
FS_global = 2.0 (mínimo)
```

#### Exemplo de Cálculo (Pseudo-código)

```python
def calcular_capacidade_estaca_aoki_velloso(
    tipo_estaca: str,
    diametro_m: float,
    comprimento_m: float,
    camadas: list[dict]
) -> dict:
    """
    Calcula capacidade de carga de estaca pelo método Aoki-Velloso.
    
    Args:
        tipo_estaca: 'helice_continua', 'escavada', 'pre_moldada', etc.
        diametro_m: Diâmetro da estaca (m)
        comprimento_m: Comprimento total (m)
        camadas: Lista de dicionários com:
            - 'tipo_solo': str
            - 'N_SPT': float
            - 'espessura_m': float
    
    Returns:
        dict com Q_ponta, Q_lateral, Q_ult, Q_adm
    """
    # Coeficientes
    coef_estaca = {
        'helice_continua': {'alpha': 1.0, 'beta': 3.0},
        'escavada': {'alpha': 1.0, 'beta': 2.8},
        'pre_moldada': {'alpha': 1.75, 'beta': 3.5}
    }
    
    coef_solo_K = {
        'areia': 1000,
        'areia_siltosa': 800,
        'argila': 500,
        'silte': 400
    }
    
    alpha = coef_estaca[tipo_estaca]['alpha']
    beta = coef_estaca[tipo_estaca]['beta']
    
    A_ponta = 3.14159 * (diametro_m / 2) ** 2
    U = 3.14159 * diametro_m
    
    # Resistência de ponta (última camada)
    camada_ponta = camadas[-1]
    K_ponta = coef_solo_K[camada_ponta['tipo_solo']]
    N_ponta = camada_ponta['N_SPT']
    
    Q_ponta = (alpha * N_ponta * K_ponta * A_ponta) / 4.0
    
    # Resistência lateral (todas as camadas)
    Q_lateral = 0
    for camada in camadas:
        K = coef_solo_K[camada['tipo_solo']]
        N = camada['N_SPT']
        L = camada['espessura_m']
        Q_lateral += (beta * N * K * U * L) / 3.0
    
    Q_ult = Q_ponta + Q_lateral
    Q_adm = Q_ult / 2.0
    
    return {
        'Q_ponta_kN': round(Q_ponta, 2),
        'Q_lateral_kN': round(Q_lateral, 2),
        'Q_ult_kN': round(Q_ult, 2),
        'Q_adm_kN': round(Q_adm, 2)
    }
```

#### Método de Décourt-Quaresma (1996)

**Descrição:**
Método semi-empírico brasileiro amplamente utilizado, especialmente adequado para estacas escavadas e hélice contínua. Baseado em correlações com N-SPT.

**Fórmula Geral:**
```
Q_ult = Q_ponta + Q_lateral

Q_ponta = q_p · A_ponta · α
Q_lateral = q_l · U · L · β

Onde:
q_p = C · N_p + 100 (kPa)  [Resistência unitária de ponta]
q_l = (N_l / 3) + 10 (kPa) [Resistência unitária lateral]

N_p = Valor médio do SPT na ponta (média de 1D acima e 1D abaixo da ponta)
N_l = Valor médio do SPT ao longo do fuste
C   = Coeficiente de tipo de solo (tabela)
α   = Coeficiente de tipo de estaca para ponta (tabela)
β   = Coeficiente de tipo de estaca para lateral (tabela)
A_ponta = Área da seção transversal da ponta (m²)
U   = Perímetro da estaca (m)
L   = Comprimento embutido (m)
```

**Tabela de Coeficientes C (kPa):**

| Tipo de Solo          | C (kPa) |
|-----------------------|---------|
| Argilas               | 120     |
| Siltes argilosos      | 200     |
| Siltes arenosos       | 250     |
| Areias                | 400     |

**Tabela de Coeficientes α e β (Décourt-Quaresma 1996):**

| Tipo de Estaca                    | α    | β    |
|-----------------------------------|------|------|
| Escavada (lama bentonítica)       | 0.85 | 0.80 |
| Escavada (revestimento metálico)  | 0.85 | 0.90 |
| Hélice contínua                   | 0.30 | 0.90 |
| Raiz                              | 0.85 | 0.80 |
| Injetada (alta pressão)           | 1.00 | 1.50 |
| Pré-moldada (cravada)             | 1.00 | 1.00 |

**Implementação em Python:**

```python
def calcular_capacidade_estaca_decourt_quaresma(
    tipo_estaca: str,
    diametro_m: float,
    comprimento_m: float,
    N_ponta: float,
    N_lateral_medio: float,
    tipo_solo_ponta: str
) -> dict:
    """
    Calcula capacidade de carga de estaca pelo método Décourt-Quaresma (1996).
    
    Args:
        tipo_estaca: 'helice_continua', 'escavada_lama', 'escavada_revestimento', 
                     'raiz', 'injetada', 'pre_moldada'
        diametro_m: Diâmetro da estaca (m)
        comprimento_m: Comprimento embutido (m)
        N_ponta: SPT médio na ponta (1D acima + 1D abaixo)
        N_lateral_medio: SPT médio ao longo do fuste
        tipo_solo_ponta: 'argila', 'silte_argiloso', 'silte_arenoso', 'areia'
    
    Returns:
        dict com Q_ponta, Q_lateral, Q_ult, Q_adm (kN)
    """
    # Coeficientes α e β
    coef_estaca = {
        'helice_continua': {'alpha': 0.30, 'beta': 0.90},
        'escavada_lama': {'alpha': 0.85, 'beta': 0.80},
        'escavada_revestimento': {'alpha': 0.85, 'beta': 0.90},
        'raiz': {'alpha': 0.85, 'beta': 0.80},
        'injetada': {'alpha': 1.00, 'beta': 1.50},
        'pre_moldada': {'alpha': 1.00, 'beta': 1.00}
    }
    
    # Coeficiente C (kPa)
    coef_C = {
        'argila': 120,
        'silte_argiloso': 200,
        'silte_arenoso': 250,
        'areia': 400
    }
    
    alpha = coef_estaca[tipo_estaca]['alpha']
    beta = coef_estaca[tipo_estaca]['beta']
    C = coef_C[tipo_solo_ponta]
    
    # Geometria
    A_ponta = 3.14159 * (diametro_m / 2) ** 2
    U = 3.14159 * diametro_m
    
    # Resistência unitária de ponta (kPa)
    q_p = C * N_ponta + 100
    
    # Resistência unitária lateral (kPa)
    q_l = (N_lateral_medio / 3) + 10
    
    # Capacidades (kN)
    Q_ponta = (q_p * A_ponta * alpha)
    Q_lateral = (q_l * U * comprimento_m * beta)
    Q_ult = Q_ponta + Q_lateral
    Q_adm = Q_ult / 2.0  # FS = 2.0
    
    return {
        'q_p_kPa': round(q_p, 2),
        'q_l_kPa': round(q_l, 2),
        'Q_ponta_kN': round(Q_ponta, 2),
        'Q_lateral_kN': round(Q_lateral, 2),
        'Q_ult_kN': round(Q_ult, 2),
        'Q_adm_kN': round(Q_adm, 2)
    }
```

#### Método de Teixeira (1996)

**Descrição:**
Método semi-empírico brasileiro desenvolvido especificamente para estacas tipo hélice contínua, baseado em extenso banco de dados de provas de carga.

**Fórmula Geral:**
```
Q_ult = Q_ponta + Q_lateral

Q_ponta = α · N_p · A_ponta
Q_lateral = β · (N_l / 3 + 1) · U · L

Onde:
N_p = Valor médio do SPT na ponta (média de 1D acima e 1D abaixo)
N_l = Valor médio do SPT ao longo do fuste
α   = Coeficiente de ponta (kPa) - função do tipo de solo
β   = Coeficiente lateral (kPa) - função do tipo de solo
A_ponta = Área da seção transversal da ponta (m²)
U   = Perímetro da estaca (m)
L   = Comprimento embutido (m)
```

**Tabela de Coeficientes α (kPa) - Resistência de Ponta:**

| Tipo de Solo          | α (kPa) |
|-----------------------|---------|
| Argilas               | 100     |
| Siltes argilosos      | 115     |
| Siltes arenosos       | 130     |
| Areias                | 200     |

**Tabela de Coeficientes β (kPa) - Resistência Lateral:**

| Tipo de Solo          | β (kPa) |
|-----------------------|---------|
| Argilas               | 5.0     |
| Siltes argilosos      | 5.5     |
| Siltes arenosos       | 6.0     |
| Areias                | 7.0     |

**Observações Importantes:**
- Método calibrado para estacas hélice contínua com D = 25-60 cm
- Aplicável para solos sedimentares brasileiros
- Recomenda-se prova de carga para validação

**Implementação em Python:**

```python
def calcular_capacidade_estaca_teixeira(
    diametro_m: float,
    comprimento_m: float,
    N_ponta: float,
    N_lateral_medio: float,
    tipo_solo_ponta: str,
    tipo_solo_lateral: str
) -> dict:
    """
    Calcula capacidade de carga de estaca hélice contínua pelo método Teixeira (1996).
    
    Args:
        diametro_m: Diâmetro da estaca (m) - recomendado 0.25 a 0.60m
        comprimento_m: Comprimento embutido (m)
        N_ponta: SPT médio na ponta (1D acima + 1D abaixo)
        N_lateral_medio: SPT médio ao longo do fuste
        tipo_solo_ponta: 'argila', 'silte_argiloso', 'silte_arenoso', 'areia'
        tipo_solo_lateral: 'argila', 'silte_argiloso', 'silte_arenoso', 'areia'
    
    Returns:
        dict com Q_ponta, Q_lateral, Q_ult, Q_adm (kN)
    
    Nota: Método específico para estacas hélice contínua
    """
    # Coeficientes α (kPa) - Ponta
    coef_alpha = {
        'argila': 100,
        'silte_argiloso': 115,
        'silte_arenoso': 130,
        'areia': 200
    }
    
    # Coeficientes β (kPa) - Lateral
    coef_beta = {
        'argila': 5.0,
        'silte_argiloso': 5.5,
        'silte_arenoso': 6.0,
        'areia': 7.0
    }
    
    alpha = coef_alpha[tipo_solo_ponta]
    beta = coef_beta[tipo_solo_lateral]
    
    # Geometria
    A_ponta = 3.14159 * (diametro_m / 2) ** 2
    U = 3.14159 * diametro_m
    
    # Capacidades (kN)
    Q_ponta = alpha * N_ponta * A_ponta
    Q_lateral = beta * ((N_lateral_medio / 3) + 1) * U * comprimento_m
    Q_ult = Q_ponta + Q_lateral
    Q_adm = Q_ult / 2.0  # FS = 2.0
    
    return {
        'Q_ponta_kN': round(Q_ponta, 2),
        'Q_lateral_kN': round(Q_lateral, 2),
        'Q_ult_kN': round(Q_ult, 2),
        'Q_adm_kN': round(Q_adm, 2),
        'aplicavel': 0.25 <= diametro_m <= 0.60,
        'aviso': 'Método calibrado para D=25-60cm' if not (0.25 <= diametro_m <= 0.60) else None
    }
```

#### Comparativo de Métodos

| Método            | Melhor Aplicação                          | Vantagens                           | Limitações                        |
|-------------------|-------------------------------------------|-------------------------------------|-----------------------------------|
| **Aoki-Velloso**  | Todos os tipos de estacas                 | Versátil, amplamente validado       | Coeficientes tabelados fixos      |
| **Décourt-Quaresma** | Estacas escavadas e hélice contínua    | Simples, conservador                | Menos preciso para cravadas       |
| **Teixeira**      | Hélice contínua (D=25-60cm)               | Calibrado para HC brasileiras       | Específico para um tipo de estaca |

**Recomendação de Uso:**
1. Calcular por **pelo menos 2 métodos** diferentes
2. Adotar o **valor mais conservador** (menor capacidade)
3. Validar com **prova de carga** (mínimo 1% das estacas, NBR 12131)


### 5. Checklist de Projeto

#### Fundações Rasas
- [ ] SPT até profundidade mínima de 1.5B abaixo da cota de apoio
- [ ] Verificar presença de nível d'água
- [ ] Calcular capacidade de carga (Terzaghi ou Hansen)
- [ ] Verificar recalques (absoluto < 50mm, diferencial < 20mm)
- [ ] Dimensionar armadura (NBR 6118)
- [ ] Detalhar drenagem e impermeabilização

#### Fundações Profundas
- [ ] SPT até atingir camada resistente (N > 25) ou rocha
- [ ] Definir tipo de estaca (método executivo)
- [ ] Calcular capacidade (Aoki-Velloso ou Décourt-Quaresma)
- [ ] Verificar atrito negativo (se aterro recente)
- [ ] Dimensionar bloco de coroamento
- [ ] Especificar prova de carga (mínimo 1% das estacas)

### 6. Referências Normativas

- **NBR 6122:2019** - Projeto e execução de fundações
- **NBR 6484:2001** - Sondagens de simples reconhecimento (SPT)
- **NBR 12131:2006** - Estacas - Prova de carga estática
- **NBR 13208:2007** - Estacas - Ensaio de carregamento dinâmico

### 7. Premissas e Limitações

**Premissas:**
- Solo homogêneo em cada camada
- Nível d'água estável
- Ausência de solos colapsíveis ou expansivos
- Carregamento centrado

**Limitações:**
- Métodos semi-empíricos têm incertezas inerentes
- Prova de carga é OBRIGATÓRIA para obras críticas
- Monitoramento de recalques durante execução

### 8. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Relatório de Seleção de Fundação**
   - Justificativa técnica
   - Comparativo de alternativas
   - Análise custo-benefício

2. **Memória de Cálculo**
   - Dados de entrada (SPT, cargas)
   - Fórmulas aplicadas
   - Resultados com fatores de segurança

3. **Especificações Técnicas**
   - Tipo e dimensões
   - Profundidade de assentamento
   - Controle de execução

4. **Desenhos Esquemáticos**
   - Planta de locação
   - Cortes típicos
   - Detalhes de armação
