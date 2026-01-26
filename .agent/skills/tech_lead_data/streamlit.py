"""
Streamlit Dashboard Module - ObraTaxonomia

Skill: Streamlit UI Components
Agent: tech_lead_data
Category: Frontend Development
Version: 1.0.0

Este módulo fornece funções para criação de dashboards interativos usando Streamlit,
com componentes especializados para visualização de dados de engenharia.

Padrões seguidos:
- PEP8 (Style Guide for Python Code)
- Google-style docstrings
- Type hints obrigatórios
- Componentização reutilizável
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np


def render_project_dashboard(
    df: pd.DataFrame,
    title: str = "Dashboard de Projeto",
    kpi_columns: Optional[List[str]] = None,
    gantt_config: Optional[Dict[str, str]] = None
) -> None:
    """
    Renderiza dashboard completo de projeto com KPIs e gráfico de Gantt.
    
    Esta função cria automaticamente:
    1. Cabeçalho com título e data de atualização
    2. Linha de KPIs no topo (métricas principais)
    3. Gráfico de Gantt interativo para cronograma
    4. Tabela de dados detalhados (opcional)
    
    Args:
        df: DataFrame com dados do projeto. Deve conter colunas para Gantt:
            - 'atividade' ou 'descricao': Nome da atividade
            - 'inicio': Data de início (datetime ou string ISO)
            - 'fim': Data de término (datetime ou string ISO)
            - 'responsavel' (opcional): Responsável pela atividade
            - 'status' (opcional): Status da atividade
        title: Título do dashboard.
        kpi_columns: Lista de colunas numéricas para exibir como KPIs.
            Se None, detecta automaticamente colunas numéricas.
        gantt_config: Configuração do gráfico de Gantt:
            - 'task_col': Nome da coluna de atividades
            - 'start_col': Nome da coluna de início
            - 'end_col': Nome da coluna de término
            - 'resource_col': Nome da coluna de responsável
    
    Returns:
        None: Renderiza diretamente no Streamlit.
    
    Example:
        >>> import streamlit as st
        >>> import pandas as pd
        >>> 
        >>> df = pd.DataFrame({
        ...     'atividade': ['Fundação', 'Estrutura', 'Acabamento'],
        ...     'inicio': ['2026-01-01', '2026-02-01', '2026-03-01'],
        ...     'fim': ['2026-01-31', '2026-02-28', '2026-03-31'],
        ...     'custo': [50000, 120000, 80000],
        ...     'status': ['Concluído', 'Em Andamento', 'Planejado']
        ... })
        >>> 
        >>> render_project_dashboard(
        ...     df,
        ...     title="Obra Residencial XYZ",
        ...     kpi_columns=['custo']
        ... )
    
    Notes:
        - Requer Streamlit e Plotly instalados
        - Datas são automaticamente convertidas para datetime
        - Gráfico de Gantt é interativo (zoom, pan, hover)
    """
    # Header
    st.title(title)
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.divider()
    
    # KPIs
    render_kpi_row(df, kpi_columns)
    
    # Gráfico de Gantt
    if gantt_config or _has_gantt_columns(df):
        st.subheader("📅 Cronograma (Gantt)")
        render_gantt_chart(df, gantt_config)
    
    # Tabela de dados (expansível)
    with st.expander("📊 Ver Dados Detalhados"):
        st.dataframe(df, use_container_width=True)


def render_kpi_row(
    df: pd.DataFrame,
    kpi_columns: Optional[List[str]] = None
) -> None:
    """
    Renderiza linha de KPIs (Key Performance Indicators) no topo do dashboard.
    
    Args:
        df: DataFrame com dados.
        kpi_columns: Lista de colunas para exibir como KPIs.
            Se None, usa todas as colunas numéricas.
    
    Example:
        >>> render_kpi_row(df, kpi_columns=['custo_total', 'prazo_dias'])
    """
    if kpi_columns is None:
        # Detectar colunas numéricas automaticamente
        kpi_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not kpi_columns:
        st.warning("Nenhuma coluna numérica encontrada para KPIs")
        return
    
    # Limitar a 4 KPIs por linha
    kpi_columns = kpi_columns[:4]
    
    cols = st.columns(len(kpi_columns))
    
    for i, col_name in enumerate(kpi_columns):
        with cols[i]:
            value = df[col_name].sum()
            
            # Formatar valor
            if value > 1_000_000:
                formatted_value = f"R$ {value/1_000_000:.2f}M"
            elif value > 1_000:
                formatted_value = f"R$ {value/1_000:.1f}K"
            else:
                formatted_value = f"{value:,.2f}"
            
            # Calcular delta (comparação com média)
            mean_value = df[col_name].mean()
            delta = ((value / len(df)) - mean_value) / mean_value * 100 if mean_value != 0 else 0
            
            st.metric(
                label=col_name.replace('_', ' ').title(),
                value=formatted_value,
                delta=f"{delta:+.1f}%" if abs(delta) > 0.1 else None
            )


def render_gantt_chart(
    df: pd.DataFrame,
    config: Optional[Dict[str, str]] = None
) -> go.Figure:
    """
    Renderiza gráfico de Gantt interativo usando Plotly.
    
    Args:
        df: DataFrame com dados de cronograma.
        config: Configuração de mapeamento de colunas:
            - 'task_col': Coluna de atividades (padrão: 'atividade')
            - 'start_col': Coluna de início (padrão: 'inicio')
            - 'end_col': Coluna de término (padrão: 'fim')
            - 'resource_col': Coluna de responsável (padrão: 'responsavel')
            - 'color_col': Coluna para colorir barras (padrão: 'status')
    
    Returns:
        go.Figure: Objeto Figure do Plotly (também renderiza no Streamlit).
    
    Example:
        >>> config = {
        ...     'task_col': 'descricao',
        ...     'start_col': 'data_inicio',
        ...     'end_col': 'data_fim',
        ...     'color_col': 'fase'
        ... }
        >>> render_gantt_chart(df, config)
    """
    # Configuração padrão
    if config is None:
        config = {}
    
    task_col = config.get('task_col', _find_column(df, ['atividade', 'descricao', 'task']))
    start_col = config.get('start_col', _find_column(df, ['inicio', 'start', 'data_inicio']))
    end_col = config.get('end_col', _find_column(df, ['fim', 'end', 'data_fim']))
    resource_col = config.get('resource_col', _find_column(df, ['responsavel', 'resource', 'equipe']))
    color_col = config.get('color_col', _find_column(df, ['status', 'fase', 'categoria']))
    
    # Validar colunas obrigatórias
    if not all([task_col, start_col, end_col]):
        st.error("Colunas obrigatórias não encontradas para Gantt: atividade, inicio, fim")
        return None
    
    # Preparar dados
    df_gantt = df.copy()
    df_gantt[start_col] = pd.to_datetime(df_gantt[start_col])
    df_gantt[end_col] = pd.to_datetime(df_gantt[end_col])
    
    # Criar gráfico
    fig = px.timeline(
        df_gantt,
        x_start=start_col,
        x_end=end_col,
        y=task_col,
        color=color_col if color_col else None,
        hover_data=[resource_col] if resource_col else None,
        title="Cronograma de Atividades"
    )
    
    # Customizar layout
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Atividade",
        height=max(400, len(df_gantt) * 40),  # Altura dinâmica
        showlegend=True if color_col else False,
        hovermode='closest'
    )
    
    # Adicionar linha vertical "Hoje"
    fig.add_vline(
        x=datetime.now().timestamp() * 1000,
        line_dash="dash",
        line_color="red",
        annotation_text="Hoje",
        annotation_position="top"
    )
    
    # Renderizar no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def render_cost_breakdown_chart(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    chart_type: str = 'pie'
) -> go.Figure:
    """
    Renderiza gráfico de composição de custos (pizza ou barras).
    
    Args:
        df: DataFrame com dados de custos.
        category_col: Coluna de categorias (ex: 'tipo_insumo', 'fase').
        value_col: Coluna de valores (ex: 'custo', 'valor').
        chart_type: Tipo de gráfico ('pie', 'bar', 'treemap').
    
    Returns:
        go.Figure: Objeto Figure do Plotly.
    
    Example:
        >>> render_cost_breakdown_chart(
        ...     df,
        ...     category_col='tipo_insumo',
        ...     value_col='custo_total',
        ...     chart_type='pie'
        ... )
    """
    # Agregar por categoria
    df_agg = df.groupby(category_col)[value_col].sum().reset_index()
    df_agg = df_agg.sort_values(value_col, ascending=False)
    
    if chart_type == 'pie':
        fig = px.pie(
            df_agg,
            values=value_col,
            names=category_col,
            title=f"Composição de {value_col.replace('_', ' ').title()}"
        )
    
    elif chart_type == 'bar':
        fig = px.bar(
            df_agg,
            x=category_col,
            y=value_col,
            title=f"Distribuição de {value_col.replace('_', ' ').title()}",
            text=value_col
        )
        fig.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
    
    elif chart_type == 'treemap':
        fig = px.treemap(
            df_agg,
            path=[category_col],
            values=value_col,
            title=f"Treemap de {value_col.replace('_', ' ').title()}"
        )
    
    else:
        raise ValueError(f"Tipo de gráfico '{chart_type}' não suportado")
    
    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def render_eva_dashboard(
    pv: float,
    ev: float,
    ac: float,
    bac: float
) -> None:
    """
    Renderiza dashboard de Análise de Valor Agregado (EVA).
    
    Args:
        pv: Planned Value (Valor Planejado).
        ev: Earned Value (Valor Agregado).
        ac: Actual Cost (Custo Real).
        bac: Budget at Completion (Orçamento no Término).
    
    Example:
        >>> render_eva_dashboard(
        ...     pv=25000,
        ...     ev=20000,
        ...     ac=22000,
        ...     bac=50000
        ... )
    """
    st.subheader("📊 Análise de Valor Agregado (EVA)")
    
    # Calcular índices
    cpi = ev / ac if ac != 0 else 0
    spi = ev / pv if pv != 0 else 0
    cv = ev - ac
    sv = ev - pv
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "CPI (Custo)",
            f"{cpi:.2f}",
            delta="Bom" if cpi >= 1.0 else "Ruim",
            delta_color="normal" if cpi >= 1.0 else "inverse"
        )
    
    with col2:
        st.metric(
            "SPI (Prazo)",
            f"{spi:.2f}",
            delta="Bom" if spi >= 1.0 else "Ruim",
            delta_color="normal" if spi >= 1.0 else "inverse"
        )
    
    with col3:
        st.metric(
            "CV (Variação Custo)",
            f"R$ {cv:,.0f}",
            delta=f"{(cv/bac)*100:.1f}% do orçamento"
        )
    
    with col4:
        st.metric(
            "SV (Variação Prazo)",
            f"R$ {sv:,.0f}",
            delta=f"{(sv/pv)*100:.1f}% do planejado"
        )
    
    # Gráfico de curvas
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=['PV', 'EV', 'AC'],
        y=[pv, ev, ac],
        mode='lines+markers',
        name='Valores',
        line=dict(width=3)
    ))
    
    fig.update_layout(
        title="Curvas de Valor Agregado",
        xaxis_title="Métrica",
        yaxis_title="Valor (R$)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def _has_gantt_columns(df: pd.DataFrame) -> bool:
    """Verifica se DataFrame tem colunas necessárias para Gantt."""
    required_patterns = [
        ['atividade', 'descricao', 'task'],
        ['inicio', 'start', 'data_inicio'],
        ['fim', 'end', 'data_fim']
    ]
    
    for patterns in required_patterns:
        if not any(col.lower() in [p.lower() for p in patterns] for col in df.columns):
            return False
    
    return True


def _find_column(df: pd.DataFrame, patterns: List[str]) -> Optional[str]:
    """Encontra coluna que corresponde a um dos padrões."""
    for col in df.columns:
        if col.lower() in [p.lower() for p in patterns]:
            return col
    return None


# Exemplo de uso standalone
if __name__ == '__main__':
    # Dados de exemplo
    df_projeto = pd.DataFrame({
        'atividade': [
            'Fundação',
            'Estrutura',
            'Alvenaria',
            'Instalações',
            'Acabamento'
        ],
        'inicio': [
            '2026-01-01',
            '2026-02-01',
            '2026-03-01',
            '2026-04-01',
            '2026-05-01'
        ],
        'fim': [
            '2026-01-31',
            '2026-02-28',
            '2026-03-31',
            '2026-04-30',
            '2026-05-31'
        ],
        'custo': [50000, 120000, 60000, 80000, 70000],
        'status': ['Concluído', 'Em Andamento', 'Planejado', 'Planejado', 'Planejado'],
        'responsavel': ['Equipe A', 'Equipe B', 'Equipe A', 'Equipe C', 'Equipe B']
    })
    
    # Renderizar dashboard
    render_project_dashboard(
        df_projeto,
        title="Projeto Residencial XYZ",
        kpi_columns=['custo']
    )
    
    # Renderizar EVA
    st.divider()
    render_eva_dashboard(
        pv=250000,
        ev=200000,
        ac=220000,
        bac=500000
    )
