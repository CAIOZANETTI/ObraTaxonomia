---
skill_name: "Dimensionamento de Estruturas Metálicas"
agent: calculista_senior
category: "Cálculo Estrutural"
difficulty: expert
version: 1.0.0
---

# Skill: Dimensionamento de Estruturas Metálicas

## Objetivo

Fornecer metodologia completa para projeto e dimensionamento de estruturas de aço, incluindo vigas, pilares, treliças e ligações, conforme NBR 8800:2008 e AISC 360.

## Fundamentos Teóricos

### 1. Propriedades dos Aços Estruturais

#### 1.1 Aços Carbono (ASTM)

| Especificação | f_y (MPa) | f_u (MPa) | Aplicação |
|---------------|-----------|-----------|-----------|
| ASTM A36 | 250 | 400 | Perfis, chapas (uso geral) |
| ASTM A572 Gr.50 | 345 | 450 | Perfis de alta resistência |
| ASTM A588 | 345 | 485 | Aço patinável (weathering) |
| ASTM A992 | 345-450 | 450 | Perfis W (vigas) |

#### 1.2 Perfis Laminados

**Perfis I e W (Abas Paralelas):**
```
Nomenclatura: W 310 x 52
              │   │    │
              │   │    └─ Peso (kg/m)
              │   └────── Altura nominal (mm)
              └────────── Tipo de perfil

Propriedades geométricas:
- A = área da seção (cm²)
- I_x, I_y = momentos de inércia (cm⁴)
- W_x, W_y = módulos elásticos (cm³)
- Z_x, Z_y = módulos plásticos (cm³)
- r_x, r_y = raios de giração (cm)
```

**Perfis U e L:**
```
U: Cantoneira de abas desiguais
L: Cantoneira de abas iguais ou desiguais

Aplicações:
- Terças, montantes
- Contraventamentos
- Torres, treliças
```

### 2. Dimensionamento de Vigas

#### 2.1 Momento Fletor

**Estados Limites:**
```
1. Escoamento da seção (FLM - Flambagem Local da Mesa)
2. Flambagem Lateral com Torção (FLT)
3. Flambagem Local da Alma (FLA)
```

**Classificação de Seções:**
```
Parâmetro de esbeltez da mesa:
λ = b / t_f

λ_p = 0.38 × √(E / f_y)  (limite plástico)
λ_r = 1.0 × √(E / f_y)   (limite elástico)

Se λ ≤ λ_p: Seção compacta (plastificação total)
Se λ_p < λ ≤ λ_r: Seção semi-compacta
Se λ > λ_r: Seção esbelta
```

**Momento Resistente:**
```python
def dimensionar_viga_aco_flexao(
    perfil: str,
    vao_m: float,
    carga_kN_m: float,
    f_y_MPa: float = 250,
    E_GPa: float = 200
) -> dict:
    """
    Dimensiona viga de aço à flexão simples.
    
    Args:
        perfil: Designação do perfil (ex: 'W310x52')
        vao_m: Vão da viga (m)
        carga_kN_m: Carga distribuída (kN/m)
        f_y_MPa: Tensão de escoamento (MPa)
        E_GPa: Módulo de elasticidade (GPa)
    
    Returns:
        dict com verificações de momento e flecha
    
    Referência: NBR 8800:2008
    """
    import math
    
    # Banco de dados simplificado de perfis W
    perfis_db = {
        'W250x25.3': {'d': 257, 'b_f': 102, 't_f': 8.4, 't_w': 5.8, 
                      'A': 32.3, 'I_x': 4020, 'W_x': 313, 'Z_x': 354, 'r_x': 11.2},
        'W310x52': {'d': 317, 'b_f': 167, 't_f': 13.2, 't_w': 7.6,
                    'A': 66.2, 'I_x': 11900, 'W_x': 752, 'Z_x': 852, 'r_x': 13.4},
        'W410x85': {'d': 417, 'b_f': 181, 't_f': 18.2, 't_w': 10.9,
                    'A': 108, 'I_x': 31600, 'W_x': 1510, 'Z_x': 1710, 'r_x': 17.1}
    }
    
    if perfil not in perfis_db:
        return {'erro': f'Perfil {perfil} não encontrado no banco de dados'}
    
    p = perfis_db[perfil]
    
    # Momento máximo (viga biapoiada)
    M_k = (carga_kN_m * vao_m**2) / 8  # kN.m
    M_Sd = M_k * 1.4  # kN.m (majorado)
    
    # Verificação de FLM (Flambagem Local da Mesa)
    lambda_mesa = (p['b_f'] / 2) / p['t_f']
    lambda_p = 0.38 * math.sqrt(E_GPa * 1000 / f_y_MPa)
    lambda_r = 1.0 * math.sqrt(E_GPa * 1000 / f_y_MPa)
    
    if lambda_mesa <= lambda_p:
        # Seção compacta
        M_n = p['Z_x'] * f_y_MPa / 1000  # kN.m (momento plástico)
        classificacao = 'Compacta'
    elif lambda_mesa <= lambda_r:
        # Seção semi-compacta (interpolação)
        M_p = p['Z_x'] * f_y_MPa / 1000
        M_y = p['W_x'] * f_y_MPa / 1000
        M_n = M_p - (M_p - M_y) * ((lambda_mesa - lambda_p) / (lambda_r - lambda_p))
        classificacao = 'Semi-compacta'
    else:
        # Seção esbelta
        M_n = p['W_x'] * f_y_MPa / 1000  # kN.m (momento elástico)
        classificacao = 'Esbelta'
    
    # Momento resistente de cálculo
    gamma_a1 = 1.10
    M_Rd = M_n / gamma_a1
    
    # Verificação de FLT (Flambagem Lateral com Torção)
    # Simplificado: assumir contenção lateral adequada
    # Para análise completa, verificar L_b vs L_p e L_r
    
    # Verificação de segurança
    aprovado_momento = M_Sd <= M_Rd
    taxa_utilizacao = (M_Sd / M_Rd) * 100
    
    # Verificação de flecha (ELS)
    E = E_GPa * 1e6  # kPa
    I_x = p['I_x'] * 1e-8  # m⁴ (conversão de cm⁴)
    delta_max = (5 * carga_kN_m * vao_m**4) / (384 * E * I_x)  # m
    delta_lim = vao_m / 350  # m (limite L/350)
    
    aprovado_flecha = delta_max <= delta_lim
    
    return {
        'perfil': perfil,
        'classificacao_secao': classificacao,
        'lambda_mesa': round(lambda_mesa, 2),
        'lambda_p': round(lambda_p, 2),
        'M_Sd_kNm': round(M_Sd, 2),
        'M_Rd_kNm': round(M_Rd, 2),
        'aprovado_momento': aprovado_momento,
        'taxa_utilizacao_pct': round(taxa_utilizacao, 1),
        'flecha_mm': round(delta_max * 1000, 2),
        'flecha_limite_mm': round(delta_lim * 1000, 2),
        'aprovado_flecha': aprovado_flecha,
        'status': 'OK' if (aprovado_momento and aprovado_flecha) else 'REPROVAR'
    }

# Exemplo de uso
resultado = dimensionar_viga_aco_flexao(
    perfil='W310x52',
    vao_m=8.0,
    carga_kN_m=25.0,
    f_y_MPa=250
)

print(f"Perfil: {resultado['perfil']}")
print(f"M_Sd = {resultado['M_Sd_kNm']} kN.m")
print(f"M_Rd = {resultado['M_Rd_kNm']} kN.m")
print(f"Taxa de utilização: {resultado['taxa_utilizacao_pct']}%")
print(f"Flecha: {resultado['flecha_mm']} mm (limite: {resultado['flecha_limite_mm']} mm)")
print(f"Status: {resultado['status']}")
```

#### 2.2 Cisalhamento

**Resistência ao Cisalhamento:**
```
V_Rd = 0.6 × A_w × f_y / γ_a1

Onde:
A_w = área da alma = d × t_w
d = altura da alma
t_w = espessura da alma
γ_a1 = 1.10
```

### 3. Dimensionamento de Pilares

#### 3.1 Compressão Axial

**Esbeltez Reduzida:**
```
λ_0 = (K × L / r) × √(f_y / E) / π

Onde:
K = coeficiente de flambagem
L = comprimento do pilar
r = raio de giração mínimo
```

**Fator de Redução (Curva de Flambagem):**
```python
def calcular_fator_reducao_flambagem(
    lambda_0: float,
    curva: str = 'a'
) -> float:
    """
    Calcula fator de redução χ para flambagem.
    
    Args:
        lambda_0: Esbeltez reduzida
        curva: Curva de flambagem ('a', 'b', 'c', 'd')
    
    Returns:
        χ: Fator de redução
    
    Referência: NBR 8800:2008, Tabela E.3
    """
    import math
    
    # Fator de imperfeição
    alpha_curvas = {
        'a': 0.21,
        'b': 0.34,
        'c': 0.49,
        'd': 0.76
    }
    
    alpha = alpha_curvas.get(curva, 0.21)
    
    # Fator auxiliar
    beta = 0.5 * (1 + alpha * (lambda_0 - 0.2) + lambda_0**2)
    
    # Fator de redução
    if lambda_0 <= 1.5:
        chi = 1 / (beta + math.sqrt(beta**2 - lambda_0**2))
    else:
        chi = 0.877 / lambda_0**2
    
    # Limite
    chi = min(chi, 1.0)
    
    return chi

def dimensionar_pilar_aco_compressao(
    perfil: str,
    comprimento_m: float,
    forca_kN: float,
    K: float = 1.0,
    f_y_MPa: float = 250,
    curva_flambagem: str = 'a'
) -> dict:
    """
    Dimensiona pilar de aço à compressão axial.
    
    Args:
        perfil: Designação do perfil
        comprimento_m: Comprimento do pilar (m)
        forca_kN: Força de compressão (kN)
        K: Coeficiente de flambagem
        f_y_MPa: Tensão de escoamento (MPa)
        curva_flambagem: Curva de flambagem ('a', 'b', 'c', 'd')
    
    Returns:
        dict com verificações
    """
    import math
    
    # Banco de dados de perfis
    perfis_db = {
        'W200x46.1': {'A': 58.8, 'r_x': 8.89, 'r_y': 5.08},
        'W250x73': {'A': 93.1, 'r_x': 11.2, 'r_y': 6.37},
        'W310x97': {'A': 123, 'r_x': 13.7, 'r_y': 7.75}
    }
    
    if perfil not in perfis_db:
        return {'erro': f'Perfil {perfil} não encontrado'}
    
    p = perfis_db[perfil]
    
    # Força de cálculo
    N_Sd = forca_kN * 1.4  # kN
    
    # Esbeltez
    L = comprimento_m * 100  # cm
    r_min = min(p['r_x'], p['r_y'])  # cm
    lambda_real = (K * L) / r_min
    
    # Esbeltez reduzida
    E = 200000  # MPa
    lambda_0 = (lambda_real / math.pi) * math.sqrt(f_y_MPa / E)
    
    # Fator de redução
    chi = calcular_fator_reducao_flambagem(lambda_0, curva_flambagem)
    
    # Força normal resistente
    gamma_a1 = 1.10
    N_Rd = (chi * p['A'] * f_y_MPa) / gamma_a1  # kN
    
    # Verificação
    aprovado = N_Sd <= N_Rd
    taxa_utilizacao = (N_Sd / N_Rd) * 100
    
    return {
        'perfil': perfil,
        'comprimento_m': comprimento_m,
        'esbeltez_real': round(lambda_real, 1),
        'esbeltez_reduzida': round(lambda_0, 3),
        'fator_reducao_chi': round(chi, 3),
        'N_Sd_kN': round(N_Sd, 2),
        'N_Rd_kN': round(N_Rd, 2),
        'aprovado': aprovado,
        'taxa_utilizacao_pct': round(taxa_utilizacao, 1),
        'status': 'OK' if aprovado else 'REPROVAR'
    }
```

### 4. Ligações

#### 4.1 Ligações Parafusadas

**Resistência ao Cisalhamento:**
```
F_v,Rd = 0.42 × A_b × f_ub / γ_a2

Onde:
A_b = área bruta do parafuso (mm²)
f_ub = resistência à ruptura do parafuso (MPa)
γ_a2 = 1.35

Parafusos ASTM A325:
f_ub = 825 MPa (até 1")
f_ub = 725 MPa (> 1" até 1.5")
```

**Resistência ao Esmagamento:**
```
F_p,Rd = 2.4 × d × t × f_u / γ_a2

Onde:
d = diâmetro do parafuso (mm)
t = espessura da chapa (mm)
f_u = resistência à ruptura da chapa (MPa)
```

**Código Python:**
```python
def dimensionar_parafuso_cisalhamento(
    diametro_mm: float,
    num_parafusos: int,
    forca_kN: float,
    tipo_parafuso: str = 'A325',
    espessura_chapa_mm: float = 10,
    f_u_chapa_MPa: float = 400
) -> dict:
    """
    Dimensiona ligação parafusada ao cisalhamento.
    
    Referência: NBR 8800:2008, item 6.3
    """
    import math
    
    # Propriedades dos parafusos
    f_ub_parafuso = {
        'A307': 400,
        'A325': 825,
        'A490': 1035
    }
    
    f_ub = f_ub_parafuso.get(tipo_parafuso, 825)
    
    # Área do parafuso
    A_b = math.pi * (diametro_mm / 2)**2  # mm²
    
    # Resistência ao cisalhamento (1 plano de corte)
    gamma_a2 = 1.35
    F_v_Rd_parafuso = (0.42 * A_b * f_ub) / gamma_a2 / 1000  # kN
    
    # Resistência ao esmagamento
    F_p_Rd_parafuso = (2.4 * diametro_mm * espessura_chapa_mm * f_u_chapa_MPa) / gamma_a2 / 1000  # kN
    
    # Resistência mínima
    F_Rd_parafuso = min(F_v_Rd_parafuso, F_p_Rd_parafuso)
    
    # Resistência total
    F_Rd_total = F_Rd_parafuso * num_parafusos
    
    # Força de cálculo
    F_Sd = forca_kN * 1.4
    
    # Verificação
    aprovado = F_Sd <= F_Rd_total
    taxa_utilizacao = (F_Sd / F_Rd_total) * 100
    
    return {
        'diametro_mm': diametro_mm,
        'tipo_parafuso': tipo_parafuso,
        'num_parafusos': num_parafusos,
        'F_v_Rd_kN': round(F_v_Rd_parafuso, 2),
        'F_p_Rd_kN': round(F_p_Rd_parafuso, 2),
        'F_Rd_parafuso_kN': round(F_Rd_parafuso, 2),
        'F_Rd_total_kN': round(F_Rd_total, 2),
        'F_Sd_kN': round(F_Sd, 2),
        'aprovado': aprovado,
        'taxa_utilizacao_pct': round(taxa_utilizacao, 1),
        'status': 'OK' if aprovado else 'REPROVAR'
    }
```

#### 4.2 Ligações Soldadas

**Solda de Filete:**
```
F_w,Rd = 0.6 × A_w × f_u / (√3 × γ_a2)

Onde:
A_w = área efetiva da solda = 0.7 × a × l
a = garganta efetiva (mm)
l = comprimento da solda (mm)
f_u = resistência do metal base (MPa)
```

## Outputs Esperados

1. **Memorial de Cálculo**
   - Cargas e combinações
   - Verificações de ELU e ELS
   - Dimensionamento de perfis

2. **Detalhamento de Ligações**
   - Tipo de ligação (parafusada/soldada)
   - Quantidade e disposição
   - Especificações técnicas

3. **Especificações**
   - Aço estrutural (ASTM A36, A572, etc.)
   - Parafusos (ASTM A325, A490)
   - Soldas (eletrodos, processos)
   - Proteção anticorrosiva

4. **Desenhos**
   - Detalhes de ligações
   - Furação de chapas
   - Sequência de montagem

## Referências

- **NBR 8800:2008** - Projeto de estruturas de aço e de estruturas mistas
- **AISC 360-16** - Specification for Structural Steel Buildings
- **Pfeil, W.; Pfeil, M.** - Estruturas de Aço - Dimensionamento Prático
- **Bellei, I.H.** - Edifícios Industriais em Aço
