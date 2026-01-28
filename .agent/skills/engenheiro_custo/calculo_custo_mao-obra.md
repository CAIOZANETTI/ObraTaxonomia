---
skill_name: "Cálculo de Custo de Mão de Obra"
agent: engenheiro_custo
category: "Orçamentação e Custos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Cálculo de Custo de Mão de Obra

## Objetivo

Fornecer metodologia detalhada para cálculo do custo total de mão de obra, incluindo salários, encargos sociais, benefícios, alimentação, transporte, EPI, alojamento e horas extras.

## Componentes do Custo

### 1. Salário Base

**Fontes:**
- Convenção Coletiva de Trabalho (CCT)
- Sindicatos (SINDUSCON)
- Tabelas regionais (SINAPI)

**Categorias Típicas:**

| Função | Salário Mensal (R$) | Salário Horário (R$) |
|--------|---------------------|----------------------|
| Servente | 1.800 - 2.200 | 8.18 - 10.00 |
| Pedreiro | 3.000 - 3.800 | 13.64 - 17.27 |
| Carpinteiro | 3.200 - 4.000 | 14.55 - 18.18 |
| Armador | 3.400 - 4.200 | 15.45 - 19.09 |
| Encarregado | 4.500 - 5.500 | 20.45 - 25.00 |
| Mestre de obras | 5.500 - 7.000 | 25.00 - 31.82 |

### 2. Encargos Sociais e Leis Trabalhistas

**Detalhamento Completo:**

```python
def calcular_encargos_sociais(
    salario_mensal: float,
    regime: str = 'sem_desoneracao',
    categoria: str = 'horista'
) -> dict:
    """
    Calcula encargos sociais e leis trabalhistas.
    
    Referência: Acórdão TCU 2622/2013
    """
    # Grupo A - Encargos Sociais Básicos
    if regime == 'com_desoneracao':
        # Lei 12.546/2011 - Desoneração da folha
        inss_patronal = 0.0  # Substituído por CPP
        cpp = 0.045  # 4.5% sobre faturamento
    else:
        inss_patronal = 0.20  # 20%
        cpp = 0.0
    
    sesi_senai = 0.015 + 0.01  # 1.5% + 1.0%
    incra_sebrae = 0.002 + 0.006  # 0.2% + 0.6%
    salario_educacao = 0.025  # 2.5%
    seguro_acidente = 0.03  # 3.0% (RAT médio)
    fgts = 0.08  # 8.0%
    
    grupo_a = (inss_patronal + sesi_senai + incra_sebrae + 
               salario_educacao + seguro_acidente + fgts)
    
    # Grupo B - Leis Sociais
    ferias = 1/12 * 1.333  # 11.11%
    decimo_terceiro = 1/12  # 8.33%
    auxilio_doenca = 0.0055  # 0.55%
    licenca_paternidade = 0.0003  # 0.03%
    faltas_justificadas = 0.0083  # 0.83%
    dias_chuva = 0.0139  # 1.39% (região sudeste)
    aviso_previo = 0.0198  # 1.98%
    
    grupo_b = (ferias + decimo_terceiro + auxilio_doenca + 
               licenca_paternidade + faltas_justificadas + 
               dias_chuva + aviso_previo)
    
    # Total
    encargos_total = grupo_a + grupo_b
    
    # Custo horário
    horas_mes = 220 if categoria == 'horista' else 200
    salario_horario = salario_mensal / horas_mes
    custo_horario = salario_horario * (1 + encargos_total)
    
    return {
        'salario_mensal': salario_mensal,
        'salario_horario': round(salario_horario, 2),
        'grupo_a_pct': round(grupo_a * 100, 2),
        'grupo_b_pct': round(grupo_b * 100, 2),
        'encargos_total_pct': round(encargos_total * 100, 2),
        'custo_horario_com_encargos': round(custo_horario, 2),
        'custo_mensal_com_encargos': round(custo_horario * horas_mes, 2)
    }
```

### 3. Benefícios e Auxílios

**Vale Alimentação/Refeição:**
```
Valor típico: R$ 25-35 por dia trabalhado
Dias por mês: 22 dias úteis
Custo mensal: R$ 550-770

Observação: Não incide encargos sociais (PAT)
```

**Vale Transporte:**
```
Cálculo:
Custo_VT = (Passagem_ida_volta × Dias_úteis) - Desconto_funcionário

Desconto_funcionário = min(6% × Salário, Custo_VT)

Exemplo:
Passagem: R$ 4.50 (ida) + R$ 4.50 (volta) = R$ 9.00/dia
Dias: 22 dias
Custo total: R$ 198.00
Desconto (6% de R$ 3.000): R$ 180.00
Custo empresa: R$ 198.00 - R$ 180.00 = R$ 18.00
```

**EPI (Equipamento de Proteção Individual):**
```
Custo médio por funcionário:
- Capacete: R$ 25 (6 meses)
- Botina: R$ 80 (6 meses)
- Luvas: R$ 15 (mensal)
- Óculos: R$ 20 (6 meses)
- Protetor auricular: R$ 5 (mensal)

Custo mensal médio: R$ 40-60/funcionário
```

### 4. Alojamento

**Quando necessário:**
- Obras remotas (> 50km da cidade)
- Obras em locais sem infraestrutura

**Custo:**
```
Opção 1: Container habitável
- Capacidade: 8-12 pessoas
- Custo: R$ 800-1.200/mês por container
- Custo por pessoa: R$ 80-120/mês

Opção 2: Aluguel de casa
- Custo: R$ 1.500-3.000/mês
- Capacidade: 10-15 pessoas
- Custo por pessoa: R$ 100-200/mês

Opção 3: Hotel/pousada
- Custo: R$ 80-150/dia por pessoa
- Custo mensal: R$ 1.760-3.300/pessoa
```

### 5. Horas Extras

**Cálculo:**
```python
def calcular_hora_extra(
    salario_horario: float,
    horas_extras_mes: float,
    tipo: str = 'normal'
) -> dict:
    """
    Calcula custo de horas extras.
    
    Args:
        salario_horario: Salário horário base
        horas_extras_mes: Quantidade de HE no mês
        tipo: 'normal' (50%), 'domingo_feriado' (100%), 'noturno' (20%)
    """
    adicional = {
        'normal': 0.50,  # 50%
        'domingo_feriado': 1.00,  # 100%
        'noturno': 0.20  # 20%
    }
    
    percentual = adicional.get(tipo, 0.50)
    valor_he = salario_horario * (1 + percentual)
    custo_total_he = valor_he * horas_extras_mes
    
    # Encargos sobre HE (mesmo percentual do salário)
    encargos_pct = 0.6462  # 64.62% típico
    custo_total_com_encargos = custo_total_he * (1 + encargos_pct)
    
    return {
        'tipo_he': tipo,
        'adicional_pct': percentual * 100,
        'valor_hora_extra': round(valor_he, 2),
        'horas_mes': horas_extras_mes,
        'custo_he_sem_encargos': round(custo_total_he, 2),
        'custo_he_com_encargos': round(custo_total_com_encargos, 2)
    }
```

### 6. Custo Total Mensal por Funcionário

**Exemplo Completo:**

```python
def calcular_custo_total_funcionario(
    funcao: str = 'pedreiro',
    salario_base: float = 3500.00,
    horas_extras_mes: float = 20,
    necessita_alojamento: bool = False,
    distancia_km: float = 10
) -> dict:
    """
    Calcula custo total mensal de um funcionário.
    """
    # 1. Salário com encargos
    encargos = calcular_encargos_sociais(salario_base)
    custo_salario = encargos['custo_mensal_com_encargos']
    
    # 2. Vale alimentação
    vale_alimentacao = 30 * 22  # R$ 30/dia × 22 dias
    
    # 3. Vale transporte
    if distancia_km <= 5:
        vale_transporte = 0  # Caminha
    else:
        passagem_dia = 9.00  # R$ 4.50 ida + volta
        custo_vt_total = passagem_dia * 22
        desconto_func = min(0.06 * salario_base, custo_vt_total)
        vale_transporte = custo_vt_total - desconto_func
    
    # 4. EPI
    epi = 50
    
    # 5. Alojamento
    alojamento = 100 if necessita_alojamento else 0
    
    # 6. Horas extras
    he = calcular_hora_extra(
        encargos['salario_horario'], 
        horas_extras_mes
    )
    custo_he = he['custo_he_com_encargos']
    
    # Total
    custo_total = (custo_salario + vale_alimentacao + vale_transporte + 
                   epi + alojamento + custo_he)
    
    return {
        'funcao': funcao,
        'salario_base': salario_base,
        'custo_salario_com_encargos': round(custo_salario, 2),
        'vale_alimentacao': vale_alimentacao,
        'vale_transporte': round(vale_transporte, 2),
        'epi': epi,
        'alojamento': alojamento,
        'horas_extras': round(custo_he, 2),
        'custo_total_mensal': round(custo_total, 2),
        'custo_diario': round(custo_total / 22, 2)
    }

# Exemplo
resultado = calcular_custo_total_funcionario(
    funcao='Pedreiro',
    salario_base=3500.00,
    horas_extras_mes=20,
    necessita_alojamento=False,
    distancia_km=15
)

print(f"Custo total mensal: R$ {resultado['custo_total_mensal']:.2f}")
print(f"Custo diário: R$ {resultado['custo_diario']:.2f}")
```

## Outputs Esperados

1. **Planilha de Custos de MO**
   - Salário base por função
   - Encargos detalhados
   - Benefícios e auxílios
   - Custo total mensal

2. **Memória de Cálculo**
   - Percentuais aplicados
   - Fontes de dados
   - Premissas adotadas

## Referências

- **Acórdão TCU 2622/2013** - Encargos sociais
- **Lei 12.546/2011** - Desoneração da folha
- **CLT** - Consolidação das Leis do Trabalho
- **Convenções Coletivas** - SINDUSCON
