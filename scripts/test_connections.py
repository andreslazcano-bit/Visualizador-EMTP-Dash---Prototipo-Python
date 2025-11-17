"""
Script de Prueba de Conexiones a MINEDUC
Verifica que las credenciales y conectividad sean correctas antes de la actualización automática
"""

import pyodbc
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

def test_sql_connection(name, server_var, database_var, user_var, password_var):
    """
    Prueba conexión a SQL Server
    """
    print(f"\n{'='*70}")
    print(f"🔌 Probando conexión: {name}")
    print(f"{'='*70}")
    
    server = os.getenv(server_var)
    database = os.getenv(database_var)
    user = os.getenv(user_var)
    password = os.getenv(password_var)
    
    print(f"  Servidor: {server}")
    print(f"  Base de Datos: {database}")
    print(f"  Usuario: {user}")
    print(f"  Password: {'*' * 8 if password else 'NO CONFIGURADO'}")
    
    if not all([server, database, user, password]):
        print(f"  ❌ Faltan credenciales en el archivo .env")
        return False
    
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes;"
        f"Connection Timeout=10;"
    )
    
    try:
        print(f"  🔄 Conectando...")
        conn = pyodbc.connect(connection_string, timeout=10)
        
        # Probar una consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print(f"  ✅ Conexión exitosa!")
        print(f"  📊 Versión SQL Server: {version.split('\\n')[0]}")
        
        conn.close()
        return True
        
    except pyodbc.Error as e:
        print(f"  ❌ Error de conexión:")
        print(f"     {str(e)}")
        return False


def main():
    """
    Ejecuta pruebas de conexión
    """
    print("\n" + "="*70)
    print("  🧪 TEST DE CONEXIONES A BASES DE DATOS MINEDUC")
    print("  Visualizador EMTP - Dash")
    print("="*70)
    
    # Verificar archivo .env
    if not Path('.env').exists():
        print("\n❌ ERROR: No se encuentra el archivo .env")
        print("   Crea el archivo .env basándote en .env.example.mineduc")
        sys.exit(1)
    
    resultados = []
    
    # Probar SQL Server - SIGE
    resultados.append(test_sql_connection(
        "SQL Server - SIGE",
        "MINEDUC_SQL_SERVER",
        "MINEDUC_SQL_DATABASE",
        "MINEDUC_SQL_USER",
        "MINEDUC_SQL_PASSWORD"
    ))
    
    # Resumen
    print("\n" + "="*70)
    print("  📋 RESUMEN DE PRUEBAS")
    print("="*70)
    
    exitosas = sum(resultados)
    total = len(resultados)
    
    print(f"\n  Conexiones exitosas: {exitosas}/{total}")
    
    if exitosas == total:
        print(f"\n  ✅ Todas las conexiones funcionan correctamente")
        print(f"  📝 Puedes ejecutar la actualización de datos con:")
        print(f"     python scripts/actualizar_datos_semanal.py")
        sys.exit(0)
    else:
        print(f"\n  ⚠️  Algunas conexiones fallaron")
        print(f"  📝 Verifica las credenciales en el archivo .env")
        print(f"  📝 Contacta a TI si el problema persiste")
        sys.exit(1)


if __name__ == "__main__":
    main()
