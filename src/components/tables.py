"""
============================================================================
COMPONENTES DE TABLAS REUTILIZABLES
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd
from typing import Optional, List


def create_data_table(
    df: pd.DataFrame,
    table_id: str,
    columns: Optional[List[str]] = None,
    page_size: int = 10,
    style_table: Optional[dict] = None
) -> dash_table.DataTable:
    """
    Crea una tabla de datos interactiva
    
    Args:
        df: DataFrame con datos
        table_id: ID del componente
        columns: Lista de columnas a mostrar (None = todas)
        page_size: Filas por página
        style_table: Estilos personalizados
    
    Returns:
        DataTable de Dash
    """
    if columns is None:
        columns = df.columns.tolist()
    
    # Formatear columnas
    table_columns = [
        {
            "name": col.replace('_', ' ').title(),
            "id": col,
            "type": "numeric" if pd.api.types.is_numeric_dtype(df[col]) else "text"
        }
        for col in columns
    ]
    
    default_style_table = {
        'overflowX': 'auto',
        'maxHeight': '600px',
        'overflowY': 'auto'
    }
    
    if style_table:
        default_style_table.update(style_table)
    
    return dash_table.DataTable(
        id=table_id,
        columns=table_columns,
        data=df[columns].to_dict('records'),
        page_size=page_size,
        page_action='native',
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        style_table=default_style_table,
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'border': '1px solid black'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'border': '1px solid grey'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        export_format='xlsx',
        export_headers='display'
    )


def create_kpi_card(
    value: str,
    label: str,
    color: str = "primary",
    icon: Optional[str] = None
) -> dbc.Card:
    """
    Crea una tarjeta KPI
    
    Args:
        value: Valor a mostrar
        label: Etiqueta descriptiva
        color: Color del borde (primary, success, info, etc.)
        icon: Clase de icono FontAwesome (opcional)
    
    Returns:
        Card de Bootstrap con KPI
    """
    icon_element = html.I(className=f"{icon} me-2") if icon else None
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                icon_element,
                html.H3(value, className=f"text-{color} d-inline")
            ]),
            html.P(label, className="text-muted small mb-0")
        ])
    ], className="shadow-sm text-center")
