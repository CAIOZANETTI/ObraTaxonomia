# Estrutura de Diretórios - ObraTaxonomia

## 📁 Estrutura Final (Português)

```
data/
├── excel/                  # 📥 Entrada
│   └── *.xlsx              # Planilhas originais
│
├── master/                 # 🗂️ Taxonomia
│   └── *.json              # Arquivos mestre
│
├── output/                 # 📤 Saída Principal
│   ├── validado/           # ✅ Resultado final
│   └── arquivo/            # 📦 Backup
│
├── revisar/                # ⚠️ Itens para Revisão
│   ├── inbox/              # 📨 Novos
│   ├── processados/        # ✔️ Resolvidos
│   └── arquivo/            # 📦 Histórico
│
└── desconhecidos/          # ❓ Não Identificados
    ├── entrada/            # 📨 Novos
    ├── processados/        # ✔️ Resolvidos
    └── arquivo/            # 📦 Histórico
```

## 🎯 Padrão Consistente

Ambos `revisar/` e `desconhecidos/` seguem a mesma estrutura:

- **inbox/** ou **entrada/** → Arquivos novos baixados da aplicação
- **processados/** → Arquivos já tratados e resolvidos
- **arquivo/** → Histórico antigo (pode ser deletado após 90 dias)

## 📥 Mapeamento de Downloads

| Botão na Aplicação | Arquivo | Salvar em |
|-------------------|---------|-----------|
| 📥 Baixar Validado | `orcamento_validado.csv` | `data/output/validado/` |
| 📥 Baixar Revisar | `itens_revisar.csv` | `data/revisar/inbox/` |
| 📥 Baixar Desconhecidos | `desconhecidos.csv` | `data/desconhecidos/entrada/` |

## 🔄 Ciclo de Vida dos Arquivos

### Revisar
```
inbox/ → [Analisar e corrigir] → processados/ → [Após 30 dias] → arquivo/
```

### Desconhecidos
```
entrada/ → [Adicionar ao YAML] → processados/ → [Após 30 dias] → arquivo/
```

### Validado
```
validado/ → [Antes de sobrescrever] → arquivo/
```
