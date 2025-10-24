"""
============================================================================
CALLBACKS PARA LAYOUT CON SIDEBAR Y DATOS REALES
============================================================================
"""

from dash import Input, Output, State, callback_context, html
import dash_bootstrap_components as dbc
from src.layouts.real_data_content import create_real_kpi_cards, create_real_chart, create_real_table
from src.utils.helpers import format_chilean


def create_breadcrumb(items):
    """Helper para crear breadcrumbs"""
    return dbc.Breadcrumb(items=items, className="mb-3")


def create_export_buttons(section_name, subtab=''):
    """
    Crea botones de exportación para PDF y CSV
    
    Args:
        section_name: Nombre de la sección (matricula, egresados, etc.)
        subtab: Sub-pestaña actual (opcional)
    """
    button_id_base = f"export-{section_name}"
    if subtab:
        button_id_base += f"-{subtab}"
    
    return html.Div([
        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col([
                html.H5([
                    html.I(className="fas fa-download me-2", style={"color": "var(--primary-color)"}),
                    "Exportar Datos"
                ], className="mb-3 text-secondary-custom")
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Button([
                    html.I(className="fas fa-file-pdf me-2"),
                    "Descargar PDF"
                ], 
                id=f"{button_id_base}-pdf",
                color="danger",
                outline=True,
                size="md",
                className="w-100",
                style={
                    "borderRadius": "8px",
                    "fontWeight": "500",
                    "transition": "all 0.3s ease"
                })
            ], md=3, sm=6, className="mb-2"),
            dbc.Col([
                dbc.Button([
                    html.I(className="fas fa-file-csv me-2"),
                    "Descargar CSV"
                ], 
                id=f"{button_id_base}-csv",
                color="success",
                outline=True,
                size="md",
                className="w-100",
                style={
                    "borderRadius": "8px",
                    "fontWeight": "500",
                    "transition": "all 0.3s ease"
                })
            ], md=3, sm=6, className="mb-2"),
            dbc.Col([
                dbc.Button([
                    html.I(className="fas fa-file-excel me-2"),
                    "Descargar Excel"
                ], 
                id=f"{button_id_base}-excel",
                color="primary",
                outline=True,
                size="md",
                className="w-100",
                style={
                    "borderRadius": "8px",
                    "fontWeight": "500",
                    "transition": "all 0.3s ease"
                })
            ], md=3, sm=6, className="mb-2"),
            dbc.Col([
                html.Div([
                    html.Small("Los reportes incluyen datos filtrados actualmente", 
                              className="text-muted fst-italic")
                ], className="d-flex align-items-center justify-content-center h-100")
            ], md=3, sm=12)
        ]),
    ], className="export-section mt-4 p-3 bg-light rounded")


def register_sidebar_callbacks(app):
    """Registra todos los callbacks para el layout con sidebar"""
    
    # Callbacks para mostrar/ocultar sub-pestañas con toggle
    @app.callback(
        [Output('sub-matricula-evolucion', 'style'),
         Output('sub-matricula-demografia', 'style'),
         Output('sub-matricula-retencion', 'style'),
         Output('sub-matricula-comparacion', 'style')],
        [Input('nav-matricula', 'n_clicks')],
        [State('sub-matricula-evolucion', 'style')],
        prevent_initial_call=True
    )
    def toggle_matricula_subnav(n_clicks, current_style):
        """Muestra/oculta las sub-pestañas de matrícula con toggle"""
        if n_clicks and n_clicks > 0:
            # Si están ocultas o es la primera vez, mostrar
            if not current_style or current_style.get("display") == "none":
                return [{"display": "block"}] * 4
            else:
                # Si están visibles, ocultar
                return [{"display": "none"}] * 4
        return [{"display": "none"}] * 4
    
    @app.callback(
        [Output('sub-egresados-transicion', 'style'),
         Output('sub-egresados-empleabilidad', 'style')],
        [Input('nav-egresados', 'n_clicks')],
        [State('sub-egresados-transicion', 'style')],
        prevent_initial_call=True
    )
    def toggle_egresados_subnav(n_clicks, current_style):
        """Muestra/oculta las sub-pestañas de egresados con toggle"""
        if n_clicks and n_clicks > 0:
            if not current_style or current_style.get("display") == "none":
                return [{"display": "block"}] * 2
            else:
                return [{"display": "none"}] * 2
        return [{"display": "none"}] * 2
    
    @app.callback(
        [Output('sub-titulacion-tasas', 'style'),
         Output('sub-titulacion-tiempo', 'style')],
        [Input('nav-titulacion', 'n_clicks')],
        [State('sub-titulacion-tasas', 'style')],
        prevent_initial_call=True
    )
    def toggle_titulacion_subnav(n_clicks, current_style):
        """Muestra/oculta las sub-pestañas de titulación con toggle"""
        if n_clicks and n_clicks > 0:
            if not current_style or current_style.get("display") == "none":
                return [{"display": "block"}] * 2
            else:
                return [{"display": "none"}] * 2
        return [{"display": "none"}] * 2
    
    @app.callback(
        [Output('sub-establecimientos-geografia', 'style'),
         Output('sub-establecimientos-infraestructura', 'style')],
        [Input('nav-establecimientos', 'n_clicks')],
        [State('sub-establecimientos-geografia', 'style')],
        prevent_initial_call=True
    )
    def toggle_establecimientos_subnav(n_clicks, current_style):
        """Muestra/oculta las sub-pestañas de establecimientos con toggle"""
        if n_clicks and n_clicks > 0:
            if not current_style or current_style.get("display") == "none":
                return [{"display": "block"}] * 2
            else:
                return [{"display": "none"}] * 2
        return [{"display": "none"}] * 2
    
    @app.callback(
        [Output('sub-docentes-perfil', 'style'),
         Output('sub-docentes-capacitacion', 'style')],
        [Input('nav-docentes', 'n_clicks')],
        [State('sub-docentes-perfil', 'style')],
        prevent_initial_call=True
    )
    def toggle_docentes_subnav(n_clicks, current_style):
        """Muestra/oculta las sub-pestañas de docentes con toggle"""
        if n_clicks and n_clicks > 0:
            if not current_style or current_style.get("display") == "none":
                return [{"display": "block"}] * 2
            else:
                return [{"display": "none"}] * 2
        return [{"display": "none"}] * 2
    
    @app.callback(
        [Output('sub-proyectos-financiamiento', 'style'),
         Output('sub-proyectos-impacto', 'style')],
        [Input('nav-proyectos', 'n_clicks')],
        [State('sub-proyectos-financiamiento', 'style')],
        prevent_initial_call=True
    )
    def toggle_proyectos_subnav(n_clicks, current_style):
        """Muestra/oculta las sub-pestañas de proyectos con toggle"""
        if n_clicks and n_clicks > 0:
            if not current_style or current_style.get("display") == "none":
                return [{"display": "block"}] * 2
            else:
                return [{"display": "none"}] * 2
        return [{"display": "none"}] * 2
    
    # Callback para navegación principal
    @app.callback(
        [Output('navigation-state', 'data'),
         Output('main-content-area', 'children'),
         Output('breadcrumb-container', 'children')],
        [Input('nav-inicio', 'n_clicks'),
         Input('nav-matricula', 'n_clicks'),
         Input('nav-egresados', 'n_clicks'),
         Input('nav-titulacion', 'n_clicks'),
         Input('nav-establecimientos', 'n_clicks'),
         Input('nav-docentes', 'n_clicks'),
         # Sub-pestañas de Matrícula
         Input('sub-matricula-evolucion', 'n_clicks'),
         Input('sub-matricula-demografia', 'n_clicks'),
         Input('sub-matricula-retencion', 'n_clicks'),
         Input('sub-matricula-comparacion', 'n_clicks'),
         # Sub-pestañas de Egresados
         Input('sub-egresados-transicion', 'n_clicks'),
         Input('sub-egresados-empleabilidad', 'n_clicks'),
         # Sub-pestañas de Titulación
         Input('sub-titulacion-tasas', 'n_clicks'),
         Input('sub-titulacion-tiempo', 'n_clicks'),
         # Sub-pestañas de Establecimientos
         Input('sub-establecimientos-geografia', 'n_clicks'),
         Input('sub-establecimientos-infraestructura', 'n_clicks'),
         # Sub-pestañas de Docentes
         Input('sub-docentes-perfil', 'n_clicks'),
         Input('sub-docentes-capacitacion', 'n_clicks')],
        [State('navigation-state', 'data'),
         State('filters-state', 'data')]
    )
    def handle_navigation(nav_inicio, nav_mat, nav_egr, nav_tit, nav_est, nav_doc,
                         sub_mat_evo, sub_mat_dem, sub_mat_ret, sub_mat_comp,
                         sub_egr_trans, sub_egr_emp,
                         sub_tit_tasas, sub_tit_tiempo,
                         sub_est_geo, sub_est_infra,
                         sub_doc_perfil, sub_doc_cap,
                         nav_state, filters):
        """Maneja la navegación entre secciones"""
        
        ctx = callback_context
        if not ctx.triggered:
            # Estado inicial - mostrar inicio
            content = create_inicio_content()
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "active": True}
            ])
            return {'active_main': 'nav-inicio', 'active_sub': None}, content, breadcrumb
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Navegación principal
        if button_id == 'nav-inicio':
            content = create_inicio_content()
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "active": True}
            ])
            return {'active_main': 'nav-inicio', 'active_sub': None}, content, breadcrumb
        
        elif button_id == 'nav-matricula':
            content = create_matricula_content('evolucion', filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Matrícula", "active": True}
            ])
            return {'active_main': 'nav-matricula', 'active_sub': 'evolucion'}, content, breadcrumb
        
        elif button_id == 'nav-egresados':
            content = create_egresados_content('transicion', filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Egresados", "active": True}
            ])
            return {'active_main': 'nav-egresados', 'active_sub': 'transicion'}, content, breadcrumb
        
        elif button_id == 'nav-titulacion':
            content = create_titulacion_content('evolucion', filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Titulación", "active": True}
            ])
            return {'active_main': 'nav-titulacion', 'active_sub': 'evolucion'}, content, breadcrumb
        
        elif button_id == 'nav-establecimientos':
            content = create_establecimientos_content('geografia', filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Establecimientos", "active": True}
            ])
            return {'active_main': 'nav-establecimientos', 'active_sub': 'geografia'}, content, breadcrumb
        
        elif button_id == 'nav-docentes':
            content = create_docentes_content('distribucion', filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Docentes", "active": True}
            ])
            return {'active_main': 'nav-docentes', 'active_sub': 'distribucion'}, content, breadcrumb
        
        # Sub-navegación para matrícula
        elif button_id.startswith('sub-matricula-'):
            subtab = button_id.replace('sub-matricula-', '')
            content = create_matricula_content(subtab, filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Matrícula", "href": "#"},
                {"label": subtab.title(), "active": True}
            ])
            return {'active_main': 'nav-matricula', 'active_sub': subtab}, content, breadcrumb
        
        # Sub-navegación para egresados
        elif button_id.startswith('sub-egresados-'):
            subtab = button_id.replace('sub-egresados-', '')
            content = create_egresados_content(subtab, filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Egresados", "href": "#"},
                {"label": subtab.title(), "active": True}
            ])
            return {'active_main': 'nav-egresados', 'active_sub': subtab}, content, breadcrumb
        
        # Sub-navegación para titulación
        elif button_id.startswith('sub-titulacion-'):
            subtab = button_id.replace('sub-titulacion-', '')
            content = create_titulacion_content(subtab, filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Titulación", "href": "#"},
                {"label": subtab.title(), "active": True}
            ])
            return {'active_main': 'nav-titulacion', 'active_sub': subtab}, content, breadcrumb
        
        # Sub-navegación para establecimientos
        elif button_id.startswith('sub-establecimientos-'):
            subtab = button_id.replace('sub-establecimientos-', '')
            content = create_establecimientos_content(subtab, filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Establecimientos", "href": "#"},
                {"label": subtab.title(), "active": True}
            ])
            return {'active_main': 'nav-establecimientos', 'active_sub': subtab}, content, breadcrumb
        
        # Sub-navegación para docentes
        elif button_id.startswith('sub-docentes-'):
            subtab = button_id.replace('sub-docentes-', '')
            content = create_docentes_content(subtab, filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Docentes", "href": "#"},
                {"label": subtab.title(), "active": True}
            ])
            return {'active_main': 'nav-docentes', 'active_sub': subtab}, content, breadcrumb
        
        # Estado por defecto - mostrar inicio
        content = create_inicio_content()
        breadcrumb = create_breadcrumb([
            {"label": "Inicio", "active": True}
        ])
        return {'active_main': 'nav-inicio', 'active_sub': None}, content, breadcrumb
    
    # Callback para aplicar filtros
    @app.callback(
        Output('filters-state', 'data'),
        [Input('apply-filters-btn', 'n_clicks'),
         Input('clear-filters-btn', 'n_clicks')],
        [State('filter-years', 'value'),
         State('filter-region', 'value'),
         State('filter-especialidad', 'value'),
         State('filter-dependencia', 'value'),
         State('filter-genero', 'value'),
         State('filter-zona', 'value')]
    )
    def handle_filters(apply_clicks, clear_clicks, years, region, especialidad, 
                      dependencia, genero, zona):
        """Maneja los filtros del sistema"""
        
        ctx = callback_context
        if not ctx.triggered:
            return {}
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'clear-filters-btn':
            return {}  # Limpiar filtros
        
        elif button_id == 'apply-filters-btn':
            return {
                'years': years,
                'region': region,
                'especialidad': especialidad,
                'dependencia': dependencia,
                'genero': genero,
                'zona': zona
            }
        
        return {}


    # Callback específico para proyectos (solo en modo Admin)
    @app.callback(
        [Output('navigation-state', 'data', allow_duplicate=True),
         Output('main-content-area', 'children', allow_duplicate=True),
         Output('breadcrumb-container', 'children', allow_duplicate=True)],
        [Input('nav-proyectos', 'n_clicks'),
         Input('sub-proyectos-financiamiento', 'n_clicks'),
         Input('sub-proyectos-impacto', 'n_clicks')],
        [State('navigation-state', 'data'),
         State('filters-state', 'data')],
        prevent_initial_call=True
    )
    def handle_proyectos_navigation(nav_proy, sub_proy_fin, sub_proy_imp, nav_state, filters):
        """Maneja la navegación de proyectos (solo modo Admin)"""
        from dash.exceptions import PreventUpdate
        
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Navegación principal a proyectos
        if button_id == 'nav-proyectos':
            content = create_proyectos_content('recursos', filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Proyectos SEEMTP", "active": True}
            ])
            return {'active_main': 'nav-proyectos', 'active_sub': 'recursos'}, content, breadcrumb
        
        # Sub-navegación para proyectos
        elif button_id.startswith('sub-proyectos-'):
            subtab = button_id.replace('sub-proyectos-', '')
            content = create_proyectos_content(subtab, filters)
            breadcrumb = create_breadcrumb([
                {"label": "Inicio", "href": "#"},
                {"label": "Proyectos SEEMTP", "href": "#"},
                {"label": subtab.title(), "active": True}
            ])
            return {'active_main': 'nav-proyectos', 'active_sub': subtab}, content, breadcrumb
        
        raise PreventUpdate


def create_inicio_content():
    """Crea el contenido de la página de inicio"""
    return html.Div([
        # Header principal con estadísticas generales
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H1([
                            html.I(className="fas fa-chart-area me-3", style={"color": "var(--primary-color)"}),
                            "Visualizador EMTP Chile"
                        ], className="text-center mb-4"),
                        
                        html.P([
                            "Sistema integral de análisis y visualización de datos del ",
                            html.Strong("Sistema de Educación Media Técnico-Profesional "), 
                            "de Chile. Esta plataforma proporciona insights profundos sobre la evolución, ",
                            "distribución y tendencias de la educación técnica en el país."
                        ], className="text-center lead mb-4"),
                        
                        html.Hr(),
                        
                        # Estadísticas destacadas - Diseño institucional
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H2(format_chilean(36411), 
                                           style={"color": "var(--primary-color)", "fontWeight": "var(--font-semibold)"}, 
                                           className="display-6 mb-0"),
                                    html.P("Registros de datos", 
                                          style={"color": "var(--text-muted)", "fontSize": "var(--text-sm)"})
                                ], className="text-center")
                            ], md=3),
                            dbc.Col([
                                html.Div([
                                    html.H2("10", 
                                           style={"color": "var(--primary-color)", "fontWeight": "var(--font-semibold)"}, 
                                           className="display-6 mb-0"),
                                    html.P("Años de cobertura", 
                                          style={"color": "var(--text-muted)", "fontSize": "var(--text-sm)"})
                                ], className="text-center")
                            ], md=3),
                            dbc.Col([
                                html.Div([
                                    html.H2("16", 
                                           style={"color": "var(--primary-color)", "fontWeight": "var(--font-semibold)"}, 
                                           className="display-6 mb-0"),
                                    html.P("Regiones incluidas", 
                                          style={"color": "var(--text-muted)", "fontSize": "var(--text-sm)"})
                                ], className="text-center")
                            ], md=3),
                            dbc.Col([
                                html.Div([
                                    html.H2("17", 
                                           style={"color": "var(--primary-color)", "fontWeight": "var(--font-semibold)"}, 
                                           className="display-6 mb-0"),
                                    html.P("Especialidades técnicas", 
                                          style={"color": "var(--text-muted)", "fontSize": "var(--text-sm)"})
                                ], className="text-center")
                            ], md=3)
                        ], className="mb-4")
                    ])
                ], className="shadow-sm mb-4")
            ])
        ]),
        
        # Secciones de navegación
        html.H3([
            html.I(className="fas fa-compass me-2", style={"color": "var(--primary-color)"}),
            "Explorar Secciones"
        ], className="mb-4"),
        
        dbc.Row([
            # Matrícula
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fas fa-user-graduate me-2", style={"color": "var(--primary-color)"}),
                            "Matrícula"
                        ]),
                        html.P("Análisis de evolución, demografía, retención y comparación de matrícula EMTP"),
                        html.Ul([
                            html.Li("Evolución Anual 2015-2024"),
                            html.Li("Distribución Demográfica"),
                            html.Li("Análisis de Retención"),
                            html.Li("Comparación Regional")
                        ])
                    ])
                ], className="h-100 border-start border-primary border-3")
            ], md=4, className="mb-3"),
            
            # Egresados
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fas fa-graduation-cap me-2", style={"color": "var(--green)"}),
                            "Egresados"
                        ]),
                        html.P("Seguimiento de egresados y su transición al mundo laboral"),
                        html.Ul([
                            html.Li("Transición Laboral"),
                            html.Li("Empleabilidad por Especialidad"),
                            html.Li("Inserción Profesional"),
                            html.Li("Seguimiento de Trayectorias")
                        ])
                    ])
                ], className="h-100 border-start border-success border-3")
            ], md=4, className="mb-3"),
            
            # Titulación
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fas fa-certificate me-2", style={"color": "var(--orange)"}),
                            "Titulación"
                        ]),
                        html.P("Análisis de procesos y tasas de titulación técnica"),
                        html.Ul([
                            html.Li("Tasas de Titulación"),
                            html.Li("Tiempo de Titulación"),
                            html.Li("Certificaciones por Especialidad"),
                            html.Li("Eficiencia del Sistema")
                        ])
                    ])
                ], className="h-100 border-start border-warning border-3")
            ], md=4, className="mb-3")
        ]),
        
        dbc.Row([
            # Establecimientos
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fas fa-school me-2", style={"color": "var(--secondary-color)"}),
                            "Establecimientos"
                        ]),
                        html.P("Análisis de infraestructura y distribución de establecimientos"),
                        html.Ul([
                            html.Li("Distribución Geográfica"),
                            html.Li("Infraestructura Educativa"),
                            html.Li("Capacidad Instalada"),
                            html.Li("Cobertura Regional")
                        ])
                    ])
                ], className="h-100 border-start border-danger border-3")
            ], md=4, className="mb-3"),
            
            # Docentes
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fas fa-chalkboard-teacher me-2", style={"color": "var(--purple)"}),
                            "Docentes"
                        ]),
                        html.P("Perfil profesional y capacitación del cuerpo docente"),
                        html.Ul([
                            html.Li("Perfil Profesional"),
                            html.Li("Programas de Capacitación"),
                            html.Li("Distribución por Especialidad"),
                            html.Li("Desarrollo Profesional")
                        ])
                    ])
                ], className="h-100 border-start border-secondary border-3")
            ], md=4, className="mb-3"),
            
            # Proyectos SEEMTP
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4([
                            html.I(className="fas fa-tasks me-2", style={"color": "var(--orange-light)"}),
                            "Proyectos SEEMTP"
                        ]),
                        html.P("Sistema de fortalecimiento de la educación técnica"),
                        html.Ul([
                            html.Li("Financiamiento de Proyectos"),
                            html.Li("Impacto y Resultados"),
                            html.Li("Mejoramiento Continuo"),
                            html.Li("Innovación Educativa")
                        ])
                    ])
                ], className="h-100 border-start border-info border-3")
            ], md=4, className="mb-3")
        ]),
        
        # Información adicional
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4([
                        html.I(className="fas fa-info-circle me-2"),
                        "Información del Sistema"
                    ], className="alert-heading"),
                    html.P([
                        "Los datos presentados en este visualizador corresponden a información simulada ",
                        "basada en estadísticas reales del sistema EMTP chileno. El período de análisis ",
                        "abarca desde 2015 hasta 2024, proporcionando una década completa de insights."
                    ]),
                    html.Hr(),
                    html.P([
                        html.I(className="fas fa-lightbulb me-2", style={"color": "var(--orange)"}),
                        html.Strong("Consejo:"), " Utiliza los filtros laterales para personalizar ",
                        "los análisis según región, especialidad, dependencia y otros criterios."
                    ], className="mb-0")
                ], color="info", className="border-info")
            ])
        ])
    ])


def create_matricula_content(subtab='evolucion', filters=None):
    """Crea contenido para la sección de matrícula"""
    
    subtab_config = {
        'evolucion': {
            'title': html.Span([html.I(className="fas fa-chart-area me-2"), "Evolución Anual de la Matrícula EMTP"]),
            'charts': [
                {'type': 'line', 'title': 'Evolución Histórica de Matrícula (2015-2024)'},
                {'type': 'bar', 'title': 'Matrícula por Especialidad (Top 10)'}
            ]
        },
        'demografia': {
            'title': html.Span([html.I(className="fas fa-user-friends me-2"), "Distribución Demográfica de Estudiantes"]),
            'charts': [
                {'type': 'pie', 'title': 'Distribución por Género'},
                {'type': 'bar', 'title': 'Matrícula por Dependencia'}
            ]
        },
        'retencion': {
            'title': html.Span([html.I(className="fas fa-user-check me-2"), "Análisis de Retención Estudiantil"]),
            'charts': [
                {'type': 'bar', 'title': 'Tasa de Retención por Especialidad'},
                {'type': 'line', 'title': 'Evolución de Retención por Año'}
            ]
        },
        'comparacion': {
            'title': '⚖️ Comparación con Sistema Educativo',
            'charts': [
                {'type': 'bar', 'title': 'EMTP vs HC por Región'},
                {'type': 'pie', 'title': 'Distribución Nacional del Sistema'}
            ]
        }
    }
    
    config = subtab_config.get(subtab, subtab_config['evolucion'])
    
    return html.Div([
        # Título de sección
        html.H2(config['title'], className="mb-4 text-primary-custom"),
        
        # KPIs
        create_real_kpi_cards('matricula', filters),
        
        html.Hr(className="my-4"),
        
        # Gráficos
        dbc.Row([
            dbc.Col([
                create_real_chart('matricula', config['charts'][0]['type'], 
                                config['charts'][0]['title'], filters)
            ], md=6),
            dbc.Col([
                create_real_chart('matricula', config['charts'][1]['type'], 
                                config['charts'][1]['title'], filters)
            ], md=6)
        ]),
        
        # Tabla de datos
        html.H4([
            html.I(className="fas fa-table me-2", style={"color": "var(--primary-color)"}),
            "Datos Detallados"
        ], className="mt-4 mb-3"),
        create_real_table('matricula', filters),
        
        # Botones de exportación
        create_export_buttons('matricula', subtab)
    ])


def create_egresados_content(subtab='transicion', filters=None):
    """Crea contenido para la sección de egresados"""
    
    return html.Div([
        html.H2([
            html.I(className="fas fa-graduation-cap me-2"),
            "Egresados EMTP en Educación Superior"
        ], className="mb-4 text-secondary-custom"),
        
        create_real_kpi_cards('egresados', filters),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                create_real_chart('egresados', 'line', 'Evolución Tasa de Transición', filters)
            ], md=6),
            dbc.Col([
                create_real_chart('egresados', 'bar', 'Transición por Especialidad', filters)
            ], md=6)
        ]),
        
        html.H4([
            html.I(className="fas fa-table me-2", style={"color": "var(--primary-color)"}),
            "Datos Detallados"
        ], className="mt-4 mb-3"),
        create_real_table('egresados', filters),
        
        # Botones de exportación
        create_export_buttons('egresados', subtab)
    ])


def create_titulacion_content(subtab='evolucion', filters=None):
    """Crea contenido para la sección de titulación"""
    
    return html.Div([
        html.H2([
            html.Span([
                html.I(className="fas fa-certificate me-2"),
                "Proceso de Titulación EMTP"
            ])
        ], className="mb-4 text-green"),
        
        create_real_kpi_cards('titulacion', filters),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                create_real_chart('titulacion', 'line', 'Evolución de Titulados por Año', filters)
            ], md=6),
            dbc.Col([
                create_real_chart('titulacion', 'bar', 'Tasa de Titulación por Especialidad', filters)
            ], md=6)
        ]),
        
        html.H4([
            html.I(className="fas fa-table me-2", style={"color": "var(--primary-color)"}),
            "Datos Detallados"
        ], className="mt-4 mb-3"),
        create_real_table('titulacion', filters),
        
        # Botones de exportación
        create_export_buttons('titulacion', subtab)
    ])


def create_establecimientos_content(subtab='geografia', filters=None):
    """Crea contenido para la sección de establecimientos"""
    
    return html.Div([
        html.H2([
            html.I(className="fas fa-school me-2"),
            "Establecimientos EMTP Nacional"
        ], className="mb-4 text-orange"),
        
        create_real_kpi_cards('establecimientos', filters),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                create_real_chart('establecimientos', 'bar', 'Establecimientos por Región', filters)
            ], md=6),
            dbc.Col([
                create_real_chart('establecimientos', 'pie', 'Distribución por Dependencia', filters)
            ], md=6)
        ]),
        
        html.H4([
            html.I(className="fas fa-table me-2", style={"color": "var(--primary-color)"}),
            "Datos Detallados"
        ], className="mt-4 mb-3"),
        create_real_table('establecimientos', filters),
        
        # Botones de exportación
        create_export_buttons('establecimientos', subtab)
    ])


def create_docentes_content(subtab='distribucion', filters=None):
    """Crea contenido para la sección de docentes"""
    
    return html.Div([
        html.H2([
            html.I(className="fas fa-chalkboard-teacher me-2"),
            "Docentes de Especialidad EMTP"
        ], className="mb-4 text-purple"),
        
        create_real_kpi_cards('docentes', filters),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                create_real_chart('docentes', 'bar', 'Docentes por Especialidad', filters)
            ], md=6),
            dbc.Col([
                create_real_chart('docentes', 'pie', 'Distribución por Género', filters)
            ], md=6)
        ]),
        
        html.H4([
            html.I(className="fas fa-table me-2", style={"color": "var(--primary-color)"}),
            "Datos Detallados"
        ], className="mt-4 mb-3"),
        create_real_table('docentes', filters),
        
        # Botones de exportación
        create_export_buttons('docentes', subtab)
    ])


def create_proyectos_content(subtab='recursos', filters=None):
    """Crea contenido para la sección de proyectos"""
    
    return html.Div([
        html.H2([
            html.I(className="fas fa-tasks me-3", style={"color": "var(--primary-color)"}),
            "Proyectos SEEMTP - Sistema de Educación EMTP"
        ], className="mb-4"),
        
        create_real_kpi_cards('proyectos', filters),
        
        html.Hr(className="my-4"),
        
        dbc.Row([
            dbc.Col([
                create_real_chart('proyectos', 'bar', 'Inversión por Región', filters)
            ], md=6),
            dbc.Col([
                create_real_chart('proyectos', 'pie', 'Distribución por Tipo de Proyecto', filters)
            ], md=6)
        ]),
        
        html.H4([
            html.I(className="fas fa-table me-2", style={"color": "var(--primary-color)"}),
            "Datos Detallados"
        ], className="mt-4 mb-3"),
        create_real_table('proyectos', filters),
        
        # Botones de exportación
        create_export_buttons('proyectos', subtab)
    ])