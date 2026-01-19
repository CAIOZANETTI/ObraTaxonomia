PROMPT — STREAMLIT (PÁGINA 2) DETECÇÃO AUTOMÁTICA DE CABEÇALHO POR ABA (DESCRIÇÃO / UNIDADE / QTD / PU / PT)

Você é um desenvolvedor Python especialista em Streamlit e deve implementar a Página 2 (“Detectar Cabeçalhos”) de um app. Entrada da Página 2: o DataFrame consolidado bruto df_all (gerado na Página 1) que contém a coluna obrigatória aba e as demais colunas originais vindas das abas do Excel.

Objetivo: para cada aba, identificar automaticamente:

a linha que representa o cabeçalho (ou a melhor candidata)

o mapeamento de colunas para estes campos-alvo:

descricao

unidade

quantidade

preco_unitario

preco_total

A Página 2 deve mostrar o resultado por aba e permitir ajuste manual (se necessário), mas a primeira entrega é o autodetect.

REGRAS DE ESCOPO
Operar por aba:

for aba in df_all["aba"].unique():

filtrar df_sheet = df_all[df_all["aba"] == aba]

Não assumir que o cabeçalho está na primeira linha.

Não assumir que os nomes de colunas do DataFrame já são o cabeçalho correto (na Página 1 foi carregamento bruto).

A detecção deve ser baseada em uma varredura (scan) das primeiras N linhas da aba (configurável).

INTERFACE (UI) — MÍNIMO NECESSÁRIO
Componentes:

Configurações globais:

“Máx. linhas para varrer por aba” (default 80, min 20, max 300)

“Pontuação mínima para aceitar cabeçalho” (default 0.55)

“Estratégia” (dropdown):

“Somente palavras-chave”

“Palavras-chave + validação por tipo (número/moeda)”

“Palavras-chave + validação por consistência (qtd×pu≈pt)”

Resultado por aba em st.expander(f"Aba: {aba}"):

Linha candidata do cabeçalho (índice relativo na aba)

Score da detecção

Mapeamento encontrado (descricao, unidade, quantidade, preco_unitario, preco_total)

Prévia: mostrar:

a linha do cabeçalho candidata

as 5 linhas seguintes já “interpretadas” (após aplicar o cabeçalho)

DICIONÁRIO DE PALAVRAS-CHAVE (OBRIGATÓRIO)
Criar um dicionário fixo (editável depois) com sinônimos por campo:

CANDIDATOS = { "descricao": [ "descricao", "descrição", "item", "itens", "servico", "serviço", "produto", "nome", "especificacao", "especificação", "material", "insumo" ], "unidade": [ "un", "und", "unid", "unidade", "u.m", "um", "un. med", "un_med", "medida" ], "quantidade": [ "qtd", "qtde", "quantidade", "quantidades", "quant", "qnt", "qte", "volume" ], "preco_unitario": [ "preco unit", "preço unit", "preco unitario", "preço unitário", "p.u", "pu", "valor unit", "vl unit", "unitario", "unitário" ], "preco_total": [ "preco total", "preço total", "total", "valor total", "vl total", "subtotal", "parcial", "valor", "montante" ], }

Regras:

Normalizar texto (lower, remover acentos, remover pontuação, colapsar espaços).

Matching deve aceitar:

substring (“preco unit” dentro de “Preço Unitário (R$)”)

token (“qtd” como célula inteira)

Aceitar variações comuns (R$, (R$), “R$/un”, etc.) sem travar.

HEURÍSTICA DE DETECÇÃO (OBRIGATÓRIA)
Para cada aba:

Selecionar um bloco de varredura:

df_scan = df_sheet.head(N_scan) (N_scan configurável)

Para cada linha i de df_scan, calcular um score_linha:

Cada célula da linha vira string normalizada.

Verificar se a linha contém termos que casam com os grupos do dicionário.

Pontuar por cobertura:

Sugestão de score simples e efetivo:

+1.0 se encontrar um candidato de descricao

+1.0 se encontrar um candidato de quantidade

+0.7 se encontrar um candidato de unidade

+0.7 se encontrar um candidato de preco_unitario

+0.7 se encontrar um candidato de preco_total

Score máximo = 4.1 Normalizar para 0–1: score_norm = score / 4.1

Escolher como cabeçalho a linha com maior score_norm.

Aceitar se score_norm >= threshold (default 0.55).

Se nenhuma linha passar:

status “não detectado”

ainda assim sugerir a melhor candidata com aviso.

MAPEAR COLUNAS PARA OS 5 CAMPOS (OBRIGATÓRIO)
Depois de decidir a linha do cabeçalho i_header:

Usar os valores da linha i_header como nomes de colunas (strings).

Aplicar normalização e tentar mapear cada coluna para um dos 5 campos-alvo:

Para cada coluna_nome, buscar match com CANDIDATOS[campo].

Resolver conflitos:

Se uma coluna casar com múltiplos campos, escolher o campo de maior prioridade:

descricao > quantidade > unidade > preco_unitario > preco_total

Se houver duplicidade (duas colunas batendo em quantidade), escolher a mais forte e marcar a outra como “candidato secundário”.

Gerar um dict final por aba:

resultado[aba] = { "header_row": i_header, "score": score_norm, "map": { "descricao": "nome_coluna_X", "unidade": "nome_coluna_Y", "quantidade": "nome_coluna_Z", "preco_unitario": "nome_coluna_A", "preco_total": "nome_coluna_B" }, "status": "ok | fraco | nao_detectado" }

VALIDAÇÕES OPCIONAIS (MAS RECOMENDADAS)
Se estratégia selecionada incluir validação:

Validação de tipo:

Em linhas abaixo do cabeçalho (ex.: 10 linhas), verificar se:

quantidade tem “cara” de número

preço unitário e total têm “cara” de moeda/número

descrição tem “cara” de texto (alto % de strings não numéricas)

Ajustar score com bônus/penalidade.

Validação de consistência (mais forte, mas opcional):

Checar se em parte das linhas: qtd * pu ≈ pt (tolerância 5–15% por causa de arredondamentos/BDI/descontos).

Se bater em várias linhas, dar bônus.

OUTPUT DA PÁGINA 2
A Página 2 deve produzir para o app:

Um DataFrame “limpo estruturalmente” por aba (ainda sem limpeza de valores), contendo:

aba

descricao, unidade, quantidade, preco_unitario, preco_total

mais colunas extras originais podem ser mantidas opcionalmente

Uma tabela resumo final:

Aba

header_row

score

colunas mapeadas (5 campos)

Persistência em st.session_state:

session_state["header_detection"] = resultado

session_state["df_structured"] = df_structured (consolidado já com as 5 colunas-alvo, quando possível)

RESTRIÇÕES
Não chamar isso de “IA”. É heurística determinística.

Não fazer limpeza avançada nesta página (moeda, separador decimal, etc.) além do mínimo necessário para validação.

Não apagar linhas: se cabeçalho identificado, remover linhas acima do cabeçalho para estruturar; o resto permanece.

 
