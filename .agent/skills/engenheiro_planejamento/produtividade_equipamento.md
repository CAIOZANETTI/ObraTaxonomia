---
skill_name: "Produtividade de Equipamentos"
agent: engenheiro_planejamento
category: "Planejamento e Custos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Produtividade de Equipamentos

## Objetivo

Fornecer metodologia para calcular coeficientes de produção horária de equipamentos de construção, estimar ciclos de trabalho e dimensionar frotas para atender cronogramas de obra.

## Fundamentos Teóricos

### 1. Conceitos Básicos

**Produtividade:**
```
Produtividade = Quantidade Produzida / Tempo Gasto
Unidade: m³/h, ton/h, m²/h, etc.
```

**Coeficiente de Produção (RUP - Razão Unitária de Produção):**
```
RUP = Horas de Trabalho / Quantidade Produzida
Unidade: Hh/m³, Hh/ton, Hh/m², etc.

Relação: RUP = 1 / Produtividade
```

**Fatores de Eficiência:**
- **Fator de Operação (FO):** Tempo efetivamente trabalhando / Tempo total disponível
- **Fator de Utilização (FU):** Capacidade real / Capacidade nominal
- **Fator de Eficiência Global (FE):** FO × FU

### 2. Produtividade de Escavadeiras

#### Fórmula Geral

```
Q = (C × N × FE × FV) / T_ciclo

Onde:
Q = Produtividade (m³/h)
C = Capacidade da caçamba (m³)
N = Número de ciclos por hora
FE = Fator de eficiência (0.75 - 0.85 típico)
FV = Fator de volume (empolamento/compactação)
T_ciclo = Tempo de ciclo (min)
```

#### Tempo de Ciclo Típico

| Operação | Tempo de Ciclo (min) |
|----------|----------------------|
| Escavação em solo mole | 0.3 - 0.5 |
| Escavação em solo médio | 0.5 - 0.8 |
| Escavação em rocha fragmentada | 0.8 - 1.2 |
| Carga em caminhão (90° giro) | 0.4 - 0.6 |
| Carga em caminhão (180° giro) | 0.6 - 0.9 |

#### Exemplo de Cálculo

```python
def calcular_produtividade_escavadeira(
    capacidade_cacamba_m3: float,
    tempo_ciclo_min: float,
    fator_eficiencia: float = 0.80,
    fator_volume: float = 1.0
) -> dict:
    """
    Calcula produtividade de escavadeira hidráulica.
    
    Args:
        capacidade_cacamba_m3: Capacidade nominal da caçamba (m³)
        tempo_ciclo_min: Tempo médio de ciclo (minutos)
        fator_eficiencia: FE típico 0.75-0.85
        fator_volume: Fator de empolamento (>1) ou compactação (<1)
    
    Returns:
        dict com produtividade horária e diária
    """
    ciclos_por_hora = 60 / tempo_ciclo_min
    
    prod_horaria = (capacidade_cacamba_m3 * ciclos_por_hora * 
                    fator_eficiencia * fator_volume)
    
    prod_diaria = prod_horaria * 8  # Jornada de 8h
    
    return {
        'produtividade_m3_h': round(prod_horaria, 2),
        'produtividade_m3_dia': round(prod_diaria, 2),
        'ciclos_por_hora': round(ciclos_por_hora, 1),
        'RUP_Hh_m3': round(1 / prod_horaria, 4)
    }

# Exemplo: Escavadeira CAT 320 (caçamba 1.2m³)
resultado = calcular_produtividade_escavadeira(
    capacidade_cacamba_m3=1.2,
    tempo_ciclo_min=0.5,
    fator_eficiencia=0.80
)
# Resultado: ~115 m³/h, ~920 m³/dia
```

### 3. Produtividade de Caminhões Basculantes

#### Fórmula de Ciclo

```
T_ciclo = T_carga + T_ida + T_descarga + T_volta + T_manobras

Onde:
T_carga = Tempo de carregamento (min)
T_ida = Distância / Velocidade_carregado (min)
T_descarga = Tempo de basculamento (min)
T_volta = Distância / Velocidade_vazio (min)
T_manobras = Tempo de posicionamento (min)
```

#### Velocidades Típicas

| Condição da Via | Velocidade Carregado (km/h) | Velocidade Vazio (km/h) |
|-----------------|----------------------------|-------------------------|
| Pavimentada plana | 40-50 | 50-60 |
| Terra batida plana | 25-35 | 35-45 |
| Terra batida rampa 5% | 15-25 | 30-40 |
| Terra batida rampa 10% | 10-15 | 20-30 |

#### Dimensionamento de Frota

```python
def dimensionar_frota_caminhoes(
    volume_total_m3: float,
    capacidade_caminhao_m3: float,
    distancia_km: float,
    velocidade_carregado_kmh: float,
    velocidade_vazio_kmh: float,
    tempo_carga_min: float = 3,
    tempo_descarga_min: float = 2,
    tempo_manobras_min: float = 2,
    jornada_horas: float = 8,
    dias_disponiveis: int = 30
) -> dict:
    """
    Dimensiona frota de caminhões para transporte de material.
    
    Returns:
        dict com número de caminhões necessários e produtividade
    """
    # Tempo de ciclo (minutos)
    tempo_ida_min = (distancia_km / velocidade_carregado_kmh) * 60
    tempo_volta_min = (distancia_km / velocidade_vazio_kmh) * 60
    
    tempo_ciclo_total = (tempo_carga_min + tempo_ida_min + 
                         tempo_descarga_min + tempo_volta_min + 
                         tempo_manobras_min)
    
    # Viagens por dia
    viagens_por_dia = (jornada_horas * 60) / tempo_ciclo_total
    
    # Volume por caminhão por dia
    volume_caminhao_dia = viagens_por_dia * capacidade_caminhao_m3
    
    # Volume total por dia necessário
    volume_necessario_dia = volume_total_m3 / dias_disponiveis
    
    # Número de caminhões
    num_caminhoes = volume_necessario_dia / volume_caminhao_dia
    num_caminhoes_arredondado = int(num_caminhoes) + (1 if num_caminhoes % 1 > 0 else 0)
    
    return {
        'tempo_ciclo_min': round(tempo_ciclo_total, 2),
        'viagens_por_dia': round(viagens_por_dia, 1),
        'volume_caminhao_dia_m3': round(volume_caminhao_dia, 2),
        'num_caminhoes_necessarios': num_caminhoes_arredondado,
        'dias_reais': round(volume_total_m3 / (volume_caminhao_dia * num_caminhoes_arredondado), 1)
    }
```

### 4. Produtividade de Betoneiras e Bombas de Concreto

#### Betoneira Estacionária

```
Produtividade = (Capacidade × Ciclos_hora × FE) / 1000

Capacidade típica: 400L (0.4m³)
Ciclos por hora: 12-15
FE: 0.85
Produtividade: ~5 m³/h
```

#### Bomba de Concreto

| Tipo de Bomba | Vazão Nominal (m³/h) | Vazão Real (m³/h) | Aplicação |
|---------------|----------------------|-------------------|-----------|
| Bomba lança 24m | 60-80 | 40-60 | Lajes, vigas |
| Bomba lança 32m | 80-120 | 60-90 | Edifícios médios |
| Bomba lança 42m | 120-160 | 90-120 | Edifícios altos |
| Bomba estacionária | 30-60 | 25-50 | Fundações, pisos |

**Fator de Eficiência:** 0.70 - 0.80 (inclui paradas, limpeza, ajustes)

### 5. Produtividade de Gruas e Guindastes

#### Tempo de Ciclo

```
T_ciclo = T_içamento + T_translação + T_descida + T_retorno

Componentes:
- Içamento: Altura / Velocidade_içamento
- Translação horizontal: Distância / Velocidade_translação
- Descida: Altura / Velocidade_descida
- Retorno: Distância / Velocidade_retorno
```

#### Velocidades Típicas (Grua Torre)

| Movimento | Velocidade Típica |
|-----------|-------------------|
| Içamento (carga) | 20-40 m/min |
| Descida (carga) | 30-60 m/min |
| Translação lança | 30-50 m/min |
| Rotação | 0.5-1.0 rpm |

### 6. Tabela de Produtividades Referenciais

#### Terraplenagem

| Equipamento | Operação | Produtividade | RUP (Hh/m³) |
|-------------|----------|---------------|-------------|
| Escavadeira CAT 320 | Escavação solo | 100-120 m³/h | 0.008-0.010 |
| Retroescavadeira | Escavação valas | 30-50 m³/h | 0.020-0.033 |
| Trator de esteiras D6 | Espalhamento | 150-200 m³/h | 0.005-0.007 |
| Motoniveladora | Regularização | 300-400 m²/h | 0.0025-0.0033 |
| Rolo compactador | Compactação | 200-300 m³/h | 0.0033-0.005 |

#### Estruturas

| Equipamento | Operação | Produtividade | RUP (Hh/m³) |
|-------------|----------|---------------|-------------|
| Bomba concreto 32m | Lançamento concreto | 60-90 m³/h | 0.011-0.017 |
| Grua torre | Içamento formas | 15-25 ciclos/h | - |
| Vibrador de imersão | Adensamento | 40-60 m³/h | 0.017-0.025 |

### 7. Checklist de Análise de Produtividade

Ao calcular produtividade de equipamentos:

- [ ] Capacidade nominal do equipamento está correta?
- [ ] Tempo de ciclo foi medido ou estimado realisticamente?
- [ ] Fator de eficiência considera paradas, manutenção, clima?
- [ ] Condições do terreno/via foram consideradas?
- [ ] Distâncias de transporte estão corretas?
- [ ] Interferências com outras atividades foram previstas?
- [ ] Disponibilidade de mão de obra de apoio está garantida?
- [ ] Frota dimensionada tem margem de segurança (10-15%)?

### 8. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Memória de Cálculo de Produtividade**
   - Dados de entrada (capacidades, tempos, distâncias)
   - Fórmulas aplicadas
   - Resultados (m³/h, Hh/m³)

2. **Dimensionamento de Frota**
   - Número de equipamentos necessários
   - Justificativa técnica
   - Cronograma de mobilização

3. **Análise de Sensibilidade**
   - Impacto de variações (±10% em tempo de ciclo)
   - Cenários otimista/realista/pessimista

## Referências

- **TCPO - Tabelas de Composições de Preços para Orçamentos** (Editora PINI)
- **Manual de Equipamentos de Terraplenagem** (Caterpillar)
- **NBR 12721** - Avaliação de custos unitários de construção
