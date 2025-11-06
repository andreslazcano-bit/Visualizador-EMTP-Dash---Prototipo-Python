#  Visualizador EMTP - Dashboard Python/Dash

> Sistema de análisis y visualización interactiva de datos del Sistema de Educación Media Técnico-Profesional de Chile

[![Dash](https://img.shields.io/badge/Dash-2.14.2-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-orange.svg)](https://plotly.com/)
[![Status](https://img.shields.io/badge/Status-Funcional-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

##  Inicio Rápido (3 pasos)

### 1️⃣ Clonar y preparar entorno

```bash
# Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# Crear entorno virtual
python3 -m venv venv

# Activar entorno (macOS/Linux)
source venv/bin/activate

# Activar entorno (Windows)
# venv\Scripts\activate
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar aplicación

```bash
python app_v2.py
```

**¡Listo!** Abre tu navegador en: **http://localhost:8051**

---

## Características Principales

### ✨ Funcionalidades
- **📊 Visualización Interactiva**: Gráficos dinámicos con Plotly
- **🗺️ Mapas Geográficos**: Visualización territorial con GeoJSON real de Chile
- **🎨 Colores Institucionales**: Paleta basada en diseño Shiny original (#34536A, #B35A5A, #C2A869)
- **🔍 Filtros Avanzados**: Por región, especialidad, dependencia, género, zona
- **👥 Perfiles de Usuario**: Modo Usuario (acceso directo) y Modo Admin (con autenticación)
- **🌓 Tema Claro/Oscuro**: Cambio de tema visual
- **📱 Responsive**: Funciona en desktop, tablet y móvil
- **🔐 Autenticación Segura**: Sistema de login con bcrypt

### 📚 Módulos de Análisis
- **📈 Matrícula EMTP**: Evolución, demografía, retención, comparación
- **🎓 Egresados**: Transición a educación superior, empleabilidad
- **🏅 Titulación**: Tasas y tiempos de titulación
- **🏫 Establecimientos**: Distribución geográfica e infraestructura
- **👨‍🏫 Docentes**: Perfil profesional y capacitación
- **🗺️ Mapas**: Visualización geográfica de matrícula y establecimientos por región
- **📋 Proyectos SEEMTP**: Financiamiento e impacto (solo Admin)

### 🔑 Credenciales de Acceso

**Modo Usuario**: Acceso directo sin contraseña (funcionalidad limitada)

**Modo Administrador**:
- Usuario: `admin`
- Contraseña: `admin123`
- Acceso completo a todas las secciones

---

## 🗺️ Nuevo: Mapas Geográficos

### Características de los Mapas
- **✅ GeoJSON Real**: Utiliza geometría auténtica de Chile desde [fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON)
- **✅ Mapas Choropleth**: Regiones coloreadas según intensidad de datos
- **✅ 16 Regiones**: Cobertura completa del territorio nacional
- **✅ Colores Degradados**: Escalas de color institucionales
- **✅ Interactividad**: Tooltips con información detallada al pasar el cursor
- **✅ Dos Visualizaciones**:
  - Mapa de Matrícula EMTP por región
  - Mapa de Establecimientos por región

### Tecnología de Mapas
- **Plotly Choropleth Mapbox**: Visualizaciones geográficas profesionales
- **OpenStreetMap**: Capa base de mapa
- **GeoJSON Dinámico**: Carga en tiempo real desde repositorio público
- **Geometría Realista**: Coastlines, borders y fronteras reales de Chile

---

##  Arquitectura del Proyecto

### Estructura de Archivos

```
VisualizadorEMTP-Dash/
├── app_v2.py                    # 🚀 Punto de entrada principal
├── requirements.txt             # 📦 Dependencias Python
├── README.md                    # 📖 Documentación
│
├── assets/                      # 🎨 Recursos estáticos
│   ├── custom.css              # Estilos institucionales Shiny
│   ├── navigation.js           # Script para navegación activa
│   └── theme.js                # JavaScript para temas
│
├── config/                      # ⚙️ Configuración
│   ├── __init__.py
│   └── settings.py             # Variables de entorno
│
├── data/                        # 📊 Datos
│   └── processed/              # CSV con datos simulados
│       ├── matricula_simulada.csv
│       ├── egresados_simulados.csv
│       ├── titulacion_simulada.csv
│       ├── establecimientos_simulados.csv
│       ├── docentes_simulados.csv
│       └── proyectos_simulados.csv
│
├── src/                         # 💻 Código fuente
│   ├── callbacks/              # 🔄 Lógica de interacción
│   │   ├── auth_callbacks.py   # Autenticación y perfiles
│   │   ├── sidebar_callbacks.py # Navegación, filtros y mapas
│   │   └── theme_callbacks.py  # Cambio de tema
│   │
│   ├── layouts/                # 🖼️ Interfaces visuales
│   │   ├── login_layout.py     # Pantalla de login
│   │   ├── welcome_screen.py   # Pantalla de bienvenida
│   │   ├── sidebar_layout_clean.py  # Layout principal con sidebar
│   │   ├── mapas.py            # 🗺️ Layout de mapas geográficos
│   │   └── real_data_content.py     # Contenido con datos
│   │
│   └── utils/                  # 🛠️ Utilidades
│       ├── auth.py             # Gestión de autenticación
│       ├── helpers.py          # Funciones auxiliares
│       └── rate_limiter.py     # Control de acceso
│
└── logs/                        # 📝 Logs de la aplicación
    └── app.log
```

### Flujo de la Aplicación

```
┌─────────────────────────────────────────────────────────────┐
│                    app_v2.py (Inicio)                       │
│  - Inicializa Dash                                          │
│  - Configura logging                                        │
│  - Registra callbacks                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
    ┌────▼─────┐              ┌───────▼────────┐
    │ Usuario  │              │  Administrador │
    │ (directo)│              │  (con login)   │
    └────┬─────┘              └───────┬────────┘
         │                            │
         └──────────┬─────────────────┘
                    │
         ┌──────────▼──────────┐
         │  Dashboard Sidebar  │
         │  - Navegación       │
         │  - Filtros          │
         │  - Visualizaciones  │
         └─────────────────────┘
```

---

## Guía de Instalación Detallada

### Requisitos del Sistema

- **Python**: 3.10 o superior ([Descargar](https://www.python.org/downloads/))
- **pip**: Incluido con Python
- **Git**: Para clonar el repositorio ([Descargar](https://git-scm.com/))
- **Navegador web**: Chrome, Firefox, Safari o Edge (versiones actuales)

### Instalación Paso a Paso

#### 1. Clonar el repositorio

```bash
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python
```

#### 2. Crear entorno virtual

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat
```

#### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configuración (Opcional)

Para personalizar configuraciones, crea un archivo `.env`:

```bash
# Copiar plantilla
cp .env.example .env

# Editar con tu editor favorito
nano .env  # o code .env, vim .env, etc.
```

Variables disponibles:
```env
PORT=8051                    # Puerto de la aplicación
DEBUG=False                  # Modo debug (desactivar en producción)
LOG_LEVEL=INFO              # Nivel de logs (DEBUG, INFO, WARNING, ERROR)
```

#### 5. Ejecutar la aplicación

```bash
python app_v2.py
```

Verás un mensaje como:
```
Iniciando Visualizador EMTP v2.0
Entorno: development
Host: 0.0.0.0:8051
Datos: Simulados con 36k+ registros

Dash is running on http://0.0.0.0:8051/
```

#### 6. Acceder a la aplicación

Abre tu navegador en: **http://localhost:8051**

---

## Configuración Avanzada

### Variables de Entorno

Archivo `.env` (opcional):

```env
# Aplicación
APP_NAME=Visualizador EMTP
ENVIRONMENT=development
PORT=8051
DEBUG=False

# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=otra-clave-secreta
JWT_EXPIRATION_HOURS=24

# Autenticación
AUTH_ENABLED=True
ADMIN_USERNAME=admin

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_BACKUP_COUNT=5

# Datos
LOCAL_DATA_ENABLED=True
```

### Personalización de Puerto

Si el puerto 8051 está ocupado:

```bash
# Opción 1: Variable de entorno
PORT=8052 python app_v2.py

# Opción 2: Editar .env
echo "PORT=8052" > .env
python app_v2.py
```

### Modo Producción

Para ejecutar en producción, usa un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn app_v2:server -b 0.0.0.0:8051 --workers 4
```

---

## Datos y Fuentes

### Datos Simulados

La aplicación incluye datos simulados (por IA) del sistema EMTP chileno:

- **36,411 registros** totales
- **Período**: 2015-2024 (10 años)
- **16 regiones** de Chile
- **17 especialidades** técnicas
- **3 tipos de dependencia**: Municipal, Particular Subvencionado, Particular

Los datos se encuentran en `data/processed/` en formato CSV:
- `matricula_simulada.csv` - Datos de matrícula por año, región y especialidad
- `egresados_simulados.csv` - Transición a educación superior
- `titulacion_simulada.csv` - Tasas y tiempos de titulación
- `establecimientos_simulados.csv` - Infraestructura educativa
- `docentes_simulados.csv` - Perfil del cuerpo docente
- `proyectos_simulados.csv` - Financiamiento SEEMTP

### Integración con Datos Reales

El sistema está preparado para conectarse a fuentes de datos reales:

- **SQL Server** (configurar en `.env`)
- **PostgreSQL** (configurar en `.env`)
- **SharePoint** (configurar en `.env`)
- **CSV/Excel** locales (en `data/raw/`)

Para más detalles, consulta `config/settings.py`.

---

## Solución de Problemas (FAQ)

### Errores Comunes

#### "ModuleNotFoundError: No module named 'dash'"
```bash
# Solución: Activar entorno virtual e instalar dependencias
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### "Address already in use" / Puerto ocupado
```bash
# Solución 1: Liberar el puerto (macOS/Linux)
lsof -ti:8051 | xargs kill -9

# Solución 2: Usar otro puerto
PORT=8052 python app_v2.py
```

#### "DuplicateIdError: 'session-store'"
**Causa**: Múltiples definiciones del mismo `dcc.Store`  
**Solución**: Ya está corregido en la versión actual. El store solo existe en `app_v2.py`

#### "No se muestran datos" / Gráficos vacíos
**Causa**: Archivos CSV faltantes en `data/processed/`  
**Solución**: Los CSVs simulados deberían estar en el repositorio. Si faltan, la app mostrará placeholders.

### Ayuda Adicional

Si el problema persiste:

1. **Revisa los logs**: `logs/app.log`
2. **Modo verbose**: `LOG_LEVEL=DEBUG` en `.env`
3. **Abre un issue**: [GitHub Issues](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)

---

## Roadmap y Próximos Pasos

- [ ] Exportación de reportes (PDF/Excel)
- [ ] Mapas geográficos interactivos
- [ ] Comparación entre períodos
- [ ] Sistema de alertas
- [ ] API REST
- [ ] Deployment en la nube

---

## Recursos

- **Dash**: https://dash.plotly.com/
- **Plotly**: https://plotly.com/python/

---

## Créditos

**Desarrollado por**: Andrés Lazcano  
**Año**: 2025

**Stack tecnológico**:
- Python 3.12+ • Dash 2.x • Plotly • Pandas
- Dash Bootstrap • Loguru • bcrypt

---

## Licencia

Proyecto bajo Licencia MIT.

---

## Contacto

- **GitHub**: [@andreslazcano-bit](https://github.com/andreslazcano-bit)
- **Repositorio**: [Visualizador-EMTP-Dash](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python)
- **Issues**: [Reportar problema](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)

---

</div>

---

## Seguridad

- Autenticación con bcrypt
- Variables de entorno para credenciales
- HTTPS en producción
- Rate limiting
- Logging de accesos

---
## Documentación
Este repositorio fue simplificado para centrarse en la versión v2. La documentación se concentra en este README.

---
