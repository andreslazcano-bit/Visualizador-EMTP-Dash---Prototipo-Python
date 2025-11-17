# Actualización Automática de Datos SIGE - Tema Pendiente

**Estado:** ⚠️ PENDIENTE DE DEFINIR  
**Responsables:** Jefatura EMTP + TI MINEDUC  
**Criticidad:** 🔴 Alta  
**Fecha Documento:** 17 de Noviembre 2025

---

## Resumen Ejecutivo

El sistema **Visualizador EMTP v2.0** está completamente funcional para visualización de datos, pero **requiere definición de estrategia** para actualización automática de datos desde fuentes del MINEDUC.

### Estado Actual

```
✅ Aplicación funcional
✅ SQLite para usuarios del sistema
✅ Procesamiento de datos CSV/Parquet
❌ Conexión automática a fuentes MINEDUC (NO IMPLEMENTADO)
```

---

## Aclaración Importante: SQLite

### ¿Para qué se usa SQLite en este proyecto?

SQLite (`data/users.db`) se utiliza **ÚNICAMENTE** para:

- ✅ Gestión de usuarios del sistema (admin, analista, usuario)
- ✅ Almacenamiento de credenciales encriptadas
- ✅ Control de permisos y roles
- ✅ Log de sesiones (parte de auditoría)

**Total usuarios esperados:** < 100 (máximo)  
**Tamaño esperado:** < 1 MB

### ¿Para qué NO se usa SQLite?

❌ **NO** para datos SIGE del MINEDUC (matrícula, egresados, etc.)  
❌ **NO** para datos históricos masivos  
❌ **NO** para datos geográficos  
❌ **NO** como fuente de dashboards

### ¿Dónde están los datos SIGE?

Los datos SIGE están en **archivos CSV/Parquet**:

```
data/
├── users.db                    ← SQLite (solo usuarios app)
│
└── processed/                  ← CSV/Parquet (datos SIGE)
    ├── matricula_completa.csv
    ├── egresados.csv
    ├── titulacion.csv
    ├── establecimientos.csv
    ├── docentes.csv
    └── proyectos.csv
```

---

## Situación Actual de Datos

### Flujo Actual (Manual)

```
1. [Portal MINEDUC] 
       ↓ (Descarga manual)
2. [TI descarga CSVs]
       ↓ (Copia manual)
3. [data/raw/]
       ↓ (Script automático)
4. [data/processed/]
       ↓ (Lectura automática)
5. [Dashboards actualizados]
```

**Frecuencia actual:** Semanal (lunes 6:00 AM)  
**Problema:** Paso 1-3 es **manual**, propenso a errores/olvidos

### Script de Actualización Actual

```python
# scripts/actualizar_datos_semanal.py

def actualizar():
    """
    Procesa archivos CSV en data/raw/
    Los limpia, valida y mueve a data/processed/
    """
    archivos_nuevos = glob.glob('data/raw/*.csv')
    
    for archivo in archivos_nuevos:
        # Limpiar datos
        df = limpiar_datos(archivo)
        
        # Validar estructura
        if validar_estructura(df):
            # Guardar procesado
            guardar_procesado(df)
            
            # Mover a histórico
            mover_a_historico(archivo)
        else:
            log_error(f"Estructura inválida: {archivo}")
```

**Limitación:** Espera que archivos estén en `data/raw/`

---

## Opciones para Actualización Automática

### Opción 1: Manual (Actual - Temporal)

**Descripción:** TI descarga y coloca archivos manualmente

**Proceso:**
```bash
# Cada lunes a las 6 AM (cron ejecuta script)
# Pero antes TI debe:
1. Ingresar a portal MINEDUC
2. Descargar CSVs de la semana
3. Copiarlos a data/raw/ del servidor
4. Script automático los procesa
```

**Ventajas:**
- ✅ No requiere coordinación con TI MINEDUC
- ✅ Control total sobre los datos
- ✅ Funciona sin credenciales externas

**Desventajas:**
- ❌ Requiere intervención manual cada semana
- ❌ Propenso a olvidos
- ❌ No escalable
- ❌ Depende de disponibilidad humana

**Recomendación:** Solo como solución temporal inicial

---

### Opción 2: SharePoint/OneDrive MINEDUC (RECOMENDADA)

**Descripción:** Sincronización automática desde SharePoint institucional

**Requisitos:**
- Carpeta SharePoint del MINEDUC con datos actualizados
- Credenciales de servicio (no usuario personal)
- Biblioteca `office365-rest-python-client`

**Implementación:**

```python
# scripts/actualizar_desde_sharepoint.py
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

def descargar_desde_sharepoint():
    # Configuración
    site_url = "https://mineduc.sharepoint.com/sites/datos-sige"
    client_id = os.getenv('SHAREPOINT_CLIENT_ID')
    client_secret = os.getenv('SHAREPOINT_CLIENT_SECRET')
    
    # Autenticación
    credentials = ClientCredential(client_id, client_secret)
    ctx = ClientContext(site_url).with_credentials(credentials)
    
    # Descargar archivos
    archivos = [
        '/Datos/Matricula/matricula_2025.csv',
        '/Datos/Egresados/egresados_2025.csv',
        '/Datos/Titulacion/titulacion_2025.csv',
    ]
    
    for archivo_remoto in archivos:
        archivo_local = f"data/raw/{os.path.basename(archivo_remoto)}"
        
        file = ctx.web.get_file_by_server_relative_url(archivo_remoto)
        with open(archivo_local, 'wb') as local_file:
            file.download(local_file)
        
        print(f"✓ Descargado: {archivo_remoto}")
    
    # Procesar archivos descargados
    actualizar_datos()
```

**Ventajas:**
- ✅ Completamente automático
- ✅ Institucional y respaldado por MINEDUC
- ✅ Fácil de mantener
- ✅ Logs claros de éxito/error

**Desventajas:**
- ⚠️ Requiere coordinación con TI MINEDUC
- ⚠️ Necesita credenciales de servicio (no personales)
- ⚠️ Depende de que MINEDUC mantenga SharePoint actualizado

**Pasos para Implementar:**
1. Reunión con TI MINEDUC
2. Identificar carpeta SharePoint con datos
3. Solicitar credenciales de servicio (Service Principal)
4. Instalar biblioteca: `pip install Office365-REST-Python-Client`
5. Configurar variables de entorno con credenciales
6. Probar descarga manual
7. Activar cron job automático

---

### Opción 3: SFTP/FTP del MINEDUC

**Descripción:** Descarga automática desde servidor FTP

**Requisitos:**
- Servidor SFTP/FTP del MINEDUC
- Credenciales de acceso
- Biblioteca `paramiko`

**Implementación:**

```python
# scripts/actualizar_desde_ftp.py
import paramiko
import os

def descargar_desde_ftp():
    # Configuración
    hostname = os.getenv('FTP_HOST')  # ftp.mineduc.cl
    username = os.getenv('FTP_USER')
    password = os.getenv('FTP_PASS')
    port = 22
    
    # Conexión
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    
    sftp = ssh.open_sftp()
    
    # Descargar archivos
    archivos_remotos = {
        '/datos/sige/matricula_2025.csv': 'data/raw/matricula_2025.csv',
        '/datos/sige/egresados_2025.csv': 'data/raw/egresados_2025.csv',
    }
    
    for remoto, local in archivos_remotos.items():
        sftp.get(remoto, local)
        print(f"✓ Descargado: {remoto}")
    
    sftp.close()
    ssh.close()
    
    # Procesar
    actualizar_datos()
```

**Ventajas:**
- ✅ Estándar y confiable
- ✅ Protocolo seguro (SFTP)
- ✅ Fácil de monitorear

**Desventajas:**
- ⚠️ Requiere que MINEDUC tenga servidor FTP
- ⚠️ Necesita credenciales
- ⚠️ Menos común que SharePoint en instituciones públicas

---

### Opción 4: API REST del MINEDUC

**Descripción:** Consulta directa a API del MINEDUC

**Requisitos:**
- API REST del MINEDUC (probablemente no existe)
- API Key
- Documentación de endpoints

**Implementación (hipotética):**

```python
# scripts/actualizar_desde_api.py
import requests
import pandas as pd

def obtener_desde_api():
    base_url = "https://api.mineduc.cl/sige/v1"
    api_key = os.getenv('MINEDUC_API_KEY')
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Obtener matrícula
    response = requests.get(
        f"{base_url}/matricula",
        headers=headers,
        params={'ano': 2025}
    )
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['records'])
        df.to_csv('data/raw/matricula_2025.csv', index=False)
    else:
        log_error(f"API error: {response.status_code}")
```

**Ventajas:**
- ✅ Más moderno y flexible
- ✅ Datos en tiempo real
- ✅ Consultas parametrizadas

**Desventajas:**
- ❌ Probablemente no existe actualmente
- ⚠️ Requiere desarrollo por parte del MINEDUC
- ⚠️ Mantenimiento de la API

**Probabilidad:** Baja (requeriría inversión del MINEDUC)

---

### Opción 5: Base de Datos Institucional (⭐ MÁS PROBABLE)

**Descripción:** Conexión a réplica SQL Server o DataMart del SIGE

**CONTEXTO REAL DEL MINEDUC:**

🔹 **SIGE corre sobre SQL Server** (repositorio principal o réplicas)
🔹 **NO te darán acceso al transaccional** (nunca, por estabilidad y seguridad)
🔹 **SÍ existe réplica o DataMart para análisis** (esto es lo común en Gobierno)

**Servidores típicos del MINEDUC:**
- `SQL-SIGE-REPLICA` (réplica cada hora/día/semana)
- `SQL-DATAMART-MINEDUC` (vistas consolidadas)
- `SQL-ANALISIS-EDUCACION` (para reportería)
- Otros nombres según infraestructura TI

**Lo que TI puede otorgar:**
- ✅ Usuario **read-only** en servidor de réplicas
- ✅ Acceso a vistas específicas de EMTP
- ✅ Conexión desde IP autorizada o VPN
- ✅ Actualización según frecuencia de réplica

**Requisitos:**
- Usuario de solo lectura (sin permisos de escritura)
- Acceso a vistas/tablas específicas del SIGE
- Conexión desde IP fija o VPN institucional
- Credenciales corporativas (no personales)

**Implementación:**

```python
# scripts/actualizar_desde_bd_sige.py
import pyodbc
import pandas as pd
import os
from datetime import datetime

def conectar_replica_sige():
    """
    Conecta a réplica SQL Server del SIGE
    NO al transaccional, sino al DataMart/réplica
    """
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SIGE_DB_HOST')};"  # ej: SQL-SIGE-REPLICA.mineduc.cl
        f"DATABASE={os.getenv('SIGE_DB_NAME')};"  # ej: SIGE_DataMart
        f"UID={os.getenv('SIGE_DB_USER')};"      # usuario read-only
        f"PWD={os.getenv('SIGE_DB_PASS')}"
    )
    
    return pyodbc.connect(connection_string, timeout=30)

def consultar_matricula_emtp():
    """
    Extrae datos de matrícula EMTP desde vistas del SIGE
    """
    conn = conectar_replica_sige()
    
    # Usar vistas creadas por TI específicamente para EMTP
    query = """
        SELECT 
            RBD,
            DV_RBD,
            NOMBRE_ESTABLECIMIENTO,
            REGION,
            COMUNA,
            MRUN AS RUT_ESTUDIANTE,
            NOMBRES,
            APELLIDO_PATERNO,
            APELLIDO_MATERNO,
            FECHA_NACIMIENTO,
            SEXO,
            CODIGO_ENSENANZA,
            NOMBRE_ENSENANZA,
            GRADO,
            LETRA_CURSO,
            ESPECIALIDAD,
            ANO_LECTIVO,
            ESTADO_MATRICULA
        FROM vw_sige_matricula_emtp_ano  -- Vista creada por TI
        WHERE ANO_LECTIVO = YEAR(GETDATE())
          AND ESTADO_MATRICULA = 'ACTIVO'
          AND CODIGO_ENSENANZA IN (310, 410, 510, 610, 710, 810)  -- TP
    """
    
    print(f"[{datetime.now()}] Consultando matrícula EMTP...")
    df = pd.read_sql(query, conn)
    
    # Guardar como CSV
    output_path = 'data/raw/matricula_emtp_actualizada.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✓ {len(df):,} registros extraídos")
    print(f"✓ Guardado en: {output_path}")
    
    conn.close()
    return output_path

def consultar_egresados_emtp():
    """
    Extrae datos de egresados EMTP
    """
    conn = conectar_replica_sige()
    
    query = """
        SELECT 
            RBD,
            RUT_ESTUDIANTE,
            NOMBRES_COMPLETOS,
            ANO_EGRESO,
            ESPECIALIDAD,
            SITUACION_FINAL,
            PROMEDIO_NOTAS
        FROM vw_sige_egresados_emtp
        WHERE ANO_EGRESO >= YEAR(GETDATE()) - 5  -- Últimos 5 años
    """
    
    df = pd.read_sql(query, conn)
    df.to_csv('data/raw/egresados_emtp_actualizada.csv', index=False)
    
    conn.close()
    return len(df)

def consultar_establecimientos_emtp():
    """
    Extrae datos de establecimientos con EMTP
    """
    conn = conectar_replica_sige()
    
    query = """
        SELECT DISTINCT
            e.RBD,
            e.DV_RBD,
            e.NOMBRE_ESTABLECIMIENTO,
            e.REGION,
            e.COMUNA,
            e.DIRECCION,
            e.DEPENDENCIA,
            e.ZONA,
            e.LATITUD,
            e.LONGITUD,
            COUNT(m.MRUN) as TOTAL_MATRICULA_TP
        FROM vw_sige_establecimientos e
        LEFT JOIN vw_sige_matricula_emtp_ano m 
            ON e.RBD = m.RBD 
            AND m.ANO_LECTIVO = YEAR(GETDATE())
        WHERE e.TIENE_ENSENANZA_TP = 1
        GROUP BY e.RBD, e.DV_RBD, e.NOMBRE_ESTABLECIMIENTO, 
                 e.REGION, e.COMUNA, e.DIRECCION, e.DEPENDENCIA, 
                 e.ZONA, e.LATITUD, e.LONGITUD
    """
    
    df = pd.read_sql(query, conn)
    df.to_csv('data/raw/establecimientos_emtp_actualizada.csv', index=False)
    
    conn.close()
    return len(df)

def actualizar_todos_los_datos():
    """
    Ejecuta extracción completa de datos del SIGE
    """
    try:
        print("="*60)
        print("ACTUALIZACIÓN AUTOMÁTICA DESDE RÉPLICA SIGE")
        print("="*60)
        
        # 1. Matrícula
        consultar_matricula_emtp()
        
        # 2. Egresados
        total_egresados = consultar_egresados_emtp()
        print(f"✓ Egresados: {total_egresados:,} registros")
        
        # 3. Establecimientos
        total_estab = consultar_establecimientos_emtp()
        print(f"✓ Establecimientos: {total_estab:,} registros")
        
        # 4. Procesar datos (script existente)
        print("\nProcesando datos...")
        from actualizar_datos_semanal import procesar_archivos_nuevos
        procesar_archivos_nuevos()
        
        print("\n✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print(f"Fecha: {datetime.now()}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN ACTUALIZACIÓN: {e}")
        
        # Enviar alerta a TI
        from utils.alerts import enviar_alerta_error
        enviar_alerta_error(f"Fallo actualización SIGE: {e}")
        
        return False

if __name__ == '__main__':
    actualizar_todos_los_datos()
```

**Configuración de variables de entorno (.env):**

```bash
# Conexión a réplica SQL Server del SIGE
# (Credenciales otorgadas por TI MINEDUC)

SIGE_DB_HOST=SQL-SIGE-REPLICA.mineduc.cl  # o nombre real del servidor
SIGE_DB_NAME=SIGE_DataMart                # o SIGE_Replica, o nombre asignado
SIGE_DB_USER=readonly_emtp                # usuario read-only
SIGE_DB_PASS=contraseña_segura            # credencial corporativa
SIGE_DB_PORT=1433                         # puerto SQL Server
```

**Cron job (ejecución automática):**

```bash
# Ejecutar cada lunes a las 6 AM (después de actualización de réplica)
0 6 * * 1 /path/to/venv/bin/python /path/to/scripts/actualizar_desde_bd_sige.py >> /path/to/logs/actualizacion_sige.log 2>&1
```

**Ventajas:**
- ✅ **MÁS PROBABLE** que exista en infraestructura MINEDUC
- ✅ Datos siempre actualizados (según frecuencia de réplica)
- ✅ Consultas SQL flexibles y específicas
- ✅ No depende de archivos intermedios
- ✅ Escalable y profesional
- ✅ TI ya tiene experiencia otorgando estos accesos
- ✅ Vistas pueden estar pre-filtradas para EMTP

**Desventajas:**
- ⚠️ Requiere coordinación formal con TI MINEDUC
- ⚠️ Proceso de solicitud puede tomar 2-4 semanas
- ⚠️ Necesita IP fija o VPN institucional
- ⚠️ Depende de frecuencia de actualización de réplica (puede ser diaria, semanal)

**Diferencia clave:**
- ❌ NO es conexión al SIGE transaccional (nunca te lo darán)
- ✅ SÍ es conexión a réplica/DataMart (diseñado para esto)

**Probabilidad:** 🟢 **ALTA (80%)** - Es la práctica estándar en Gobierno de Chile

---

## Comparación de Opciones

| Criterio | Manual | SharePoint | SFTP/FTP | API REST | SQL Server Réplica |
|----------|--------|------------|----------|----------|-------------------|
| **Automatización** | ❌ No | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| **Complejidad técnica** | ✅ Baja | 🟡 Media | 🟡 Media | 🟡 Media | � Media |
| **Requiere MINEDUC** | ❌ No | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| **Seguridad** | ✅ Alta | ✅ Alta | 🟡 Media | ✅ Alta | ✅ **Muy Alta** |
| **Mantenibilidad** | ❌ Baja | ✅ Alta | ✅ Alta | ✅ Alta | ✅ **Muy Alta** |
| **Probabilidad existe** | ✅ 100% | 🟡 60% | 🟡 30% | ❌ 5% | � **80%** |
| **Tiempo implementación** | ✅ 0h | 🟡 4h | 🟡 4h | 🔴 40h | � **6h** |
| **Recomendación** | Temporal | 2da opción | 3era opción | No viable | ⭐ **1era opción** |
| **Datos en tiempo real** | ❌ No | ❌ No | ❌ No | ✅ Sí | ✅ **Según réplica** |
| **Escalabilidad** | ❌ Baja | 🟡 Media | 🟡 Media | ✅ Alta | ✅ **Muy Alta** |
| **Ya usado en Mineduc** | ✅ Sí | 🟡 A veces | ❌ Raro | ❌ No | ✅ **Estándar** |

### Recomendación Final Actualizada

**1ra Opción (⭐ RECOMENDADA):** SQL Server - Réplica del SIGE
- **Por qué:** Es la práctica estándar del Gobierno de Chile
- **Ventaja clave:** TI ya tiene experiencia otorgando estos accesos
- **Realidad:** SIGE corre sobre SQL Server, tienen réplicas para análisis
- **Probabilidad de éxito:** 80%

**2da Opción (alternativa):** SharePoint/OneDrive
- **Por qué:** Si TI prefiere no dar acceso directo a BD
- **Ventaja:** Más simple para TI, sin riesgo de carga en BD
- **Probabilidad de éxito:** 60%

**3era Opción (menos probable):** SFTP/FTP
- **Por qué:** Menos común en instituciones modernas
- **Probabilidad de éxito:** 30%

**Opción Temporal (actual):** Manual
- **Usar solo:** Mientras se coordina con TI
- **Duración máxima:** 2-3 meses

---

## 📋 Solicitud Formal para TI MINEDUC

**Puedes usar esta plantilla para solicitar el acceso:**

---

### SOLICITUD DE ACCESO A RÉPLICA SQL SERVER DEL SIGE

**DE:** Andrés Lazcano - División EMTP  
**PARA:** TI MINEDUC / Administración de Bases de Datos  
**ASUNTO:** Solicitud de usuario read-only para réplica SIGE (Plataforma Visualizador EMTP)  
**FECHA:** [Completar]

---

#### 1. PROPÓSITO

Solicito acceso de **solo lectura** a la réplica o DataMart del SIGE para alimentar la plataforma **Visualizador EMTP**, herramienta interna de análisis de datos de Educación Media Técnico-Profesional.

**Objetivo:** Automatizar la actualización semanal de datos para dashboards de:
- Matrícula EMTP
- Egresados y titulación
- Establecimientos con modalidad TP
- Docentes de especialidades

Actualmente el proceso es **manual** (descarga de CSVs), lo que genera:
- Riesgo de datos desactualizados
- Carga operativa para TI
- Dependencia de intervención humana

---

#### 2. TIPO DE ACCESO SOLICITADO

✅ **Usuario read-only** (sin permisos de escritura)  
✅ **Acceso a réplica o DataMart** (NO al SIGE transaccional)  
✅ **Conexión desde IP fija** (servidor interno MINEDUC) o VPN institucional  
✅ **Credenciales corporativas** (no personales)

**NO se requiere:**
❌ Acceso al SIGE transaccional  
❌ Permisos de escritura/modificación  
❌ Acceso a datos personales sensibles (RUT puede anonimizarse si es necesario)

---

#### 3. VISTAS/TABLAS NECESARIAS

Solicitamos acceso a las siguientes vistas (si ya existen) o tablas equivalentes:

**A) Matrícula EMTP:**
```sql
vw_sige_matricula_emtp_ano
-- Campos requeridos: RBD, región, comuna, especialidad, año lectivo, estado
```

**B) Egresados:**
```sql
vw_sige_egresados_emtp
-- Campos requeridos: RBD, año egreso, especialidad, situación final
```

**C) Establecimientos con EMTP:**
```sql
vw_sige_establecimientos
-- Campos requeridos: RBD, nombre, región, comuna, dependencia, coordenadas
```

**D) Docentes (opcional):**
```sql
vw_sige_docentes_emtp
-- Campos requeridos: RBD, especialidad que imparte, título profesional
```

**Nota:** Si estas vistas no existen, podemos trabajar con las tablas base del DataMart y crear las consultas necesarias.

---

#### 4. FRECUENCIA DE ACTUALIZACIÓN

**Frecuencia de consulta:** Semanal (lunes 6:00 AM)  
**Volumen estimado:** ~200,000 registros por consulta  
**Impacto en BD:** Mínimo (consulta fuera de horario peak, solo lectura)

**Pregunta para TI:** ¿Con qué frecuencia se actualiza la réplica del SIGE?  
- Si es diaria → perfecto  
- Si es semanal → nos ajustamos a ese cronograma

---

#### 5. INFORMACIÓN TÉCNICA

**Servidor donde se ejecutará:**
- Ubicación: [Completar: servidor interno MINEDUC o cloud autorizado]
- IP fija: [Completar o indicar "Conexión vía VPN institucional"]
- Sistema Operativo: Linux (Ubuntu 22.04) o Windows Server

**Tecnología de conexión:**
- Python 3.12 con biblioteca `pyodbc`
- Driver: ODBC Driver 17 for SQL Server
- Conexión cifrada (TLS 1.2+)

**Cadena de conexión (referencia):**
```python
DRIVER={ODBC Driver 17 for SQL Server};
SERVER=[nombre_servidor];
DATABASE=[nombre_bd];
UID=[usuario_readonly];
PWD=[credencial]
```

---

#### 6. MEDIDAS DE SEGURIDAD

**Compromiso de seguridad:**

✅ **Credenciales cifradas** en variables de entorno (nunca en código)  
✅ **Solo lectura** - sin capacidad de modificar datos  
✅ **Logging completo** de consultas ejecutadas  
✅ **Acceso limitado** a personal autorizado (Jefatura EMTP + desarrollador)  
✅ **Rotación de credenciales** según política institucional  
✅ **Datos anonimizados** si se requiere (podemos trabajar sin RUT de estudiantes)

**Responsables:**
- Jefe de División EMTP: [Nombre y contacto]
- Desarrollador responsable: Andrés Lazcano (ext.andres.lazcano@mineduc.cl)
- Soporte TI interno: [Completar]

---

#### 7. NIVEL DE ANONIMIZACIÓN (OPCIONAL)

Si hay restricciones sobre datos personales, podemos trabajar con:

**Opción A - Datos Agregados (sin RUT):**
```sql
-- Solo totales, sin identificación individual
SELECT RBD, ESPECIALIDAD, COUNT(*) as TOTAL_MATRICULA
FROM vw_matricula_emtp
GROUP BY RBD, ESPECIALIDAD
```

**Opción B - RUT Hasheado:**
```sql
-- RUT encriptado para seguimiento sin identificación
SELECT HASHBYTES('SHA2_256', RUT) as RUT_HASH, ...
```

**Opción C - Acceso completo (preferido):**
- Justificación: Análisis detallado de trayectorias educativas
- Compromiso: Solo para uso interno MINEDUC

---

#### 8. TIEMPO ESTIMADO DE IMPLEMENTACIÓN

Una vez otorgado el acceso:

**Desarrollo:** 4-6 horas
- Configurar conexión
- Adaptar consultas SQL a estructura real
- Implementar logging y alertas
- Probar extracción completa

**Pruebas:** 1-2 semanas
- Validar datos extraídos
- Comparar con fuentes actuales
- Ajustar según feedback TI

**Despliegue:** 1 día
- Activar cron job semanal
- Monitoreo primera semana

---

#### 9. CONTACTO Y COORDINACIÓN

**Para coordinación técnica:**
- Andrés Lazcano
- Email: ext.andres.lazcano@mineduc.cl
- Disponibilidad: Lunes a Viernes 9:00-18:00

**Preguntas específicas para TI:**

1. ¿Cuál es el nombre del servidor de réplica del SIGE?  
   _Respuesta: ___________________________________

2. ¿Qué base de datos/schema contiene las vistas de análisis?  
   _Respuesta: ___________________________________

3. ¿Con qué frecuencia se actualiza la réplica?  
   _Respuesta: ___________________________________

4. ¿Ya existen vistas para EMTP o debemos trabajar con tablas base?  
   _Respuesta: ___________________________________

5. ¿Hay restricciones de horario para consultas?  
   _Respuesta: ___________________________________

6. ¿Se requiere VPN o basta con IP fija?  
   _Respuesta: ___________________________________

7. ¿Quién es el responsable de administración de esta BD?  
   _Nombre: _________________ Email: _________________

---

#### 10. PRÓXIMOS PASOS

1. **Reunión de coordinación** (30-60 min)
   - Aclarar dudas técnicas
   - Definir estructura de vistas
   - Establecer cronograma

2. **Creación de usuario read-only**
   - Usuario: `readonly_emtp` (o nombre sugerido por TI)
   - Permisos: SELECT en vistas/tablas acordadas

3. **Entrega de credenciales**
   - Sobre sellado o email cifrado
   - Incluir: servidor, puerto, base de datos, usuario, contraseña

4. **Prueba piloto**
   - Validar conexión
   - Ejecutar consultas de prueba
   - Ajustar según necesidad

5. **Despliegue en producción**
   - Activar actualización semanal automática
   - Monitoreo y seguimiento

---

**FECHA ESPERADA DE RESPUESTA:** [Sugerir: 2 semanas]

**URGENCIA:** 🟡 Media - Funcional con proceso manual actual, pero automatización mejorará significativamente la operación.

---

**Firma:**

_______________________________  
Andrés Lazcano  
División EMTP - MINEDUC  
ext.andres.lazcano@mineduc.cl

_______________________________  
[Jefe División EMTP - Nombre]  
[Email y firma]

---

**CC:**
- Jefatura TI MINEDUC
- Administrador de Base de Datos
- [Otros según corresponda]

---

## Plan de Acción Recomendado

### Fase 1: Definición (Semana 1-2)

**Responsable:** Jefatura EMTP

1. **Reunión con TI MINEDUC**
   - Solicitar información sobre acceso a datos SIGE
   - Preguntar sobre SharePoint/carpetas compartidas
   - Consultar sobre SFTP o acceso a BD
   - Definir frecuencia de actualización de MINEDUC

2. **Documentar hallazgos**
   - ¿Qué opciones están disponibles?
   - ¿Qué credenciales se pueden obtener?
   - ¿Quién es el responsable en TI MINEDUC?

### Fase 2: Implementación (Semana 3-4)

**Responsable:** Desarrollador (Andrés Lazcano o freelancer)

1. **Según opción definida, implementar:**
   - Modificar `scripts/actualizar_datos_semanal.py`
   - Agregar autenticación y descarga automática
   - Implementar logging detallado
   - Crear alertas por email si falla

2. **Configurar credenciales seguras:**
   ```bash
   # .env (nunca subir a GitHub)
   SHAREPOINT_CLIENT_ID=xxx
   SHAREPOINT_CLIENT_SECRET=yyy
   # o
   FTP_HOST=ftp.mineduc.cl
   FTP_USER=usuario
   FTP_PASS=contraseña
   ```

3. **Probar en desarrollo:**
   - Ejecutar descarga manual
   - Verificar datos procesados correctamente
   - Confirmar cron job funciona

### Fase 3: Despliegue (Semana 5)

**Responsable:** TI Interno

1. **Configurar en producción:**
   - Instalar dependencias adicionales
   - Configurar variables de entorno
   - Activar cron job automático

2. **Monitoreo inicial:**
   - Revisar logs primera semana
   - Confirmar actualizaciones exitosas
   - Ajustar frecuencia si es necesario

### Fase 4: Contingencia (Permanente)

**Responsable:** TI Interno

1. **Si actualización automática falla:**
   ```bash
   # Volver a modo manual temporal
   # Descargar CSVs y colocar en data/raw/
   # Script procesará automáticamente
   ```

2. **Alertar a desarrollador si:**
   - Falla >3 veces consecutivas
   - Cambia estructura de datos MINEDUC
   - Error no documentado en logs

---

## Solución Temporal (Mientras se Define)

### Para Desarrollo y Pruebas

Usar datos **simulados** (ya implementado):

```python
# src/data/loaders.py
def cargar_datos():
    if MODO_DESARROLLO:
        return generar_datos_simulados()  # ✅ Ya funciona
    else:
        return cargar_desde_archivos()
```

### Para Producción Inicial

Proceso **manual** documentado:

```markdown
## Procedimiento Semanal TI

1. Lunes 5:00 AM - Descargar datos:
   - Ingresar a [Portal MINEDUC]
   - Descargar CSVs de la semana
   - Guardar en carpeta temporal

2. Copiar a servidor:
   scp matricula.csv usuario@servidor:/path/to/data/raw/

3. Verificar procesamiento automático:
   tail -f /path/to/logs/app.log

4. Confirmar dashboards actualizados:
   curl http://localhost:8051
```

**Documentar en:** `docs/MANUAL_MANTENIMIENTO.md`

---

## Preguntas para TI MINEDUC (ACTUALIZADAS)

### Reunión de Coordinación

**🎯 Pregunta 1 (CRÍTICA):** ¿Tienen servidor de réplica o DataMart del SIGE?
- ¿Cómo se llama el servidor? (ej: SQL-SIGE-REPLICA, SQL-DATAMART-MINEDUC)
- ¿Qué base de datos contiene? (ej: SIGE_DataMart, SIGE_Replica)
- ¿Con qué frecuencia se actualiza? (cada hora, diario, semanal)

**🎯 Pregunta 2:** ¿Ya existen vistas para análisis de datos SIGE?
- ¿Hay vistas predefinidas para EMTP?
- ¿Otras divisiones ya consultan este servidor?
- ¿Tienen documentación de las tablas/vistas disponibles?

**Pregunta 3:** ¿Cómo acceden actualmente otras áreas a datos SIGE?
- ¿Descargan CSVs manualmente?
- ¿Tienen conexión SQL directa?
- ¿Usan SharePoint o carpetas compartidas?
- ¿Existe API o servicio web?

**Pregunta 4:** ¿Qué tipo de credenciales pueden otorgar?
- ¿Usuario SQL Server read-only?
- ¿Service Principal de SharePoint?
- ¿Usuario FTP de solo lectura?
- ¿Cuál es el proceso de solicitud formal?

**Pregunta 5:** ¿Hay restricciones de horario o volumen?
- ¿Se pueden hacer consultas los lunes 6 AM?
- ¿Hay límite de registros por consulta?
- ¿Requiere VPN o basta IP fija?

**Pregunta 6:** ¿Cuáles son los requisitos de seguridad?
- ¿Se requiere anonimización de RUT?
- ¿Hay logging de consultas ejecutadas?
- ¿Cada cuánto rotan credenciales?

**Pregunta 7:** ¿Quién es el responsable técnico?
- Nombre y contacto del administrador de BD
- ¿A quién contactar si hay problemas?
- ¿Hay soporte técnico 24/7 o solo horario hábil?

**Pregunta 8:** ¿Hay cambios programados en estructura de datos?
- ¿Se mantiene estable la estructura de tablas?
- ¿Hay versionamiento?
- ¿Notifican cambios con anticipación?

### NUEVA Pregunta Clave (basada en realidad MINEDUC):

**❓ Pregunta 9:** ¿El SIGE transaccional corre sobre SQL Server?
- **Respuesta esperada:** Sí → Confirmar que existe réplica
- ¿Oracle también? → Preguntar si réplica está en SQL Server de todos modos

**❓ Pregunta 10:** ¿Cuánto demora el proceso de solicitud?
- ¿2 semanas, 1 mes?
- ¿Qué documentos formales se requieren?
- ¿Hay formulario estándar de solicitud?
- ¿Hay portal de descarga?
- ¿Tienen SharePoint institucional?
- ¿Existe API o servicio web?

**Pregunta 2:** ¿Con qué frecuencia se actualizan los datos en la fuente?
- ¿Diaria, semanal, mensual?
- ¿Hay calendario de actualizaciones?

**Pregunta 3:** ¿Qué tipo de credenciales pueden otorgar?
- ¿Service Principal de SharePoint?
- ¿Usuario FTP de solo lectura?
- ¿Acceso a BD con permisos limitados?

**Pregunta 4:** ¿Quién es el responsable técnico de datos SIGE?
- Nombre y contacto
- Para coordinación y soporte

**Pregunta 5:** ¿Hay cambios programados en estructura de datos?
- ¿Se mantiene estable?
- ¿Hay versionamiento?

---

## 💡 Contexto Real del MINEDUC (Información Clave)

### ¿Cómo funciona realmente el SIGE en el MINEDUC?

**✅ Confirmado por fuentes expertas:**

1. **SIGE corre sobre SQL Server**
   - Sistema transaccional principal: SQL Server
   - Algunos módulos pueden usar Oracle, pero réplicas están en SQL Server
   - Es el estándar del Gobierno de Chile (licencias históricas)

2. **NO te darán acceso al transaccional**
   - **Nunca** acceso al SIGE "en vivo"
   - Razones: estabilidad, bloqueos, datos sensibles, auditoría estricta
   - Esto es política estándar en todo el Gobierno

3. **SÍ tienen réplicas para análisis**
   - Servidor de réplicas del SIGE (cada hora/día/semana)
   - DataMart o DataWarehouse institucional
   - Diseñado específicamente para consultas y análisis
   - Otras divisiones ya lo usan

4. **Nombres típicos de servidores:**
   - `SQL-SIGE-REPLICA`
   - `SQL-DATAMART-MINEDUC`
   - `SQL-ANALISIS-EDUCACION`
   - `DW Educacional`
   - `Repositorio Institucional`

5. **Vistas comunes que pueden existir:**
   - `vw_sige_matricula_emtp_ano`
   - `vw_sige_estudiantes_con_rut`
   - `vw_sige_egresados`
   - `vw_sige_establecimientos`
   - `vw_sige_cursos`
   - `vw_sige_docentes`

### ¿Qué significa esto para tu proyecto?

✅ **BUENA NOTICIA:** La Opción 5 (SQL Server) es la MÁS probable  
✅ **TI ya tiene experiencia** otorgando estos accesos  
✅ **Es el proceso estándar** que otras divisiones ya usan  
✅ **Probabilidad de éxito: 80%**

### ¿Qué pedir exactamente?

**Lenguaje que TI entiende:**

> "Acceso SQL read-only a las réplicas del SIGE o al DataMart institucional"

**NO pedir:**
- ❌ "Acceso al SIGE" (muy ambiguo, lo rechazarán)
- ❌ "Conexión a la base de datos de producción" (nunca lo darán)

**SÍ pedir:**
- ✅ "Usuario read-only en réplica del SIGE"
- ✅ "Acceso a vistas de análisis de EMTP"
- ✅ "Consulta a DataMart institucional"

### ¿Cuánto demora?

**Proceso típico:**
- Solicitud formal: 1-2 días (preparar documento)
- Aprobación: 1-2 semanas (según burocracia)
- Creación de usuario: 1-3 días (TI crea cuenta)
- Pruebas: 1 semana
- **TOTAL: 3-4 semanas**

### ¿Qué hacer mientras tanto?

**Opción temporal (1-3 meses):**
- Seguir con proceso manual
- TI descarga CSVs semanalmente
- Script automático procesa

**Preparación:**
- Enviar solicitud formal (usar plantilla de este documento)
- Agendar reunión con TI
- Preparar preguntas específicas

---

## Decisión Final

**A definir en reunión con TI:** __________  
**Opción más probable:** SQL Server - Réplica del SIGE (80% probabilidad)  
**Opción alternativa:** SharePoint (si TI prefiere)  
**Responsable implementación:** Andrés Lazcano + TI MINEDUC  
**Fecha límite estimada:** [4 semanas desde solicitud]  
**Fecha primera prueba:** [Tras recibir credenciales]

---

## 📞 Próximos Pasos Inmediatos

1. **✅ Leer este documento completo** (ya lo hiciste)
2. **📧 Enviar solicitud formal a TI** (usar plantilla de este doc)
3. **📅 Agendar reunión** (30-60 min con administrador BD)
4. **📝 Preparar preguntas** (lista incluida arriba)
5. **⏳ Esperar respuesta** (2-4 semanas típicamente)
6. **🔧 Implementar** (4-6 horas una vez tengamos credenciales)

---

**Documento creado:** 17 de Noviembre 2025  
**Última actualización:** 17 de Noviembre 2025  
**Basado en:** Experiencia real del MINEDUC + consulta a expertos  
**Próxima revisión:** Tras reunión con TI MINEDUC  
**Contacto:** ext.andres.lazcano@mineduc.cl
