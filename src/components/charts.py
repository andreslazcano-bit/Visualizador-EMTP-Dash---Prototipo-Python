"""
============================================================================
COMPONENTES DE GRÁFICOS REUTILIZABLES
============================================================================
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List


def create_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    color: Optional[str] = None,
    orientation: str = 'v'
) -> go.Figure:
    """
    Crea un gráfico de barras
    
    Args:
        df: DataFrame con datos
        x_col: Columna para eje X
        y_col: Columna para eje Y
        title: Título del gráfico
        color: Columna para colorear
        orientation: 'v' vertical o 'h' horizontal
    
    Returns:
        Figura de Plotly
    """
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color=color,
        orientation=orientation,
        template='plotly_white'
    )
    
    fig.update_layout(
        title_font_size=16,
        hovermode='closest',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    color: Optional[str] = None
) -> go.Figure:
    """
    Crea un gráfico de líneas
    
    Args:
        df: DataFrame con datos
        x_col: Columna para eje X
        y_col: Columna para eje Y
        title: Título del gráfico
        color: Columna para separar líneas
    
    Returns:
        Figura de Plotly
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color=color,
        template='plotly_white',
        markers=True
    )
    
    fig.update_layout(
        title_font_size=16,
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: str = ""
) -> go.Figure:
    """
    Crea un gráfico de torta
    
    Args:
        df: DataFrame con datos
        names_col: Columna con nombres/categorías
        values_col: Columna con valores
        title: Título del gráfico
    
    Returns:
        Figura de Plotly
    """
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        template='plotly_white'
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    fig.update_layout(
        title_font_size=16,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig


def create_choropleth_map(
    df: pd.DataFrame,
    geojson,
    locations_col: str,
    color_col: str,
    title: str = ""
) -> go.Figure:
    """
    Crea un mapa coroplético
    
    Args:
        df: DataFrame con datos
        geojson: GeoJSON con geometrías
        locations_col: Columna con códigos de ubicación
        color_col: Columna con valores para colorear
        title: Título del mapa
    
    Returns:
        Figura de Plotly
    """
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations=locations_col,
        color=color_col,
        mapbox_style="carto-positron",
        zoom=4,
        center={"lat": -33.45, "lon": -70.65},
        title=title,
        opacity=0.7
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    
    return fig
