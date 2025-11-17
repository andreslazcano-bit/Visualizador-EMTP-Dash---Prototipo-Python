# 📊 Visualizador EMTP v2.0

> Sistema integral de análisis y visualización de datos del Sistema de Educación Media Técnico-Profesional de Chile

[![Dash](https://img.shields.io/badge/Dash-2.14.2-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-orange.svg)](https://plotly.com/)
[![Status](https://img.shields.io/badge/Status-Producción-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

---

## 🚀 Inicio Rápido (3 pasos)

### 1️⃣ Clonar y preparar entorno

```bash
# Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate     # Windows
```

### 2️⃣ Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Ejecutar aplicación

```bash
python app_v2.py
```

✅ **¡Listo!** Abre tu navegador en: **http://localhost:8051**

---

## 📋 Características Principales

### ✨ Funcionalidades Core

- **📈 Visualización Interactiva**: Gráficos dinámicos con Plotly
- **🗺️ Mapas Geográficos**: Visualización territorial con GeoJSON real de Chile (16 regiones, 345 comunas)
- **🎨 Tema Claro/Oscuro**: Cambio dinámico de tema visual
- **📱 Responsive**: Optimizado para desktop, tablet y móvil
- **🔍 Filtros Avanzados**: Por región, comuna, especialidad, dependencia, género, zona
- **📊 Exportación de Datos**: PDF, Excel, CSV (próximamente)
- **🔒 Autenticación Segura**: Sistema bcrypt + SQLite

### 🆕 Nuevas Funcionalidades v2.0

- **👥 Gestión de Usuarios**: Sistema completo de administración de usuarios con 3 perfiles (Usuario, Analista, Admin)
- **📋 Auditoría de Accesos**: Registro completo de acciones, login/logout, exportaciones
- **🔐 Base de Datos de Usuarios**: SQLite con encriptación bcrypt (12 rounds)
- **📊 Dashboard de Auditoría**: Visualización de estadísticas de uso y seguridad

---

## 🎯 Módulos de Análisis

### Dashboards Principales

| Módulo | Submódulos | Acceso |
|--------|-----------|---------|
| **📚 Matrícula** | Evolución, Demografía, Retención, Comparación | Usuario, Analista, Admin |
| **🎓 Egresados** | Transición, Empleabilidad | Usuario, Analista, Admin |
| **📜 Titulación** | Tasas, Tiempos | Usuario, Analista, Admin |
| **🏫 Establecimientos** | Geografía, Infraestructura | Usuario, Analista, Admin |
| **👨‍🏫 Docentes** | Perfil, Capacitación | Usuario, Analista, Admin |
| **🗺️ Mapas** | Distribución Matrícula, Establecimientos | Usuario, Analista, Admin |
| **📊 Proyectos EMTP** | Gestión Administrativa, Fortalecimiento | **Solo Admin** |
| **👥 Gestión Usuarios** | CRUD completo de usuarios | **Solo Admin** |
| **📋 Auditoría** | Logs, Estadísticas, Seguridad | **Solo Admin** |

---

## 🔐 Credenciales de Acceso

### Modo Usuario (Público)
- **Acceso:** Click en "Acceso como Usuario"
- **Sin contraseña:** Acceso directo
- **Funcionalidad:** Dashboards básicos (Matrícula, Egresados, Titulación, Docentes, Establecimientos, Mapas)

### Modo Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123` ⚠️ **CAMBIAR EN PRIMER ACCESO**
- **Funcionalidad:** Acceso completo + Gestión Usuarios + Auditoría + Proyectos

> **⚠️ Importante:** En producción, cambiar inmediatamente la contraseña por defecto desde el menú "Gestión de Usuarios"

---

## 📁 Estructura del Proyecto

```
Visualizador-EMTP-Dash/
├── app_v2.py                    # Aplicación principal
├── requirements.txt             # Dependencias Python
├── requirements-dev.txt         # Dependencias de desarrollo
├── Dockerfile                   # Imagen Docker
├── docker-compose.yml           # Orquestación Docker
│
├── assets/                      # Recursos estáticos
│   └── custom.css              # Estilos personalizados
│
├── config/                      # Configuración
│   ├── __init__.py
│   ├── settings.py             # Variables de configuración
│   └── database.py             # Conexión BD (futuro)
│
├── data/                        # Datos
│   ├── users.db                # Base de datos de usuarios (SQLite)
│   ├── geographic/             # GeoJSON de Chile
│   ├── processed/              # Datos procesados (Parquet)
│   └── raw/                    # Datos originales
│
├── logs/                        # Logs del sistema
│   ├── app.log                 # Logs generales
│   └── audit.jsonl             # Logs de auditoría
│
├── src/                         # Código fuente
│   ├── callbacks/              # Callbacks de Dash
│   │   ├── auth_callbacks.py
│   │   ├── sidebar_callbacks.py
│   │   ├── user_management_callbacks.py
│   │   └── audit_callbacks.py
│   │
│   ├── components/             # Componentes reutilizables
│   │   ├── charts.py
│   │   ├── filters.py
│   │   └── tables.py
│   │
│   ├── layouts/                # Layouts de páginas
│   │   ├── main_layout.py
│   │   ├── sidebar_layout_clean.py
│   │   ├── user_management.py
│   │   └── audit.py
│   │
│   ├── utils/                  # Utilidades
│   │   ├── auth.py             # Autenticación
│   │   ├── user_management.py  # Gestión de usuarios
│   │   ├── audit.py            # Sistema de auditoría
│   │   └── helpers.py
│   │
│   └── data/                   # Procesamiento de datos
│       ├── loaders.py
│       └── processors.py
│
├── docs/                        # Documentación completa
│   ├── INDICE.md               # Índice general
│   ├── MANUAL_DESPLIEGUE.md    # Para TI (instalación)
│   ├── MANUAL_MANTENIMIENTO.md # Para TI (operaciones)
│   ├── MANUAL_USUARIO.md       # Para usuarios finales
│   ├── GUIA_RAPIDA.md          # Referencia rápida
│   ├── ARQUITECTURA.md         # Diseño técnico
│   ├── SISTEMA_USUARIOS_AUDITORIA.md
│   └── INTEGRACION_COMPLETADA.md
│
├── scripts/                     # Scripts auxiliares
│   ├── actualizar_datos_semanal.py
│   ├── convert_rds_to_parquet.py
│   └── test_connections.py
│
└── tests/                       # Tests unitarios
    ├── test_callbacks.py
    └── test_data.py
```

---

## 🛠️ Instalación Detallada

### Requisitos Previos

- **Python:** 3.12 o superior
- **Sistema Operativo:** Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)
- **RAM:** 4 GB mínimo, 8 GB recomendado
- **Disco:** 10 GB disponibles

### Instalación en Desarrollo

```bash
# 1. Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Ejecutar en modo desarrollo
python app_v2.py
```

### Instalación en Producción

**Ver documentación completa:** [`docs/MANUAL_DESPLIEGUE.md`](docs/MANUAL_DESPLIEGUE.md)

```bash
# 1. Configurar como servicio (Linux - systemd)
sudo cp deployment/visualizador-emtp.service /etc/systemd/system/
sudo systemctl enable visualizador-emtp
sudo systemctl start visualizador-emtp

# 2. Verificar estado
sudo systemctl status visualizador-emtp

# 3. Ver logs
sudo journalctl -u visualizador-emtp -f
```

**Para Windows:** Ver sección NSSM en el Manual de Despliegue

---

## 📚 Documentación Completa

### Para Diferentes Roles

| Documento | Audiencia | Contenido |
|-----------|-----------|-----------|
| [📘 Manual de Usuario](docs/MANUAL_USUARIO.md) | Secretaría, Analistas | Uso del sistema, dashboards, filtros, exportación |
| [🔧 Manual de Despliegue](docs/MANUAL_DESPLIEGUE.md) | TI (instalación) | Instalación paso a paso, sin necesidad de Python |
| [🛠️ Manual de Mantenimiento](docs/MANUAL_MANTENIMIENTO.md) | TI (operaciones) | Backups, logs, troubleshooting, emergencias |
| [⚡ Guía Rápida](docs/GUIA_RAPIDA.md) | Todos | Referencia rápida, comandos esenciales |
| [🏗️ Arquitectura](docs/ARQUITECTURA.md) | Desarrolladores | Diseño técnico, stack, componentes |
| [📋 Índice General](docs/INDICE.md) | Todos | Navegación por toda la documentación |

---

## 🔒 Seguridad

### Autenticación y Autorización

- **Encriptación de contraseñas:** bcrypt con 12 rounds
- **Base de datos:** SQLite con protección contra SQL injection
- **Control de acceso:** Basado en roles (Usuario, Analista, Admin)
- **Auditoría completa:** Registro de todos los accesos y acciones
- **Sesiones seguras:** Tokens JWT con expiración de 24 horas

### Buenas Prácticas

✅ Cambiar contraseña de admin por defecto  
✅ Revisar logs de auditoría semanalmente  
✅ Configurar backups automáticos  
✅ Limitar acceso por IP (firewall)  
✅ Usar HTTPS en producción

---

## 📊 Datos

### Fuentes de Datos

- **Matrícula:** 178,700+ registros (2014-2024)
- **Regiones:** 16 regiones de Chile
- **Comunas:** 345 comunas
- **Especialidades:** 17 especialidades técnicas
- **Formato:** CSV, Parquet (optimizado)

### Actualización de Datos

- **Frecuencia:** Semanal (lunes 6:00 AM)
- **Método:** Script automatizado (`scripts/actualizar_datos_semanal.py`)
- **Validación:** Automática con logging

---

## 🚀 Deployment

### Docker (Recomendado)

**Nivel 3: Sub-subpestañas** (ejemplo: Monitoreo de Proyectos)

*Gestión Administrativa y Financiera*:
- Convenios Activos
- Rendiciones

*Fortalecimiento EMTP*:
- Equipamiento Regular
- Equipamiento SLEP
- Red Futuro Técnico (RFT)
- Apoyo SLEP

### Beneficios de la Estructura
- **Organización Clara**: Información agrupada lógicamente
- **Navegación Intuitiva**: Breadcrumbs y menús desplegables
- **Escalabilidad**: Fácil agregar nuevas secciones
- **Rendimiento**: Carga bajo demanda (lazy loading)
- **Responsive**: Adaptable a diferentes dispositivos

---

## Nuevo: Mapas Geográficos Interactivos

### Características de los Mapas
- **Navegación por Pestañas**:
  - **Distribución de Matrícula**: Visualización de matrícula EMTP por territorio con tabla resumen
  - **Mapa de Establecimientos**: Distribución de establecimientos educativos con tabla resumen
- **Dos Niveles de Granularidad**:
  - **Regional**: 16 regiones de Chile con GeoJSON desde [fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON)
  - **Comunal**: 345 comunas con datos detallados
- **Mapas Choropleth**: Territorios coloreados según intensidad de datos
- **Colores Degradados**: Escalas de color institucionales de 5 puntos
  - Matrícula: Gradiente azul claro a oscuro (#E8EEF2 → #1e293b)
  - Establecimientos: Gradiente blanco a rojo oscuro (#FFFFFF → #8B3A3A)
- **Interactividad**: Tooltips con información detallada al pasar el cursor
- **Tablas Resumen Dinámicas**: Se actualizan automáticamente según la granularidad seleccionada
- **Filtros Integrados**:
  - **Filtro de Región**: Selector regional en sidebar
  - **Filtro de Comuna**: Selector comunal dinámico (se actualiza según región seleccionada)
  - **Granularidad**: Selector para cambiar entre vista regional y comunal

### Tecnología de Mapas
- **Plotly Choropleth Mapbox**: Visualizaciones geográficas profesionales
- **OpenStreetMap**: Capa base de mapa
- **GeoJSON Dinámico**: 
  - Regiones: Carga desde GitHub (fcortes/Chile-GeoJSON)
  - Comunas: Carga desde GitHub (fcortes/Chile-GeoJSON)
- **Geometría Oficial**: 
  - 16 regiones con códigos de región (1-16)
  - 345 comunas con códigos comunales
- **GeoPandas**: Procesamiento de datos geoespaciales
- **142,000+ registros comunales**: Datos simulados distribuidos estadísticamente
- **Caché Inteligente**: @lru_cache para optimizar carga de GeoJSON

### Fuentes de Datos Geográficos
- **Regiones**: [https://github.com/fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON) - Regional.geojson
- **Comunas**: [https://github.com/fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON) - comunas.geojson
- **Datos de Matrícula**: 142,289 registros simulados con distribución estadística realista por comuna
- **Datos de Establecimientos**: Distribución simulada de establecimientos EMTP por región y comuna

---

## Arquitectura del Proyecto

### Estructura de Archivos

```
VisualizadorEMTP-Dash/
├── app_v2.py                    # Punto de entrada principal
├── requirements.txt             # Dependencias Python
├── README.md                    # Documentación
│
├── assets/                      # Recursos estáticos
│   ├── custom.css              # Estilos institucionales Shiny
│   ├── navigation.js           # Script para navegación activa
│   └── theme.js                # JavaScript para temas
│
├── config/                      # Configuración
│   ├── __init__.py
│   └── settings.py             # Variables de entorno
│
├── data/                        # Datos
│   └── processed/              # CSV con datos simulados
│       ├── matricula_simulada.csv          # Datos regionales (36k registros)
│       ├── matricula_comunal_simulada.csv  # Datos comunales (142k registros)
│       ├── egresados_simulados.csv
│       ├── titulacion_simulada.csv
│       ├── establecimientos_simulados.csv
│       ├── docentes_simulados.csv
│       └── proyectos_simulados.csv
│
├── scripts/                     # Scripts de utilidad
│   ├── generate_comunal_data.py  # Generador de datos comunales
│   └── test_connections.py
│
├── src/                         # Código fuente
│   ├── callbacks/              # Lógica de interacción
│   │   ├── auth_callbacks.py   # Autenticación y perfiles
│   │   ├── sidebar_callbacks.py # Navegación, filtros y contenido
│   │   ├── mapas_callbacks.py  # Interactividad de mapas
│   │   └── theme_callbacks.py  # Cambio de tema
│   │
│   ├── layouts/                # Interfaces visuales
│   │   ├── login_layout.py     # Pantalla de login
│   │   ├── welcome_screen.py   # Pantalla de bienvenida
│   │   ├── sidebar_layout_clean.py  # Layout principal con sidebar
│   │   ├── mapas.py            # Layout de mapas geográficos con tabs
│   │   └── real_data_content.py     # Contenido con datos
│   │
│   └── utils/                  # Utilidades
│       ├── auth.py             # Gestión de autenticación
│       ├── helpers.py          # Funciones auxiliares
│       └── rate_limiter.py     # Control de acceso
│
└── logs/                        # Logs de la aplicación
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

La aplicación incluye datos simulados del sistema EMTP chileno:

**Datos Regionales**:
- **36,411 registros** totales
- **Período**: 2015-2024 (10 años)
- **16 regiones** de Chile
- **17 especialidades** técnicas
- **3 tipos de dependencia**: Municipal, Particular Subvencionado, Particular

**Datos Comunales** (para mapas):
- **142,289 registros** de matrícula
- **345 comunas** de Chile
- Distribución estadística realista por territorio
- Datos sincronizados con códigos oficiales de región y comuna

Los datos se encuentran en `data/processed/` en formato CSV:
- `matricula_simulada.csv` - Datos de matrícula regionales por año y especialidad
- `matricula_comunal_simulada.csv` - Datos de matrícula a nivel comunal (para mapas)
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

### Funcionalidades Implementadas ✅
- [x] Mapas geográficos interactivos (regional y comunal)
- [x] Visualización choropleth con GeoJSON oficial
- [x] Sistema de pestañas jerárquicas (3 niveles)
- [x] Filtros dinámicos (región → comuna)
- [x] Tablas resumen actualizables
- [x] Paleta de colores institucional
- [x] Sistema de navegación completo
- [x] Estructura modular y escalable

### En Desarrollo 🚧
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Comparación entre períodos temporales
- [ ] Sistema de alertas y notificaciones
- [ ] API REST para integración externa
- [ ] Dashboard de métricas en tiempo real

### Futuras Mejoras 📋
- [ ] Deployment en la nube (AWS/Azure)
- [ ] Integración con bases de datos reales
- [ ] Visualizaciones predictivas con ML
- [ ] Sistema de usuarios y roles avanzado
- [ ] Caché distribuido (Redis)
- [ ] Tests automatizados (pytest)

---

## Recursos y Referencias

### Documentación Oficial
- **Dash Framework**: https://dash.plotly.com/
- **Plotly Graphing**: https://plotly.com/python/
- **Dash Bootstrap Components**: https://dash-bootstrap-components.opensource.faculty.ai/
- **Pandas**: https://pandas.pydata.org/
- **GeoPandas**: https://geopandas.org/

### Datos Geográficos
- **Chile GeoJSON**: https://github.com/fcortes/Chile-GeoJSON (fcortes)
  - Regional.geojson (16 regiones)
  - comunas.geojson (345 comunas)

### Herramientas de Desarrollo
- **VS Code**: https://code.visualstudio.com/
- **Git**: https://git-scm.com/
- **Python**: https://www.python.org/

---

## Créditos y Agradecimientos

**Desarrollado por**: Andrés Lazcano  
**Año**: 2025  
**Organización**: Ministerio de Educación de Chile

### Stack Tecnológico
- **Backend**: Python 3.12+
- **Framework**: Dash 2.x
- **Visualización**: Plotly 5.18+
- **UI Components**: Dash Bootstrap Components
- **Data Processing**: Pandas, GeoPandas
- **Mapas**: Plotly Choropleth Mapbox
- **Autenticación**: bcrypt
- **Logging**: Loguru
- **Geográficos**: fcortes/Chile-GeoJSON

### Agradecimientos Especiales
- **fcortes** por los archivos GeoJSON de Chile
- **Plotly Team** por el excelente framework Dash
- **Comunidad Python** por las bibliotecas de código abierto

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
