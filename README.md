# ObraTaxonomia — Repositório de Taxonomia da Engenharia Civil (Texto/Planilha → Chaves Canônicas)

## 1. O que é este repositório

Este repositório é uma base versionável de **taxonomia da engenharia civil**: um conjunto de regras e vocabulários em YAML para transformar descrições livres (texto “sujo”) de itens de obra em uma estrutura padronizada, consistente e integrável.

O resultado principal do processo é gerar uma **chave canônica** (apelido) para cada item, por exemplo:

* `concreto_cad_m3`
* `armadura_kg`
* `geotextil_m2`
* `contencao_solo_m2`

Essa chave canônica funciona como `primary_key` (ou `alias`) para fazer ligação entre diferentes mundos:

* planilhas de orçamento (Excel), bancos de preços e cotações, CPU/compósitos, EAP/WBS, medições e boletins, e relatórios, memoriais e documentos técnicos.

Em resumo: **texto e planilhas entram; estrutura e chaves confiáveis saem.**

---

## 2. O que é “taxonomia” na engenharia civil

### 2.1 Hierarquia do maior para o menor

Na engenharia civil, a taxonomia fica mais útil quando segue uma hierarquia que vai do contexto amplo até a definição que realmente fecha custo, medição e integração. Uma forma prática é pensar em **obra → sistema/estrutura → elemento → método/condição → classe canônica (unidade única)**. Exemplo: **obra rodoviária → viaduto → viga → concretagem → `concreto_estrutural_m3`**. Outro exemplo: **obra portuária → cais → contenção → estaca-prancha → `estaca_prancha_m2`**. Esse encadeamento ajuda a interpretar descrições ambíguas porque o “mesmo material” muda de significado e preço conforme o elemento e o método.

Importante: o ObraLex foca em padronizar a parte mais determinística desse fluxo (método/condição e classe canônica), mas sem perder a relação com obra, sistema e elemento, que podem entrar como metadados para contexto, busca e auditoria.

### 2.2 De onde vem e onde é usado

O conceito de taxonomia vem de áreas que precisaram organizar conhecimento em escala, como biblioteconomia, ciência da informação e modelagem de domínio em software. Na construção civil ele aparece, muitas vezes sem esse nome, em catálogos de insumos, códigos internos, listas de medição contratual, EAP/WBS e composições de custo. O problema é que normalmente essas estruturas nascem fragmentadas: cada obra cria seus próprios nomes, cada cliente mede de um jeito, e o mesmo item vira vários “quase iguais”. O ObraLex consolida esse conhecimento em um repositório versionável (YAML) para que a classificação deixe de ser artesanal e passe a ser reproduzível, auditável e integrável com bancos de preço, CPU e medição.

### 2.3 Por que isso é importante na engenharia civil

Uma taxonomia bem definida reduz erros caros (principalmente de unidade e fator), melhora consistência entre proposta, orçamento e medição, e viabiliza consolidação de bases históricas sem depender de “memória” de quem montou a planilha. Mas o ganho mais subestimado é a **busca eficiente em fontes de dados**: quando você normaliza nomes e unidades em um `primary_key`, você cria um índice estável para procurar, filtrar, agrupar e cruzar informação em diferentes repositórios (planilhas, banco de cotações, CPU, contratos, relatórios e documentos técnicos). Isso acelera análises, torna o ETL mais simples (join por chave canônica em vez de fuzzy matching eterno) e melhora muito qualquer camada de IA de recuperação (RAG), porque a taxonomia vira um “dicionário de aterramento” que conecta linguagem humana ao dado estruturado.

---

## 3. Conceitos principais do ObraLex

### 3.1 Unidade normalizada

Toda unidade textual deve ser normalizada para um código canônico:

* `m3`, `m2`, `m`, `un`, `kg`, `t`, `h`, `vb`

Isso viabiliza validação determinística e evita ambiguidade.

### 3.2 Classe canônica com unidade única (classe de preço)

A unidade mínima de classificação é a **classe canônica**, que deve ter **unidade única**.

Exemplos:

* `armadura_kg` aceita apenas `kg`
* `concreto_submerso_m3` aceita apenas `m3`
* `pre_moldado_un` aceita apenas `un`

Regra de ouro:

* Se a unidade não bate, **não é a mesma classe**.

Estratégias de tratamento:

* Strict (recomendada): marcar `unit_mismatch` e exigir correção.
* Converter segura: converter apenas unidades inequívocas (ex.: `t → kg`, `ft → m`) e registrar a conversão.

### 3.3 Macro-sistemas de obra (roteamento)

Para reduzir ambiguidade e aumentar a precisão, as classes são organizadas por macro-sistemas de obra e o pipeline faz um roteamento inicial para decidir quais regras carregar e aplicar. Na prática, isso evita que termos comuns em diferentes contextos gerem classificações erradas: o mesmo vocabulário pode aparecer em infraestrutura, contenção, fundação, estrutura ou arquitetura/acabamentos, mas o conjunto de classes relevantes e o comportamento de precificação mudam. O roteamento por macro diminui conflitos semânticos, acelera o matching e deixa a curadoria mais controlável.

### 3.4 `primary_key` (apelido) como cola do ecossistema

A chave canônica (`primary_key`) é o identificador estável que transforma descrições humanas em uma referência de dados consistente. Ela conecta um item de planilha (descrição + unidade) a uma classe de preço e, a partir daí, permite cruzar e reutilizar informação em diferentes camadas: tabelas de preço e cotações, composições/CPU, EAP/WBS, medições, boletins e relatórios. Em vez de depender de textos “quase iguais” e comparações aproximadas, o `primary_key` vira o ponto de junção (join) para ETL, dashboards e automações, além de servir como âncora para busca e recuperação de conhecimento em documentos técnicos.

---

## 4. Taxonomia na prática (hierarquia de entendimento)

Uma forma útil de pensar a engenharia civil é por camadas:

1. Obra (estrutura/empreendimento)
2. Sistemas (infra/edificações/saneamento/...)
3. Elementos construtivos (viga, pilar, laje...)
4. Materiais/serviços (concreto, armadura, formas...)
5. Classe de preço (unidade única)

Exemplos de encadeamento (entendimento):

* `viaduto` → `viga` → `concreto` → `concreto_estrutural_m3`
* `barragem` → `vertedouro` → `concreto` → `concreto_massa_m3`
* `cais` → `cortina` → `estaca prancha` → `estaca_prancha_m2`

ObraLex foca em padronizar o nível 4 e 5, mas sem perder a visão do nível 1 a 3.

---

## 5. Elementos construtivos e obras típicas

### 5.1 Elementos construtivos (exemplos)

Em memoriais, projetos e planilhas, é comum que a descrição do item traga (explícita ou implicitamente) o **elemento construtivo** ao qual ele pertence. Exemplos típicos são fundações (sapata, bloco, radier, estaca, tubulão), pilares, vigas (travamento, baldrame, anel, longarina), lajes, paredes (alvenaria, concreto, contenção), pisos e contrapisos, coberturas, escadas, juntas e apoios. Esses elementos ajudam a dar contexto e a orientar a interpretação do texto, mas não substituem a classe canônica: o que fecha precificação e validação continua sendo a combinação de descrição + unidade normalizada → `primary_key`.

### 5.2 Obras/estruturas típicas (exemplos)

No nível de “obra” ou “estrutura”, aparecem empreendimentos e conjuntos típicos como edifícios e galpões industriais, pontes e viadutos, barragens e vertedouros, tanques e reservatórios, silos e armazéns, bases e fundações de equipamentos, cais e píeres, muros e contenções. Essa camada é útil para entendimento, rastreabilidade e organização do conhecimento (por exemplo, “viaduto” normalmente terá vigas, pilares, apoios e juntas), e permite construir encadeamentos do tipo **obra → sistema → elemento → método → classe canônica**. No ObraLex, a obra/estrutura pode entrar como metadado, enquanto a padronização para custo e integração é resolvida pela classe de unidade única.

---

## 6. Estrutura do repositório

O repositório é organizado para permitir evolução modular por macro-sistemas e, ao mesmo tempo, manter um núcleo único de normalização de unidades e roteamento. As pastas de `macro/` devem refletir os grandes conjuntos de engenharia que aparecem no orçamento e na documentação, como **infraestrutura, estrutura, fundação, contenção e arquitetura/edificações**, além de saneamento, elétrica, mecânica, obra marítima e barragens quando aplicável.

Recomendação de pastas:

```text
yaml/
  unidades.yaml
  router_macro.yaml
  geral/
    terraplenagem.yaml
    contencao_solo.yaml
    fundacao.yaml
    concreto_armado.yaml
    estrutura_metalica.yaml
    drenagem.yaml
    urbanizacao.yaml
    edificacao.yaml
    arquitetura.yaml  
  especiais/
    obra_arte.yaml
    saneamento.yaml
    oleo_gas.yaml
    eletrica.yaml
    mecanica.yaml
    obra_mar.yaml
    barragens.yaml
tests/
  tests_end2end.yaml
```

---

## 7. Arquivos YAML

### 7.1 `yaml/unidades.yaml`

Responsável por normalizar unidade (e suportar conversões imperiais no pipeline).

Exemplo:

```yaml
meta:
  nome: unidades
  versao: "0.1.0"

units:
  m3: [m3, "m³", metro cubico, metro cúbico, "m^3"]
  m2: [m2, "m²", metro quadrado, "m^2"]
  m:  [m, metro, metros, ml, metro linear]
  un: [un, und, unidade, peças, pc]
  kg: [kg, quilo, quilograma]
  t:  [t, ton, tonelada]
  h:  [h, hora, hr]
  vb: [vb, verba, global, pacote]
```

### 7.2 `yaml/router_macro.yaml`

Índice leve de roteamento por macro (pode ser expandido para EN/ES).

```yaml
macros:
  obra_mar:
    file: "macro/obra_mar.yaml"
    route_keywords: [dragagem, cais, pier, estaca prancha, enrocamento]

  infraestrutura:
    file: "macro/infraestrutura.yaml"
    route_keywords: [escavacao, aterro, concreto, armacao, formas, contencao, geotextil]

  edificacoes:
    file: "macro/edificacoes.yaml"
    route_keywords: [pintura, piso, porcelanato, forro, drywall, porta, janela]
```

### 7.3 `yaml/macro/<macro>.yaml`

Cada macro contém classes com unidade única e sinônimos/subtipos.

#### Exemplo: `yaml/macro/infraestrutura.yaml`

```yaml
meta:
  macro: infraestrutura

classes:
  concreto_m3:
    unit: m3
    synonyms: [concreto, concretagem, lancamento de concreto, lançamento de concreto]

  concreto_estrutural_m3:
    unit: m3
    synonyms: [concreto estrutural, concreto armado, estrutural]

  concreto_massa_m3:
    unit: m3
    synonyms: [concreto massa, concreto de massa]

  concreto_cad_m3:
    unit: m3
    synonyms: [concreto alto desempenho, cad, high performance concrete, hpc]

  concreto_submerso_m3:
    unit: m3
    synonyms: [concreto submerso, underwater concrete, tremie]

  concreto_fluido_m3:
    unit: m3
    synonyms: [concreto fluido, alta fluidez]

  concreto_estacas_m3:
    unit: m3
    synonyms: [concreto para estaca, concreto de estaca, estaca escavada concretada, tubulão concretado]

  pre_moldado_un:
    unit: un
    synonyms: [pré-moldado, pre moldado, pre-moldado, pré-fabricado, prefabricado, precast, painel, viga pré-moldada, laje pré-moldada]

  armadura_kg:
    unit: kg
    synonyms: [armacao, armação, vergalhao, vergalhão, ca-50, ca50, corte e dobra, estribo]

  geotextil_m2:
    unit: m2
    synonyms: [geotextil, geotêxtil, manta geotextil, bidim]

  contencao_solo_m2:
    unit: m2
    synonyms: [contencao, contenção, cortina, muro de arrimo, solo grampeado, tirante]
    children:
      jet_grouting:
        synonyms: [jet grouting, jet-grouting, cortina de jet]
      estaca_prancha:
        synonyms: [estaca prancha, sheet pile]
      concreto_projetado:
        synonyms: [concreto projetado, shotcrete, talude em concreto projetado]
```

Regras:

* `unit` define a unidade única da classe.
* Se a mesma ideia aparece com outra unidade no seu cadastro, crie outra classe.

---

## 8. Internacionalização e conversões

### 8.1 Idiomas (PT/EN/ES)

Manter a classe canônica invariável e adicionar sinônimos por idioma.

Exemplo:

```yaml
concreto_estrutural_m3:
  unit: m3
  synonyms: [concreto estrutural]
  synonyms_i18n:
    en: [structural concrete]
    es: [hormigón estructural]
```

### 8.2 Conversão de unidades (Imperial → Métrica)

Converter antes de classificar e registrar rastreabilidade.

Colunas recomendadas:

* `quantidade_orig`, `unidade_orig`
* `quantidade_norm`, `unidade_norm`
* `conv_aplicada`

Conversões comuns:

* `in → m`, `ft → m`, `yd → m`
* `ft2 → m2`, `yd3 → m3`
* `lb → kg`

Regra:

* Se houver ambiguidade (ex.: `ton` sem qualificador), marcar para revisão.

---

## 9. Pipeline recomendado (Excel in → Excel out)

### 9.1 Saídas recomendadas

* `unidade_norm`
* `macro`
* `classe` (primary_key)
* `n2` (opcional)
* `status` (`ok`, `unknown`, `unit_mismatch`, `unknown_unit`)
* `debug` (opcional)

### 9.2 Passos

1. Normalizar texto do nome (lower, sem acento, sem pontuação).
2. Normalizar unidade (e converter imperial → métrico quando aplicável).
3. Roteamento de macro por palavras-chave.
4. Filtrar classes por unidade (`classe.unit == unidade_norm`).
5. Matching por sinônimos e, se existir, `children`.
6. Registrar `unknown` e `unit_mismatch` para curadoria.

### 9.3 Ingestão de documentos (memoriais, relatórios, PDFs)

Quando a fonte não for planilha:

1. Extrair texto e tabelas.
2. Segmentar em “linhas classificáveis” (itens, bullets, linhas de tabela).
3. Aplicar o pipeline normal.
4. Devolver estrutura em CSV/Excel/JSON e uma lista de trechos `unknown` para curadoria.

---

## 10. Verificação e qualidade

### 10.1 Testes end-to-end

Arquivo `tests/tests_end2end.yaml` com casos reais.

Exemplo:

```yaml
- input: {nome: "Cortina de jet grouting", unidade: "m²"}
  expected: {macro: infraestrutura, classe: contencao_solo_m2, n2: jet_grouting}

- input: {nome: "Concreto submerso (tremie)", unidade: "m3"}
  expected: {macro: infraestrutura, classe: concreto_submerso_m3}

- input: {nome: "Armação CA-50", unidade: "t"}
  expected: {classe: armadura_kg, status: unit_mismatch}
```

### 10.2 Governança

Toda alteração em YAML deve incluir:

1. ajuste mínimo e específico (evitar sinônimos genéricos)
2. pelo menos 1 teste novo
3. revisão de conflitos (termos que possam afetar outras classes)

---

## 11. Diretrizes de modelagem

1. Classe sempre embute unidade: `nome_unidade`.
2. Separar classes quando preço muda de forma relevante (ex.: `concreto_cad_m3` vs `concreto_m3`).
3. Evitar termos genéricos como sinônimo único (`base`, `suporte`, `montagem`).
4. Preferir `children` (n2) para método/condição quando não justificar uma nova classe.
5. Se o cadastro do cliente medir diferente, criar classe compatível (ex.: `estaca_prancha_m` e `estaca_prancha_m2`).

---

## 12. Próximos passos

1. Completar macros iniciais (infra, edificações, saneamento, elétrica, mecânica, obra_mar, barragens).
2. Criar uma bateria de testes com linhas reais e casos ambíguos.
3. Implementar validador automatizado que gera relatório de `unknown` e `unit_mismatch`.
4. Integrar com Streamlit (upload Excel, classificação, download Excel).
5. Evoluir para atributos (DN, PN, fck, kVA, bitola) quando houver necessidade de precisão adicional.

