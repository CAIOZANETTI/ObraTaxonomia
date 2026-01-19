PROMPT — STREAMLIT (PÁGINA 3)
NORMALIZAÇÃO + ETL LEVE (COLUNAS/VALORES) + LIMPEZA DE COLUNAS INÚTEIS + PASSO A PASSO AO USUÁRIO
ENTRADA: CSV MASTER BRUTO (GERADO NA PÁGINA 1)
SAÍDA: CSV MASTER NORMALIZADO + LOG DE TRANSFORMAÇÕES

Você é um desenvolvedor Python especialista em Streamlit e deve implementar a Página 3 (“Normalização / ETL”) de um app.
Esta página recebe um CSV master bruto consolidado (gerado na Página 1) e executa uma normalização leve, auditável e reversível.
O objetivo é preparar os dados para reconhecimento e extração semântica em páginas posteriores, sem “inventar” nada.
Observação: conversão/compatibilização de unidades é outra etapa do sistema e não deve existir nesta página.

1. ESCOPO

A Página 3 deve:

1. Carregar o DataFrame bruto `df_all` do `st.session_state` (preferencial) ou permitir upload do CSV master bruto.
2. Exibir ao usuário um fluxo de ETL em passos, com:

   1. o que vai mudar
   2. quantas células/linhas foram afetadas
   3. exemplos antes/depois
3. Permitir que o usuário ligue/desligue etapas (checklist) e reexecute.
4. Executar normalização mínima de forma:

   1. strings em minúsculo (quando aplicável)
   2. remoção de espaços extras
   3. normalização de nomes de colunas (forma, não semântica)
5. Executar limpeza de colunas “sem serventia”, baseado em heurísticas objetivas e configuráveis.
6. Gerar e permitir download de:

   1. `master_normalizado.csv`
   2. `etl_log.json` (ou `.csv`) com o histórico das transformações
7. Persistir tudo em session_state.

Restrições (importante):

1. Nada de reconhecimento semântico aqui.
2. Nada de tratamento de cabeçalho definitivo.
3. Nada de conversão de unidades.
4. Nada de reclassificar materiais/serviços.
5. Tudo deve ser rastreável e reversível via log.

2) ENTRADAS E SAÍDAS

2.1) Entrada (obrigatória)

* `df_all` bruto (concat das abas), contendo a coluna `aba` e colunas variadas (schemas diferentes entre abas).

2.2) Saídas (obrigatórias)

1. `df_norm` (DataFrame normalizado)
2. `csv_norm_bytes` (para download)
3. `etl_steps_df` (tabela de passos executados e métricas)
4. `etl_log` (estrutura detalhada com exemplos antes/depois e contagens)

3) UI / EXPERIÊNCIA (OBRIGATÓRIO)

A Página 3 deve ter:

1. Bloco “Visão geral do bruto”:

   1. shape bruto (linhas × colunas)
   2. lista de colunas disponíveis
   3. dtypes
   4. % de nulos por coluna (top 10)
   5. preview head(20)
2. Bloco “Configuração do ETL” (checklist de etapas + parâmetros):

   1. Normalizar nomes de colunas (ligado por padrão)
   2. Normalizar valores string (ligado por padrão)
   3. Sugerir/remover colunas inúteis (ligado por padrão)
   4. Parsing leve de números (desligado por padrão, pois pode ser sensível)
3. Bloco “Passos e evidências”:

   * cada etapa em um st.expander com:

     1. descrição objetiva
     2. métricas (células alteradas, linhas afetadas, colunas afetadas)
     3. tabela “antes vs depois” (amostra 5–10 linhas)
     4. warnings (se existirem)
4. Botões:

   1. “Executar ETL” (roda pipeline)
   2. “Resetar para bruto” (descarta df_norm e volta a df_all)
5. Final da página:

   1. exibir `etl_steps_df` (resumo)
   2. preview do `df_norm`
   3. download do CSV normalizado
   4. download do log

4) ETAPAS DO ETL (DEFINIÇÃO EXATA)

4.1) Passo 1 — Normalização mínima de nomes de colunas (forma)
Objetivo: deixar colunas previsíveis sem alterar o conteúdo.

Regras:

1. Converter nomes de colunas para string
2. strip
3. lower
4. substituir sequências de espaços por underscore
5. remover caracteres invisíveis e quebras de linha
6. manter unicidade:

   * se colunas duplicarem após normalização, sufixar `__2`, `__3` etc.
7. Não “traduzir” nomes (ex.: não trocar “descrição” por “descricao”). Apenas forma.

Métricas:

* colunas renomeadas (lista)
* total de renomes

4.2) Passo 2 — Normalização de valores string (minúsculo e limpeza)
Aplicar apenas em colunas object/string.

Regras:

1. Processar apenas valores não nulos
2. strip
3. lower
4. colapsar espaços múltiplos para um espaço
5. remover caracteres invisíveis (ex.: \u00A0)
6. Não remover acentos (pode ser toggle opcional, desligado por padrão)
7. Não mexer em colunas que pareçam código/ID (heurística):

   * nomes contendo: “id”, “codigo”, “código”, “cod”, “cpf”, “cnpj”, “ncm”, “gtin”, “sku”
   * nessas, aplicar apenas strip e remoção de invisíveis, sem lower obrigatório (configurável)

Métricas:

* células alteradas por coluna
* exemplos antes/depois

4.3) Passo 3 — Sugestão e remoção de colunas inúteis (com revisão do usuário)
Objetivo: remover colunas que atrapalham e não agregam para etapas seguintes.

A página deve:

1. Gerar uma tabela de sugestão com colunas:

   1. coluna
   2. motivo
   3. % nulos
   4. valores_unicos
   5. manter? (checkbox padrão = manter)
2. O usuário escolhe quais remover (multi-select ou checkboxes).
3. Aplicar remoção e registrar log.

Heurísticas mínimas para “sugerir remoção”:

1. Coluna 100% nula
2. Coluna com 1 valor único (constante) e não é `aba`
3. Coluna com nome parecido com:

   * “unnamed”, “index”, “linha”, “row”, “coluna_vazia”, “sem_nome” (regex)
4. Coluna com altíssima nulidade (> 99,5%) deve ser apenas sugerida, nunca removida automaticamente.

Regras de segurança:

1. Nunca remover `aba`
2. Nunca remover colunas explicitamente marcadas como “manter”
3. Se o usuário não selecionar nada, não remover nada

4.4) Passo 4 — Parsing leve de números (opcional)
Objetivo: facilitar etapas futuras, sem recalcular nada.

Regras:

1. Detectar colunas candidatas a numérico por nome (heurística):

   * contém: “qtd”, “quant”, “preco”, “valor”, “total”, “unit”, “parcial”
2. Parsing seguro (configurável por toggle):

   * strings vazias -> NaN
   * remover espaços
   * padrão BR:

     * remover separador de milhar “.” quando apropriado
     * trocar vírgula por ponto para decimal
3. Não arredondar, não refazer total, não inferir moeda.
4. Se taxa de falha for alta em uma coluna, manter como string e registrar warning.

Métricas:

* colunas convertidas
* % de sucesso de parsing por coluna
* warnings

5. LOG E AUDITORIA (OBRIGATÓRIO)

Criar um log estruturado com:

1. timestamp
2. versão do pipeline (ex.: “p3_etl_v2”)
3. etapas executadas e configurações (toggles)
4. por etapa:

   1. colunas afetadas
   2. células alteradas
   3. linhas afetadas
   4. exemplos antes/depois (amostra)
   5. warnings
5. colunas removidas e motivos
6. hash do input e hash do output (sha1 do CSV)

Mostrar ao usuário:

1. `etl_steps_df`: (etapa, status, cols_affected, cells_changed, warnings_count)
2. expander “Log completo” com o JSON formatado

6) SESSION_STATE (OBRIGATÓRIO)

Persistir em `st.session_state`:

1. df_all (bruto, preservado)
2. df_norm
3. csv_norm_bytes
4. etl_steps_df
5. etl_log
6. etl_config (toggles e decisões do usuário, ex.: colunas removidas, remover_acentos, parse_numeros)

7) FUNÇÕES (OBRIGATÓRIO)

Implementar pipeline em funções puras (testáveis):

1. normalize_colnames(df) -> (df2, step_log)
2. normalize_strings(df, config) -> (df2, step_log)
3. suggest_drop_columns(df) -> suggestions_df
4. drop_columns(df, cols_to_drop) -> (df2, step_log)
5. parse_numeric_columns(df, config) -> (df2, step_log)
6. run_etl(df, config) -> (df_norm, etl_steps_df, etl_log)

8) CRITÉRIOS DE SUCESSO

1. Usuário vê exatamente o que mudou (antes/depois + contagens).
2. CSV normalizado é baixável e auditável.
3. Remoção de colunas é segura e revisável.
4. Não existe conversão de unidades nem semântica.
5. Tudo persiste no session_state para as próximas páginas.
