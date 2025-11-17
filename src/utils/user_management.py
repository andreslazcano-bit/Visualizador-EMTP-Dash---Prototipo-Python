"""
============================================================================
GESTIÓN DE USUARIOS - CRUD Y PERSISTENCIA
============================================================================
Sistema completo de gestión de usuarios con SQLite
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import bcrypt
from loguru import logger

from config.settings import settings
from src.utils.auth import USER_PROFILES


class UserManager:
    """Gestor de usuarios con persistencia en SQLite"""
    
    def __init__(self):
        """Inicializa el gestor de usuarios"""
        self.db_path = settings.DATA_DIR / 'users.db'
        
        # Crear directorio si no existe
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Inicializar base de datos
        self._init_database()
        
        # Crear usuario admin por defecto si no existe
        self._create_default_admin()
    
    def _init_database(self):
        """Crea la tabla de usuarios si no existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            profile TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            last_login TEXT,
            created_by TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Base de datos de usuarios inicializada: {self.db_path}")
    
    def _create_default_admin(self):
        """Crea usuario admin por defecto si no existe"""
        if not self.user_exists('admin'):
            self.create_user(
                username='admin',
                password='admin123',
                profile='admin',
                full_name='Administrador',
                email='admin@emtp.cl',
                created_by='system'
            )
            logger.info("✅ Usuario admin creado por defecto")
    
    def _hash_password(self, password: str) -> str:
        """Genera hash bcrypt de contraseña"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verifica contraseña contra hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(
        self,
        username: str,
        password: str,
        profile: str,
        full_name: str,
        email: Optional[str] = None,
        created_by: str = 'admin'
    ) -> Dict[str, Any]:
        """
        Crea un nuevo usuario
        
        Args:
            username: Nombre de usuario (único)
            password: Contraseña en texto plano
            profile: Perfil del usuario (usuario, analista, admin)
            full_name: Nombre completo
            email: Email del usuario
            created_by: Usuario que crea este usuario
        
        Returns:
            Diccionario con resultado
        """
        # Validar perfil
        if profile not in USER_PROFILES:
            return {
                'success': False,
                'error': f'Perfil inválido. Debe ser: {", ".join(USER_PROFILES.keys())}'
            }
        
        # Validar que username no exista
        if self.user_exists(username):
            return {
                'success': False,
                'error': f'El usuario "{username}" ya existe'
            }
        
        # Hash de contraseña
        password_hash = self._hash_password(password)
        
        # Insertar en base de datos
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        try:
            cursor.execute('''
            INSERT INTO users (username, password_hash, profile, full_name, email, created_at, updated_at, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, profile, full_name, email, now, now, created_by))
            
            conn.commit()
            user_id = cursor.lastrowid
            
            logger.info(f"✅ Usuario creado: {username} ({profile}) por {created_by}")
            
            return {
                'success': True,
                'user_id': user_id,
                'message': f'Usuario "{username}" creado exitosamente'
            }
        
        except sqlite3.Error as e:
            logger.error(f"❌ Error al crear usuario: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            conn.close()
    
    def user_exists(self, username: str) -> bool:
        """Verifica si un usuario existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count > 0
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
        
        Returns:
            Diccionario con info del usuario o None si falla
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM users WHERE username = ? AND is_active = 1
        ''', (username,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return None
        
        # Verificar contraseña
        if not self._verify_password(password, user['password_hash']):
            conn.close()
            return None
        
        # Actualizar last_login
        cursor.execute('''
        UPDATE users SET last_login = ? WHERE username = ?
        ''', (datetime.now().isoformat(), username))
        
        conn.commit()
        conn.close()
        
        # Retornar info del usuario
        profile_info = USER_PROFILES[user['profile']]
        
        return {
            'username': user['username'],
            'profile': user['profile'],
            'full_name': user['full_name'],
            'email': user['email'],
            'permissions': profile_info['permissions'],
            'hidden_sections': profile_info['hidden_sections']
        }
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un usuario"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        
        if not user:
            return None
        
        return dict(user)
    
    def get_all_users(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Obtiene lista de todos los usuarios
        
        Args:
            include_inactive: Si True, incluye usuarios desactivados
        
        Returns:
            Lista de diccionarios con info de usuarios
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if include_inactive:
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY created_at DESC')
        
        users = cursor.fetchall()
        conn.close()
        
        return [dict(user) for user in users]
    
    def update_user(
        self,
        username: str,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        profile: Optional[str] = None,
        password: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Actualiza información de un usuario
        
        Args:
            username: Usuario a actualizar
            full_name: Nuevo nombre completo (opcional)
            email: Nuevo email (opcional)
            profile: Nuevo perfil (opcional)
            password: Nueva contraseña (opcional)
        
        Returns:
            Diccionario con resultado
        """
        if not self.user_exists(username):
            return {
                'success': False,
                'error': f'Usuario "{username}" no existe'
            }
        
        # Validar perfil si se proporciona
        if profile and profile not in USER_PROFILES:
            return {
                'success': False,
                'error': f'Perfil inválido. Debe ser: {", ".join(USER_PROFILES.keys())}'
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if full_name:
            updates.append('full_name = ?')
            params.append(full_name)
        
        if email:
            updates.append('email = ?')
            params.append(email)
        
        if profile:
            updates.append('profile = ?')
            params.append(profile)
        
        if password:
            updates.append('password_hash = ?')
            params.append(self._hash_password(password))
        
        if not updates:
            conn.close()
            return {
                'success': False,
                'error': 'No hay campos para actualizar'
            }
        
        # Agregar updated_at
        updates.append('updated_at = ?')
        params.append(datetime.now().isoformat())
        
        # Agregar username al final
        params.append(username)
        
        try:
            query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
            cursor.execute(query, params)
            conn.commit()
            
            logger.info(f"✅ Usuario actualizado: {username}")
            
            return {
                'success': True,
                'message': f'Usuario "{username}" actualizado exitosamente'
            }
        
        except sqlite3.Error as e:
            logger.error(f"❌ Error al actualizar usuario: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            conn.close()
    
    def deactivate_user(self, username: str) -> Dict[str, Any]:
        """Desactiva un usuario (soft delete)"""
        if username == 'admin':
            return {
                'success': False,
                'error': 'No se puede desactivar el usuario admin principal'
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE users SET is_active = 0, updated_at = ? WHERE username = ?
            ''', (datetime.now().isoformat(), username))
            
            conn.commit()
            
            logger.info(f"🔒 Usuario desactivado: {username}")
            
            return {
                'success': True,
                'message': f'Usuario "{username}" desactivado'
            }
        
        except sqlite3.Error as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            conn.close()
    
    def activate_user(self, username: str) -> Dict[str, Any]:
        """Activa un usuario previamente desactivado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE users SET is_active = 1, updated_at = ? WHERE username = ?
            ''', (datetime.now().isoformat(), username))
            
            conn.commit()
            
            logger.info(f"✅ Usuario activado: {username}")
            
            return {
                'success': True,
                'message': f'Usuario "{username}" activado'
            }
        
        except sqlite3.Error as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            conn.close()
    
    def delete_user(self, username: str) -> Dict[str, Any]:
        """Elimina permanentemente un usuario (hard delete)"""
        if username == 'admin':
            return {
                'success': False,
                'error': 'No se puede eliminar el usuario admin principal'
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            
            logger.warning(f"🗑️ Usuario eliminado permanentemente: {username}")
            
            return {
                'success': True,
                'message': f'Usuario "{username}" eliminado permanentemente'
            }
        
        except sqlite3.Error as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            conn.close()
    
    def get_user_count_by_profile(self) -> Dict[str, int]:
        """Obtiene conteo de usuarios por perfil"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT profile, COUNT(*) as count
        FROM users
        WHERE is_active = 1
        GROUP BY profile
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        counts = {profile: 0 for profile in USER_PROFILES.keys()}
        for profile, count in results:
            counts[profile] = count
        
        return counts


# Instancia global del gestor de usuarios
user_manager = UserManager()
