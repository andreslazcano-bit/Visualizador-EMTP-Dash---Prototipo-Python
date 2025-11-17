"""
============================================================================
GESTIÓN DE SESIONES CON TIMEOUT AUTOMÁTICO
============================================================================
Sistema de seguridad que maneja timeout de sesión y reautenticación
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from loguru import logger
import uuid


class SessionManager:
    """Gestiona sesiones de usuario con timeout automático"""
    
    # Configuración de timeouts (en minutos)
    SESSION_TIMEOUT_MINUTES = 30  # Timeout de inactividad
    MAX_SESSION_DURATION_HOURS = 8  # Duración máxima de sesión
    
    def __init__(self):
        """Inicializa el gestor de sesiones"""
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, username: str, profile: str, requires_password: bool = True) -> str:
        """
        Crea una nueva sesión para el usuario
        
        Args:
            username: Nombre de usuario
            profile: Perfil del usuario
            requires_password: Si el usuario requiere contraseña (admin, editor, viewer)
        
        Returns:
            session_id: ID único de la sesión
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        self._sessions[session_id] = {
            'username': username,
            'profile': profile,
            'requires_password': requires_password,
            'created_at': now,
            'last_activity': now,
            'expires_at': now + timedelta(hours=self.MAX_SESSION_DURATION_HOURS)
        }
        
        logger.info(f"Sesión creada para {username} (perfil: {profile}, session_id: {session_id})")
        return session_id
    
    def validate_session(self, session_id: Optional[str]) -> Dict[str, Any]:
        """
        Valida una sesión existente
        
        Args:
            session_id: ID de la sesión a validar
        
        Returns:
            dict: {
                'valid': bool,
                'expired': bool,
                'reason': str,
                'session_data': dict (si válida)
            }
        """
        if not session_id:
            return {
                'valid': False,
                'expired': False,
                'reason': 'no_session',
                'session_data': None
            }
        
        session = self._sessions.get(session_id)
        
        if not session:
            return {
                'valid': False,
                'expired': True,
                'reason': 'session_not_found',
                'session_data': None
            }
        
        now = datetime.utcnow()
        
        # Verificar si la sesión ha expirado por duración máxima
        if now > session['expires_at']:
            self.destroy_session(session_id)
            return {
                'valid': False,
                'expired': True,
                'reason': 'max_duration_exceeded',
                'session_data': None
            }
        
        # Verificar timeout de inactividad
        last_activity = session['last_activity']
        inactive_time = (now - last_activity).total_seconds() / 60  # minutos
        
        if inactive_time > self.SESSION_TIMEOUT_MINUTES:
            self.destroy_session(session_id)
            logger.info(f"Sesión expirada por inactividad: {session['username']} ({inactive_time:.1f} min)")
            return {
                'valid': False,
                'expired': True,
                'reason': 'inactivity_timeout',
                'inactive_minutes': int(inactive_time),
                'session_data': None
            }
        
        # Sesión válida - actualizar última actividad
        session['last_activity'] = now
        
        return {
            'valid': True,
            'expired': False,
            'reason': 'active',
            'session_data': {
                'username': session['username'],
                'profile': session['profile'],
                'requires_password': session['requires_password'],
                'created_at': session['created_at'].isoformat(),
                'remaining_minutes': self.SESSION_TIMEOUT_MINUTES - int(inactive_time)
            }
        }
    
    def update_activity(self, session_id: str) -> bool:
        """
        Actualiza la última actividad de la sesión
        
        Args:
            session_id: ID de la sesión
        
        Returns:
            bool: True si se actualizó correctamente
        """
        session = self._sessions.get(session_id)
        if session:
            session['last_activity'] = datetime.utcnow()
            return True
        return False
    
    def destroy_session(self, session_id: str) -> bool:
        """
        Destruye una sesión
        
        Args:
            session_id: ID de la sesión a destruir
        
        Returns:
            bool: True si se destruyó correctamente
        """
        if session_id in self._sessions:
            username = self._sessions[session_id]['username']
            del self._sessions[session_id]
            logger.info(f"Sesión destruida para {username}")
            return True
        return False
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de la sesión sin validar timeout
        
        Args:
            session_id: ID de la sesión
        
        Returns:
            dict: Información de la sesión o None
        """
        session = self._sessions.get(session_id)
        if not session:
            return None
        
        now = datetime.utcnow()
        last_activity = session['last_activity']
        inactive_time = (now - last_activity).total_seconds() / 60
        
        return {
            'username': session['username'],
            'profile': session['profile'],
            'requires_password': session['requires_password'],
            'created_at': session['created_at'].isoformat(),
            'last_activity': session['last_activity'].isoformat(),
            'inactive_minutes': int(inactive_time),
            'remaining_minutes': max(0, self.SESSION_TIMEOUT_MINUTES - int(inactive_time))
        }
    
    def cleanup_expired_sessions(self):
        """Limpia sesiones expiradas del sistema"""
        now = datetime.utcnow()
        expired_sessions = []
        
        for session_id, session in self._sessions.items():
            last_activity = session['last_activity']
            inactive_time = (now - last_activity).total_seconds() / 60
            
            # Marcar para eliminación si excede timeout o duración máxima
            if inactive_time > self.SESSION_TIMEOUT_MINUTES or now > session['expires_at']:
                expired_sessions.append(session_id)
        
        # Eliminar sesiones expiradas
        for session_id in expired_sessions:
            username = self._sessions[session_id]['username']
            del self._sessions[session_id]
            logger.info(f"Sesión limpiada (expirada): {username}")
        
        if expired_sessions:
            logger.info(f"Limpieza de sesiones: {len(expired_sessions)} sesiones eliminadas")
        
        return len(expired_sessions)


# Instancia global del gestor de sesiones
session_manager = SessionManager()
