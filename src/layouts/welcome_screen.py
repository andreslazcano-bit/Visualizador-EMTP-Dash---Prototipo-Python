"""
============================================================================
PANTALLA DE BIENVENIDA Y SELECCIÓN DE MODO
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_welcome_screen():
    """Crea la pantalla de bienvenida con selección de modo"""
    
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    # Logo y título principal
                    html.Div([
                        html.I(className="fas fa-chart-area", 
                              style={"fontSize": "80px", "color": "var(--primary-color)"}),
                        html.H1("Visualizador EMTP", className="mt-4 mb-2"),
                        html.P([
                            "Sistema de análisis y visualización de datos del ",
                            html.Strong("Sistema de Educación Media Técnico-Profesional"), 
                            " de Chile."
                        ], className="text-muted mb-5 lead")
                    ], className="text-center mb-5"),
                    
                    # Tarjetas de selección de modo
                    dbc.Row([
                        # Modo Usuario
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-user fa-3x mb-3", 
                                              style={"color": "var(--primary-color)"}),
                                        html.H3("Modo Usuario", className="mb-3"),
                                        html.P([
                                            "Acceso directo sin autenticación.",
                                            html.Br(),
                                            "Visualización de datos principales."
                                        ], className="text-muted mb-4"),
                                        
                                        html.Ul([
                                            html.Li("Matrícula"),
                                            html.Li("Egresados"),
                                            html.Li("Titulación"),
                                            html.Li("Establecimientos"),
                                            html.Li("Docentes")
                                        ], className="text-start mb-4"),
                                        
                                        dbc.Button([
                                            html.I(className="fas fa-arrow-right me-2"),
                                            "Acceder"
                                        ], id="btn-modo-usuario", 
                                           size="lg", 
                                           className="w-100 btn-primary-custom")
                                    ], className="text-center")
                                ])
                            ], className="shadow-lg border-0 h-100 hover-card")
                        ], md=6, className="mb-4"),
                        
                        # Modo Administrador
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-user-shield fa-3x mb-3", 
                                              style={"color": "var(--secondary-color)"}),
                                        html.H3("Modo Administrador", className="mb-3"),
                                        html.P([
                                            "Acceso completo con autenticación.",
                                            html.Br(),
                                            "Incluye gestión de proyectos."
                                        ], className="text-muted mb-4"),
                                        
                                        html.Ul([
                                            html.Li("Todas las secciones"),
                                            html.Li("Gestión de Proyectos"),
                                            html.Li("Exportación de datos"),
                                            html.Li("Configuración avanzada")
                                        ], className="text-start mb-4"),
                                        
                                        dbc.Button([
                                            html.I(className="fas fa-lock me-2"),
                                            "Iniciar Sesión"
                                        ], id="btn-modo-admin", 
                                           size="lg", 
                                           className="w-100 btn-secondary-custom")
                                    ], className="text-center")
                                ])
                            ], className="shadow-lg border-0 h-100 hover-card")
                        ], md=6, className="mb-4")
                    ])
                    
                ], md=10, lg=8, className="mx-auto")
            ], className="min-vh-100 d-flex align-items-center py-5")
        ], fluid=True),
        
        # Modal para login admin
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle([
                html.I(className="fas fa-user-shield me-2"),
                "Acceso Administrador"
            ])),
            dbc.ModalBody([
                html.P("Ingrese la contraseña de administrador:", className="text-muted mb-3"),
                
                dbc.Input(
                    id="admin-password-input",
                    type="password",
                    placeholder="Contraseña",
                    className="mb-3"
                ),
                
                html.Div(id="admin-login-message")
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancel-admin", color="light", className="me-2"),
                dbc.Button([
                    html.I(className="fas fa-check me-2"),
                    "Acceder"
                ], id="btn-confirm-admin", className="btn-secondary-custom")
            ])
        ], id="modal-admin-login", is_open=False, centered=True)
        
    ], className="welcome-screen", style={
        "background": "linear-gradient(135deg, #34536A 0%, #5A6E79 50%, #2A4255 100%)",
        "minHeight": "100vh"
    })


def create_welcome_layout():
    """Crea el layout completo de bienvenida con stores necesarios"""
    
    return html.Div([
        # Pantalla de bienvenida (los stores viven en el layout raíz en app_v2)
        create_welcome_screen()
    ])


def add_welcome_screen_styles():
    """Retorna estilos CSS adicionales para la pantalla de bienvenida"""
    
    return """
    .welcome-screen {
        animation: fadeIn 0.5s ease-in;
    }
    
    .welcome-screen .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .welcome-screen .hover-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
    }
    
    .welcome-screen h1 {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .welcome-screen .lead {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    """
