"""
============================================================================
LAYOUT PRINCIPAL CON SIDEBAR IZQUIERDO
============================================================================
Layout mejorado con navegación lateral y filtros completos
"""

import dash_bootstrap_components as dbc
from dash import html, dcc


def create_advanced_filters():
    """Crea filtros avanzados para el sistema EMTP"""
    
    # Opciones de filtros basadas en datos reales
    regiones = [
        "Todas las regiones", "Arica y Parinacota", "Tarapacá", "Antofagasta", 
        "Atacama", "Coquimbo", "Valparaíso", "Metropolitana", "O'Higgins", 
        "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos", 
        "Los Lagos", "Aysén", "Magallanes"
    ]
    
    especialidades = [
        "Todas las especialidades", "Administración", "Electricidad", 
        "Mecánica Industrial", "Construcción", "Gastronomía", "Contabilidad", 
        "Enfermería", "Programación", "Telecomunicaciones", "Soldadura", 
        "Turismo", "Párvulos", "Agropecuaria", "Forestal", "Acuicultura", 
        "Minería", "Química Industrial"
    ]
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-filter me-2", style={"color": "var(--primary-color)"}),
                "Filtros"
            ], className="mb-0 text-primary-custom")
        ]),
        dbc.CardBody([
            # Filtro por Año
            html.Div([
                html.Label([
                    html.I(className="fas fa-calendar me-2", style={"color": "var(--primary-color)"}),
                    "Año:"
                ], className="filter-label fw-bold mb-2"),
                dcc.RangeSlider(
                    id='filter-years',
                    min=2015,
                    max=2024,
                    value=[2020, 2024],
                    marks={year: str(year) for year in [2015, 2018, 2021, 2024]},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], className="mb-4"),
            
            # Filtro por Región
            html.Div([
                html.Label([
                    html.I(className="fas fa-map-marker-alt me-2", style={"color": "var(--primary-color)"}),
                    "Región:"
                ], className="filter-label fw-bold mb-2"),
                dcc.Dropdown(
                    id='filter-region',
                    options=[{'label': region, 'value': region} for region in regiones],
                    value='Todas las regiones',
                    style={'borderColor': '#A8B7C7'}
                )
            ], className="mb-3"),
            
            # Filtro por Especialidad
            html.Div([
                html.Label([
                    html.I(className="fas fa-tools me-2", style={"color": "var(--primary-color)"}),
                    "Especialidad:"
                ], className="filter-label fw-bold mb-2"),
                dcc.Dropdown(
                    id='filter-especialidad',
                    options=[{'label': esp, 'value': esp} for esp in especialidades],
                    value='Todas las especialidades',
                    multi=True,
                    placeholder="Selecciona especialidades...",
                    style={'borderColor': '#A8B7C7'}
                )
            ], className="mb-3"),
            
            # Filtro por Dependencia
            html.Div([
                html.Label([
                    html.I(className="fas fa-university me-2", style={"color": "var(--primary-color)"}),
                    "Dependencia:"
                ], className="filter-label fw-bold mb-2"),
                dcc.Dropdown(
                    id='filter-dependencia',
                    options=[
                        {'label': 'Todas las dependencias', 'value': 'todas'},
                        {'label': 'Municipal', 'value': 'Municipal'},
                        {'label': 'Particular Subvencionado', 'value': 'Particular Subvencionado'},
                        {'label': 'Particular', 'value': 'Particular'}
                    ],
                    value='todas',
                    style={'borderColor': '#A8B7C7'}
                )
            ], className="mb-3"),
            
            # Filtro por Género
            html.Div([
                html.Label([
                    html.I(className="fas fa-user-friends me-2", style={"color": "var(--primary-color)"}),
                    "Género:"
                ], className="filter-label fw-bold mb-2"),
                dcc.Dropdown(
                    id='filter-genero',
                    options=[
                        {'label': 'Ambos', 'value': 'ambos'},
                        {'label': 'Masculino', 'value': 'Masculino'},
                        {'label': 'Femenino', 'value': 'Femenino'}
                    ],
                    value='ambos',
                    style={'borderColor': '#A8B7C7'}
                )
            ], className="mb-3"),
            
            # Filtro por Zona
            html.Div([
                html.Label([
                    html.I(className="fas fa-city me-2", style={"color": "var(--primary-color)"}),
                    "Zona:"
                ], className="filter-label fw-bold mb-2"),
                dcc.Dropdown(
                    id='filter-zona',
                    options=[
                        {'label': 'Ambas zonas', 'value': 'ambas'},
                        {'label': 'Urbana', 'value': 'Urbana'},
                        {'label': 'Rural', 'value': 'Rural'}
                    ],
                    value='ambas',
                    style={'borderColor': '#A8B7C7'}
                )
            ], className="mb-4"),
            
            # Botones de acción
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-filter me-2"), "Aplicar"],
                        className="btn-primary-custom w-100 mb-2",
                        id="apply-filters-btn"
                    )
                ], width=12),
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-eraser me-2"), "Limpiar"],
                        className="btn-outline-primary-custom w-100",
                        id="clear-filters-btn"
                    )
                ], width=12)
            ])
        ])
    ], className="mb-4 border-accent-custom")


def create_sidebar_navigation_filtered(hidden_sections=None):
    """Crea la navegación lateral filtrada según perfil de usuario"""
    if hidden_sections is None:
        hidden_sections = []
    
    nav_items = []
    
    # Inicio (siempre visible)
    nav_items.append(
        dbc.ListGroupItem([
            html.Div([
                html.I(className="fas fa-home me-2", style={"color": "var(--primary-color)"}),
                "Inicio"
            ])
        ], id="nav-inicio", n_clicks=0, action=True, className="fw-bold mb-2 active")
    )
    
    # Matrícula
    if 'matricula' not in hidden_sections:
        nav_items.extend([
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-user-graduate me-2", style={"color": "var(--primary-color)"}),
                    "Matrícula"
                ])
            ], id="nav-matricula", n_clicks=0, action=True, className="fw-bold mb-1"),
            
            # Sub-pestañas de Matrícula
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-chart-area me-2", style={"color": "var(--text-secondary)"}), 
                    "Evolución Anual"
                ])
            ], id="sub-matricula-evolucion", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-user-friends me-2", style={"color": "var(--text-secondary)"}), 
                    "Demografía"
                ])
            ], id="sub-matricula-demografia", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-user-check me-2", style={"color": "var(--text-secondary)"}), 
                    "Retención"
                ])
            ], id="sub-matricula-retencion", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-chart-bar me-2", style={"color": "var(--text-secondary)"}), 
                    "Comparación"
                ])
            ], id="sub-matricula-comparacion", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
        ])
    
    # Egresados 
    if 'egresados' not in hidden_sections:
        nav_items.extend([
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-graduation-cap me-2", style={"color": "var(--primary-color)"}),
                    "Egresados"
                ])
            ], id="nav-egresados", n_clicks=0, action=True, className="fw-bold mb-1"),
            
            # Sub-pestañas de Egresados
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-arrow-right me-2", style={"color": "var(--text-secondary)"}), 
                    "Transición Laboral"
                ])
            ], id="sub-egresados-transicion", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-briefcase me-2", style={"color": "var(--text-secondary)"}), 
                    "Empleabilidad"
                ])
            ], id="sub-egresados-empleabilidad", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
        ])
    
    # Titulación
    if 'titulacion' not in hidden_sections:
        nav_items.extend([
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-certificate me-2", style={"color": "var(--primary-color)"}),
                    "Titulación"  
                ])
            ], id="nav-titulacion", n_clicks=0, action=True, className="fw-bold mb-1"),
            
            # Sub-pestañas de Titulación
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-percentage me-2", style={"color": "var(--text-secondary)"}), 
                    "Tasas de Titulación"
                ])
            ], id="sub-titulacion-tasas", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-clock me-2", style={"color": "var(--text-secondary)"}), 
                    "Tiempo de Titulación"
                ])
            ], id="sub-titulacion-tiempo", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
        ])
    
    # Establecimientos
    if 'establecimientos' not in hidden_sections:
        nav_items.extend([
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-school me-2", style={"color": "var(--primary-color)"}),
                    "Establecimientos"
                ])
            ], id="nav-establecimientos", n_clicks=0, action=True, className="fw-bold mb-1"),
            
            # Sub-pestañas de Establecimientos
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-map-marker-alt me-2", style={"color": "var(--text-secondary)"}), 
                    "Distribución Geográfica"
                ])
            ], id="sub-establecimientos-geografia", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-building me-2", style={"color": "var(--text-secondary)"}), 
                    "Infraestructura"
                ])
            ], id="sub-establecimientos-infraestructura", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
        ])
    
    # Docentes
    if 'docentes' not in hidden_sections:
        nav_items.extend([
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-chalkboard-teacher me-2", style={"color": "var(--primary-color)"}),
                    "Docentes"
                ])
            ], id="nav-docentes", n_clicks=0, action=True, className="fw-bold mb-1"),
            
            # Sub-pestañas de Docentes
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-user-tie me-2", style={"color": "var(--text-secondary)"}), 
                    "Perfil Profesional"
                ])
            ], id="sub-docentes-perfil", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-graduation-cap me-2", style={"color": "var(--text-secondary)"}), 
                    "Capacitación"
                ])
            ], id="sub-docentes-capacitacion", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
        ])
    
    # Mapas
    if 'mapas' not in hidden_sections:
        nav_items.append(
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-map-marked-alt me-2", style={"color": "var(--primary-color)"}),
                    "Mapas"
                ])
            ], id="nav-mapas", n_clicks=0, action=True, className="fw-bold mb-1")
        )
    
    # Proyectos SEEMTP (oculto para usuario básico)
    if 'proyectos' not in hidden_sections:
        nav_items.extend([
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-tasks me-2", style={"color": "var(--primary-color)"}),
                    "Proyectos SEEMTP"
                ])
            ], id="nav-proyectos", n_clicks=0, action=True, className="fw-bold mb-1"),
            
            # Sub-pestañas de Proyectos
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-dollar-sign me-2", style={"color": "var(--text-secondary)"}), 
                    "Financiamiento"
                ])
            ], id="sub-proyectos-financiamiento", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
            
            dbc.ListGroupItem([
                html.Div([
                    html.I(className="fas fa-chart-line me-2", style={"color": "var(--text-secondary)"}), 
                    "Impacto y Resultados"
                ])
            ], id="sub-proyectos-impacto", n_clicks=0, action=True, 
               className="ps-4 small sub-nav", style={"display": "none"}),
        ])
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-compass me-2", style={"color": "var(--primary-color)"}),
                "Navegación"
            ], className="mb-0 text-primary-custom")
        ]),
        dbc.CardBody([
            dbc.ListGroup(nav_items, flush=True)
        ], className="p-0")
    ], className="mb-4 border-accent-custom")


def create_sidebar_layout_filtered(hidden_sections=None):
    """Crea el layout del sidebar izquierdo filtrado según perfil"""
    return html.Div([
        # Navegación filtrada
        create_sidebar_navigation_filtered(hidden_sections),
        
        # Filtros avanzados
        create_advanced_filters(),
        
        # Información adicional
        dbc.Card([
            dbc.CardBody([
                html.H6([
                    html.I(className="fas fa-info-circle me-2", style={"color": "var(--primary-color)"}),
                    "Información"
                ], className="text-primary-custom mb-3"),
                html.P([
                    "Los datos mostrados son simulados para efectos de demostración. ",
                    "Basados en estadísticas reales del sistema EMTP chileno."
                ], className="small text-muted mb-2"),
                html.P([
                    html.I(className="fas fa-database me-2", style={"color": "var(--primary-color)"}),
                    "Total registros: ", html.Strong("36.411", className="text-primary-custom")
                ], className="small mb-1"),
                html.P([
                    html.I(className="fas fa-calendar me-2", style={"color": "var(--primary-color)"}),
                    "Período: ", html.Strong("2015-2024", className="text-primary-custom")
                ], className="small mb-0")
            ])
        ], className="border-accent-custom")
        
    ], id="sidebar-content")


def create_sidebar_navigation():
    """Crea la navegación lateral con pestañas principales y sub-pestañas"""
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-compass me-2", style={"color": "var(--primary-color)"}),
                "Navegación"
            ], className="mb-0 text-primary-custom")
        ]),
        dbc.CardBody([
            dbc.ListGroup([
                # Inicio
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-home me-2", style={"color": "var(--primary-color)"}),
                        "Inicio"
                    ])
                ], id="nav-inicio", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                # Matrícula
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-user-graduate me-2", style={"color": "var(--primary-color)"}),
                        "Matrícula"
                    ])
                ], id="nav-matricula", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-chart-line me-2", style={"color": "var(--text-secondary)"}), 
                        "Evolución Anual"
                    ])
                ], id="sub-matricula-evolucion", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-users me-2", style={"color": "var(--text-secondary)"}), 
                        "Demografía"
                    ])
                ], id="sub-matricula-demografia", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-shield-alt me-2", style={"color": "var(--text-secondary)"}), 
                        "Retención"
                    ])
                ], id="sub-matricula-retencion", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-balance-scale me-2", style={"color": "var(--text-secondary)"}), 
                        "Comparación"
                    ])
                ], id="sub-matricula-comparacion", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                # Egresados
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-graduation-cap me-2", style={"color": "var(--primary-color)"}),
                        "Egresados"
                    ])
                ], id="nav-egresados", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-briefcase me-2", style={"color": "var(--text-secondary)"}), 
                        "Transición Laboral"
                    ])
                ], id="sub-egresados-transicion", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-chart-pie me-2", style={"color": "var(--text-secondary)"}), 
                        "Empleabilidad"
                    ])
                ], id="sub-egresados-empleabilidad", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                # Titulación
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-certificate me-2", style={"color": "var(--primary-color)"}),
                        "Titulación"
                    ])
                ], id="nav-titulacion", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-percentage me-2", style={"color": "var(--text-secondary)"}), 
                        "Tasas de Titulación"
                    ])
                ], id="sub-titulacion-tasas", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-clock me-2", style={"color": "var(--text-secondary)"}), 
                        "Tiempo de Titulación"
                    ])
                ], id="sub-titulacion-tiempo", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                # Establecimientos
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-school me-2", style={"color": "var(--primary-color)"}),
                        "Establecimientos"
                    ])
                ], id="nav-establecimientos", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-map-marked-alt me-2", style={"color": "var(--text-secondary)"}), 
                        "Distribución Geográfica"
                    ])
                ], id="sub-establecimientos-geografia", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-building me-2", style={"color": "var(--text-secondary)"}), 
                        "Infraestructura"
                    ])
                ], id="sub-establecimientos-infraestructura", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                # Docentes
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-chalkboard-teacher me-2", style={"color": "var(--primary-color)"}),
                        "Docentes"
                    ])
                ], id="nav-docentes", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-user-tie me-2", style={"color": "var(--text-secondary)"}), 
                        "Perfil Profesional"
                    ])
                ], id="sub-docentes-perfil", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-book-open me-2", style={"color": "var(--text-secondary)"}), 
                        "Capacitación"
                    ])
                ], id="sub-docentes-capacitacion", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                # Mapas
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-map-marked-alt me-2", style={"color": "var(--primary-color)"}),
                        "Mapas"
                    ])
                ], id="nav-mapas", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                # Proyectos
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-tasks me-2", style={"color": "var(--primary-color)"}),
                        "Proyectos SEEMTP"
                    ])
                ], id="nav-proyectos", n_clicks=0, action=True, className="fw-bold mb-1"),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-coins me-2", style={"color": "var(--text-secondary)"}), 
                        "Financiamiento"
                    ])
                ], id="sub-proyectos-financiamiento", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"}),
                
                dbc.ListGroupItem([
                    html.Div([
                        html.I(className="fas fa-chart-bar me-2", style={"color": "var(--text-secondary)"}), 
                        "Impacto y Resultados"
                    ])
                ], id="sub-proyectos-impacto", n_clicks=0, action=True, 
                   className="ps-4 small sub-nav", style={"display": "none"})
                
            ], flush=True)
        ], className="p-0")
    ], className="mb-3 border-accent-custom")


def create_sidebar_layout():
    """Crea el layout del sidebar izquierdo completo"""
    return html.Div([
        # Navegación principal
        create_sidebar_navigation(),
        
        # Filtros avanzados
        create_advanced_filters(),
        
        # Información adicional
        dbc.Card([
            dbc.CardBody([
                html.H6([
                    html.I(className="fas fa-info-circle me-2", style={"color": "var(--primary-color)"}),
                    "Información"
                ], className="text-primary-custom mb-3"),
                html.P([
                    "Los datos mostrados son simulados para efectos de demostración. ",
                    "Basados en estadísticas reales del sistema EMTP chileno."
                ], className="small text-muted mb-2"),
                html.P([
                    html.I(className="fas fa-database me-2", style={"color": "var(--primary-color)"}),
                    "Total registros: ", html.Strong("36.411", className="text-primary-custom")
                ], className="small mb-1"),
                html.P([
                    html.I(className="fas fa-calendar me-2", style={"color": "var(--primary-color)"}),
                    "Período: ", html.Strong("2015-2024", className="text-primary-custom")
                ], className="small mb-0")
            ])
        ], className="border-accent-custom")
        
    ], id="sidebar-content")


def create_main_content_area():
    """Crea el área de contenido principal"""
    return html.Div([
        # Breadcrumb de navegación
        html.Div(id="breadcrumb-container", className="mb-3"),
        
        # Contenido dinámico
        html.Div(id="main-content-area", children=[
            # El contenido será manejado por los callbacks
        ])
        
    ], id="content-area")


def create_new_main_layout(hidden_sections=None):
    """Crea el layout principal con sidebar izquierdo
    
    Args:
        hidden_sections: Lista de secciones a ocultar según perfil de usuario
    """
    if hidden_sections is None:
        hidden_sections = []
    
    return html.Div([
        dbc.Container([
        # Store para estado de navegación
        dcc.Store(id='navigation-state', data={'active_main': 'nav-matricula', 'active_sub': 'sub-matricula-evolucion'}),
        
        # Store para filtros
        dcc.Store(id='filters-state', data={}),
        
        # Store para tema
        dcc.Store(id='theme-store', data={'theme': 'light'}),
        
        # Nota: session-store ya está definido en login_layout.py
        
        # Store para perfil de usuario
        dcc.Store(id='user-profile-store', storage_type='session'),

        
        # Layout principal con sidebar
        dbc.Row([
            # Sidebar izquierdo (filtrado según perfil)
            dbc.Col([
                create_sidebar_layout_filtered(hidden_sections)
            ], width=3, className="bg-light border-end border-accent-custom p-3", 
               style={"minHeight": "calc(100vh - 80px)", "overflowY": "auto"}),
            
            # Área de contenido principal
            dbc.Col([
                create_main_content_area()
            ], width=9, className="p-4")
            
        ], className="g-0", style={"minHeight": "calc(100vh - 80px)"})
        
        ], fluid=True, className="p-0")
    ], id="main-layout", **{"data-dummy": ""})