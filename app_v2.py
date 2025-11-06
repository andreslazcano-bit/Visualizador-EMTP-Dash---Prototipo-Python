"""
============================================================================
VISUALIZADOR EMTP V2 - Layout con Sidebar y Datos Reales
============================================================================
Aplicación web interactiva mejorada con navegación lateral y datos simulados
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from loguru import logger
import sys

# Configuración
from config.settings import settings
from src.layouts.sidebar_layout_clean import create_new_main_layout
from src.layouts.login_layout import create_login_layout
from src.callbacks.sidebar_callbacks import register_sidebar_callbacks
from src.callbacks.theme_callbacks import register_theme_callbacks
from src.callbacks.auth_callbacks import register_auth_callbacks

# Importar callbacks de mapas (usan decorador @callback)
import src.callbacks.mapas_callbacks  # noqa: F401

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
logger.add(
    settings.LOG_FILE,
    rotation="10 MB",
    retention=settings.LOG_BACKUP_COUNT,
    level=settings.LOG_LEVEL
)

# ============================================================================
# INICIALIZACIÓN DE LA APP
# ============================================================================
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    external_scripts=[
        '/assets/theme.js'
    ],
    suppress_callback_exceptions=True,
    title="Visualizador EMTP v2.0",
    update_title="Cargando datos...",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        },
        {
            "name": "description",
            "content": "Visualizador EMTP v2.0 - Dashboard con datos simulados del sistema técnico-profesional chileno"
        }
    ]
)

# Configuración del servidor
server = app.server

# ============================================================================
# LAYOUT PRINCIPAL CON AUTENTICACIÓN
# ============================================================================
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='session'),
    html.Div(id='app-content', children=[create_login_layout()])
])

# ============================================================================
# REGISTRO DE CALLBACKS
# ============================================================================
register_auth_callbacks(app)
register_sidebar_callbacks(app)
register_theme_callbacks(app)

# ============================================================================
# EJECUCIÓN
# ============================================================================
if __name__ == '__main__':
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v2.0")
    logger.info(f"📊 Entorno: {settings.ENVIRONMENT}")
    logger.info(f"🔧 Debug: {settings.DEBUG}")
    logger.info(f"🌐 Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"📁 Datos: Simulados con 36k+ registros")
    
    app.run_server(
        debug=False,  # Desactivado temporalmente para ngrok
        host=settings.HOST,
        port=settings.PORT + 1  # Puerto 8051 para no conflictos
    )