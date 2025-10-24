"""
============================================================================
DATA LOADERS - Carga de datos desde múltiples fuentes
============================================================================
Soporte para: SQL Server, PostgreSQL, SharePoint, CSV, Excel, Parquet, RDS
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union, Dict, Any
from loguru import logger
import pickle

from config.settings import settings
from config.database import db_manager


class DataLoader:
    """Cargador de datos desde múltiples fuentes"""
    
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}
    
    # ========================================================================
    # CARGA DESDE SQL
    # ========================================================================
    
    def load_from_sql_server(
        self, 
        query: Optional[str] = None,
        table: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde SQL Server
        
        Args:
            query: SQL query personalizada
            table: Nombre de tabla (si no se proporciona query)
        
        Returns:
            DataFrame con los datos
        """
        if not settings.SQL_SERVER_ENABLED:
            logger.warning("SQL Server no está habilitado")
            return None
        
        if query is None and table is None:
            logger.error("Debe proporcionar query o table")
            return None
        
        if query is None:
            query = f"SELECT * FROM {table}"
        
        logger.info(f"📊 Cargando datos desde SQL Server...")
        df = db_manager.execute_query(query, engine_name='sql_server')
        
        if df is not None:
            logger.success(f"✅ {len(df)} filas cargadas desde SQL Server")
        
        return df
    
    def load_from_postgres(
        self, 
        query: Optional[str] = None,
        table: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde PostgreSQL
        
        Args:
            query: SQL query personalizada
            table: Nombre de tabla (si no se proporciona query)
        
        Returns:
            DataFrame con los datos
        """
        if not settings.POSTGRES_ENABLED:
            logger.warning("PostgreSQL no está habilitado")
            return None
        
        if query is None and table is None:
            logger.error("Debe proporcionar query o table")
            return None
        
        if query is None:
            query = f"SELECT * FROM {table}"
        
        logger.info(f"📊 Cargando datos desde PostgreSQL...")
        df = db_manager.execute_query(query, engine_name='postgres')
        
        if df is not None:
            logger.success(f"✅ {len(df)} filas cargadas desde PostgreSQL")
        
        return df
    
    # ========================================================================
    # CARGA DESDE SHAREPOINT
    # ========================================================================
    
    def load_from_sharepoint(
        self,
        folder_path: str,
        file_name: str
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde SharePoint
        
        Args:
            folder_path: Ruta de la carpeta en SharePoint
            file_name: Nombre del archivo
        
        Returns:
            DataFrame con los datos
        """
        if not settings.SHAREPOINT_ENABLED:
            logger.warning("SharePoint no está habilitado")
            return None
        
        try:
            from Office365.runtime.auth.authentication_context import AuthenticationContext
            from Office365.SharePoint.client_context import ClientContext
            
            # Autenticación
            ctx_auth = AuthenticationContext(settings.SHAREPOINT_SITE_URL)
            if ctx_auth.acquire_token_for_user(
                settings.SHAREPOINT_USERNAME, 
                settings.SHAREPOINT_PASSWORD
            ):
                ctx = ClientContext(settings.SHAREPOINT_SITE_URL, ctx_auth)
                
                # Construir ruta completa
                file_url = f"{folder_path}/{file_name}"
                
                logger.info(f"📊 Descargando desde SharePoint: {file_url}")
                
                # Aquí iría la lógica específica para descargar
                # Por ahora retornamos None y logging
                logger.warning("⚠️ Implementación de SharePoint pendiente")
                return None
            else:
                logger.error("❌ Autenticación en SharePoint falló")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error cargando desde SharePoint: {e}")
            return None
    
    # ========================================================================
    # CARGA DESDE ARCHIVOS LOCALES
    # ========================================================================
    
    def load_from_csv(
        self,
        file_path: Union[str, Path],
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde CSV
        
        Args:
            file_path: Ruta al archivo CSV
            **kwargs: Argumentos adicionales para pd.read_csv
        
        Returns:
            DataFrame con los datos
        """
        try:
            file_path = Path(file_path)
            logger.info(f"📊 Cargando CSV: {file_path.name}")
            
            df = pd.read_csv(file_path, **kwargs)
            
            logger.success(f"✅ {len(df)} filas cargadas desde CSV")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando CSV: {e}")
            return None
    
    def load_from_excel(
        self,
        file_path: Union[str, Path],
        sheet_name: Union[str, int] = 0,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde Excel
        
        Args:
            file_path: Ruta al archivo Excel
            sheet_name: Nombre o índice de la hoja
            **kwargs: Argumentos adicionales para pd.read_excel
        
        Returns:
            DataFrame con los datos
        """
        try:
            file_path = Path(file_path)
            logger.info(f"📊 Cargando Excel: {file_path.name}")
            
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            
            logger.success(f"✅ {len(df)} filas cargadas desde Excel")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando Excel: {e}")
            return None
    
    def load_from_parquet(
        self,
        file_path: Union[str, Path],
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde Parquet
        
        Args:
            file_path: Ruta al archivo Parquet
            **kwargs: Argumentos adicionales para pd.read_parquet
        
        Returns:
            DataFrame con los datos
        """
        try:
            file_path = Path(file_path)
            logger.info(f"📊 Cargando Parquet: {file_path.name}")
            
            df = pd.read_parquet(file_path, **kwargs)
            
            logger.success(f"✅ {len(df)} filas cargadas desde Parquet")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando Parquet: {e}")
            return None
    
    def load_from_rds(
        self,
        file_path: Union[str, Path]
    ) -> Optional[pd.DataFrame]:
        """
        Carga datos desde archivo RDS de R (usando pyreadr o rpy2)
        
        Args:
            file_path: Ruta al archivo RDS
        
        Returns:
            DataFrame con los datos
        """
        try:
            # Opción 1: Usar pyreadr (más simple)
            try:
                import pyreadr
                file_path = Path(file_path)
                logger.info(f"📊 Cargando RDS: {file_path.name}")
                
                result = pyreadr.read_r(str(file_path))
                # RDS contiene un solo objeto, tomar el primero
                df = result[None] if None in result else list(result.values())[0]
                
                logger.success(f"✅ {len(df)} filas cargadas desde RDS")
                return df
                
            except ImportError:
                logger.warning("pyreadr no instalado, intentando con pickle...")
                
                # Opción 2: Si el RDS fue guardado como pickle
                with open(file_path, 'rb') as f:
                    df = pickle.load(f)
                
                logger.success(f"✅ {len(df)} filas cargadas desde RDS (pickle)")
                return df
                
        except Exception as e:
            logger.error(f"❌ Error cargando RDS: {e}")
            logger.info("💡 Tip: Convertir RDS a Parquet en R: arrow::write_parquet(data, 'file.parquet')")
            return None
    
    # ========================================================================
    # MÉTODOS DE CONVENIENCIA
    # ========================================================================
    
    def load_matricula(self) -> Optional[pd.DataFrame]:
        """Carga datos de matrícula desde la fuente configurada"""
        # Prioridad: SQL Server > Local > SharePoint
        
        if settings.SQL_SERVER_ENABLED:
            return self.load_from_sql_server(table='matricula')
        
        elif settings.LOCAL_DATA_ENABLED:
            # Buscar archivo de matrícula en data/processed
            matricula_files = list(settings.PROCESSED_DATA_DIR.glob('*Matricula*.parquet'))
            if not matricula_files:
                matricula_files = list(settings.PROCESSED_DATA_DIR.glob('*Matricula*.csv'))
            if not matricula_files:
                matricula_files = list(settings.PROCESSED_DATA_DIR.glob('*Matricula*.rds'))
            
            if matricula_files:
                file_path = matricula_files[0]
                if file_path.suffix == '.parquet':
                    return self.load_from_parquet(file_path)
                elif file_path.suffix == '.csv':
                    return self.load_from_csv(file_path)
                elif file_path.suffix == '.rds':
                    return self.load_from_rds(file_path)
        
        logger.warning("⚠️ No se pudo cargar datos de matrícula")
        return None
    
    def load_docentes(self) -> Optional[pd.DataFrame]:
        """Carga datos de docentes desde la fuente configurada"""
        if settings.SQL_SERVER_ENABLED:
            return self.load_from_sql_server(table='docentes')
        
        elif settings.LOCAL_DATA_ENABLED:
            docentes_files = list(settings.PROCESSED_DATA_DIR.glob('*Docentes*.parquet'))
            if not docentes_files:
                docentes_files = list(settings.PROCESSED_DATA_DIR.glob('*Docentes*.csv'))
            if not docentes_files:
                docentes_files = list(settings.PROCESSED_DATA_DIR.glob('*Docentes*.rds'))
            
            if docentes_files:
                file_path = docentes_files[0]
                if file_path.suffix == '.parquet':
                    return self.load_from_parquet(file_path)
                elif file_path.suffix == '.csv':
                    return self.load_from_csv(file_path)
                elif file_path.suffix == '.rds':
                    return self.load_from_rds(file_path)
        
        logger.warning("⚠️ No se pudo cargar datos de docentes")
        return None
    
    def load_geographic_data(self) -> Optional[pd.DataFrame]:
        """Carga datos geográficos (comunas)"""
        if settings.LOCAL_DATA_ENABLED:
            geo_files = list(settings.GEOGRAPHIC_DATA_DIR.glob('comunas*.parquet'))
            if not geo_files:
                geo_files = list(settings.GEOGRAPHIC_DATA_DIR.glob('comunas*.geojson'))
            if not geo_files:
                geo_files = list(settings.GEOGRAPHIC_DATA_DIR.glob('comunas*.rds'))
            
            if geo_files:
                file_path = geo_files[0]
                if file_path.suffix == '.parquet':
                    return self.load_from_parquet(file_path)
                elif file_path.suffix == '.geojson':
                    import geopandas as gpd
                    return gpd.read_file(file_path)
                elif file_path.suffix == '.rds':
                    return self.load_from_rds(file_path)
        
        logger.warning("⚠️ No se pudo cargar datos geográficos")
        return None


# Instancia global del loader
data_loader = DataLoader()
