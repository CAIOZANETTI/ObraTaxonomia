ObraTaxonomia — Especificação Técnica do MVP

Versão: 1.8.0-comprehensive
Objetivo: Motor de normalização determinística para orçamentação, planeamento, compras e controlo de custos de obras.

1. Visão Geral e Contrato de Valor

O sistema foi concebido para resolver o problema endémico da fragmentação de dados ("A Torre de Babel") na construção civil. Atualmente, a mesma descrição de insumo ou serviço (ex.: "Concreto fck 30", "Conc. Estrut. 30MPa", "Concreto Usinado FCK30 Bombeado", "Betoão C25/30") aparece de formas heterogéneas em Orçamentos Executivos, ERPs legados (Sienge, Totvs, SAP) e em extrações de quantitativos de modelos BIM e CAD.

Essa falta de padronização, ou "entropia de dados", impede a inteligência de negócio, tornando impossível a criação de bases históricas confiáveis, a automação de auditorias ou a comparação automática de propostas de fornecedores. Sem normalização, cada obra é uma ilha de dados isolada, incapaz de aprender com as obras anteriores.

O Valor Estratégico para a Engenharia:
Ao normalizar o dado na entrada (ingestão), o sistema habilita três pilares de valor imediato e mitigação de riscos:

Homologação de Fornecedores (Procurement Inteligente):

O Problema: Comparar propostas desiguais. Um fornecedor cota o cimento em "sacos", outro em "toneladas", e um terceiro inclui o frete no preço unitário.

A Solução: O sistema permite comparar "laranjas com laranjas". Garante que um item classificado como cimento_cp2_kg seja comparado apenas com os seus pares, alertando se houver discrepâncias de unidade (ex: conversão implícita de saco para kg).

Histórico de Preços Confiável (Data Lake Limpo):

O Problema: O custo histórico do "m³ de betão/concreto" é frequentemente contaminado por custos acessórios lançados incorretamente na mesma rubrica (ex: taxas de bombeamento, aluguer de vibradores, horas extras de concretagem).

A Solução: O sistema expurga o ruído, separando o material (concreto_estrutural_m3) do serviço (concretagem_lancamento_m3), permitindo projeções de custo baseadas em dados puros.

Auditoria de EAP (WBS Governance):

O Problema: "Custos Ocultos". Itens de infraestrutura pesada lançados em centros de custo de acabamento, ou verbas genéricas escondendo custos diretos para maquilhar o orçamento.

A Solução: A classificação automática atua como um "Raio-X", garantindo a integridade orçamental e sinalizando anomalias de alocação (ex: um item classificado como "estrutura" dentro de um centro de custo de "pintura").

1.1 O Contrato de "Apelido" (A Chave de Ouro)

Para garantir a interoperabilidade entre sistemas distintos (ex: Orçamento vs. Compras vs. Planeamento), todo o apelido gerado deve obedecer estritamente a um formato hierárquico, semântico e legível por humanos. A estrutura segue a lógica fundamental de separação entre Insumo e Serviço.

Formato Canónico: {classe}_{tipo}_{unidade}

Categorias Fundamentais (A Importância do "Tipo de Item"):

A classificação correta do tipo vai além da organização; ela tem implicações tributárias, legais e de gestão de contratos.

Material: O recurso físico tangível entregue na obra.

Implicação: Incidência de impostos sobre circulação de mercadorias (ICMS/IVA), gestão de stock físico, controlo de perdas e desperdício.

Mão de Obra (MO): Funcionários próprios da construtora (Horistas/Mensalistas).

Implicação: Custos de folha de pagamento, Encargos Sociais (LS), alimentação, transporte, EPIs. Não deve ser misturado com empreitada para evitar passivos trabalhistas.

Serviço: Subempreitada ou serviço terceirizado (com ou sem fornecimento de material).

Implicação: Incidência de impostos sobre serviços (ISS), gestão de contratos, medições de avanço físico, retenções técnicas de garantia.

Equipamento: Locação externa ou depreciação de maquinário próprio.

Implicação: Controlo de horímetro, consumo de combustível, manutenção preventiva/corretiva.

Verba: Itens de difícil mensuração unitária ou custos indiretos.

Implicação: Itens de alto risco gerencial (caixas negras) que exigem decomposição futura. Geralmente representam riscos contratuais ou despesas administrativas.

Exemplos Detalhados de Aplicação da Taxonomia:

Material Puro: concreto_estrutural_m3

Contexto: O líquido entregue pelo camião betoneira.

Serviço de Aplicação: concretagem_lancamento_m3

Contexto: O ato de vibrar, sarrafear e curar o concreto (mão de obra ou subempreiteiro).

Equipamento de Apoio: bomba_lanca_h

Contexto: A hora da máquina parada à espera do camião ou a bombear efetivamente.

Mão de Obra Própria: pedreiro_oficial_h

Contexto: O homem-hora do funcionário registado na folha.

Custo Indireto: mobilizacao_canteiro_vb

Contexto: Pacote fechado de despesas iniciais (tapumes, ligações provisórias, contentores).

2. Arquitetura de Dados

A arquitetura foi desenhada para separar a Inteligência de Engenharia (Definição Humana) da Performance Computacional (Processamento de Máquina). Isso garante que o conhecimento técnico permaneça acessível e auditável, enquanto a execução se mantém performante.

2.1 Camada de Definição (Conhecimento de Engenharia)

Os arquivos YAML representam o "Caderno de Critérios" da orçamentação. Eles são a Single Source of Truth (Fonte Única da Verdade). O uso de YAML permite que engenheiros (não programadores) auditem e ajustem as regras usando ferramentas simples de controle de versão (Git), promovendo a colaboração entre equipas.

A. Schema das Regras (geral/*.yaml, edificacao/*.yaml)

regras:
  - id: "conc_est_m3_v1"
    apelido: "concreto_estrutural_m3"
    unit: "m3"            # Unidade volumétrica (referência cruzada obrigatória com unidades.yaml)
    tipo_item: "material" # IMPORTANTE: Define que é compra de insumo físico (Estoque)
    
    # Critérios de Aceite (Match Required - Lógica AND entre linhas, OR dentro da linha)
    # O item deve conter termos do Grupo 1 (Substantivo) E termos do Grupo 2 (Qualificador)
    match_required:
      - ["concreto", "usinado", "c25", "c30", "c-30", "c-40", "betão", "betao"] # Grupo 1: Material e Traço
      - ["fck", "mpa", "bombeavel", "convencional", "armado"]                  # Grupo 2: Especificação Técnica
    
    # Critérios de Exclusão (Defesa Ativa - Hard Filter)
    # Se contiver QUALQUER um destes termos, a regra é descartada imediatamente.
    # Esta é a principal barreira contra a contaminação de dados.
    match_exclude:
      - ["lancamento", "aplicacao", "sarrafeamento", "polimento", "acabamento"] # Evita Serviços
      - ["locacao", "bomba", "caminhao", "betoneira"]                           # Evita Equipamentos
      - ["aditivo", "superplastificante", "fibra", "sílica"]                    # Evita Insumos Químicos separados
      - ["teste", "ensaio", "rompimento", "slump", "laboratorio"]               # Evita Serviços de Controle Tecnológico
    
    # Peso da regra para desempate
    # Regras específicas (ex: Concreto FCK) têm prioridade sobre regras genéricas (ex: Argamassa)
    prioridade: 10


B. Schema de Unidades (unidades.yaml)

Este arquivo é um dicionário de sinónimos. A chave é o valor canónico, a lista contém as variações permitidas no input.

# unidades.yaml
m3: ["m3", "m³", "mc", "metro cubico", "cu.m."]
kg: ["kg", "kilograma", "quilo", "kgf", "ton"] # 'ton' requer conversão numérica posterior (V2)
un: ["un", "und", "pç", "peca", "unidade"]
vb: ["vb", "verba", "gl", "cj", "jogo"]


2.2 Camada de Processamento (CSV - Machine Optimized)

O sistema não lê os YAMLs em tempo de execução para evitar latência de I/O e overhead de parsing. Um script de build dedicado (build_reconhecimento.py) converte a árvore de critérios de engenharia numa tabela de verificação rápida (reconhecimento.csv).

Estrutura Otimizada: Esta tabela funciona como um índice invertido ou tabela hash, otimizada para carregamento direto em Pandas/Polars.

Validação de Build (Fail-Fast): O script deve falhar se houver IDs duplicados ou unidades nos YAMLs de regras que não existam nas chaves do unidades.yaml. Isso impede que regras quebradas cheguem à produção.

2.3 Contrato de Entrada (Excel)

Para o engenheiro de custos, a rastreabilidade é inegociável. O sistema deve ser robusto o suficiente para aceitar a "sujeira" do mundo real (typos, formatações estranhas), mas exigir o mínimo indispensável para operar com segurança.

Coluna

Status

Relevância para Engenharia e Validação

descricao

Obrigatório

O texto descritivo do insumo, serviço ou composição. É a matéria-prima da mineração.

unidade

Obrigatório

Vital para o contexto semântico. Diferencia "Cimento (kg)" de "Cimento (saco 50kg)" ou "Cabo (m)" de "Cabo (kg)". Sem unidade, a classificação é, por definição, um risco inaceitável.

codigo_origem

Recomendado

O ID do insumo no ERP (ex: INS-1020) ou Código da Composição. Permite devolver o dado tratado (apelido) para o sistema de origem via VLOOKUP/PROCV ou API, enriquecendo o legado sem destruir a chave primária original.

custo_unitario

Opcional

O motor ignora para classificação (para evitar viés), mas ajuda o engenheiro a validar visualmente (ex: se o m³ do concreto custa R$ 50,00, a probabilidade estatística diz que é apenas a taxa de bombeamento e não o material).

Nota Técnica (Idempotência): Se o arquivo de entrada já contiver colunas começando por tax_, o sistema deve sobrescrevê-las ou ignorá-las na leitura, garantindo que uma re-classificação não duplique colunas.

2.4 Contrato de Saída (Excel Enriquecido)

O arquivo de saída é uma cópia não destrutiva do original. O sistema preserva integralmente a integridade dos dados primários (colunas originais), anexando colunas de inteligência ("Taxonomy Tags") que permitem filtros rápidos e Pivot Tables no Excel.

tax_apelido: A chave única de classificação gerada.

tax_tipo: Coluna extraída explicitamente (Material, Serviço, Equipamento, MO) para facilitar a análise de incidência de custos e carga tributária.

tax_confianca: Semáforo de qualidade (HIGH, LOW, UNKNOWN, UNIT_MISMATCH).

tax_validado: Check booleano de auditoria (se o dado foi revisto por humano ou aceito automaticamente pela alta confiança).

tax_similares: Lista JSON com as "segundas melhores opções" para auxiliar a correção manual rápida em casos de ambiguidade.

3. Algoritmo de Matching (Lógica de Engenharia Detalhada)

O algoritmo prioriza a precisão (Accuracy) sobre a cobertura (Recall). É preferível um "Falso Negativo" (ficar como Unknown) do que um "Falso Positivo" (classificar errado).

3.1 Normalização Prévia (O Segredo do Sucesso)

Antes de qualquer match, o texto e a unidade passam por limpeza para resolver problemas de formatação:

Regex Sticky Numbers: Na engenharia, números colados a letras têm significados estruturais diferentes e exigem separação correta antes da tokenização:

Resistência: fck30, fck-30 ou c30 → Normalizado para fck 30 (Tokenização separada permite match com regra que exige o valor numérico "30").

Bitolas: 10mm, dn100, ø20 → Normalizado para 10 mm, dn 100.

Traços (Exceção Vital): 1:3 ou 1:2:3 → NÃO DEVE ser separado para 1 3 se for identificado como traço de argamassa. A Regex deve preservar a notação \d+:\d+ como um token único.

Normalização de Unidade (Semântica): Converte a unidade de entrada (ex: M.C., cu.m., Metro Cubico) para a chave canónica (ex: m3) usando unidades.yaml. Se a unidade não puder ser normalizada com segurança (ex: caixa, saco), ela é mantida como está para posterior validação manual.

3.2 O Funil de Decisão (Pipeline)

Para cada linha do Excel, o motor executa os seguintes passos sequenciais:

Filtro de Unidade (Otimização): Seleciona apenas as regras que atendem à unidade normalizada da linha. Se a linha é kg, o sistema ignora instantaneamente todas as regras de m3 ou m. Isso reduz o espaço de busca em ~80%.

Filtro de Exclusão (Defesa - Hard Filter): Se o texto contiver qualquer termo da lista match_exclude da regra, essa regra é descartada imediatamente, independentemente de quantos termos positivos ela tenha.

Exemplo: "Lançamento de Concreto" é eliminado da regra de material por conter "lançamento".

Verificação de Requisitos (Soft Filter): Verifica se todos os grupos definidos em match_required foram satisfeitos. A lógica é: (Pelo menos um token do Grupo 1) AND (Pelo menos um token do Grupo 2).

Cálculo de Score (Ranking):
$$ Score = (Prioridade \times 100) + (TotalTokensMatch \times 10) $$

Lógica: A prioridade define a "classe" de certeza. Regras específicas ganham de regras genéricas por uma ordem de grandeza (fator 100). Os tokens extras servem apenas para desempatar regras dentro da mesma prioridade.

3.3 Critérios de Confiança

HIGH: Vencedor único com margem de score clara (> 20 pontos de diferença do segundo colocado). O sistema confia na escolha.

LOW: Vencedor existe, mas houve empate de score ou margem muito apertada (ambiguidade). Exige validação humana.

UNIT_MISMATCH: O texto bate perfeitamente com uma regra, mas a unidade não (ex: "Cimento" comprado em "litros"). Isso geralmente indica erro de cadastro no ERP.

UNKNOWN: Nenhuma regra satisfeita após todos os filtros.

4. Fluxo de Trabalho e UX (Streamlit)

4.1 Arquitetura de Execução (Cache)

Como o Streamlit re-executa o código a cada interação do utilizador, é vital usar cache para não recarregar os arquivos YAML repetidamente, o que degradaria a performance.

Boot (Start-up): O script classify_excel.py e o carregamento da taxonomia devem ser decorados com @st.cache_resource para manter a estrutura de regras na memória do servidor.

Health Check: Ao iniciar, o sistema valida a integridade dos YAMLs. Se houver erro crítico (sintaxe inválida, referência circular, unidade órfã), exibe o erro na tela e bloqueia o upload de arquivos para evitar contaminação de dados.

4.2 Jornada do Utilizador (Princípio de Pareto)

O fluxo foi desenhado para maximizar a produtividade humana, focando na gestão por exceção.

Upload: O utilizador carrega o Excel "sujo".

Processamento: O sistema processa milhares de linhas em segundos e exibe métricas iniciais (% Sucesso Automático, % Dúvida).

Validação (Foco na Exceção):

O utilizador ativa o filtro "Ver Pendentes".

O sistema esconde os itens VALID_HIGH (que são a maioria, ~80%).

O utilizador foca 100% da atenção em resolver LOW, UNKNOWN e UNIT_MISMATCH.

Utiliza ferramentas de "Edição em Lote" para corrigir grupos de erros repetitivos.

Exportação: Baixa o Excel enriquecido para importar no BI ou devolver ao ERP.

5. Estrutura de Diretórios (GitHub Aligned)

A estrutura de arquivos reflete a organização atual do repositório, otimizada para implantação direta e mimetizando a estrutura de uma EAP (Estrutura Analítica de Projeto).

/
├── .streamlit/             # Configurações de tema e aparência do Streamlit (Branding)
├── app/
│   └── streamlit_app.py    # Interface do Usuário (Frontend) - Ponto de entrada da UX
├── artifacts/              # Artefatos gerados dinamicamente pelo processo de Build
│   ├── reconhecimento.csv  # Tabela hash compilada para performance (O "Cérebro" rápido)
│   └── validacao_report.json # Log de saúde dos YAMLs (Aponta erros de sintaxe antes do boot)
├── scripts/                # Lógica de Negócio, Pipelines e ETL
│   ├── build_reconhecimento.py # Compilador: Transforma regras humanas (YAML) em máquina (CSV)
│   ├── classify_excel.py       # Motor de Classificação: Contém a lógica de Score e Regex
│   └── validate_yaml.py        # Testes de Integridade: Garante que não existem duplicatas
├── yaml/                   # Base de Conhecimento (Regras de Engenharia - Editável por Humanos)
│   ├── unidades.yaml       # Dicionário Canônico de Grandezas e Sinónimos (Vital)
│   ├── router_dominios.yaml # Mapa de navegação e ativação de módulos
│   ├── geral/              # Regras Transversais (Canteiro, Mobilização, Despesas Indiretas)
│   ├── edificacao/         # Regras Verticais (Estrutura, Vedação, Cobertura, Acabamentos)
│   ├── sistemas/           # Instalações Prediais (Elétrica, Hidráulica, HVAC, Incêndio)
│   └── especiais/          # Infraestrutura Pesada (OAE, Túneis, Drenagem, Terraplenagem)
├── tests/                  # Testes Automatizados para garantir estabilidade
│   └── tests_end2end.yaml  # Cenários de regressão (Golden Dataset) para evitar quebras futuras
├── requirements.txt        # Dependências Python (Pandas, Streamlit, PyYAML, etc.)
└── README.md               # Este documento de especificação


6. Roadmap de Evolução

V1 (MVP - Atual): Classificação determinística baseada em palavras-chave e exclusão rígida. Foco em limpar a base, criar confiança no utilizador e estabelecer a governação.

V1.5 (Composições Inteligentes): Capacidade de identificar "Kits" ou "Composições" (ex: "Kit Porta Pronta com Batente e Ferragens") e classificá-los como um item único (porta_kit_cj) em vez de tentar classificar os componentes isolados se a descrição vier aglutinada.

V2 (Integração de Mercado SINAPI/TCPO): Capacidade de cruzar os apelidos gerados internamente com códigos de referência de mercado (SINAPI, TCPO, SICRO). Isso permitirá o benchmark automático de custos da obra contra a média nacional e a análise de desvios.

V3 (IA Assistiva - Human-in-the-loop): Utilização de LLMs (Large Language Models) apenas para sugerir classificações nos itens UNKNOWN persistentes, aprendendo com as correções manuais feitas pelos engenheiros nas versões anteriores para enriquecer o router automaticamente.
