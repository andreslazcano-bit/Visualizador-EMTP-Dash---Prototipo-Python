# 📊 Visualizador EMTP v2.0

> Sistema integral de análisis y visualización de datos del Sistema de Educación Media Técnico-Profesional de Chile

[![Dash](https://img.shields.io/badge/Dash-2.14.2-blue.svg)](https://dash.plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-orange.svg)](https://plotly.com/)
[![Status](https://img.shields.io/badge/Status-Producción-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# 2. Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Ejecutar aplicación
python app_v2.py
```

✅ **¡Listo!** Abre tu navegador en: **http://localhost:8051**

---

## 📋 Descripción

El **Visualizador EMTP** es una plataforma web interactiva que permite analizar datos del sistema de Educación Media Técnico-Profesional de Chile mediante dashboards, mapas geográficos y reportes exportables.

### Principales Características

- 📈 **Dashboards Interactivos**: Análisis de matrícula, egresados, titulación, establecimientos y docentes
- 🗺️ **Mapas Geográficos**: Visualización territorial de 16 regiones y 345 comunas
- 👥 **Gestión de Usuarios**: Sistema completo con 3 perfiles (Usuario, Analista, Admin)
- 📋 **Auditoría**: Registro completo de accesos y acciones de usuarios
- 🔐 **Seguridad**: Autenticación bcrypt + SQLite
- 🎨 **Tema Claro/Oscuro**: Interfaz adaptable
- 📱 **Responsive**: Optimizado para desktop, tablet y móvil

---

## 🔐 Acceso al Sistema

### Modo Usuario (Público)
- **Sin contraseña** - Acceso directo
- **Dashboards básicos**: Matrícula, Egresados, Titulación, Docentes, Establecimientos, Mapas

### Modo Administrador
- **Usuario**: `admin`
- **Contraseña**: `admin123` ⚠️ *Cambiar en primer acceso*
- **Funciones adicionales**: Gestión de Usuarios + Auditoría + Proyectos EMTP

---

## 📁 Estructura del Proyecto

```
Visualizador-EMTP-Dash/
├── app_v2.py                    # Aplicación principal ⭐
├── requirements.txt             # Dependencias Python
│
├── src/                         # Código fuente
│   ├── callbacks/              # Lógica de interacción
│   ├── layouts/                # Interfaces visuales
│   ├── components/             # Componentes reutilizables
│   └── utils/                  # Utilidades (auth, audit, etc.)
│
├── data/                        # Datos y base de datos
│   ├── users.db                # SQLite - Usuarios
│   ├── processed/              # Datos procesados (CSV/Parquet)
│   └── geographic/             # GeoJSON de Chile
│
├── docs/                        # 📚 Documentación completa
│   ├── MANUAL_USUARIO.md       # Para usuarios finales
│   ├── MANUAL_DESPLIEGUE.md    # Para TI (instalación)
│   ├── MANUAL_MANTENIMIENTO.md # Para TI (operaciones)
│   ├── GUIA_RAPIDA.md          # Referencia rápida
│   └── INDICE.md               # Índice general
│
├── logs/                        # Logs del sistema
│   ├── app.log                 # Logs generales
│   └── audit.jsonl             # Auditoría de accesos
│
└── scripts/                     # Scripts auxiliares
    ├── actualizar_datos_semanal.py
    └── test_connections.py
```

---

## 📊 Módulos Disponibles

| Módulo | Descripción | Acceso |
|--------|-------------|--------|
| **📚 Matrícula** | Evolución, demografía, retención, comparación regional | Todos |
| **🎓 Egresados** | Transición a educación superior, empleabilidad | Todos |
| **📜 Titulación** | Tasas y tiempos de titulación por especialidad | Todos |
| **🏫 Establecimientos** | Distribución geográfica e infraestructura | Todos |
| **👨‍🏫 Docentes** | Perfil profesional, capacitación | Todos |
| **🗺️ Mapas** | Visualización territorial (regiones y comunas) | Todos |
| **📊 Proyectos EMTP** | Gestión administrativa y fortalecimiento | Solo Admin |
| **👥 Gestión Usuarios** | Crear, editar, desactivar usuarios | Solo Admin |
| **📋 Auditoría** | Logs de accesos, estadísticas de uso | Solo Admin |

---

## 🛠️ Instalación Detallada

### Requisitos Previos

- Python 3.12 o superior
- pip (incluido con Python)
- 4 GB RAM mínimo (8 GB recomendado)
- 10 GB espacio en disco

### Instalación en Desarrollo

```bash
# 1. Clonar repositorio
git clone https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python.git
cd Visualizador-EMTP-Dash---Prototipo-Python

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# 4. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 5. Ejecutar
python app_v2.py
```

### Instalación en Producción

Para despliegue en producción, consultar la **documentación completa**:

📘 **[Manual de Despliegue](docs/MANUAL_DESPLIEGUE.md)** - Instalación paso a paso para TI  
🛠️ **[Manual de Mantenimiento](docs/MANUAL_MANTENIMIENTO.md)** - Backups, logs, troubleshooting

---

## 📚 Documentación

### Para Usuarios Finales
- 📘 **[Manual de Usuario](docs/MANUAL_USUARIO.md)** - Cómo usar el sistema (30 páginas)
- ⚡ **[Guía Rápida](docs/GUIA_RAPIDA.md)** - Referencia rápida (6 páginas)

### Para TI (sin conocimientos Python)
- 🔧 **[Manual de Despliegue](docs/MANUAL_DESPLIEGUE.md)** - Instalación completa (25 páginas)
- 🛠️ **[Manual de Mantenimiento](docs/MANUAL_MANTENIMIENTO.md)** - Operaciones día a día (35 páginas)
- ⚡ **[Guía Rápida](docs/GUIA_RAPIDA.md)** - Comandos esenciales

### Para Desarrolladores
- 🏗️ **[Arquitectura](docs/ARQUITECTURA.md)** - Diseño técnico completo
- 📋 **[Sistema de Usuarios y Auditoría](docs/SISTEMA_USUARIOS_AUDITORIA.md)** - Implementación técnica
- ✅ **[Integración Completada](docs/INTEGRACION_COMPLETADA.md)** - Estado del proyecto

### Índice General
- 📚 **[Índice de Documentación](docs/INDICE.md)** - Navegación por todos los documentos

---

## 🔒 Seguridad

### Implementación

- ✅ **Encriptación de contraseñas**: bcrypt con 12 rounds
- ✅ **Base de datos segura**: SQLite con protección contra SQL injection
- ✅ **Control de acceso**: Basado en roles (Usuario, Analista, Admin)
- ✅ **Auditoría completa**: Registro de todos los accesos y acciones
- ✅ **Sesiones seguras**: Gestión de sesiones con validación

### Buenas Prácticas

1. Cambiar contraseña de `admin` en primer acceso
2. Revisar logs de auditoría semanalmente
3. Configurar backups automáticos
4. Limitar acceso por IP (firewall)
5. Usar HTTPS en producción

---

## 📊 Datos

### Estadísticas

- **178,700+ registros** de matrícula (2014-2024)
- **16 regiones** de Chile
- **345 comunas** con datos detallados
- **17 especialidades** técnicas
- **Actualización**: Semanal (lunes 6:00 AM)

### Formato de Datos

- CSV para compatibilidad
- Parquet para optimización
- GeoJSON para mapas (desde [fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON))

---

## 🚀 Deployment

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

---

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=src tests/
```

---

## 📝 Changelog

### v2.0.0 (Noviembre 2025)
- ✨ **Nuevo**: Sistema de gestión de usuarios (CRUD completo)
- ✨ **Nuevo**: Sistema de auditoría de accesos y acciones
- ✨ **Nuevo**: Dashboard de auditoría con estadísticas
- ✨ **Nuevo**: Documentación completa de sostenibilidad
- 📚 Manuales para TI, usuarios y desarrolladores
- 🔒 Mejoras de seguridad (bcrypt, SQLite)

### v1.0.0 (Octubre 2025)
- 🚀 Lanzamiento inicial
- 📊 7 módulos de dashboards
- 🗺️ Mapas geográficos (regiones y comunas)
- 🔐 Autenticación básica
- 🎨 Tema claro/oscuro

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📧 Contacto

### Desarrollador
**Andrés Lazcano**  
📧 andres.lazcano@mineduc.cl  
🐙 [@andreslazcano-bit](https://github.com/andreslazcano-bit)

### Soporte Técnico
📧 ti@mineduc.cl  
📞 +56 2 XXXX XXXX  
🕒 Lunes a Viernes, 9:00 - 18:00

### Soporte Funcional
**Secretaría EMTP**  
📧 secretaria.emtp@mineduc.cl  
🕒 Lunes a Viernes, 9:00 - 17:00

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Ministerio de Educación de Chile** - Por los datos del sistema EMTP
- **[fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON)** - Por los archivos GeoJSON de Chile
- **Plotly/Dash** - Por el framework de visualización
- **Bootstrap** - Por los componentes UI

---

**Desarrollado con ❤️ para mejorar la educación técnico-profesional en Chile**

---

## 📌 Links Rápidos

- 📚 [Documentación Completa](docs/INDICE.md)
- 🐛 [Reportar un Bug](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)
- 💡 [Solicitar Feature](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues/new)
- 📖 [Wiki del Proyecto](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/wiki)

---

**Última actualización**: Noviembre 2025 | **Versión**: 2.0.0
