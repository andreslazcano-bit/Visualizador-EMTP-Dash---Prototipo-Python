"""
============================================================================
DATA VALIDATORS - Validación de datos
============================================================================
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from loguru import logger


class DataValidator:
    """Validador de calidad de datos"""
    
    @staticmethod
    def validate_matricula(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida estructura y calidad de datos de matrícula
        
        Args:
            df: DataFrame de matrícula
        
        Returns:
            Tuple (es_valido, lista_errores)
        """
        errors = []
        
        # Columnas requeridas
        required_cols = ['rbd', 'nom_rbd', 'cod_ense']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Columnas faltantes: {', '.join(missing_cols)}")
        
        # Validar que rbd no sea nulo
        if 'rbd' in df.columns and df['rbd'].isna().any():
            errors.append(f"RBD con valores nulos: {df['rbd'].isna().sum()}")
        
        # Validar rangos de cod_ense
        if 'cod_ense' in df.columns:
            invalid_ense = df[
                (df['cod_ense'] < 410) | (df['cod_ense'] > 863)
            ]
            if len(invalid_ense) > 0:
                errors.append(
                    f"Códigos de enseñanza fuera de rango EMTP: {len(invalid_ense)}"
                )
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.success("✅ Validación de matrícula exitosa")
        else:
            logger.warning(f"⚠️ Errores en validación de matrícula: {len(errors)}")
        
        return is_valid, errors
    
    @staticmethod
    def validate_docentes(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida estructura y calidad de datos de docentes
        
        Args:
            df: DataFrame de docentes
        
        Returns:
            Tuple (es_valido, lista_errores)
        """
        errors = []
        
        # Columnas requeridas
        required_cols = ['rbd', 'MRUN']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            errors.append(f"Columnas faltantes: {', '.join(missing_cols)}")
        
        # Validar duplicados
        if 'MRUN' in df.columns and 'rbd' in df.columns:
            duplicates = df.duplicated(subset=['MRUN', 'rbd'], keep=False)
            if duplicates.any():
                errors.append(
                    f"Registros duplicados (MRUN+RBD): {duplicates.sum()}"
                )
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.success("✅ Validación de docentes exitosa")
        else:
            logger.warning(f"⚠️ Errores en validación de docentes: {len(errors)}")
        
        return is_valid, errors
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera resumen de un DataFrame
        
        Args:
            df: DataFrame a resumir
        
        Returns:
            Dict con información del DataFrame
        """
        return {
            'n_rows': len(df),
            'n_cols': len(df.columns),
            'columns': list(df.columns),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'null_counts': df.isna().sum().to_dict(),
            'dtypes': df.dtypes.astype(str).to_dict()
        }


# Instancia global del validador
data_validator = DataValidator()
