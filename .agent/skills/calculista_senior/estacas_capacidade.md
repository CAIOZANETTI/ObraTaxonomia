---
skill_name: "Capacidade de Carga de Estacas"
agent: calculista_senior
category: "Fundações"
difficulty: expert
version: 1.0.0
---

# Skill: Capacidade de Carga de Estacas

## Objetivo

Fornecer metodologia completa para cálculo de capacidade de carga de estacas (fundações profundas) utilizando métodos semi-empíricos baseados em ensaios SPT e CPT, conforme NBR 6122:2019.

## Fundamentos Teóricos

### 1. Tipos de Estacas

#### 1.1 Estacas Moldadas In Loco

**Estaca Escavada (Broca/Trado):**
```
Diâmetros: 20, 25, 30, 35, 40 cm
Profundidade: até 25m
Execução: Trado manual ou mecânico
Concreto: fck ≥ 20 MPa
```

**Estaca Hélice Contínua (CFA):**
```
Diâmetros: 40, 50, 60, 70, 80, 100 cm
Profundidade: até 32m
Execução: Trado helicoidal contínuo
Concreto: fck ≥ 25 MPa, slump 20-24cm
```

**Estaca Strauss:**
```
Diâmetros: 25, 32, 38, 42 cm
Profundidade: até 20m
Execução: Piteira + soquete
Concreto: fck ≥ 15 MPa
```

**Estaca Raiz (Microestaca):**
```
Diâmetros: 10, 15, 20, 25, 31 cm
Profundidade: até 50m
Execução: Perfuração rotativa + injeção
Concreto: fck ≥ 25 MPa
```

#### 1.2 Estacas Pré-Moldadas

**Estaca de Concreto Cravada:**
```
Seções: Quadrada (20x20, 25x25, 30x30, 35x35 cm)
        Circular (φ 26, 33, 38, 42 cm)
Comprimento: 6 a 12m por segmento
Concreto: fck ≥ 35 MPa
Armadura: CA-50, taxa ≥ 0.5%
```

**Estaca Metálica:**
```
Perfis: I, H, Tubular
Comprimento: Variável (emendas soldadas)
Aço: ASTM A36, A572
Proteção: Pintura, galvanização
```

### 2. Métodos Semi-Empíricos (SPT)

#### 2.1 Método Aoki-Velloso (1975)

**Capacidade de Ponta:**
```
Q_p = (q_p × A_p) / F1

q_p = K × N_p

Onde:
Q_p = capacidade de ponta (kN)
q_p = resistência unitária de ponta (kPa)
A_p = área da ponta da estaca (m²)
K = coeficiente que depende do tipo de solo
N_p = SPT médio na ponta (média de 1D acima e 1D abaixo)
F1 = fator de correção do tipo de estaca
```

**Capacidade Lateral:**
```
Q_l = (Σ q_l × A_l) / F2

q_l = α × N_l

Onde:
Q_l = capacidade lateral (kN)
q_l = resistência unitária lateral (kPa)
A_l = área lateral da camada (m²)
α = coeficiente que depende do tipo de solo
N_l = SPT médio da camada
F2 = fator de correção do tipo de estaca
```

**Tabela de Coeficientes K e α:**

| Tipo de Solo | K (kPa) | α (kPa) |
|--------------|---------|---------|
| Areia | 1000 | 20 |
| Areia siltosa | 800 | 24 |
| Areia silto-argilosa | 700 | 20 |
| Areia argilosa | 600 | 24 |
| Areia argilo-siltosa | 500 | 20 |
| Silte | 400 | 30 |
| Silte arenoso | 550 | 24 |
| Silte argiloso | 450 | 28 |
| Argila | 200 | 60 |
| Argila arenosa | 350 | 24 |
| Argila siltosa | 250 | 30 |

**Fatores F1 e F2:**

| Tipo de Estaca | F1 | F2 |
|----------------|----|----|
| Franki | 2.5 | 5.0 |
| Metálica | 1.75 | 3.5 |
| Pré-moldada (cravada) | 2.5 | 5.0 |
| Escavada (bentonita) | 3.0 | 6.0 |
| Hélice contínua | 3.0 | 6.0 |
| Raiz | 2.0 | 4.0 |

**Código Python:**

```python
def aoki_velloso(
    diametro_cm: float,
    profundidade_m: float,
    spt_perfil: list,
    tipo_solo_perfil: list,
    tipo_estaca: str = 'helice_continua'
) -> dict:
    """
    Calcula capacidade de carga pelo método Aoki-Velloso.
    
    Args:
        diametro_cm: Diâmetro da estaca (cm)
        profundidade_m: Profundidade da ponta (m)
        spt_perfil: Lista de valores SPT por metro [N1, N2, ..., Nn]
        tipo_solo_perfil: Lista de tipos de solo ['areia', 'argila', ...]
        tipo_estaca: Tipo de estaca
    
    Returns:
        dict com Q_p, Q_l, Q_total e fator de segurança
    
    Referência: Aoki & Velloso (1975), NBR 6122:2019
    """
    import math
    
    # Coeficientes K e α por tipo de solo
    coef_solo = {
        'areia': {'K': 1000, 'alpha': 20},
        'areia_siltosa': {'K': 800, 'alpha': 24},
        'areia_argilo_siltosa': {'K': 500, 'alpha': 20},
        'silte': {'K': 400, 'alpha': 30},
        'silte_arenoso': {'K': 550, 'alpha': 24},
        'argila': {'K': 200, 'alpha': 60},
        'argila_siltosa': {'K': 250, 'alpha': 30}
    }
    
    # Fatores F1 e F2 por tipo de estaca
    fatores_estaca = {
        'franki': {'F1': 2.5, 'F2': 5.0},
        'metalica': {'F1': 1.75, 'F2': 3.5},
        'pre_moldada': {'F1': 2.5, 'F2': 5.0},
        'escavada': {'F1': 3.0, 'F2': 6.0},
        'helice_continua': {'F1': 3.0, 'F2': 6.0},
        'raiz': {'F1': 2.0, 'F2': 4.0},
        'strauss': {'F1': 4.0, 'F2': 8.0}
    }
    
    F1 = fatores_estaca[tipo_estaca]['F1']
    F2 = fatores_estaca[tipo_estaca]['F2']
    
    # Geometria
    D = diametro_cm / 100  # m
    A_p = math.pi * (D/2)**2  # m²
    perimetro = math.pi * D  # m
    
    # Capacidade de ponta
    # N_p = média de 1D acima e 1D abaixo da ponta
    idx_ponta = int(profundidade_m) - 1
    D_int = int(D) if D >= 1 else 1
    
    inicio = max(0, idx_ponta - D_int)
    fim = min(len(spt_perfil), idx_ponta + D_int + 1)
    N_p = sum(spt_perfil[inicio:fim]) / len(spt_perfil[inicio:fim])
    
    tipo_solo_ponta = tipo_solo_perfil[idx_ponta]
    K = coef_solo[tipo_solo_ponta]['K']
    
    q_p = K * N_p  # kPa
    Q_p = (q_p * A_p) / F1  # kN
    
    # Capacidade lateral
    Q_l_total = 0
    detalhes_lateral = []
    
    for i in range(int(profundidade_m)):
        if i >= len(spt_perfil):
            break
            
        N_l = spt_perfil[i]
        tipo_solo = tipo_solo_perfil[i]
        alpha = coef_solo[tipo_solo]['alpha']
        
        q_l = alpha * N_l  # kPa
        A_l = perimetro * 1.0  # m² (1m de altura)
        Q_l_camada = (q_l * A_l) / F2  # kN
        
        Q_l_total += Q_l_camada
        
        detalhes_lateral.append({
            'profundidade_m': i + 1,
            'SPT': N_l,
            'tipo_solo': tipo_solo,
            'q_l_kPa': round(q_l, 1),
            'Q_l_kN': round(Q_l_camada, 2)
        })
    
    # Capacidade total
    Q_total = Q_p + Q_l_total
    
    # Carga admissível (FS = 2.0)
    Q_adm = Q_total / 2.0
    
    return {
        'diametro_cm': diametro_cm,
        'profundidade_m': profundidade_m,
        'tipo_estaca': tipo_estaca,
        'N_p': round(N_p, 1),
        'Q_ponta_kN': round(Q_p, 2),
        'Q_lateral_kN': round(Q_l_total, 2),
        'Q_total_kN': round(Q_total, 2),
        'Q_admissivel_kN': round(Q_adm, 2),
        'fator_seguranca': 2.0,
        'detalhes_lateral': detalhes_lateral[:5]  # Primeiras 5 camadas
    }

# Exemplo de uso
spt = [3, 4, 5, 8, 12, 15, 18, 22, 25, 28, 30, 32, 35, 38, 40]
solos = ['areia'] * 5 + ['silte_arenoso'] * 5 + ['areia'] * 5

resultado = aoki_velloso(
    diametro_cm=40,
    profundidade_m=12,
    spt_perfil=spt,
    tipo_solo_perfil=solos,
    tipo_estaca='helice_continua'
)

print(f"Capacidade de ponta: {resultado['Q_ponta_kN']:.2f} kN")
print(f"Capacidade lateral: {resultado['Q_lateral_kN']:.2f} kN")
print(f"Capacidade total: {resultado['Q_total_kN']:.2f} kN")
print(f"Carga admissível (FS=2): {resultado['Q_admissivel_kN']:.2f} kN")
```

#### 2.2 Método Décourt-Quaresma (1978/1996)

**Fórmula Geral:**
```
Q_p = q_p × A_p = (α × N_p × K) × A_p

Q_l = Σ (q_l × A_l) = Σ (β × (N_l / 3 + 1)) × A_l

Onde:
α = 1.0 (estacas escavadas)
    1.0 (hélice contínua - versão 1996)
K = 12 t/m² (argilas)
    20 t/m² (siltes argilosos/arenosos)
    40 t/m² (areias)
β = 1.0 (estacas escavadas)
    1.0 (hélice contínua - versão 1996)
```

**Código Python:**

```python
def decourt_quaresma(
    diametro_cm: float,
    profundidade_m: float,
    spt_perfil: list,
    tipo_solo_perfil: list,
    tipo_estaca: str = 'helice_continua'
) -> dict:
    """
    Calcula capacidade de carga pelo método Décourt-Quaresma (1996).
    
    Referência: Décourt & Quaresma (1978, 1996), NBR 6122:2019
    """
    import math
    
    # Coeficientes K por tipo de solo
    K_solo = {
        'argila': 120,  # kPa
        'argila_siltosa': 120,
        'silte': 200,
        'silte_arenoso': 200,
        'areia': 400,
        'areia_siltosa': 300
    }
    
    # Fatores α e β por tipo de estaca
    if tipo_estaca in ['escavada', 'helice_continua', 'strauss']:
        alpha = 1.0
        beta = 1.0
    elif tipo_estaca in ['pre_moldada', 'metalica']:
        alpha = 1.0
        beta = 1.0
    else:
        alpha = 1.0
        beta = 1.0
    
    # Geometria
    D = diametro_cm / 100
    A_p = math.pi * (D/2)**2
    perimetro = math.pi * D
    
    # Capacidade de ponta
    idx_ponta = int(profundidade_m) - 1
    N_p = spt_perfil[idx_ponta]
    tipo_solo_ponta = tipo_solo_perfil[idx_ponta]
    K = K_solo.get(tipo_solo_ponta, 200)
    
    q_p = alpha * N_p * K  # kPa
    Q_p = q_p * A_p  # kN
    
    # Capacidade lateral
    Q_l_total = 0
    for i in range(int(profundidade_m)):
        if i >= len(spt_perfil):
            break
        
        N_l = spt_perfil[i]
        q_l = beta * (N_l / 3 + 1) * 10  # kPa (fator 10 para converter t/m² em kPa)
        A_l = perimetro * 1.0
        Q_l_total += q_l * A_l
    
    Q_total = Q_p + Q_l_total
    Q_adm = Q_total / 2.0
    
    return {
        'metodo': 'Décourt-Quaresma (1996)',
        'Q_ponta_kN': round(Q_p, 2),
        'Q_lateral_kN': round(Q_l_total, 2),
        'Q_total_kN': round(Q_total, 2),
        'Q_admissivel_kN': round(Q_adm, 2)
    }
```

### 3. Prova de Carga

#### 3.1 Interpretação de Prova de Carga Estática

**Critério de Ruptura de Van der Veen:**
```
Curva carga-recalque:
P = P_rup × (1 - e^(-α×ρ))

Onde:
P = carga aplicada
P_rup = carga de ruptura
ρ = recalque
α = coeficiente de forma da curva
```

**Critério NBR 6122:**
```
Carga de ruptura convencional:
- Recalque = 10% do diâmetro (estacas rígidas)
- Recalque = D/30 + 3mm (estacas flexíveis)
```

#### 3.2 Fator de Segurança

**NBR 6122:2019:**
```
Carga admissível estrutural:
Q_adm_estrutural = Q_estrutural / FS_estrutural

FS_estrutural = 1.4 (ELU)

Carga admissível geotécnica:
Q_adm_geo = Q_rup / FS_geo

FS_geo = 2.0 (métodos semi-empíricos)
        = 1.6 (prova de carga)
        = 3.0 (métodos teóricos)
```

### 4. Recalques

#### 4.1 Recalque Elástico (Poulos & Davis)

```
ρ = (Q × I) / (E_s × D)

Onde:
ρ = recalque (m)
Q = carga aplicada (kN)
I = fator de influência (0.5 - 0.85)
E_s = módulo de elasticidade do solo (kPa)
D = diâmetro da estaca (m)

E_s estimado:
E_s ≈ 3 × N × 100 kPa (areias)
E_s ≈ 2 × N × 100 kPa (argilas)
```

## Outputs Esperados

1. **Memorial de Cálculo**
   - Perfil de sondagem SPT
   - Método utilizado (Aoki-Velloso, Décourt-Quaresma)
   - Cálculo de Q_p e Q_l
   - Capacidade total e admissível

2. **Dimensionamento de Armadura**
   - Armadura longitudinal
   - Armadura transversal (estribos)
   - Comprimento de ancoragem

3. **Especificações**
   - Tipo e diâmetro da estaca
   - Profundidade mínima
   - Concreto (fck)
   - Critérios de aceitação

4. **Recomendações**
   - Prova de carga (quantidade, localização)
   - Controle de execução
   - Monitoramento de recalques

## Referências

- **NBR 6122:2019** - Projeto e execução de fundações
- **Aoki, N.; Velloso, D.A. (1975)** - An approximate method to estimate the bearing capacity of piles
- **Décourt, L.; Quaresma, A.R. (1978, 1996)** - Capacidade de carga de estacas a partir de valores SPT
- **Velloso, D.A.; Lopes, F.R.** - Fundações (volumes 1 e 2)
- **Cintra, J.C.A.; Aoki, N.** - Fundações por Estacas: Projeto Geotécnico
