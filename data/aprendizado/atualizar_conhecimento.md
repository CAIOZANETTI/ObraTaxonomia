# Prompt: Atualizar Conhecimento da Taxonomia

## Contexto

Você está analisando arquivos CSV da pasta `data/aprendizado/` para melhorar a taxonomia do ObraTaxonomia. Estes arquivos contêm:

1. **Itens marcados para revisão** - Classificações que precisam correção
2. **Itens desconhecidos** - Itens que o sistema não conseguiu classificar

Seu objetivo é propor atualizações nos arquivos YAML da taxonomia e no arquivo master de reconhecimento.

## Arquivos de Entrada

### 1. Marcados para Revisão
**Localização:** `data/aprendizado/revisar/aprendizado_revisar_*.csv`

**Colunas principais:**
- `descricao_norm` - Descrição normalizada
- `apelido_sugerido` - Classificação atual do sistema
- `status` - Status da classificação (ok/revisar/desconhecido)
- `motivo` - Por que precisa revisão
- `score` - Score de confiança
- `alternativa` - Outras classificações possíveis

### 2. Desconhecidos
**Localização:** `data/aprendizado/desconhecidos/aprendizado_desconhecidos_*.csv`

**Colunas principais:**
- `descricao_norm` - Descrição normalizada
- `unidade` - Unidade de medida
- `quantidade` - Quantidade
- `status` - Sempre "desconhecido"

## Objetivo

Gerar dois tipos de atualizações:

1. **Correções em YAMLs existentes** - Ajustar palavras-chave, prioridades
2. **Novos YAMLs** - Criar apelidos para itens desconhecidos
3. **Atualização do Master** - Melhorar reconhecimento de padrões

## Instruções de Análise

### PARTE 1: Analisar Itens Marcados para Revisão

#### 1.1 Categorizar Problemas

Agrupe os itens por tipo de problema:

**A. Classificação Incorreta**
- Apelido sugerido está completamente errado
- Causa: Falta palavra-chave específica ou palavra-chave genérica demais

**B. Ambiguidade**
- Múltiplas alternativas com scores similares
- Causa: Falta especificidade nas regras

**C. Prioridade Errada**
- Classificação correta existe mas não foi escolhida
- Causa: Ordem de prioridade dos YAMLs

#### 1.2 Propor Correções

Para cada problema, sugira:

```yaml
# Tipo de correção: [ADICIONAR_PALAVRA / REMOVER_PALAVRA / AJUSTAR_PRIORIDADE]
# Arquivo: yaml/[categoria]/[apelido].yaml
# Problema: [descrição do problema]

apelido: [nome_existente]
unit: [unidade]
contem:
  - [palavras_existentes]
  - [NOVA_PALAVRA]  # ← Adicionar para maior especificidade
ignorar:
  - [palavras_ignorar]
  - [NOVA_PALAVRA_IGNORAR]  # ← Adicionar para evitar falsos positivos
```

### PARTE 2: Analisar Itens Desconhecidos

#### 2.1 Agrupar por Similaridade

Identifique grupos de itens similares:

- Palavras-chave comuns
- Mesma unidade
- Mesmo contexto técnico

#### 2.2 Propor Novos Apelidos

Para cada grupo, crie novo YAML:

```yaml
# Novo arquivo: yaml/[categoria]/[novo_apelido].yaml
# Ocorrências: [N] itens
# Justificativa: [por que este apelido é necessário]

apelido: [novo_nome_descritivo]
unit: [unidade_padrao]
contem:
  - [palavra_chave_1]
  - [palavra_chave_2]
  - [palavra_chave_n]
ignorar:
  - [palavra_a_ignorar]
```

### PARTE 3: Atualizar Master de Reconhecimento

#### 3.1 Identificar Padrões Novos

Analise se há padrões que devem ser adicionados ao `data/master/reconhecimento_master.json`:

- Novos sinônimos
- Novas variações de escrita
- Novos contextos técnicos

#### 3.2 Propor Atualizações

```json
{
  "categoria": "[nome_categoria]",
  "padroes_adicionais": [
    {
      "termo": "[novo_termo]",
      "sinonimos": ["variacao1", "variacao2"],
      "contexto": "[quando_usar]"
    }
  ],
  "melhorias": [
    {
      "tipo": "normalizacao",
      "de": "[termo_antigo]",
      "para": "[termo_padrao]",
      "justificativa": "[por_que]"
    }
  ]
}
```

## Formato de Saída

### Resumo Executivo

```markdown
# Análise de Aprendizado - [DATA]

## Estatísticas
- Total de itens marcados para revisão: [N]
- Total de itens desconhecidos: [M]
- Correções propostas em YAMLs existentes: [X]
- Novos YAMLs propostos: [Y]
- Atualizações no master: [Z]

## Impacto Estimado
- Taxa de classificação correta esperada: [%] → [%]
- Itens desconhecidos que serão resolvidos: [N] ([%])
```

### Detalhamento de Correções

```markdown
## 1. Correções em YAMLs Existentes

### 1.1 [Nome do Apelido]

**Arquivo:** `yaml/[categoria]/[arquivo].yaml`
**Problema:** [descrição]
**Ocorrências afetadas:** [N] itens

**Exemplos de itens afetados:**
- [descrição 1]
- [descrição 2]

**Correção proposta:**
```yaml
# Adicionar palavras-chave
contem:
  - [existentes]
  - [NOVA]  # ← Resolver ambiguidade
```

**Validação:**
- [ ] Testar com itens de exemplo
- [ ] Verificar não causa falsos positivos
- [ ] Rebuild taxonomia
```

### Detalhamento de Novos YAMLs

```markdown
## 2. Novos Apelidos Propostos

### 2.1 [Nome do Novo Apelido]

**Arquivo:** `yaml/[categoria]/[novo_arquivo].yaml`
**Ocorrências:** [N] itens
**Unidade:** [unidade]

**Exemplos:**
- [descrição 1] (quantidade: X)
- [descrição 2] (quantidade: Y)

**YAML proposto:**
```yaml
apelido: [nome]
unit: [unidade]
contem:
  - [palavra1]
  - [palavra2]
ignorar:
  - [palavra_ignorar]
```

**Justificativa:** [por que este apelido é necessário]

**Validação:**
- [ ] Verificar unicidade do apelido
- [ ] Testar com exemplos
- [ ] Validar unidade
```

### Atualizações no Master

```markdown
## 3. Atualizações no Reconhecimento Master

### 3.1 Novos Padrões Identificados

**Categoria:** [nome]

**Padrões:**
```json
{
  "novos_sinonimos": {
    "[termo_base]": ["variacao1", "variacao2", "variacao3"]
  },
  "normalizacoes": [
    {
      "de": "[termo_variante]",
      "para": "[termo_padrao]",
      "contexto": "[quando_aplicar]"
    }
  ]
}
```

**Impacto:** Melhora reconhecimento de [X] variações
```

## Checklist de Implementação

Após gerar as propostas, siga estes passos:

### 1. Validar Propostas
- [ ] Revisar todos os YAMLs propostos
- [ ] Verificar unicidade de apelidos
- [ ] Validar unidades
- [ ] Confirmar palavras-chave são específicas

### 2. Implementar Correções
```bash
# Editar YAMLs existentes
# Criar novos YAMLs em yaml/[categoria]/

# Validar sintaxe
python scripts/validate_yaml.py

# Rebuild taxonomia
python scripts/builder.py
```

### 3. Atualizar Master
```bash
# Editar data/master/reconhecimento_master.json
# Adicionar novos padrões identificados
```

### 4. Testar
```bash
# Re-processar orçamento original
# Verificar melhorias:
# - Taxa de "ok" aumentou?
# - Taxa de "desconhecido" diminuiu?
# - Itens marcados agora classificam corretamente?
```

### 5. Documentar
```bash
# Criar changelog
# Documentar padrões aprendidos
# Arquivar arquivos de aprendizado processados
```

## Critérios de Qualidade

### Para Correções em YAMLs

✅ **Aprovar** se:
- Resolve o problema específico
- Não causa novos falsos positivos
- Palavras-chave são técnicas e específicas
- Melhora score de confiança

❌ **Rejeitar** se:
- Palavra-chave muito genérica
- Pode causar ambiguidade
- Não resolve problema raiz

### Para Novos YAMLs

✅ **Aprovar** se:
- Apelido é único e descritivo
- Ocorre com frequência (>3 vezes)
- Tem especificação técnica clara
- Unidade está correta

❌ **Rejeitar** se:
- Ocorrência única ou rara
- Pode ser coberto por YAML existente
- Apelido muito genérico
- Falta contexto técnico

## Exemplo Completo

```markdown
# Análise de Aprendizado - 2026-01-25

## Resumo Executivo
- Itens marcados: 15
- Itens desconhecidos: 50
- Correções propostas: 8
- Novos YAMLs: 12
- Impacto: 45 itens (90%) serão resolvidos

---

## 1. Correções em YAMLs Existentes

### 1.1 concreto_fck_25

**Arquivo:** `yaml/concreto/concreto_fck_25.yaml`
**Problema:** Não reconhece "c25" como variação de "fck 25"
**Ocorrências:** 8 itens

**Correção:**
```yaml
contem:
  - concreto
  - fck
  - "25"
  - c25  # ← Adicionar variação
```

---

## 2. Novos Apelidos

### 2.1 armadura_passiva_laje_nervurada

**Arquivo:** `yaml/armadura/armadura_passiva_laje_nervurada.yaml`
**Ocorrências:** 12 itens

**YAML:**
```yaml
apelido: armadura_passiva_laje_nervurada
unit: kg
contem:
  - armadura
  - passiva
  - laje
  - nervurada
ignorar:
  - montagem
```

**Justificativa:** Laje nervurada é estrutura específica com custo diferente de laje maciça.
```

## Métricas de Sucesso

Após implementar as atualizações, meça:

1. **Taxa de classificação correta** - % de itens com status "ok"
2. **Taxa de desconhecidos** - % de itens não classificados
3. **Score médio** - Confiança média das classificações
4. **Itens resolvidos** - Quantos dos marcados/desconhecidos agora classificam

**Meta:** 
- Taxa "ok": >85%
- Taxa "desconhecido": <5%
- Score médio: >0.8

## Próximos Passos

1. Implementar todas as correções aprovadas
2. Validar e rebuild taxonomia
3. Re-processar orçamento
4. Comparar métricas antes/depois
5. Arquivar arquivos de aprendizado processados
6. Documentar padrões aprendidos
