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

> **Papel**: Você é um Engenheiro de Custos Sênior e Arquiteto de Taxonomia.
>
> **Entrada**: Uma lista de pares `descrição | unidade` que falharam na classificação.
> **Contexto**: O conteúdo atual dos arquivos na pasta `yaml/`.
>
> **Tarefa**:
> 1. Analise cada item desconhecido.
> 2. Tente encontrar uma `classe` existente nos YAMLs que seja semanticamente equivalente.
>    - Se encontrar: Sugira adicionar o termo à lista `match_required` ou `synonyms` dessa classe.
>    - Se a unidade for incompatível (ex: Classificar "Cimento (saco)" em uma regra de "kg"): Sugira uma estratégia de conversão ou alerta.
> 3. Se o item for totalmente novo (ex: uma tecnologia nova de impermeabilização), sugira o esqueleto de uma **nova regra YAML**, definindo `id`, `política de busca` e `tipo`.
>
> **Saída Esperada**: Um relatório de alteração (Diff) para os arquivos YAML.

## 4. Benefícios do Modelo

*   **Autocorreção**: O sistema aprende com os dados reais do dia a dia.
*   **Zero atrito**: O usuário não precisa parar o trabalho para "cadastrar itens". Ele apenas joga o desconhecido no balde, e a IA processa depois.
*   **Curadoria Inteligente**: A IA remove o trabalho braçal de ler milhares de linhas de erro, apresentando para o humano apenas as decisões estruturais ("Aprovar nova regra para Argamassa Polimérica?").
