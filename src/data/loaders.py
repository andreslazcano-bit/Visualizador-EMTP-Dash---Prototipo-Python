"""
Módulo de carga de datos desde cache local
Los datos se actualizan semanalmente mediante scripts/actualizar_datos_semanal.py

Ventajas de usar cache:
- Velocidad: Lectura instantánea desde archivos Parquet locales
- Confiabilidad: Funciona aunque SQL Server esté caído
- Eficiencia: No sobrecarga las bases de datos MINEDUC
- Datos actualizados semanalmente (suficiente para datos educativos)
"""

import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# Directorio de cache
CACHE_DIR = Path('data/processed')

class CacheDataLoader:
    """
    Gestor de carga de datos desde cache local
    """
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.metadata = self.cargar_metadata()
    
    def cargar_metadata(self) -> Dict:
        """
        Carga la metadata de la última actualización
        """
        metadata_file = self.cache_dir / 'cache_metadata.json'
        
        if not metadata_file.exists():
            logger.warning("⚠️  No se encuentra metadata de cache")
            return {
                'fecha_actualizacion': None,
                'registros_totales': 0,
                'fuentes_actualizadas': []
            }
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"📋 Cache actualizado: {metadata.get('fecha_actualizacion')}")
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Error cargando metadata: {e}")
            return {}
    
    def get_ultima_actualizacion(self) -> Optional[datetime]:
        """
        Retorna la fecha de la última actualización del cache
        """
        fecha_str = self.metadata.get('fecha_actualizacion')
        if fecha_str:
            return datetime.fromisoformat(fecha_str)
        return None
    
    def get_dias_desde_actualizacion(self) -> Optional[int]:
        """
        Retorna cuántos días han pasado desde la última actualización
        """
        ultima = self.get_ultima_actualizacion()
        if ultima:
            return (datetime.now() - ultima).days
        return None
    
    def cargar_establecimientos(
        self, 
        region: Optional[str] = None,
        comuna: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Carga datos de establecimientos desde cache
        
        Args:
            region: Filtrar por región (opcional)
            comuna: Filtrar por comuna (opcional)
            
        Returns:
            DataFrame con datos de establecimientos
        """
        cache_file = self.cache_dir / 'cache_establecimientos.parquet'
        
        if not cache_file.exists():
            logger.error(f"❌ No existe archivo de cache: {cache_file}")
            # Retornar desde CSV de respaldo si existe
            return self._cargar_csv_respaldo('establecimientos.csv')
        
        try:
            df = pd.read_parquet(cache_file)
            logger.info(f"✅ Establecimientos cargados: {len(df)} registros")
            
            # Aplicar filtros
            if region:
                df = df[df['Region'] == region]
            if comuna:
                df = df[df['Comuna'] == comuna]
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando establecimientos: {e}")
            return pd.DataFrame()
    
    def cargar_matricula(
        self,
        region: Optional[str] = None,
        año: Optional[int] = None,
        agregado: bool = False
    ) -> pd.DataFrame:
        """
        Carga datos de matrícula desde cache
        
        Args:
            region: Filtrar por región (opcional)
            año: Filtrar por año (opcional)
            agregado: Si True, carga datos agregados (más rápido para dashboards)
            
        Returns:
            DataFrame con datos de matrícula
        """
        if agregado:
            cache_file = self.cache_dir / 'cache_matricula_agregado.parquet'
        else:
            cache_file = self.cache_dir / 'cache_matricula.parquet'
        
        if not cache_file.exists():
            logger.error(f"❌ No existe archivo de cache: {cache_file}")
            return self._cargar_csv_respaldo('matricula_region.csv')
        
        try:
            df = pd.read_parquet(cache_file)
            logger.info(f"✅ Matrícula cargada: {len(df)} registros {'(agregado)' if agregado else ''}")
            
            # Aplicar filtros
            if region:
                df = df[df['Region'] == region]
            if año:
                df = df[df['Año'] == año]
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando matrícula: {e}")
            return pd.DataFrame()
    
    def cargar_docentes(
        self,
        region: Optional[str] = None,
        especialidad: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Carga datos de docentes desde cache
        
        Args:
            region: Filtrar por región (opcional)
            especialidad: Filtrar por especialidad (opcional)
            
        Returns:
            DataFrame con datos de docentes
        """
        cache_file = self.cache_dir / 'cache_docentes.parquet'
        
        if not cache_file.exists():
            logger.error(f"❌ No existe archivo de cache: {cache_file}")
            return self._cargar_csv_respaldo('docentes_especialidad.csv')
        
        try:
            df = pd.read_parquet(cache_file)
            logger.info(f"✅ Docentes cargados: {len(df)} registros")
            
            # Aplicar filtros
            if region:
                df = df[df['Region'] == region]
            if especialidad:
                df = df[df['Especialidad'] == especialidad]
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando docentes: {e}")
            return pd.DataFrame()
    
    def cargar_titulados(
        self,
        region: Optional[str] = None,
        año: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Carga datos de titulados desde cache
        
        Args:
            region: Filtrar por región (opcional)
            año: Filtrar por año (opcional)
            
        Returns:
            DataFrame con datos de titulados
        """
        cache_file = self.cache_dir / 'cache_titulados.parquet'
        
        if not cache_file.exists():
            logger.error(f"❌ No existe archivo de cache: {cache_file}")
            return self._cargar_csv_respaldo('titulados_2023.csv')
        
        try:
            df = pd.read_parquet(cache_file)
            logger.info(f"✅ Titulados cargados: {len(df)} registros")
            
            # Aplicar filtros
            if region:
                df = df[df['Region'] == region]
            if año:
                df = df[df['Año'] == año]
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error cargando titulados: {e}")
            return pd.DataFrame()
    
    def _cargar_csv_respaldo(self, filename: str) -> pd.DataFrame:
        """
        Carga datos desde CSV de respaldo si el cache no está disponible
        """
        csv_path = Path('data/raw') / filename
        
        if csv_path.exists():
            logger.warning(f"⚠️  Cargando desde CSV de respaldo: {filename}")
            return pd.read_csv(csv_path)
        else:
            logger.error(f"❌ No se encuentra archivo de respaldo: {csv_path}")
            return pd.DataFrame()
    
    def get_estadisticas_cache(self) -> Dict:
        """
        Retorna estadísticas del cache actual
        """
        return {
            'ultima_actualizacion': self.get_ultima_actualizacion(),
            'dias_desde_actualizacion': self.get_dias_desde_actualizacion(),
            'registros_totales': self.metadata.get('registros_totales', 0),
            'fuentes_disponibles': len(self.metadata.get('fuentes_actualizadas', [])),
            'estado': 'actualizado' if self.get_dias_desde_actualizacion() and self.get_dias_desde_actualizacion() <= 7 else 'desactualizado'
        }


# Instancia global para usar en toda la app
data_loader = CacheDataLoader()


# Funciones de conveniencia para importar directamente
def get_establecimientos(region=None, comuna=None):
    """Carga establecimientos desde cache"""
    return data_loader.cargar_establecimientos(region, comuna)


def get_matricula(region=None, año=None, agregado=False):
    """Carga matrícula desde cache"""
    return data_loader.cargar_matricula(region, año, agregado)


def get_docentes(region=None, especialidad=None):
    """Carga docentes desde cache"""
    return data_loader.cargar_docentes(region, especialidad)


def get_titulados(region=None, año=None):
    """Carga titulados desde cache"""
    return data_loader.cargar_titulados(region, año)


def get_cache_stats():
    """Obtiene estadísticas del cache"""
    return data_loader.get_estadisticas_cache()
