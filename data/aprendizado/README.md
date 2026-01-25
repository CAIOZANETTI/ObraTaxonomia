# Pasta Aprendizado - ObraTaxonomia

## 📚 Objetivo

A pasta `data/aprendizado/` centraliza todos os dados para melhoria contínua da taxonomia. Aqui você salva os arquivos baixados da aplicação que contêm itens marcados para revisão ou desconhecidos.

## 📁 Estrutura

```
data/aprendizado/
├── revisar/                # Itens marcados para revisão
│   └── aprendizado_revisar_*.csv
│
└── desconhecidos/          # Itens não identificados
    └── aprendizado_desconhecidos_*.csv
```

## 📥 Onde Salvar

### Marcados para Revisão
```
Botão: 📥 Marcados Revisar
Arquivo: aprendizado_revisar.csv
Salvar em: data/aprendizado/revisar/
```

**O que são:** Itens que você marcou manualmente na coluna "Revisar?" da aplicação. São itens que você identificou como precisando atenção especial, independente do status automático.

### Desconhecidos
```
Botão: 📥 Desconhecidos
Arquivo: aprendizado_desconhecidos.csv
Salvar em: data/aprendizado/desconhecidos/
```

**O que são:** Itens que o sistema não conseguiu classificar automaticamente (status = "desconhecido").

## 🔄 Workflow

### 1. Marcar Itens para Revisão
```
1. Na página "4. Apelidar e Validar"
2. Revise a lista de itens
3. Marque checkbox "Revisar?" nos itens que precisam atenção
4. Clique "💾 Salvar Alterações na Sessão"
```

### 2. Baixar para Aprendizado
```
5. Clique "📥 Marcados Revisar"
   → Salve em: data/aprendizado/revisar/aprendizado_revisar_PROJETO_2026-01-25.csv

6. Clique "📥 Desconhecidos"
   → Salve em: data/aprendizado/desconhecidos/aprendizado_desconhecidos_PROJETO_2026-01-25.csv
```

### 3. Analisar e Melhorar
```
7. Abra os arquivos salvos
8. Identifique padrões comuns
9. Para revisar: Corrija classificações ou adicione palavras-chave
10. Para desconhecidos: Crie novos apelidos em yaml/
11. Rebuild taxonomia: python scripts/builder.py
12. Re-processe o orçamento
```

## 🎯 Diferença: Revisar vs Desconhecidos

| Aspecto | Revisar | Desconhecidos |
|---------|---------|---------------|
| **Origem** | Marcado manualmente pelo usuário | Identificado automaticamente pelo sistema |
| **Status** | Pode ser "ok", "revisar" ou "desconhecido" | Sempre "desconhecido" |
| **Tem classificação?** | Sim (pode estar errada ou incerta) | Não |
| **Ação** | Validar/corrigir classificação existente | Criar nova classificação |

## 💡 Quando Marcar para Revisão?

Marque um item quando:

- ✅ A classificação parece errada
- ✅ Você tem dúvida sobre a classificação
- ✅ O item é importante e quer validar manualmente
- ✅ Quer estudar esse tipo de item depois
- ✅ Precisa de contexto adicional para decidir

**Não precisa marcar:**
- ❌ Itens com status "ok" e classificação obviamente correta
- ❌ Desconhecidos (já vão para o arquivo de desconhecidos automaticamente)

## 📊 Exemplo de Uso

```
Cenário: Processando orçamento de obra rodoviária

1. Sistema classifica 1000 itens:
   - 850 com status "ok"
   - 100 com status "revisar"
   - 50 com status "desconhecido"

2. Você revisa e marca 15 itens adicionais:
   - 10 que parecem ter classificação errada
   - 5 que quer estudar melhor

3. Downloads:
   📥 Marcados Revisar: 15 itens (os que você marcou)
   📥 Desconhecidos: 50 itens (os que o sistema não classificou)

4. Aprendizado:
   - Dos 15 marcados: 8 estavam errados → ajustar YAMLs
   - Dos 50 desconhecidos: 30 são variações de 3 novos apelidos → criar YAMLs
```

## 🗂️ Organização

### Nomenclatura Recomendada
```
aprendizado_revisar_PROJETO_2026-01-25.csv
aprendizado_desconhecidos_PROJETO_2026-01-25.csv
```

### Limpeza
```
⚠️ Após processar e melhorar a taxonomia:
   - Mova arquivos antigos para subpasta "processados/"
   - Ou delete após 30 dias
   - Mantenha apenas os mais recentes
```

## 📝 Boas Práticas

1. **Seja seletivo** - Não marque tudo, apenas o que realmente precisa atenção
2. **Documente** - Anote por que marcou cada item
3. **Processe regularmente** - Não deixe acumular
4. **Valide melhorias** - Após ajustar YAMLs, re-processe para confirmar
5. **Compartilhe aprendizados** - Documente padrões encontrados

## 🔗 Veja Também

- [README.md](../../README.md) - Visão geral do projeto
- [estrutura_diretorios.md](../../readme/estrutura_diretorios.md) - Organização completa
- [taxonomia.md](../../readme/taxonomia.md) - Como funciona a taxonomia
