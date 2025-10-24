<<<<<<< HEAD
# Visualizador-EMTP-Dash---Prototipo-Python
=======
# 📊 Visualizador EMTP - Dash Python

> Aplicación web interactiva para explorar y analizar datos de Enseñanza Media Técnico Profesional en Chile - Versión Python/Dash

[![Dash](https://img.shields.io/badge/Dash-3.0-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-En_Desarrollo-yellow.svg)]()

---

## 🌟 Migración desde Shiny R

Esta es la versión Python/Dash del Visualizador EMTP, migrada desde la aplicación original en R Shiny.

### Ventajas de la migración a Python:
- 🚀 Mayor escalabilidad y rendimiento
- 🔧 Integración más sencilla con múltiples fuentes de datos (SQL, APIs, SharePoint)
- 📦 Ecosistema robusto de librerías de data science
- 🐳 Mejor soporte para contenedores y deployment cloud
- 💼 Soporte institucional y estándares de TI

---

## 📋 Características

- **📈 Visualización Interactiva**: Dashboards con Plotly y Dash
- **🗺️ Mapas Geográficos**: Visualización con Folium/Plotly Maps
- **📥 Descarga de Datos**: Exportación en múltiples formatos (CSV, Excel, JSON)
- **📄 Generación de Reportes**: PDFs y Word con reportes personalizados
- **🔐 Autenticación**: Sistema de login seguro
- **💾 Múltiples Fuentes de Datos**: SQL Server, PostgreSQL, SharePoint, CSV, Excel
- **⚡ Optimizado**: Caching y procesamiento eficiente

---

## 🏗️ Arquitectura

```
VisualizadorEMTP-Dash/
├── app.py                      # Aplicación principal Dash
├── config/                     # Configuración
│   ├── __init__.py
│   ├── settings.py            # Variables de configuración
│   └── database.py            # Configuración de bases de datos
├── src/                       # Código fuente
│   ├── __init__.py
│   ├── data/                  # Módulos de datos
│   │   ├── __init__.py
│   │   ├── loaders.py        # Carga desde múltiples fuentes
│   │   ├── processors.py      # Procesamiento de datos
│   │   └── validators.py      # Validación de datos
│   ├── layouts/               # Layouts de la UI
│   │   ├── __init__.py
│   │   ├── main_layout.py
│   │   ├── matricula.py
│   │   ├── docentes.py
│   │   ├── titulados.py
│   │   └── mapas.py
│   ├── callbacks/             # Callbacks de Dash
│   │   ├── __init__.py
│   │   ├── matricula_callbacks.py
│   │   ├── docentes_callbacks.py
│   │   └── mapa_callbacks.py
│   ├── components/            # Componentes reutilizables
│   │   ├── __init__.py
│   │   ├── filters.py
│   │   ├── charts.py
│   │   └── tables.py
│   └── utils/                 # Utilidades
│       ├── __init__.py
│       ├── auth.py           # Autenticación
│       ├── exports.py        # Exportación de datos
│       └── helpers.py        # Funciones auxiliares
├── data/                      # Datos
│   ├── raw/                  # Datos crudos
│   ├── processed/            # Datos procesados
│   └── geographic/           # Datos geográficos
├── reports/                   # Reportes generados
│   └── templates/            # Plantillas de reportes
├── assets/                    # Assets estáticos
│   ├── css/
│   ├── images/
│   └── js/
├── tests/                     # Tests
│   ├── __init__.py
│   ├── test_data.py
│   └── test_callbacks.py
├── docs/                      # Documentación
├── requirements.txt           # Dependencias Python
├── requirements-dev.txt       # Dependencias de desarrollo
├── Dockerfile                 # Para containerización
├── docker-compose.yml         # Orquestación de servicios
└── .env.example              # Variables de entorno de ejemplo
```

---

## 💻 Instalación

### Requisitos Previos

- **Python** >= 3.9 ([Descargar](https://www.python.org/))
- **pip** (incluido con Python)
- **Git** (opcional)

### Instalación Local

1. **Clonar o crear el entorno virtual**
```bash
cd VisualizadorEMTP-Dash
python -m venv venv
```

2. **Activar entorno virtual**
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:8050`

---

## 🔧 Configuración de Fuentes de Datos

### SQL Server
```python
# En .env
SQL_SERVER_HOST=tu-servidor.database.windows.net
SQL_SERVER_DATABASE=tu_base_datos
SQL_SERVER_USERNAME=tu_usuario
SQL_SERVER_PASSWORD=tu_password
```

### PostgreSQL
```python
# En .env
POSTGRES_HOST=localhost
POSTGRES_DATABASE=emtp_db
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=tu_password
```

### SharePoint
```python
# En .env
SHAREPOINT_SITE_URL=https://tuempresa.sharepoint.com/sites/tu-sitio
SHAREPOINT_CLIENT_ID=tu_client_id
SHAREPOINT_CLIENT_SECRET=tu_client_secret
```

### CSV/Excel Local
```python
# Colocar archivos en data/raw/
# La aplicación los detectará automáticamente
```

---

## 📊 Migración de Datos

Los datos de la versión R Shiny pueden ser reutilizados:

1. **Archivos .rds**: Convertir a Parquet o CSV
```bash
python scripts/convert_rds_to_parquet.py
```

2. **Estructura de datos**: Los DataFrames de pandas son equivalentes a los de R
3. **Procesamiento**: Los pipelines se migran a pandas/polars

---

## 🚀 Deployment

### Docker
```bash
docker-compose up -d
```

### Azure App Service / AWS
Ver documentación en `docs/DEPLOYMENT.md`

### Heroku
```bash
heroku create visualizador-emtp-dash
git push heroku main
```

---

## 🔐 Seguridad

- Autenticación con bcrypt
- Variables de entorno para credenciales
- HTTPS en producción
- Rate limiting
- Logging de accesos

---

## 📝 Roadmap

- [x] Estructura base del proyecto
- [ ] Migración módulo de matrícula
- [ ] Migración módulo de docentes
- [ ] Migración módulo de titulados
- [ ] Integración con SQL Server
- [ ] Integración con SharePoint
- [ ] Sistema de autenticación
- [ ] Generación de reportes PDF/Word
- [ ] Tests unitarios
- [ ] Deployment a producción

---

## 🤝 Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

---

## 📄 Licencia

[Definir licencia según institución]
>>>>>>> c773f7e (Primer commit - Visualizador EMTP Dash)
