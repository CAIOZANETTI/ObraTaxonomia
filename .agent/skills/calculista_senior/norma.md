---
skill_name: "Normas Técnicas - Interpretação e Aplicação"
agent: calculista_senior
category: "Normas e Regulamentação"
difficulty: advanced
version: 1.0.0
---

# Skill: Normas Técnicas (NBR 6118, 6122, Eurocode)

## Objetivo

Fornecer guia de referência rápida para interpretação e aplicação das principais normas técnicas brasileiras e internacionais em projetos estruturais de concreto armado, fundações e estruturas metálicas.

## Normas Brasileiras (ABNT)

### 1. NBR 6118:2014 - Projeto de Estruturas de Concreto

#### 1.1 Resistências Características

**Concreto:**
```
f_ck = Resistência característica à compressão (MPa)

Classes usuais:
- C20: f_ck = 20 MPa (uso geral)
- C25: f_ck = 25 MPa (estruturas correntes)
- C30: f_ck = 30 MPa (edifícios, pontes)
- C40: f_ck = 40 MPa (estruturas especiais)
- C50+: f_ck ≥ 50 MPa (concreto de alto desempenho)

Resistência de cálculo:
f_cd = f_ck / γ_c
γ_c = 1.4 (coeficiente de ponderação)

Resistência à tração:
f_ctk,inf = 0.7 × 0.3 × f_ck^(2/3)  (valor inferior)
f_ctk,sup = 1.3 × 0.3 × f_ck^(2/3)  (valor superior)
```

**Aço:**
```
f_yk = Resistência característica ao escoamento (MPa)

Categorias:
- CA-25: f_yk = 250 MPa (barras lisas)
- CA-50: f_yk = 500 MPa (barras nervuradas - mais comum)
- CA-60: f_yk = 600 MPa (fios e telas soldadas)

Resistência de cálculo:
f_yd = f_yk / γ_s
γ_s = 1.15 (coeficiente de ponderação)
```

#### 1.2 Cobrimentos Mínimos (Tabela 7.2)

| Classe de Agressividade | Laje | Viga/Pilar | Fundação |
|-------------------------|------|------------|----------|
| **I (Fraca)**           | 20mm | 25mm       | 30mm     |
| **II (Moderada)**       | 25mm | 30mm       | 35mm     |
| **III (Forte)**         | 35mm | 40mm       | 45mm     |
| **IV (Muito Forte)**    | 45mm | 50mm       | 55mm     |

**Classe de Agressividade:**
- **I:** Interior de edificações (exceto áreas molhadas)
- **II:** Exterior de edificações, áreas molhadas
- **III:** Ambiente marinho (> 50m do mar), industrial
- **IV:** Respingos de maré, zona de variação de maré

#### 1.3 Limites de Flechas (Tabela 13.3)

**Vigas:**
```
Flecha imediata:        δ_i ≤ L / 250
Flecha total:           δ_total ≤ L / 350 (com contra-flecha)
                        δ_total ≤ L / 250 (sem contra-flecha)
Flecha após construção: δ_2 ≤ L / 500 (aceitação sensorial)

Onde:
L = vão da viga (mm)
δ = flecha (mm)
```

**Balanços:**
```
Flecha imediata: δ_i ≤ L / 125
```

#### 1.4 Armadura Mínima e Máxima

**Armadura Longitudinal (Vigas):**
```
A_s,min = 0.15 × N_d / f_yd  (seção comprimida)
A_s,min = ρ_min × A_c         (seção tracionada)

ρ_min = 0.15% (CA-50)
ρ_min = 0.164% (CA-25)

A_s,max = 4% × A_c (fora de regiões de emenda)
A_s,max = 8% × A_c (em regiões de emenda)
```

**Armadura de Cisalhamento:**
```
ρ_sw,min = 0.2 × f_ctm / f_ywk

Espaçamento máximo:
s_max = 0.6 × d ≤ 300mm (se V_Sd ≤ 0.67 × V_Rd2)
s_max = 0.3 × d ≤ 200mm (se V_Sd > 0.67 × V_Rd2)
```

#### 1.5 Combinações de Ações

**Estado Limite Último (ELU):**
```
F_d = γ_g × G_k + γ_q × Q_k

Combinação Normal:
γ_g = 1.4 (ações permanentes)
γ_q = 1.4 (ações variáveis)

Combinação Especial:
γ_g = 1.2
γ_q = 1.2

Combinação Excepcional:
γ_g = 1.0
γ_q = 0.0 (exceto ação excepcional)
```

**Estado Limite de Serviço (ELS):**
```
Combinação Quase Permanente:
F_ser = G_k + ψ_2 × Q_k

ψ_2 (edifícios residenciais) = 0.3
ψ_2 (edifícios comerciais) = 0.4
ψ_2 (bibliotecas, arquivos) = 0.6
```

### 2. NBR 6122:2019 - Projeto e Execução de Fundações

#### 2.1 Fatores de Segurança

**Fundações Rasas:**
```
FS_global ≥ 3.0 (tensões admissíveis)

Verificação:
σ_atuante ≤ σ_admissível = σ_ruptura / FS
```

**Fundações Profundas (Estacas):**
```
Método Semi-Empírico:
FS_ponta = 4.0
FS_lateral = 3.0
FS_global = 2.0

Prova de Carga:
FS = 2.0 (carga de trabalho)
```

#### 2.2 Recalques Admissíveis

| Tipo de Estrutura | Recalque Absoluto | Recalque Diferencial |
|-------------------|-------------------|----------------------|
| Estruturas de concreto | < 50mm | < 20mm |
| Estruturas metálicas | < 75mm | < 30mm |
| Muros de arrimo | < 100mm | - |
| Silos e chaminés | < 300mm | - |

**Distorção Angular:**
```
β = Δδ / L

β_max = 1/500 (estruturas sensíveis)
β_max = 1/300 (estruturas convencionais)

Onde:
Δδ = recalque diferencial
L = distância entre apoios
```

#### 2.3 Profundidade Mínima de Fundação

```
h_min ≥ 0.60m (sapatas isoladas)
h_min ≥ 0.80m (sapatas corridas)
h_min ≥ 1.50m (tubulões)

Proteção contra erosão:
h_min ≥ 1.00m (próximo a cursos d'água)
```

### 3. NBR 8800:2008 - Projeto de Estruturas de Aço

#### 3.1 Resistências de Cálculo

**Aço Estrutural:**
```
Tipos comuns:
- ASTM A36: f_y = 250 MPa
- ASTM A572 Gr50: f_y = 345 MPa
- ASTM A992: f_y = 345 MPa

Resistência de cálculo:
f_yd = f_y / γ_a1
γ_a1 = 1.10 (escoamento, instabilidade)
γ_a2 = 1.35 (ruptura)
```

#### 3.2 Esbeltez Limite

**Barras Comprimidas:**
```
λ = KL / r ≤ 200

Onde:
K = coeficiente de flambagem
L = comprimento da barra
r = raio de giração mínimo

Esbeltez reduzida:
λ_0 = (KL/r) × √(f_y / E) / π
```

**Barras Tracionadas:**
```
λ ≤ 300 (barras principais)
λ ≤ 400 (barras secundárias)
```

## Eurocodes (Normas Europeias)

### 4. EN 1992 (Eurocode 2) - Estruturas de Concreto

#### 4.1 Classes de Resistência

```
Concreto:
C20/25, C25/30, C30/37, C35/45, C40/50, C45/55, C50/60

Notação: C(f_ck cilindro)/(f_ck cubo)

Exemplo: C30/37
f_ck = 30 MPa (cilindro 150×300mm)
f_ck,cube = 37 MPa (cubo 150×150mm)
```

#### 4.2 Coeficientes Parciais

```
Concreto:
γ_c = 1.5 (situações persistentes)
γ_c = 1.2 (situações acidentais)

Aço:
γ_s = 1.15 (situações persistentes)
γ_s = 1.0 (situações acidentais)
```

### 5. EN 1997 (Eurocode 7) - Projeto Geotécnico

#### 5.1 Abordagens de Projeto

**Approach 1 (Combinação A1+M1+R1 ou A2+M2+R1):**
```
Ações:
γ_G = 1.35 (permanentes desfavoráveis)
γ_Q = 1.50 (variáveis desfavoráveis)

Resistência do solo:
γ_φ = 1.0 (ângulo de atrito)
γ_c = 1.0 (coesão)
```

**Approach 2 (A1+M1+R2):**
```
Resistência estrutural:
γ_R = 1.4 (fundações rasas)
γ_R = 1.1 (estacas em compressão)
```

## Checklist de Conformidade Normativa

### Projeto de Concreto Armado (NBR 6118)

- [ ] Classe de agressividade definida
- [ ] Cobrimento adequado à classe
- [ ] f_ck ≥ 20 MPa (mínimo para estruturas)
- [ ] Armadura mínima atendida
- [ ] Armadura máxima não excedida (4% ou 8%)
- [ ] Espaçamentos entre barras respeitados
- [ ] Flechas dentro dos limites
- [ ] Combinações de ações aplicadas corretamente
- [ ] Ancoragem e emendas dimensionadas

### Projeto de Fundações (NBR 6122)

- [ ] Investigação geotécnica adequada (SPT)
- [ ] Tipo de fundação justificado
- [ ] Fatores de segurança atendidos
- [ ] Recalques estimados e verificados
- [ ] Profundidade mínima respeitada
- [ ] Nível d'água considerado
- [ ] Prova de carga especificada (se aplicável)

### Projeto de Estruturas Metálicas (NBR 8800)

- [ ] Tipo de aço especificado
- [ ] Esbeltez dentro dos limites
- [ ] Ligações dimensionadas
- [ ] Proteção contra corrosão especificada
- [ ] Proteção contra incêndio (se aplicável)
- [ ] Contraventamento adequado

## Tabelas de Referência Rápida

### Cargas Permanentes Típicas (kN/m²)

| Material | Peso Específico |
|----------|-----------------|
| Concreto armado | 25 kN/m³ |
| Alvenaria de tijolo maciço | 18 kN/m³ |
| Alvenaria de bloco cerâmico | 13 kN/m³ |
| Revestimento argamassa (2cm) | 0.40 kN/m² |
| Piso cerâmico | 0.25 kN/m² |
| Forro de gesso | 0.10 kN/m² |

### Cargas Acidentais (NBR 6120) - kN/m²

| Uso | Carga |
|-----|-------|
| Residencial (dormitórios, salas) | 1.5 kN/m² |
| Residencial (despensa, área de serviço) | 2.0 kN/m² |
| Escritórios | 2.0 kN/m² |
| Salas de aula | 3.0 kN/m² |
| Bibliotecas (estantes) | 4.0 kN/m² |
| Garagens (veículos leves) | 3.0 kN/m² |
| Lojas | 4.0 kN/m² |

### Módulos de Elasticidade

```
Concreto (NBR 6118):
E_ci = 5600 × √f_ck  (MPa) - módulo inicial
E_cs = 0.85 × E_ci         - módulo secante

Aço:
E_s = 210.000 MPa (CA-25, CA-50, CA-60)

Aço Estrutural:
E = 200.000 MPa
```

## Referências Normativas Completas

### Normas Brasileiras (ABNT)
- **NBR 6118:2014** - Projeto de estruturas de concreto - Procedimento
- **NBR 6120:2019** - Ações para o cálculo de estruturas de edificações
- **NBR 6122:2019** - Projeto e execução de fundações
- **NBR 6123:1988** - Forças devidas ao vento em edificações
- **NBR 8800:2008** - Projeto de estruturas de aço e de estruturas mistas de aço e concreto de edifícios
- **NBR 14762:2010** - Dimensionamento de estruturas de aço constituídas por perfis formados a frio

### Eurocodes
- **EN 1990** - Basis of structural design
- **EN 1991** - Actions on structures
- **EN 1992** - Design of concrete structures
- **EN 1993** - Design of steel structures
- **EN 1997** - Geotechnical design

## Outputs Esperados

Ao aplicar esta skill, o agente deve:

1. **Identificar norma aplicável** ao elemento/sistema estrutural
2. **Citar artigo/seção específica** da norma
3. **Aplicar coeficientes corretos** (γ_c, γ_s, FS)
4. **Verificar limites normativos** (flechas, esbeltez, armaduras)
5. **Documentar conformidade** em memorial de cálculo
