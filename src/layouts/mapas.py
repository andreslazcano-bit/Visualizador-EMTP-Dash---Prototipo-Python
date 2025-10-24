"""
Layout de mapas
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_mapa_layout():
    """Crea el layout del módulo de mapas"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4("🗺️ Módulo de Mapas", className="alert-heading"),
                    html.P("Este módulo estará disponible próximamente con:"),
                    html.Hr(),
                    html.Ul([
                        html.Li("Mapa interactivo de Chile"),
                        html.Li("Visualización de establecimientos EMTP"),
                        html.Li("Capas por indicadores"),
                        html.Li("Clustering de establecimientos"),
                        html.Li("Tooltips con información detallada"),
                    ])
                ], color="success")
            ])
        ])
    ], fluid=True)
