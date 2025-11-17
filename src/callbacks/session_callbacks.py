"""
============================================================================
CALLBACKS DE GESTIÓN DE SESIÓN CON TIMEOUT
============================================================================
Maneja el timeout automático de sesión y re-autenticación
"""

from dash import Input, Output, State, callback_context, html, no_update
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from config.settings import settings
from src.utils.user_management import user_manager
from src.utils.audit import audit_logger
from src.layouts.welcome_screen import create_welcome_layout
from loguru import logger


def register_session_callbacks(app):
    """Registra callbacks de gestión de sesión"""
    
    @app.callback(
        [Output('modal-session-timeout', 'is_open'),
         Output('modal-reauth', 'is_open'),
         Output('session-timeout-message', 'children'),
         Output('session-store', 'data', allow_duplicate=True)],
        [Input('session-check-interval', 'n_intervals')],
        [State('session-store', 'data')],
        prevent_initial_call=True
    )
    def check_session_timeout(n_intervals, session_data):
        """
        Verifica timeout de sesión cada minuto
        
        Comportamiento:
        - Usuario sin contraseña: Redirige suavemente después del timeout
        - Admin/Analista: Solicita re-autenticación
        """
        # Si no hay sesión activa, no hacer nada
        if not session_data or not session_data.get('authenticated'):
            return False, False, "", no_update
        
        user_info = session_data.get('user_info', {})
        username = user_info.get('username', '')
        profile = user_info.get('profile', 'usuario')
        
        # Obtener timestamp de última actividad
        last_activity_str = session_data.get('last_activity')
        
        if not last_activity_str:
            # Si no existe, agregar timestamp actual y continuar
            session_data['last_activity'] = datetime.utcnow().isoformat()
            return False, False, "", session_data
        
        # Calcular tiempo de inactividad
        last_activity = datetime.fromisoformat(last_activity_str)
        current_time = datetime.utcnow()
        inactive_minutes = (current_time - last_activity).total_seconds() / 60
        
        # Verificar si excede el timeout configurado
        if inactive_minutes > settings.SESSION_TIMEOUT_MINUTES:
            logger.info(f"Sesión expirada para {username} (inactividad: {inactive_minutes:.1f} min)")
            
            # Registrar en auditoría
            audit_logger.log_event(
                username=username,
                event_type='session_timeout',
                details={
                    'profile': profile,
                    'inactive_minutes': round(inactive_minutes, 1)
                }
            )
            
            # Comportamiento diferente según el perfil
            if profile == 'usuario':
                # Usuario sin contraseña: Mostrar mensaje amigable y redireccionar
                message = html.Div([
                    html.P("Tu sesión ha expirado por inactividad.", className="mb-2"),
                    html.P(
                        f"Por motivos de seguridad, las sesiones se cierran automáticamente "
                        f"después de {settings.SESSION_TIMEOUT_MINUTES} minutos sin actividad.",
                        className="text-muted small mb-0"
                    )
                ])
                # Limpiar sesión
                return True, False, message, None
            
            else:
                # Admin/Analista: Solicitar re-autenticación
                # Mantener datos de sesión para validar después
                return False, True, "", session_data
        
        # Sesión activa - no hacer nada
        return False, False, "", no_update
    
    @app.callback(
        [Output('app-content', 'children', allow_duplicate=True),
         Output('session-store', 'data', allow_duplicate=True),
         Output('modal-session-timeout', 'is_open', allow_duplicate=True)],
        [Input('btn-timeout-return', 'n_clicks')],
        prevent_initial_call=True
    )
    def return_from_timeout(n_clicks):
        """Volver a la pantalla de bienvenida desde timeout"""
        if n_clicks:
            return create_welcome_layout(), None, False
        return no_update, no_update, no_update
    
    @app.callback(
        [Output('app-content', 'children', allow_duplicate=True),
         Output('session-store', 'data', allow_duplicate=True),
         Output('modal-reauth', 'is_open', allow_duplicate=True),
         Output('reauth-message', 'children')],
        [Input('btn-reauth-confirm', 'n_clicks'),
         Input('btn-reauth-cancel', 'n_clicks')],
        [State('reauth-password-input', 'value'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def handle_reauth(confirm_clicks, cancel_clicks, password, session_data):
        """
        Maneja re-autenticación para admin/analista
        """
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Si cancela, volver a bienvenida
        if button_id == 'btn-reauth-cancel':
            if session_data:
                username = session_data.get('user_info', {}).get('username', 'unknown')
                logger.info(f"Usuario {username} canceló re-autenticación")
            return create_welcome_layout(), None, False, ""
        
        # Validar re-autenticación
        if button_id == 'btn-reauth-confirm':
            if not session_data or not password:
                return no_update, no_update, True, dbc.Alert(
                    "Por favor, ingresa tu contraseña",
                    color="warning",
                    dismissable=True
                )
            
            user_info = session_data.get('user_info', {})
            username = user_info.get('username', '')
            
            # Validar contraseña
            authenticated_user = user_manager.authenticate_user(username, password)
            
            if authenticated_user:
                # Contraseña correcta - renovar sesión
                session_data['last_activity'] = datetime.utcnow().isoformat()
                
                logger.info(f"Re-autenticación exitosa para {username}")
                audit_logger.log_event(
                    username=username,
                    event_type='reauth_success',
                    details={'profile': user_info.get('profile')}
                )
                
                # Mantener layout actual, renovar sesión, cerrar modal
                return no_update, session_data, False, ""
            
            else:
                # Contraseña incorrecta
                logger.warning(f"Re-autenticación fallida para {username}")
                audit_logger.log_event(
                    username=username,
                    event_type='reauth_failed',
                    details={'profile': user_info.get('profile')}
                )
                
                return no_update, no_update, True, dbc.Alert(
                    "Contraseña incorrecta. Intenta nuevamente.",
                    color="danger",
                    dismissable=True
                )
        
        return no_update, no_update, no_update, no_update
    
    @app.callback(
        Output('session-store', 'data', allow_duplicate=True),
        [Input('url', 'pathname'),
         Input('sidebar-tabs', 'value')],
        [State('session-store', 'data')],
        prevent_initial_call=True
    )
    def update_activity(*args):
        """
        Actualiza timestamp de última actividad en cualquier interacción
        
        Monitorea:
        - Cambios de URL
        - Cambios de pestaña
        """
        session_data = args[-1]  # Último argumento es el State
        
        # Solo actualizar si hay sesión activa
        if session_data and session_data.get('authenticated'):
            session_data['last_activity'] = datetime.utcnow().isoformat()
            return session_data
        
        return no_update
