PROMPT — PYTHON (MOTOR DE TAXONOMIA)
GERAR taxonomia.csv A PARTIR DOS YAMLs EM /yaml + CHECAGEM DE SANIDADE + RELATÓRIO DE ERROS

Você é um desenvolvedor Python (padrão produção) e deve implementar um motor que:

1. percorre recursivamente um diretório `yaml/` com múltiplas subpastas (ex.: `elementos/`, `equipamentos/`, `estruturas/`, `grupos/`, `mao_obra/`, `materiais/`, `obras/`, `servico/`, `unidades/`)
2. valida a sanidade/consistência dos arquivos YAML
3. consolida tudo em um único arquivo `taxonomia.csv` que será o “cérebro” de reconhecimento do sistema (usado para reconhecer dados em CSVs carregados, principalmente via colunas de descrição e unidade)
4. persiste também um relatório técnico de sanidade (ex.: `sanidade_taxonomia.json`) com erros, warnings e estatísticas

Restrições:

1. Tudo em Python. Pode usar `pathlib`, `json`, `re`, `hashlib`, `dataclasses` (opcional), `pandas`, `numpy`.

2. Para ler YAML, usar `pyyaml` (yaml.safe_load). Se quiser melhor rastreio de linha/coluna, pode usar `ruamel.yaml` opcionalmente, mas manter fallback.

3. Não inventar dados: apenas consolidar o que está nos YAMLs. Quando algo estiver ausente/inconsistente, registrar no relatório e seguir (modo tolerante) ou falhar (modo estrito) conforme configuração.

4. A saída `taxonomia.csv` deve ser reprodutível (mesma ordenação, mesmas colunas, mesma serialização).

5. OBJETIVO DO taxonomia.csv

O `taxonomia.csv` deve permitir que um motor de reconhecimento, dado:

* uma `descricao` (texto livre de planilha carregada)
* uma `unidade` (texto livre, ex.: “m2”, “m²”, “metro quadrado”, “un”, “UND”, etc.)
  consiga pontuar qual item de taxonomia é o candidato mais provável (por apelido, sinônimos e unidade compatível).

Portanto, a taxonomia precisa concentrar, no mínimo:

1. chave única (apelido)

2. nome “canônico”

3. tipo/categoria (de qual pasta veio: material, serviço, equipamento etc.)

4. unidades aceitas (e unidade base, se existir)

5. lista de sinônimos/alternativas para match textual

6. metadados de origem (arquivo, caminho, versão/commit se existir, hash) para auditoria

7. DESCOBERTA E LEITURA DOS YAMLs

Entrada: `yaml_dir` (ex.: `./yaml`)

Regras de descoberta:

1. Percorrer recursivamente todos os arquivos com extensão `.yaml` e `.yml`.

2. Ignorar arquivos temporários e ocultos (ex.: iniciados por `.`).

3. Registrar no relatório: total de arquivos encontrados, total lidos, total ignorados.

4. SUPORTE A FORMATOS DE YAML (FLEXÍVEL)

Os YAMLs podem ter formatos diferentes. O motor deve suportar pelo menos estes padrões:

Padrão 1 (lista de itens):

* [ {item...}, {item...} ]

Padrão 2 (dicionário com chave raiz):

* { itens: [ {item...}, ... ] }
* { data:  [ {item...}, ... ] }

Padrão 3 (dicionário por apelido):

* { apelido_1: {campos...}, apelido_2: {campos...} }

O código deve normalizar tudo para uma lista final de “registros” (records) tabulares.

4. ESQUEMA CANÔNICO DO REGISTRO (NORMALIZAÇÃO DE CAMPOS)

Cada item de taxonomia deve virar um record com estes campos mínimos (colunas do CSV), nesta ordem:

1. apelido
2. nome
3. categoria
4. grupo
5. unidade_base
6. unidades_aceitas
7. sinonimos
8. alternativas
9. spec_json
10. tags
11. origem_arquivo
12. origem_caminho
13. origem_hash
14. origem_mtime
15. status_item

Definições:

* apelido: string, obrigatório, único globalmente
* nome: string, obrigatório
* categoria: derivada da subpasta (ex.: “materiais”, “servico”, “equipamentos”, “mao_obra”, “elementos”, “estruturas”, “obras”, “grupos”, “unidades”)
* grupo: opcional, mas se existir nos YAMLs deve ser trazido; se não houver, preencher vazio
* unidade_base: string (canônica), opcional, mas recomendado quando existir “unidades” (ex.: m, m2, m3, un, kg, h)
* unidades_aceitas: string serializada (ex.: “m2|m²|metro quadrado”) ou JSON string; manter padrão fixo
* sinonimos: string serializada (pipe-separated) contendo sinônimos para match
* alternativas: string serializada (pipe-separated) contendo termos alternativos (variações usuais, grafias, abreviações)
* spec_json: JSON string; se não existir, vazio
* tags: string serializada (pipe-separated)
* origem_arquivo: nome do arquivo YAML
* origem_caminho: caminho relativo a `yaml_dir`
* origem_hash: sha1 do conteúdo do arquivo (para auditoria)
* origem_mtime: timestamp (opcional)
* status_item: “ok” | “warn” | “error” (por item, não por arquivo)

Observação: não “limpar” o conteúdo sem necessidade. Apenas padronizar tipos (string/list) e serializar listas de forma consistente.

5. CHECAGENS DE SANIDADE (OBRIGATÓRIO)

O motor deve validar em dois níveis: arquivo e item.

5.1) Sanidade de arquivo YAML
Para cada arquivo:

1. YAML parseável (sem erro de sintaxe)
2. Estrutura suportada (padrões acima)
3. Se falhar: registrar `status=error` do arquivo, guardar mensagem e seguir para o próximo (modo tolerante)

5.2) Sanidade de item
Para cada item extraído:

1. `apelido` existe, é string, não vazia
2. `nome` existe, é string, não vazia
3. `apelido` único global (entre todos os arquivos)
4. Campos de lista (`sinonimos`, `alternativas`, `tags`, `unidades_aceitas`) devem ser lista de strings ou string; normalizar para lista
5. Unidade: se o item declara unidade(s), validar contra o dicionário de `unidades/` quando existir.
6. Se houver `grupo`, validar se esse grupo existe nos YAMLs de `grupos/` (se aplicável).
7. Duplicidades:

   1. sinônimos duplicados dentro do mesmo item devem ser removidos (registrar warning)
   2. se o mesmo sinônimo aparecer em itens diferentes, registrar warning de colisão (não bloquear por padrão)
8. Se `spec_json` existir, validar se é dict ou string JSON parseável; persistir como JSON string canônica (json.dumps sort_keys=True)

Modo estrito vs tolerante (parametrizável):

* tolerante (default): gera `taxonomia.csv` com itens ok e itens warn; itens error são excluídos do CSV e vão para o relatório
* estrito: qualquer erro em arquivo ou item aborta o processo (exit code != 0)

6. CONSOLIDAÇÃO E OUTPUT

6.1) DataFrame final

1. Montar `df_taxonomia` com todos os records ok/warn
2. Ordenação determinística: por `categoria`, depois `grupo`, depois `apelido`
3. Garantir que todas as colunas existam (preencher vazio quando faltar)

6.2) taxonomia.csv

1. Salvar em UTF-8
2. Separador padrão vírgula
3. Sem índice
4. Nome do arquivo: `taxonomia.csv` (fixo) ou configurável via CLI

6.3) Relatório sanidade_taxonomia.json
Salvar um JSON com:

1. stats gerais (arquivos lidos, itens ok/warn/error)

2. lista de erros por arquivo (mensagem, stack reduzido, caminho)

3. lista de erros por item (apelido se existir, arquivo, motivo)

4. lista de warnings (colisões de sinônimos, unidade desconhecida, campos ausentes etc.)

5. top N colisões de sinônimos e contagem

6. CAMADA DE RECONHECIMENTO (PREPARAÇÃO PARA O MOTOR)

Além do CSV “bruto consolidado”, criar também colunas auxiliares para facilitar match (sem interpretar o mundo, só preparar):

1. descricao_tokens (derivado de nome + sinonimos + alternativas)

   * normalização simples:

     * lower
     * remover acentos (unicodedata.normalize)
     * substituir pontuação por espaço
     * colapsar espaços
   * serializar como pipe-separated

2. unidade_norm (derivada de unidade_base e unidades_aceitas normalizadas)

   * ex.: “m²” -> “m2”; “UND” -> “un”

Essas colunas podem ser incluídas no `taxonomia.csv` ou geradas em um `taxonomia__index.csv`. Decidir e manter consistente.

8. INTERFACE DE EXECUÇÃO

Implementar como:

Opção A) CLI

* `python -m obra_taxonomia.build --yaml-dir ./yaml --out ./taxonomia.csv --report ./sanidade_taxonomia.json --strict 0`

Opção B) Função importável

* `build_taxonomia(yaml_dir: str, out_csv: str, out_report: str, strict: bool=False) -> dict`

9. QUALIDADE E TESTES (OBRIGATÓRIO)

10. Criar testes unitários mínimos:

    1. YAML inválido gera erro no relatório e não quebra no modo tolerante
    2. apelido duplicado gera erro por item
    3. item sem nome gera erro por item
    4. serialização determinística (mesmo hash do CSV para mesma entrada)

11. Criar um “smoke test” executando no diretório real `yaml/` e imprimindo resumo final.

12. ENTREGÁVEIS

13. `obra_taxonomia/build.py` (motor principal)

14. `obra_taxonomia/io_yaml.py` (leitura + normalização de estrutura YAML)

15. `obra_taxonomia/validate.py` (regras de sanidade)

16. `obra_taxonomia/serialize.py` (CSV/JSON e normalizações)

17. `taxonomia.csv` gerado

18. `sanidade_taxonomia.json` gerado

19. `README.md` curto com: como rodar, como interpretar relatório, como adicionar novos YAMLs sem quebrar

Critério de sucesso:

1. Rodar no diretório `yaml/` real sem travar (modo tolerante)
2. Gerar `taxonomia.csv` com ordenação determinística
3. Relatório apontar exatamente onde estão problemas (arquivo e item)
4. Garantir apelidos únicos e dados auditáveis por origem

Observação final (importante):
Esse motor não “entende” planilha ainda. Ele só cria o cérebro (taxonomia.csv) e garante que o cérebro não está delirando (sanidade). O reconhecimento das linhas do CSV carregado será outra etapa do sistema.
