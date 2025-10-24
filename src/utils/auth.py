"""
============================================================================
UTILIDADES DE AUTENTICACIÓN Y PERFILES DE USUARIO
============================================================================
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from loguru import logger
import hashlib
import secrets

from config.settings import settings


# Definición de perfiles y permisos
USER_PROFILES = {
    'usuario': {
        'name': 'Usuario',
        'description': 'Acceso básico a visualización de datos',
        'permissions': [
            'view_matricula',
            'view_egresados', 
            'view_titulacion',
            'view_establecimientos',
            'view_docentes'
        ],
        'hidden_sections': ['proyectos']
    },
    'analista': {
        'name': 'Analista',
        'description': 'Acceso completo a análisis y reportes',
        'permissions': [
            'view_matricula',
            'view_egresados',
            'view_titulacion', 
            'view_establecimientos',
            'view_docentes',
            'view_proyectos',
            'export_data'
        ],
        'hidden_sections': []
    },
    'admin': {
        'name': 'Administrador',
        'description': 'Acceso total al sistema y configuración',
        'permissions': [
            'view_matricula',
            'view_egresados',
            'view_titulacion',
            'view_establecimientos', 
            'view_docentes',
            'view_proyectos',
            'export_data',
            'manage_users',
            'system_config'
        ],
        'hidden_sections': []
    }
}

# Usuarios predefinidos (en producción usar base de datos)
DEMO_USERS = {
    'usuario': {
        'username': 'usuario',
        'password_hash': None,  # Se genera dinámicamente
        'profile': 'usuario',
        'full_name': 'Usuario Demo'
    },
    'analista': {
        'username': 'analista', 
        'password_hash': None,  # Se genera dinámicamente
        'profile': 'analista',
        'full_name': 'Analista Demo'
    },
    'admin': {
        'username': 'admin',
        'password_hash': None,  # Se genera dinámicamente
        'profile': 'admin', 
        'full_name': 'Administrador'
    }
}


class AuthManager:
    """Gestor de autenticación"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera hash bcrypt de una contraseña
        
        Args:
            password: Contraseña en texto plano
        
        Returns:
            Hash bcrypt
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verifica una contraseña contra su hash
        
        Args:
            password: Contraseña en texto plano
            hashed: Hash bcrypt
        
        Returns:
            True si la contraseña es correcta
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Error verificando contraseña: {e}")
            return False
    
    @staticmethod
    def generate_token(username: str, profile: str = 'usuario') -> str:
        """
        Genera un JWT token con perfil de usuario
        
        Args:
            username: Nombre de usuario
            profile: Perfil del usuario (usuario, analista, admin)
        
        Returns:
            JWT token
        """
        payload = {
            'username': username,
            'profile': profile,
            'permissions': USER_PROFILES.get(profile, {}).get('permissions', []),
            'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica y decodifica un JWT token
        
        Args:
            token: JWT token
        
        Returns:
            Payload decodificado o None si es inválido
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Token inválido: {e}")
            return None
    
    @staticmethod
    def initialize_demo_users():
        """Inicializa usuarios demo con contraseñas"""
        # Solo admin con contraseña admin123
        default_passwords = {
            'admin': 'admin123'
        }
        
        # Solo inicializar admin
        if 'admin' in DEMO_USERS:
            DEMO_USERS['admin']['password_hash'] = AuthManager.hash_password(default_passwords['admin'])
            
        logger.info("🔐 Usuario admin inicializado")
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario - Solo admin con admin123
        
        Args:
            username: Nombre de usuario
            password: Contraseña
        
        Returns:
            Dict con info del usuario o None si falla
        """
        # Inicializar admin si es necesario
        if 'admin' in DEMO_USERS and not DEMO_USERS['admin']['password_hash']:
            AuthManager.initialize_demo_users()
        
        # Solo verificar usuario admin
        if username == 'admin':
            user_data = DEMO_USERS.get('admin')
            if user_data and AuthManager.verify_password(password, user_data['password_hash']):
                logger.info(f"✅ Administrador autenticado")
                
                return {
                    'username': 'admin',
                    'profile': 'admin',
                    'full_name': 'Administrador',
                    'permissions': USER_PROFILES['admin']['permissions'],
                    'hidden_sections': [],  # Admin ve todo
                    'token': AuthManager.generate_token('admin', 'admin')
                }
        
        logger.warning(f"❌ Autenticación fallida para: {username}")
        return None
    
    @staticmethod
    def get_user_profile(username: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el perfil de un usuario
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Diccionario con perfil del usuario
        """
        if username in DEMO_USERS:
            user_data = DEMO_USERS[username]
            profile_info = USER_PROFILES[user_data['profile']].copy()
            profile_info.update({
                'username': username,
                'full_name': user_data['full_name']
            })
            return profile_info
        return None
    
    @staticmethod
    def has_permission(user_permissions: List[str], required_permission: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico
        
        Args:
            user_permissions: Lista de permisos del usuario
            required_permission: Permiso requerido
            
        Returns:
            True si tiene el permiso
        """
        return required_permission in user_permissions
    
    @staticmethod
    def get_visible_sections(user_profile: str) -> List[str]:
        """
        Obtiene las secciones visibles para un perfil de usuario
        
        Args:
            user_profile: Perfil del usuario
            
        Returns:
            Lista de secciones visibles
        """
        all_sections = ['matricula', 'egresados', 'titulacion', 'establecimientos', 'docentes', 'proyectos']
        hidden = USER_PROFILES.get(user_profile, {}).get('hidden_sections', [])
        return [section for section in all_sections if section not in hidden]


# Instancia global
auth_manager = AuthManager()


# Función auxiliar para generar hash de contraseña (uso en desarrollo)
def generate_password_hash(password: str) -> None:
    """
    Función auxiliar para generar hash de contraseñas
    Usar en consola para generar nuevos hashes
    """
    hashed = auth_manager.hash_password(password)
    print(f"\nHash generado para '{password}':")
    print(hashed)
    print("\nAgregar a .env como:")
    print(f"ADMIN_PASSWORD_HASH={hashed}\n")


if __name__ == '__main__':
    # Ejemplo de uso
    import sys
    
    if len(sys.argv) > 1:
        generate_password_hash(sys.argv[1])
    else:
        print("Uso: python auth.py <contraseña>")
