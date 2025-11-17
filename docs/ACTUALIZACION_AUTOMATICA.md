# 🔄 Sistema de Actualización Automática de Datos

## Descripción General

Este sistema actualiza automáticamente los datos del Visualizador EMTP desde las bases de datos de MINEDUC **cada lunes a las 2:00 AM**, manteniendo un cache local de alta velocidad.

---

## ✅ Ventajas del Sistema

| Característica | Beneficio |
|----------------|-----------|
| **⚡ Velocidad** | Lectura instantánea desde archivos Parquet locales (10-100x más rápido que SQL) |
| **🛡️ Confiabilidad** | Funciona aunque SQL Server esté caído o en mantenimiento |
| **📊 Eficiencia** | No sobrecarga las bases de datos productivas de MINEDUC |
| **🔄 Actualización** | Datos actualizados semanalmente (suficiente para datos educativos) |
| **💾 Almacenamiento** | Formato Parquet comprimido (10x menor tamaño que CSV) |

---

## 📁 Arquitectura de Archivos

```
VisualizadorEMTP-Dash/
├── scripts/
│   ├── actualizar_datos_semanal.py    # Script de actualización automática
│   ├── setup_cron.sh                   # Configurador del cron job
│   └── test_connections.py             # Verificador de conexiones
│
├── data/
│   └── processed/                      # Cache local (NO subir a GitHub)
│       ├── cache_establecimientos.parquet      # 1,124 registros
│       ├── cache_matricula.parquet             # ~100,000 registros
│       ├── cache_matricula_agregado.parquet    # ~1,000 registros (más rápido)
│       ├── cache_docentes.parquet              # ~5,000 registros
│       ├── cache_titulados.parquet             # ~10,000 registros
│       └── cache_metadata.json                 # Timestamp + estadísticas
│
├── src/
│   └── data/
│       └── loaders.py                  # Cargador de datos desde cache
│
├── logs/
│   ├── actualizacion_datos.log         # Logs del script
│   └── actualizacion_cron.log          # Logs del cron
│
├── .env                                # Credenciales (NO subir a GitHub)
└── .env.example.mineduc                # Plantilla de credenciales
```

---

## 🚀 Instalación y Configuración

### Paso 1: Configurar Credenciales

```bash
# Copiar plantilla de variables de entorno
cp .env.example.mineduc .env

# Editar .env con las credenciales reales de MINEDUC
nano .env
```

Completar en `.env`:
```bash
MINEDUC_SQL_SERVER=sql-sige.mineduc.cl
MINEDUC_SQL_DATABASE=SIGE_Produccion
MINEDUC_SQL_USER=tu_usuario_readonly
MINEDUC_SQL_PASSWORD=tu_password_seguro
```

> ⚠️ **IMPORTANTE**: Solicita estas credenciales al equipo de TI MINEDUC

---

### Paso 2: Instalar Dependencias

```bash
# Instalar pyodbc para conectar a SQL Server
pip install pyodbc python-dotenv pandas pyarrow

# En macOS: Instalar ODBC Driver
brew install unixodbc freetds
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17
```

---

### Paso 3: Probar Conexión

```bash
# Verificar que las credenciales sean correctas
python scripts/test_connections.py
```

**Salida esperada**:
```
🧪 TEST DE CONEXIONES A BASES DE DATOS MINEDUC
  
🔌 Probando conexión: SQL Server - SIGE
  Servidor: sql-sige.mineduc.cl
  Base de Datos: SIGE_Produccion
  Usuario: app_visualizador_readonly
  Password: ********
  🔄 Conectando...
  ✅ Conexión exitosa!
  📊 Versión SQL Server: Microsoft SQL Server 2019
  
📋 RESUMEN DE PRUEBAS
  Conexiones exitosas: 1/1
  
  ✅ Todas las conexiones funcionan correctamente
```

---

### Paso 4: Ejecutar Actualización Manual (Primera Vez)

```bash
# Ejecutar actualización manualmente para poblar el cache
python scripts/actualizar_datos_semanal.py
```

**Salida esperada**:
```
================================================================================
🚀 INICIANDO ACTUALIZACIÓN SEMANAL DE DATOS
📅 Fecha: 2025-11-17 14:30:00
================================================================================
🔌 Conectando a SQL Server MINEDUC...
✅ Conexión exitosa

📋 Actualizando datos de establecimientos...
✅ Establecimientos actualizados: 1,124 registros
   Guardado en: data/processed/cache_establecimientos.parquet

📊 Actualizando datos de matrícula...
✅ Matrícula actualizada: 98,453 registros
   Agregado generado: 720 registros

👨‍🏫 Actualizando datos de docentes...
✅ Docentes actualizados: 4,782 registros

🎓 Actualizando datos de titulados...
✅ Titulados actualizados: 12,345 registros

💾 Metadata guardada en: data/processed/cache_metadata.json

================================================================================
✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE
📊 Total de registros actualizados: 116,704
📁 Fuentes actualizadas: 4
================================================================================
```

---

### Paso 5: Configurar Actualización Automática (Cron)

```bash
# Dar permisos de ejecución
chmod +x scripts/setup_cron.sh

# Ejecutar configurador
./scripts/setup_cron.sh
```

Esto configura un cron job que ejecuta **cada lunes a las 2:00 AM**:
```cron
0 2 * * 1 cd /ruta/proyecto && python3 scripts/actualizar_datos_semanal.py >> logs/actualizacion_cron.log 2>&1
```

---

## 📖 Uso en la Aplicación

### Cargar Datos desde Cache

```python
# src/callbacks/matricula_callbacks.py
from src.data.loaders import get_matricula, get_cache_stats
from dash import callback, Input, Output
import plotly.express as px

@callback(
    Output('grafico-matricula', 'figure'),
    Input('dropdown-region', 'value'),
    Input('dropdown-año', 'value')
)
def actualizar_grafico_matricula(region, año):
    """
    Carga datos DESDE EL CACHE (súper rápido)
    NO consulta SQL Server directamente
    """
    # Leer desde cache local (actualizado semanalmente)
    df = get_matricula(region=region, año=año, agregado=True)
    
    # Generar gráfico
    fig = px.bar(
        df, 
        x='Region', 
        y='TotalMatricula',
        title=f'Matrícula EMTP {año}'
    )
    
    return fig


@callback(
    Output('info-cache', 'children')
)
def mostrar_info_cache():
    """
    Muestra información de la última actualización
    """
    stats = get_cache_stats()
    
    return f"""
    📅 Última actualización: {stats['ultima_actualizacion']}
    📊 Registros en cache: {stats['registros_totales']:,}
    ⏰ Actualizado hace {stats['dias_desde_actualizacion']} días
    """
```

---

## 🔍 Monitoreo y Logs

### Ver Logs de Actualización

```bash
# Ver logs en tiempo real
tail -f logs/actualizacion_datos.log

# Ver últimas 50 líneas
tail -n 50 logs/actualizacion_datos.log

# Ver logs del cron
tail -f logs/actualizacion_cron.log
```

### Ver Cron Jobs Activos

```bash
# Listar todos los cron jobs
crontab -l

# Editar cron jobs manualmente
crontab -e
```

### Verificar Estado del Cache

```python
# En Python/iPython
from src.data.loaders import get_cache_stats

stats = get_cache_stats()
print(f"Última actualización: {stats['ultima_actualizacion']}")
print(f"Días desde actualización: {stats['dias_desde_actualizacion']}")
print(f"Estado: {stats['estado']}")
```

---

## ⚙️ Personalización

### Cambiar Frecuencia de Actualización

Editar el cron job:
```bash
crontab -e
```

**Ejemplos de frecuencia**:
```cron
# Cada día a las 2 AM
0 2 * * * /ruta/script.py

# Cada lunes a las 2 AM (actual)
0 2 * * 1 /ruta/script.py

# Cada 1 y 15 del mes a las 3 AM
0 3 1,15 * * /ruta/script.py

# Cada domingo a las 1 AM
0 1 * * 0 /ruta/script.py
```

### Modificar Consultas SQL

Editar `scripts/actualizar_datos_semanal.py`:

```python
def actualizar_matricula(self, conn):
    query = """
    SELECT 
        -- Agregar/quitar columnas según necesidad
        m.RBD,
        m.Año,
        m.NuevaColumna,  -- ← Agregar aquí
        -- ...
    FROM dbo.Matricula m
    WHERE m.Año >= YEAR(GETDATE()) - 5  -- ← Cambiar años de histórico
    """
```

---

## 🐛 Solución de Problemas

### Error: "No se puede conectar a SQL Server"

**Posibles causas**:
1. VPN MINEDUC no está activa
2. Credenciales incorrectas en `.env`
3. Firewall bloqueando puerto 1433
4. IP no está en whitelist de SQL Server

**Solución**:
```bash
# 1. Verificar VPN
ping sql-sige.mineduc.cl

# 2. Probar conexión
python scripts/test_connections.py

# 3. Contactar a TI para verificar:
#    - Usuario tiene permisos READ
#    - IP está en whitelist
#    - Firewall permite puerto 1433
```

### Error: "No existe archivo de cache"

**Causa**: Primera vez que se ejecuta o cache fue borrado

**Solución**:
```bash
# Ejecutar actualización manual
python scripts/actualizar_datos_semanal.py

# Verificar que se crearon los archivos
ls -lh data/processed/cache_*.parquet
```

### El Cron No Se Ejecuta

**Diagnóstico**:
```bash
# 1. Verificar que el cron está configurado
crontab -l

# 2. Ver logs del cron
tail -f logs/actualizacion_cron.log

# 3. Verificar que el servicio cron está corriendo
# macOS:
sudo launchctl list | grep cron

# Linux:
sudo systemctl status cron
```

---

## 📊 Formato de Archivos Cache

### Parquet vs CSV

| Característica | CSV | Parquet (usado) |
|----------------|-----|-----------------|
| **Tamaño** | 100 MB | 10 MB ⭐ |
| **Velocidad lectura** | 5 seg | 0.5 seg ⭐ |
| **Compresión** | No | Sí (Snappy) ⭐ |
| **Tipos de datos** | Strings | Nativos ⭐ |
| **Compatibilidad** | Universal | pandas, Spark, etc. |

### Estructura de Metadata (`cache_metadata.json`)

```json
{
  "fecha_actualizacion": "2025-11-17T02:00:15.234567",
  "registros_totales": 116704,
  "fuentes_actualizadas": [
    {
      "nombre": "establecimientos",
      "registros": 1124,
      "archivo": "data/processed/cache_establecimientos.parquet"
    },
    {
      "nombre": "matricula",
      "registros": 98453,
      "registros_agregados": 720,
      "archivo": "data/processed/cache_matricula.parquet"
    }
  ],
  "errores": []
}
```

---

## 🔐 Seguridad

### Credenciales

- ✅ Almacenadas solo en `.env` (NO en código)
- ✅ `.env` está en `.gitignore` (NO se sube a GitHub)
- ✅ Usuario SQL solo tiene permisos READ (no puede modificar datos)
- ✅ Conexión cifrada (`Encrypt=yes`)

### Recomendaciones para Producción

1. **Azure Key Vault**: Almacenar credenciales en servicio dedicado
2. **Service Principal**: Usar autenticación de Azure AD en vez de usuario/password
3. **IP Whitelist**: Restringir acceso solo desde IP del servidor
4. **Auditoría**: Logs de todas las conexiones y consultas

---

## 📞 Contacto

**Desarrollador**: Andrés Lazcano  
**Email**: ext.andres.lazcano@mineduc.cl  
**Proyecto**: Visualizador EMTP Dash  
**Versión**: 2.0  
**Fecha**: Noviembre 2025

Para solicitar credenciales de acceso a bases de datos MINEDUC, contactar a **Equipo TI MINEDUC**: ti@mineduc.cl

---

## 📚 Documentos Relacionados

- `docs/ARQUITECTURA_DETALLADA.md` - Arquitectura completa del sistema
- `_docs-planificacion/DEFINICIONES_PARA_PRODUCCION.md` - Decisiones estratégicas
- `.env.example.mineduc` - Plantilla de credenciales
