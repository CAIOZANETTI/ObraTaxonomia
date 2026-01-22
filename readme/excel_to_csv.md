# Utilitário de Conversão XLSX para CSV - 8 Métodos

## 📋 Resumo

Este utilitário fornece **8 métodos diferentes** para converter arquivos Excel (.xlsx) em CSV, com fallback automático caso um método falhe.

## ✅ Teste de Extração - Resultado

**Arquivo testado:** `orcamento_tunel-submerso_santos.xlsx`

**Status:** ✅ **SUCESSO**

**Método usado:** Pandas (método 1 de 8)

**Resultado:**
- 7 planilhas convertidas com sucesso
- Arquivos CSV gerados em: `data/output/csv_extracted/`

### Arquivos Gerados

| # | Arquivo | Tamanho | Linhas |
|---|---------|---------|--------|
| 1 | `Insumo.csv` | 40,977 bytes | 721 linhas × 5 colunas |
| 2 | `CP_ Auxiliar.csv` | 3,662 bytes | - |
| 3 | `CP_ Principal.csv` | 71,773 bytes | - |
| 4 | `Planilha de serviços.csv` | 170,496 bytes | - |
| 5 | `Original.csv` | 171,953 bytes | - |
| 6 | `INSUMOS.csv` | 128,401 bytes | - |
| 7 | `CPU AUX.csv` | 5 bytes | - |

---

## 🛠️ Métodos Disponíveis

A função `convert_xlsx_to_csv_all_methods()` tenta os seguintes métodos em ordem:

### 1. **Pandas** ⭐ (Padrão de mercado)
- **Dependências:** `pandas`, `openpyxl`
- **Vantagens:** Mais usado, bem documentado, integração com análise de dados
- **Status:** ✅ **FUNCIONANDO** (usado no teste)

### 2. **Openpyxl** (Manipulação direta)
- **Dependências:** `openpyxl`
- **Vantagens:** Acesso direto às células, sem overhead do Pandas
- **Uso:** Quando você precisa de controle fino sobre células

### 3. **Xlsx2csv** (Baixo consumo de memória)
- **Dependências:** `xlsx2csv`
- **Vantagens:** Ideal para arquivos muito grandes
- **Uso:** Quando memória é limitada

### 4. **Polars** (Ultra-rápido)
- **Dependências:** `polars`, `openpyxl`
- **Vantagens:** Performance extrema, processamento paralelo
- **Uso:** Para grandes volumes de dados

### 5. **Win32com** (Automação nativa do Excel)
- **Dependências:** `pywin32`, Excel instalado
- **Vantagens:** Usa o próprio Excel, suporta fórmulas complexas
- **Uso:** Quando você tem Excel instalado e precisa de compatibilidade total

### 6. **Xlwings** (Interface moderna para Excel)
- **Dependências:** `xlwings`, Excel instalado
- **Vantagens:** API moderna, fácil de usar
- **Uso:** Alternativa moderna ao Win32com

### 7. **Pyexcel** (API unificada)
- **Dependências:** `pyexcel`, `pyexcel-xlsx`
- **Vantagens:** API simples e consistente
- **Uso:** Quando você quer simplicidade

### 8. **Python-Calamine** (Baseado em Rust)
- **Dependências:** `python-calamine`
- **Vantagens:** Velocidade extrema (implementação em Rust)
- **Uso:** Para performance máxima

---

## 📖 Como Usar

### Uso Básico

```python
from scripts.utils import convert_xlsx_to_csv_all_methods

# Converter arquivo XLSX para CSV
result = convert_xlsx_to_csv_all_methods(
    xlsx_path="caminho/para/arquivo.xlsx",
    output_dir="caminho/para/saida"  # Opcional
)

# Verificar resultado
if result['success']:
    print(f"Sucesso! Método usado: {result['method']}")
    print(f"Arquivos gerados: {result['output_files']}")
else:
    print(f"Falhou: {result['message']}")
    # Ver histórico de tentativas
    for attempt in result['attempts']:
        print(f"- {attempt['method']}: {attempt['message']}")
```

### Especificar Métodos Preferidos

```python
# Tentar apenas métodos específicos
result = convert_xlsx_to_csv_all_methods(
    xlsx_path="arquivo.xlsx",
    preferred_methods=['pandas', 'openpyxl', 'polars']
)
```

### Usar Método Específico

```python
from scripts.utils import xlsx_to_csv_pandas, xlsx_to_csv_openpyxl

# Usar apenas Pandas
success, message, files = xlsx_to_csv_pandas(
    xlsx_path="arquivo.xlsx",
    output_dir="saida"
)
```

---

## 📦 Instalação de Dependências

### Mínimo (apenas Pandas + Openpyxl)
```bash
pip install pandas openpyxl
```

### Recomendado (métodos mais comuns)
```bash
pip install pandas openpyxl xlsx2csv polars
```

### Completo (todos os métodos)
```bash
pip install openpyxl pandas xlsx2csv polars pywin32 xlwings pyexcel pyexcel-xlsx python-calamine
```

### Instalação Individual

```bash
# Método 1: Pandas
pip install pandas openpyxl

# Método 2: Openpyxl
pip install openpyxl

# Método 3: Xlsx2csv
pip install xlsx2csv

# Método 4: Polars
pip install polars openpyxl

# Método 5: Win32com
pip install pywin32

# Método 6: Xlwings
pip install xlwings

# Método 7: Pyexcel
pip install pyexcel pyexcel-xlsx

# Método 8: Calamine
pip install python-calamine
```

---

## 🔍 Estrutura do Resultado

A função `convert_xlsx_to_csv_all_methods()` retorna um dicionário:

```python
{
    'success': bool,              # True se algum método funcionou
    'method': str,                # Nome do método que funcionou (ou None)
    'message': str,               # Mensagem de status
    'output_files': List[str],    # Lista de arquivos CSV gerados
    'attempts': List[Dict]        # Histórico de todas as tentativas
}
```

### Exemplo de `attempts`:

```python
[
    {
        'method': 'pandas',
        'success': True,
        'message': 'Pandas: 7 sheets converted'
    }
]
```

---

## 🎯 Casos de Uso

### 1. Processamento Batch
```python
import os
from scripts.utils import convert_xlsx_to_csv_all_methods

input_dir = "data/input"
output_dir = "data/output/csv"

for filename in os.listdir(input_dir):
    if filename.endswith('.xlsx'):
        xlsx_path = os.path.join(input_dir, filename)
        result = convert_xlsx_to_csv_all_methods(xlsx_path, output_dir)
        print(f"{filename}: {result['message']}")
```

### 2. Pipeline de Dados
```python
def process_budget_file(xlsx_path):
    # Converter para CSV
    result = convert_xlsx_to_csv_all_methods(xlsx_path)
    
    if not result['success']:
        raise Exception(f"Falha na conversão: {result['message']}")
    
    # Processar cada CSV gerado
    for csv_file in result['output_files']:
        df = pd.read_csv(csv_file)
        # ... processar dados ...
    
    return result
```

### 3. Fallback Robusto
```python
# Tentar Pandas primeiro, depois Openpyxl como fallback
result = convert_xlsx_to_csv_all_methods(
    xlsx_path="arquivo.xlsx",
    preferred_methods=['pandas', 'openpyxl']
)

# Sistema automaticamente tenta o próximo método se o primeiro falhar
```

---

## 📝 Notas Importantes

1. **Encoding:** Todos os métodos usam `utf-8-sig` para compatibilidade com Excel
2. **Nomes de Arquivos:** Caracteres especiais nos nomes das planilhas são substituídos por `_`
3. **Diretório de Saída:** Se não especificado, usa o mesmo diretório do arquivo XLSX
4. **Todas as Abas:** Todos os métodos convertem **todas as planilhas** do arquivo XLSX

---

## 🧪 Script de Teste

Execute o script de teste para validar a instalação:

```bash
python scripts/test_xlsx_extraction.py
```

O script irá:
1. Tentar converter o arquivo de teste
2. Mostrar qual método funcionou
3. Listar todos os arquivos CSV gerados
4. Exibir o histórico de tentativas

---

## 🐛 Troubleshooting

### Erro: "Missing optional dependency 'openpyxl'"
```bash
pip install openpyxl
```

### Erro: "No module named 'win32com'"
```bash
pip install pywin32
```

### Todos os métodos falharam
```bash
# Instalar dependências mínimas
pip install pandas openpyxl
```

### Arquivo muito grande (memória insuficiente)
```bash
# Usar xlsx2csv (baixo consumo de memória)
pip install xlsx2csv
```

---

## 📊 Comparação de Performance

| Método | Velocidade | Memória | Dependências | Excel Necessário |
|--------|-----------|---------|--------------|------------------|
| Pandas | ⭐⭐⭐ | ⭐⭐ | 2 | ❌ |
| Openpyxl | ⭐⭐⭐ | ⭐⭐⭐ | 1 | ❌ |
| Xlsx2csv | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 1 | ❌ |
| Polars | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 2 | ❌ |
| Win32com | ⭐⭐ | ⭐⭐ | 1 + Excel | ✅ |
| Xlwings | ⭐⭐ | ⭐⭐ | 1 + Excel | ✅ |
| Pyexcel | ⭐⭐⭐ | ⭐⭐⭐ | 2 | ❌ |
| Calamine | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 1 | ❌ |

---

## ✅ Conclusão

O utilitário foi testado com sucesso no arquivo `orcamento_tunel-submerso_santos.xlsx`:
- ✅ 7 planilhas convertidas
- ✅ Método Pandas funcionou perfeitamente
- ✅ Fallback automático disponível para 7 outros métodos
- ✅ Pronto para uso em produção
