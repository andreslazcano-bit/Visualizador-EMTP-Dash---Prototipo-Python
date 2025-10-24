"""
============================================================================
COMPONENTES DE FILTROS REUTILIZABLES
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from typing import List, Optional


def create_filter_panel(
    filters: List[dict],
    panel_title: str = "Filtros"
) -> dbc.Card:
    """
    Crea un panel de filtros reutilizable
    
    Args:
        filters: Lista de configuraciones de filtros
        panel_title: Título del panel
    
    Returns:
        Card de Bootstrap con filtros
    
    Ejemplo:
        filters = [
            {
                'id': 'filter-region',
                'label': 'Región',
                'type': 'dropdown',
                'options': [...],
                'multi': True
            }
        ]
    """
    filter_components = []
    
    for filter_config in filters:
        filter_type = filter_config.get('type', 'dropdown')
        filter_id = filter_config.get('id')
        label = filter_config.get('label', '')
        
        # Label
        filter_components.append(
            html.Label(label, className="fw-bold")
        )
        
        # Componente según tipo
        if filter_type == 'dropdown':
            component = dcc.Dropdown(
                id=filter_id,
                options=filter_config.get('options', []),
                multi=filter_config.get('multi', False),
                placeholder=filter_config.get('placeholder', f"Seleccione {label}..."),
                className="mb-3"
            )
        
        elif filter_type == 'date':
            component = dcc.DatePickerRange(
                id=filter_id,
                display_format='DD/MM/YYYY',
                className="mb-3"
            )
        
        elif filter_type == 'slider':
            component = dcc.RangeSlider(
                id=filter_id,
                min=filter_config.get('min', 0),
                max=filter_config.get('max', 100),
                step=filter_config.get('step', 1),
                className="mb-3"
            )
        
        else:
            component = html.Div(f"Tipo de filtro no soportado: {filter_type}")
        
        filter_components.append(component)
        filter_components.append(html.Br())
    
    # Botones de acción
    filter_components.append(
        dbc.ButtonGroup([
            dbc.Button("Aplicar", id="btn-apply-filters", color="primary", className="w-100"),
            dbc.Button("Limpiar", id="btn-clear-filters", color="secondary", className="w-100"),
        ], className="w-100")
    )
    
    return dbc.Card([
        dbc.CardHeader(html.H5([
            html.I(className="fas fa-filter me-2"),
            panel_title
        ])),
        dbc.CardBody(filter_components)
    ], className="shadow-sm")


def create_multi_select(
    id: str,
    label: str,
    options: List[dict],
    placeholder: Optional[str] = None
) -> html.Div:
    """
    Crea un selector múltiple
    
    Args:
        id: ID del componente
        label: Etiqueta
        options: Lista de opciones
        placeholder: Texto placeholder
    
    Returns:
        Div con label y dropdown
    """
    return html.Div([
        html.Label(label, className="fw-bold"),
        dcc.Dropdown(
            id=id,
            options=options,
            multi=True,
            placeholder=placeholder or f"Seleccione {label}...",
            className="mb-3"
        )
    ])
