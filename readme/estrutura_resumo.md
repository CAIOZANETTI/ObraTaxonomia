# Estrutura de Diretórios - Resumo

## 📁 Estrutura Final (Português)

```
data/
├── excel/                  # 📥 Entrada (Excel originais)
│
├── uploads/                # 📥 ZONA DE ENTRADA (downloads da app)
│   ├── validado/           # Baixe validados aqui
│   ├── revisar/            # Baixe revisar aqui
│   └── desconhecidos/      # Baixe desconhecidos aqui
│
├── output/                 # 📤 RESULTADO FINAL
│   ├── validado/           # ✅ Orçamentos finais
│   └── arquivo/            # 📦 Backups
│
├── revisar/                # ⚠️ GESTÃO DE REVISÕES
│   ├── inbox/              # Para processar
│   ├── processados/        # Já processados
│   └── arquivo/            # Histórico
│
└── desconhecidos/          # ❓ GESTÃO DE DESCONHECIDOS
    ├── entrada/            # Para processar
    ├── processados/        # Já processados
    └── arquivo/            # Histórico
```

## 🎯 Conceito: Zona de Entrada

**uploads/** = Lugar temporário para TODOS os downloads da aplicação

Depois você move para os destinos apropriados conforme processa.

## 📥 Mapeamento de Downloads

| Botão na Aplicação | Arquivo | 1. Baixar em | 2. Mover para |
|-------------------|---------|--------------|---------------|
| 📥 Baixar Validado | `orcamento_validado.csv` | `uploads/validado/` | `output/validado/` |
| 📥 Baixar Revisar | `itens_revisar.csv` | `uploads/revisar/` | `revisar/inbox/` |
| 📥 Baixar Desconhecidos | `desconhecidos.csv` | `uploads/desconhecidos/` | `desconhecidos/entrada/` |

## 🔄 Ciclo de Vida dos Arquivos

### Validado (Resultado Final)
```
uploads/validado/ → output/validado/ (FINAL)
```

### Revisar (Precisa Processar)
```
uploads/revisar/ → revisar/inbox/ → [processar] → revisar/processados/ → revisar/arquivo/
```

### Desconhecidos (Precisa Processar)
```
uploads/desconhecidos/ → desconhecidos/entrada/ → [adicionar YAML] → desconhecidos/processados/ → desconhecidos/arquivo/
```

## 💡 Regras Importantes

1. **uploads/ é temporário** - Mova e delete após processar
2. **Padrão consistente** - revisar/ e desconhecidos/ têm mesma estrutura
3. **Sempre mova** - Não delete direto, mova para processados/ primeiro
4. **Backup** - Mova para arquivo/ antes de deletar (após 90 dias)
