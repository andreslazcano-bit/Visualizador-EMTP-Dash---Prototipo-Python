"""
============================================================================
DATA PROCESSORS - Procesamiento y transformación de datos
============================================================================
Lógica de negocio para procesar datos EMTP
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
from loguru import logger


class DataProcessor:
    """Procesador de datos EMTP"""
    
    # ========================================================================
    # PROCESAMIENTO DE MATRÍCULA
    # ========================================================================
    
    @staticmethod
    def process_matricula(df: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa datos de matrícula
        
        Args:
            df: DataFrame crudo de matrícula
        
        Returns:
            DataFrame procesado
        """
        logger.info("🔄 Procesando datos de matrícula...")
        
        try:
            df_processed = df.copy()
            
            # Asegurar tipos de datos
            if 'rbd' in df_processed.columns:
                df_processed['rbd'] = df_processed['rbd'].astype(str)
            
            if 'cod_ense' in df_processed.columns:
                df_processed['cod_ense'] = pd.to_numeric(
                    df_processed['cod_ense'], 
                    errors='coerce'
                )
            
            if 'cod_grado' in df_processed.columns:
                df_processed['cod_grado'] = pd.to_numeric(
                    df_processed['cod_grado'], 
                    errors='coerce'
                )
            
            if 'gen_alu' in df_processed.columns:
                df_processed['gen_alu'] = pd.to_numeric(
                    df_processed['gen_alu'], 
                    errors='coerce'
                )
            
            # Filtrar solo EMTP (códigos 410-863)
            if 'cod_ense' in df_processed.columns:
                df_processed = df_processed[
                    (df_processed['cod_ense'] >= 410) & 
                    (df_processed['cod_ense'] <= 863)
                ]
            
            # Limpiar nombres de columnas
            df_processed.columns = df_processed.columns.str.strip().str.lower()
            
            logger.success(f"✅ Matrícula procesada: {len(df_processed)} registros")
            return df_processed
            
        except Exception as e:
            logger.error(f"❌ Error procesando matrícula: {e}")
            return df
    
    @staticmethod
    def process_docentes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa datos de docentes
        
        Args:
            df: DataFrame crudo de docentes
        
        Returns:
            DataFrame procesado
        """
        logger.info("🔄 Procesando datos de docentes...")
        
        try:
            df_processed = df.copy()
            
            # Asegurar tipos de datos
            if 'rbd' in df_processed.columns:
                df_processed['rbd'] = df_processed['rbd'].astype(str)
            
            if 'COD_ENS_1' in df_processed.columns:
                df_processed['COD_ENS_1'] = pd.to_numeric(
                    df_processed['COD_ENS_1'], 
                    errors='coerce'
                )
            
            if 'COD_ENS_2' in df_processed.columns:
                df_processed['COD_ENS_2'] = pd.to_numeric(
                    df_processed['COD_ENS_2'], 
                    errors='coerce'
                )
            
            # Clasificar población (Jóvenes/Adultos)
            df_processed['tiene_joven'] = (
                (~df_processed['COD_ENS_1'].isna() & (df_processed['COD_ENS_1'] % 100 == 10)) |
                (~df_processed['COD_ENS_2'].isna() & (df_processed['COD_ENS_2'] % 100 == 10))
            )
            
            df_processed['tiene_adulto'] = (
                (~df_processed['COD_ENS_1'].isna() & (df_processed['COD_ENS_1'] % 100 == 63)) |
                (~df_processed['COD_ENS_2'].isna() & (df_processed['COD_ENS_2'] % 100 == 63))
            )
            
            df_processed['Poblacion'] = np.where(
                df_processed['tiene_joven'] & df_processed['tiene_adulto'],
                'Ambas',
                np.where(
                    df_processed['tiene_joven'],
                    'Jóvenes',
                    np.where(
                        df_processed['tiene_adulto'],
                        'Adultos',
                        None
                    )
                )
            )
            
            # Filtrar solo EMTP
            df_processed = df_processed[
                ((df_processed['COD_ENS_1'] >= 410) & (df_processed['COD_ENS_1'] <= 863)) |
                ((df_processed['COD_ENS_2'] >= 410) & (df_processed['COD_ENS_2'] <= 863))
            ]
            
            # Limpiar columnas auxiliares
            df_processed = df_processed.drop(columns=['tiene_joven', 'tiene_adulto'], errors='ignore')
            
            logger.success(f"✅ Docentes procesados: {len(df_processed)} registros")
            return df_processed
            
        except Exception as e:
            logger.error(f"❌ Error procesando docentes: {e}")
            return df
    
    # ========================================================================
    # AGREGACIONES
    # ========================================================================
    
    @staticmethod
    def aggregate_by_region(df: pd.DataFrame, value_col: str = 'count') -> pd.DataFrame:
        """
        Agrega datos por región
        
        Args:
            df: DataFrame a agregar
            value_col: Columna con valores a sumar
        
        Returns:
            DataFrame agregado
        """
        try:
            if 'nom_reg_rbd_a' in df.columns:
                agg_df = df.groupby('nom_reg_rbd_a').agg({
                    value_col: 'sum' if value_col in df.columns else 'size'
                }).reset_index()
                
                agg_df.columns = ['region', 'total']
                return agg_df
            else:
                logger.warning("Columna 'nom_reg_rbd_a' no encontrada")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Error en agregación por región: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def aggregate_by_comuna(df: pd.DataFrame, value_col: str = 'count') -> pd.DataFrame:
        """
        Agrega datos por comuna
        
        Args:
            df: DataFrame a agregar
            value_col: Columna con valores a sumar
        
        Returns:
            DataFrame agregado
        """
        try:
            if 'nom_com_rbd' in df.columns:
                agg_df = df.groupby(['nom_com_rbd', 'cod_com_rbd']).agg({
                    value_col: 'sum' if value_col in df.columns else 'size'
                }).reset_index()
                
                agg_df.columns = ['comuna', 'cod_comuna', 'total']
                return agg_df
            else:
                logger.warning("Columna 'nom_com_rbd' no encontrada")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ Error en agregación por comuna: {e}")
            return pd.DataFrame()
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    @staticmethod
    def asignar_rft(deprov: str) -> str:
        """
        Asigna región de fomento técnico (RFT) según deprov
        
        Args:
            deprov: Nombre de la deprov
        
        Returns:
            Región RFT asignada
        """
        deprov = str(deprov).upper().strip()
        
        rft_mapping = {
            'Norte 1': ['ARICA', 'IQUIQUE'],
            'Norte 2': ['ANTOFAGASTA - TOCOPILLA', 'EL LOA', 'COPIAPÓ', 'HUASCO'],
            'Centro Norte': ['ELQUI', 'LIMARÍ', 'CHOAPA', 'QUILLOTA', 'SAN FELIPE', 
                            'VALPARAÍSO', 'SAN ANTONIO'],
            'Metropolitana Norte': ['SANTIAGO CENTRO', 'SANTIAGO NORTE', 
                                   'SANTIAGO PONIENTE', 'SANTIAGO ORIENTE'],
            'Metropolitana Sur': ['CORDILLERA', 'SANTIAGO SUR', 'TALAGANTE'],
            'Centro Sur': ['CACHAPOAL', 'COLCHAGUA', 'CARDENAL CARO', 'CURICÓ', 
                          'TALCA', 'LINARES', 'CAUQUENES'],
            'Sur 1': ['ÑUBLE', 'BIOBÍO', 'CONCEPCIÓN', 'ARAUCO'],
            'Sur 2': ['MALLECO', 'CAUTÍN NORTE', 'CAUTÍN SUR', 'VALDIVIA', 'RANCO'],
            'Sur 3': ['OSORNO', 'LLANQUIHUE', 'CHILOÉ', 'COYHAIQUE', 'MAGALLANES']
        }
        
        for rft, deprovs in rft_mapping.items():
            if deprov in deprovs:
                return rft
        
        return 'Sin Asignar'
    
    @staticmethod
    def get_especialidades_dict() -> Dict[int, str]:
        """
        Retorna diccionario de especialidades EMTP
        
        Returns:
            Dict con código: nombre de especialidad
        """
        return {
            41001: "Administración",
            41002: "Contabilidad",
            41003: "Secretariado",
            41004: "Ventas",
            51001: "Edificación",
            51002: "Terminaciones de Construcción",
            51003: "Montaje Industrial",
            51004: "Obras Viales y de Infraestructura",
            51005: "Instalaciones sanitarias",
            51006: "Refrigeración y climatización",
            52008: "Mecánica industrial",
            52009: "Construcciones metálicas",
            52010: "Mecánica",
            52011: "Matricería",
            52012: "Mecánica de mantención de aeronaves",
            53014: "Electricidad",
            53015: "Electrónica",
            53016: "Telecomunicaciones",
            54018: "Explotación minera",
            54019: "Metalurgia extractiva",
            54020: "Asistencia en geología",
            55022: "Gráfica",
            55023: "Dibujo técnico",
            56025: "Operación de planta química",
            56026: "Laboratorio químico",
            57028: "Tejido",
            57029: "Textil",
            57030: "Vestuario y confección textil",
            57031: "Productos del cuero",
            58033: "Conectividad y Redes",
            58034: "Programación",
            58035: "Telecomunicaciones (Redes)",
            61001: "Elaboración industrial de alimentos",
            61002: "Servicio de alimentación colectiva",
            62004: "Atención de párvulos",
            62005: "Atención de adultos mayores",
            62006: "Atención de enfermos",
            62007: "Atención social y recreativa",
            63009: "Servicio de Turismo",
            63010: "Servicio de Hotelería",
            71001: "Forestal",
            71002: "Procesamiento de la madera",
            71003: "Productos de la madera",
            71004: "Celulosa y papel",
            72006: "Agropecuaria",
            81001: "Naves mercantes y especiales",
            81002: "Pesquería",
            81003: "Acuicultura",
            81004: "Operación portuaria"
        }


# Instancia global del procesador
data_processor = DataProcessor()
