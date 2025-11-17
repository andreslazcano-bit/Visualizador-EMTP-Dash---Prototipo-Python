"""
============================================================================
CALLBACKS PARA MANEJO DE TEMA (MODO OSCURO/CLARO)
============================================================================
"""

from dash import Input, Output, State
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