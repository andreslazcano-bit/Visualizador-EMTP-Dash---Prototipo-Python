"""
============================================================================
CALLBACKS DE AUTENTICACIÓN Y SELECCIÓN DE MODO
============================================================================
"""

from dash import Input, Output, State, callback_context, html, dcc, no_update
import dash_bootstrap_components as dbc
from datetime import datetime
from src.utils.auth import AuthManager, USER_PROFILES, DEMO_USERS
from src.utils.user_management import user_manager
from src.utils.audit import audit_logger
from src.layouts.welcome_screen import create_welcome_layout
from src.layouts.login_layout import create_navbar_with_user
from src.layouts.sidebar_layout_clean import create_new_main_layout


def create_authenticated_layout(user_info):
    """Crea el layout para usuarios autenticados"""
    
    # Obtener secciones ocultas según el perfil
    hidden_sections = user_info.get('hidden_sections', [])
    
    return html.Div([
        # Navbar con información del usuario
        create_navbar_with_user(user_info),
        
        # Contenido principal con filtrado de secciones
        create_new_main_layout(hidden_sections=hidden_sections)
    ])


def register_auth_callbacks(app):
    """Registra todos los callbacks de autenticación"""
    
    # Callback de inicialización - muestra pantalla de bienvenida solo si no hay sesión
    @app.callback(
        [Output('app-content', 'children'),
         Output('session-store', 'data')],
        [Input('url', 'pathname')],
        [State('session-store', 'data')],
        prevent_initial_call=False
    )
    def initialize_app(pathname, session_data):
        """Inicializa la aplicación mostrando pantalla de bienvenida o mantiene sesión"""
        # Si ya hay sesión activa, mantenerla
        if session_data and session_data.get('authenticated'):
            user_info = session_data.get('user_info', {})
            return create_authenticated_layout(user_info), session_data
        
        # Si no hay sesión, mostrar pantalla de bienvenida
        return create_welcome_layout(), None
    
    # Callback para abrir modal de admin
    @app.callback(
        Output('modal-admin-login', 'is_open'),
        [Input('btn-modo-admin', 'n_clicks'),
         Input('btn-cancel-admin', 'n_clicks'),
         Input('btn-confirm-admin', 'n_clicks')],
        [State('modal-admin-login', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_admin_modal(open_clicks, cancel_clicks, confirm_clicks, is_open):
        """Abre/cierra el modal de login admin"""
        ctx = callback_context
        if not ctx.triggered:
            return is_open
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'btn-modo-admin':
            return True
        elif button_id in ['btn-cancel-admin', 'btn-confirm-admin']:
            return False
        
        return is_open
    
    # Callback para acceso modo usuario (directo)
    @app.callback(
        [Output('app-content', 'children', allow_duplicate=True),
         Output('session-store', 'data', allow_duplicate=True)],
        [Input('btn-modo-usuario', 'n_clicks')],
        prevent_initial_call=True
    )
    def access_user_mode(n_clicks):
        """Acceso directo al modo usuario"""
        if n_clicks:
            user_session = {
                'authenticated': True,
                'last_activity': datetime.utcnow().isoformat(),
                'user_info': {
                    'username': 'usuario',
                    'profile': 'usuario', 
                    'full_name': 'Modo Usuario',
                    'hidden_sections': ['proyectos', 'gestion-usuarios', 'auditoria', 'indicadores-mds']
                }
            }
            # Registrar acceso en auditoría
            audit_logger.log_login('usuario', success=True)
            
            return create_authenticated_layout(user_session['user_info']), user_session
        return no_update, no_update
    
    # Callback para acceso modo admin (con password)
    @app.callback(
        [Output('app-content', 'children', allow_duplicate=True),
         Output('session-store', 'data', allow_duplicate=True),
         Output('admin-login-message', 'children'),
         Output('modal-admin-login', 'is_open', allow_duplicate=True)],
        [Input('btn-confirm-admin', 'n_clicks')],
        [State('admin-password-input', 'value')],
        prevent_initial_call=True
    )
    def access_admin_mode(n_clicks, password):
        """Acceso al modo admin con validación de contraseña usando user_manager"""
        if n_clicks and password:
            # Usar user_manager para autenticar
            user_info = user_manager.authenticate_user('admin', password)
            
            if user_info:
                # Autenticación exitosa
                admin_session = {
                    'authenticated': True,
                    'last_activity': datetime.utcnow().isoformat(),
                    'user_info': user_info
                }
                return (
                    create_authenticated_layout(admin_session['user_info']), 
                    admin_session, 
                    "", 
                    False
                )
            else:
                # Contraseña incorrecta
                audit_logger.log_login('admin', success=False)
                return (
                    no_update,
                    no_update,
                    dbc.Alert("Contraseña incorrecta", color="danger", dismissable=True),
                    True
                )
        return no_update, no_update, no_update, no_update
    
    # Callback para volver a la pantalla de bienvenida
    @app.callback(
        [Output('app-content', 'children', allow_duplicate=True),
         Output('session-store', 'data', allow_duplicate=True)],
        [Input('logout-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def return_to_welcome(logout_clicks):
        """Vuelve a la pantalla de bienvenida"""
        if logout_clicks and logout_clicks > 0:
            return create_welcome_layout(), None
        return no_update, no_update


def check_permission(required_permission):
    """Decorador para verificar permisos"""
    def decorator(callback_func):
        def wrapper(*args, **kwargs):
            # Aquí se verificaría el permiso desde el store de sesión
            # Por simplicidad, se implementa básico
            return callback_func(*args, **kwargs)
        return wrapper
    return decorator