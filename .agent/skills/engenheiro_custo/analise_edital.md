---
skill_name: "Análise de Edital de Licitação"
agent: engenheiro_custo
category: "Orçamentação e Licitações"
difficulty: intermediate
version: 1.0.0
---

# Skill: Análise de Edital de Licitação

## Objetivo

Fornecer metodologia sistemática para análise crítica de editais de licitação pública, identificando requisitos, riscos, oportunidades e pontos de atenção para elaboração de propostas competitivas e conformes.

## Fundamentos

### 1. Estrutura de um Edital

**Componentes Principais:**
```
1. Preâmbulo
   - Órgão licitante
   - Modalidade (concorrência, tomada de preços, convite, pregão, RDC)
   - Regime de execução (empreitada global, por preço unitário, etc.)
   - Tipo de licitação (menor preço, técnica e preço, melhor técnica)

2. Objeto
   - Descrição detalhada da obra/serviço
   - Quantitativos
   - Prazos

3. Condições de Participação
   - Habilitação jurídica
   - Qualificação técnica
   - Qualificação econômico-financeira
   - Regularidade fiscal

4. Critérios de Julgamento
   - Pontuação técnica
   - Fórmula de combinação (se técnica e preço)

5. Anexos
   - Projeto básico/executivo
   - Planilha orçamentária
   - Cronograma físico-financeiro
   - Minuta de contrato
```

### 2. Checklist de Análise

#### 2.1 Análise Preliminar

- [ ] **Prazo de entrega da proposta é viável?**
  - Tempo suficiente para visita técnica
  - Tempo para elaboração de proposta técnica
  - Tempo para cotação de preços

- [ ] **Objeto está claramente definido?**
  - Escopo bem delimitado
  - Quantitativos conferem com projeto
  - Especificações técnicas completas

- [ ] **Empresa atende requisitos de habilitação?**
  - Certidões fiscais em dia
  - Atestados técnicos compatíveis
  - Índices financeiros adequados

#### 2.2 Análise do Projeto

- [ ] **Projeto está completo?**
  - Plantas, cortes, detalhes
  - Especificações técnicas
  - Memorial descritivo
  - Sondagens (se fundações)

- [ ] **Quantitativos estão corretos?**
  - Conferir amostragem (10-20% dos itens)
  - Verificar unidades de medida
  - Identificar omissões ou duplicidades

- [ ] **Orçamento de referência é realista?**
  - Comparar com SINAPI/SICRO
  - Verificar BDI aplicado
  - Identificar itens sub ou superfaturados

#### 2.3 Análise de Riscos

**Riscos Técnicos:**
```python
def analisar_riscos_tecnicos(edital: dict) -> list:
    """
    Identifica riscos técnicos no edital.
    
    Returns:
        Lista de riscos com severidade e mitigação
    """
    riscos = []
    
    # Verificar prazo de execução
    if edital.get('prazo_meses', 0) < edital.get('prazo_minimo_estimado', 0):
        riscos.append({
            'tipo': 'Prazo',
            'descricao': 'Prazo de execução apertado',
            'severidade': 'Alta',
            'mitigacao': 'Aumentar equipe, trabalhar em turnos, subcontratar'
        })
    
    # Verificar complexidade técnica
    if 'fundacoes_profundas' in edital.get('servicos', []):
        riscos.append({
            'tipo': 'Técnico',
            'descricao': 'Fundações profundas requerem equipamento especializado',
            'severidade': 'Média',
            'mitigacao': 'Subcontratar empresa especializada'
        })
    
    # Verificar condições do terreno
    if not edital.get('sondagem_disponivel', False):
        riscos.append({
            'tipo': 'Geotécnico',
            'descricao': 'Ausência de sondagem SPT',
            'severidade': 'Alta',
            'mitigacao': 'Solicitar sondagem ou prever contingência'
        })
    
    return riscos
```

**Riscos Contratuais:**
- Multas por atraso excessivas (> 0.5% ao dia)
- Retenção de pagamentos elevada (> 10%)
- Reajuste não previsto ou limitado
- Prazo de medição muito longo (> 30 dias)

**Riscos Financeiros:**
- Pagamento apenas após conclusão de etapas
- Garantia contratual elevada (> 5%)
- Antecipação de materiais sem pagamento
- Desconto de ISS na fonte

### 3. Análise de Viabilidade

#### 3.1 Margem de Contribuição

```python
def calcular_viabilidade_proposta(
    custo_direto: float,
    bdi_percentual: float,
    preco_referencia: float,
    desconto_maximo_pct: float = 10.0
) -> dict:
    """
    Analisa viabilidade econômica da proposta.
    
    Args:
        custo_direto: Custo direto total (R$)
        bdi_percentual: BDI a aplicar (%)
        preco_referencia: Preço de referência do edital (R$)
        desconto_maximo_pct: Desconto máximo aceitável (%)
    
    Returns:
        dict com análise de viabilidade
    """
    # Preço com BDI cheio
    preco_bdi_cheio = custo_direto * (1 + bdi_percentual / 100)
    
    # Preço mínimo viável (com desconto máximo)
    preco_minimo = custo_direto * (1 + (bdi_percentual - desconto_maximo_pct) / 100)
    
    # Análise
    if preco_referencia >= preco_bdi_cheio:
        status = 'Viável - Margem cheia'
        desconto_necessario = 0
    elif preco_referencia >= preco_minimo:
        status = 'Viável - Com desconto'
        desconto_necessario = ((preco_bdi_cheio - preco_referencia) / preco_bdi_cheio) * 100
    else:
        status = 'Inviável - Preço abaixo do mínimo'
        desconto_necessario = ((preco_bdi_cheio - preco_referencia) / preco_bdi_cheio) * 100
    
    margem_percentual = ((preco_referencia - custo_direto) / preco_referencia) * 100
    
    return {
        'custo_direto': custo_direto,
        'preco_bdi_cheio': round(preco_bdi_cheio, 2),
        'preco_minimo_viavel': round(preco_minimo, 2),
        'preco_referencia': preco_referencia,
        'desconto_necessario_pct': round(desconto_necessario, 2),
        'margem_percentual': round(margem_percentual, 2),
        'status': status,
        'recomendacao': 'Participar' if 'Viável' in status else 'Não participar'
    }
```

### 4. Pontos de Atenção (Red Flags)

**Alertas Críticos:**

1. **Prazo inexequível**
   - Prazo < 50% do tempo técnico necessário
   - Exemplo: 100.000m² de terraplenagem em 1 mês

2. **Orçamento subdimensionado**
   - Preço de referência < 80% do custo SINAPI
   - BDI < 15% (obras públicas)

3. **Especificações conflitantes**
   - Memorial descritivo ≠ Projeto
   - Planilha ≠ Quantitativos do projeto

4. **Exigências desproporcionais**
   - Atestado técnico > 2x o valor da obra
   - Garantia contratual > 10%

5. **Cláusulas abusivas**
   - Multa > 10% do valor contratual
   - Impossibilidade de reajuste

### 5. Relatório de Análise

**Estrutura do Relatório:**

```markdown
# Relatório de Análise de Edital

## 1. Identificação
- Órgão: [Nome]
- Edital nº: [Número]
- Objeto: [Descrição resumida]
- Valor de referência: R$ [Valor]
- Prazo: [Meses]

## 2. Análise de Conformidade
### 2.1 Habilitação
- ✅ Certidões fiscais em dia
- ✅ Atestados técnicos compatíveis
- ⚠️ Índice de Liquidez Geral: 1.2 (mínimo 1.5)

### 2.2 Projeto
- ✅ Projeto completo
- ⚠️ Quantitativos: divergência de 5% em terraplenagem
- ❌ Sondagem SPT não fornecida

## 3. Análise de Riscos
| Risco | Severidade | Probabilidade | Mitigação |
|-------|------------|---------------|-----------|
| Prazo apertado | Alta | Alta | Aumentar equipe |
| Solo desconhecido | Alta | Média | Solicitar sondagem |

## 4. Análise Econômica
- Custo direto estimado: R$ 1.500.000
- BDI proposto: 25%
- Preço com BDI: R$ 1.875.000
- Preço de referência: R$ 1.800.000
- **Desconto necessário: 4%**
- **Status: VIÁVEL**

## 5. Recomendação
**PARTICIPAR** com as seguintes condições:
- Solicitar prorrogação de prazo de 30 dias
- Exigir fornecimento de sondagem SPT
- Aplicar desconto de 4% no BDI
```

## Outputs Esperados

1. **Checklist de Conformidade**
   - Requisitos atendidos/não atendidos
   - Documentação necessária

2. **Matriz de Riscos**
   - Identificação de riscos
   - Severidade e probabilidade
   - Plano de mitigação

3. **Análise Econômica**
   - Viabilidade financeira
   - Margem de contribuição
   - Desconto máximo aceitável

4. **Relatório Executivo**
   - Recomendação (participar/não participar)
   - Condições e ressalvas
   - Estratégia de proposta

## Referências

- **Lei 8.666/1993** - Licitações e contratos administrativos
- **Lei 14.133/2021** - Nova Lei de Licitações
- **Acórdão TCU 2622/2013** - Orçamento de obras públicas
- **NBR 12721** - Avaliação de custos unitários
