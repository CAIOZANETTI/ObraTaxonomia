# Estrutura de Diretórios - ObraTaxonomia

Este documento descreve a organização de diretórios do projeto ObraTaxonomia e onde salvar cada tipo de arquivo.

## 📁 Estrutura Completa (em Português)

```
ObraTaxonomia/
│
├── app/                    # Aplicação Streamlit
│   ├── pages/              # Páginas do fluxo
│   └── Home.py             # Página inicial
│
├── data/                   # Dados e arquivos de trabalho
│   ├── excel/              # 📥 Arquivos Excel originais (entrada)
│   │
│   ├── master/             # 🗂️ Taxonomia mestre e referências
│   │
│   ├── output/             # 📤 Arquivos processados (saída)
│   │   ├── validado/       # ✅ Orçamentos validados finais
│   │   └── arquivo/        # 📦 Versões anteriores (backup)
│   │
│   ├── revisar/            # ⚠️ Itens que precisam revisão
│   │   ├── inbox/          # 📨 Novos itens para revisar
│   │   ├── processados/    # ✔️ Itens revisados e corrigidos
│   │   └── arquivo/        # 📦 Histórico de revisões
│   │
│   └── desconhecidos/      # ❓ Itens não identificados
│       ├── entrada/        # 📨 Novos desconhecidos
│       ├── processados/    # ✔️ Desconhecidos resolvidos
│       └── arquivo/        # 📦 Histórico antigo
│
├── scripts/                # Scripts Python do backend
├── yaml/                   # Definições da taxonomia
├── readme/                 # Documentação
└── requirements.txt        # Dependências
```

## 📥 Onde Salvar Cada Arquivo

### Arquivos de Entrada

| Tipo | Diretório | Descrição |
|------|-----------|-----------|
| **Excel original** | `data/excel/` | Planilhas de orçamento originais |

### Arquivos de Saída (Downloads da Aplicação)

| Arquivo | Diretório Recomendado | Descrição |
|---------|----------------------|-----------|
| **orcamento_validado.csv** | `data/output/validado/` | Orçamento completo validado (resultado final) |
| **itens_revisar.csv** | `data/revisar/inbox/` | Itens que precisam de revisão manual |
| **desconhecidos.csv** | `data/desconhecidos/entrada/` | Novos itens desconhecidos para análise |

### Arquivos de Backup

| Tipo | Diretório | Quando Usar |
|------|-----------|-------------|
| **Versões antigas** | `data/output/arquivo/` | Antes de sobrescrever um validado |
| **Revisões antigas** | `data/revisar/arquivo/` | Itens de revisão já processados |
| **Desconhecidos antigos** | `data/desconhecidos/arquivo/` | Desconhecidos já processados |

## 🔄 Fluxo de Trabalho Recomendado

### 1. Upload e Processamento
```
1. Coloque Excel em: data/excel/
2. Faça upload na aplicação
3. Siga o fluxo: Upload → Mapear → Normalizar → Validar
```

### 2. Validação e Exportação
```
4. Na página "Apelidar e Validar":
   - Revise e valide os itens
   - Baixe "orcamento_validado.csv" → Salve em data/output/validado/
   - Baixe "itens_revisar.csv" → Salve em data/revisar/inbox/
   - Baixe "desconhecidos.csv" → Salve em data/desconhecidos/entrada/
```

### 3. Tratamento de Itens Especiais

#### Para Revisar
```
1. Abra: data/revisar/inbox/itens_revisar.csv
2. Analise os itens manualmente
3. Corrija na aplicação ou na planilha original
4. Mova para: data/revisar/processados/
5. Re-processe se necessário
```

#### Para Desconhecidos
```
1. Abra: data/desconhecidos/entrada/desconhecidos.csv
2. Analise padrões e frequências
3. Adicione novos apelidos em: yaml/
4. Mova para: data/desconhecidos/processados/
5. Re-processe o orçamento
```

## 🎯 Boas Práticas

### Nomenclatura de Arquivos
```
# Validados
orcamento_validado_PROJETO_2026-01-25.csv

# Revisar
itens_revisar_PROJETO_2026-01-25.csv

# Desconhecidos
desconhecidos_PROJETO_2026-01-25.csv
```

### Organização por Projeto
```
data/output/validado/
├── projeto_a/
│   ├── orcamento_validado_2026-01-25.csv
│   └── orcamento_validado_2026-01-20.csv
└── projeto_b/
    └── orcamento_validado_2026-01-25.csv
```

### Backup Antes de Sobrescrever
```powershell
# Mover versão antiga para arquivo
Move-Item data/output/validado/orcamento.csv data/output/arquivo/orcamento_2026-01-25.csv
```

## 📊 Exemplo de Uso Completo

```
1. Upload: data/excel/orcamento_obra_x.xlsx
2. Processar na aplicação
3. Baixar e salvar:
   ✅ data/output/validado/orcamento_obra_x_validado.csv
   ⚠️ data/revisar/inbox/obra_x_revisar.csv (se houver)
   ❓ data/desconhecidos/entrada/obra_x_desconhecidos.csv (se houver)
4. Tratar revisar e desconhecidos
5. Mover processados:
   - data/revisar/processados/obra_x_revisar.csv
   - data/desconhecidos/processados/obra_x_desconhecidos.csv
6. Re-processar se necessário
7. Arquivo final: data/output/validado/orcamento_obra_x_validado.csv
```

## 🔍 Monitoramento

### Verificar Pendências
```powershell
# Quantos arquivos para revisar?
Get-ChildItem data/revisar/inbox/*.csv | Measure-Object

# Quantos desconhecidos novos?
Get-ChildItem data/desconhecidos/entrada/*.csv | Measure-Object
```

### Limpar Arquivos Antigos
```powershell
# Mover arquivos com mais de 30 dias para arquivo
Get-ChildItem data/output/validado/*.csv | 
  Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} |
  Move-Item -Destination data/output/arquivo/
```

## 📝 Notas Importantes

> [!IMPORTANT]
> - **Sempre faça backup** antes de sobrescrever arquivos validados
> - **Não delete desconhecidos** sem antes analisá-los - eles são fonte de melhoria da taxonomia
> - **Organize por projeto** para facilitar rastreamento
> - **Mova para processados** após tratar revisar e desconhecidos

> [!TIP]
> - Use datas no nome dos arquivos (YYYY-MM-DD)
> - Mantenha `data/revisar/inbox/` limpo - processe e mova
> - Revise `data/desconhecidos/entrada/` regularmente para melhorar a taxonomia
> - Use subpastas por projeto para melhor organização

> [!WARNING]
> - Arquivos em `data/*/arquivo/` podem ser deletados após 90 dias
> - Não versione arquivos grandes no Git (use .gitignore)
> - Sempre mova arquivos processados, não delete diretamente
