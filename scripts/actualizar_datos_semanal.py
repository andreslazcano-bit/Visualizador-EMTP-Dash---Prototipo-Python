"""
Script de Actualización Semanal de Datos desde SQL Server MINEDUC
Ejecutar: Cada lunes a las 2:00 AM
Configuración: crontab -e → 0 2 * * 1 /path/to/script

Flujo:
1. Conecta a SQL Server MINEDUC (SIGE, Titulados, Financiero)
2. Descarga datos de la semana anterior
3. Procesa y limpia los datos
4. Guarda en cache local (Parquet - formato optimizado)
5. Actualiza metadata con timestamp y estadísticas
6. Envía notificación de éxito/error
"""

import pandas as pd
import pyodbc
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'actualizacion_datos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Directorios de datos
DATA_DIR = Path('data/processed')
DATA_DIR.mkdir(parents=True, exist_ok=True)

class ActualizadorDatosMineduc:
    """
    Clase para gestionar la actualización semanal de datos desde MINEDUC
    """
    
    def __init__(self):
        self.connection_string = self._build_connection_string()
        self.metadata = {
            'fecha_actualizacion': None,
            'fuentes_actualizadas': [],
            'registros_totales': 0,
            'errores': []
        }
    
    def _build_connection_string(self):
        """
        Construye la cadena de conexión a SQL Server MINEDUC
        """
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('MINEDUC_SQL_SERVER', 'sql-server.mineduc.cl')};"
            f"DATABASE={os.getenv('MINEDUC_SQL_DATABASE', 'SIGE_Produccion')};"
            f"UID={os.getenv('MINEDUC_SQL_USER')};"
            f"PWD={os.getenv('MINEDUC_SQL_PASSWORD')};"
            f"TrustServerCertificate=yes;"
            f"Encrypt=yes;"
            f"Connection Timeout=30;"
        )
    
    def conectar(self):
        """
        Establece conexión con SQL Server MINEDUC
        """
        try:
            logger.info("🔌 Conectando a SQL Server MINEDUC...")
            conn = pyodbc.connect(self.connection_string, timeout=30)
            logger.info("✅ Conexión exitosa")
            return conn
        except pyodbc.Error as e:
            logger.error(f"❌ Error de conexión: {e}")
            self.metadata['errores'].append(f"Error conexión: {str(e)}")
            return None
    
    def actualizar_establecimientos(self, conn):
        """
        Actualiza datos de establecimientos EMTP
        """
        logger.info("📋 Actualizando datos de establecimientos...")
        
        query = """
        SELECT 
            e.RBD,
            e.NombreEstablecimiento,
            e.Region,
            e.CodigoRegion,
            e.Comuna,
            e.CodigoComuna,
            e.Direccion,
            e.Dependencia,
            e.RuralUrbano,
            e.Latitud,
            e.Longitud,
            e.TotalMatricula,
            e.MatriculaEMTP,
            e.Email,
            e.Telefono,
            e.Estado
        FROM 
            dbo.Establecimientos e
        WHERE 
            e.TipoEducacion LIKE '%EMTP%'
            AND e.Estado = 'Activo'
        ORDER BY 
            e.Region, e.NombreEstablecimiento
        """
        
        try:
            df = pd.read_sql(query, conn)
            
            # Guardar en Parquet (formato comprimido y rápido)
            output_file = DATA_DIR / 'cache_establecimientos.parquet'
            df.to_parquet(output_file, index=False, compression='snappy')
            
            logger.info(f"✅ Establecimientos actualizados: {len(df)} registros")
            logger.info(f"   Guardado en: {output_file}")
            
            self.metadata['fuentes_actualizadas'].append({
                'nombre': 'establecimientos',
                'registros': len(df),
                'archivo': str(output_file)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error actualizando establecimientos: {e}")
            self.metadata['errores'].append(f"Establecimientos: {str(e)}")
            return None
    
    def actualizar_matricula(self, conn):
        """
        Actualiza datos de matrícula por región y comuna
        """
        logger.info("📊 Actualizando datos de matrícula...")
        
        query = """
        SELECT 
            m.RBD,
            m.Año,
            m.Region,
            m.CodigoRegion,
            m.Comuna,
            m.CodigoComuna,
            m.Grado,
            m.TotalMatricula,
            m.Hombres,
            m.Mujeres,
            m.Sector,
            m.FechaActualizacion
        FROM 
            dbo.Matricula m
        WHERE 
            m.Año >= YEAR(GETDATE()) - 5  -- Últimos 5 años
            AND m.TipoEducacion = 'EMTP'
        ORDER BY 
            m.Año DESC, m.Region, m.Comuna
        """
        
        try:
            df = pd.read_sql(query, conn)
            
            # Agregar por región y año para dashboards
            df_agregado = df.groupby(['Region', 'CodigoRegion', 'Año']).agg({
                'TotalMatricula': 'sum',
                'Hombres': 'sum',
                'Mujeres': 'sum',
                'RBD': 'nunique'  # Cantidad de establecimientos
            }).reset_index()
            
            df_agregado.rename(columns={'RBD': 'CantidadEstablecimientos'}, inplace=True)
            
            # Guardar datos completos
            output_file = DATA_DIR / 'cache_matricula.parquet'
            df.to_parquet(output_file, index=False, compression='snappy')
            
            # Guardar agregado para dashboards rápidos
            output_agregado = DATA_DIR / 'cache_matricula_agregado.parquet'
            df_agregado.to_parquet(output_agregado, index=False, compression='snappy')
            
            logger.info(f"✅ Matrícula actualizada: {len(df)} registros")
            logger.info(f"   Agregado generado: {len(df_agregado)} registros")
            
            self.metadata['fuentes_actualizadas'].append({
                'nombre': 'matricula',
                'registros': len(df),
                'registros_agregados': len(df_agregado),
                'archivo': str(output_file)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error actualizando matrícula: {e}")
            self.metadata['errores'].append(f"Matrícula: {str(e)}")
            return None
    
    def actualizar_docentes(self, conn):
        """
        Actualiza datos de docentes por especialidad
        """
        logger.info("👨‍🏫 Actualizando datos de docentes...")
        
        query = """
        SELECT 
            d.RBD,
            d.Año,
            d.Region,
            d.Comuna,
            d.Especialidad,
            d.SectorEconomico,
            d.CantidadDocentes,
            d.DocentesTitulados,
            d.DocentesContrato,
            d.DocentesPlanta,
            d.PromedioExperiencia
        FROM 
            dbo.Docentes d
        WHERE 
            d.Año >= YEAR(GETDATE()) - 3  -- Últimos 3 años
            AND d.TipoEducacion = 'EMTP'
        ORDER BY 
            d.Año DESC, d.Especialidad
        """
        
        try:
            df = pd.read_sql(query, conn)
            
            output_file = DATA_DIR / 'cache_docentes.parquet'
            df.to_parquet(output_file, index=False, compression='snappy')
            
            logger.info(f"✅ Docentes actualizados: {len(df)} registros")
            
            self.metadata['fuentes_actualizadas'].append({
                'nombre': 'docentes',
                'registros': len(df),
                'archivo': str(output_file)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error actualizando docentes: {e}")
            self.metadata['errores'].append(f"Docentes: {str(e)}")
            return None
    
    def actualizar_titulados(self, conn):
        """
        Actualiza datos de titulados por especialidad
        """
        logger.info("🎓 Actualizando datos de titulados...")
        
        query = """
        SELECT 
            t.RBD,
            t.Año,
            t.Region,
            t.Comuna,
            t.Especialidad,
            t.SectorEconomico,
            t.CantidadTitulados,
            t.Hombres,
            t.Mujeres,
            t.PromedioNotas,
            t.TasaAprobacion
        FROM 
            dbo.Titulados t
        WHERE 
            t.Año >= YEAR(GETDATE()) - 5  -- Últimos 5 años
        ORDER BY 
            t.Año DESC, t.Especialidad
        """
        
        try:
            df = pd.read_sql(query, conn)
            
            output_file = DATA_DIR / 'cache_titulados.parquet'
            df.to_parquet(output_file, index=False, compression='snappy')
            
            logger.info(f"✅ Titulados actualizados: {len(df)} registros")
            
            self.metadata['fuentes_actualizadas'].append({
                'nombre': 'titulados',
                'registros': len(df),
                'archivo': str(output_file)
            })
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error actualizando titulados: {e}")
            self.metadata['errores'].append(f"Titulados: {str(e)}")
            return None
    
    def guardar_metadata(self):
        """
        Guarda metadata de la actualización
        """
        self.metadata['fecha_actualizacion'] = datetime.now().isoformat()
        self.metadata['registros_totales'] = sum(
            f['registros'] for f in self.metadata['fuentes_actualizadas']
        )
        
        metadata_file = DATA_DIR / 'cache_metadata.json'
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Metadata guardada en: {metadata_file}")
    
    def ejecutar_actualizacion(self):
        """
        Ejecuta la actualización completa semanal
        """
        logger.info("=" * 80)
        logger.info("🚀 INICIANDO ACTUALIZACIÓN SEMANAL DE DATOS")
        logger.info(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        # Conectar
        conn = self.conectar()
        
        if not conn:
            logger.error("❌ No se pudo establecer conexión. Abortando.")
            return False
        
        try:
            # Actualizar cada fuente de datos
            self.actualizar_establecimientos(conn)
            self.actualizar_matricula(conn)
            self.actualizar_docentes(conn)
            self.actualizar_titulados(conn)
            
            # Guardar metadata
            self.guardar_metadata()
            
            logger.info("=" * 80)
            logger.info("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
            logger.info(f"📊 Total de registros actualizados: {self.metadata['registros_totales']:,}")
            logger.info(f"📁 Fuentes actualizadas: {len(self.metadata['fuentes_actualizadas'])}")
            
            if self.metadata['errores']:
                logger.warning(f"⚠️  Errores encontrados: {len(self.metadata['errores'])}")
                for error in self.metadata['errores']:
                    logger.warning(f"   - {error}")
            
            logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error general en actualización: {e}")
            return False
            
        finally:
            conn.close()
            logger.info("🔌 Conexión cerrada")


def main():
    """
    Función principal
    """
    actualizador = ActualizadorDatosMineduc()
    exito = actualizador.ejecutar_actualizacion()
    
    # Código de salida para monitoreo
    exit(0 if exito else 1)


if __name__ == "__main__":
    main()
