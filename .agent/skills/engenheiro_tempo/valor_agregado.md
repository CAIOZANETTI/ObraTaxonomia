---
skill_name: "Análise de Valor Agregado (EVA)"
agent: engenheiro_planejamento
category: "Controle de Projetos"
difficulty: advanced
version: 1.0.0
---

# Skill: Análise de Valor Agregado (Earned Value Analysis - EVA)

## Objetivo

Fornecer metodologia completa para monitoramento e controle de desempenho de projetos através da técnica de Valor Agregado (Earned Value Management - EVM), conforme PMI PMBOK Guide.

## Fundamentos Teóricos

### 1. Conceitos Básicos

#### Três Valores Fundamentais

**PV - Planned Value (Valor Planejado)**
```
PV = Custo orçado do trabalho PLANEJADO até a data

Também conhecido como: BCWS (Budgeted Cost of Work Scheduled)
```

**EV - Earned Value (Valor Agregado)**
```
EV = Custo orçado do trabalho REALIZADO até a data

Também conhecido como: BCWP (Budgeted Cost of Work Performed)
```

**AC - Actual Cost (Custo Real)**
```
AC = Custo REAL incorrido pelo trabalho realizado até a data

Também conhecido como: ACWP (Actual Cost of Work Performed)
```

#### Exemplo Visual

```
Projeto: Construção de Muro (100m)
Orçamento Total (BAC): R$ 50.000
Prazo: 10 semanas
Custo planejado: R$ 5.000/semana

Semana 5 (Data de Corte):
┌────────────────────────────────────────────────┐
│ PV = 5 semanas × R$ 5.000 = R$ 25.000        │ (Deveria ter gasto)
│ EV = 40m × R$ 500/m = R$ 20.000              │ (Valor do que fez)
│ AC = R$ 22.000                                 │ (Gastou de fato)
└────────────────────────────────────────────────┘

Interpretação:
- Atraso: EV < PV (fez menos que planejou)
- Sobre-custo: AC > EV (gastou mais que deveria)
```

### 2. Índices de Desempenho

#### 2.1 CPI - Cost Performance Index (Índice de Desempenho de Custo)

**Fórmula:**
```
CPI = EV / AC

Interpretação:
CPI > 1.0 → Abaixo do orçamento (BOM)
CPI = 1.0 → No orçamento (NEUTRO)
CPI < 1.0 → Acima do orçamento (RUIM)
```

**Exemplo:**
```
CPI = 20.000 / 22.000 = 0.91

Interpretação: Para cada R$ 1,00 gasto, está agregando apenas R$ 0,91 de valor.
Eficiência de custo: 91%
```

#### 2.2 SPI - Schedule Performance Index (Índice de Desempenho de Prazo)

**Fórmula:**
```
SPI = EV / PV

Interpretação:
SPI > 1.0 → Adiantado (BOM)
SPI = 1.0 → No prazo (NEUTRO)
SPI < 1.0 → Atrasado (RUIM)
```

**Exemplo:**
```
SPI = 20.000 / 25.000 = 0.80

Interpretação: Está executando a 80% da velocidade planejada.
Atraso equivalente: 20%
```

### 3. Variações (Variances)

#### 3.1 CV - Cost Variance (Variação de Custo)

**Fórmula:**
```
CV = EV - AC

Interpretação:
CV > 0 → Abaixo do orçamento (BOM)
CV = 0 → No orçamento (NEUTRO)
CV < 0 → Acima do orçamento (RUIM)
```

**Exemplo:**
```
CV = 20.000 - 22.000 = -R$ 2.000

Interpretação: Sobre-custo de R$ 2.000 até o momento.
```

#### 3.2 SV - Schedule Variance (Variação de Prazo)

**Fórmula:**
```
SV = EV - PV

Interpretação:
SV > 0 → Adiantado (BOM)
SV = 0 → No prazo (NEUTRO)
SV < 0 → Atrasado (RUIM)
```

**Exemplo:**
```
SV = 20.000 - 25.000 = -R$ 5.000

Interpretação: Atraso equivalente a R$ 5.000 de trabalho não realizado.
```

### 4. Projeções (Forecasting)

#### 4.1 EAC - Estimate at Completion (Estimativa no Término)

**Método 1: Baseado em CPI (Variação típica)**
```
EAC = BAC / CPI

Premissa: Desempenho futuro = Desempenho passado
```

**Método 2: Baseado em CPI e SPI (Variação atípica)**
```
EAC = AC + (BAC - EV)

Premissa: Variação foi pontual, futuro será conforme planejado
```

**Método 3: Baseado em nova estimativa**
```
EAC = AC + ETC

ETC = Estimate to Complete (nova estimativa para o trabalho restante)
```

**Exemplo:**
```
BAC = R$ 50.000
CPI = 0.91

EAC = 50.000 / 0.91 = R$ 54.945

Interpretação: Projeto deve terminar com R$ 54.945 (sobre-custo de R$ 4.945)
```

#### 4.2 ETC - Estimate to Complete (Estimativa para Terminar)

**Fórmula:**
```
ETC = EAC - AC

ou

ETC = (BAC - EV) / CPI
```

**Exemplo:**
```
ETC = 54.945 - 22.000 = R$ 32.945

Interpretação: Ainda precisa gastar R$ 32.945 para concluir.
```

#### 4.3 VAC - Variance at Completion (Variação no Término)

**Fórmula:**
```
VAC = BAC - EAC

Interpretação:
VAC > 0 → Projeto terminará abaixo do orçamento
VAC = 0 → Projeto terminará no orçamento
VAC < 0 → Projeto terminará acima do orçamento
```

**Exemplo:**
```
VAC = 50.000 - 54.945 = -R$ 4.945

Interpretação: Previsão de sobre-custo de R$ 4.945 no final.
```

#### 4.4 TCPI - To-Complete Performance Index (Índice de Desempenho para Terminar)

**Para terminar no orçamento (BAC):**
```
TCPI = (BAC - EV) / (BAC - AC)
```

**Para terminar em EAC:**
```
TCPI = (BAC - EV) / (EAC - AC)
```

**Interpretação:**
```
TCPI > 1.0 → Precisa melhorar eficiência
TCPI = 1.0 → Manter eficiência atual
TCPI < 1.0 → Pode relaxar eficiência
```

**Exemplo:**
```
TCPI = (50.000 - 20.000) / (50.000 - 22.000) = 30.000 / 28.000 = 1.07

Interpretação: Precisa ter eficiência de 107% (CPI = 1.07) no trabalho restante para terminar no orçamento original.
```

### 5. Implementação em Python

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class EVAMetrics:
    """
    Métricas de Análise de Valor Agregado.
    
    Attributes:
        data_corte: Data de referência da medição
        BAC: Budget at Completion (Orçamento no Término)
        PV: Planned Value (Valor Planejado)
        EV: Earned Value (Valor Agregado)
        AC: Actual Cost (Custo Real)
    """
    data_corte: date
    BAC: float  # Budget at Completion
    PV: float   # Planned Value
    EV: float   # Earned Value
    AC: float   # Actual Cost
    
    @property
    def CPI(self) -> float:
        """Cost Performance Index."""
        if self.AC == 0:
            return 0.0
        return self.EV / self.AC
    
    @property
    def SPI(self) -> float:
        """Schedule Performance Index."""
        if self.PV == 0:
            return 0.0
        return self.EV / self.PV
    
    @property
    def CV(self) -> float:
        """Cost Variance."""
        return self.EV - self.AC
    
    @property
    def SV(self) -> float:
        """Schedule Variance."""
        return self.EV - self.PV
    
    @property
    def percentual_completo(self) -> float:
        """Percentual de conclusão do projeto."""
        if self.BAC == 0:
            return 0.0
        return (self.EV / self.BAC) * 100
    
    def EAC(self, metodo: str = 'CPI') -> float:
        """
        Estimate at Completion.
        
        Args:
            metodo: 'CPI', 'CPI_SPI', ou 'nova_estimativa'
        
        Returns:
            Estimativa de custo total no término
        """
        if metodo == 'CPI':
            if self.CPI == 0:
                return float('inf')
            return self.BAC / self.CPI
        
        elif metodo == 'CPI_SPI':
            if self.CPI * self.SPI == 0:
                return float('inf')
            return self.BAC / (self.CPI * self.SPI)
        
        elif metodo == 'nova_estimativa':
            # Premissa: variação foi atípica
            return self.AC + (self.BAC - self.EV)
        
        else:
            raise ValueError(f"Método '{metodo}' não reconhecido")
    
    def ETC(self, metodo: str = 'CPI') -> float:
        """Estimate to Complete."""
        return self.EAC(metodo) - self.AC
    
    def VAC(self, metodo: str = 'CPI') -> float:
        """Variance at Completion."""
        return self.BAC - self.EAC(metodo)
    
    def TCPI(self, objetivo: str = 'BAC') -> float:
        """
        To-Complete Performance Index.
        
        Args:
            objetivo: 'BAC' (terminar no orçamento) ou 'EAC' (terminar na estimativa)
        
        Returns:
            CPI necessário para atingir objetivo
        """
        trabalho_restante = self.BAC - self.EV
        
        if objetivo == 'BAC':
            fundos_restantes = self.BAC - self.AC
        elif objetivo == 'EAC':
            fundos_restantes = self.EAC('CPI') - self.AC
        else:
            raise ValueError(f"Objetivo '{objetivo}' não reconhecido")
        
        if fundos_restantes == 0:
            return float('inf')
        
        return trabalho_restante / fundos_restantes
    
    def interpretar_CPI(self) -> str:
        """Retorna interpretação textual do CPI."""
        if self.CPI > 1.1:
            return "Excelente - Muito abaixo do orçamento"
        elif self.CPI > 1.0:
            return "Bom - Abaixo do orçamento"
        elif self.CPI >= 0.95:
            return "Aceitável - Próximo ao orçamento"
        elif self.CPI >= 0.90:
            return "Atenção - Ligeiramente acima do orçamento"
        else:
            return "Crítico - Muito acima do orçamento"
    
    def interpretar_SPI(self) -> str:
        """Retorna interpretação textual do SPI."""
        if self.SPI > 1.1:
            return "Excelente - Muito adiantado"
        elif self.SPI > 1.0:
            return "Bom - Adiantado"
        elif self.SPI >= 0.95:
            return "Aceitável - Próximo ao cronograma"
        elif self.SPI >= 0.90:
            return "Atenção - Ligeiramente atrasado"
        else:
            return "Crítico - Muito atrasado"
    
    def gerar_relatorio(self) -> dict:
        """Gera relatório completo de EVA."""
        return {
            'data_corte': self.data_corte.isoformat(),
            'valores_base': {
                'BAC': self.BAC,
                'PV': self.PV,
                'EV': self.EV,
                'AC': self.AC
            },
            'indices': {
                'CPI': round(self.CPI, 3),
                'SPI': round(self.SPI, 3),
                'interpretacao_CPI': self.interpretar_CPI(),
                'interpretacao_SPI': self.interpretar_SPI()
            },
            'variacoes': {
                'CV': round(self.CV, 2),
                'SV': round(self.SV, 2),
                'percentual_completo': round(self.percentual_completo, 1)
            },
            'projecoes': {
                'EAC': round(self.EAC('CPI'), 2),
                'ETC': round(self.ETC('CPI'), 2),
                'VAC': round(self.VAC('CPI'), 2),
                'TCPI_BAC': round(self.TCPI('BAC'), 3),
                'TCPI_EAC': round(self.TCPI('EAC'), 3)
            },
            'alertas': self._gerar_alertas()
        }
    
    def _gerar_alertas(self) -> list:
        """Gera lista de alertas baseados nos índices."""
        alertas = []
        
        if self.CPI < 0.90:
            alertas.append({
                'tipo': 'CRÍTICO',
                'categoria': 'Custo',
                'mensagem': f'CPI = {self.CPI:.2f} - Projeto muito acima do orçamento'
            })
        elif self.CPI < 0.95:
            alertas.append({
                'tipo': 'ATENÇÃO',
                'categoria': 'Custo',
                'mensagem': f'CPI = {self.CPI:.2f} - Projeto ligeiramente acima do orçamento'
            })
        
        if self.SPI < 0.90:
            alertas.append({
                'tipo': 'CRÍTICO',
                'categoria': 'Prazo',
                'mensagem': f'SPI = {self.SPI:.2f} - Projeto muito atrasado'
            })
        elif self.SPI < 0.95:
            alertas.append({
                'tipo': 'ATENÇÃO',
                'categoria': 'Prazo',
                'mensagem': f'SPI = {self.SPI:.2f} - Projeto ligeiramente atrasado'
            })
        
        tcpi_bac = self.TCPI('BAC')
        if tcpi_bac > 1.2:
            alertas.append({
                'tipo': 'CRÍTICO',
                'categoria': 'Viabilidade',
                'mensagem': f'TCPI = {tcpi_bac:.2f} - Muito difícil terminar no orçamento'
            })
        elif tcpi_bac > 1.1:
            alertas.append({
                'tipo': 'ATENÇÃO',
                'categoria': 'Viabilidade',
                'mensagem': f'TCPI = {tcpi_bac:.2f} - Desafiador terminar no orçamento'
            })
        
        return alertas

# Exemplo de uso
eva = EVAMetrics(
    data_corte=date(2026, 1, 26),
    BAC=50000.00,
    PV=25000.00,
    EV=20000.00,
    AC=22000.00
)

relatorio = eva.gerar_relatorio()
print(f"CPI: {relatorio['indices']['CPI']} - {relatorio['indices']['interpretacao_CPI']}")
print(f"SPI: {relatorio['indices']['SPI']} - {relatorio['indices']['interpretacao_SPI']}")
print(f"EAC: R$ {relatorio['projecoes']['EAC']:,.2f}")
print(f"VAC: R$ {relatorio['projecoes']['VAC']:,.2f}")

for alerta in relatorio['alertas']:
    print(f"[{alerta['tipo']}] {alerta['categoria']}: {alerta['mensagem']}")
```

### 6. Ações Corretivas Baseadas em EVA

#### Matriz de Decisão

| Situação | CPI | SPI | Ação Recomendada |
|----------|-----|-----|------------------|
| **Ideal** | > 1.0 | > 1.0 | Manter curso, documentar boas práticas |
| **Sobre-custo** | < 1.0 | > 1.0 | Revisar custos, otimizar recursos |
| **Atraso** | > 1.0 | < 1.0 | Acelerar cronograma, adicionar recursos |
| **Crítico** | < 1.0 | < 1.0 | Replanejar, considerar fast-tracking ou crashing |

#### Quando SPI < 1.0 (Atrasado)

**Opções:**
1. **Fast-Tracking:** Executar atividades em paralelo (aumenta risco)
2. **Crashing:** Adicionar recursos (aumenta custo)
3. **Reduzir Escopo:** Negociar com cliente (última opção)

#### Quando CPI < 1.0 (Sobre-custo)

**Opções:**
1. **Value Engineering:** Otimizar soluções técnicas
2. **Renegociar Contratos:** Fornecedores e subempreiteiros
3. **Melhorar Produtividade:** Treinamento, melhores processos

### 7. Outputs Esperados

Ao aplicar esta skill, o agente deve fornecer:

1. **Dashboard EVA**
   - Gráfico de curvas PV, EV, AC
   - Índices CPI e SPI
   - Semáforo de status (verde/amarelo/vermelho)

2. **Relatório de Análise**
   - Interpretação de índices
   - Variações identificadas
   - Projeções de término

3. **Plano de Ação**
   - Causas raiz de desvios
   - Ações corretivas propostas
   - Responsáveis e prazos

4. **Tendências**
   - Evolução histórica de CPI e SPI
   - Previsão de EAC
   - Análise de risco

### 8. Referências

- **PMI PMBOK Guide** (7th Edition) - Chapter on Project Cost Management
- **Practice Standard for Earned Value Management** (PMI, 2019)
- **ANSI/EIA-748** - Earned Value Management Systems Standard
- **Acórdão TCU 1977/2013** - Aplicação de EVM em obras públicas
