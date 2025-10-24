"""
Layout de docentes
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_docentes_layout():
    """Crea el layout del módulo de docentes"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4("👨‍🏫 Módulo de Docentes", className="alert-heading"),
                    html.P("Este módulo estará disponible próximamente con:"),
                    html.Hr(),
                    html.Ul([
                        html.Li("Distribución de docentes por establecimiento"),
                        html.Li("Análisis por especialidad"),
                        html.Li("Análisis de género y horas"),
                        html.Li("Filtros avanzados"),
                    ])
                ], color="info")
            ])
        ])
    ], fluid=True)
