import streamlit as st
import pandas as pd
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="upload e conversão",
    page_icon="📂",
    layout="wide"
)

# --- REQUISITOS TÉCNICOS E FUNÇÕES ---

REQUIRED_COLUMNS = ["codigo", "nome", "qtd", "unid"]

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    normaliza nomes de colunas: strip + lowercase.
    """
    df.columns = df.columns.astype(str).str.strip().str.lower()
    return df

def validate_sheet(df: pd.DataFrame) -> bool:
    """
    verifica se as colunas obrigatórias existem.
    case insensitive (assumindo que o df já passou por normalize_columns).
    """
    if df is None or df.empty:
        return False
    
    # normaliza antes de validar (embora a ordem de chamada deva garantir, reforçamos)
    df = normalize_columns(df)
    cols = df.columns.tolist()
    
    # verifica interseção
    # não precisamos ser exatos (colunas extras permitidas, mas ignoradas depois)
    # MAS todas as required devem estar presentes
    for req in REQUIRED_COLUMNS:
        if req not in cols:
            return False
    return True

@st.cache_data
def load_and_consolidate(file_content, filename_for_cache):
    """
    lê o arquivo excel, valida abas e consolida.
    retorna:
      - df_final: dataframe consolidado
      - summary: dict com contagens
      - validation_log: list de dicts com status por aba
    """
    try:
        # lê todas as abas
        xls = pd.ExcelFile(file_content)
        all_sheets = xls.sheet_names
        
        valid_sheets_data = []
        validation_log = []
        
        ignored_count = 0
        valid_count = 0
        
        for sheet_name in all_sheets:
            try:
                # lê aba sem header para checar se está vazia? 
                # o formato exige colunas nomeadas. vamos ler com header=0 padrão.
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # normaliza
                df = normalize_columns(df)
                
                if validate_sheet(df):
                    # mantém apenas colunas obrigatórias
                    df_valid = df[REQUIRED_COLUMNS].copy()
                    
                    # limpa linhas vazias essenciais (se codigo ou nome for nulo, talvez?)
                    # requisitos dizem: "se faltar qualquer uma das quatro colunas, ignora". 
                    # sobre linhas vazias: "gerar csv bruto". vamos manter bruto, apenas dropna se tudo vazio.
                    df_valid.dropna(how='all', inplace=True)
                    
                    df_valid['aba'] = sheet_name
                    valid_sheets_data.append(df_valid)
                    valid_count += 1
                    validation_log.append({"aba": sheet_name, "status": "válida", "linhas": len(df_valid)})
                else:
                    ignored_count += 1
                    validation_log.append({"aba": sheet_name, "status": "ignorada (formato inválido)", "linhas": 0})
            except Exception as e:
                ignored_count += 1
                validation_log.append({"aba": sheet_name, "status": f"erro: {str(e)}", "linhas": 0})
        
        if valid_sheets_data:
            df_final = pd.concat(valid_sheets_data, ignore_index=True)
            # garante ordem das colunas + aba no final
            df_final = df_final[REQUIRED_COLUMNS + ['aba']]
        else:
            df_final = pd.DataFrame(columns=REQUIRED_COLUMNS + ['aba'])
            
        summary = {
            "validas": valid_count,
            "ignoradas": ignored_count,
            "total_linhas": len(df_final)
        }
        
        return df_final, summary, validation_log

    except Exception as e:
        return None, {"error": str(e)}, []

# --- GERAÇÃO DE EXEMPLOS ---

def create_example_excel(type_key):
    """
    gera bytes de um excel de exemplo em memória.
    """
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    if type_key == 'simples':
        df1 = pd.DataFrame({
            'codigo': ['C001', 'C002'],
            'nome': ['Cimento', 'Areia'],
            'qtd': [10, 5],
            'unid': ['sc', 'm3']
        })
        df2 = pd.DataFrame({
            'codigo': ['E001'],
            'nome': ['Tijolo'],
            'qtd': [1000],
            'unid': ['mil']
        })
        df1.to_excel(writer, sheet_name='Material_Base', index=False)
        df2.to_excel(writer, sheet_name='Alvenaria', index=False)
        
    elif type_key == 'extras':
        df1 = pd.DataFrame({
            'codigo': ['P010'],
            'nome': ['Tinta'],
            'qtd': [4],
            'unid': ['gl'],
            'preco': [150.00], # extra
            'obs': ['urgente'] # extra
        })
        df1.to_excel(writer, sheet_name='Pintura', index=False)
        
    elif type_key == 'invalidas':
        # Aba válida
        df1 = pd.DataFrame({
            'codigo': ['X1'], 'nome': ['Item X'], 'qtd': [1], 'unid': ['un']
        })
        # Aba inválida (falta unid)
        df2 = pd.DataFrame({
            'codigo': ['Y1'], 'nome': ['Item Y'], 'qtd': [10]
        })
        # Aba inválida (colunas erradas)
        df3 = pd.DataFrame({
            'DESC': ['Item Z'], 'QTD': [50]
        })
        
        df1.to_excel(writer, sheet_name='Valida', index=False)
        df2.to_excel(writer, sheet_name='Sem_Unidade', index=False)
        df3.to_excel(writer, sheet_name='Formato_Errado', index=False)
        
    writer.close()
    output.seek(0)
    return output

# --- UI LAYER ---

# 1. Cabeçalho
st.title("upload e conversão")
st.markdown("envie uma planilha excel no formato padrão para gerar um csv consolidado.")

# 2. Especificação do Formato
st.divider()
st.markdown("**formato obrigatório da planilha**")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown("`codigo`\n\nidentificador do item")
with c2: st.markdown("`nome`\n\ndescrição do item")
with c3: st.markdown("`qtd`\n\nquantidade")
with c4: st.markdown("`unid`\n\nunidade de medida")
st.caption("abas sem esse formato serão ignoradas.")
st.divider()

# 3. Uploader
file = st.file_uploader(
    "selecione um arquivo excel", 
    type=["xlsx", "xls"], 
    help="limite de 200mb. formatos .xlsx ou .xls."
)

if not file:
    st.info("nenhum arquivo carregado.")
else:
    # 6. Resultado (Processamento)
    with st.status("processando arquivo...", expanded=True) as status:
        st.write("lendo planilha...")
        
        # BytesIO para cache funcionar bem precisa ser tratado, 
        # mas st.cache_data lida bem se passarmos o .getvalue() ou id único se o objeto mudar
        # vamos passar o bytes
        bytes_data = file.getvalue()
        
        st.write("validando formato...")
        df_final, summary, logs = load_and_consolidate(bytes_data, file.name)
        
        if df_final is None:
            status.update(label="erro no processamento", state="error", expanded=True)
            st.error(f"falha: {summary.get('error')}")
        else:
            status.update(label="csv gerado com sucesso.", state="complete", expanded=False)
            
            # Métricas e Feedback
            m1, m2, m3 = st.columns(3)
            m1.metric("abas válidas", summary['validas'])
            m2.metric("abas ignoradas", summary['ignoradas'])
            m3.metric("linhas consolidadas", summary['total_linhas'])
            
            # Detalhes das abas (expander para não poluir se for mt coisa)
            if logs:
                with st.expander("ver detalhes da validação por aba"):
                    st.dataframe(pd.DataFrame(logs), use_container_width=True)
            
            # Preview (Top 20)
            st.subheader("preview (primeiras 20 linhas)")
            st.dataframe(df_final.head(20), use_container_width=True)
            
            # Download
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="baixar csv",
                data=csv,
                file_name="consolidado_obra.csv",
                mime="text/csv",
                type="primary"
            )


# 5. Exemplos
st.divider()
st.markdown("### exemplos de planilha")
st.markdown("use estes modelos para testar a validação:")

c_ex1, c_ex2, c_ex3 = st.columns(3)

def load_example(key):
    # gera o excel em mémoria e coloca no uploader? 
    # Streamlit não permite injetar no file_uploader diretamente via código facil sem hack.
    # O prompt diz: "permitir carregar o exemplo diretamente no fluxo (sem download)."
    # Solução: setar session_state e renderizar a parte de processamento como se fosse um upload
    # mas o uploader padrão é visual. 
    # Vamos adaptar: se clicar no botão, processamos o bytes gerados e ignoramos o uploader vazio.
    st.session_state['active_example'] = key

if c_ex1.button("exemplo simples"):
    load_example('simples')
    
if c_ex2.button("exemplo com colunas extras"):
    load_example('extras')
    
if c_ex3.button("exemplo com abas inválidas"):
    load_example('invalidas')

# Lógica para processar exemplo se selecionado E nenhum arquivo real carregado
if 'active_example' in st.session_state and not file:
    ex_key = st.session_state['active_example']
    st.markdown(f"--- \n**visualizando exemplo: {ex_key}**")
    
    # Gera bytes
    ex_bytes = create_example_excel(ex_key)
    ex_content = ex_bytes.getvalue()
    
    # Reutiliza lógica de display
    # (Idealmente refatoraria a parte do 'if not file: else: ...' para uma função, 
    # mas para manter simples e linear como script streamlit, repito a chamada da função de processamento)
    
    df_final, summary, logs = load_and_consolidate(ex_content, f"example_{ex_key}.xlsx")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("abas válidas", summary['validas'])
    m2.metric("abas ignoradas", summary['ignoradas'])
    m3.metric("linhas consolidadas", summary['total_linhas'])
    
    with st.expander("analisar logs de validação"):
        st.dataframe(pd.DataFrame(logs), use_container_width=True)
        
    st.dataframe(df_final.head(20), use_container_width=True)
