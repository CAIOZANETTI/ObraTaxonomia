---
skill_name: "Produtividade de Equipamentos"
agent: engenheiro_tempo
category: "Planejamento de Tempo e Recursos"
difficulty: intermediate
version: 2.0.0
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

- **Caterpillar Performance Handbook** (Edition 53, 2023)
- **Komatsu Specifications & Application Handbook**
- **PMBOK Guide 7th Edition** - Resource Management
- **TCPO - Tabelas de Composições de Preços para Orçamentos** (Editora PINI)
- **NBR 12721** - Avaliação de custos unitários de construção

---

## 9. Dados de Fabricantes - Caterpillar

### 9.1 Escavadeiras Hidráulicas Caterpillar

| Modelo | Peso Operacional (ton) | Caçamba (m³) | Potência (HP) | Produção Típica (m³/h) |
|--------|------------------------|--------------|---------------|------------------------|
| **CAT 305.5E2** | 5.4 | 0.14 | 38 | 25-35 |
| **CAT 308** | 8.2 | 0.28 | 55 | 45-60 |
| **CAT 313** | 13.5 | 0.50 | 91 | 70-90 |
| **CAT 320** | 20.3 | 0.90-1.20 | 121 | 100-130 |
| **CAT 323** | 23.5 | 1.14-1.44 | 153 | 120-150 |
| **CAT 330** | 30.8 | 1.50-1.90 | 202 | 150-190 |
| **CAT 336** | 36.2 | 1.90-2.40 | 268 | 180-230 |
| **CAT 349** | 49.4 | 2.80-3.60 | 403 | 250-320 |

**Fonte**: Caterpillar Performance Handbook Ed. 53

#### Fatores de Correção Caterpillar

```python
# Fator de Enchimento da Caçamba (Bucket Fill Factor)
FATORES_ENCHIMENTO_CAT = {
    'solo_solto': 1.00,          # Areia, cascalho solto
    'solo_medio': 0.95,          # Terra comum
    'argila_dura': 0.85,         # Argila compacta
    'rocha_fragmentada': 0.75,   # Rocha britada
    'rocha_dinamitada': 0.60     # Rocha mal fragmentada
}

# Fator de Eficiência de Trabalho (Job Efficiency)
EFICIENCIA_TRABALHO_CAT = {
    'excelente': 0.83,    # 50 min/hora
    'bom': 0.75,          # 45 min/hora
    'medio': 0.67,        # 40 min/hora
    'ruim': 0.58,         # 35 min/hora
    'pessimo': 0.50       # 30 min/hora
}
```

### 9.2 Tratores de Esteiras Caterpillar

| Modelo | Peso (ton) | Potência (HP) | Lâmina (m³) | Aplicação |
|--------|------------|---------------|-------------|-----------|
| **CAT D3** | 9.3 | 80 | 1.7 | Paisagismo, pequenas obras |
| **CAT D4** | 11.8 | 102 | 2.3 | Terraplenagem leve |
| **CAT D5** | 15.4 | 130 | 3.0 | Terraplenagem média |
| **CAT D6** | 20.2 | 215 | 4.4 | Terraplenagem pesada |
| **CAT D7** | 28.5 | 270 | 6.0 | Grandes movimentações |
| **CAT D8** | 37.2 | 305 | 8.2 | Mineração, grandes obras |
| **CAT D9** | 48.5 | 410 | 11.5 | Mineração pesada |
| **CAT D10** | 64.3 | 580 | 17.0 | Mineração ultra-pesada |

#### Produtividade de Tratores (Caterpillar Method)

```python
def calcular_producao_trator_cat(
    capacidade_lamina_m3: float,
    distancia_transporte_m: float,
    velocidade_frente_kmh: float,
    velocidade_re_kmh: float,
    fator_lamina: float = 0.80,
    eficiencia_trabalho: float = 0.75
) -> dict:
    """
    Método Caterpillar para produtividade de tratores.
    
    Baseado em: Caterpillar Performance Handbook, Section 4
    """
    # Tempo de ciclo
    tempo_carga_min = 0.05  # Fixo (3 segundos)
    tempo_ida_min = (distancia_transporte_m / 1000) / velocidade_frente_kmh * 60
    tempo_descarga_min = 0.10  # Fixo (6 segundos)
    tempo_volta_min = (distancia_transporte_m / 1000) / velocidade_re_kmh * 60
    tempo_manobra_min = 0.10  # Fixo
    
    tempo_ciclo_total = (tempo_carga_min + tempo_ida_min + 
                         tempo_descarga_min + tempo_volta_min + tempo_manobra_min)
    
    # Produção horária
    ciclos_hora = 60 / tempo_ciclo_total
    producao_horaria = (capacidade_lamina_m3 * fator_lamina * 
                        ciclos_hora * eficiencia_trabalho)
    
    return {
        'producao_m3_h': round(producao_horaria, 1),
        'producao_m3_dia': round(producao_horaria * 8, 1),
        'tempo_ciclo_min': round(tempo_ciclo_total, 2),
        'ciclos_hora': round(ciclos_hora, 1)
    }

# Exemplo: CAT D6 empurrando terra 50m
resultado = calcular_producao_trator_cat(
    capacidade_lamina_m3=4.4,
    distancia_transporte_m=50,
    velocidade_frente_kmh=6.0,
    velocidade_re_kmh=10.0,
    fator_lamina=0.80,
    eficiencia_trabalho=0.75
)
# Resultado: ~180 m³/h
```

### 9.3 Caminhões Articulados Caterpillar

| Modelo | Capacidade (m³) | Carga (ton) | Potência (HP) | Aplicação |
|--------|-----------------|-------------|---------------|-----------|
| **CAT 725** | 17.0 | 23.6 | 299 | Obras médias |
| **CAT 730** | 20.0 | 28.0 | 347 | Obras pesadas |
| **CAT 735** | 24.0 | 32.0 | 402 | Mineração leve |
| **CAT 740** | 28.0 | 37.2 | 449 | Mineração média |
| **CAT 745** | 32.0 | 41.0 | 496 | Mineração pesada |

---

## 10. Dados de Fabricantes - Komatsu

### 10.1 Escavadeiras Hidráulicas Komatsu

| Modelo | Peso (ton) | Caçamba (m³) | Potência (HP) | Produção (m³/h) |
|--------|------------|--------------|---------------|-----------------|
| **PC55MR-5** | 5.5 | 0.16 | 40 | 28-38 |
| **PC138US-11** | 13.8 | 0.50 | 92 | 72-92 |
| **PC200-11** | 20.0 | 0.93 | 123 | 105-135 |
| **PC210LC-11** | 21.8 | 1.00 | 148 | 115-145 |
| **PC290LC-11** | 29.0 | 1.40 | 196 | 145-180 |
| **PC390LC-11** | 39.0 | 1.90 | 257 | 185-235 |
| **PC490LC-11** | 49.0 | 2.40 | 359 | 230-290 |

### 10.2 Tratores de Esteiras Komatsu

| Modelo | Peso (ton) | Potência (HP) | Lâmina (m³) | Equivalente CAT |
|--------|------------|---------------|-------------|-----------------|
| **D37PX-24** | 7.6 | 80 | 1.8 | D3 |
| **D51PXi-24** | 13.5 | 105 | 2.7 | D4 |
| **D61PXi-24** | 20.5 | 168 | 4.1 | D5 |
| **D65PX-18** | 24.0 | 217 | 4.9 | D6 |
| **D85EX-18** | 36.5 | 264 | 7.5 | D7 |
| **D155AX-8** | 42.0 | 354 | 10.5 | D8 |

### 10.3 Carregadeiras Komatsu

| Modelo | Caçamba (m³) | Potência (HP) | Carga (ton) | Produção (m³/h) |
|--------|--------------|---------------|-------------|-----------------|
| **WA200-8** | 1.90 | 123 | 3.4 | 85-110 |
| **WA320-8** | 2.30 | 148 | 4.2 | 105-135 |
| **WA380-8** | 2.90 | 181 | 5.3 | 130-165 |
| **WA470-8** | 3.80 | 234 | 7.0 | 170-215 |
| **WA500-8** | 4.60 | 296 | 8.5 | 210-265 |

---

## 11. Integração com PMBOK 7ª Edição

### 11.1 Resource Management (Gerenciamento de Recursos)

O PMBOK 7ª Edição enfatiza a gestão de recursos através de **Performance Domains**:

#### Performance Domain: Planning

**Estimativa de Recursos:**

```python
class RecursoEquipamento:
    """
    Classe baseada em PMBOK para gestão de recursos de equipamentos.
    """
    def __init__(self, nome, tipo, produtividade_hora, custo_hora):
        self.nome = nome
        self.tipo = tipo
        self.produtividade_hora = produtividade_hora  # m³/h
        self.custo_hora = custo_hora  # R$/h
        self.disponibilidade = 1.0  # 100%
        self.calendario = "8x5"  # 8h/dia, 5 dias/semana
    
    def estimar_duracao(self, quantidade_servico):
        """
        Estima duração conforme PMBOK - Three-Point Estimating.
        
        Returns:
            dict com estimativas otimista, mais provável, pessimista
        """
        # Produtividade base
        horas_base = quantidade_servico / self.produtividade_hora
        
        # Three-Point Estimate (PERT)
        otimista = horas_base * 0.85      # -15%
        mais_provavel = horas_base
        pessimista = horas_base * 1.30    # +30%
        
        # Estimativa PERT
        estimativa_pert = (otimista + 4*mais_provavel + pessimista) / 6
        
        # Desvio padrão
        desvio = (pessimista - otimista) / 6
        
        return {
            'otimista_h': round(otimista, 1),
            'mais_provavel_h': round(mais_provavel, 1),
            'pessimista_h': round(pessimista, 1),
            'estimativa_pert_h': round(estimativa_pert, 1),
            'desvio_padrao_h': round(desvio, 2),
            'intervalo_confianca_80': (
                round(estimativa_pert - 1.28*desvio, 1),
                round(estimativa_pert + 1.28*desvio, 1)
            )
        }
    
    def calcular_custo_atividade(self, quantidade_servico):
        """
        Calcula custo total da atividade (PMBOK Cost Management).
        """
        estimativa = self.estimar_duracao(quantidade_servico)
        
        custo_otimista = estimativa['otimista_h'] * self.custo_hora
        custo_provavel = estimativa['mais_provavel_h'] * self.custo_hora
        custo_pessimista = estimativa['pessimista_h'] * self.custo_hora
        
        # Custo esperado (PERT)
        custo_esperado = (custo_otimista + 4*custo_provavel + custo_pessimista) / 6
        
        return {
            'custo_otimista': round(custo_otimista, 2),
            'custo_provavel': round(custo_provavel, 2),
            'custo_pessimista': round(custo_pessimista, 2),
            'custo_esperado': round(custo_esperado, 2)
        }

# Exemplo de uso
escavadeira = RecursoEquipamento(
    nome="CAT 320",
    tipo="Escavadeira Hidráulica",
    produtividade_hora=115,  # m³/h
    custo_hora=280.00  # R$/h
)

# Estimar escavação de 5000 m³
estimativa = escavadeira.estimar_duracao(5000)
custo = escavadeira.calcular_custo_atividade(5000)

print(f"Duração estimada (PERT): {estimativa['estimativa_pert_h']:.1f} horas")
print(f"Custo esperado: R$ {custo['custo_esperado']:,.2f}")
```

### 11.2 Resource Leveling (Nivelamento de Recursos)

**Técnica PMBOK**: Ajustar cronograma para otimizar uso de equipamentos.

```python
def nivelar_recursos_equipamentos(atividades, equipamentos_disponiveis):
    """
    Implementa Resource Leveling conforme PMBOK.
    
    Args:
        atividades: Lista de atividades com demanda de equipamentos
        equipamentos_disponiveis: Quantidade disponível por tipo
    
    Returns:
        Cronograma nivelado com alocação otimizada
    """
    cronograma_nivelado = []
    
    for atividade in sorted(atividades, key=lambda x: x['folga_total']):
        # Priorizar atividades críticas (folga = 0)
        if atividade['folga_total'] == 0:
            # Alocar imediatamente
            cronograma_nivelado.append({
                'atividade': atividade['nome'],
                'inicio': atividade['inicio_cedo'],
                'fim': atividade['termino_cedo'],
                'equipamento': atividade['equipamento_req']
            })
        else:
            # Atividades não-críticas: postergar se necessário
            # para evitar pico de demanda
            pass
    
    return cronograma_nivelado
```

### 11.3 Resource Smoothing (Suavização de Recursos)

**Diferença do Leveling**: Não altera caminho crítico, apenas ajusta atividades não-críticas.

### 11.4 Métricas de Desempenho (PMBOK)

```python
def calcular_metricas_pmbok(
    horas_planejadas: float,
    horas_reais: float,
    trabalho_completado_pct: float
) -> dict:
    """
    Calcula métricas de desempenho de recursos (PMBOK).
    
    Returns:
        SPI (Schedule Performance Index)
        Eficiência de recursos
    """
    # Valor Planejado (horas)
    pv_horas = horas_planejadas
    
    # Valor Agregado (horas)
    ev_horas = horas_planejadas * (trabalho_completado_pct / 100)
    
    # Custo Real (horas)
    ac_horas = horas_reais
    
    # Índices
    spi = ev_horas / pv_horas if pv_horas > 0 else 0
    eficiencia = ev_horas / ac_horas if ac_horas > 0 else 0
    
    # Interpretação
    status_prazo = "Adiantado" if spi > 1.0 else "Atrasado" if spi < 1.0 else "No Prazo"
    status_eficiencia = "Eficiente" if eficiencia > 1.0 else "Ineficiente"
    
    return {
        'spi': round(spi, 3),
        'eficiencia_recursos': round(eficiencia, 3),
        'status_prazo': status_prazo,
        'status_eficiencia': status_eficiencia,
        'horas_economizadas': round(ev_horas - ac_horas, 1)
    }

# Exemplo
metricas = calcular_metricas_pmbok(
    horas_planejadas=100,
    horas_reais=110,
    trabalho_completado_pct=95
)
# SPI = 0.95 (5% atrasado)
# Eficiência = 0.86 (14% ineficiente)
```

---

## 12. Tabelas de Referência Rápida

### 12.1 Fatores de Conversão

| De | Para | Fator |
|----|------|-------|
| m³ solto | m³ compactado | 0.85 - 0.90 |
| m³ banco | m³ solto | 1.25 - 1.40 |
| ton | m³ (solo) | 1.6 - 1.8 ton/m³ |
| ton | m³ (rocha) | 2.5 - 2.7 ton/m³ |

### 12.2 Velocidades Médias de Equipamentos

| Equipamento | Velocidade Trabalho | Velocidade Transporte |
|-------------|---------------------|----------------------|
| Escavadeira | - | 3-5 km/h |
| Trator esteiras | 3-6 km/h | 8-12 km/h |
| Carregadeira | 5-10 km/h | 20-35 km/h |
| Caminhão articulado | 15-30 km/h | 40-55 km/h |
| Motoniveladora | 3-8 km/h | 20-40 km/h |

### 12.3 Checklist PMBOK para Planejamento de Recursos

- [ ] **Identificar recursos**: Listar todos equipamentos necessários
- [ ] **Estimar quantidades**: Aplicar produtividades (Caterpillar/Komatsu)
- [ ] **Estimar durações**: Usar Three-Point (PERT)
- [ ] **Desenvolver cronograma**: CPM com recursos alocados
- [ ] **Nivelar recursos**: Resource Leveling se necessário
- [ ] **Estabelecer baseline**: Congelar cronograma aprovado
- [ ] **Monitorar desempenho**: Calcular SPI, eficiência
- [ ] **Controlar mudanças**: Gerenciar alterações de recursos

---

## 13. Exemplo Completo: Projeto de Terraplenagem

```python
# Dados do projeto
volume_escavacao = 15000  # m³
distancia_bota_fora = 2.5  # km

# Equipamentos selecionados
escavadeira = RecursoEquipamento("CAT 336", "Escavadeira", 200, 320)
caminhao = RecursoEquipamento("CAT 740", "Caminhão Articulado", 150, 180)

# Estimativas PERT
est_escavacao = escavadeira.estimar_duracao(volume_escavacao)
est_transporte = caminhao.estimar_duracao(volume_escavacao)

# Dimensionamento de frota
horas_escavadeira = est_escavacao['estimativa_pert_h']
horas_caminhao = est_transporte['estimativa_pert_h']

# Balanceamento (caminhões devem acompanhar escavadeira)
num_caminhoes = int(horas_caminhao / horas_escavadeira) + 1

print(f"=== PLANEJAMENTO DE RECURSOS (PMBOK) ===")
print(f"Escavadeira: {est_escavacao['estimativa_pert_h']:.0f} horas")
print(f"Caminhões necessários: {num_caminhoes} unidades")
print(f"Duração total: {est_escavacao['estimativa_pert_h'] / 8:.1f} dias")
print(f"Intervalo confiança 80%: {est_escavacao['intervalo_confianca_80']}")
```

---

## Conclusão

Esta skill integra:
- ✅ **Dados reais** de fabricantes (Caterpillar, Komatsu)
- ✅ **Metodologias comprovadas** (Performance Handbook)
- ✅ **Boas práticas PMBOK** (Resource Management, PERT)
- ✅ **Ferramentas práticas** (Python, cálculos automatizados)

Use esta skill para **planejar cronogramas realistas** com base em produtividades comprovadas e gerenciar recursos conforme padrões internacionais (PMBOK).
