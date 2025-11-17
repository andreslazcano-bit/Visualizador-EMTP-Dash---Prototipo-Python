# Visualizador EMTP v2.0

Sistema integral de análisis y visualización de datos del Sistema de Educación Media Técnico-Profesional de Chile.

[![Dash](https://img.shields.io/badge/Dash-2.14.2-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-orange.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Ejecutar aplicación
python app_v2.py
```

La aplicación estará disponible en: **http://localhost:8051**

## Descripción

Plataforma web interactiva para análisis de datos del sistema de Educación Media Técnico-Profesional de Chile. Permite visualizar datos mediante dashboards, mapas geográficos y generar reportes exportables.

### Características Principales

- **Dashboards Interactivos**: Análisis de matrícula, egresados, titulación, establecimientos y docentes
- **Mapas Geográficos**: Visualización territorial de 16 regiones y 345 comunas
- **Integración Power BI**: Espacio dedicado para dashboards externos (RFT 2025-2026)
- **Gestión de Usuarios**: Sistema con perfiles (actualmente Usuario y Admin)
- **Auditoría**: Registro completo de accesos y acciones
- **Seguridad**: Autenticación bcrypt + SQLite + Timeout de sesión automático
- **Interfaz Adaptable**: Tema claro/oscuro, responsive para desktop, tablet y móvil

## Acceso al Sistema

### Modo Usuario
- Acceso sin contraseña
- Disponible: Matrícula, Egresados, Titulación, Docentes, Establecimientos, Mapas

### Modo Administrador
- Usuario: `admin`
- Contraseña: `admin123` (cambiar en primer acceso)
- Acceso adicional: Gestión de Usuarios, Auditoría, Proyectos EMTP

## Estructura del Proyecto

```
Visualizador-EMTP-Dash/
├── app_v2.py                    # Aplicación principal
├── requirements.txt             # Dependencias Python
├── Dockerfile                   # Contenedor Docker
├── docker-compose.yml           # Orquestación Docker
│
├── config/                      # Configuración
│   ├── settings.py             # Variables de configuración
│   └── database.py             # Configuración de BD
│
├── src/                         # Código fuente
│   ├── callbacks/              # Lógica de interacción (Dash callbacks)
│   │   ├── auth_callbacks.py
│   │   ├── sidebar_callbacks.py
│   │   ├── user_management_callbacks.py
│   │   └── audit_callbacks.py
│   ├── layouts/                # Interfaces visuales
│   │   ├── sidebar_layout_clean.py
│   │   ├── login_layout.py
│   │   ├── user_management.py
│   │   └── audit.py
│   ├── data/                   # Cargadores y procesadores
│   │   └── loaders.py
│   └── utils/                  # Utilidades
│       ├── auth.py             # Autenticación
│       ├── user_management.py  # Gestión de usuarios
│       └── audit.py            # Sistema de auditoría
│
├── data/                        # Datos y base de datos
│   ├── users.db                # SQLite - Usuarios
│   ├── processed/              # Datos procesados (CSV/Parquet)
│   ├── geographic/             # GeoJSON de Chile
│   └── raw/                    # Datos fuente
│
├── docs/                        # Documentación técnica
│   ├── ARQUITECTURA_DETALLADA.md
│   ├── MANUAL_DESPLIEGUE.md    # Instalación y despliegue
│   ├── MANUAL_MANTENIMIENTO.md # Operaciones y mantenimiento
│   ├── SISTEMA_USUARIOS_AUDITORIA.md
│   └── INDICE.md               # Índice de documentación
│
├── logs/                        # Logs del sistema
│   ├── app.log                 # Logs generales
│   └── audit.jsonl             # Auditoría de accesos
│
├── assets/                      # Recursos estáticos
│   ├── custom.css              # Estilos personalizados
│   └── theme.js                # Tema claro/oscuro
│
└── scripts/                     # Scripts auxiliares
    ├── actualizar_datos_semanal.py
    └── test_connections.py
```

## Módulos Disponibles

| Módulo | Descripción | Acceso |
|--------|-------------|--------|
| Matrícula | Evolución, demografía, retención, comparación regional | Todos |
| Egresados | Transición a educación superior, empleabilidad | Todos |
| Titulación | Tasas y tiempos de titulación por especialidad | Todos |
| Establecimientos | Distribución geográfica e infraestructura | Todos |
| Docentes | Perfil profesional, capacitación | Todos |
| Mapas | Visualización territorial (regiones y comunas) | Todos |
| Proyectos EMTP | Gestión administrativa y fortalecimiento | Solo Admin |
| Gestión Usuarios | Crear, editar, desactivar usuarios | Solo Admin |
| Auditoría | Logs de accesos, estadísticas de uso | Solo Admin |

## Instalación Detallada

### Requisitos Previos

- Python 3.12 o superior
- pip (incluido con Python)
- 4 GB RAM mínimo (8 GB recomendado)
- 10 GB espacio en disco

### Instalación en Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar
python app_v2.py
```

### Instalación en Producción

Para despliegue en producción, consultar la documentación completa:

- [Manual de Despliegue](docs/MANUAL_DESPLIEGUE.md) - Instalación paso a paso para TI
- [Manual de Mantenimiento](docs/MANUAL_MANTENIMIENTO.md) - Backups, logs, troubleshooting

## Documentación

### Arquitectura y Diseño
- [Arquitectura Detallada](docs/ARQUITECTURA_DETALLADA.md) - Diseño completo del sistema
- [Arquitectura - Visión General](docs/ARQUITECTURA_VISION_GENERAL.md) - Vista de alto nivel
- [Diagramas de Flujos](docs/DIAGRAMA_FLUJOS_ARQUITECTURA.md) - Flujos de datos

### Manuales para TI
- [Manual de Despliegue](docs/MANUAL_DESPLIEGUE.md) - Instalación completa
- [Manual de Mantenimiento](docs/MANUAL_MANTENIMIENTO.md) - Operaciones día a día
- [Guía de Sostenibilidad](docs/GUIA_SOSTENIBILIDAD.md) - Plan de sostenibilidad y transición
- [⚠️ Pendiente: Actualización Datos](docs/PENDIENTE_ACTUALIZACION_DATOS.md) - Integración con MINEDUC

### Sistemas Implementados
- [Sistema de Usuarios y Auditoría](docs/SISTEMA_USUARIOS_AUDITORIA.md) - Implementación técnica
- [Configuración de Timeout de Sesión](docs/CONFIGURACION_TIMEOUT_SESION.md) - Sistema de timeout automático
- [Configuración Power BI RFT](docs/CONFIGURACION_POWERBI_RFT.md) - Integración de dashboards Power BI
- [Actualización Automática](docs/ACTUALIZACION_AUTOMATICA.md) - Sistema de actualización
- [Integración Completada](docs/INTEGRACION_COMPLETADA.md) - Estado del proyecto

### Navegación
- [Índice de Documentación](docs/INDICE.md) - Índice general
- [README de Documentación](docs/README.md) - Guía de navegación

## Seguridad

### Implementación

- Encriptación de contraseñas con bcrypt (12 rounds)
- Base de datos SQLite con protección contra SQL injection
- Control de acceso basado en roles (Usuario, Analista, Admin)
- **Timeout automático de sesión** (30 minutos de inactividad, configurable)
- **Re-autenticación obligatoria** para usuarios con privilegios
- Auditoría completa de accesos y acciones
- Gestión de sesiones con validación

### Buenas Prácticas

1. Cambiar contraseña de `admin` en primer acceso
2. Revisar logs de auditoría semanalmente
3. Configurar backups automáticos
4. Limitar acceso por IP (firewall)
5. Usar HTTPS en producción
6. Ajustar timeout de sesión según política de seguridad institucional

## Datos

### Estadísticas (SIMULADOS)

- 178,700+ registros de matrícula (2014-2024)
- 16 regiones de Chile
- 345 comunas con datos detallados
- 17 especialidades técnicas
- Actualización: Semanal (lunes 6:00 AM)

### Formato de Datos

- CSV para compatibilidad
- Parquet para optimización
- GeoJSON para mapas (desde [fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON))

## Deployment

### Docker (Recomendado)

```bash
# Construir imagen
docker build -t visualizador-emtp .

# Ejecutar contenedor
docker run -d -p 8051:8051 --name emtp-app visualizador-emtp
```

### Docker Compose

```bash
docker-compose up -d
```

### Servidor de Producción

**Linux (systemd):**
```bash
# Ver configuración completa en docs/MANUAL_DESPLIEGUE.md
sudo systemctl enable visualizador-emtp
sudo systemctl start visualizador-emtp
```

**Windows (NSSM):**
```cmd
# Ver configuración completa en docs/MANUAL_DESPLIEGUE.md
nssm install VisualizadorEMTP
```

## Testing

```bash
# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=src tests/
```

## Changelog

### v2.0.1 (17 Noviembre 2025)
- ✨ **Sistema de timeout de sesión automático** (30 min configurable)
- ✨ **Re-autenticación para admin/analista** después de timeout
- ✨ **Integración Power BI** para dashboard RFT 2025-2026
- 📄 Documentación completa de timeout y Power BI
- 🔒 Mejoras de seguridad en gestión de sesiones
- 📋 Registro de eventos de timeout en auditoría

### v2.0.0 (Noviembre 2025)
- Sistema de gestión de usuarios (CRUD completo)
- Sistema de auditoría de accesos y acciones
- Dashboard de auditoría con estadísticas
- Documentación completa de sostenibilidad
- Manuales para TI, usuarios y desarrolladores
- Mejoras de seguridad (bcrypt, SQLite)

### v1.0.0 (Octubre 2025)
- Lanzamiento inicial
- 7 módulos de dashboards
- Mapas geográficos (regiones y comunas)
- Autenticación básica
- Tema claro/oscuro

## Contacto

### Desarrollador
**Andrés Lazcano**  
ext.andres.lazcano@mineduc.cl  
[@andreslazcano-bit](https://github.com/andreslazcano-bit)

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## Autoría

**Desarrollado por:** [Andrés Lazcano](https://github.com/andreslazcano-bit)  
**Con colaboración de:** GitHub Copilot (GPT-4o) y Claude 3.5 Sonnet

Este proyecto combina experiencia humana en análisis de datos educacionales con asistencia de IA para arquitectura de software, documentación técnica y optimización de código.

---

## Links Rápidos

- [Documentación Completa](docs/INDICE.md)
- [Reportar un Bug](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)
- [Solicitar Feature](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues/new)
- [Wiki del Proyecto](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/wiki)

---

**Última actualización**: 17 Noviembre 2025 | **Versión**: 2.0.1
