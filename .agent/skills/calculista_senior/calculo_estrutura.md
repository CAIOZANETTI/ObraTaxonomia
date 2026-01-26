---
skill_name: "Dimensionamento de Estruturas de Concreto e Aço"
agent: calculista_senior
category: "Cálculo Estrutural"
difficulty: expert
version: 1.0.0
---

# Skill: Cálculo de Estruturas (Concreto Armado e Aço)

## Objetivo

Fornecer metodologia completa para dimensionamento de elementos estruturais de concreto armado e aço, incluindo vigas, pilares, lajes e ligações, conforme NBR 6118 e NBR 8800.

## PARTE I: ESTRUTURAS DE CONCRETO ARMADO

### 1. Dimensionamento de Vigas à Flexão

#### 1.1 Domínios de Deformação (NBR 6118)

```
Domínio 1: Tração pura ou flexo-tração (toda seção tracionada)
Domínio 2: Flexo-tração (LN corta a seção, ε_c < 3.5‰)
Domínio 3: Flexão simples ou composta (ε_c = 3.5‰, ε_s ≥ ε_yd)
Domínio 4: Flexo-compressão (ε_c = 3.5‰, ε_s < ε_yd)
Domínio 5: Compressão simples ou composta (toda seção comprimida)

Domínio ideal: Domínio 3 (seção subarmada, ruptura dúctil)
```

#### 1.2 Cálculo de Armadura Longitudinal

**Momento Resistente:**
```
M_d = momento de cálculo
M_d = γ_f × M_k

Posição da linha neutra:
x = (A_s × f_yd) / (0.68 × b × f_cd)

Verificação de domínio:
x/d ≤ 0.45 (Domínio 3 - seção subarmada)
x/d > 0.45 (Domínio 4 - seção superarmada - EVITAR)

Área de aço necessária:
A_s = M_d / (f_yd × z)

Braço de alavanca:
z = d - 0.4x  (aproximado)
z = d - 0.5a  (onde a = 0.8x é altura do bloco de tensões)
```

**Exemplo de Código:**

```python
def dimensionar_viga_flexao_simples(
    b_cm: float,
    h_cm: float,
    d_cm: float,
    M_kNm: float,
    f_ck_MPa: float = 25,
    f_yk_MPa: float = 500
) -> dict:
    """
    Dimensiona armadura longitudinal de viga à flexão simples.
    
    Args:
        b_cm: Largura da seção (cm)
        h_cm: Altura total da seção (cm)
        d_cm: Altura útil (cm)
        M_kNm: Momento fletor característico (kN.m)
        f_ck_MPa: Resistência característica do concreto (MPa)
        f_yk_MPa: Resistência característica do aço (MPa)
    
    Returns:
        dict com A_s (cm²), número de barras, e verificações
    
    Referência: NBR 6118:2014
    """
    # Conversões
    b = b_cm / 100  # m
    d = d_cm / 100  # m
    M_d = M_kNm * 1.4  # kN.m (majorado)
    
    # Resistências de cálculo
    f_cd = (f_ck_MPa / 1.4) * 1000  # kPa
    f_yd = (f_yk_MPa / 1.15) * 1000  # kPa
    
    # Cálculo da linha neutra (iterativo simplificado)
    # Assumindo domínio 3 inicialmente
    K_md = M_d / (b * d**2 * f_cd)
    
    if K_md > 0.295:
        return {
            'erro': 'Seção superarmada (Domínio 4). Aumentar seção ou usar armadura dupla.',
            'K_md': K_md
        }
    
    # Coeficiente K_z (tabela)
    K_z = 1.0 - 0.5 * (1 - (1 - 2*K_md)**0.5)
    z = K_z * d
    
    # Área de aço
    A_s_m2 = M_d / (f_yd * z)
    A_s_cm2 = A_s_m2 * 10000
    
    # Verificar armadura mínima
    rho_min = 0.15 / 100  # 0.15% para CA-50
    A_s_min_cm2 = rho_min * b_cm * d_cm
    
    A_s_final_cm2 = max(A_s_cm2, A_s_min_cm2)
    
    # Sugerir bitola e quantidade
    bitolas = [10, 12.5, 16, 20, 25]  # mm
    areas_bitola = [0.79, 1.23, 2.01, 3.14, 4.91]  # cm²
    
    melhor_config = None
    for i, (bitola, area) in enumerate(zip(bitolas, areas_bitola)):
        n_barras = int(np.ceil(A_s_final_cm2 / area))
        if n_barras <= 6:  # Limite prático
            melhor_config = {
                'bitola_mm': bitola,
                'n_barras': n_barras,
                'area_efetiva_cm2': n_barras * area
            }
            break
    
    # Verificar posição da LN
    x = (A_s_final_cm2 / 10000 * f_yd) / (0.68 * b * f_cd)
    x_d = x / d
    
    dominio = 'Domínio 3 (OK)' if x_d <= 0.45 else 'Domínio 4 (Superarmada)'
    
    return {
        'A_s_calculado_cm2': round(A_s_cm2, 2),
        'A_s_minimo_cm2': round(A_s_min_cm2, 2),
        'A_s_adotado_cm2': round(A_s_final_cm2, 2),
        'configuracao': melhor_config,
        'x_d': round(x_d, 3),
        'dominio': dominio,
        'K_md': round(K_md, 3)
    }

# Exemplo de uso
resultado = dimensionar_viga_flexao_simples(
    b_cm=20,
    h_cm=50,
    d_cm=45,
    M_kNm=80,
    f_ck_MPa=25
)

print(f"Armadura necessária: {resultado['A_s_adotado_cm2']} cm²")
print(f"Configuração: {resultado['configuracao']['n_barras']}φ{resultado['configuracao']['bitola_mm']}")
print(f"Domínio: {resultado['dominio']}")
```

#### 1.3 Dimensionamento ao Cisalhamento

**Verificação de Compressão Diagonal:**
```
V_Rd2 = 0.27 × (1 - f_ck/250) × f_cd × b_w × d

Condição:
V_Sd ≤ V_Rd2 (caso contrário, aumentar seção)
```

**Armadura Transversal (Estribos):**
```
Modelo de Treliça (θ = 45°):

V_Rd3 = (A_sw / s) × 0.9 × d × f_ywd

Onde:
A_sw = área de aço do estribo (2 ramos)
s = espaçamento entre estribos
f_ywd = f_yk / γ_s

Resolvendo para A_sw/s:
(A_sw / s) = V_Sd / (0.9 × d × f_ywd)

Armadura mínima:
ρ_sw,min = 0.2 × f_ctm / f_ywk
A_sw,min / s = ρ_sw,min × b_w × sen(α)
```

**Exemplo:**
```python
def dimensionar_estribos(
    V_kN: float,
    b_cm: float,
    d_cm: float,
    f_ck_MPa: float = 25,
    f_ywk_MPa: float = 500
) -> dict:
    """
    Dimensiona armadura transversal (estribos) para cisalhamento.
    
    Args:
        V_kN: Força cortante de cálculo (kN)
        b_cm: Largura da viga (cm)
        d_cm: Altura útil (cm)
        f_ck_MPa: Resistência do concreto (MPa)
        f_ywk_MPa: Resistência do aço (MPa)
    
    Returns:
        dict com espaçamento e configuração de estribos
    """
    # Conversões
    V_Sd = V_kN * 1.4  # kN
    b_w = b_cm / 100  # m
    d = d_cm / 100  # m
    
    f_cd = (f_ck_MPa / 1.4) * 1000  # kPa
    f_ywd = (f_ywk_MPa / 1.15) * 1000  # kPa
    
    # Verificar V_Rd2
    V_Rd2 = 0.27 * (1 - f_ck_MPa/250) * f_cd * b_w * d
    
    if V_Sd > V_Rd2:
        return {'erro': f'V_Sd ({V_Sd:.1f} kN) > V_Rd2 ({V_Rd2:.1f} kN). Aumentar seção.'}
    
    # Calcular A_sw/s necessário
    Asw_s_necessario = V_Sd / (0.9 * d * f_ywd)  # m²/m
    Asw_s_cm2_m = Asw_s_necessario * 10000  # cm²/m
    
    # Armadura mínima
    f_ctm = 0.3 * f_ck_MPa**(2/3)
    rho_sw_min = 0.2 * f_ctm / f_ywk_MPa
    Asw_s_min = rho_sw_min * b_cm  # cm²/m
    
    Asw_s_final = max(Asw_s_cm2_m, Asw_s_min)
    
    # Configurações de estribos (2 ramos)
    configs = [
        {'bitola': 5.0, 'area_2_ramos': 0.40},
        {'bitola': 6.3, 'area_2_ramos': 0.63},
        {'bitola': 8.0, 'area_2_ramos': 1.01},
        {'bitola': 10.0, 'area_2_ramos': 1.57}
    ]
    
    resultados = []
    for config in configs:
        s_cm = (config['area_2_ramos'] / Asw_s_final) * 100
        
        # Espaçamento máximo
        if V_Sd <= 0.67 * V_Rd2:
            s_max = min(0.6 * d_cm, 300)
        else:
            s_max = min(0.3 * d_cm, 200)
        
        s_adotado = min(s_cm, s_max)
        
        # Arredondar para múltiplo de 5cm
        s_adotado = int(s_adotado / 5) * 5
        if s_adotado < 10:
            s_adotado = 10
        
        resultados.append({
            'bitola_mm': config['bitola'],
            'espacamento_cm': s_adotado,
            'notacao': f'φ{config["bitola"]} c/ {s_adotado}cm'
        })
    
    return {
        'Asw_s_necessario_cm2_m': round(Asw_s_cm2_m, 2),
        'Asw_s_minimo_cm2_m': round(Asw_s_min, 2),
        'configuracoes': resultados,
        'recomendacao': resultados[0]['notacao']
    }
```

### 2. Dimensionamento de Pilares

#### 2.1 Classificação quanto à Esbeltez

```
Índice de esbeltez:
λ = l_e / i

Onde:
l_e = comprimento de flambagem
i = raio de giração = √(I/A)

Classificação:
λ ≤ 35: Pilar curto (desprezar efeitos de 2ª ordem)
35 < λ ≤ 90: Pilar medianamente esbelto
90 < λ ≤ 140: Pilar esbelto
λ > 140: Pilar muito esbelto (evitar)

Comprimento de flambagem:
l_e = l_0 × β

β = 1.0 (engastado-livre)
β = 0.7 (engastado-engastado)
β = 0.5 (engastado-apoiado)
β = 1.0 (apoiado-apoiado)
```

#### 2.2 Armadura Longitudinal

```
Armadura mínima:
A_s,min = 0.15 × N_d / f_yd ≥ 0.004 × A_c

Armadura máxima:
A_s,max = 0.08 × A_c (fora de emendas)
A_s,max = 0.04 × A_c (em emendas)

Número mínimo de barras:
- Seção circular: 6 barras
- Seção retangular: 4 barras (1 em cada canto)
- Seção triangular: 3 barras

Bitola mínima:
φ_min = 10 mm (pilares)
φ_min = 12.5 mm (pilares principais)
```

#### 2.3 Armadura Transversal (Estribos)

```
Bitola mínima:
φ_t ≥ 5 mm
φ_t ≥ φ_l / 4 (1/4 da bitola longitudinal)

Espaçamento máximo:
s ≤ 20 cm
s ≤ menor dimensão da seção
s ≤ 12 × φ_l (12× bitola longitudinal)
```

### 3. Dimensionamento de Lajes

#### 3.1 Tipos de Lajes

**Laje Maciça:**
```
Espessura mínima:
h_min = l / 35 (laje bi-apoiada)
h_min = l / 42 (laje contínua)
h_min ≥ 7 cm (lajes de cobertura)
h_min ≥ 10 cm (lajes de piso)
```

**Laje Nervurada:**
```
Espessura da mesa:
h_f ≥ 4 cm (sem tubulação)
h_f ≥ 5 cm (com tubulação)

Largura da nervura:
b_w ≥ 5 cm
```

#### 3.2 Armadura de Lajes

```
Armadura mínima:
ρ_min = 0.15% (CA-50)
A_s,min = 0.0015 × b × h

Espaçamento máximo:
s_max = 2h ≤ 20 cm (armadura principal)
s_max = 3h ≤ 33 cm (armadura secundária)

Armadura de distribuição:
A_s,dist = 20% × A_s,principal
```

## PARTE II: ESTRUTURAS DE AÇO

### 4. Dimensionamento de Vigas de Aço

#### 4.1 Verificação de Momento Fletor

**Flambagem Local da Mesa (FLM):**
```
λ = b / t_f

λ_p = 0.38 × √(E / f_y)  (limite plástico)
λ_r = 1.0 × √(E / f_y)   (limite elástico)

Se λ ≤ λ_p: Seção compacta (M_n = M_p)
Se λ_p < λ ≤ λ_r: Seção semi-compacta (interpolação)
Se λ > λ_r: Seção esbelta (M_n < M_y)
```

**Momento Resistente:**
```
M_Rd = M_n / γ_a1

M_p = Z × f_y (momento plástico)
M_y = W × f_y (momento de escoamento)

Onde:
Z = módulo plástico
W = módulo elástico
γ_a1 = 1.10
```

#### 4.2 Verificação de Cisalhamento

```
V_Rd = 0.6 × A_w × f_y / γ_a1

Onde:
A_w = área da alma = d × t_w
d = altura da alma
t_w = espessura da alma
```

#### 4.3 Verificação de Flecha

```
δ_max = L / 350 (vigas de piso)
δ_max = L / 250 (vigas de cobertura)
δ_max = L / 180 (balanços)
```

### 5. Dimensionamento de Pilares de Aço

#### 5.1 Resistência à Compressão

**Esbeltez Reduzida:**
```
λ_0 = (KL/r) × √(f_y / E) / π

Onde:
K = coeficiente de flambagem
L = comprimento do pilar
r = raio de giração mínimo
```

**Fator de Redução:**
```
Se λ_0 ≤ 1.5:
χ = 0.658^(λ_0²)

Se λ_0 > 1.5:
χ = 0.877 / λ_0²
```

**Força Normal Resistente:**
```
N_Rd = χ × A_g × f_y / γ_a1

Onde:
A_g = área bruta da seção
```

### 6. Ligações

#### 6.1 Ligações Parafusadas

**Resistência ao Cisalhamento:**
```
F_v,Rd = 0.42 × A_b × f_ub / γ_a2

Onde:
A_b = área bruta do parafuso
f_ub = resistência à ruptura do parafuso
γ_a2 = 1.35
```

**Resistência ao Esmagamento:**
```
F_p,Rd = 2.4 × d × t × f_u / γ_a2

Onde:
d = diâmetro do parafuso
t = espessura da chapa
f_u = resistência à ruptura da chapa
```

#### 6.2 Ligações Soldadas

**Solda de Filete:**
```
F_w,Rd = 0.6 × A_w × f_u / (√3 × γ_a2)

Onde:
A_w = área efetiva da solda = 0.7 × a × l
a = garganta efetiva
l = comprimento da solda
```

## Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Memorial de Cálculo Estruturado**
   - Dados de entrada
   - Fórmulas aplicadas
   - Verificações normativas
   - Resultados finais

2. **Detalhamento de Armaduras**
   - Bitolas e quantidades
   - Espaçamentos
   - Comprimentos de ancoragem
   - Desenhos esquemáticos

3. **Verificações de Segurança**
   - Domínios de deformação
   - Esbeltez
   - Flechas
   - Tensões

4. **Especificações Técnicas**
   - Classe de concreto
   - Tipo de aço
   - Cobrimentos
   - Procedimentos executivos

## Referências

- **NBR 6118:2014** - Projeto de estruturas de concreto
- **NBR 8800:2008** - Projeto de estruturas de aço
- **Fusco, P.B.** - Técnica de Armar as Estruturas de Concreto
- **Pfeil, W.** - Estruturas de Aço - Dimensionamento Prático
