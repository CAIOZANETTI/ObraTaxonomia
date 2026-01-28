---
skill_name: "Estruturas de Concreto Pré-Moldado"
agent: calculista_senior
category: "Cálculo Estrutural"
difficulty: expert
version: 1.0.0
---

# Skill: Estruturas de Concreto Pré-Moldado

## Objetivo

Fornecer metodologia completa para projeto, dimensionamento e detalhamento de estruturas de concreto pré-moldado, incluindo elementos, ligações, transporte e montagem, conforme NBR 9062:2017.

## Fundamentos Teóricos

### 1. Tipos de Elementos Pré-Moldados

#### 1.1 Elementos Lineares

**Vigas:**
```
Tipos:
- Viga I (seção duplo T)
- Viga retangular
- Viga calha (U invertido)
- Viga L (apoio de laje)

Vãos típicos: 6m a 30m
fck mínimo: 30 MPa
```

**Pilares:**
```
Seções:
- Retangular
- Quadrada
- Circular
- H ou I (pilares mistos)

Altura típica: 3m a 12m por segmento
fck mínimo: 35 MPa
```

#### 1.2 Elementos de Superfície

**Lajes Alveolares:**
```
Espessuras: 16, 20, 26, 32, 40 cm
Largura padrão: 1.20m ou 2.40m
Vãos: até 15m (sem protensão)
      até 25m (com protensão)
Sobrecarga: 2 a 10 kN/m²
```

**Painéis de Fachada:**
```
Espessura: 10 a 20 cm
Dimensões: até 3.0m x 6.0m
Peso: 250 a 500 kg/m²
```

### 2. Dimensionamento de Elementos

#### 2.1 Vigas Pré-Moldadas

**Verificação de Momento Fletor:**
```python
def dimensionar_viga_premoldada_I(
    vao_m: float,
    carga_kN_m: float,
    largura_mesa_sup_cm: float,
    largura_alma_cm: float,
    altura_total_cm: float,
    f_ck_MPa: float = 35,
    f_yk_MPa: float = 500
) -> dict:
    """
    Dimensiona viga pré-moldada seção I.
    
    Args:
        vao_m: Vão da viga (m)
        carga_kN_m: Carga distribuída total (kN/m)
        largura_mesa_sup_cm: Largura da mesa superior (cm)
        largura_alma_cm: Largura da alma (cm)
        altura_total_cm: Altura total da viga (cm)
        f_ck_MPa: Resistência do concreto (MPa)
        f_yk_MPa: Resistência do aço (MPa)
    
    Returns:
        dict com armadura necessária e verificações
    
    Referência: NBR 9062:2017
    """
    import numpy as np
    
    # Momento máximo (viga biapoiada)
    M_k = (carga_kN_m * vao_m**2) / 8  # kN.m
    M_d = M_k * 1.4  # kN.m
    
    # Resistências de cálculo
    f_cd = (f_ck_MPa / 1.4) * 1000  # kPa
    f_yd = (f_yk_MPa / 1.15) * 1000  # kPa
    
    # Altura útil (assumindo cobrimento + estribo + metade da barra)
    d_cm = altura_total_cm - 5  # cm (aproximado)
    d = d_cm / 100  # m
    
    # Cálculo simplificado (seção T)
    b_f = largura_mesa_sup_cm / 100  # m
    b_w = largura_alma_cm / 100  # m
    
    # Momento resistente da mesa
    M_f = 0.68 * f_cd * b_f * 0.1 * (d - 0.05)  # Assumindo mesa de 10cm
    
    if M_d <= M_f:
        # LN na mesa - calcular como seção retangular
        K_md = M_d / (b_f * d**2 * f_cd)
        
        if K_md > 0.295:
            return {
                'erro': 'Seção superarmada. Aumentar altura ou usar armadura dupla.',
                'K_md': K_md
            }
        
        K_z = 1.0 - 0.5 * (1 - (1 - 2*K_md)**0.5)
        z = K_z * d
        A_s_m2 = M_d / (f_yd * z)
        A_s_cm2 = A_s_m2 * 10000
        
    else:
        # LN na alma - seção T
        M_alma = M_d - M_f
        A_s_mesa = (0.68 * f_cd * (b_f - b_w) * 0.1) / f_yd
        
        K_md_alma = M_alma / (b_w * d**2 * f_cd)
        K_z_alma = 1.0 - 0.5 * (1 - (1 - 2*K_md_alma)**0.5)
        z_alma = K_z_alma * d
        
        A_s_alma = M_alma / (f_yd * z_alma)
        A_s_cm2 = (A_s_mesa + A_s_alma) * 10000
    
    # Armadura mínima
    rho_min = 0.15 / 100
    A_s_min_cm2 = rho_min * largura_alma_cm * d_cm
    
    A_s_final_cm2 = max(A_s_cm2, A_s_min_cm2)
    
    # Sugestão de bitolas
    bitolas = [12.5, 16, 20, 25, 32]
    areas = [1.23, 2.01, 3.14, 4.91, 8.04]
    
    config = None
    for bitola, area in zip(bitolas, areas):
        n_barras = int(np.ceil(A_s_final_cm2 / area))
        if n_barras <= 8:
            config = {
                'bitola_mm': bitola,
                'n_barras': n_barras,
                'area_cm2': round(n_barras * area, 2)
            }
            break
    
    return {
        'M_d_kNm': round(M_d, 2),
        'A_s_calculado_cm2': round(A_s_cm2, 2),
        'A_s_minimo_cm2': round(A_s_min_cm2, 2),
        'A_s_adotado_cm2': round(A_s_final_cm2, 2),
        'configuracao': config
    }
```

#### 2.2 Lajes Alveolares

**Capacidade de Carga:**
```
Verificação de flexão:
M_Rd = A_p × f_ptd × z + A_s × f_yd × z

Onde:
A_p = área de armadura ativa (protensão)
f_ptd = resistência de cálculo do aço de protensão
A_s = área de armadura passiva
z = braço de alavanca

Verificação de cisalhamento:
V_Rd = V_c + V_sw

V_c = contribuição do concreto
V_sw = contribuição dos estribos (se houver)
```

**Exemplo de Tabela de Capacidade:**

| Espessura (cm) | Vão Máximo (m) | Sobrecarga (kN/m²) | Peso Próprio (kN/m²) |
|----------------|----------------|-------------------|---------------------|
| 16 | 6.0 | 3.0 | 2.8 |
| 20 | 8.0 | 4.0 | 3.2 |
| 26 | 10.0 | 5.0 | 3.8 |
| 32 | 12.0 | 6.0 | 4.5 |
| 40 | 15.0 | 8.0 | 5.2 |

### 3. Ligações

#### 3.1 Tipos de Ligações

**Ligação Viga-Pilar:**
```
Tipos:
1. Apoio simples (neoprene)
2. Chumbador + graute
3. Consolo + dente
4. Ligação soldada (insertos metálicos)

Esforços transmitidos:
- Reação vertical (V)
- Momento fletor (M) - se ligação rígida
- Força horizontal (H) - vento, desaprumo
```

**Dimensionamento de Consolo:**
```python
def dimensionar_consolo_curto(
    forca_vertical_kN: float,
    forca_horizontal_kN: float,
    distancia_a_cm: float,
    largura_cm: float,
    altura_cm: float,
    f_ck_MPa: float = 35
) -> dict:
    """
    Dimensiona consolo curto (a/d <= 1).
    
    Referência: NBR 9062:2017, item 5.4.3
    """
    # Conversões
    V_d = forca_vertical_kN * 1.4
    H_d = max(forca_horizontal_kN * 1.4, 0.2 * V_d)  # Mínimo 20% de V
    a = distancia_a_cm / 100  # m
    d = (altura_cm - 4) / 100  # m (altura útil)
    b_w = largura_cm / 100  # m
    
    f_cd = (f_ck_MPa / 1.4) * 1000  # kPa
    f_yd = (500 / 1.15) * 1000  # kPa (CA-50)
    
    # Verificar tensão de compressão diagonal
    sigma_cd = V_d / (b_w * 0.85 * d)
    sigma_cd_lim = 0.85 * f_cd
    
    if sigma_cd > sigma_cd_lim:
        return {'erro': f'Tensão de compressão ({sigma_cd:.0f} kPa) excede limite ({sigma_cd_lim:.0f} kPa)'}
    
    # Armadura do tirante
    A_s_tirante = (V_d * a / d + H_d) / f_yd
    A_s_tirante_cm2 = A_s_tirante * 10000
    
    # Armadura de costura (estribos horizontais)
    A_s_costura = 0.4 * A_s_tirante
    A_s_costura_cm2 = A_s_costura * 10000
    
    return {
        'tensao_compressao_kPa': round(sigma_cd, 0),
        'tensao_limite_kPa': round(sigma_cd_lim, 0),
        'A_s_tirante_cm2': round(A_s_tirante_cm2, 2),
        'A_s_costura_cm2': round(A_s_costura_cm2, 2),
        'recomendacao_tirante': f'Usar barras próximas à face superior',
        'recomendacao_costura': f'Distribuir em 2/3 da altura útil'
    }
```

#### 3.2 Aparelhos de Apoio

**Neoprene Fretado:**
```
Dimensionamento:
σ_c = V / (a × b) ≤ 7 MPa (compressão)
τ = H / (a × b) ≤ 1.5 MPa (cisalhamento)

Espessura total:
h_total = n × t_i + (n+1) × t_chapa

Onde:
n = número de camadas de elastômero
t_i = espessura de cada camada (8-12mm)
t_chapa = espessura das chapas de aço (2-3mm)

Dimensões típicas:
100x200mm, 150x250mm, 200x300mm
Espessura: 30-60mm
```

### 4. Transporte e Montagem

#### 4.1 Içamento

**Pontos de Içamento:**
```
Posição dos insertos:
- Vigas: 0.207 × L (pontos de Ritter)
- Lajes: 1/4 do vão de cada extremidade
- Pilares: 1/3 da altura do topo

Esforços durante içamento:
M_içamento = (g × L²) / 8 × fator_dinâmico

fator_dinâmico = 1.5 (içamento normal)
                = 2.0 (içamento com impacto)
```

**Dimensionamento de Inserto:**
```python
def dimensionar_inserto_icamento(
    peso_elemento_kN: float,
    angulo_cabo_graus: float = 60,
    fator_dinamico: float = 1.5
) -> dict:
    """
    Dimensiona inserto metálico para içamento.
    
    Args:
        peso_elemento_kN: Peso do elemento (kN)
        angulo_cabo_graus: Ângulo do cabo com a horizontal (graus)
        fator_dinamico: Fator de impacto (1.5 típico)
    
    Returns:
        dict com força no inserto e especificação
    """
    import math
    
    # Força em cada cabo (2 pontos de içamento)
    angulo_rad = math.radians(angulo_cabo_graus)
    F_cabo = (peso_elemento_kN * fator_dinamico) / (2 * math.sin(angulo_rad))
    
    # Força de tração no inserto
    F_tracao = F_cabo * 1.4  # Majoração
    
    # Especificar inserto (aço ASTM A36, f_y = 250 MPa)
    f_yd = 250 / 1.15  # MPa
    A_necessaria = (F_tracao * 1000) / f_yd  # mm²
    
    # Diâmetro de barra equivalente
    diametros = [12.5, 16, 20, 25, 32]
    areas = [123, 201, 314, 491, 804]  # mm²
    
    inserto = None
    for d, a in zip(diametros, areas):
        if a >= A_necessaria:
            inserto = {'diametro_mm': d, 'area_mm2': a}
            break
    
    return {
        'peso_elemento_kN': peso_elemento_kN,
        'forca_cabo_kN': round(F_cabo, 2),
        'forca_tracao_kN': round(F_tracao, 2),
        'area_necessaria_mm2': round(A_necessaria, 0),
        'inserto_recomendado': inserto
    }
```

#### 4.2 Tolerâncias Dimensionais

**NBR 9062:2017 - Tabela A.1:**

| Elemento | Dimensão | Tolerância |
|----------|----------|------------|
| Viga | Comprimento | ±10mm |
| Viga | Altura | ±5mm |
| Pilar | Altura | ±10mm |
| Pilar | Seção transversal | ±5mm |
| Laje | Comprimento | ±10mm |
| Laje | Largura | ±5mm |
| Laje | Espessura | ±5mm |

**Tolerâncias de Montagem:**
- Prumo de pilares: ≤ h/500
- Nível de vigas: ±10mm
- Posição em planta: ±10mm

### 5. Checklist de Projeto

- [ ] Resistência do concreto ≥ 30 MPa (elementos estruturais)
- [ ] Cobrimento adequado (classe de agressividade)
- [ ] Armadura de suspensão dimensionada
- [ ] Insertos de içamento especificados
- [ ] Ligações detalhadas (consolos, chumbadores)
- [ ] Aparelhos de apoio dimensionados
- [ ] Tolerâncias de fabricação especificadas
- [ ] Sequência de montagem definida
- [ ] Escoramento temporário previsto
- [ ] Juntas de dilatação localizadas

## Outputs Esperados

1. **Memorial de Cálculo**
   - Dimensionamento de elementos
   - Verificação de ligações
   - Cálculo de aparelhos de apoio

2. **Detalhamento**
   - Armaduras e insertos
   - Posição de apoios
   - Juntas e interfaces

3. **Especificações**
   - Concreto (fck, slump, agregados)
   - Aço (CA-50, CA-60)
   - Aparelhos de apoio (neoprene)

4. **Plano de Montagem**
   - Sequência de içamento
   - Equipamentos necessários
   - Escoramento temporário

## Referências

- **NBR 9062:2017** - Projeto e execução de estruturas de concreto pré-moldado
- **NBR 6118:2014** - Projeto de estruturas de concreto
- **El Debs, M.K.** - Concreto Pré-Moldado: Fundamentos e Aplicações
- **PCI Design Handbook** - Precast and Prestressed Concrete
