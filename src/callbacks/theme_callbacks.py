"""
============================================================================
CALLBACKS PARA MANEJO DE TEMA (MODO OSCURO/CLARO)
============================================================================
"""

from dash import Input, Output, State, clientside_callback, ClientsideFunction
from dash.exceptions import PreventUpdate


def register_theme_callbacks(app):
    """Registra los callbacks para el manejo del tema"""
    
    # Callback para cambiar el tema
    @app.callback(
        [Output('theme-store', 'data'),
         Output('theme-icon', 'className')],
        [Input('theme-toggle', 'n_clicks')],
        [State('theme-store', 'data')],
        prevent_initial_call=True
    )
    def toggle_theme(n_clicks, theme_data):
        """Alterna entre modo claro y oscuro"""
        if not n_clicks:
            raise PreventUpdate
        
        if not theme_data:
            theme_data = {'theme': 'light'}
        
        current_theme = theme_data.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        
        # Cambiar el ícono según el tema
        icon_class = 'fas fa-sun' if new_theme == 'dark' else 'fas fa-moon'
        
        return {'theme': new_theme}, icon_class
    
    # Callback clientside para aplicar el tema al documento
    app.clientside_callback(
        """
        function(theme_data) {
            if (!theme_data || !theme_data.theme) {
                return window.dash_clientside.no_update;
            }
            
            const body = document.body;
            const mainLayout = document.getElementById('main-layout');
            const theme = theme_data.theme;
            
            // Aplicar tema al body y al layout principal
            if (theme === 'dark') {
                body.setAttribute('data-theme', 'dark');
                if (mainLayout) {
                    mainLayout.setAttribute('data-theme', 'dark');
                }
            } else {
                body.setAttribute('data-theme', 'light');
                if (mainLayout) {
                    mainLayout.setAttribute('data-theme', 'light');
                }
            }
            
            return window.dash_clientside.no_update;
        }
        """,
        Output('main-layout', 'data-dummy'),
        Input('theme-store', 'data'),
        prevent_initial_call=False
    )


def register_tab_callbacks(app):
    """Registra los callbacks para el manejo de pestañas"""
    
    @app.callback(
        Output("tab-content", "children"),
        [Input("main-tabs", "active_tab")]
    )
    def render_main_tab_content(active_tab):
        """Renderiza el contenido según la tab principal activa"""
        
        if active_tab == "tab-matricula":
            from src.layouts.main_layout import create_sub_tabs
            return create_matricula_content()
            
        elif active_tab == "tab-egresados":
            return create_egresados_content()
            
        elif active_tab == "tab-titulacion":
            return create_titulacion_content()
            
        elif active_tab == "tab-establecimientos":
            return create_establecimientos_content()
            
        elif active_tab == "tab-docentes":
            return create_docentes_content()
            
        elif active_tab == "tab-proyectos":
            return create_proyectos_content()
            
        else:
            return create_matricula_content()


def create_matricula_content():
    """Crea el contenido de la pestaña Matrícula"""
    from dash import html
    import dash_bootstrap_components as dbc
    from src.layouts.main_layout import create_sub_tabs
    from src.layouts.demo_content import create_matricula_subtab_content
    
    return html.Div([
        create_sub_tabs("matricula"),
        html.Hr(),
        html.Div(id="matricula-subtab-content"),
    ])


def create_egresados_content():
    """Crea el contenido de la pestaña Egresados"""
    from dash import html
    import dash_bootstrap_components as dbc
    from src.layouts.main_layout import create_sub_tabs
    
    return html.Div([
        create_sub_tabs("egresados"),
        html.Hr(),
        html.Div(id="egresados-subtab-content"),
    ])


def create_titulacion_content():
    """Crea el contenido de la pestaña Titulación"""
    from dash import html
    import dash_bootstrap_components as dbc
    from src.layouts.main_layout import create_sub_tabs
    
    return html.Div([
        create_sub_tabs("titulacion"),
        html.Hr(),
        html.Div(id="titulacion-subtab-content"),
    ])


def create_establecimientos_content():
    """Crea el contenido de la pestaña Establecimientos"""
    from dash import html
    import dash_bootstrap_components as dbc
    from src.layouts.main_layout import create_sub_tabs
    
    return html.Div([
        create_sub_tabs("establecimientos"),
        html.Hr(),
        html.Div(id="establecimientos-subtab-content"),
    ])


def create_docentes_content():
    """Crea el contenido de la pestaña Docentes"""
    from dash import html
    import dash_bootstrap_components as dbc
    from src.layouts.main_layout import create_sub_tabs
    
    return html.Div([
        create_sub_tabs("docentes"),
        html.Hr(),
        html.Div(id="docentes-subtab-content"),
    ])


def create_proyectos_content():
    """Crea el contenido de la pestaña Proyectos"""
    from dash import html
    import dash_bootstrap_components as dbc
    from src.layouts.main_layout import create_sub_tabs
    
    return html.Div([
        create_sub_tabs("proyectos"),
        html.Hr(),
        html.Div(id="proyectos-subtab-content"),
    ])


    # Callbacks para sub-pestañas
    @app.callback(
        Output("matricula-subtab-content", "children"),
        [Input("sub-tabs-matricula", "active_tab")]
    )
    def render_matricula_subtab(active_subtab):
        """Renderiza contenido de sub-pestañas de matrícula"""
        from src.layouts.demo_content import create_matricula_subtab_content
        if not active_subtab:
            return create_matricula_subtab_content("evolucion")
        
        subtab = active_subtab.replace("sub-matricula-", "")
        return create_matricula_subtab_content(subtab)

    @app.callback(
        Output("egresados-subtab-content", "children"),
        [Input("sub-tabs-egresados", "active_tab")]
    )
    def render_egresados_subtab(active_subtab):
        """Renderiza contenido de sub-pestañas de egresados"""
        from src.layouts.demo_content import create_egresados_subtab_content
        if not active_subtab:
            return create_egresados_subtab_content("transicion")
        
        subtab = active_subtab.replace("sub-egresados-", "")
        return create_egresados_subtab_content(subtab)

    @app.callback(
        Output("titulacion-subtab-content", "children"),
        [Input("sub-tabs-titulacion", "active_tab")]
    )
    def render_titulacion_subtab(active_subtab):
        """Renderiza contenido de sub-pestañas de titulación"""
        from src.layouts.demo_content import create_titulacion_subtab_content
        if not active_subtab:
            return create_titulacion_subtab_content("evolucion")
        
        subtab = active_subtab.replace("sub-titulacion-", "")
        return create_titulacion_subtab_content(subtab)

    @app.callback(
        Output("establecimientos-subtab-content", "children"),
        [Input("sub-tabs-establecimientos", "active_tab")]
    )
    def render_establecimientos_subtab(active_subtab):
        """Renderiza contenido de sub-pestañas de establecimientos"""
        from src.layouts.demo_content import create_establecimientos_subtab_content
        if not active_subtab:
            return create_establecimientos_subtab_content("geografia")
        
        subtab = active_subtab.replace("sub-establecimientos-", "")
        return create_establecimientos_subtab_content(subtab)

    @app.callback(
        Output("docentes-subtab-content", "children"),
        [Input("sub-tabs-docentes", "active_tab")]
    )
    def render_docentes_subtab(active_subtab):
        """Renderiza contenido de sub-pestañas de docentes"""
        from src.layouts.demo_content import create_docentes_subtab_content
        if not active_subtab:
            return create_docentes_subtab_content("distribucion")
        
        subtab = active_subtab.replace("sub-docentes-", "")
        return create_docentes_subtab_content(subtab)

    @app.callback(
        Output("proyectos-subtab-content", "children"),
        [Input("sub-tabs-proyectos", "active_tab")]
    )
    def render_proyectos_subtab(active_subtab):
        """Renderiza contenido de sub-pestañas de proyectos"""
        from src.layouts.demo_content import create_proyectos_subtab_content
        if not active_subtab:
            return create_proyectos_subtab_content("recursos")
        
        subtab = active_subtab.replace("sub-proyectos-", "")
        return create_proyectos_subtab_content(subtab)