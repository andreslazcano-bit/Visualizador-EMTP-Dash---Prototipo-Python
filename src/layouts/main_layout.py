"""
============================================================================
LAYOUT PRINCIPAL - Visualizador EMTP (VERSIÓN CORREGIDA)
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_main_layout():
    """Crea el layout principal de la aplicación"""
    
    layout = html.Div([
        # Store para datos compartidos y tema
        dcc.Store(id='session-data', storage_type='session'),
        dcc.Store(id='user-data', storage_type='session'),
        dcc.Store(id='theme-store', data={'theme': 'light'}, storage_type='local'),
        
        # Botón toggle para modo oscuro
        html.Button([
            html.I(id="theme-icon", className="fas fa-adjust")
        ], 
        id="theme-toggle", 
        className="theme-toggle",
        title="Cambiar modo oscuro/claro"),
        
        # Container principal
        dbc.Container([
            # Header
            create_header(),
            
            html.Hr(),
            
            # Tabs principales con íconos vía CSS
            dbc.Tabs([
                dbc.Tab(
                    label="Matrícula EMTP", 
                    tab_id="tab-matricula",
                    className="nav-link tab-matricula"
                ),
                dbc.Tab(
                    label="Egresados EMTP en ESUP", 
                    tab_id="tab-egresados",
                    className="nav-link tab-egresados"
                ),
                dbc.Tab(
                    label="Titulación EMTP", 
                    tab_id="tab-titulacion",
                    className="nav-link tab-titulacion"
                ),
                dbc.Tab(
                    label="Establecimientos EMTP", 
                    tab_id="tab-establecimientos",
                    className="nav-link tab-establecimientos"
                ),
                dbc.Tab(
                    label="Docentes EMTP", 
                    tab_id="tab-docentes",
                    className="nav-link tab-docentes"
                ),
                dbc.Tab(
                    label="Proyectos SEEMTP", 
                    tab_id="tab-proyectos",
                    className="nav-link tab-proyectos"
                ),
            ], 
            id="main-tabs", 
            active_tab="tab-matricula",
            className="nav-tabs"),
            
            html.Br(),
            
            # Contenido dinámico según tab seleccionada
            html.Div(id="tab-content"),
            
            html.Hr(),
            
            # Footer
            create_footer(),
            
        ], fluid=True, className="py-3"),
        
        ], id="main-container", **{'data-dummy': ''})
    
    return layout


def create_header():
    """Crea el header de la aplicación"""
    return dbc.Row([
        dbc.Col([
            html.H1([
                html.I(className="fas fa-graduation-cap me-2 text-primary-custom"),
                "Visualizador EMTP"
            ], className="text-primary-custom mb-1", style={'fontWeight': 'bold'}),
            html.P(
                "Enseñanza Media Técnico Profesional en Chile",
                className="lead text-gray-dark mb-2"
            ),
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "Modo Demo - Datos simulados para demostración"
            ], className="alert-primary-custom py-2 mb-3", dismissable=True)
        ], md=8),
        dbc.Col([
            html.Div([
                dbc.ButtonGroup([
                    dbc.Button(
                        html.Span([html.I(className="fas fa-download me-1"), "Exportar"]),
                        id="btn-download",
                        className="btn-outline-primary-custom",
                        size="sm",
                        disabled=True
                    ),
                    dbc.Button(
                        html.Span([html.I(className="fas fa-file-pdf me-1"), "Reporte"]),
                        id="btn-report",
                        className="btn-outline-primary-custom",
                        size="sm",
                        disabled=True
                    ),
                ], className="mb-2"),
                html.Br(),
                dbc.Button(
                    html.Span([html.I(className="fas fa-user me-1"), "Iniciar Sesión"]),
                    id="btn-login",
                    className="btn-primary-custom",
                    size="sm",
                    disabled=True
                ),
            ], className="text-end")
        ], md=4),
    ])


def create_sub_tabs(tab_type):
    """Crea sub-pestañas según el tipo de tab principal"""
    
    sub_tabs_config = {
        "matricula": [
            {"label": "Evolución Anual", "value": "evolucion"},
            {"label": "Distribución Demográfica", "value": "demografia"},
            {"label": "Tasa de Retención", "value": "retencion"},
            {"label": "Comparación Sistema", "value": "comparacion"}
        ],
        "egresados": [
            {"label": "Tasa de Transición", "value": "transicion"},
            {"label": "Áreas y Carreras", "value": "areas"},
            {"label": "Distribución Geográfica", "value": "geografia"},
            {"label": "Análisis por Género", "value": "genero"}
        ],
        "titulacion": [
            {"label": "Evolución Titulados", "value": "evolucion"},
            {"label": "Tasa de Titulación", "value": "tasa"},
            {"label": "Tiempo de Titulación", "value": "tiempo"},
            {"label": "Análisis Comparativo", "value": "comparativo"}
        ],
        "establecimientos": [
            {"label": "Distribución Geográfica", "value": "geografia"},
            {"label": "Especialidades", "value": "especialidades"},
            {"label": "Dependencia", "value": "dependencia"},
            {"label": "Evolución Temporal", "value": "evolucion"}
        ],
        "docentes": [
            {"label": "Distribución Total", "value": "distribucion"},
            {"label": "Perfil Demográfico", "value": "demografia"},
            {"label": "Titulación", "value": "titulacion"},
            {"label": "Estabilidad Laboral", "value": "estabilidad"}
        ],
        "proyectos": [
            {"label": "Asignación de Recursos", "value": "recursos"},
            {"label": "Ejecución Financiera", "value": "ejecucion"},
            {"label": "Cobertura", "value": "cobertura"},
            {"label": "Evolución Anual", "value": "evolucion"}
        ]
    }
    
    if tab_type not in sub_tabs_config:
        return html.Div()
    
    tabs = sub_tabs_config[tab_type]
    
    return dbc.Tabs([
        dbc.Tab(label=tab["label"], tab_id=f"sub-{tab_type}-{tab['value']}")
        for tab in tabs
    ], id=f"sub-tabs-{tab_type}", active_tab=f"sub-{tab_type}-{tabs[0]['value']}", className="sub-tabs")


def create_footer():
    """Crea el footer de la aplicación"""
    return dbc.Row([
        dbc.Col([
            html.P([
                "Visualizador EMTP © 2025 | ",
                html.A("Documentación", href="#", className="text-decoration-none"),
                " | ",
                html.A("Soporte", href="#", className="text-decoration-none"),
            ], className="text-center text-muted small")
        ])
    ])