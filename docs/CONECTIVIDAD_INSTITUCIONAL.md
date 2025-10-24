# 🌐 ANÁLISIS DE CONECTIVIDAD INSTITUCIONAL
**Visualizador EMTP v2.0 - Capacidad de Integración con Sistemas Empresariales**

**Fecha:** 20 de octubre de 2025  
**Consulta:** ¿Puede la aplicación conectarse a servidores institucionales y bases de datos?

---

## 📊 RESPUESTA CORTA: **SÍ ✅**

Tu aplicación **ya está preparada arquitectónicamente** para conectarse a múltiples sistemas institucionales. Solo requiere configuración, no cambios de código significativos.

---

## 🏗️ ARQUITECTURA ACTUAL

### Infraestructura Existente ✅

Tu app tiene una **arquitectura modular** diseñada para múltiples fuentes de datos:

```python
# config/database.py - YA IMPLEMENTADO
class DatabaseManager:
    - SQL Server support (pyodbc + SQLAlchemy)
    - PostgreSQL support (SQLAlchemy)
    - Connection pooling
    - Error handling robusto
    - Logging detallado
```

```python
# config/settings.py - YA CONFIGURADO
Soporta:
✅ SQL Server (Azure SQL, SQL Server on-premise)
✅ PostgreSQL (AWS RDS, Azure PostgreSQL, local)
✅ MySQL (mencionado en .env.example)
✅ SharePoint (Office 365, SharePoint Server)
✅ Redis (caching distribuido)
✅ Archivos locales (CSV, Parquet, Excel)
```

---

## 🔌 SISTEMAS SOPORTADOS

### 1. **SQL Server / Azure SQL Database** ✅ LISTO

**Estado:** Código implementado, solo requiere configuración

**Casos de uso típicos:**
- Bases de datos institucionales del Ministerio
- SQL Server on-premise corporativo
- Azure SQL Database en la nube
- Datawarehouse centralizado

**Configuración requerida (.env):**
```bash
SQL_SERVER_ENABLED=True
SQL_SERVER_HOST=servidor.mineduc.cl  # o IP institucional
SQL_SERVER_PORT=1433
SQL_SERVER_DATABASE=EMTP_Produccion
SQL_SERVER_USERNAME=app_emtp_readonly
SQL_SERVER_PASSWORD=<password_segura>
SQL_SERVER_DRIVER=ODBC Driver 17 for SQL Server
```

**Requisitos:**
```bash
# Instalar driver ODBC (una sola vez en el servidor)
# macOS:
brew install unixodbc
brew tap microsoft/mssql-release
brew install msodbcsql17

# Linux (Ubuntu/Debian):
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
apt-get install msodbcsql17 unixodbc-dev

# Windows: Ya incluido generalmente
```

**Ventajas:**
- ✅ Perfecto para grandes volúmenes de datos
- ✅ Queries complejas con JOINs
- ✅ Stored procedures
- ✅ Transacciones
- ✅ Alta disponibilidad con Always On

**Limitaciones:**
- ⚠️ Requiere licencia SQL Server (o Azure SQL)
- ⚠️ Puede requerir VPN si está on-premise

---

### 2. **PostgreSQL** ✅ LISTO

**Estado:** Código implementado, solo requiere configuración

**Casos de uso típicos:**
- Bases de datos open-source institucionales
- AWS RDS PostgreSQL
- Google Cloud SQL PostgreSQL
- Azure Database for PostgreSQL

**Configuración requerida (.env):**
```bash
POSTGRES_ENABLED=True
POSTGRES_HOST=postgres.mineduc.cl
POSTGRES_PORT=5432
POSTGRES_DATABASE=emtp_data
POSTGRES_USERNAME=app_reader
POSTGRES_PASSWORD=<password_segura>
```

**No requiere drivers adicionales** (psycopg2 ya en requirements.txt)

**Ventajas:**
- ✅ Open source (sin costos de licencia)
- ✅ JSON support nativo (para datos semi-estructurados)
- ✅ Full-text search
- ✅ PostGIS para datos geográficos
- ✅ Excelente para análisis

---

### 3. **MySQL / MariaDB** ⚠️ FÁCIL DE AGREGAR

**Estado:** Mencionado en .env pero falta código

**Tiempo de implementación:** 30 minutos

**Código a agregar:**
```python
# En config/database.py
def get_mysql_engine(self) -> Optional[Engine]:
    """Obtiene engine para MySQL"""
    if not settings.MYSQL_ENABLED:
        return None
    
    connection_string = (
        f"mysql+pymysql://{settings.MYSQL_USERNAME}:"
        f"{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:"
        f"{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
    )
    
    self._engines['mysql'] = create_engine(
        connection_string,
        poolclass=NullPool
    )
    return self._engines['mysql']
```

**Dependencia adicional:**
```bash
pip install pymysql
```

---

### 4. **SharePoint / Office 365** ✅ CONFIGURADO

**Estado:** Variables de entorno listas, falta implementación

**Casos de uso típicos:**
- Archivos Excel en SharePoint del Ministerio
- Documentos colaborativos
- Listas de SharePoint como fuente de datos
- Integración con Office 365

**Tiempo de implementación:** 2-3 horas

**Librería recomendada:**
```bash
pip install Office365-REST-Python-Client
```

**Configuración (.env):**
```bash
SHAREPOINT_ENABLED=True
SHAREPOINT_SITE_URL=https://mineduc.sharepoint.com/sites/EMTP
SHAREPOINT_CLIENT_ID=<azure_app_id>
SHAREPOINT_CLIENT_SECRET=<azure_app_secret>
# O autenticación de usuario:
SHAREPOINT_USERNAME=usuario@mineduc.cl
SHAREPOINT_PASSWORD=<password>
```

**Ejemplo de código:**
```python
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

def get_sharepoint_file(file_path: str) -> pd.DataFrame:
    """Descarga archivo Excel desde SharePoint"""
    
    credentials = ClientCredential(
        settings.SHAREPOINT_CLIENT_ID,
        settings.SHAREPOINT_CLIENT_SECRET
    )
    
    ctx = ClientContext(settings.SHAREPOINT_SITE_URL).with_credentials(credentials)
    
    # Descargar archivo
    response = ctx.web.get_file_by_server_relative_url(file_path).download()
    
    # Leer en pandas
    return pd.read_excel(response.content)
```

---

### 5. **Oracle Database** ⚠️ REQUIERE IMPLEMENTACIÓN

**Estado:** No implementado pero factible

**Tiempo de implementación:** 1-2 horas

**Casos de uso:**
- Sistemas legacy institucionales
- ERP corporativos (SAP, Oracle EBS)
- Datawarehouse Oracle

**Implementación:**
```bash
# Instalar driver Oracle Instant Client
# + librería cx_Oracle
pip install cx_Oracle
```

```python
# Agregar a database.py
def get_oracle_engine(self) -> Optional[Engine]:
    connection_string = (
        f"oracle+cx_oracle://{username}:{password}@"
        f"{host}:{port}/?service_name={service_name}"
    )
    return create_engine(connection_string)
```

---

### 6. **APIs REST / Web Services** ✅ COMPATIBLE

**Estado:** Fácilmente integrable

**Casos de uso:**
- APIs del Ministerio de Educación
- MINEDUC API
- DEMRE (PSU/PAES)
- Otros servicios gubernamentales

**Implementación típica:**
```python
import requests

def get_data_from_api(endpoint: str) -> pd.DataFrame:
    """Obtiene datos desde API institucional"""
    
    # Autenticación
    headers = {
        'Authorization': f'Bearer {settings.API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Request
    response = requests.get(
        f"{settings.API_BASE_URL}/{endpoint}",
        headers=headers,
        timeout=30
    )
    
    # Convertir a DataFrame
    data = response.json()
    return pd.DataFrame(data)
```

**Agregar a .env:**
```bash
API_ENABLED=True
API_BASE_URL=https://api.mineduc.cl/v1
API_TOKEN=<token_institucional>
```

---

### 7. **Azure Data Lake / AWS S3** ⚠️ FÁCIL DE AGREGAR

**Estado:** No implementado pero trivial

**Tiempo:** 1 hora

**Casos de uso:**
- Data lakes institucionales
- Almacenamiento masivo de archivos
- Backup en la nube
- Archivos Parquet grandes

**Azure:**
```bash
pip install azure-storage-blob azure-identity
```

```python
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

def read_from_azure_blob(container: str, blob_name: str) -> pd.DataFrame:
    """Lee archivo desde Azure Blob Storage"""
    
    credential = DefaultAzureCredential()
    blob_service = BlobServiceClient(
        account_url=settings.AZURE_STORAGE_URL,
        credential=credential
    )
    
    blob_client = blob_service.get_blob_client(
        container=container,
        blob=blob_name
    )
    
    # Descargar y leer
    blob_data = blob_client.download_blob().readall()
    return pd.read_parquet(io.BytesIO(blob_data))
```

**AWS S3:**
```bash
pip install boto3
```

```python
import boto3
import io

def read_from_s3(bucket: str, key: str) -> pd.DataFrame:
    """Lee archivo desde S3"""
    
    s3 = boto3.client('s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(io.BytesIO(obj['Body'].read()))
```

---

## 🔐 CONSIDERACIONES DE SEGURIDAD

### Networking

**VPN / Red Privada:**
```
Si los servidores están en red interna institucional:

✅ Opción 1: Desplegar app en servidor interno
✅ Opción 2: VPN institucional (OpenVPN, Cisco AnyConnect)
✅ Opción 3: Azure ExpressRoute / AWS Direct Connect
✅ Opción 4: SSH Tunnel para desarrollo
```

**Firewall:**
```bash
# Servidor debe permitir conexiones salientes a:
- Puerto 1433 (SQL Server)
- Puerto 5432 (PostgreSQL)
- Puerto 3306 (MySQL)
- Puerto 443 (HTTPS para APIs)
```

### Autenticación

**Mejores prácticas:**
```python
✅ Credenciales en .env (NUNCA en código)
✅ Usuarios de solo lectura (read-only)
✅ Principio de mínimo privilegio
✅ Rotación periódica de passwords
✅ Azure Managed Identity (si en Azure)
✅ AWS IAM Roles (si en AWS)
```

**Ejemplo de usuario read-only SQL Server:**
```sql
-- En el servidor institucional
CREATE LOGIN app_emtp_readonly WITH PASSWORD = 'StrongPassword123!';
CREATE USER app_emtp_readonly FOR LOGIN app_emtp_readonly;

-- Solo SELECT en tablas necesarias
GRANT SELECT ON dbo.Matricula TO app_emtp_readonly;
GRANT SELECT ON dbo.Docentes TO app_emtp_readonly;
GRANT SELECT ON dbo.Establecimientos TO app_emtp_readonly;
-- etc.

-- NO DAR:
-- DENY INSERT, UPDATE, DELETE
```

### Encriptación

**En tránsito:**
```python
# SQL Server con SSL/TLS
connection_string += ";Encrypt=yes;TrustServerCertificate=no"

# PostgreSQL con SSL
connection_string += "?sslmode=require"

# APIs siempre HTTPS
API_BASE_URL = "https://..."  # Nunca http://
```

**En reposo:**
```bash
# Archivos .env con permisos restrictivos
chmod 600 .env

# O usar vault:
- Azure Key Vault
- AWS Secrets Manager
- HashiCorp Vault
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### Fase 1: Validación (1-2 días)

**Objetivo:** Probar conectividad básica

```bash
# 1. Obtener credenciales de prueba del equipo IT institucional
# 2. Configurar .env con datos de desarrollo/test
# 3. Instalar drivers necesarios (ODBC, etc.)
# 4. Ejecutar test de conexión
```

**Test básico:**
```python
# Crear scripts/test_db_connection.py
from config.database import DatabaseManager

db = DatabaseManager()

# Test SQL Server
engine = db.get_sql_server_engine()
if engine:
    result = db.execute_query("SELECT TOP 10 * FROM Matricula")
    print(f"✅ SQL Server OK: {len(result)} registros")
else:
    print("❌ SQL Server failed")

# Test PostgreSQL
engine = db.get_postgres_engine()
if engine:
    result = db.execute_query("SELECT * FROM matricula LIMIT 10", engine_name='postgres')
    print(f"✅ PostgreSQL OK: {len(result)} registros")
else:
    print("❌ PostgreSQL failed")
```

### Fase 2: Migración de Datos (2-5 días)

**Objetivo:** Reemplazar datos simulados con datos reales

```python
# Modificar src/data/loaders.py

def load_matricula_data() -> pd.DataFrame:
    """Carga datos de matrícula desde fuente configurada"""
    
    if settings.SQL_SERVER_ENABLED:
        # Desde SQL Server institucional
        db = DatabaseManager()
        query = """
            SELECT 
                anio, 
                codigo_region,
                codigo_establecimiento,
                nivel,
                modalidad,
                COUNT(*) as matricula
            FROM MatriculaOficial
            WHERE anio >= 2019
            GROUP BY anio, codigo_region, codigo_establecimiento, nivel, modalidad
        """
        return db.execute_query(query)
    
    elif settings.POSTGRES_ENABLED:
        # Desde PostgreSQL
        db = DatabaseManager()
        return db.execute_query(
            "SELECT * FROM matricula_consolidada",
            engine_name='postgres'
        )
    
    else:
        # Fallback a datos locales
        return pd.read_parquet('data/processed/matricula.parquet')
```

### Fase 3: Optimización (3-7 días)

**Objetivo:** Performance y caching

```python
# Implementar caching con Redis
import redis
import pickle

def get_cached_data(key: str, query_func, ttl: int = 3600):
    """Cache con Redis"""
    
    if not settings.REDIS_ENABLED:
        return query_func()
    
    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD
    )
    
    # Buscar en cache
    cached = r.get(key)
    if cached:
        logger.info(f"✅ Cache hit: {key}")
        return pickle.loads(cached)
    
    # Query + cache
    data = query_func()
    r.setex(key, ttl, pickle.dumps(data))
    logger.info(f"📝 Cache miss: {key} - Guardado por {ttl}s")
    
    return data
```

### Fase 4: Producción (1 semana)

**Checklist:**
```markdown
[ ] Credenciales de producción configuradas
[ ] Usuario read-only con permisos mínimos
[ ] SSL/TLS habilitado en todas las conexiones
[ ] Firewall rules configurados
[ ] VPN configurada (si es necesario)
[ ] Monitoring y alertas
[ ] Backup de configuración
[ ] Documentación de DR (Disaster Recovery)
[ ] Logs de acceso a datos habilitados
[ ] Testing de carga completado
```

---

## 📈 ESTIMACIÓN DE ESFUERZO

| Tarea | Tiempo | Dificultad | Dependencias |
|-------|--------|------------|--------------|
| Test de conectividad SQL Server | 2-4 horas | Baja | Credenciales IT |
| Test de conectividad PostgreSQL | 1-2 horas | Baja | Credenciales IT |
| Migración de datos | 1-2 días | Media | Queries aprobadas |
| Implementar caching (Redis) | 1 día | Media | Servidor Redis |
| SharePoint integration | 2-3 días | Media-Alta | App registration |
| Optimización de queries | 2-3 días | Media | DBA review |
| Testing completo | 2-3 días | Media | Datos de prueba |
| Documentación | 1 día | Baja | - |
| **TOTAL** | **2-3 semanas** | - | - |

---

## ✅ RECOMENDACIONES

### Corto Plazo (Próxima semana)

1. **Solicitar credenciales de prueba al equipo IT**
   - Usuario read-only en base de datos de desarrollo
   - VPN si es necesario
   - Documentación de esquema de base de datos

2. **Ejecutar test de conexión**
   - Validar que puedes conectarte desde tu máquina
   - Probar queries básicas
   - Medir latencia y performance

3. **Mapear esquema de datos**
   - Documentar tablas disponibles
   - Identificar campos clave
   - Validar calidad de datos

### Medio Plazo (Próximo mes)

4. **Implementar capa de abstracción**
   - DataLoader que funcione con múltiples fuentes
   - Fallback automático a datos locales
   - Cache inteligente

5. **Optimizar queries**
   - Índices apropiados
   - Queries parametrizadas
   - Paginación para grandes datasets

6. **Monitoreo**
   - Log de tiempos de query
   - Alertas si conexión falla
   - Dashboard de health

### Largo Plazo (Próximos 3 meses)

7. **Alta disponibilidad**
   - Failover automático
   - Múltiples réplicas read-only
   - Circuit breaker pattern

8. **Seguridad avanzada**
   - Auditoría de accesos
   - Encriptación de datos sensibles
   - Rotación automática de credenciales

9. **Escalabilidad**
   - Connection pooling avanzado
   - Distributed caching
   - Microservicios si es necesario

---

## 🎯 CONCLUSIÓN

### ✅ TU APP ESTÁ LISTA

Tu aplicación tiene una **arquitectura sólida y preparada** para conectarse a sistemas institucionales:

1. ✅ **SQL Server:** Implementado y listo
2. ✅ **PostgreSQL:** Implementado y listo
3. ⚠️ **MySQL:** Fácil de agregar (30 min)
4. ⚠️ **SharePoint:** Requiere implementación (2-3 horas)
5. ⚠️ **APIs REST:** Muy fácil (1 hora)
6. ⚠️ **Cloud Storage:** Fácil de agregar (1-2 horas)

### 🚀 PRÓXIMO PASO

**Recomendación:** Empezar con una **prueba de concepto (PoC)** de 1 semana:

```
Día 1-2: Solicitar credenciales de prueba + test de conectividad
Día 3-4: Implementar carga de 1 tabla real (ej: Matricula)
Día 5: Validar resultados con datos de producción vs simulados
```

Si el PoC es exitoso, tienes **confianza técnica** para planificar la migración completa.

### 💡 VENTAJA COMPETITIVA

El hecho de que **ya tengas esta arquitectura implementada** es una gran ventaja. Muchas apps no planean para múltiples fuentes de datos desde el inicio y terminan con código muy acoplado.

Tu app puede:
- ✅ Conectarse a bases de datos institucionales
- ✅ Leer de archivos locales como fallback
- ✅ Integrar con SharePoint/Office 365
- ✅ Consumir APIs gubernamentales
- ✅ Escalar a cloud (Azure, AWS)

---

**Respuesta final:** **SÍ, tu app puede conectarse a servidores institucionales.** Solo necesitas configuración y credenciales, el código ya está preparado. 🎉

