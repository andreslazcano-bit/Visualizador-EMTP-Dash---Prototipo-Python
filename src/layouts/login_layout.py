"""
============================================================================
LAYOUT DE LOGIN Y AUTENTICACIÓN
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from src.utils.auth import USER_PROFILES


def create_login_layout():
    """Crea el layout de login"""
    
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    # Logo y titulo
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.H1([
                                    html.I(className="fas fa-chart-area me-3", 
                                          style={"color": "var(--primary-color)"}),
                                    "Visualizador EMTP"
                                ], className="text-center text-primary mb-3"),
                                
                                html.P([
                                    "Sistema de análisis y visualización de datos del ",
                                    html.Strong("Sistema de Educación Media Técnico-Profesional"), 
                                    " de Chile."
                                ], className="text-center text-muted mb-4"),
                                
                                html.Hr(),
                                
                                # Formulario de login
                                html.H4("Iniciar Sesión", className="text-center mb-4"),
                                
                                dbc.Form([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label("Usuario:", className="fw-bold"),
                                            dbc.Input(
                                                id="login-username",
                                                type="text",
                                                placeholder="Ingrese su usuario",
                                                className="mb-3"
                                            )
                                        ])
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label("Contraseña:", className="fw-bold"),
                                            dbc.Input(
                                                id="login-password",
                                                type="password", 
                                                placeholder="Ingrese su contraseña",
                                                className="mb-3"
                                            )
                                        ])
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Ingresar",
                                                id="login-button",
                                                className="w-100 mb-3 btn-primary-custom",
                                                size="lg"
                                            )
                                        ])
                                    ]),
                                    
                                    # Mensaje de error
                                    html.Div(id="login-message", className="text-center")
                                ])
                                
                            ])
                        ])
                    ], className="shadow-lg border-0"),
                    
                    # Información de acceso admin
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5([
                                html.I(className="fas fa-info-circle me-2"),
                                "Acceso Administrador"
                            ], className="mb-0 text-info")
                        ]),
                        dbc.CardBody([
                            html.P("Ingrese con las siguientes credenciales para acceso completo:", 
                                   className="text-muted mb-3"),
                            
                            create_demo_users_table()
                        ])
                    ], className="mt-4 border-info")
                    
                ], md=8, lg=6, className="mx-auto")
            ], className="min-vh-100 d-flex align-items-center py-5")
        ], fluid=True),
        
    ], className="login-background")


def create_demo_users_table():
    """Crea tabla con información de usuario admin"""
    
    demo_info = [
        {
            'usuario': 'admin',
            'password': 'admin123', 
            'perfil': 'Administrador',
            'acceso': 'Acceso completo a todas las secciones'
        }
    ]
    
    return dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Usuario", className="text-primary"),
                html.Th("Contraseña", className="text-primary"),
                html.Th("Perfil", className="text-primary"),
                html.Th("Acceso", className="text-primary")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td([
                    html.Code(user['usuario'], className="text-dark bg-light p-1")
                ]),
                html.Td([
                    html.Code(user['password'], className="text-dark bg-light p-1")
                ]),
                html.Td(user['perfil'], className="fw-bold"),
                html.Td(user['acceso'], className="small text-muted")
            ]) for user in demo_info
        ])
    ], striped=True, hover=True, size="sm", className="mb-0")


def create_navbar_with_user(user_info):
    """Crea navbar con información del usuario logueado"""
    
    nav_items = []
    
    # Información del usuario
    nav_items.append(
        dbc.NavItem([
            html.Span([
                html.I(className="fas fa-user me-2"),
                user_info.get('full_name', user_info.get('username', 'Usuario')),
                html.Small(f" ({user_info.get('profile', 'usuario').title()})",
                          className="text-muted ms-2")
            ], className="navbar-text me-3")
        ])
    )
    
    # Botón para cambiar de modo (vuelve a pantalla de bienvenida)
    nav_items.append(
        dbc.NavItem([
            dbc.Button([
                html.I(className="fas fa-exchange-alt me-2"),
                "Cambiar Modo"
            ], id="logout-button", color="outline-light", size="sm")
        ])
    )
    
    # Toggle de tema
    nav_items.append(
        dbc.NavItem([
            dbc.Button([
                html.I(id="theme-icon", className="fas fa-moon")
            ], id="theme-toggle", className="theme-toggle ms-2")
        ])
    )
    
    return dbc.Navbar([
        dbc.Container([
            # Brand/Logo
            dbc.NavbarBrand([
                html.I(className="fas fa-chart-area me-2"),
                "Visualizador EMTP"
            ], href="#", className="fw-bold"),
            
            # Navegación
            dbc.Nav(nav_items, navbar=True)
        ])
    ], dark=True, className="navbar-custom mb-0")