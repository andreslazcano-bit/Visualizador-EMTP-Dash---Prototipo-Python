"""
============================================================================
GESTIÓN DE CONEXIONES A BASES DE DATOS
============================================================================
Soporte para múltiples fuentes de datos: SQL Server, PostgreSQL, MySQL
"""

from typing import Optional, Dict, Any
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool
from loguru import logger

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False
    logger.warning("⚠️ pyodbc no disponible - SQL Server deshabilitado")

from .settings import settings


class DatabaseManager:
    """Gestor centralizado de conexiones a bases de datos"""
    
    def __init__(self):
        self._engines: Dict[str, Engine] = {}
    
    def get_sql_server_engine(self) -> Optional[Engine]:
        """Obtiene engine para SQL Server"""
        if not PYODBC_AVAILABLE:
            logger.warning("⚠️ SQL Server no disponible - pyodbc no instalado")
            return None
            
        if not settings.SQL_SERVER_ENABLED:
            logger.warning("SQL Server no está habilitado en configuración")
            return None
        
        if 'sql_server' not in self._engines:
            try:
                connection_string = (
                    f"mssql+pyodbc://{settings.SQL_SERVER_USERNAME}:"
                    f"{settings.SQL_SERVER_PASSWORD}@{settings.SQL_SERVER_HOST}:"
                    f"{settings.SQL_SERVER_PORT}/{settings.SQL_SERVER_DATABASE}"
                    f"?driver={settings.SQL_SERVER_DRIVER.replace(' ', '+')}"
                )
                
                self._engines['sql_server'] = create_engine(
                    connection_string,
                    poolclass=NullPool,
                    echo=settings.DEBUG
                )
                logger.info("✅ Conexión a SQL Server establecida")
            except Exception as e:
                logger.error(f"❌ Error conectando a SQL Server: {e}")
                return None
        
        return self._engines['sql_server']
    
    def get_postgres_engine(self) -> Optional[Engine]:
        """Obtiene engine para PostgreSQL"""
        if not settings.POSTGRES_ENABLED:
            logger.warning("PostgreSQL no está habilitado en configuración")
            return None
        
        if 'postgres' not in self._engines:
            try:
                connection_string = settings.get_postgres_connection_string()
                
                self._engines['postgres'] = create_engine(
                    connection_string,
                    poolclass=NullPool,
                    echo=settings.DEBUG
                )
                logger.info("✅ Conexión a PostgreSQL establecida")
            except Exception as e:
                logger.error(f"❌ Error conectando a PostgreSQL: {e}")
                return None
        
        return self._engines['postgres']
    
    def execute_query(
        self, 
        query: str, 
        engine_name: str = 'sql_server',
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[pd.DataFrame]:
        """
        Ejecuta una query y retorna DataFrame
        
        Args:
            query: SQL query a ejecutar
            engine_name: 'sql_server' o 'postgres'
            params: Parámetros para la query (opcional)
        
        Returns:
            DataFrame con resultados o None si hay error
        """
        try:
            if engine_name == 'sql_server':
                engine = self.get_sql_server_engine()
            elif engine_name == 'postgres':
                engine = self.get_postgres_engine()
            else:
                logger.error(f"Engine desconocido: {engine_name}")
                return None
            
            if engine is None:
                return None
            
            with engine.connect() as conn:
                df = pd.read_sql(text(query), conn, params=params)
            
            logger.info(f"✅ Query ejecutada exitosamente: {len(df)} filas retornadas")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error ejecutando query: {e}")
            return None
    
    def test_connection(self, engine_name: str = 'sql_server') -> bool:
        """
        Prueba la conexión a la base de datos
        
        Args:
            engine_name: 'sql_server' o 'postgres'
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            test_query = "SELECT 1 as test"
            df = self.execute_query(test_query, engine_name=engine_name)
            return df is not None and len(df) > 0
        except Exception as e:
            logger.error(f"❌ Test de conexión falló: {e}")
            return False
    
    def close_all(self):
        """Cierra todas las conexiones"""
        for name, engine in self._engines.items():
            try:
                engine.dispose()
                logger.info(f"✅ Conexión {name} cerrada")
            except Exception as e:
                logger.error(f"❌ Error cerrando conexión {name}: {e}")
        
        self._engines.clear()
    
    def __del__(self):
        """Limpieza al destruir el objeto"""
        self.close_all()


# Instancia global del gestor de bases de datos
db_manager = DatabaseManager()
