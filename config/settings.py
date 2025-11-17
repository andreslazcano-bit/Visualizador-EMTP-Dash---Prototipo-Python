"""
============================================================================
CONFIGURACIÓN GLOBAL - VISUALIZADOR EMTP
============================================================================
Gestión centralizada de configuración usando variables de entorno
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from loguru import logger

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración global de la aplicación"""
    
    # ========================================================================
    # CONFIGURACIÓN GENERAL
    # ========================================================================
    APP_NAME: str = os.getenv('APP_NAME', 'Visualizador EMTP')
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'change-this-secret-key')
    PORT: int = int(os.getenv('PORT', 8050))
    HOST: str = os.getenv('HOST', '0.0.0.0')
    
    # ========================================================================
    # RUTAS
    # ========================================================================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / 'data'
    RAW_DATA_DIR: Path = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR: Path = DATA_DIR / 'processed'
    GEOGRAPHIC_DATA_DIR: Path = DATA_DIR / 'geographic'
    REPORTS_DIR: Path = BASE_DIR / 'reports'
    REPORTS_OUTPUT_DIR: Path = REPORTS_DIR / 'output'
    REPORTS_TEMPLATES_DIR: Path = REPORTS_DIR / 'templates'
    LOGS_DIR: Path = BASE_DIR / 'logs'
    
    # ========================================================================
    # SQL SERVER
    # ========================================================================
    SQL_SERVER_ENABLED: bool = os.getenv('SQL_SERVER_ENABLED', 'False').lower() == 'true'
    SQL_SERVER_DRIVER: str = os.getenv('SQL_SERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
    SQL_SERVER_HOST: str = os.getenv('SQL_SERVER_HOST', '')
    SQL_SERVER_PORT: int = int(os.getenv('SQL_SERVER_PORT', 1433))
    SQL_SERVER_DATABASE: str = os.getenv('SQL_SERVER_DATABASE', '')
    SQL_SERVER_USERNAME: str = os.getenv('SQL_SERVER_USERNAME', '')
    SQL_SERVER_PASSWORD: str = os.getenv('SQL_SERVER_PASSWORD', '')
    
    # ========================================================================
    # POSTGRESQL
    # ========================================================================
    POSTGRES_ENABLED: bool = os.getenv('POSTGRES_ENABLED', 'False').lower() == 'true'
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DATABASE: str = os.getenv('POSTGRES_DATABASE', '')
    POSTGRES_USERNAME: str = os.getenv('POSTGRES_USERNAME', '')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '')
    
    # ========================================================================
    # SHAREPOINT
    # ========================================================================
    SHAREPOINT_ENABLED: bool = os.getenv('SHAREPOINT_ENABLED', 'False').lower() == 'true'
    SHAREPOINT_SITE_URL: str = os.getenv('SHAREPOINT_SITE_URL', '')
    SHAREPOINT_CLIENT_ID: str = os.getenv('SHAREPOINT_CLIENT_ID', '')
    SHAREPOINT_CLIENT_SECRET: str = os.getenv('SHAREPOINT_CLIENT_SECRET', '')
    SHAREPOINT_USERNAME: str = os.getenv('SHAREPOINT_USERNAME', '')
    SHAREPOINT_PASSWORD: str = os.getenv('SHAREPOINT_PASSWORD', '')
    
    # ========================================================================
    # ARCHIVOS LOCALES
    # ========================================================================
    LOCAL_DATA_ENABLED: bool = os.getenv('LOCAL_DATA_ENABLED', 'True').lower() == 'true'
    
    # ========================================================================
    # REDIS / CACHE
    # ========================================================================
    REDIS_ENABLED: bool = os.getenv('REDIS_ENABLED', 'False').lower() == 'true'
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD', None)
    REDIS_DB: int = int(os.getenv('REDIS_DB', 0))
    CACHE_TIMEOUT: int = int(os.getenv('CACHE_TIMEOUT', 3600))
    
    # ========================================================================
    # AUTENTICACIÓN
    # ========================================================================
    AUTH_ENABLED: bool = os.getenv('AUTH_ENABLED', 'True').lower() == 'true'
    ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD_HASH: str = os.getenv('ADMIN_PASSWORD_HASH', '')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS: int = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    
    # ========================================================================
    # GESTIÓN DE SESIONES
    # ========================================================================
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))
    SESSION_WARNING_MINUTES: int = int(os.getenv('SESSION_WARNING_MINUTES', 5))
    MAX_SESSION_DURATION_HOURS: int = int(os.getenv('MAX_SESSION_DURATION_HOURS', 8))
    SESSION_CLEANUP_INTERVAL_MINUTES: int = int(os.getenv('SESSION_CLEANUP_INTERVAL_MINUTES', 15))
    
    # ========================================================================
    # LOGGING
    # ========================================================================
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: Path = LOGS_DIR / 'app.log'
    LOG_MAX_SIZE: str = os.getenv('LOG_MAX_SIZE', '10 MB')
    LOG_BACKUP_COUNT: int = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # ========================================================================
    # LÍMITES Y PERFORMANCE
    # ========================================================================
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv('MAX_UPLOAD_SIZE_MB', 100))
    MAX_ROWS_DISPLAY: int = int(os.getenv('MAX_ROWS_DISPLAY', 10000))
    MAX_ROWS_EXPORT: int = int(os.getenv('MAX_ROWS_EXPORT', 100000))
    ENABLE_PROFILING: bool = os.getenv('ENABLE_PROFILING', 'False').lower() == 'true'
    
    # ========================================================================
    # SENTRY
    # ========================================================================
    SENTRY_ENABLED: bool = os.getenv('SENTRY_ENABLED', 'False').lower() == 'true'
    SENTRY_DSN: str = os.getenv('SENTRY_DSN', '')
    
    def __init__(self):
        """Inicializa y crea directorios necesarios"""
        self._create_directories()
        self._validate_config()
    
    def _create_directories(self):
        """Crea directorios necesarios si no existen"""
        directories = [
            self.DATA_DIR,
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.GEOGRAPHIC_DATA_DIR,
            self.REPORTS_DIR,
            self.REPORTS_OUTPUT_DIR,
            self.REPORTS_TEMPLATES_DIR,
            self.LOGS_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _validate_config(self):
        """Valida configuración básica"""
        if self.ENVIRONMENT == 'production' and self.SECRET_KEY == 'change-this-secret-key':
            logger.warning("⚠️ ADVERTENCIA: Usando SECRET_KEY por defecto en producción!")
        
        if self.SQL_SERVER_ENABLED and not self.SQL_SERVER_HOST:
            logger.warning("⚠️ SQL Server habilitado pero sin host configurado")
        
        if self.SHAREPOINT_ENABLED and not self.SHAREPOINT_SITE_URL:
            logger.warning("⚠️ SharePoint habilitado pero sin URL configurada")
    
    @property
    def is_production(self) -> bool:
        """Verifica si está en producción"""
        return self.ENVIRONMENT == 'production'
    
    @property
    def is_development(self) -> bool:
        """Verifica si está en desarrollo"""
        return self.ENVIRONMENT == 'development'
    
    def get_sql_server_connection_string(self) -> str:
        """Genera string de conexión para SQL Server"""
        return (
            f"DRIVER={{{self.SQL_SERVER_DRIVER}}};"
            f"SERVER={self.SQL_SERVER_HOST},{self.SQL_SERVER_PORT};"
            f"DATABASE={self.SQL_SERVER_DATABASE};"
            f"UID={self.SQL_SERVER_USERNAME};"
            f"PWD={self.SQL_SERVER_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
        )
    
    def get_postgres_connection_string(self) -> str:
        """Genera string de conexión para PostgreSQL"""
        return (
            f"postgresql://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        )

# Instancia global de configuración
settings = Settings()
