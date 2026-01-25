# ObraTaxonomia

Sistema de classificação e normalização de orçamentos de obras usando taxonomia YAML.

## 📋 Visão Geral

O ObraTaxonomia é uma aplicação Streamlit que processa planilhas de orçamento, normaliza descrições e classifica itens automaticamente usando uma taxonomia customizável.

## 🚀 Início Rápido

### Instalação

```powershell
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app/Home.py
```

### Fluxo de Uso

1. **Upload** - Carregue arquivo Excel
2. **Mapear Colunas** - Valide o mapeamento de colunas
3. **Normalizar** - Normalize textos e números
4. **Apelidar e Validar** - Valide as classificações sugeridas
5. **Desconhecidos** - Gerencie itens não identificados

## 📁 Estrutura de Diretórios

```
ObraTaxonomia/
├── app/                    # Aplicação Streamlit
├── data/                   # Dados e arquivos
│   ├── excel/              # Arquivos Excel de entrada
│   ├── output/             # Arquivos processados
│   │   ├── validado/       # Orçamentos validados
│   │   └── arquivo/        # Backups
│   ├── revisar/            # Itens para revisão
│   │   ├── inbox/          # Novos
│   │   ├── processados/    # Resolvidos
│   │   └── arquivo/        # Histórico
│   └── desconhecidos/      # Desconhecidos
│       ├── entrada/        # Novos
│       ├── processados/    # Resolvidos
│       └── arquivo/        # Histórico
├── scripts/                # Backend Python
├── yaml/                   # Taxonomia
└── readme/                 # Documentação
```

**📖 Documentação completa:** [estrutura_diretorios.md](readme/estrutura_diretorios.md)

## 📥 Onde Salvar Arquivos

| Arquivo | Diretório | Descrição |
|---------|-----------|-----------|
| `orcamento_validado.csv` | `data/output/validado/` | Resultado final validado |
| `itens_revisar.csv` | `data/revisar/inbox/` | Itens que precisam revisão |
| `desconhecidos.csv` | `data/desconhecidos/entrada/` | Desconhecidos para análise |

## 📚 Documentação

- [Arquitetura](readme/arquitetura.md) - Fluxo e princípios do sistema
- [Estrutura de Diretórios](readme/estrutura_diretorios.md) - Organização de arquivos
- [Taxonomia](readme/taxonomia.md) - Como funciona a classificação
- [Desconhecidos](readme/desconhecido.md) - Gestão de unknowns
- [Excel to CSV](readme/excel_to_csv.md) - Conversão de arquivos
- [YAML to JSON](readme/yaml_to_json.md) - Build da taxonomia
- [Update](readme/update.md) - Roadmap e atualizações

## 🎯 Funcionalidades

- ✅ Upload e conversão de Excel para CSV
- ✅ Mapeamento interativo de colunas
- ✅ Normalização de texto e números
- ✅ Classificação automática com taxonomia YAML
- ✅ Validação humana de classificações
- ✅ Filtros avançados (Status, Validado, Tipo, Apelido)
- ✅ Exportação de validados, revisar e desconhecidos
- ✅ Gestão de unknowns para melhoria contínua

## 🛠️ Tecnologias

- **Frontend:** Streamlit
- **Backend:** Python 3.x
- **Dados:** Pandas, CSV
- **Taxonomia:** YAML

## 📝 Workflow Recomendado

### 1. Processar Orçamento
```
1. Coloque Excel em: data/excel/
2. Abra aplicação: streamlit run app/Home.py
3. Siga o fluxo: Upload → Mapear → Normalizar → Validar
```

### 2. Exportar Resultados
```
4. Na página "Apelidar e Validar":
   - Baixe "orcamento_validado.csv" → data/output/validado/
   - Baixe "itens_revisar.csv" → data/revisar/inbox/ (se houver)
   - Baixe "desconhecidos.csv" → data/desconhecidos/entrada/ (se houver)
```

### 3. Melhorar Taxonomia
```
5. Analise desconhecidos em: data/desconhecidos/entrada/
6. Adicione novos apelidos em: yaml/
7. Mova processados para: data/desconhecidos/processados/
8. Re-processe orçamento
```

## 🔧 Manutenção

### Atualizar Taxonomia
```powershell
# Validar YAMLs
python scripts/validate_yaml.py

# Rebuild taxonomia
python scripts/builder.py
```

### Limpar Arquivos Antigos
```powershell
# Mover arquivos antigos para arquivo
Get-ChildItem data/output/validado/*.csv | 
  Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} |
  Move-Item -Destination data/output/arquivo/
```

## 📊 Estrutura da Taxonomia

A taxonomia é definida em arquivos YAML na pasta `yaml/`:

```yaml
apelido: concreto_fck_25
unit: m3
contem:
  - concreto
  - fck
  - "25"
ignorar:
  - bombeamento
```

## 🤝 Contribuindo

1. Adicione novos apelidos em `yaml/`
2. Valide com `python scripts/validate_yaml.py`
3. Teste na aplicação
4. Documente mudanças

## 📄 Licença

[Adicionar licença aqui]

## 👥 Autores

[Adicionar autores aqui]
