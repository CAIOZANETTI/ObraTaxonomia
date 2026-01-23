# Tratamento de itens desconhecidos

Ciclo de melhoria contínua: tudo que não foi reconhecido pela taxonomia vira insumo para evoluir os YAMLs com apoio do agente Antigravity.

## Objetivo

1. Não descartar falhas de reconhecimento (`tax_desconhecido = true`)
2. Agrupar e priorizar desconhecidos (por frequência e unidade)
3. Gerar um pacote de entrada para o Antigravity propor atualizações de YAML
4. Aprovar mudanças (humano no loop)
5. Rodar o build para atualizar `data/master/reconhecimento_master.json`

---

## Onde isso encaixa no fluxo do app

Pipeline resumido:

1. upload excel → conversão para csv em `st.session_state` (`csv_raw`)
2. escolha/validação de colunas (descricao, unidade, quantidade, preço) (`csv_struct`)
3. normalização de texto (`descricao_norm`) (`csv_norm`)
4. reconhecimento (apelido sugerido, score, semelhantes) (`csv_labeled`)
5. validação do usuário (apelido_final + validado) (`csv_validated`)
6. extração e consolidação de desconhecidos (`unknowns`)

Recomendação:

* gerar uma prévia de `unknowns` ao final da etapa 4 (para transparência)
* consolidar e salvar o lote ao final da etapa 5

---

## O que é considerado “desconhecido”

Um item entra em `unknowns` se qualquer condição for verdadeira:

1. `no_match`: nenhum candidato passou no filtro (unidade + must/must_not)
2. `low_score`: houve candidato, mas o melhor score ficou abaixo do limiar (ex.: `< 0.65`)
3. `ambiguous`: top1 e top2 muito próximos (risco alto)
4. `bad_unit`: unidade inválida ou não mapeada (problema de normalização)

Campos úteis para debug:

* `motivo_desconhecido`: `no_match | low_score | ambiguous | bad_unit`
* `top_candidates`: lista curta (apelido + score)

---

## Estrutura de armazenamento

### Diretórios

```
repo/
  data/
    master/
      reconhecimento_master.json
      sanidade_master.json
    unknowns/
      inbox/
      processed/
      archive/
```

Papel de cada pasta:

* `inbox/`: entrada do Antigravity (pronta para consumir)
* `processed/`: lotes já analisados (com resultado/decisão)
* `archive/`: histórico antigo (compactação/backup)

### Naming dos lotes

Formato recomendado:

* `YYYY-MM-DD_HHMM_<origem>_unknowns.jsonl`

Exemplo:

* `2026-01-23_1740_orcamento_tesc_unknowns.jsonl`

Por que `jsonl`:

* cada linha é um objeto json independente
* permite `top_candidates`, motivos, amostras de origem sem virar string
* fácil de anexar por lote e versionar

---

## Formato do lote unknowns (entrada do Antigravity)

Formato recomendado: `jsonl`.

Cada linha:

```json
{
  "descricao_original": "concreto bombeavel fck 30",
  "descricao_norm": "concreto bombeavel fck 30",
  "unidade_original": "m3",
  "unidade_canonica": "m3",
  "frequencia": 12,
  "arquivo_origem": "orcamento_tesc.xlsx",
  "aba_origem": "planilha 1",
  "linha_origem": 153,
  "motivo_desconhecido": "low_score",
  "top_candidates": [
    {"apelido": "concreto_usinado_m3", "score": 0.61},
    {"apelido": "concreto_bombeado_m3", "score": 0.58}
  ]
}
```

Mínimo obrigatório:

* `descricao_original`
* `unidade_original`
* `frequencia`
* `arquivo_origem`

Recomendado:

* `descricao_norm`
* `unidade_canonica`
* `motivo_desconhecido`
* `top_candidates`

---

## Consolidação e deduplicação (antes de salvar)

Antes de escrever em `data/unknowns/inbox/`:

1. normalizar `descricao_original` → `descricao_norm`
2. agrupar por (`descricao_norm`, `unidade_canonica`)
3. somar `frequencia`
4. manter amostras de origem (ex.: top 3 ocorrências com `aba_origem/linha_origem`)
5. ordenar por `frequencia` desc (prioridade)

Objetivo:

* o Antigravity não deve receber 3.000 linhas repetidas com 5 variações de espaço

---

## Operação do agente Antigravity

### Missão

* expandir a base YAML sem criar duplicatas e sem criar regras frágeis

### O que ele lê

1. `data/unknowns/inbox/*.jsonl`
2. árvore `yaml/` atual
3. opcional: `data/master/reconhecimento_master.json` (para acelerar similaridade)

### Saída esperada

Gerar um pacote de propostas aplicável:

1. `patches/` com diffs por arquivo yaml
2. `relatorio.md` com justificativas e riscos

Saída mínima (sempre):

* lista de alterações sugeridas com:

  * arquivo alvo
  * regra alvo (se for extensão)
  * nova regra (se for conceito novo)
  * justificativa

### Regras de decisão (anti-lixo)

1. se o conceito já existe: preferir adicionar sinônimo em `contem`
2. se for conceito novo: criar regra com `contem` e `ignorar` mínimos e sólidos
3. respeitar unidade e padrão do apelido (`*_m3`, `*_m2`, `*_kg`, `*_un`, `_vb`, `_h`)
4. não inventar conversão de unidade: se vier “lata/saco”, registrar observação (conversão é outra etapa)

---

## Humano no loop (aprovação)

Antes de virar YAML oficial:

1. revisar diffs
2. checar duplicidade de `apelido`
3. checar se `contem` ficou genérico demais (risco de falso positivo)
4. checar se `ignorar` cobre confusões óbvias

Depois:

1. aplicar patches em `yaml/`
2. rodar `yaml_to_master(...)`
3. atualizar `data/master/reconhecimento_master.json`

---

## Atualização do master (gatilho prático)

Atualizar sempre que:

1. qualquer YAML for alterado (novo/removido/editado)
2. um lote de unknowns for aprovado e aplicado nos YAMLs

Mecanismo automático recomendado:

* `sanidade_master.json` contém `yaml_fingerprint`
* se o fingerprint atual divergir do salvo, rebuild

---

## Integração mínima no Streamlit (ux limpa)

Componentes úteis:

1. `st.dataframe` (top unknowns por frequência)
2. `st.toggle` (mostrar top N)
3. `st.pills` (filtro por `motivo_desconhecido` e `unidade_canonica`)
4. `st.download_button` (baixar `unknowns.jsonl`)
5. `st.caption` (1 linha: isso alimenta o Antigravity)

Saídas do app:

* principal: `apelidado_validado.csv` (resultado final validado)
* secundária: `unknowns.jsonl` (alimenta IA)
