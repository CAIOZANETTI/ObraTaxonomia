---
skill_name: "Canteiro de Obras - Instalações Gerais"
agent: engenheiro_custo
category: "Planejamento e Custos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Canteiro de Obras - Instalações Gerais

## Objetivo

Fornecer metodologia para dimensionamento, layout e orçamentação de instalações de canteiro de obras, incluindo escritórios, almoxarifados, oficinas, sanitários, vestiários, refeitórios e alojamentos.

## Tipos de Instalações

### 1. Escritório de Obra

**Dimensionamento:**
```
Área mínima: 6m² por pessoa
Pé-direito: 2.50m mínimo

Ocupação típica:
- Engenheiro residente: 1 pessoa
- Mestre de obras: 1 pessoa
- Administrativo: 1-2 pessoas
- Estagiários: 0-2 pessoas

Área total: 30-50m²
```

**Métodos Construtivos:**

| Método | Custo (R$/m²) | Prazo | Vida Útil | Aplicação |
|--------|---------------|-------|-----------|-----------|
| Container 20' | 800-1.200 | 1 dia | 10 anos | Obras médias/grandes |
| Madeira | 400-600 | 3-5 dias | 2-3 anos | Obras pequenas |
| Metálica (chapas) | 600-900 | 2-3 dias | 5 anos | Obras médias |
| Alvenaria | 1.000-1.500 | 10-15 dias | Permanente | Obras longas |

### 2. Almoxarifado

**Dimensionamento:**
```
Área = 0.5% a 1.0% da área construída

Exemplo:
Obra de 5.000m² → Almoxarifado de 25-50m²

Setorização:
- Materiais elétricos: 20%
- Materiais hidráulicos: 20%
- Ferramentas: 15%
- Materiais de acabamento: 25%
- Diversos: 20%
```

**Especificações:**
- Piso impermeável
- Ventilação adequada
- Prateleiras/estantes
- Controle de acesso
- Extintor de incêndio

### 3. Sanitários e Vestiários

**NR-18 - Requisitos Mínimos:**

```python
def dimensionar_sanitarios_nr18(num_trabalhadores: int) -> dict:
    """
    Dimensiona sanitários conforme NR-18.
    
    NR-18.4.2.3:
    - Até 20 trabalhadores: 1 conjunto (vaso, lavatório, chuveiro)
    - 20 a 100: 1 conjunto para cada 20
    - Acima de 100: 1 conjunto para cada 30
    """
    if num_trabalhadores <= 20:
        conjuntos = 1
    elif num_trabalhadores <= 100:
        conjuntos = (num_trabalhadores // 20) + (1 if num_trabalhadores % 20 > 0 else 0)
    else:
        conjuntos_ate_100 = 5  # 100/20
        restante = num_trabalhadores - 100
        conjuntos_acima_100 = (restante // 30) + (1 if restante % 30 > 0 else 0)
        conjuntos = conjuntos_ate_100 + conjuntos_acima_100
    
    # Área mínima por conjunto: 6m²
    area_total = conjuntos * 6
    
    return {
        'num_trabalhadores': num_trabalhadores,
        'conjuntos_necessarios': conjuntos,
        'vasos_sanitarios': conjuntos,
        'lavatorios': conjuntos,
        'chuveiros': conjuntos,
        'area_minima_m2': area_total,
        'custo_estimado': conjuntos * 3000  # R$ 3.000 por conjunto
    }
```

### 4. Refeitório

**Dimensionamento NR-24:**
```
Área mínima: 1m² por usuário
Pé-direito: 2.80m mínimo

Equipamentos:
- Mesas e bancos (0.60m por pessoa)
- Bebedouro (1 para cada 25 trabalhadores)
- Aquecedor de refeições
- Lavatório para higienização

Capacidade:
- Considerar 50% dos trabalhadores por turno
- Exemplo: 100 trabalhadores → Refeitório para 50 pessoas → 50m²
```

### 5. Alojamento

**NR-18.4.3 - Requisitos:**
```
Área mínima por cama: 3m²
Pé-direito: 2.50m mínimo
Camas: Beliche permitido (máx. 2 níveis)
Distância entre camas: 1.00m mínimo
Armários individuais obrigatórios

Capacidade por ambiente:
- Máximo: 100 pessoas por dormitório
- Recomendado: 8-12 pessoas por quarto
```

**Custo de Implantação:**

| Tipo | Capacidade | Custo Total (R$) | Custo/Pessoa (R$) |
|------|------------|------------------|-------------------|
| Container habitável | 8-12 | 15.000-25.000 | 1.500-2.500 |
| Madeira | 10-15 | 8.000-15.000 | 800-1.000 |
| Alvenaria | 20-30 | 30.000-50.000 | 1.200-1.800 |

### 6. Guarita e Portaria

**Dimensionamento:**
```
Área: 4-6m²
Equipamentos:
- Livro de registro
- Telefone/interfone
- Iluminação
- Cadeira/mesa

Custo: R$ 2.000-4.000
```

## Layout de Canteiro

### Princípios de Layout

```
1. Proximidade:
   - Almoxarifado próximo ao acesso principal
   - Escritório com visão geral da obra
   - Sanitários próximos às frentes de trabalho

2. Fluxo:
   - Entrada de materiais separada da saída de entulho
   - Circulação livre de equipamentos
   - Evitar cruzamento de fluxos

3. Segurança:
   - Áreas de vivência isoladas de áreas de risco
   - Saídas de emergência sinalizadas
   - Extintores acessíveis

4. Flexibilidade:
   - Instalações móveis (containers)
   - Possibilidade de expansão
   - Adaptação conforme fases da obra
```

### Exemplo de Layout

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │ Escritório│    │Almoxarifado│  │ Oficina  │     │
│  │  (30m²)  │    │  (40m²)   │    │  (20m²)  │     │
│  └──────────┘    └──────────┘    └──────────┘     │
│                                                     │
│  ┌──────────┐    ┌──────────┐                     │
│  │Sanitários│    │Refeitório│                     │
│  │  (12m²)  │    │  (50m²)  │                     │
│  └──────────┘    └──────────┘                     │
│                                                     │
│  ┌─────────────────────────┐                      │
│  │   Área de Estocagem     │                      │
│  │   (Areia, Brita, etc)   │                      │
│  └─────────────────────────┘                      │
│                                                     │
│  PORTÃO DE ACESSO                                  │
└─────────────────────────────────────────────────────┘
```

## Orçamento de Canteiro

```python
def orcamento_canteiro_obras(
    num_trabalhadores: int,
    duracao_meses: int,
    necessita_alojamento: bool = False
) -> dict:
    """
    Orça instalações de canteiro de obras.
    """
    # Escritório (container 20')
    custo_escritorio = 18000  # Compra
    custo_escritorio_mensal = custo_escritorio / duracao_meses
    
    # Almoxarifado (container 20')
    custo_almoxarifado = 15000
    custo_almoxarifado_mensal = custo_almoxarifado / duracao_meses
    
    # Sanitários
    sanitarios = dimensionar_sanitarios_nr18(num_trabalhadores)
    custo_sanitarios = sanitarios['custo_estimado']
    custo_sanitarios_mensal = custo_sanitarios / duracao_meses
    
    # Refeitório
    capacidade_refeitorio = num_trabalhadores // 2
    area_refeitorio = capacidade_refeitorio * 1  # 1m²/pessoa
    custo_refeitorio = area_refeitorio * 800  # R$ 800/m²
    custo_refeitorio_mensal = custo_refeitorio / duracao_meses
    
    # Alojamento (se necessário)
    if necessita_alojamento:
        num_containers_aloj = (num_trabalhadores // 10) + 1
        custo_alojamento = num_containers_aloj * 20000
        custo_alojamento_mensal = custo_alojamento / duracao_meses
    else:
        custo_alojamento = 0
        custo_alojamento_mensal = 0
    
    # Guarita
    custo_guarita = 3000
    custo_guarita_mensal = custo_guarita / duracao_meses
    
    # Ligações provisórias
    custo_agua = 1500  # Instalação
    custo_energia = 3000  # Instalação + padrão
    custo_utilidades = custo_agua + custo_energia
    custo_utilidades_mensal = custo_utilidades / duracao_meses
    
    # Consumo mensal
    consumo_agua_mensal = num_trabalhadores * 30  # R$ 30/pessoa
    consumo_energia_mensal = 1500  # Fixo
    
    # Total
    custo_implantacao = (custo_escritorio + custo_almoxarifado + 
                         custo_sanitarios + custo_refeitorio + 
                         custo_alojamento + custo_guarita + custo_utilidades)
    
    custo_mensal = (custo_escritorio_mensal + custo_almoxarifado_mensal + 
                    custo_sanitarios_mensal + custo_refeitorio_mensal + 
                    custo_alojamento_mensal + custo_guarita_mensal + 
                    custo_utilidades_mensal + consumo_agua_mensal + 
                    consumo_energia_mensal)
    
    custo_total = custo_mensal * duracao_meses
    
    return {
        'num_trabalhadores': num_trabalhadores,
        'duracao_meses': duracao_meses,
        'custo_implantacao': round(custo_implantacao, 2),
        'custo_mensal': round(custo_mensal, 2),
        'custo_total': round(custo_total, 2),
        'custo_por_trabalhador_mes': round(custo_mensal / num_trabalhadores, 2)
    }
```

## Outputs Esperados

1. **Layout de Canteiro**
   - Planta baixa com posicionamento
   - Áreas dimensionadas
   - Fluxos de circulação

2. **Orçamento Detalhado**
   - Custo de implantação
   - Custo mensal de manutenção
   - Custo total

3. **Especificações Técnicas**
   - Métodos construtivos
   - Materiais
   - Equipamentos

## Referências

- **NR-18** - Condições de segurança no trabalho na indústria da construção
- **NR-24** - Condições sanitárias e de conforto nos locais de trabalho
