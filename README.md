# 📊 Visualizador EMTP - Dashboard Python/Dash

> Sistema de análisis y visualización interactiva de datos del Sistema de Educación Media Técnico-Profesional de Chile

[![Dash](https://img.shields.io/badge/Dash-3.x-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Funcional-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

--- "ngrok ERR_NGROK_8012 (connect refused)": inicia primero la app local (http://localhost:8051) y luego ejecuta `ngrok http 8051` en otra terminal.
- "Puerto en uso (Address already in use)": liberar con `lsof -ti:8051 | xargs kill -9` o usar otro puerto en `.env` (variable `PORT`).

## ⚡ Inicio Rápido (3 pasos)

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

### 🌐 Compartir temporalmente (opcional)

Si quieres compartir tu aplicación por Internet temporalmente:

```bash
# En otra terminal (mientras app_v2.py sigue corriendo)
ngrok http 8051
```

Comparte la URL pública que muestra ngrok (ej: `https://xxxx.ngrok-free.app`)

---

## � Características Principales

### ✨ Funcionalidades
- **📊 Visualización Interactiva**: Gráficos dinámicos con Plotly
- **🔍 Filtros Avanzados**: Por región, especialidad, dependencia, género, zona
- **👥 Perfiles de Usuario**: Modo Usuario (acceso directo) y Modo Admin (con autenticación)
- **🌓 Tema Claro/Oscuro**: Cambio de tema visual
- **� Responsive**: Funciona en desktop, tablet y móvil
- **� Autenticación Segura**: Sistema de login con bcrypt

### 📈 Módulos de Análisis
- **Matrícula EMTP**: Evolución, demografía, retención, comparación
- **Egresados**: Transición a educación superior, empleabilidad
- **Titulación**: Tasas y tiempos de titulación
- **Establecimientos**: Distribución geográfica e infraestructura
- **Docentes**: Perfil profesional y capacitación
- **Proyectos SEEMTP**: Financiamiento e impacto (solo Admin)

### � Credenciales de Acceso

**Modo Usuario**: Acceso directo sin contraseña (funcionalidad limitada)

**Modo Administrador**:
- Usuario: `admin`
- Contraseña: `admin123`
- Acceso completo a todas las secciones

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Archivos

```
VisualizadorEMTP-Dash/
├── app_v2.py                    # 🚀 Punto de entrada principal
├── requirements.txt             # 📦 Dependencias Python
├── README.md                    # 📖 Documentación
│
├── assets/                      # 🎨 Recursos estáticos
│   ├── custom.css              # Estilos personalizados
│   └── theme.js                # JavaScript para temas
│
├── config/                      # ⚙️ Configuración
│   ├── __init__.py
│   └── settings.py             # Variables de entorno y configuración
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
│   │   ├── sidebar_callbacks.py # Navegación y filtros
│   │   └── theme_callbacks.py  # Cambio de tema
│   │
│   ├── layouts/                # 🖼️ Interfaces visuales
│   │   ├── login_layout.py     # Pantalla de login
│   │   ├── welcome_screen.py   # Pantalla de bienvenida
│   │   ├── sidebar_layout_clean.py  # Layout principal con sidebar
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

## 💻 Guía de Instalación Detallada

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
🚀 Iniciando Visualizador EMTP v2.0
📊 Entorno: development
🌐 Host: 0.0.0.0:8051
📁 Datos: Simulados con 36k+ registros

Dash is running on http://0.0.0.0:8051/
```

#### 6. Acceder a la aplicación

Abre tu navegador en: **http://localhost:8051**

---

## 🌐 Compartir la Aplicación

### Opción 1: Red Local

La aplicación es accesible desde otros dispositivos en tu red local:

```
http://[TU-IP-LOCAL]:8051
```

Para conocer tu IP local:
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr IPv4
```

### Opción 2: Internet (ngrok)

Para compartir temporalmente por Internet:

1. **Instalar ngrok** ([Descargar](https://ngrok.com/download))

2. **Ejecutar ngrok** (en otra terminal, mientras la app corre):
```bash
ngrok http 8051
```

3. **Compartir la URL pública**:
```
Forwarding: https://abcd-1234.ngrok-free.app -> http://localhost:8051
```

⚠️ **Nota**: La URL de ngrok cambia cada vez que reinicias ngrok. Para URLs permanentes, considera [ngrok Pro](https://ngrok.com/pricing) o un servicio de hosting.

---

## 🔧 Configuración Avanzada

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

## � Datos y Fuentes

### Datos Simulados

La aplicación incluye datos simulados basados en estadísticas reales del sistema EMTP chileno:

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

## 🛠️ Solución de Problemas (FAQ)

### Errores Comunes

#### ❌ "ModuleNotFoundError: No module named 'dash'"
```bash
# Solución: Activar entorno virtual e instalar dependencias
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### ❌ "Address already in use" / Puerto ocupado
```bash
# Solución 1: Liberar el puerto (macOS/Linux)
lsof -ti:8051 | xargs kill -9

# Solución 2: Usar otro puerto
PORT=8052 python app_v2.py
```

#### ❌ "DuplicateIdError: 'session-store'"
**Causa**: Múltiples definiciones del mismo `dcc.Store`  
**Solución**: Ya está corregido en la versión actual. El store solo existe en `app_v2.py`

#### ❌ ngrok "ERR_NGROK_8012" (conexión rechazada)
**Causa**: La aplicación no está corriendo  
**Solución**:
1. Verifica que `app_v2.py` esté ejecutándose
2. Abre http://localhost:8051 para confirmar
3. Luego ejecuta `ngrok http 8051` en otra terminal

#### ❌ "No se muestran datos" / Gráficos vacíos
**Causa**: Archivos CSV faltantes en `data/processed/`  
**Solución**: Los CSVs simulados deberían estar en el repositorio. Si faltan, la app mostrará placeholders.

### Ayuda Adicional

Si el problema persiste:

1. **Revisa los logs**: `logs/app.log`
2. **Modo verbose**: `LOG_LEVEL=DEBUG` en `.env`
3. **Abre un issue**: [GitHub Issues](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)

---

## 🚀 Roadmap y Próximos Pasos

- [ ] Exportación de reportes (PDF/Excel)
- [ ] Mapas geográficos interactivos
- [ ] Comparación entre períodos
- [ ] Sistema de alertas
- [ ] API REST
- [ ] Deployment en la nube

---

## 📚 Recursos

- **Dash**: https://dash.plotly.com/
- **Plotly**: https://plotly.com/python/
- **MINEDUC**: https://www.mineduc.cl/

---

## 👥 Créditos

**Desarrollado por**: Andrés Lazcano  
**Año**: 2025

**Stack tecnológico**:
- Python 3.12+ • Dash 2.x • Plotly • Pandas
- Dash Bootstrap • Loguru • bcrypt

---

## 📄 Licencia

Proyecto bajo Licencia MIT.

---

## 🤝 Contacto

- **GitHub**: [@andreslazcano-bit](https://github.com/andreslazcano-bit)
- **Repositorio**: [Visualizador-EMTP-Dash](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python)
- **Issues**: [Reportar problema](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)

---

</div>

---

## 🔐 Seguridad

- Autenticación con bcrypt
- Variables de entorno para credenciales
- HTTPS en producción
- Rate limiting
- Logging de accesos

---
## 📝 Documentación
Este repositorio fue simplificado para centrarse en la versión v2. La documentación se concentra en este README.

---

## 🧰 Solución de problemas (FAQ)

- “DuplicateIdError: `session-store`”: se consolidó el `dcc.Store(id="session-store")` sólo en `app_v2.py`. No debe aparecer en otros layouts.
- “ngrok ERR_NGROK_8012 (connect refused)”: inicia primero la app local (http://localhost:8051) y luego ejecuta `ngrok http 8051` en otra terminal.
- “Puerto en uso (Address already in use)”: liberar con `lsof -ti:8051 | xargs kill -9` o usar otro puerto en `.env` (variable `PORT`).

  