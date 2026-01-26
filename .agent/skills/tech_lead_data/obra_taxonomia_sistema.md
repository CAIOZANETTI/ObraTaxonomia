---
skill_name: "ObraTaxonomia - Arquitetura e Desenvolvimento"
agent: tech_lead_data
category: "Sistema e ETL"
difficulty: advanced
version: 1.0.0
---

# Skill: ObraTaxonomia - Arquitetura Técnica e Manutenção

## Objetivo

Fornecer conhecimento técnico sobre a arquitetura, scripts backend, ETL pipeline e manutenção do sistema ObraTaxonomia v4.

## 1. Arquitetura do Sistema

### Stack Tecnológico

```
Frontend:  Streamlit (Python)
Backend:   Python 3.10+
Data:      Pandas, NumPy
Storage:   CSV, JSON, YAML
```

### Estrutura de Diretórios

```
ObraTaxonomia/
├── app/                      # Frontend Streamlit
│   ├── Home.py              # Página inicial
│   └── pages/               # Fluxo de 5 páginas
│       ├── 1_Upload.py
│       ├── 2_Mapear_Colunas.py
│       ├── 3_Normalizar.py
│       ├── 4_Apelidar_Validar.py
│       └── 5_Desconhecidos.py
│
├── scripts/                  # Backend (Core Logic)
│   ├── builder.py           # TaxonomyBuilder (YAML → JSON)
│   ├── classify.py          # ClassifierEngine (Matching)
│   ├── unknowns.py          # Agregação de desconhecidos
│   ├── excel_to_csv.py      # Conversão Excel
│   └── normalize.py         # Normalização de texto
│
├── yaml/                     # Taxonomia (Source of Truth)
│   ├── estrutura/
│   ├── fundacao/
│   ├── alvenaria/
│   └── ...
│
├── data/                     # Dados e outputs
│   ├── excel/               # Inputs originais
│   ├── master/              # taxonomia.json (compilado)
│   ├── output/              # Resultados processados
│   │   ├── validados/
│   │   ├── revisar/
│   │   └── archive/
│   └── unknowns/            # Desconhecidos
│       ├── inbox/
│       ├── processed/
│       └── archive/
│
└── readme/                   # Documentação técnica
    ├── arquitetura.md
    ├── update.md
    └── taxonomia.md
```

## 2. Pipeline ETL

### Fase 1: Extract (Upload)

**Script:** `app/pages/1_Upload.py`

```python
# Conversão Excel → CSV
from scripts.excel_to_csv import convert_excel_to_csv

csv_data, sheets_info = convert_excel_to_csv(
    uploaded_file,
    selected_sheets=['Planilha1', 'Orcamento']
)

# Armazenamento em session_state
st.session_state['csv_raw'] = csv_data
st.session_state['sheets_info'] = sheets_info
```

**Funcionalidades:**
- Upload de múltiplos formatos (Excel, CSV)
- Seleção de planilhas específicas
- Preview de dados
- Validação de estrutura

### Fase 2: Transform - Mapeamento

**Script:** `app/pages/2_Mapear_Colunas.py`

```python
# Auto-detecção de colunas
mapeamento_auto = {
    'descricao': detectar_coluna_descricao(df.columns),
    'quantidade': detectar_coluna_quantidade(df.columns),
    'unidade': detectar_coluna_unidade(df.columns),
    'preco_unitario': detectar_coluna_preco(df.columns)
}

# Renomear colunas para padrão
df_padronizado = df.rename(columns=mapeamento_inverso)
```

**Padrão de Colunas:**
```python
COLUNAS_OBRIGATORIAS = [
    'descricao',
    'quantidade',
    'unidade',
    'preco_unitario'
]

COLUNAS_OPCIONAIS = [
    'codigo',
    'categoria',
    'observacao'
]
```

### Fase 3: Transform - Normalização

**Script:** `scripts/normalize.py`

```python
def normalizar_texto(texto: str) -> str:
    """
    Normalização completa de texto para matching.
    
    Pipeline:
    1. Lowercase
    2. Remover acentos
    3. Remover caracteres especiais
    4. Normalizar espaços
    5. Remover stopwords (opcional)
    """
    if pd.isna(texto):
        return ""
    
    # Lowercase
    texto = texto.lower()
    
    # Remover acentos
    texto = unidecode(texto)
    
    # Remover caracteres especiais (manter números e espaços)
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    
    # Normalizar espaços
    texto = ' '.join(texto.split())
    
    return texto
```

**Aplicação:**
```python
df['descricao_norm'] = df['descricao'].apply(normalizar_texto)
```

### Fase 4: Transform - Classificação

**Script:** `scripts/classify.py`

```python
class ClassifierEngine:
    """
    Engine de classificação baseada em matching fuzzy.
    """
    
    def __init__(self, taxonomia_json: dict):
        self.taxonomia = taxonomia_json
        self._build_index()
    
    def _build_index(self):
        """Constrói índice invertido para busca rápida."""
        self.index = {}
        for tipo, grupos in self.taxonomia.items():
            for grupo, apelidos in grupos.items():
                for apelido_data in apelidos:
                    for keyword in apelido_data['contem']:
                        if keyword not in self.index:
                            self.index[keyword] = []
                        self.index[keyword].append({
                            'tipo': tipo,
                            'grupo': grupo,
                            'apelido': apelido_data['apelido']
                        })
    
    def classify(self, descricao_norm: str) -> dict:
        """
        Classifica item baseado em descrição normalizada.
        
        Returns:
            dict com tax_tipo, tax_grupo, apelido, similaridade, status
        """
        # 1. Buscar keywords no índice
        candidatos = self._buscar_candidatos(descricao_norm)
        
        # 2. Calcular similaridade para cada candidato
        scores = []
        for candidato in candidatos:
            score = self._calcular_similaridade(
                descricao_norm,
                candidato['keywords'],
                candidato['ignorar']
            )
            scores.append({
                **candidato,
                'similaridade': score
            })
        
        # 3. Selecionar melhor match
        if not scores:
            return self._resultado_desconhecido()
        
        melhor = max(scores, key=lambda x: x['similaridade'])
        
        # 4. Determinar status baseado em threshold
        if melhor['similaridade'] >= 0.8:
            status = 'ok'
        elif melhor['similaridade'] >= 0.6:
            status = 'revisar'
        else:
            status = 'desconhecido'
        
        return {
            'tax_tipo': melhor['tipo'],
            'tax_grupo': melhor['grupo'],
            'apelido_sugerido': melhor['apelido'],
            'similaridade': melhor['similaridade'],
            'status': status,
            'tax_desconhecido': (status == 'desconhecido')
        }
    
    def _calcular_similaridade(self, texto, keywords, ignorar):
        """
        Calcula score de similaridade (0-1).
        
        Algoritmo:
        - +1 para cada keyword encontrada
        - Normalizado pelo número total de keywords
        - Penalização se palavras importantes faltam
        """
        palavras_texto = set(texto.split())
        
        # Remover palavras ignoradas
        palavras_texto = palavras_texto - set(ignorar)
        
        # Contar matches
        matches = sum(1 for kw in keywords if kw in texto)
        
        # Score normalizado
        score = matches / len(keywords) if keywords else 0
        
        return score
```

### Fase 5: Load - Validação e Export

**Script:** `app/pages/4_Apelidar_Validar.py`

```python
# Validação manual
df_working = st.session_state['df_working'].copy()

# Edição inline
edited_df = st.data_editor(
    df_working,
    column_config={
        'apelido_final': st.column_config.TextColumn(
            'Apelido Final',
            help='Edite para corrigir classificação'
        ),
        'validado': st.column_config.CheckboxColumn(
            'Validado',
            help='Marque como validado'
        )
    },
    disabled=['descricao', 'tax_tipo', 'tax_grupo'],
    use_container_width=True
)

# Salvar alterações
if st.button('Salvar Alterações'):
    st.session_state['df_working'] = edited_df
    st.session_state['csv_validated'] = edited_df.to_csv(index=False)
    st.success('Alterações salvas!')
```

## 3. Módulos Backend Detalhados

### 3.1 TaxonomyBuilder (`scripts/builder.py`)

**Responsabilidade:** Compilar YAMLs → JSON master

```python
class TaxonomyBuilder:
    """
    Constrói taxonomia mestre a partir de arquivos YAML.
    """
    
    def __init__(self, yaml_dir: str = 'yaml/'):
        self.yaml_dir = Path(yaml_dir)
        self.taxonomia = {}
    
    def build(self) -> dict:
        """
        Varre diretório YAML e compila taxonomia.
        
        Estrutura de saída:
        {
            'estrutura': {
                'concreto': [
                    {'apelido': 'concreto_fck25', 'unit': 'm³', 'contem': [...], 'ignorar': [...]},
                    ...
                ]
            }
        }
        """
        for tipo_dir in self.yaml_dir.iterdir():
            if not tipo_dir.is_dir():
                continue
            
            tipo = tipo_dir.name
            self.taxonomia[tipo] = {}
            
            for yaml_file in tipo_dir.glob('*.yaml'):
                grupo = yaml_file.stem
                
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    apelidos = yaml.safe_load(f)
                
                self.taxonomia[tipo][grupo] = apelidos
        
        return self.taxonomia
    
    def save_json(self, output_path: str = 'data/master/taxonomia.json'):
        """Salva taxonomia compilada em JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.taxonomia, f, ensure_ascii=False, indent=2)
```

### 3.2 Unknowns Aggregator (`scripts/unknowns.py`)

**Responsabilidade:** Agregar e analisar desconhecidos

```python
def aggregate_unknowns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega itens desconhecidos com análise de frequência.
    
    Args:
        df: DataFrame com coluna 'tax_desconhecido' = True
    
    Returns:
        DataFrame agregado com:
        - descricao_norm
        - frequencia (count)
        - sugestao_tipo (baseado em keywords)
        - sugestao_grupo
    """
    # Filtrar desconhecidos
    df_unknown = df[df['tax_desconhecido'] == True].copy()
    
    # Agrupar por descrição normalizada
    agregado = df_unknown.groupby('descricao_norm').agg({
        'descricao': 'first',
        'quantidade': 'sum',
        'custo_total': 'sum'
    }).reset_index()
    
    agregado['frequencia'] = df_unknown.groupby('descricao_norm').size().values
    
    # Sugerir classificação baseado em keywords comuns
    agregado['sugestao_tipo'] = agregado['descricao_norm'].apply(sugerir_tipo)
    agregado['sugestao_grupo'] = agregado['descricao_norm'].apply(sugerir_grupo)
    
    # Ordenar por frequência
    agregado = agregado.sort_values('frequencia', ascending=False)
    
    return agregado

def sugerir_tipo(descricao_norm: str) -> str:
    """Sugere tipo baseado em keywords."""
    keywords_tipo = {
        'estrutura': ['concreto', 'aco', 'forma', 'pilar', 'viga', 'laje'],
        'fundacao': ['estaca', 'bloco', 'sapata', 'tubulao'],
        'alvenaria': ['bloco', 'tijolo', 'parede'],
        'revestimento': ['argamassa', 'reboco', 'gesso', 'ceramica'],
        'instalacao': ['tubo', 'cano', 'fio', 'cabo', 'eletrica', 'hidraulica']
    }
    
    for tipo, keywords in keywords_tipo.items():
        if any(kw in descricao_norm for kw in keywords):
            return tipo
    
    return 'indefinido'
```

## 4. Fluxo de Dados (Session State)

### Streamlit Session State Management

```python
# Inicialização
if 'df_working' not in st.session_state:
    st.session_state['df_working'] = None

# Passagem entre páginas
# Página 1 → 2
st.session_state['csv_raw'] = csv_data

# Página 2 → 3
st.session_state['df_mapped'] = df_padronizado

# Página 3 → 4
st.session_state['df_normalized'] = df_normalizado
st.session_state['df_classified'] = df_classificado

# Página 4 → 5
st.session_state['csv_validated'] = df_validado.to_csv(index=False)
st.session_state['unknowns'] = df_unknowns
```

## 5. Performance e Otimização

### Caching

```python
@st.cache_resource
def get_taxonomy_engine():
    """Cache da engine de classificação (carregamento lento)."""
    builder = TaxonomyBuilder()
    taxonomia = builder.build()
    engine = ClassifierEngine(taxonomia)
    return engine

@st.cache_data
def load_master_taxonomy():
    """Cache do JSON master."""
    with open('data/master/taxonomia.json', 'r') as f:
        return json.load(f)
```

### Vetorização

```python
# EVITAR: Loop linha por linha
for idx, row in df.iterrows():
    df.loc[idx, 'descricao_norm'] = normalizar_texto(row['descricao'])

# PREFERIR: Vetorização
df['descricao_norm'] = df['descricao'].apply(normalizar_texto)

# MELHOR AINDA: Vetorização NumPy (quando possível)
df['custo_total'] = df['quantidade'] * df['preco_unitario']  # Vetorizado
```

## 6. Testes e Validação

### Testes Unitários

```python
# tests/test_normalize.py
import unittest
from scripts.normalize import normalizar_texto

class TestNormalize(unittest.TestCase):
    def test_remover_acentos(self):
        self.assertEqual(
            normalizar_texto("CONCRETO FCK=25MPa"),
            "concreto fck 25 mpa"
        )
    
    def test_lowercase(self):
        self.assertEqual(
            normalizar_texto("CONCRETO"),
            "concreto"
        )
    
    def test_caracteres_especiais(self):
        self.assertEqual(
            normalizar_texto("AÇO CA-50 Ø12,5mm"),
            "aco ca 50 12 5 mm"
        )
```

### Teste de Sanidade

```python
# Validar taxonomia compilada
def validar_taxonomia(taxonomia: dict) -> list:
    """
    Valida estrutura da taxonomia.
    
    Returns:
        Lista de erros encontrados
    """
    erros = []
    
    for tipo, grupos in taxonomia.items():
        for grupo, apelidos in grupos.items():
            for apelido_data in apelidos:
                # Validar campos obrigatórios
                if 'apelido' not in apelido_data:
                    erros.append(f"{tipo}/{grupo}: falta campo 'apelido'")
                
                if 'contem' not in apelido_data or not apelido_data['contem']:
                    erros.append(f"{tipo}/{grupo}/{apelido_data.get('apelido')}: 'contem' vazio")
    
    return erros
```

## 7. Manutenção e Troubleshooting

### Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Uso
logger.info(f"Processando {len(df)} itens")
logger.warning(f"Taxa de desconhecidos alta: {taxa_desconhecidos:.1f}%")
logger.error(f"Erro ao carregar YAML: {e}")
```

### Monitoramento de Qualidade

```python
def calcular_metricas_qualidade(df: pd.DataFrame) -> dict:
    """
    Calcula métricas de qualidade da classificação.
    """
    total = len(df)
    
    return {
        'total_itens': total,
        'taxa_ok_%': (df['status'] == 'ok').sum() / total * 100,
        'taxa_revisar_%': (df['status'] == 'revisar').sum() / total * 100,
        'taxa_desconhecidos_%': df['tax_desconhecido'].sum() / total * 100,
        'similaridade_media': df['similaridade'].mean(),
        'tipos_unicos': df['tax_tipo'].nunique()
    }
```

## 8. Deployment

### Requisitos

```txt
# requirements.txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
pyyaml>=6.0
unidecode>=1.3.0
openpyxl>=3.1.0
```

### Execução

```bash
# Desenvolvimento
streamlit run app/Home.py

# Produção
streamlit run app/Home.py --server.port 8501 --server.address 0.0.0.0
```

## Referências

- **Arquitetura**: `readme/arquitetura.md`
- **Roadmap**: `readme/update.md`
- **Taxonomia**: `readme/taxonomia.md`
- **Streamlit Docs**: https://docs.streamlit.io/
