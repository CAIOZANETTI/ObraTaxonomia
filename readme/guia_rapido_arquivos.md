# Guia Rápido - Onde Salvar Arquivos

## 📥 Downloads da Aplicação

Quando você baixar arquivos da página **"4. Apelidar e Validar"**, salve-os nos seguintes diretórios:

### ✅ Orçamento Validado (Completo)
```
Arquivo: orcamento_validado.csv
Salvar em: data/output/validado/
```
**O que é:** Arquivo completo com todos os itens validados. Este é o resultado final do processamento.

---

### ⚠️ Itens para Revisar
```
Arquivo: itens_revisar.csv
Salvar em: data/revisar/inbox/
```
**O que é:** Itens que o sistema marcou como "revisar" - precisam de atenção manual.

**O que fazer:**
1. Abra o arquivo
2. Analise cada item
3. Corrija na aplicação ou na planilha original
4. Mova para: `data/revisar/processados/`
5. Re-processe se necessário

---

### ❓ Desconhecidos
```
Arquivo: desconhecidos.csv
Salvar em: data/desconhecidos/entrada/
```
**O que é:** Itens que o sistema não conseguiu classificar automaticamente.

**O que fazer:**
1. Abra o arquivo
2. Identifique padrões comuns
3. Adicione novos apelidos em `yaml/`
4. Mova para: `data/desconhecidos/processados/`
5. Re-processe o orçamento

---

## 📂 Estrutura Visual

```
data/
│
├── excel/                          # 📥 ENTRADA
│   └── seu_orcamento.xlsx          # Coloque aqui os Excel originais
│
├── output/                         # 📤 SAÍDA
│   ├── validado/                   # ✅ RESULTADO FINAL
│   │   └── orcamento_validado.csv  # Salve aqui o arquivo completo
│   │
│   └── arquivo/                    # 📦 BACKUP
│       └── orcamento_old.csv       # Versões antigas
│
├── revisar/                        # ⚠️ PRECISA ATENÇÃO
│   ├── inbox/                      # 📨 NOVOS
│   │   └── itens_revisar.csv       # Salve aqui itens para revisar
│   │
│   ├── processados/                # ✔️ RESOLVIDOS
│   │   └── itens_resolvidos.csv    # Mova para cá após processar
│   │
│   └── arquivo/                    # 📦 HISTÓRICO
│       └── revisar_old.csv         # Revisões antigas
│
└── desconhecidos/                  # ❓ DESCONHECIDOS
    ├── entrada/                    # 📨 NOVOS
    │   └── desconhecidos.csv       # Salve aqui os desconhecidos
    │
    ├── processados/                # ✔️ RESOLVIDOS
    │   └── desconhecidos_ok.csv    # Mova para cá após processar
    │
    └── arquivo/                    # 📦 HISTÓRICO
        └── desconhecidos_old.csv   # Desconhecidos antigos
```

---

## 🔄 Workflow Completo

### Passo 1: Upload
```
1. Coloque Excel em: data/excel/
2. Abra: streamlit run app/Home.py
3. Faça upload do arquivo
```

### Passo 2: Processar
```
4. Mapear Colunas
5. Normalizar
6. Apelidar e Validar
```

### Passo 3: Baixar e Salvar
```
7. Clique em "📥 Baixar Validado"
   → Salve em: data/output/validado/orcamento_validado.csv

8. Clique em "📥 Baixar Revisar" (se houver)
   → Salve em: data/revisar/inbox/itens_revisar.csv

9. Clique em "📥 Baixar Desconhecidos" (se houver)
   → Salve em: data/desconhecidos/entrada/desconhecidos.csv
```

### Passo 4: Tratar Pendências

#### Se tiver itens para revisar:
```
1. Abra: data/revisar/inbox/itens_revisar.csv
2. Analise e corrija
3. Re-processe na aplicação
4. Mova para: data/revisar/processados/
```

#### Se tiver desconhecidos:
```
1. Abra: data/desconhecidos/entrada/desconhecidos.csv
2. Identifique padrões
3. Adicione apelidos em: yaml/
4. Mova para: data/desconhecidos/processados/
5. Re-processe o orçamento
```

---

## 💡 Dicas

### Nomenclatura Recomendada
```
# Inclua projeto e data
orcamento_validado_OBRA_X_2026-01-25.csv
itens_revisar_OBRA_X_2026-01-25.csv
desconhecidos_OBRA_X_2026-01-25.csv
```

### Backup Antes de Sobrescrever
```powershell
# Mover versão antiga para arquivo
Move-Item data/output/validado/orcamento.csv data/output/arquivo/orcamento_2026-01-25.csv
```

### Limpar Inbox Regularmente
```
⚠️ Não deixe arquivos acumulados em inbox/
   Processe e mova para processados/
```

### Analisar Desconhecidos Periodicamente
```
📊 Revise data/desconhecidos/entrada/ semanalmente
   Desconhecidos são oportunidades de melhorar a taxonomia!
```

---

## ❓ FAQ

**P: Onde salvo o Excel original?**  
R: `data/excel/`

**P: Onde fica o resultado final?**  
R: `data/output/validado/orcamento_validado.csv`

**P: O que fazer com itens "revisar"?**  
R: Salve em `data/revisar/inbox/`, analise, corrija, re-processe e mova para `processados/`

**P: Como melhorar a classificação?**  
R: Analise desconhecidos em `data/desconhecidos/entrada/` e adicione apelidos em `yaml/`

**P: Posso deletar arquivos antigos?**  
R: Sim, mova para `arquivo/` antes. Após 90 dias pode deletar do arquivo.

**P: Qual a diferença entre revisar e desconhecidos?**  
R: **Revisar** = Sistema classificou mas tem baixa confiança. **Desconhecidos** = Sistema não conseguiu classificar.

---

## 📞 Precisa de Ajuda?

Consulte a documentação completa:
- [README.md](../README.md) - Visão geral
- [estrutura_diretorios.md](estrutura_diretorios.md) - Detalhes completos
- [arquitetura.md](arquitetura.md) - Como funciona o sistema
