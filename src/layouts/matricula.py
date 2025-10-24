"""
============================================================================
LAYOUT MATRÍCULA
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_matricula_layout():
    """Crea el layout del módulo de matrícula"""
    
    return dbc.Container([
        dbc.Row([
            # Panel de filtros
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5([
                        html.I(className="fas fa-filter me-2"),
                        "Filtros"
                    ])),
                    dbc.CardBody([
                        # Región
                        html.Label("Región", className="fw-bold"),
                        dcc.Dropdown(
                            id='filter-region-matricula',
                            options=[
                                {'label': 'Metropolitana', 'value': 'metropolitana'},
                                {'label': 'Valparaíso', 'value': 'valparaiso'},
                                {'label': 'Biobío', 'value': 'biobio'},
                                {'label': 'Araucanía', 'value': 'araucania'},
                            ],
                            placeholder="Seleccione región...",
                            multi=True
                        ),
                        html.Br(),
                        
                        # Comuna
                        html.Label("Comuna", className="fw-bold"),
                        dcc.Dropdown(
                            id='filter-comuna-matricula',
                            options=[
                                {'label': 'Santiago', 'value': 'santiago'},
                                {'label': 'Valparaíso', 'value': 'valparaiso'},
                                {'label': 'Concepción', 'value': 'concepcion'},
                            ],
                            placeholder="Seleccione comuna...",
                            multi=True
                        ),
                        html.Br(),
                        
                        # Dependencia
                        html.Label("Dependencia", className="fw-bold"),
                        dcc.Dropdown(
                            id='filter-dependencia-matricula',
                            options=[
                                {'label': 'Municipal', 'value': 'municipal'},
                                {'label': 'Particular Subvencionado', 'value': 'subvencionado'},
                                {'label': 'Particular Pagado', 'value': 'pagado'},
                            ],
                            placeholder="Seleccione dependencia...",
                            multi=True
                        ),
                        html.Br(),
                        
                        # Especialidad
                        html.Label("Especialidad", className="fw-bold"),
                        dcc.Dropdown(
                            id='filter-especialidad-matricula',
                            options=[
                                {'label': 'Administración', 'value': 'admin'},
                                {'label': 'Contabilidad', 'value': 'contabilidad'},
                                {'label': 'Electricidad', 'value': 'electricidad'},
                                {'label': 'Mecánica', 'value': 'mecanica'},
                            ],
                            placeholder="Seleccione especialidad...",
                            multi=True
                        ),
                        html.Br(),
                        
                        # Botones
                        dbc.ButtonGroup([
                            dbc.Button(
                                "Aplicar",
                                id="btn-apply-filters-matricula",
                                color="primary",
                                className="w-100"
                            ),
                            dbc.Button(
                                "Limpiar",
                                id="btn-clear-filters-matricula",
                                color="secondary",
                                className="w-100"
                            ),
                        ], className="w-100"),
                    ])
                ], className="shadow-sm")
            ], md=3),
            
            # Panel principal
            dbc.Col([
                # KPIs
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id="kpi-total-estudiantes", className="text-primary"),
                                html.P("Total Estudiantes", className="text-muted small")
                            ])
                        ], className="shadow-sm text-center")
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id="kpi-total-establecimientos", className="text-success"),
                                html.P("Establecimientos", className="text-muted small")
                            ])
                        ], className="shadow-sm text-center")
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id="kpi-total-especialidades", className="text-info"),
                                html.P("Especialidades", className="text-muted small")
                            ])
                        ], className="shadow-sm text-center")
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3(id="kpi-ratio-genero", className="text-warning"),
                                html.P("Ratio H/M", className="text-muted small")
                            ])
                        ], className="shadow-sm text-center")
                    ], md=3),
                ]),
                
                html.Br(),
                
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Matrícula por Región"),
                            dbc.CardBody([
                                dcc.Graph(id="graph-matricula-region")
                            ])
                        ], className="shadow-sm")
                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Top 10 Especialidades"),
                            dbc.CardBody([
                                dcc.Graph(id="graph-matricula-especialidades")
                            ])
                        ], className="shadow-sm")
                    ], md=6),
                ]),
                
                html.Br(),
                
                # Tabla de datos
                dbc.Card([
                    dbc.CardHeader("Datos Detallados"),
                    dbc.CardBody([
                        html.Div(id="table-matricula")
                    ])
                ], className="shadow-sm")
                
            ], md=9),
        ])
    ], fluid=True)
