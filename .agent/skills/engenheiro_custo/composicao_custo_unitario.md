---
skill_name: "Composição de Custo Unitário (CPU)"
agent: engenheiro_planejamento
category: "Orçamentação e Custos"
difficulty: intermediate
version: 1.0.0
---

# Skill: Composição de Custo Unitário (CPU)

## Objetivo

Fornecer metodologia completa para elaboração, análise e validação de Composições de Custo Unitário (CPU), incluindo tratamento de encargos sociais, leis sociais e BDI.

## Fundamentos Teóricos

### 1. Estrutura de uma CPU

```
CPU = Σ (Insumo_i × Coeficiente_i × Preço_Unitário_i)

Onde:
CPU           = Custo Unitário do Serviço (R$/unidade)
Insumo_i      = Tipo de insumo (material, mão de obra, equipamento)
Coeficiente_i = Quantidade consumida por unidade de serviço
Preço_Unit_i  = Preço do insumo no mercado (R$/unidade do insumo)
```

**Exemplo: Concreto FCK 25 MPa (m³)**
```
┌─────────────────────────────────────────────────────────────┐
│ COMPOSIÇÃO: Concreto FCK 25 MPa (m³)                       │
├─────────────────────────────────────────────────────────────┤
│ Insumo              │ Unid │ Coef.  │ Preço R$ │ Total R$ │
├─────────────────────┼──────┼────────┼──────────┼──────────┤
│ Cimento CP-II       │ kg   │ 350.00 │ 0.65     │ 227.50   │
│ Areia média         │ m³   │ 0.55   │ 80.00    │ 44.00    │
│ Brita 1             │ m³   │ 0.85   │ 90.00    │ 76.50    │
│ Água                │ m³   │ 0.18   │ 5.00     │ 0.90     │
│ Pedreiro            │ h    │ 0.50   │ 25.00    │ 12.50    │
│ Servente            │ h    │ 1.00   │ 18.00    │ 18.00    │
│ Betoneira 400L      │ h    │ 0.50   │ 15.00    │ 7.50     │
├─────────────────────┴──────┴────────┴──────────┼──────────┤
│ CUSTO DIRETO TOTAL (sem encargos)              │ 386.90   │
└────────────────────────────────────────────────┴──────────┘
```

### 2. Categorias de Insumos

#### 2.1 Materiais
**Características:**
- Incorporados permanentemente à obra
- Preço = Custo de aquisição + Frete + Perdas

**Fórmula com Perdas:**
```
Custo_Material = Preço_Base × (1 + Taxa_Perda)

Taxa_Perda típica:
- Concreto: 5%
- Cerâmica: 10%
- Aço (barras): 10%
- Madeira: 15%
```

#### 2.2 Mão de Obra
**Componentes do Custo Horário:**
```
Custo_MO_Horário = Salário_Horário × (1 + Encargos_Sociais + Leis_Sociais)

Salário_Horário = Salário_Mensal / 220h

Encargos Sociais (Grupo A):
- INSS: 20%
- SESI/SENAI: 3.6%
- INCRA/Sebrae: 3.3%
- Salário Educação: 2.5%
- Seguro Acidente: 3.0%
- FGTS: 8.0%
Total Grupo A: 40.4%

Leis Sociais (Grupo B):
- Férias: 11.11%
- 13º Salário: 8.33%
- Auxílio Doença: 0.55%
- Licença Paternidade: 0.03%
- Faltas Justificadas: 0.83%
- Dias de Chuva: 1.39%
- Aviso Prévio: 1.98%
Total Grupo B: 24.22%

TOTAL ENCARGOS: 64.62% (obra sem desoneração)
```

**Exemplo de Cálculo:**

```python
def calcular_custo_horario_mo(
    salario_mensal: float,
    categoria: str = 'horista',
    regime: str = 'com_desoneracao'
) -> dict:
    """
    Calcula custo horário de mão de obra com encargos sociais.
    
    Args:
        salario_mensal: Salário base mensal (R$)
        categoria: 'horista' ou 'mensalista'
        regime: 'com_desoneracao' ou 'sem_desoneracao'
    
    Returns:
        dict com salário horário, encargos e custo total
    
    Referência: Acórdão TCU 2622/2013
    """
    # Salário horário
    horas_mes = 220 if categoria == 'horista' else 200
    salario_horario = salario_mensal / horas_mes
    
    # Encargos Sociais (Grupo A)
    if regime == 'com_desoneracao':
        # Lei 12.546/2011 - Desoneração da folha
        grupo_a = 0.119  # 11.9% (sem INSS patronal)
    else:
        grupo_a = 0.404  # 40.4% (regime normal)
    
    # Leis Sociais (Grupo B)
    grupo_b = 0.2422  # 24.22%
    
    # Custo total
    encargos_total = grupo_a + grupo_b
    custo_horario = salario_horario * (1 + encargos_total)
    
    return {
        'salario_horario': round(salario_horario, 2),
        'encargos_grupo_a_pct': grupo_a * 100,
        'encargos_grupo_b_pct': grupo_b * 100,
        'encargos_total_pct': encargos_total * 100,
        'custo_horario_total': round(custo_horario, 2)
    }

# Exemplo de uso
pedreiro = calcular_custo_horario_mo(
    salario_mensal=3500.00,
    categoria='horista',
    regime='sem_desoneracao'
)

print(f"Salário horário: R$ {pedreiro['salario_horario']}")
print(f"Encargos totais: {pedreiro['encargos_total_pct']:.2f}%")
print(f"Custo horário: R$ {pedreiro['custo_horario_total']}")

# Output:
# Salário horário: R$ 15.91
# Encargos totais: 64.62%
# Custo horário: R$ 26.19
```

#### 2.3 Equipamentos
**Componentes do Custo Horário:**
```
Custo_Equip_Horário = Depreciação + Juros + Manutenção + Combustível + Operador

Depreciação = (Valor_Novo - Valor_Residual) / Vida_Útil_Horas

Juros = (Valor_Novo × Taxa_Juros_Anual) / Horas_Ano

Manutenção = % do Valor_Novo (tipicamente 5-10% ao ano)

Combustível = Consumo_L/h × Preço_Diesel

Operador = Custo_Horário_MO (se aplicável)
```

**Exemplo: Escavadeira Hidráulica**
```
Valor novo: R$ 450.000
Vida útil: 10.000 horas
Valor residual: 20% (R$ 90.000)
Taxa juros: 12% a.a.
Horas/ano: 2.000h

Depreciação = (450.000 - 90.000) / 10.000 = R$ 36.00/h
Juros = (450.000 × 0.12) / 2.000 = R$ 27.00/h
Manutenção = (450.000 × 0.08) / 2.000 = R$ 18.00/h
Combustível = 15 L/h × R$ 5.50 = R$ 82.50/h
Operador = R$ 30.00/h

TOTAL = R$ 193.50/h
```

### 3. Fontes de Preços

#### 3.1 Bases Oficiais (Referenciais)

**SINAPI (Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil)**
- Mantido: IBGE + Caixa Econômica Federal
- Atualização: Mensal
- Aplicação: Obras públicas federais (obrigatório)
- Acesso: https://www.caixa.gov.br/sinapi

**SICRO (Sistema de Custos Rodoviários)**
- Mantido: DNIT
- Aplicação: Obras rodoviárias
- Atualização: Trimestral

**Tabelas Estaduais**
- ORSE (Rio de Janeiro)
- PINI (São Paulo)
- DER (Departamentos Estaduais de Estradas)

#### 3.2 Pesquisa de Mercado

**Requisitos (TCU):**
- Mínimo 3 cotações por insumo
- Fornecedores idôneos
- Documentação (propostas, e-mails, notas fiscais)
- Atualização trimestral

### 4. Coeficientes de Consumo

#### 4.1 Fontes de Coeficientes

**Tabelas Técnicas:**
- TCPO (Tabela de Composições de Preços para Orçamentos)
- SINAPI (composições oficiais)
- Manuais de fabricantes

**Produtividade Medida:**
```
Coeficiente_Real = Quantidade_Consumida / Quantidade_Executada

Exemplo: Assentamento de cerâmica
- Executado: 100 m²
- Consumo de argamassa: 550 kg
- Coeficiente = 550 / 100 = 5.5 kg/m²
```

#### 4.2 Ajuste de Coeficientes

**Fatores de Influência:**
- Condições locais (clima, acesso)
- Qualificação da mão de obra
- Tecnologia empregada
- Escala de produção

**Exemplo: Concretagem**
```
Coeficiente base (SINAPI): 0.50 h/m³ (pedreiro)

Ajustes:
× 1.2 (acesso difícil)
× 0.9 (equipe experiente)
× 1.1 (geometria complexa)

Coeficiente ajustado = 0.50 × 1.2 × 0.9 × 1.1 = 0.594 h/m³
```

### 5. Estrutura de Dados (Python)

```python
from dataclasses import dataclass
from typing import List, Literal

@dataclass
class Insumo:
    """Representa um insumo da composição."""
    codigo: str
    descricao: str
    unidade: str
    tipo: Literal['material', 'mao_obra', 'equipamento']
    preco_unitario: float
    origem: str  # 'SINAPI', 'SICRO', 'Cotacao', etc.

@dataclass
class ItemComposicao:
    """Item de uma composição de custo."""
    insumo: Insumo
    coeficiente: float
    
    @property
    def custo_total(self) -> float:
        """Calcula custo total do item."""
        return self.coeficiente * self.insumo.preco_unitario

@dataclass
class ComposicaoCustoUnitario:
    """Composição de Custo Unitário completa."""
    codigo: str
    descricao: str
    unidade: str
    itens: List[ItemComposicao]
    
    @property
    def custo_material(self) -> float:
        """Soma custos de materiais."""
        return sum(
            item.custo_total 
            for item in self.itens 
            if item.insumo.tipo == 'material'
        )
    
    @property
    def custo_mao_obra(self) -> float:
        """Soma custos de mão de obra."""
        return sum(
            item.custo_total 
            for item in self.itens 
            if item.insumo.tipo == 'mao_obra'
        )
    
    @property
    def custo_equipamento(self) -> float:
        """Soma custos de equipamentos."""
        return sum(
            item.custo_total 
            for item in self.itens 
            if item.insumo.tipo == 'equipamento'
        )
    
    @property
    def custo_direto_total(self) -> float:
        """Custo direto total (sem BDI)."""
        return sum(item.custo_total for item in self.itens)
    
    def aplicar_bdi(self, bdi_percentual: float) -> float:
        """
        Aplica BDI ao custo direto.
        
        Args:
            bdi_percentual: BDI em percentual (ex: 25.5 para 25.5%)
        
        Returns:
            Preço de venda unitário
        """
        return self.custo_direto_total * (1 + bdi_percentual / 100)
    
    def to_dict(self) -> dict:
        """Exporta composição para dicionário."""
        return {
            'codigo': self.codigo,
            'descricao': self.descricao,
            'unidade': self.unidade,
            'itens': [
                {
                    'codigo': item.insumo.codigo,
                    'descricao': item.insumo.descricao,
                    'unidade': item.insumo.unidade,
                    'tipo': item.insumo.tipo,
                    'coeficiente': item.coeficiente,
                    'preco_unitario': item.insumo.preco_unitario,
                    'custo_total': item.custo_total
                }
                for item in self.itens
            ],
            'resumo': {
                'custo_material': self.custo_material,
                'custo_mao_obra': self.custo_mao_obra,
                'custo_equipamento': self.custo_equipamento,
                'custo_direto_total': self.custo_direto_total
            }
        }
```

### 6. Validação de CPU

#### Checklist de Qualidade

- [ ] Todos os insumos têm fonte documentada
- [ ] Coeficientes compatíveis com tabelas técnicas (variação < 20%)
- [ ] Encargos sociais aplicados corretamente
- [ ] Perdas de materiais consideradas
- [ ] Unidades consistentes (m³, m², kg, h)
- [ ] Custo total coerente com mercado (benchmark)

#### Análise de Sensibilidade

```python
def analise_sensibilidade_cpu(
    cpu: ComposicaoCustoUnitario,
    variacao_percentual: float = 10.0
) -> dict:
    """
    Analisa impacto de variação de preços no custo total.
    
    Args:
        cpu: Composição a analisar
        variacao_percentual: Variação a simular (%)
    
    Returns:
        dict com impactos por tipo de insumo
    """
    custo_base = cpu.custo_direto_total
    
    impactos = {}
    for tipo in ['material', 'mao_obra', 'equipamento']:
        # Simular aumento de preço
        custo_tipo_base = getattr(cpu, f'custo_{tipo}')
        custo_tipo_variado = custo_tipo_base * (1 + variacao_percentual / 100)
        delta = custo_tipo_variado - custo_tipo_base
        
        custo_total_variado = custo_base + delta
        impacto_percentual = (delta / custo_base) * 100
        
        impactos[tipo] = {
            'custo_base': custo_tipo_base,
            'variacao_absoluta': delta,
            'impacto_no_total_pct': impacto_percentual
        }
    
    return impactos
```

### 7. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Planilha de CPU Detalhada**
   - Código e descrição do serviço
   - Lista completa de insumos
   - Coeficientes e preços
   - Subtotais por categoria

2. **Memória de Cálculo de Encargos**
   - Regime tributário aplicado
   - Percentuais de Grupo A e B
   - Custo horário resultante

3. **Fontes e Referências**
   - Origem de cada preço (SINAPI, cotação, etc.)
   - Data de referência
   - Documentação de cotações

4. **Análise de Sensibilidade**
   - Impacto de variação de materiais
   - Impacto de variação de mão de obra
   - Recomendações de contingência

### 8. Referências Normativas

- **Acórdão TCU 2622/2013** - Encargos sociais e trabalhistas
- **Lei 12.546/2011** - Desoneração da folha de pagamento
- **NBR 12721:2006** - Avaliação de custos unitários
- **SINAPI** - Metodologia e conceitos (Caixa Econômica Federal)
