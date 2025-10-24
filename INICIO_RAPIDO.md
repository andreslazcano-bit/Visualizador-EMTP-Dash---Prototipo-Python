# 🚀 Guía de Inicio Rápido

## Paso 1: Configurar Entorno

```bash
# Crear entorno virtual
python -m venv venv

# Activar (macOS/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Paso 2: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
nano .env  # o tu editor preferido
```

Configuraciones mínimas requeridas:
- `SECRET_KEY`: Generar una clave segura
- Fuentes de datos: Habilitar SQL Server, PostgreSQL o Local

## Paso 3: Convertir Datos de R (si aplica)

Si tienes datos en formato .rds de R:

```bash
# Instalar pyreadr
pip install pyreadr

# Convertir todos los archivos
python scripts/convert_rds_to_parquet.py --all

# O convertir uno específico
python scripts/convert_rds_to_parquet.py ../VisualizadorEMTP/data/processed/archivo.rds
```

## Paso 4: Probar Conexiones (opcional)

```bash
python scripts/test_connections.py
```

## Paso 5: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:8050

---

## Siguiente: Migración de Datos

Ver `docs/MIGRACION_DATOS.md` para instrucciones detalladas sobre cómo migrar los datos desde la versión R.

---

## Desarrollo

Para desarrollo activo:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Formatear código
black .
isort .

# Linting
flake8 src/
```

---

## Docker (Producción)

```bash
# Construir imagen
docker-compose build

# Ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Detener
docker-compose down
```
