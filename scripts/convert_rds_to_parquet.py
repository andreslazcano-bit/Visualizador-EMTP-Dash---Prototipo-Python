"""
============================================================================
SCRIPT: Convertir archivos RDS a Parquet
============================================================================
Convierte archivos .rds de R a formato Parquet para uso en Python
"""

import sys
from pathlib import Path
from loguru import logger

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings

try:
    import pyreadr
    PYREADR_AVAILABLE = True
except ImportError:
    PYREADR_AVAILABLE = False
    logger.warning("pyreadr no está instalado. Instalar con: pip install pyreadr")


def convert_rds_to_parquet(rds_file: Path, output_file: Path = None):
    """
    Convierte un archivo RDS a Parquet
    
    Args:
        rds_file: Path al archivo RDS
        output_file: Path de salida (opcional)
    """
    if not PYREADR_AVAILABLE:
        logger.error("❌ pyreadr no está disponible")
        return
    
    try:
        logger.info(f"📖 Leyendo {rds_file.name}...")
        result = pyreadr.read_r(str(rds_file))
        
        # RDS contiene un solo objeto
        df = result[None] if None in result else list(result.values())[0]
        
        logger.info(f"✅ Leído: {len(df)} filas, {len(df.columns)} columnas")
        
        # Determinar nombre de salida
        if output_file is None:
            output_file = rds_file.with_suffix('.parquet')
        
        # Guardar como Parquet
        logger.info(f"💾 Guardando como {output_file.name}...")
        df.to_parquet(output_file, compression='snappy', index=False)
        
        logger.success(f"✅ Convertido exitosamente a {output_file}")
        
        # Mostrar info del tamaño
        original_size = rds_file.stat().st_size / 1024 / 1024
        parquet_size = output_file.stat().st_size / 1024 / 1024
        logger.info(f"📊 Tamaño original: {original_size:.2f} MB")
        logger.info(f"📊 Tamaño Parquet: {parquet_size:.2f} MB")
        logger.info(f"📊 Reducción: {((1 - parquet_size/original_size) * 100):.1f}%")
        
    except Exception as e:
        logger.error(f"❌ Error convirtiendo {rds_file.name}: {e}")


def convert_all_rds_in_directory(directory: Path):
    """
    Convierte todos los archivos RDS en un directorio
    
    Args:
        directory: Path al directorio
    """
    rds_files = list(directory.glob('*.rds'))
    
    if not rds_files:
        logger.warning(f"⚠️ No se encontraron archivos RDS en {directory}")
        return
    
    logger.info(f"📁 Encontrados {len(rds_files)} archivos RDS")
    
    for rds_file in rds_files:
        convert_rds_to_parquet(rds_file)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convierte archivos RDS de R a Parquet'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Archivo RDS o directorio con archivos RDS'
    )
    parser.add_argument(
        '-o', '--output',
        help='Archivo de salida (solo si input es un archivo)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convertir todos los RDS en data/processed'
    )
    
    args = parser.parse_args()
    
    if args.all:
        # Convertir todos en data/processed
        logger.info("🔄 Convirtiendo todos los archivos en data/processed")
        convert_all_rds_in_directory(settings.PROCESSED_DATA_DIR)
        
        logger.info("🔄 Convirtiendo todos los archivos en data/geographic")
        convert_all_rds_in_directory(settings.GEOGRAPHIC_DATA_DIR)
        
    elif args.input:
        input_path = Path(args.input)
        
        if input_path.is_dir():
            convert_all_rds_in_directory(input_path)
        elif input_path.is_file():
            output_path = Path(args.output) if args.output else None
            convert_rds_to_parquet(input_path, output_path)
        else:
            logger.error(f"❌ Ruta no válida: {input_path}")
    else:
        parser.print_help()
