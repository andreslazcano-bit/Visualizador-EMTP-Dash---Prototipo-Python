# 📊 Guía de Migración de Datos

## Desde R Shiny a Python Dash

Esta guía te ayudará a migrar tus datos desde la versión R Shiny actual a la nueva versión Python Dash.

---

## Opción 1: Archivos Locales (Más Simple)

### Paso 1: Convertir .rds a Parquet

Los archivos `.rds` de R no son nativamente compatibles con Python. Necesitamos convertirlos:

```bash
# Instalar pyreadr
pip install pyreadr

# Convertir todos los archivos automáticamente
python scripts/convert_rds_to_parquet.py --all

# O convertir archivos específicos
python scripts/convert_rds_to_parquet.py ../VisualizadorEMTP/data/processed/20240913_Matricula_unica_2024_TP.rds
```

### Paso 2: Copiar archivos convertidos

Los archivos Parquet generados estarán en el mismo directorio que los originales. Cópialos a tu nuevo proyecto:

```bash
# Copiar desde el proyecto R
cp ../VisualizadorEMTP/data/processed/*.parquet ./data/processed/
cp ../VisualizadorEMTP/data/geographic/*.parquet ./data/geographic/
```

### Paso 3: Configurar en .env

```bash
LOCAL_DATA_ENABLED=True
```

---

## Opción 2: Desde CSV/Excel

Si tienes datos en CSV o Excel, simplemente colócalos en las carpetas correspondientes:

```bash
# Matrícula
cp tus_datos_matricula.csv ./data/processed/

# Docentes
cp tus_datos_docentes.xlsx ./data/processed/

# Geográficos
cp comunas.geojson ./data/geographic/
```

---

## Opción 3: Desde SQL Server (Recomendado para Producción)

### Paso 1: Configurar conexión en .env

```bash
SQL_SERVER_ENABLED=True
SQL_SERVER_HOST=tu-servidor.database.windows.net
SQL_SERVER_DATABASE=emtp_database
SQL_SERVER_USERNAME=tu_usuario
SQL_SERVER_PASSWORD=tu_password
```

### Paso 2: Crear tablas en SQL Server

```sql
-- Crear tabla de matrícula
CREATE TABLE matricula (
    rbd VARCHAR(10),
    nom_rbd VARCHAR(255),
    cod_ense INT,
    -- ... más columnas
);

-- Insertar datos desde CSV o migración
BULK INSERT matricula
FROM 'path/to/matricula.csv'
WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);
```

### Paso 3: Probar conexión

```bash
python scripts/test_connections.py
```

---

## Opción 4: Desde SharePoint

### Paso 1: Configurar credenciales en .env

```bash
SHAREPOINT_ENABLED=True
SHAREPOINT_SITE_URL=https://tuempresa.sharepoint.com/sites/emtp
SHAREPOINT_CLIENT_ID=tu_client_id
SHAREPOINT_CLIENT_SECRET=tu_client_secret
SHAREPOINT_FOLDER_MATRICULA=Documentos Compartidos/Datos/Matricula
```

### Paso 2: Cargar desde SharePoint

```python
from src.data.loaders import data_loader

df = data_loader.load_from_sharepoint(
    folder_path='Documentos Compartidos/Datos/Matricula',
    file_name='matricula_2024.xlsx'
)
```

---

## Estructura de Datos Esperada

### Matrícula

Columnas mínimas requeridas:
- `rbd` (string): Código del establecimiento
- `nom_rbd` (string): Nombre del establecimiento
- `cod_ense` (int): Código de enseñanza (410-863 para EMTP)
- `nom_reg_rbd_a` (string): Región
- `nom_com_rbd` (string): Comuna
- `cod_com_rbd` (string): Código de comuna

### Docentes

Columnas mínimas requeridas:
- `rbd` (string): Código del establecimiento
- `MRUN` (string): RUN del docente
- `COD_ENS_1` (int): Código de enseñanza 1
- `COD_ENS_2` (int): Código de enseñanza 2
- `SUBSECTOR1` (int): Código de especialidad 1
- `SUBSECTOR2` (int): Código de especialidad 2

---

## Script de Migración Completa (R a Python)

Si prefieres migrar todo de una vez:

```python
# scripts/migrate_all_data.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loaders import data_loader
from loguru import logger

def migrate_all():
    """Migra todos los datos de R a Python"""
    
    # Convertir RDS a Parquet
    logger.info("Paso 1: Convertir RDS a Parquet")
    # ... código de conversión
    
    # Cargar y validar
    logger.info("Paso 2: Validar datos")
    # ... código de validación
    
    # Opcional: Subir a SQL Server
    logger.info("Paso 3: Subir a SQL Server")
    # ... código de migración a SQL

if __name__ == '__main__':
    migrate_all()
```

---

## Validación de Datos

Después de migrar, valida que todo esté correcto:

```python
from src.data.loaders import data_loader
from src.data.validators import data_validator

# Cargar datos
df_matricula = data_loader.load_matricula()
df_docentes = data_loader.load_docentes()

# Validar
is_valid, errors = data_validator.validate_matricula(df_matricula)
if not is_valid:
    print("Errores encontrados:", errors)

# Resumen
summary = data_validator.get_data_summary(df_matricula)
print(summary)
```

---

## Troubleshooting

### Error: pyreadr no puede leer el archivo RDS

**Solución**: Exporta desde R a CSV o Parquet:

```r
# En R
library(arrow)
write_parquet(tu_dataframe, "archivo.parquet")

# O CSV
write.csv(tu_dataframe, "archivo.csv", row.names = FALSE)
```

### Error: Conexión a SQL Server falla

**Solución**: Verifica el driver ODBC:

```bash
# macOS
brew install unixodbc

# Ubuntu
sudo apt-get install unixodbc unixodbc-dev

# Verificar drivers instalados
odbcinst -j
```

### Error: Memoria insuficiente

**Solución**: Procesa por chunks:

```python
import pandas as pd

# Leer en chunks
for chunk in pd.read_csv('archivo_grande.csv', chunksize=10000):
    # Procesar chunk
    pass
```

---

## Próximos Pasos

Una vez migrados los datos:

1. Ejecuta `python app.py` para verificar que todo funciona
2. Explora los módulos de matrícula y docentes
3. Configura los filtros según tus necesidades
4. Personaliza los dashboards

---

¿Necesitas ayuda? Revisa `docs/ROADMAP.md` para el plan completo de migración.
