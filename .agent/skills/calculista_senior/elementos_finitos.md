---
skill_name: "Elementos Finitos - Modelagem e Análise"
agent: calculista_senior
category: "Análise Estrutural Numérica"
difficulty: expert
version: 1.0.0
---

# Skill: Elementos Finitos (FEM)

## Objetivo

Fornecer diretrizes para modelagem, discretização de malha e interpretação de resultados em análises por Elementos Finitos (FEM) aplicadas a estruturas civis.

## Fundamentos de Modelagem

### 1. Tipos de Elementos

#### Elementos de Barra (1D)
**Aplicação:**
- Vigas, pilares, treliças
- Estruturas reticuladas
- Análise linear de pórticos

**Graus de Liberdade:**
- 6 GDL por nó (3 translações + 3 rotações)

**Quando usar:**
- Relação comprimento/altura > 5
- Comportamento predominantemente unidimensional
- Análise de esforços internos (M, N, V)

**Limitações:**
- Não captura distribuição de tensões na seção
- Inadequado para regiões de descontinuidade (apoios, cargas concentradas)

```python
# Exemplo: Elemento de viga Euler-Bernoulli
class ElementoViga:
    """
    Elemento de viga com 4 GDL (2 nós × 2 GDL/nó).
    
    Attributes:
        L: Comprimento do elemento (m)
        E: Módulo de elasticidade (kPa)
        I: Momento de inércia (m⁴)
    """
    def __init__(self, L: float, E: float, I: float):
        self.L = L
        self.E = E
        self.I = I
    
    def matriz_rigidez(self) -> np.ndarray:
        """Matriz de rigidez local 4×4."""
        k = (self.E * self.I) / (self.L ** 3)
        K = k * np.array([
            [ 12,   6*self.L,  -12,   6*self.L],
            [ 6*self.L,  4*self.L**2, -6*self.L,  2*self.L**2],
            [-12,  -6*self.L,   12,  -6*self.L],
            [ 6*self.L,  2*self.L**2, -6*self.L,  4*self.L**2]
        ])
        return K
```

#### Elementos de Casca (2D)
**Aplicação:**
- Lajes, paredes, reservatórios
- Estruturas laminares
- Análise de placas e cascas

**Graus de Liberdade:**
- 6 GDL por nó (membrana + flexão)

**Quando usar:**
- Espessura << dimensões em planta
- Distribuição de tensões na espessura é relevante
- Análise de lajes com geometria complexa

**Tipos:**
- **Casca fina (Kirchhoff):** Espessura < L/20
- **Casca espessa (Mindlin-Reissner):** Espessura ≥ L/20 (considera deformação por cisalhamento)

#### Elementos Sólidos (3D)
**Aplicação:**
- Blocos de fundação, consolos
- Regiões de descontinuidade (nós de pórtico)
- Análise de tensões localizadas

**Graus de Liberdade:**
- 3 GDL por nó (translações)

**Quando usar:**
- Geometria tridimensional complexa
- Distribuição de tensões em 3D é crítica
- Verificação de tensões principais e cisalhamento

**Tipos:**
- **Tetraédrico (4 nós):** Malha automática, menos preciso
- **Hexaédrico (8 nós):** Malha estruturada, mais preciso

### 2. Discretização de Malha

#### Princípios Fundamentais

**Regra Geral:**
```
Refinamento de malha ∝ Gradiente de tensões esperado
```

**Critérios de Qualidade:**
- **Razão de aspecto:** < 3:1 (ideal), < 5:1 (aceitável)
- **Ângulo interno:** 45° a 135° (triângulos), 60° a 120° (quadriláteros)
- **Distorção:** < 0.6 (Jacobiano)

#### Estratégias de Refinamento

**1. Refinamento Uniforme**
```
Aplicação: Análise preliminar, geometria simples
Vantagem: Fácil implementação
Desvantagem: Custo computacional elevado
```

**2. Refinamento Adaptativo (h-refinement)**
```
Aplicação: Concentração de tensões, singularidades
Estratégia: Refinar onde erro estimado > tolerância
```

**3. Refinamento por Ordem (p-refinement)**
```
Aplicação: Aumentar precisão sem aumentar nós
Estratégia: Usar elementos de ordem superior (quadráticos, cúbicos)
```

#### Tamanho de Elemento Recomendado

| Região                  | Tamanho Máximo de Elemento |
|-------------------------|----------------------------|
| Região de interesse     | L / 20                     |
| Concentração de tensões | L / 40                     |
| Região remota           | L / 5                      |
| Apoios e cargas         | L / 30                     |

**Exemplo: Laje 6m × 6m**
```
Região central:     elemento ≤ 0.30m
Próximo a apoios:   elemento ≤ 0.15m
Região de carga:    elemento ≤ 0.20m
```

### 3. Verificação de Convergência

#### Teste de Convergência de Malha

**Procedimento:**
1. Modelar com malha grosseira (M1)
2. Refinar malha (M2: 2× mais elementos)
3. Refinar novamente (M3: 4× mais elementos que M1)
4. Comparar resultados de interesse (tensões, deslocamentos)

**Critério de Convergência:**
```
Erro relativo = |Resultado_M3 - Resultado_M2| / Resultado_M3 < 5%
```

**Exemplo de Código:**

```python
def verificar_convergencia_malha(
    modelo_base: str,
    parametro_interesse: str,
    num_refinamentos: int = 3
) -> dict:
    """
    Executa análise de convergência de malha.
    
    Args:
        modelo_base: Caminho do arquivo de modelo FEM
        parametro_interesse: 'tensao_maxima', 'deslocamento_maximo', etc.
        num_refinamentos: Número de níveis de refinamento
    
    Returns:
        dict com resultados e taxa de convergência
    """
    resultados = []
    num_elementos = []
    
    for i in range(num_refinamentos):
        fator_refinamento = 2 ** i
        malha = gerar_malha(modelo_base, fator_refinamento)
        resultado = executar_analise(malha)
        
        resultados.append(resultado[parametro_interesse])
        num_elementos.append(malha.num_elementos)
    
    # Calcular erro relativo entre últimos dois refinamentos
    erro_relativo = abs(resultados[-1] - resultados[-2]) / resultados[-1]
    
    convergiu = erro_relativo < 0.05  # 5%
    
    return {
        'resultados': resultados,
        'num_elementos': num_elementos,
        'erro_relativo_pct': erro_relativo * 100,
        'convergiu': convergiu,
        'recomendacao': 'Malha adequada' if convergiu else 'Refinar mais'
    }
```

### 4. Condições de Contorno

#### Tipos de Apoio

**Apoio Simples (Pino):**
```
Restrições: Tx = 0, Ty = 0
Liberdades: Rz ≠ 0
```

**Apoio Duplo (Engaste):**
```
Restrições: Tx = 0, Ty = 0, Rz = 0
Liberdades: Nenhuma
```

**Apoio Elástico (Mola):**
```
Rigidez: k (kN/m)
Relação: F = k × δ
```

#### Modelagem de Apoios em FEM

**Regra de Ouro:**
```
Evitar restrições pontuais em modelos sólidos
→ Usar regiões de apoio distribuídas
```

**Exemplo:**
```
❌ Errado: Restringir 1 nó de laje
✅ Correto: Restringir área equivalente ao pilar (30cm × 30cm)
```

### 5. Interpretação de Resultados

#### Tensões Principais

**Critério de Falha (Concreto):**
```
σ1 (tração) < f_ctk,sup  (NBR 6118)
σ3 (compressão) < f_cd
```

**Critério de von Mises (Aço):**
```
σ_vm = √(σ1² - σ1·σ2 + σ2²) < f_yd
```

#### Deslocamentos

**Limites NBR 6118:**
```
Flechas em vigas:
- Imediata: L / 250
- Total: L / 350 (com contra-flecha)

Deslocamento horizontal (edifícios):
- Entre pavimentos: H / 500
- Total: H_total / 1700
```

#### Reações de Apoio

**Verificação de Equilíbrio:**
```
∑Fz = 0  (vertical)
∑Fx = 0  (horizontal)
∑M = 0   (momentos)
```

**Tolerância:**
```
Erro de equilíbrio < 0.1% das cargas aplicadas
```

### 6. Checklist de Modelagem FEM

#### Pré-Processamento
- [ ] Tipo de elemento adequado ao problema
- [ ] Propriedades de material corretas (E, ν, γ)
- [ ] Malha com razão de aspecto < 5:1
- [ ] Refinamento em regiões críticas
- [ ] Condições de contorno realistas
- [ ] Cargas aplicadas corretamente (distribuídas vs. concentradas)

#### Processamento
- [ ] Convergência de solução alcançada
- [ ] Tempo de processamento razoável (< 10 min para modelos médios)
- [ ] Mensagens de erro ou warning verificadas

#### Pós-Processamento
- [ ] Verificar equilíbrio global (∑F = 0, ∑M = 0)
- [ ] Deslocamentos coerentes com carregamento
- [ ] Tensões dentro de limites normativos
- [ ] Deformada visual coerente
- [ ] Convergência de malha verificada

### 7. Boas Práticas

#### Simplificações Aceitáveis
✅ **Permitido:**
- Simetria (reduzir modelo pela metade)
- Linearidade elástica (cargas de serviço)
- Seções homogeneizadas (concreto armado → concreto equivalente)

❌ **Evitar:**
- Malha muito grosseira (< 3 elementos por dimensão característica)
- Elementos distorcidos (ângulos < 30° ou > 150°)
- Apoios pontuais em modelos sólidos

#### Validação de Modelo

**Comparar com:**
1. Solução analítica (casos simples: viga bi-apoiada)
2. Tabelas de engenharia (Roark, Timoshenko)
3. Ordem de grandeza esperada

**Exemplo:**
```
Viga bi-apoiada L=6m, q=10kN/m
Flecha analítica: δ = 5qL⁴/(384EI)

Se FEM divergir > 10% → revisar modelo
```

### 8. Softwares Recomendados

| Software      | Tipo          | Aplicação Principal           |
|---------------|---------------|-------------------------------|
| SAP2000       | Comercial     | Pórticos, edifícios           |
| ANSYS         | Comercial     | Análise avançada, não-linear  |
| Abaqus        | Comercial     | Simulação complexa            |
| RFEM          | Comercial     | Estruturas 3D, cascas         |
| Code_Aster    | Open-source   | Análise geral                 |
| CalculiX      | Open-source   | Pré/pós-processamento         |

### 9. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Relatório de Modelagem**
   - Justificativa do tipo de elemento
   - Estratégia de discretização
   - Propriedades de material

2. **Estudo de Convergência**
   - Gráfico: Resultado vs. Número de elementos
   - Erro relativo calculado
   - Recomendação de malha final

3. **Resultados Críticos**
   - Tensões máximas (tração e compressão)
   - Deslocamentos máximos
   - Reações de apoio

4. **Validação**
   - Comparação com solução analítica (se disponível)
   - Verificação de equilíbrio global
   - Análise de sensibilidade

### 10. Referências

- **Zienkiewicz, O.C.** - The Finite Element Method (7th ed.)
- **Cook, R.D.** - Concepts and Applications of Finite Element Analysis
- **NBR 6118:2014** - Projeto de estruturas de concreto
- **Bathe, K.J.** - Finite Element Procedures
