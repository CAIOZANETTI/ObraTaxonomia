# Estrutura de Diretórios - ObraTaxonomia

Este documento descreve a organização de diretórios do projeto ObraTaxonomia e onde salvar cada tipo de arquivo.

## 📁 Estrutura Completa

```
ObraTaxonomia/
│
├── app/                    # Aplicação Streamlit
│   ├── pages/              # Páginas do fluxo
│   └── Home.py             # Página inicial
│
├── data/                   # Dados e arquivos de trabalho
│   ├── excel/              # 📥 Arquivos Excel originais (entrada)
│   ├── master/             # 🗂️ Taxonomia mestre e referências
│   ├── output/             # 📤 Arquivos processados (saída)
│   │   ├── validados/      # ✅ Orçamentos validados finais
│   │   ├── revisar/        # ⚠️ Itens que precisam revisão
│   │   └── archive/        # 📦 Versões anteriores (backup)
│   └── unknowns/           # ❓ Gestão de desconhecidos
│       ├── inbox/          # 📨 Novos desconhecidos
│       ├── processed/      # ✔️ Desconhecidos resolvidos
│       └── archive/        # 📦 Histórico antigo
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
| **orcamento_validado.csv** | `data/output/validados/` | Orçamento completo validado (resultado final) |
| **itens_revisar.csv** | `data/output/revisar/` | Itens que precisam de revisão manual |
| **unknowns_antigravity.csv** | `data/unknowns/inbox/` | Novos itens desconhecidos para análise |

### Arquivos de Backup

| Tipo | Diretório | Quando Usar |
|------|-----------|-------------|
| **Versões antigas** | `data/output/archive/` | Antes de sobrescrever um validado |
| **Unknowns antigos** | `data/unknowns/archive/` | Desconhecidos já processados |

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
   - Baixe "orcamento_validado.csv" → Salve em data/output/validados/
   - Baixe "itens_revisar.csv" → Salve em data/output/revisar/
   - Baixe "unknowns_antigravity.csv" → Salve em data/unknowns/inbox/
```

### 3. Tratamento de Itens Especiais

#### Para Revisar
```
1. Abra: data/output/revisar/itens_revisar.csv
2. Analise os itens manualmente
3. Corrija na aplicação ou na planilha original
4. Re-processe se necessário
```

#### Para Desconhecidos
```
1. Abra: data/unknowns/inbox/unknowns_antigravity.csv
2. Analise padrões e frequências
3. Adicione novos apelidos em: yaml/
4. Mova para: data/unknowns/processed/
5. Re-processe o orçamento
```

## 🎯 Boas Práticas

### Nomenclatura de Arquivos
```
# Validados
orcamento_validado_PROJETO_2026-01-25.csv

# Revisar
itens_revisar_PROJETO_2026-01-25.csv

# Unknowns
unknowns_PROJETO_2026-01-25.csv
```

### Organização por Projeto
```
data/output/validados/
├── projeto_a/
│   ├── orcamento_validado_2026-01-25.csv
│   └── orcamento_validado_2026-01-20.csv
└── projeto_b/
    └── orcamento_validado_2026-01-25.csv
```

### Backup Antes de Sobrescrever
```powershell
# Mover versão antiga para archive
Move-Item data/output/validados/orcamento.csv data/output/archive/orcamento_2026-01-25.csv
```

## 📊 Exemplo de Uso Completo

```
1. Upload: data/excel/orcamento_obra_x.xlsx
2. Processar na aplicação
3. Baixar e salvar:
   ✅ data/output/validados/orcamento_obra_x_validado.csv
   ⚠️ data/output/revisar/obra_x_revisar.csv (se houver)
   ❓ data/unknowns/inbox/obra_x_unknowns.csv (se houver)
4. Tratar revisar e unknowns
5. Re-processar se necessário
6. Arquivo final: data/output/validados/orcamento_obra_x_validado.csv
```

## 🔍 Monitoramento

### Verificar Pendências
```powershell
# Quantos arquivos para revisar?
Get-ChildItem data/output/revisar/*.csv | Measure-Object

# Quantos unknowns novos?
Get-ChildItem data/unknowns/inbox/*.csv | Measure-Object
```

### Limpar Arquivos Antigos
```powershell
# Mover arquivos com mais de 30 dias para archive
Get-ChildItem data/output/validados/*.csv | 
  Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} |
  Move-Item -Destination data/output/archive/
```

## 📝 Notas Importantes

> [!IMPORTANT]
> - **Sempre faça backup** antes de sobrescrever arquivos validados
> - **Não delete unknowns** sem antes analisá-los - eles são fonte de melhoria da taxonomia
> - **Organize por projeto** para facilitar rastreamento

> [!TIP]
> - Use datas no nome dos arquivos (YYYY-MM-DD)
> - Mantenha `data/output/revisar/` limpo - processe e delete
> - Revise `data/unknowns/inbox/` regularmente para melhorar a taxonomia

> [!WARNING]
> - Arquivos em `data/output/archive/` podem ser deletados após 90 dias
> - Não versione arquivos grandes no Git (use .gitignore)
