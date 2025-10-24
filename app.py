"""
============================================================================
VISUALIZADOR EMTP - Aplicación Dash Principal
============================================================================
Aplicación web interactiva para explorar y analizar datos de 
Enseñanza Media Técnico Profesional en Chile

Migrado desde R Shiny a Python Dash
Fecha de migración: Octubre 2025
============================================================================
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from loguru import logger
import sys

# Configuración de logging
from config.settings import settings
from src.layouts.main_layout import create_main_layout
from src.callbacks import register_callbacks

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
logger.remove()  # Remover handler por defecto
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
    ],
    external_scripts=[
        '/assets/theme.js'
    ],
    suppress_callback_exceptions=True,
    title="Visualizador EMTP",
    update_title="Cargando...",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        },
        {
            "name": "description",
            "content": "Visualizador de datos EMTP - Enseñanza Media Técnico Profesional en Chile"
        }
    ]
)

# Exponer el servidor para deployment
server = app.server

# ============================================================================
# LAYOUT PRINCIPAL
# ============================================================================
app.layout = create_main_layout()

# ============================================================================
# REGISTRO DE CALLBACKS
# ============================================================================
register_callbacks(app)

# ============================================================================
# EJECUCIÓN
# ============================================================================
if __name__ == '__main__':
    logger.info(f"🚀 Iniciando {settings.APP_NAME}")
    logger.info(f"📊 Entorno: {settings.ENVIRONMENT}")
    logger.info(f"🔧 Debug: {settings.DEBUG}")
    logger.info(f"🌐 Host: {settings.HOST}:{settings.PORT}")
    
    app.run_server(
        debug=settings.DEBUG,
        host=settings.HOST,
        port=settings.PORT
    )
