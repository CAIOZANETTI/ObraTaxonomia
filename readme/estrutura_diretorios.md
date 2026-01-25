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
│   ├── uploads/            # 📥 ZONA DE ENTRADA - Baixe aqui da aplicação
│   │   ├── validado/       # Orçamentos validados baixados
│   │   ├── revisar/        # Itens para revisar baixados
│   │   └── desconhecidos/  # Desconhecidos baixados
│   │
│   ├── output/             # 📤 Arquivos processados (saída final)
│   │   ├── validado/       # ✅ Orçamentos validados finais
│   │   └── arquivo/        # 📦 Versões anteriores (backup)
│   │
│   ├── revisar/            # ⚠️ Gestão de itens para revisão
│   │   ├── inbox/          # 📨 Itens movidos de uploads/ para processar
│   │   ├── processados/    # ✔️ Itens revisados e corrigidos
│   │   └── arquivo/        # 📦 Histórico de revisões
│   │
│   └── desconhecidos/      # ❓ Gestão de itens não identificados
│       ├── entrada/        # 📨 Itens movidos de uploads/ para processar
│       ├── processados/    # ✔️ Desconhecidos resolvidos
│       └── arquivo/        # 📦 Histórico antigo
│
├── scripts/                # Scripts Python do backend
├── yaml/                   # Definições da taxonomia
├── readme/                 # Documentação
└── requirements.txt        # Dependências
```

## 🎯 Conceito: Zona de Entrada Centralizada

A pasta `data/uploads/` é a **zona de entrada** onde você salva TODOS os arquivos baixados da aplicação. Depois você move eles para os lugares apropriados conforme processa.

### Por que essa estrutura?

1. **Simplicidade**: Um único lugar para salvar downloads
2. **Organização**: Separa "recém baixado" de "em processamento" de "finalizado"
3. **Rastreabilidade**: Fácil ver o que ainda precisa ser processado
4. **Backup**: Sempre tem os originais em uploads/

## 📥 Onde Salvar Cada Arquivo (Downloads)

### Arquivos Baixados da Aplicação → `data/uploads/`

| Arquivo | Salvar em | Descrição |
|---------|-----------|-----------|
| **orcamento_validado.csv** | `data/uploads/validado/` | Orçamento completo validado |
| **itens_revisar.csv** | `data/uploads/revisar/` | Itens que precisam de revisão |
| **desconhecidos.csv** | `data/uploads/desconhecidos/` | Itens não identificados |

## 🔄 Fluxo de Trabalho Completo

### 1. Upload e Processamento
```
1. Coloque Excel em: data/excel/
2. Faça upload na aplicação
3. Siga o fluxo: Upload → Mapear → Normalizar → Validar
```

### 2. Download (da Aplicação)
```
4. Na página "Apelidar e Validar", baixe os arquivos:
   
   📥 Baixar Validado → Salve em: data/uploads/validado/
   📥 Baixar Revisar → Salve em: data/uploads/revisar/
   📥 Baixar Desconhecidos → Salve em: data/uploads/desconhecidos/
```

### 3. Processar Validado
```
5. Arquivo final está pronto!
   
   Mova de: data/uploads/validado/orcamento_validado.csv
   Para: data/output/validado/orcamento_PROJETO_2026-01-25.csv
   
   (Opcional: Backup antigo para data/output/arquivo/)
```

### 4. Processar Revisar (se houver)
```
6. Mova de: data/uploads/revisar/itens_revisar.csv
   Para: data/revisar/inbox/itens_revisar_PROJETO.csv
   
7. Abra e analise o arquivo
8. Corrija na aplicação ou na planilha original
9. Mova para: data/revisar/processados/
10. Re-processe se necessário
```

### 5. Processar Desconhecidos (se houver)
```
11. Mova de: data/uploads/desconhecidos/desconhecidos.csv
    Para: data/desconhecidos/entrada/desconhecidos_PROJETO.csv
    
12. Analise padrões e frequências
13. Adicione novos apelidos em: yaml/
14. Mova para: data/desconhecidos/processados/
15. Re-processe o orçamento
```

## 📊 Exemplo de Uso Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ENTRADA                                                  │
└─────────────────────────────────────────────────────────────┘
data/excel/orcamento_obra_x.xlsx

┌─────────────────────────────────────────────────────────────┐
│ 2. PROCESSAR NA APLICAÇÃO                                   │
└─────────────────────────────────────────────────────────────┘
Upload → Mapear → Normalizar → Validar

┌─────────────────────────────────────────────────────────────┐
│ 3. DOWNLOAD (Zona de Entrada)                               │
└─────────────────────────────────────────────────────────────┘
data/uploads/validado/orcamento_validado.csv
data/uploads/revisar/itens_revisar.csv (se houver)
data/uploads/desconhecidos/desconhecidos.csv (se houver)

┌─────────────────────────────────────────────────────────────┐
│ 4. MOVER E PROCESSAR                                        │
└─────────────────────────────────────────────────────────────┘
✅ Validado:
   uploads/validado/ → output/validado/ (FINAL)

⚠️ Revisar:
   uploads/revisar/ → revisar/inbox/ → [processar] → revisar/processados/

❓ Desconhecidos:
   uploads/desconhecidos/ → desconhecidos/entrada/ → [adicionar YAML] → desconhecidos/processados/

┌─────────────────────────────────────────────────────────────┐
│ 5. RESULTADO FINAL                                          │
└─────────────────────────────────────────────────────────────┘
data/output/validado/orcamento_obra_x_2026-01-25.csv
```

## 🎯 Boas Práticas

### Nomenclatura de Arquivos
```
# Ao mover de uploads/ para destino final, adicione contexto:
orcamento_validado_PROJETO_2026-01-25.csv
itens_revisar_PROJETO_2026-01-25.csv
desconhecidos_PROJETO_2026-01-25.csv
```

### Manter uploads/ Limpo
```
⚠️ uploads/ é temporário!
   Após mover os arquivos, delete de uploads/
   Não deixe arquivos acumulados
```

### Comandos PowerShell Úteis

```powershell
# Mover validado de uploads para output
Move-Item data/uploads/validado/*.csv data/output/validado/

# Mover revisar de uploads para inbox
Move-Item data/uploads/revisar/*.csv data/revisar/inbox/

# Mover desconhecidos de uploads para entrada
Move-Item data/uploads/desconhecidos/*.csv data/desconhecidos/entrada/

# Limpar uploads após mover tudo
Remove-Item data/uploads/*/*.csv
```

## 🔍 Monitoramento

### Verificar Pendências
```powershell
# O que tem em uploads esperando ser movido?
Get-ChildItem data/uploads/*/*.csv

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
> - **uploads/ é temporário** - Mova os arquivos para os destinos apropriados
> - **Sempre faça backup** antes de sobrescrever arquivos validados
> - **Não delete desconhecidos** sem antes analisá-los
> - **Organize por projeto** usando nomes descritivos

> [!TIP]
> - Use datas no nome dos arquivos (YYYY-MM-DD)
> - Mantenha `uploads/` limpo - mova e delete
> - Revise `desconhecidos/entrada/` regularmente
> - Use subpastas por projeto para melhor organização

> [!WARNING]
> - Não versione `uploads/` no Git (é temporário)
> - Arquivos em `*/arquivo/` podem ser deletados após 90 dias
> - Sempre mova arquivos processados, não delete diretamente
