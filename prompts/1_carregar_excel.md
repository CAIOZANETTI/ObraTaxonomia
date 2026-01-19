PROMPT — STREAMLIT (PÁGINA 1) UPLOAD EXCEL + VARREDURA (LINHAS × COLUNAS) + TABELA RESUMO POR ABA + CONSOLIDAÇÃO + CSV BRUTO ÚNICO COM COLUNA aba

Você é um desenvolvedor Python especialista em Streamlit e deve implementar a Página 1 (“Upload e Conversão”) de um app. Esta página é exclusivamente responsável por carregar um arquivo Excel e gerar um CSV consolidado bruto. Tratamento de cabeçalho/normalização/limpeza será feito em outra página.

ESCOPO
A Página 1 deve:

Permitir upload de Excel (.xlsx e .xls).

Varrer todas as abas do arquivo.

Para cada aba, medir:

Número de linhas
Número de colunas
Status: ok | empty | error
Exibir cada aba em st.expander com:

Linhas, colunas, status
Prévia bruta head(N) se ok
Consolidar todas as abas ok em um DataFrame único df_all, empilhando (concat) e inserindo a coluna obrigatória aba.

Gerar um único CSV bruto e liberar download na própria Página 1.

MÉTODOS DE LEITURA DO EXCEL (OBRIGATÓRIO: NO MÍNIMO 5)
O app deve implementar (e tentar em cascata) no mínimo 5 métodos de leitura, todos em Python, usando bibliotecas como pandas, numpy e leitores de Excel. Regras para todos os métodos:

Não tratar cabeçalho: ler como bruto (preferir header=None quando aplicável).
Não normalizar colunas, não renomear, não limpar valores.
Não falhar o app inteiro por erro em uma aba: marcar aquela aba como error e continuar.
Registrar em sheets_info o método efetivamente usado (ex.: read_method) e, se der erro, o traceback resumido (error_msg).
Métodos mínimos obrigatórios (implementar todos):

Método A) pandas.read_excel por aba (engine conforme extensão)

Para .xlsx: engine="openpyxl"
Para .xls: engine="xlrd" (se disponível)
Leitura por loop de abas, uma a uma.
Método B) pandas.read_excel com sheet_name=None (leitura em lote)

Ler todas as abas de uma vez e obter dict {aba: df}.
Se falhar, cair para outro método.
Método C) pandas.ExcelFile + parse (controlando parsing por aba)

Criar pd.ExcelFile e usar xls.parse(sheet_name=...).
Útil para inspecionar nomes de abas e isolar falhas por aba.
Método D) openpyxl (leitura “python puro” de .xlsx)

Usar openpyxl.load_workbook(bytes_io, data_only=True, read_only=True).
Iterar por ws.iter_rows(values_only=True) e montar DataFrame a partir de lista de listas (pode usar numpy para performance, se quiser).
Apenas para .xlsx.
Método E) xlrd (leitura “python puro” de .xls)

Usar xlrd.open_workbook(file_contents=excel_bytes).
Iterar pelas sheets, ler linhas/colunas, montar DataFrame.
Apenas para .xls.
Observações operacionais:

O sistema deve escolher automaticamente o conjunto de métodos compatíveis com a extensão do arquivo (.xlsx vs .xls).
Se um método falhar globalmente (ex.: não abre o arquivo), tentar o próximo.
Se abrir o arquivo, mas uma aba específica falhar, registrar error só naquela aba e continuar com as demais.
O sistema deve garantir que o inventário de abas (nomes) seja consistente, mesmo se a leitura em lote falhar (fallback para métodos que listem abas).
TABELA RESUMO FINAL (OBRIGATÓRIA E SIMPLES)
Quando o carregamento terminar, antes do download, o app deve mostrar uma tabela simples (DataFrame) com exatamente estas colunas, nesta ordem:

aba (nome da aba)
linhas (número de linhas)
colunas (número de colunas)
Regras:

Cada linha da tabela corresponde a uma aba do Excel.
A tabela deve incluir todas as abas detectadas, mesmo as vazias ou com erro.
Se error, linhas e colunas devem ser 0 e o status fica registrado internamente (ou opcionalmente exibido fora da tabela, mas a tabela deve permanecer com 3 colunas apenas).
A primeira coluna chama aba e contém o nome da aba (não usar índice oculto como “nome da aba”; o nome precisa estar na coluna).
Além da tabela, exibir logo abaixo (texto simples):

Total de linhas no CSV consolidado: <N_total>
Total de colunas no CSV consolidado: <M_total> (opcional, mas útil)
Contagem de abas usadas na consolidação: ok = X, empty = Y, error = Z
CONSOLIDAÇÃO (CSV ÚNICO)
Criar df_all concatenando todas as abas com status ok.

Para cada aba ok, adicionar coluna aba com o nome da aba.

Não tratar cabeçalho, não renomear colunas, não limpar valores.

Permitir união de colunas (abas com schemas diferentes) via concat com sort=False.

O CSV final deve ser:

df_all.to_csv(..., index=False)
Nome sugerido: <nome_arquivo>__consolidado_bruto.csv
RESTRIÇÕES
Nada de tratamento de cabeçalho nesta página.
Nada de padronização de colunas.
Nada de interpretação semântica.
A página termina quando o usuário consegue baixar o CSV consolidado bruto e visualiza o resumo por aba + total de linhas do consolidado.
SESSION_STATE (OBRIGATÓRIO)
Persistir no st.session_state:

excel_bytes
sheets_info (por aba: rows, cols, status, read_method, error_msg opcional)
df_all
csv_all_bytes
df_resumo_abas (a tabela de 3 colunas)
Dica de estrutura (obrigatória como organização de código, sem “efeitos colaterais”):

Função list_sheets(excel_bytes, ext) -> lista de nomes de abas (com fallback)
Função read_sheet(excel_bytes, ext, sheet_name) -> (df, read_method) com cascata de métodos
Função build_summary(sheets_info) -> df_resumo_abas
Função consolidate_ok_sheets(dict_df_ok) -> df_all + csv_all_bytes
