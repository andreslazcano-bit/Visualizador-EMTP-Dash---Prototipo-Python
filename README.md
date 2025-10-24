# 📊 Visualizador EMTP - Dash (Python) — Versión v2 (Sidebar)

> Aplicación web interactiva para explorar y analizar datos de Enseñanza Media Técnico Profesional en Chile - Versión Python/Dash

[![Dash](https://img.shields.io/badge/Dash-3.x-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-En_Desarrollo-yellow.svg)]()

---

## ⚡ Quickstart (2 minutos)

1) Crear y activar entorno virtual (macOS/Linux):

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Instalar dependencias:

```bash
pip install -r requirements.txt
```

3) Variables de entorno (opcional):

```bash
cp .env.example .env
# Edita .env si quieres cambiar puerto, modo DEBUG u orígenes de datos
```

4) Ejecutar app:

```bash
python app_v2.py
```

La aplicación quedará disponible en: http://localhost:8051

5) Compartir por Internet (ngrok, opcional):

```bash
ngrok http 8051
```

Comparte la URL pública que muestra ngrok (https://xxxx.ngrok-free.dev)

---

## 🌟 ¿Qué incluye esta versión?

- Layout con barra lateral, filtros y navegación por secciones
- Datos simulados cargados desde `data/processed/*.csv`
- Autenticación básica (modo Usuario y modo Admin con contraseña `admin123`)
- Modo claro/oscuro

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

## 🏗️ Estructura mínima activa

```
VisualizadorEMTP-Dash/
├── app_v2.py
├── assets/
│   ├── custom.css
│   └── theme.js
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   └── processed/    # CSV simulados (necesarios)
├── src/
│   ├── callbacks/
│   │   ├── auth_callbacks.py
│   │   ├── sidebar_callbacks.py
│   │   └── theme_callbacks.py
│   ├── layouts/
│   │   ├── login_layout.py
│   │   ├── real_data_content.py
│   │   ├── sidebar_layout_clean.py
│   │   └── welcome_screen.py
│   └── utils/
│       ├── auth.py
│       └── helpers.py
├── requirements.txt
└── README.md
```

---

## 💻 Instalación y ejecución

### Requisitos Previos

- **Python** >= 3.9 ([Descargar](https://www.python.org/))
- **pip** (incluido con Python)
- **Git** (opcional)

### Instalación Local

1. **Crear el entorno virtual**
```bash
python3 -m venv venv
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
python app_v2.py
```

Disponible en: `http://localhost:8051`

### Compartir públicamente (ngrok)

```bash
ngrok http 8051
```

Si ves errores de ngrok tipo ERR_NGROK_8012, asegúrate de que la app esté corriendo localmente primero.

---

## 🔧 Datos

Los CSV simulados se leen desde `data/processed/`. Si faltan, el sistema mostrará contenido de respaldo (placeholders).

---

## 🚀 Compartir rápido (ngrok)
1. Abre una segunda terminal y ejecuta:
```bash
ngrok http 8051
```
2. Comparte la URL pública que entrega ngrok.

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

## 🤝 Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

---

## 📄 Licencia

[Definir licencia según institución]

  