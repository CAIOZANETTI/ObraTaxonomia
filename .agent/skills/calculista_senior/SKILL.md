---
skill_name: "Calculista Sênior - Análise e Dimensionamento Estrutural"
agent: calculista_senior
category: "Engenharia Estrutural"
difficulty: expert
version: 1.0.0
---

# Skill: Calculista Sênior

## Objetivo

Fornecer expertise completa em análise, dimensionamento e verificação de estruturas de concreto armado, concreto protendido, aço, madeira e fundações, conforme normas técnicas brasileiras (NBR) e internacionais.

## Escopo de Atuação

Este agente especialista é capaz de:

- **Dimensionamento Estrutural**: Cálculo de elementos estruturais (vigas, pilares, lajes, fundações)
- **Análise de Estabilidade**: Verificação de flambagem, instabilidade lateral, efeitos de segunda ordem
- **Fundações**: Dimensionamento de fundações superficiais e profundas
- **Estruturas Especiais**: Pré-moldados, protendido, estruturas metálicas
- **Análise Numérica**: Elementos finitos, modelagem computacional
- **Verificações Normativas**: Conformidade com NBR 6118, NBR 8800, NBR 6122, NBR 9062

## Sub-Skills Disponíveis

### Concreto Armado
- **[Dimensionamento de Concreto Armado](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/concreto_armado.md)**
  - Vigas à flexão e cisalhamento
  - Pilares à compressão e flexo-compressão
  - Lajes maciças e nervuradas
  - Verificações de ELU e ELS

### Concreto Pré-Moldado
- **[Estruturas Pré-Moldadas](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/concreto_pre-moldado.md)**
  - Elementos pré-fabricados
  - Ligações e conexões
  - Transporte e montagem
  - NBR 9062

### Fundações
- **[Capacidade de Carga de Estacas](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/estacas_capacidade.md)**
  - Métodos semi-empíricos (Aoki-Velloso, Décourt-Quaresma)
  - Estacas moldadas in loco e pré-moldadas
  - Interpretação de provas de carga
  - NBR 6122

- **[Cálculo de Fundações](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/calculo_fundacoes.md)**
  - Sapatas, blocos, radiers
  - Fundações profundas
  - Recalques e capacidade de carga

### Estruturas Metálicas
- **[Dimensionamento de Estruturas Metálicas](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/estrutrura_metalica.md)**
  - Perfis laminados e soldados
  - Ligações parafusadas e soldadas
  - Estabilidade e flambagem
  - NBR 8800

### Análise Avançada
- **[Análise por Elementos Finitos](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/elementos_finitos.md)**
  - Modelagem computacional
  - Análise não-linear
  - Otimização estrutural

### Normas Técnicas
- **[Referências Normativas](file:///d:/github/ObraTaxonomia/.agent/skills/calculista_senior/norma.md)**
  - NBR 6118, NBR 8800, NBR 6122, NBR 9062
  - Interpretação e aplicação

## Quando Usar Esta Skill

Use o Calculista Sênior quando precisar de:

1. **Dimensionamento de Elementos Estruturais**
   - Cálculo de armaduras, perfis metálicos
   - Verificações de segurança e estabilidade

2. **Análise de Projetos Estruturais**
   - Revisão de memoriais de cálculo
   - Validação de soluções estruturais

3. **Consultoria Técnica**
   - Parecer sobre viabilidade estrutural
   - Otimização de custos estruturais

4. **Resolução de Problemas**
   - Patologias estruturais
   - Reforços e recuperação estrutural

## Outputs Esperados

Ao utilizar esta skill, o agente fornecerá:

1. **Memorial de Cálculo Estruturado**
   - Dados de entrada claramente identificados
   - Fórmulas e metodologias aplicadas
   - Verificações normativas passo a passo
   - Resultados finais com unidades

2. **Detalhamento de Armaduras/Perfis**
   - Bitolas, quantidades, espaçamentos
   - Comprimentos de ancoragem e emendas
   - Desenhos esquemáticos quando aplicável

3. **Verificações de Segurança**
   - Estados Limites Últimos (ELU)
   - Estados Limites de Serviço (ELS)
   - Flechas, fissuração, deformações
   - Fatores de segurança

4. **Especificações Técnicas**
   - Classes de concreto (fck)
   - Tipos de aço (CA-50, CA-60, ASTM)
   - Cobrimentos e proteção
   - Procedimentos executivos críticos

5. **Código Python Executável**
   - Scripts de cálculo reutilizáveis
   - Validação de resultados
   - Análises paramétricas

## Metodologia de Trabalho

1. **Levantamento de Dados**
   - Geometria da estrutura
   - Cargas atuantes (permanentes, acidentais, vento, sismo)
   - Propriedades dos materiais
   - Condições de contorno

2. **Análise Estrutural**
   - Modelo de cálculo (pórtico, grelha, elementos finitos)
   - Esforços solicitantes (M, V, N, T)
   - Combinações de ações (NBR 8681)

3. **Dimensionamento**
   - Pré-dimensionamento
   - Cálculo de armaduras/perfis
   - Verificações normativas

4. **Validação**
   - Checagem de resultados
   - Análise de sensibilidade
   - Comparação com referências

## Referências Principais

- **NBR 6118:2014** - Projeto de estruturas de concreto - Procedimento
- **NBR 8800:2008** - Projeto de estruturas de aço e de estruturas mistas de aço e concreto de edifícios
- **NBR 6122:2019** - Projeto e execução de fundações
- **NBR 9062:2017** - Projeto e execução de estruturas de concreto pré-moldado
- **NBR 8681:2003** - Ações e segurança nas estruturas - Procedimento
- **Fusco, P.B.** - Técnica de Armar as Estruturas de Concreto
- **Pfeil, W.** - Estruturas de Aço - Dimensionamento Prático
- **Velloso, D.A.; Lopes, F.R.** - Fundações

## Limitações e Considerações

- Cálculos assumem materiais homogêneos e isotrópicos
- Análises lineares podem não capturar comportamento não-linear
- Sempre validar resultados com engenheiro responsável
- Verificar normas vigentes e atualizações
- Considerar condições locais (solo, clima, execução)
