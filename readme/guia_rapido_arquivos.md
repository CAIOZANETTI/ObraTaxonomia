# Guia Rápido - Onde Salvar Arquivos

## 📥 PASSO 1: Baixar da Aplicação → `data/uploads/`

Quando você baixar arquivos da página **"4. Apelidar e Validar"**, salve TODOS em `data/uploads/`:

| Botão | Arquivo | Salvar em |
|-------|---------|-----------|
| 📥 Baixar Validado | `orcamento_validado.csv` | `data/uploads/validado/` |
| 📥 Baixar Revisar | `itens_revisar.csv` | `data/uploads/revisar/` |
| 📥 Baixar Desconhecidos | `desconhecidos.csv` | `data/uploads/desconhecidos/` |

---

## 📂 PASSO 2: Mover para Destino Final

### ✅ Validado (PRONTO!)
```powershell
# Mover para destino final
Move-Item data/uploads/validado/orcamento_validado.csv data/output/validado/orcamento_PROJETO_2026-01-25.csv
```

### ⚠️ Revisar (PRECISA PROCESSAR)
```powershell
# Mover para inbox
Move-Item data/uploads/revisar/itens_revisar.csv data/revisar/inbox/

# Depois de processar, mover para processados
Move-Item data/revisar/inbox/itens_revisar.csv data/revisar/processados/
```

### ❓ Desconhecidos (PRECISA PROCESSAR)
```powershell
# Mover para entrada
Move-Item data/uploads/desconhecidos/desconhecidos.csv data/desconhecidos/entrada/

# Depois de adicionar ao YAML, mover para processados
Move-Item data/desconhecidos/entrada/desconhecidos.csv data/desconhecidos/processados/
```

---

## 🔄 Fluxo Visual Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. BAIXAR DA APLICAÇÃO                                      │
└─────────────────────────────────────────────────────────────┘
                        ↓
            data/uploads/validado/
            data/uploads/revisar/
            data/uploads/desconhecidos/

┌─────────────────────────────────────────────────────────────┐
│ 2. MOVER PARA DESTINOS                                      │
└─────────────────────────────────────────────────────────────┘
                        ↓
    ┌───────────────┬──────────────┬────────────────┐
    │               │              │                │
    ✅ Validado     ⚠️ Revisar     ❓ Desconhecidos
    │               │              │
    output/         revisar/       desconhecidos/
    validado/       inbox/         entrada/
    (FINAL)         (PROCESSAR)    (PROCESSAR)
                    │              │
                    ↓              ↓
                    revisar/       desconhecidos/
                    processados/   processados/
```

---

## 📁 Estrutura Completa

```
data/
│
├── uploads/                        # 📥 ZONA DE ENTRADA (temporário)
│   ├── validado/                   # Baixe validados aqui
│   ├── revisar/                    # Baixe revisar aqui
│   └── desconhecidos/              # Baixe desconhecidos aqui
│
├── output/                         # 📤 RESULTADO FINAL
│   ├── validado/                   # ✅ Orçamentos finais
│   └── arquivo/                    # 📦 Backups
│
├── revisar/                        # ⚠️ GESTÃO DE REVISÕES
│   ├── inbox/                      # Para processar
│   ├── processados/                # Já processados
│   └── arquivo/                    # Histórico
│
└── desconhecidos/                  # ❓ GESTÃO DE DESCONHECIDOS
    ├── entrada/                    # Para processar
    ├── processados/                # Já processados
    └── arquivo/                    # Histórico
```

---

## 💡 Dicas Importantes

### 1. uploads/ é Temporário
```
⚠️ Não deixe arquivos em uploads/
   Baixe → Mova → Delete de uploads/
```

### 2. Nomenclatura ao Mover
```
# Adicione contexto ao nome:
orcamento_validado_OBRA_X_2026-01-25.csv
itens_revisar_OBRA_X_2026-01-25.csv
desconhecidos_OBRA_X_2026-01-25.csv
```

### 3. Comandos Rápidos
```powershell
# Mover todos os validados
Move-Item data/uploads/validado/*.csv data/output/validado/

# Mover todos os revisar
Move-Item data/uploads/revisar/*.csv data/revisar/inbox/

# Mover todos os desconhecidos
Move-Item data/uploads/desconhecidos/*.csv data/desconhecidos/entrada/

# Limpar uploads
Remove-Item data/uploads/*/*.csv
```

---

## ❓ FAQ

**P: Por que usar uploads/?**  
R: Centraliza downloads em um lugar só. Depois você move conforme processa.

**P: Posso baixar direto para o destino final?**  
R: Pode, mas uploads/ ajuda a organizar e não misturar "recém baixado" com "já processado".

**P: Preciso sempre mover?**  
R: Para validado, sim (é o resultado final). Para revisar e desconhecidos, só se tiver.

**P: O que fazer com uploads/ depois?**  
R: Delete os arquivos após mover. Mantenha a pasta limpa.

**P: Posso deletar arquivos de processados/?**  
R: Sim, mas mova para arquivo/ primeiro. Delete de arquivo/ após 90 dias.

---

## 📞 Precisa de Ajuda?

Consulte a documentação completa:
- [README.md](../README.md) - Visão geral
- [estrutura_diretorios.md](estrutura_diretorios.md) - Detalhes completos
- [estrutura_resumo.md](estrutura_resumo.md) - Resumo visual
