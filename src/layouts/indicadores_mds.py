"""
============================================================================
LAYOUT - INDICADORES MDS (MINISTERIO DE DESARROLLO SOCIAL)
============================================================================
Visualización de indicadores solicitados por el Ministerio de Desarrollo Social
Solo accesible para usuarios con perfil Admin
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


def create_indicadores_mds_layout():
    """
    Crea el layout completo de Indicadores MDS con pestañas
    
    Estructura:
    - Indicadores de Propósito (2)
    - Indicadores Complementarios (3)
    """
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="fas fa-chart-line me-2"),
                    "Indicadores MDS"
                ], className="mb-2"),
                html.P(
                    "Indicadores solicitados por el Ministerio de Desarrollo Social para el seguimiento del programa EMTP",
                    className="text-muted mb-3"
                )
            ])
        ]),
        
        # Alerta de Datos Simulados
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.I(className="fas fa-info-circle me-2"),
                    html.Strong("Datos Simulados: "),
                    "Los datos mostrados actualmente son SIMULADOS con fines de demostración y no representan información real del sistema EMTP."
                ], color="warning", className="mb-4")
            ])
        ]),
        
        # Tabs de Indicadores
        dbc.Tabs([
            # Tab 1: Indicadores de Propósito
            dbc.Tab(
                create_indicadores_proposito(),
                label="📊 Indicadores de Propósito",
                tab_id="tab-proposito"
            ),
            
            # Tab 2: Indicadores Complementarios
            dbc.Tab(
                create_indicadores_complementarios(),
                label="📈 Indicadores Complementarios",
                tab_id="tab-complementarios"
            ),
        ], id="mds-tabs", active_tab="tab-proposito")
        
    ], fluid=True, className="p-4")


def create_indicadores_proposito():
    """
    Crea la pestaña de Indicadores de Propósito
    
    Incluye:
    1. % estudiantes egresados EMTP que ingresa a ES
    2. % docentes FD-TP que mejoran competencias de gestión curricular
    """
    
    return dbc.Container([
        html.H4("Indicadores de Propósito", className="mt-3 mb-4"),
        
        # Indicador 1: Ingreso a Educación Superior
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-graduation-cap me-2"),
                    "1. Porcentaje de estudiantes egresados de EMTP que ingresa a educación superior"
                ], className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6("Descripción", className="text-primary"),
                        html.P(
                            "Mide el porcentaje de estudiantes egresados de EMTP que logra ingresar a instituciones de educación superior en el periodo siguiente a su egreso.",
                            className="mb-3"
                        ),
                        html.H6("Fórmula de Cálculo", className="text-primary"),
                        dbc.Alert([
                            html.Strong("Indicador = "),
                            "(Número de estudiantes egresados de la EMTP afectos a este programa en el periodo t-1 que ingresan a la Educación Superior en el periodo t / Número total de estudiantes egresados de la EMTP afectos a este programa en el periodo t-1) × 100"
                        ], color="info", className="mb-3"),
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("KPIs Principales", className="text-primary"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop1-kpi-actual", className="text-center mb-0"),
                                        html.P("% Ingreso ES (2024)", className="text-center text-muted small mb-0")
                                    ])
                                ], color="primary", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop1-kpi-variacion", className="text-center mb-0"),
                                        html.P("Var. vs 2023", className="text-center text-muted small mb-0")
                                    ])
                                ], color="success", outline=True, className="mb-2")
                            ], md=6),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop1-kpi-total", className="text-center mb-0"),
                                        html.P("Total Egresados", className="text-center text-muted small mb-0")
                                    ])
                                ], color="secondary", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop1-kpi-es", className="text-center mb-0"),
                                        html.P("Ingresaron a ES", className="text-center text-muted small mb-0")
                                    ])
                                ], color="info", outline=True, className="mb-2")
                            ], md=6),
                        ])
                    ], md=12, lg=6)
                ]),
                
                html.Hr(),
                
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        html.H6("Evolución Temporal", className="text-primary mb-3"),
                        dcc.Graph(id="mds-prop1-evolucion")
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("Distribución por Región", className="text-primary mb-3"),
                        dcc.Graph(id="mds-prop1-region")
                    ], md=12, lg=6),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        html.H6("Por Especialidad", className="text-primary mb-3"),
                        dcc.Graph(id="mds-prop1-especialidad")
                    ], md=12)
                ])
            ])
        ], className="mb-4"),
        
        # Indicador 2: Docentes con Competencias Mejoradas
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-chalkboard-teacher me-2"),
                    "2. Porcentaje de docentes de Formación Diferenciada Técnico Profesional que mejoran sus competencias de gestión curricular"
                ], className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6("Descripción", className="text-primary"),
                        html.P(
                            "Mide el porcentaje de docentes de Formación Diferenciada Técnico Profesional que aprueban exitosamente "
                            "capacitaciones orientadas a mejorar sus competencias de gestión curricular, en el marco del programa EMTP.",
                            className="mb-3"
                        ),
                        html.H6("Fórmula de Cálculo", className="text-primary"),
                        dbc.Alert([
                            html.Strong("Indicador = "),
                            "(N° total de docentes que aprueban capacitaciones en el marco del programa, en cualquiera de sus componentes año t / "
                            "N° total de docentes que participa de capacitaciones en el marco del programa, en cualquiera de sus componentes año t) × 100"
                        ], color="info", className="mb-3"),
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("KPIs Principales", className="text-primary"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop2-kpi-actual", className="text-center mb-0"),
                                        html.P("% Mejora (2024)", className="text-center text-muted small mb-0")
                                    ])
                                ], color="primary", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop2-kpi-capacitados", className="text-center mb-0"),
                                        html.P("Capacitados", className="text-center text-muted small mb-0")
                                    ])
                                ], color="success", outline=True, className="mb-2")
                            ], md=6),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop2-kpi-mejoraron", className="text-center mb-0"),
                                        html.P("Mejoraron", className="text-center text-muted small mb-0")
                                    ])
                                ], color="info", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-prop2-kpi-meta", className="text-center mb-0"),
                                        html.P("Meta Anual", className="text-center text-muted small mb-0")
                                    ])
                                ], color="warning", outline=True, className="mb-2")
                            ], md=6),
                        ])
                    ], md=12, lg=6)
                ]),
                
                html.Hr(),
                
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        html.H6("Evolución Anual", className="text-primary mb-3"),
                        dcc.Graph(id="mds-prop2-evolucion")
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("Por Región", className="text-primary mb-3"),
                        dcc.Graph(id="mds-prop2-region")
                    ], md=12, lg=6),
                ])
            ])
        ], className="mb-4"),
        
    ], fluid=True)


def create_indicadores_complementarios():
    """
    Crea la pestaña de Indicadores Complementarios
    
    Incluye:
    1. % EE EMTP que mejoran equipamiento (últimos 3 años)
    2. % SLEP con UAT-TP que mejoran competencias
    3. % EE EMTP que participa en redes de trabajo colaborativo
    """
    
    return dbc.Container([
        html.H4("Indicadores Complementarios", className="mt-3 mb-4"),
        
        # Indicador 1: Mejora de Equipamiento
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-tools me-2"),
                    "1. Porcentaje de establecimientos de EMTP que han mejorado su equipamiento para especialidades por medio de Convenios con Mineduc, en los últimos 3 años"
                ], className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6("Descripción", className="text-primary"),
                        html.P(
                            "Mide el porcentaje acumulado de establecimientos de EMTP que han mejorado su equipamiento para "
                            "especialidades técnicas mediante convenios con MINEDUC durante los últimos tres años.",
                            className="mb-3"
                        ),
                        html.H6("Fórmula de Cálculo", className="text-primary"),
                        dbc.Alert([
                            html.Strong("Indicador = "),
                            "(Número acumulado de establecimientos de EMTP que han mejorado su equipamiento para especialidades por medio de convenios con Mineduc desde el año t-3 / "
                            "Número total de establecimientos de EMTP en el año t) × 100"
                        ], color="info", className="mb-3"),
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("KPIs Principales", className="text-primary"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp1-kpi-actual", className="text-center mb-0"),
                                        html.P("% EE Mejorados", className="text-center text-muted small mb-0")
                                    ])
                                ], color="primary", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp1-kpi-total-ee", className="text-center mb-0"),
                                        html.P("Total EE EMTP", className="text-center text-muted small mb-0")
                                    ])
                                ], color="secondary", outline=True, className="mb-2")
                            ], md=6),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp1-kpi-mejorados", className="text-center mb-0"),
                                        html.P("EE Mejorados", className="text-center text-muted small mb-0")
                                    ])
                                ], color="success", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp1-kpi-periodo", className="text-center mb-0"),
                                        html.P("Período", className="text-center text-muted small mb-0")
                                    ])
                                ], color="info", outline=True, className="mb-2")
                            ], md=6),
                        ])
                    ], md=12, lg=6)
                ]),
                
                html.Hr(),
                
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        html.H6("Evolución Últimos 3 Años", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp1-evolucion")
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("Por Tipo de Equipamiento", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp1-equipamiento")
                    ], md=12, lg=6),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        html.H6("Distribución Regional", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp1-region")
                    ], md=12)
                ])
            ])
        ], className="mb-4"),
        
        # Indicador 2: SLEP - Competencias UAT-TP
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-users-cog me-2"),
                    "2. Porcentaje de SLEP cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional mejoran sus competencias para el acompañamiento en las especificidades de la EMTP"
                ], className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6("Descripción", className="text-primary"),
                        html.P(
                            "Mide el porcentaje de SLEP (Servicios Locales de Educación Pública) cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional (UAT-TP) "
                            "concluyen exitosamente instancias de capacitación para el acompañamiento en las especificidades de la EMTP.",
                            className="mb-3"
                        ),
                        html.H6("Fórmula de Cálculo", className="text-primary"),
                        dbc.Alert([
                            html.Strong("Indicador = "),
                            "(Número SLEP cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional concluyen con éxito instancias de capacitación para el acompañamiento en las especificidades de la EMTP año t / "
                            "Número total de SLEP en funcionamiento año t) × 100"
                        ], color="info", className="mb-3"),
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("KPIs Principales", className="text-primary"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp2-kpi-actual", className="text-center mb-0"),
                                        html.P("% SLEP Mejorados", className="text-center text-muted small mb-0")
                                    ])
                                ], color="primary", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp2-kpi-total", className="text-center mb-0"),
                                        html.P("Total SLEP", className="text-center text-muted small mb-0")
                                    ])
                                ], color="secondary", outline=True, className="mb-2")
                            ], md=6),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp2-kpi-mejorados", className="text-center mb-0"),
                                        html.P("SLEP Mejorados", className="text-center text-muted small mb-0")
                                    ])
                                ], color="success", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp2-kpi-programa", className="text-center mb-0"),
                                        html.P("En Programa", className="text-center text-muted small mb-0")
                                    ])
                                ], color="info", outline=True, className="mb-2")
                            ], md=6),
                        ])
                    ], md=12, lg=6)
                ]),
                
                html.Hr(),
                
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        html.H6("Progreso por SLEP", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp2-slep")
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("Áreas de Competencia Mejoradas", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp2-competencias")
                    ], md=12, lg=6),
                ])
            ])
        ], className="mb-4"),
        
        # Indicador 3: Redes de Trabajo Colaborativo
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-network-wired me-2"),
                    "3. Porcentaje de establecimientos de EMTP que participa y desarrolla actividades en redes de trabajo colaborativo a nivel territorial a lo largo del año"
                ], className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6("Descripción", className="text-primary"),
                        html.P(
                            "Mide el porcentaje de establecimientos de EMTP que participa activamente y desarrolla actividades en "
                            "redes de trabajo colaborativo a nivel territorial durante el año.",
                            className="mb-3"
                        ),
                        html.H6("Fórmula de Cálculo", className="text-primary"),
                        dbc.Alert([
                            html.Strong("Indicador = "),
                            "(Número de establecimientos de EMTP que participa y desarrolla actividades en redes de trabajo colaborativo a nivel territorial en el año t / "
                            "Número total de establecimientos EMTP del país en el año t) × 100"
                        ], color="info", className="mb-3"),
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("KPIs Principales", className="text-primary"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp3-kpi-actual", className="text-center mb-0"),
                                        html.P("% Participación", className="text-center text-muted small mb-0")
                                    ])
                                ], color="primary", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp3-kpi-total", className="text-center mb-0"),
                                        html.P("Total EE EMTP", className="text-center text-muted small mb-0")
                                    ])
                                ], color="secondary", outline=True, className="mb-2")
                            ], md=6),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp3-kpi-participan", className="text-center mb-0"),
                                        html.P("EE en Redes", className="text-center text-muted small mb-0")
                                    ])
                                ], color="success", outline=True, className="mb-2")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H3(id="mds-comp3-kpi-redes", className="text-center mb-0"),
                                        html.P("Nº Redes Activas", className="text-center text-muted small mb-0")
                                    ])
                                ], color="info", outline=True, className="mb-2")
                            ], md=6),
                        ])
                    ], md=12, lg=6)
                ]),
                
                html.Hr(),
                
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        html.H6("Participación por Región", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp3-region")
                    ], md=12, lg=6),
                    dbc.Col([
                        html.H6("Tipos de Redes", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp3-tipos")
                    ], md=12, lg=6),
                ]),
                
                dbc.Row([
                    dbc.Col([
                        html.H6("Frecuencia de Actividades", className="text-primary mb-3"),
                        dcc.Graph(id="mds-comp3-frecuencia")
                    ], md=12)
                ])
            ])
        ], className="mb-4"),
        
    ], fluid=True)
