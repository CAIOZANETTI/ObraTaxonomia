# Fluxo de Processamento do Sistema (End-to-End)

Este documento descreve o ciclo de vida completo da informação dentro do sistema ObraTaxonomia, detalhando a interação via Streamlit, o processamento com Pandas e o ciclo de feedback para resolução de itens desconhecidos.

## Visão Geral do Pipeline (Streamlit + Pandas)

O sistema opera sobre uma interface web (Streamlit) que orquestra a leitura de Excel, classificação em memória e geração de saídas.

```mermaid
graph TD
    %% Atores
    User((👷 Usuário))
    Agent((🤖 Agente AI))

    %% Interface Streamlit
    subgraph "Interface Streamlit"
        Upload[("📂 Upload Excel")]
        UI_Feedback[("🖥️ Dashboard\n(% Sucesso/Falha)")]
        Download[("⬇️ Download Excel\n(Enriquecido)")]
    end

    %% Motor Pandas
    subgraph "Processamento (Pandas)"
        DF_Raw[("📊 DataFrame Bruto")]
        DF_Clean[("🧹 Normalização\n(Limpeza de String)")]
        subgraph "Loop de Classificação"
            MatchEngine("⚙️ Match vs YAML Hash")
        end
        DF_Final[("✅ DataFrame Final\n(Com colunas tax_*)")]
    end

    %% Arquivos Sistema
    subgraph "Sistema de Arquivos"
        YAML_Repo[("📜 Pasta /yaml\n(Base de Conhecimento)")]
        Unknowns_Dir[("⚠️ Pasta /data/unknowns\n(Log para IA)")]
    end

    %% Fluxo
    User -->|Carrega Planilha| Upload
    Upload -->|Lê com Pandas| DF_Raw
    DF_Raw --> DF_Clean
    
    YAML_Repo -.->|Carrega Regras| MatchEngine
    DF_Clean --> MatchEngine
    MatchEngine --> DF_Final
    
    DF_Final --> UI_Feedback
    DF_Final --> Download
    Download -->|Baixa Resultado| User

    %% Tratamento de Desconhecidos (Dual Output)
    DF_Final -.->|Filtra 'tax_desconhecido=True'| Unknowns_Dir
    Unknowns_Dir -->|Lê Pendências| Agent
    Agent -->|Cria/Atualiza Regras| YAML_Repo
```

## Detalhamento da Execução

### 1. Entrada e Ingestão (Streamlit e Pandas)
*   **Ação**: O usuário acessa a interface Streamlit e faz upload do arquivo `.xlsx` de orçamento.
*   **Técnica**: O Pandas lê o arquivo em memória (`pd.read_excel`).
*   **Idempotência**: Se a planilha já tiver colunas `tax_`, elas são removidas para garantir um processamento limpo baseada nas regras atuais.

### 2. O Processamento (Runtime)
O script itera sobre o DataFrame (ou usa vetorização do Pandas quando possível) para aplicar as regras carregadas dos YAMLs.
*   Os arquivos YAML são carregados apenas uma vez (cache) e convertidos em dicionários para busca rápida.
*   Cada linha recebe as tags: `tax_apelido`, `tax_tipo` e `tax_desconhecido`.

### 3. Saída Dupla de "Desconhecidos"
Quando o sistema encontra um item sem match, ele realiza duas ações simultâneas:
1.  **Para o Usuário (Curto Prazo)**: O item é devolvido no Excel de download marcado com `tax_desconhecido = TRUE` (e colorido visualmente na UI). O engenheiro pode corrigir manualmente na planilha se tiver pressa.
2.  **Para o Sistema (Longo Prazo)**: O sistema salva automaticamente (sem ação do usuário) uma cópia desses itens não reconhecidos em um arquivo CSV na pasta `data/unknowns/`.
    *   *Formato*: `{timestamp}_unknowns.csv`.

### 4. Ciclo de Resolução (Como o "Desconhecido" vira "Conhecido")
Este é o momento onde o aprendizado ocorre.
1.  **Monitoramento**: O Agente Antigravity monitora a pasta `data/unknowns/`.
2.  **Atualização**: O Agente cria novas regras nos arquivos YAML (ex: adiciona "cimento cp2" em `aglomerantes.yaml`) com base no prompt definido em `desconhecido.md`.
3.  **Re-processamento**:
    *   No dia seguinte (ou após o update), quando o usuário subir **a mesma planilha** (ou outra similar), o sistema vai reler os YAMLs (agora atualizados).
    *   O que antes era `tax_desconhecido = TRUE` passará a ter um match (ex: `tax_apelido = cimento_saco_50kg`), fechando o ciclo.

