# Tratamento de Itens Desconhecidos (Feedback Loop com IA)

**Objetivo**: Estabelecer um ciclo virtuoso de melhoria contínua onde os itens não reconhecidos pela taxonomia atual não são descartados, mas sim utilizados como combustível para treinar e expandir a base de conhecimento (YAMLs) assistida pelo agente Antigravity.

## 1. O Fluxo do "Refugo de Ouro"

Quando o motor de classificação roda e marca itens como `tax_desconhecido = TRUE`, esses dados representam uma lacuna de conhecimento na taxonomia. Em vez de exigir esforço manual imediato para cada linha, adotamos um processo de "Remediação em Lote" assistido por IA.

### O Processo Cíclico

1.  **Filtragem e Extração**: Durante o processamento da planilha, o sistema identifica e isola automaticamente todas as linhas onde a classificação falhou.
2.  **Persistência (Buffer)**: Esses itens "órfãos" são salvos em uma pasta dedicada (`data/unknowns`), aguardando análise.
3.  **Ingestão pelo Agente (Antigravity)**: O agente de IA lê periodicamente esses arquivos de refugo.
4.  **Verificação Cruzada**: A IA compara os itens desconhecidos contra a estrutura atual de arquivos YAML para entender se é um caso de:
    *   **Sinônimo Faltante**: O conceito já existe, mas o termo usado é novo (ex: "Bêtao" vs "Concreto").
    *   **Conceito Novo**: O item realmente não existe na base e precisa de uma nova regra/classe.
5.  **Proposta de Evolução**: A IA gera um relatório ou diretamente uma sugestão de código (Snippet YAML) para completar a taxonomia.

## 2. Estratégia de Armazenamento

Para organizar a fila de processamento da IA, sugerimos a criação de uma estrutura de diretórios dedicada para logs de erro e aprendizado:

```text
/
├── data/
│   └── unknowns/             # "Caixa de Entrada" da IA
│       ├── 2024-01-15_obra_alpha_unknowns.csv
│       ├── 2024-01-16_obra_beta_unknowns.csv
```

### Formato do Arquivo de Refugo (.csv)

O arquivo deve ser leve, contendo apenas o necessário para o contexto da IA:

| Coluna | Descrição |
| :--- | :--- |
| `descricao_original` | O texto exato que não foi reconhecido. |
| `unidade_original` | A unidade que acompanhava o texto (vital para desambiguação). |
| `frequencia` | Quantas vezes esse item apareceu na planilha (para priorizar correções de alto impacto). |
| `arquivo_origem` | Nome do arquivo original para rastreabilidade. |

## 3. Ação do Agente Antigravity (Prompt de Identificação)

O agente utiliza um prompt especializado para "limpar" essa base. A lógica de operação é:

> **Prompt para o Agente Antigravity**
>
> **Role**: Você é o **Guardião da Taxonomia**. Sua missão é analisar itens desconhecidos e expandir a base de conhecimento YAML sem criar duplicatas ou regras frágeis.
>
> **Task**: Processar o arquivo de entrada (CSV de itens desconhecidos) e gerar snippets YAML para atualização.
>
> **Regras de Leitura (Estrutura YAML Existente)**:
> Ao ler os arquivos na pasta `yaml/`, observe estritamente o seguinte schema:
> ```yaml
> regras:
>   - apelido: "nome_padronizado_unidade"
>     unit: "unidade"
>     contem:
>       - ["termo1", "termo2"] # Grupo de sinônimos (Lógica OR dentro da lista, AND entre listas)
>     ignorar:
>       - ["termo_proibido"]   # Exclusão explícita
> ```
>
> **Passo a Passo da Execução**:
>
> 1.  **Ler o Input**: Carregue o CSV de itens desconhecidos (`descricao` | `unidade`).
> 2.  **Buscar Similaridade (Fuzzy Search)**:
>     *   Para cada item, verifique se já existe um `apelido` semanticamente idêntico nos arquivos YAML existentes.
>     *   *Exemplo*: Se o item é "Concreto Bombeável" e já existe `concreto_bombeamento_m3`, **NÃO** crie uma nova regra. Apenas sugira adicionar "bombeável" na lista `contem`.
> 3.  **Detectar Novos Conceitos**:
>     *   Se o item for um material/serviço totalmente novo (ex: "Manta Geotêxtil Bidim"), crie uma nova entrada completa.
>     *   Defina um `apelido` no padrão `substantivo_qualificador_unidade` (ex: `geotextil_bidim_m2`).
>     *   Preencha `contem` com as palavras-chave mais óbvias.
>     *   Preencha `ignorar` com termos que possam causar confusão (ex: ignorar "asfalto" se for manta de impermeabilização de laje).
> 4.  **Validar Unidade**:
>     *   O `apelido` DEVE terminar com a unidade canônica (`_m3`, `_m2`, `_kg`, `_un`, `_vb`, `_h`).
>     *   Se o input tem unidade "saco" ou "lata", converta mentalmente para a unidade de engenharia (ex: Cimento é `_kg`, Tinta é `_l`) e anote a necessidade de conversão no comentário.
>
> **Output Esperado**:
> Gere um bloco de código Markdown com as alterações sugeridas no formato Diff ou Append:
>
> ```yaml
> # Arquivo: yaml/grupos/impermeabilizacao.yaml
> # Adicionar à regra existente: manta_asfaltica_m2
> contem:
>   - [ ... , "manta aluminizada" ] # Novo termo descoberto
>
> # Nova Regra Sugerida:
> - apelido: manta_liquida_pu_m2
>   unit: m2
>   contem:
>     - ["manta liquida", "poliuretano", "pu"]
>   ignorar:
>     - ["asfalto"]
> ```

## 4. Benefícios do Modelo

*   **Autocorreção**: O sistema aprende com os dados reais do dia a dia.
*   **Zero atrito**: O usuário não precisa parar o trabalho para "cadastrar itens". Ele apenas joga o desconhecido no balde, e a IA processa depois.
*   **Curadoria Inteligente**: A IA remove o trabalho braçal de ler milhares de linhas de erro, apresentando para o humano apenas as decisões estruturais ("Aprovar nova regra para Argamassa Polimérica?").
