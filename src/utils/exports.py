"""
============================================================================
UTILIDADES DE EXPORTACIÓN
============================================================================
Exporta datos a múltiples formatos: CSV, Excel, JSON, PDF
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union, List
from datetime import datetime
from loguru import logger
import io

from config.settings import settings


class ExportManager:
    """Gestor de exportación de datos"""
    
    @staticmethod
    def export_to_csv(
        df: pd.DataFrame,
        filename: Optional[str] = None,
        return_bytes: bool = False
    ) -> Optional[Union[Path, bytes]]:
        """
        Exporta DataFrame a CSV
        
        Args:
            df: DataFrame a exportar
            filename: Nombre del archivo (opcional)
            return_bytes: Si True, retorna bytes en vez de guardar
        
        Returns:
            Path al archivo guardado o bytes
        """
        try:
            if return_bytes:
                buffer = io.StringIO()
                df.to_csv(buffer, index=False, encoding='utf-8')
                return buffer.getvalue().encode('utf-8')
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'export_{timestamp}.csv'
            
            output_path = settings.REPORTS_OUTPUT_DIR / filename
            df.to_csv(output_path, index=False, encoding='utf-8')
            
            logger.success(f"✅ Exportado a CSV: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando a CSV: {e}")
            return None
    
    @staticmethod
    def export_to_excel(
        df: pd.DataFrame,
        filename: Optional[str] = None,
        sheet_name: str = 'Datos',
        return_bytes: bool = False
    ) -> Optional[Union[Path, bytes]]:
        """
        Exporta DataFrame a Excel
        
        Args:
            df: DataFrame a exportar
            filename: Nombre del archivo (opcional)
            sheet_name: Nombre de la hoja
            return_bytes: Si True, retorna bytes en vez de guardar
        
        Returns:
            Path al archivo guardado o bytes
        """
        try:
            if return_bytes:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                return buffer.getvalue()
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'export_{timestamp}.xlsx'
            
            output_path = settings.REPORTS_OUTPUT_DIR / filename
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.success(f"✅ Exportado a Excel: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando a Excel: {e}")
            return None
    
    @staticmethod
    def export_to_json(
        df: pd.DataFrame,
        filename: Optional[str] = None,
        orient: str = 'records',
        return_bytes: bool = False
    ) -> Optional[Union[Path, bytes, str]]:
        """
        Exporta DataFrame a JSON
        
        Args:
            df: DataFrame a exportar
            filename: Nombre del archivo (opcional)
            orient: Formato del JSON
            return_bytes: Si True, retorna string en vez de guardar
        
        Returns:
            Path al archivo guardado o string JSON
        """
        try:
            json_str = df.to_json(orient=orient, force_ascii=False, indent=2)
            
            if return_bytes:
                return json_str
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'export_{timestamp}.json'
            
            output_path = settings.REPORTS_OUTPUT_DIR / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            logger.success(f"✅ Exportado a JSON: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando a JSON: {e}")
            return None
    
    @staticmethod
    def export_multiple_sheets(
        dataframes: dict,
        filename: Optional[str] = None
    ) -> Optional[Path]:
        """
        Exporta múltiples DataFrames a un Excel con varias hojas
        
        Args:
            dataframes: Dict con {nombre_hoja: DataFrame}
            filename: Nombre del archivo
        
        Returns:
            Path al archivo guardado
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'export_multiple_{timestamp}.xlsx'
            
            output_path = settings.REPORTS_OUTPUT_DIR / filename
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, df in dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.success(f"✅ Exportado múltiples hojas: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando múltiples hojas: {e}")
            return None


# Instancia global
export_manager = ExportManager()
