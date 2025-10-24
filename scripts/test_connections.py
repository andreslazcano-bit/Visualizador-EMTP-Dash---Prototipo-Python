"""
============================================================================
SCRIPT: Verificar conexión a bases de datos
============================================================================
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import db_manager
from config.settings import settings
from loguru import logger


def test_all_connections():
    """Prueba todas las conexiones configuradas"""
    
    logger.info("=" * 60)
    logger.info("PRUEBA DE CONEXIONES A BASES DE DATOS")
    logger.info("=" * 60)
    
    results = {}
    
    # SQL Server
    if settings.SQL_SERVER_ENABLED:
        logger.info("\n📊 Probando SQL Server...")
        try:
            success = db_manager.test_connection('sql_server')
            results['SQL Server'] = success
            
            if success:
                logger.success("✅ SQL Server: Conexión exitosa")
            else:
                logger.error("❌ SQL Server: Conexión fallida")
        except Exception as e:
            logger.error(f"❌ SQL Server: Error - {e}")
            results['SQL Server'] = False
    else:
        logger.info("⏭️  SQL Server: No habilitado")
        results['SQL Server'] = None
    
    # PostgreSQL
    if settings.POSTGRES_ENABLED:
        logger.info("\n🐘 Probando PostgreSQL...")
        try:
            success = db_manager.test_connection('postgres')
            results['PostgreSQL'] = success
            
            if success:
                logger.success("✅ PostgreSQL: Conexión exitosa")
            else:
                logger.error("❌ PostgreSQL: Conexión fallida")
        except Exception as e:
            logger.error(f"❌ PostgreSQL: Error - {e}")
            results['PostgreSQL'] = False
    else:
        logger.info("⏭️  PostgreSQL: No habilitado")
        results['PostgreSQL'] = None
    
    # Resumen
    logger.info("\n" + "=" * 60)
    logger.info("RESUMEN")
    logger.info("=" * 60)
    
    for db_name, status in results.items():
        if status is None:
            logger.info(f"{db_name}: No configurado")
        elif status:
            logger.success(f"{db_name}: ✅ OK")
        else:
            logger.error(f"{db_name}: ❌ FALLO")
    
    logger.info("=" * 60)


if __name__ == '__main__':
    test_all_connections()
