"""
============================================================================
SISTEMA DE AUDITORÍA - LOGGING DE ACCESOS Y ACCIONES
============================================================================
Registra todas las acciones de usuarios para trazabilidad y compliance
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
from loguru import logger
import pandas as pd

from config.settings import settings


class AuditLogger:
    """Sistema de auditoría para registrar acciones de usuarios"""
    
    def __init__(self):
        """Inicializa el sistema de auditoría"""
        self.audit_file = settings.LOGS_DIR / 'audit.jsonl'
        
        # Crear directorio de logs si no existe
        settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo si no existe
        if not self.audit_file.exists():
            self.audit_file.touch()
    
    def log_action(
        self,
        username: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = 'success'
    ):
        """
        Registra una acción de usuario
        
        Args:
            username: Nombre de usuario que realiza la acción
            action: Tipo de acción (login, logout, view_dashboard, export_data, etc.)
            details: Detalles adicionales de la acción
            ip_address: Dirección IP del usuario
            user_agent: User agent del navegador
            status: Estado de la acción (success, error, denied)
        """
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'action': action,
            'status': status,
            'details': details or {},
            'ip_address': ip_address or 'unknown',
            'user_agent': user_agent or 'unknown'
        }
        
        # Escribir en archivo JSONL (JSON Lines)
        with open(self.audit_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry, ensure_ascii=False) + '\n')
        
        # Log adicional en consola para desarrollo
        logger.info(f"AUDIT | {username} | {action} | {status}")
    
    def log_login(self, username: str, success: bool, ip_address: Optional[str] = None):
        """Registra intento de login"""
        self.log_action(
            username=username,
            action='login',
            status='success' if success else 'failed',
            details={'login_attempt': True},
            ip_address=ip_address
        )
    
    def log_logout(self, username: str):
        """Registra logout de usuario"""
        self.log_action(
            username=username,
            action='logout',
            status='success'
        )
    
    def log_view_dashboard(self, username: str, dashboard: str):
        """Registra acceso a un dashboard"""
        self.log_action(
            username=username,
            action='view_dashboard',
            details={'dashboard': dashboard}
        )
    
    def log_export_data(self, username: str, export_type: str, dashboard: str):
        """Registra exportación de datos"""
        self.log_action(
            username=username,
            action='export_data',
            details={
                'export_type': export_type,
                'dashboard': dashboard
            }
        )
    
    def log_user_management(self, admin_username: str, action: str, target_username: str, details: Optional[Dict] = None):
        """Registra acciones de gestión de usuarios"""
        self.log_action(
            username=admin_username,
            action=f'user_{action}',
            details={
                'target_user': target_username,
                **(details or {})
            }
        )
    
    def log_permission_denied(self, username: str, attempted_action: str):
        """Registra intento de acción sin permisos"""
        self.log_action(
            username=username,
            action='permission_denied',
            status='denied',
            details={'attempted_action': attempted_action}
        )
    
    def get_audit_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        username: Optional[str] = None,
        action: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        Obtiene logs de auditoría con filtros
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            username: Filtrar por usuario
            action: Filtrar por tipo de acción
            status: Filtrar por estado
            limit: Número máximo de registros
        
        Returns:
            DataFrame con logs filtrados
        """
        if not self.audit_file.exists():
            return pd.DataFrame()
        
        # Leer archivo JSONL
        logs = []
        with open(self.audit_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        if not logs:
            return pd.DataFrame()
        
        df = pd.DataFrame(logs)
        
        # Convertir timestamp a datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Aplicar filtros
        if start_date:
            df = df[df['timestamp'] >= start_date]
        
        if end_date:
            df = df[df['timestamp'] <= end_date]
        
        if username:
            df = df[df['username'] == username]
        
        if action:
            df = df[df['action'] == action]
        
        if status:
            df = df[df['status'] == status]
        
        # Ordenar por fecha descendente (más recientes primero)
        df = df.sort_values('timestamp', ascending=False)
        
        # Limitar resultados
        df = df.head(limit)
        
        return df
    
    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso de los últimos N días
        
        Args:
            days: Número de días a analizar
        
        Returns:
            Diccionario con estadísticas
        """
        start_date = datetime.now() - timedelta(days=days)
        df = self.get_audit_logs(start_date=start_date)
        
        if df.empty:
            return {
                'total_actions': 0,
                'unique_users': 0,
                'logins': 0,
                'failed_logins': 0,
                'exports': 0,
                'top_users': [],
                'top_actions': []
            }
        
        stats = {
            'total_actions': len(df),
            'unique_users': df['username'].nunique(),
            'logins': len(df[df['action'] == 'login']),
            'failed_logins': len(df[(df['action'] == 'login') & (df['status'] == 'failed')]),
            'exports': len(df[df['action'] == 'export_data']),
            'top_users': df['username'].value_counts().head(10).to_dict(),
            'top_actions': df['action'].value_counts().head(10).to_dict()
        }
        
        return stats
    
    def get_user_activity(self, username: str, days: int = 30) -> Dict[str, Any]:
        """
        Obtiene actividad de un usuario específico
        
        Args:
            username: Nombre de usuario
            days: Número de días a analizar
        
        Returns:
            Diccionario con actividad del usuario
        """
        start_date = datetime.now() - timedelta(days=days)
        df = self.get_audit_logs(start_date=start_date, username=username)
        
        if df.empty:
            return {
                'total_actions': 0,
                'last_login': None,
                'actions_by_type': {},
                'dashboards_visited': []
            }
        
        # Extraer dashboards visitados de los detalles
        dashboards = []
        for _, row in df[df['action'] == 'view_dashboard'].iterrows():
            if isinstance(row['details'], dict) and 'dashboard' in row['details']:
                dashboards.append(row['details']['dashboard'])
        
        activity = {
            'total_actions': len(df),
            'last_login': df[df['action'] == 'login'].iloc[0]['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if len(df[df['action'] == 'login']) > 0 else None,
            'actions_by_type': df['action'].value_counts().to_dict(),
            'dashboards_visited': list(set(dashboards))
        }
        
        return activity


# Instancia global del sistema de auditoría
audit_logger = AuditLogger()
