**fluxo de processamento do sistema (end-to-end) — v3 (ux minimalista + mockups + mermaid)**

este documento define o fluxo do obrataxonomia para: (1) upload de excel → (2) conversão imediata para csv no `st.session_state` → (3) validação de colunas pelo usuário → (4) normalização de texto e números → (5) apelidar/classificar via `taxonomia.csv` → (6) listar desconhecidos para evoluir a memória.

1. crítica objetiva do v2 (o que estava bom e o que faltava)

1) bom: pipeline claro e estados separados (`csv_raw`, `csv_struct`, `csv_norm`, `csv_labeled`).
2) faltava ux: o texto dizia o que fazer, mas não mostrava como a tela “se parece” e quais ações o usuário toma.
3) faltava minimalismo: muitos componentes por página aumentam atrito; precisa de um padrão repetível.
4) faltava loop: quando dá erro (coluna errada, quantidade inválida, unidade vazia), o fluxo deveria voltar com instrução curta e visível.

2. regras de ux minimalista (padrão visual)

1) uma coluna principal. sidebar apenas para status e ações raras.
2) cada página tem sempre 3 blocos, nesta ordem:

   1. entrada (um único formulário curto)
   2. resumo (contagens + head/tail)
   3. ação (um botão principal + um secundário)
3) texto curto, sem títulos grandes. usar `st.caption` e `st.help` para instrução.
4) previews sempre iguais: head(10), tail(10) e métricas.
5) “uma decisão por tela”: upload, mapear, normalizar, classificar, fechar memória.
6) sempre ter um botão para limpar sessão.
7) regra prática de widgets:

   1. opções poucas (até ~8): preferir `st.pills` (mais rápido no celular)
   2. opções muitas: preferir `st.selectbox` (pills vira paredão)
   3. 2–3 opções: `st.segmented_control` ou `st.radio` também são bons.

3. contrato de dados (o csv manda)

* regra: o artefato principal na sessão é sempre csv (string ou bytes). dataframe é derivado.
* colunas padrão do sistema (internas):

  * obrigatórias: `descricao`, `unidade`, `quantidade`
  * opcionais: `codigo`, `preco_unit`, `preco_total`
  * técnicas: `id_linha`, `linha_origem`, `aba_origem`
* saída do classificador (runtime): `apelido`, `alternativa`, `score`, `status`, `motivo`.

4. estado mínimo (st.session_state)

* `excel_bytes`
* `sheet_mode` (uma aba | várias abas | concatenado)
* `sheet_selected` (quando aplicável)
* `csv_raw`
* `colmap`
* `csv_struct`
* `csv_norm`
* `csv_labeled`
* `unknowns_csv`
* `audit_log`

5. fluxo geral (mermaid)

```mermaid
graph td
    a[upload excel] --> b[(csv_raw)]
    b --> c[mapear colunas]
    c --> d[(csv_struct)]
    d --> e[normalizar]
    e --> f[(csv_norm)]
    f --> g[apelidar / classificar]
    g --> h[(csv_labeled)]
    h --> i[desconhecidos / memória]
    i --> j[(unknowns_csv)]

    g -->|status=revisar| c
    e -->|normalização zera descrição| e
    c -->|colmap inválido| c
    a -->|reset| a
```

6. páginas (mockup + componentes streamlit + validações)

a regra: cada página descreve (1) objetivo, (2) mockup, (3) componentes streamlit, (4) saídas no session_state, (5) validações.

6.1) página 1 — upload excel → `csv_raw`
objetivo: carregar excel, escolher modo de leitura e gerar `csv_raw`.

mockup (wireframe)

```text
[arquivo]   (st.file_uploader)
[modo]      (st.pills)  uma aba | concatenar abas
[aba]       (st.pills / st.selectbox)   (pills se poucas abas; selectbox se muitas)

resumo
- linhas, colunas, abas detectadas  (st.metric)

preview
- head(10)  (st.dataframe)
- tail(10)  (st.dataframe)

ações
[continuar] (st.button)   [resetar sessão] (st.button)
```

componentes streamlit

* `st.file_uploader`, `st.pills` (modo), `st.pills`/`st.selectbox` (aba)
* `st.metric` (ou `st.caption` + números simples)
* `st.dataframe`
* `st.button`
* sidebar opcional: `st.sidebar.caption` para mostrar “status da sessão”

saídas

* `excel_bytes`, `sheet_mode`, `sheet_selected`, `csv_raw`

validações

1. arquivo vazio: bloquear continuar e mostrar `st.error`.
2. aba sem tabela: warning com `st.warning` + sugestão curta.
3. normalizar nomes de colunas apenas para exibir (ainda não renomeia).

6.2) página 2 — mapear colunas → `colmap` + `csv_struct`
objetivo: o usuário escolhe quais colunas do excel viram o padrão do sistema.

mockup (wireframe)

```text
mapa de colunas
campo padrão | coluna do arquivo
- descricao  | (select)
- unidade    | (select)
- quantidade | (select)
- codigo     | (select opcional)
- preco_unit | (select opcional)
- preco_total| (select opcional)

resumo
- colunas escolhidas + avisos (st.caption)

preview
- head(10) já renomeado (st.dataframe)
- tail(10) já renomeado (st.dataframe)

ações
[aplicar mapa] (st.button)   [voltar] (st.button)
```

componentes streamlit

* preferir uma tabela única editável:

  * `st.data_editor` com `column_config.SelectboxColumn` (melhor quando há muitas colunas)
* alternativa (se poucas colunas no arquivo):

  * `st.pills` por campo padrão (mais rápido no celular)
* preview: `st.dataframe`
* avisos: `st.caption`, `st.warning`, `st.error`

saídas

* `colmap`
* `csv_struct` com: `id_linha`, campos padrão, e (opcional) `aba_origem`

validações

1. impedir duplicidade (mesma coluna mapeada para dois campos obrigatórios).
2. `quantidade` deve ser numérica (ou conversível). se falhar, mostrar % de linhas inválidas.
3. `unidade` vazia: não bloqueia, mas marca warning.

6.3) página 3 — normalizar texto e números → `csv_norm`
objetivo: limpar descrição e saneamento numérico com rastreabilidade.

mockup (wireframe)

```text
regras (compacto)
[ ] minúsculo             (st.checkbox)  default on
[ ] remover stopwords     (st.checkbox)  default on
[ ] limpar pontuação      (st.checkbox)  default on
[ ] normalizar números    (st.checkbox)  default on

resumo
- linhas alteradas por regra (st.caption)

amostra antes/depois
descricao_original | descricao_norm
(st.dataframe)

ações
[aplicar normalização] (st.button)   [voltar] (st.button)
```

componentes streamlit

* `st.checkbox` (4 regras)
* `st.dataframe` para amostra comparativa
* opcional: `st.tabs` com “amostra”, “avisos”, “auditoria”

saídas

* `csv_norm`
* `audit_log` (append de um evento por regra aplicada)

validações

1. se uma regra zera descrição em alguma linha, reverter naquela linha e registrar warning.
2. detectar decimal: `,` vs `.` em quantidade e preços; se ambíguo, pedir validação curta.

6.4) página 4 — apelidar / classificar → `csv_labeled`
objetivo: aplicar `taxonomia.csv` e produzir status (ok, revisar, desconhecido).

mockup (wireframe)

```text
resumo
ok: n   revisar: n   desconhecido: n   (st.metric)

lista (por status)
[abas] ok | revisar | desconhecido   (st.tabs)
- tabela com colunas: descricao_norm, unidade, quantidade, apelido, score, motivo
  (st.dataframe / st.data_editor)

ações
[exportar classificado] (st.download_button)
[continuar] (st.button)   [voltar] (st.button)
```

componentes streamlit

* `st.metric`, `st.tabs`
* `st.dataframe` (mvp) ou `st.data_editor` (se quiser permitir override manual)
* `st.download_button`
* filtros simples: `st.pills` para unidade (se poucas unidades) senão `st.selectbox`, e `st.text_input` para buscar descrição

saídas

* `csv_labeled`

validações

1. múltiplos candidatos com score parecido: marcar `revisar` e explicar em `motivo`.
2. divergência de unidade: marcar `revisar` mesmo com match de texto.
3. se taxonomia tiver `apelido` duplicado: isso é falha de build (bloquear antes, no build).

6.5) página 5 — desconhecidos → `unknowns_csv` + log persistente
objetivo: transformar desconhecidos em backlog de memória com volume e exemplos.

mockup (wireframe)

```text
resumo
desconhecidos: n linhas   (st.metric)

agregado
descricao_norm | unidade | ocorrencias | exemplos
(st.dataframe)

ações
[baixar unknowns.csv] (st.download_button)
[finalizar] (st.button)   [voltar] (st.button)
```

componentes streamlit

* `st.metric`, `st.dataframe`, `st.download_button`, `st.button`
* opcional minimalista: `st.expander` “como melhorar a memória” (texto curto)

saídas

* `unknowns_csv`
* persistência mvp: salvar também em `/data/unknowns/unknowns_aaaa-mm-dd_hhmm.csv`

validações

1. desconhecido raro: manter, mas ordenar por ocorrência para priorizar.
2. permitir export sem fricção (um botão).

7) build da taxonomia (contrato rígido)

* comando: `python -m obra_taxonomia.build`
* outputs: `taxonomia.csv` + `sanidade_taxonomia.json`
* validações mínimas:

  1. unicidade global de `apelido`
  2. unidades válidas (tabela de equivalências)
  3. export determinístico (mesma entrada → mesmo csv)

8. checklist de sanidade (antes de chamar de mvp)

1) sessão reseta sem deixar lixo.
2) usuário consegue terminar o fluxo com apenas 3 decisões: aba, mapa de colunas, confirmar export.
3) cada página tem um único botão principal.
4) todos os previews são consistentes (head/tail/contagem).

