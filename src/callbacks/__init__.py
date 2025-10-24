"""
============================================================================
CALLBACKS PRINCIPALES
============================================================================
"""

from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from .matricula_callbacks import register_matricula_callbacks
from .docentes_callbacks import register_docentes_callbacks
from .mapa_callbacks import register_mapa_callbacks
from .theme_callbacks import register_theme_callbacks, register_tab_callbacks


def register_callbacks(app):
    """Registra todos los callbacks de la aplicación"""
    
    # Registrar callbacks de tema y pestañas
    register_theme_callbacks(app)
    register_tab_callbacks(app)
    
    # Registrar callbacks de módulos existentes
    register_matricula_callbacks(app)
    register_docentes_callbacks(app)
    register_mapa_callbacks(app)
