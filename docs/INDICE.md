# 📚 Índice de Documentación - Visualizador EMTP v2.0

**Versión:** 2.0.0  
**Última Actualización:** 17 de Noviembre 2025

Este documento sirve como índice central para toda la documentación técnica del proyecto.

---

## 📋 Índice General

### 🏗️ Arquitectura y Diseño

| Documento | Descripción | Páginas |
|-----------|-------------|---------|
| [**Arquitectura Detallada**](ARQUITECTURA_DETALLADA.md) | Diseño completo del sistema, componentes y tecnologías | ~30 |
| [**Arquitectura - Visión General**](ARQUITECTURA_VISION_GENERAL.md) | Vista de alto nivel del sistema | ~12 |
| [**Diagramas de Flujos**](DIAGRAMA_FLUJOS_ARQUITECTURA.md) | Flujos de datos y componentes | ~25 |
| Diagramas Visuales | `*.svg`, `*.png`, `*_HQ.png` | Visual |

### 🔧 Manuales para TI

| Documento | Descripción | Páginas |
|-----------|-------------|---------|
| [**Manual de Despliegue**](MANUAL_DESPLIEGUE.md) ⭐ | Instalación y configuración paso a paso | ~25 |
| [**Manual de Mantenimiento**](MANUAL_MANTENIMIENTO.md) ⭐ | Operaciones, backups, troubleshooting | ~35 |

### 📊 Sistemas Implementados

| Documento | Descripción | Páginas |
|-----------|-------------|---------|
| [**Sistema de Usuarios y Auditoría**](SISTEMA_USUARIOS_AUDITORIA.md) | Gestión de usuarios + logs de auditoría | ~30 |
| [**Actualización Automática**](ACTUALIZACION_AUTOMATICA.md) | Sistema de actualización semanal de datos | ~18 |
| [**Integración Completada**](INTEGRACION_COMPLETADA.md) | Estado del proyecto v2.0 | ~22 |

### 📖 Navegación

| Documento | Descripción |
|-----------|-------------|
| [**README.md**](README.md) | Guía de navegación de la documentación |
| [**INDICE.md**](INDICE.md) | Este archivo - índice general |

---

## 📁 Estructura de Documentación

```
docs/
├── 📐 ARQUITECTURA (3 docs + 3 diagramas)
│   ├── ARQUITECTURA_DETALLADA.md
│   ├── ARQUITECTURA_VISION_GENERAL.md
│   ├── DIAGRAMA_FLUJOS_ARQUITECTURA.md
│   ├── Arquitectura_Vision_General.svg        (recomendado)
│   ├── Arquitectura_Vision_General.png
│   └── Arquitectura_Vision_General_HQ.png
│
├── � MANUALES TI (2 docs)
│   ├── MANUAL_DESPLIEGUE.md                   ⭐ Instalación
│   └── MANUAL_MANTENIMIENTO.md                ⭐ Operaciones
│
├── 📊 SISTEMAS (3 docs)
│   ├── SISTEMA_USUARIOS_AUDITORIA.md
│   ├── ACTUALIZACION_AUTOMATICA.md
│   └── INTEGRACION_COMPLETADA.md
│
└── 📖 NAVEGACIÓN (2 docs)
    ├── README.md
    └── INDICE.md                              ← Este archivo
```

---

## 🎯 Guía de Lectura por Rol

### 👨‍💻 Si eres **Desarrollador**:

**Orden de lectura recomendado:**

1. **Primero**: [README.md](../README.md) (raíz del proyecto)
2. **Luego**: [ARQUITECTURA_VISION_GENERAL.md](ARQUITECTURA_VISION_GENERAL.md)
3. **Profundizar**: [ARQUITECTURA_DETALLADA.md](ARQUITECTURA_DETALLADA.md)
4. **Entender flujos**: [DIAGRAMA_FLUJOS_ARQUITECTURA.md](DIAGRAMA_FLUJOS_ARQUITECTURA.md)
5. **Sistemas específicos**:
   - [SISTEMA_USUARIOS_AUDITORIA.md](SISTEMA_USUARIOS_AUDITORIA.md)
   - [ACTUALIZACION_AUTOMATICA.md](ACTUALIZACION_AUTOMATICA.md)
6. **Estado actual**: [INTEGRACION_COMPLETADA.md](INTEGRACION_COMPLETADA.md)

**Tiempo estimado**: 3-4 horas para leer toda la documentación

---

### 🔧 Si eres **Administrador de TI** (Despliegue):

**Para instalar el sistema:**

1. ⭐ **LEER PRIMERO**: [MANUAL_DESPLIEGUE.md](MANUAL_DESPLIEGUE.md)
2. Seguir los pasos de instalación
3. Configurar como servicio (Linux/Windows)
4. **Luego leer**: [MANUAL_MANTENIMIENTO.md](MANUAL_MANTENIMIENTO.md)
5. Configurar backups automáticos
6. Configurar actualización semanal ([ACTUALIZACION_AUTOMATICA.md](ACTUALIZACION_AUTOMATICA.md))

**Tiempo estimado**: 2 horas (lectura + instalación)

---

### 🛠️ Si eres **Administrador de TI** (Mantenimiento):

**Para mantener el sistema funcionando:**

1. ⭐ **LEER PRIMERO**: [MANUAL_MANTENIMIENTO.md](MANUAL_MANTENIMIENTO.md)
2. Configurar checklists de verificación (diaria/semanal/mensual)
3. Revisar sección de troubleshooting
4. Tener a mano procedimientos de backup y restauración

**Tareas semanales**:
- Verificar logs de auditoría
- Revisar espacio en disco
- Verificar actualización automática de datos

**Tiempo estimado**: 30 minutos/semana

---

### 📊 Si trabajas en **Gestión de Proyecto**:

**Para entender el proyecto:**

1. [README.md](../README.md) - Vista general
2. [INTEGRACION_COMPLETADA.md](INTEGRACION_COMPLETADA.md) - Estado actual
3. Diagramas visuales (SVG/PNG) para presentaciones

**Para presentaciones**:
- Usar `Arquitectura_Vision_General_HQ.png` (alta calidad, 345 KB)
- Ver [ARQUITECTURA_VISION_GENERAL.md](ARQUITECTURA_VISION_GENERAL.md) para explicaciones

---

## 📏 Estadísticas de Documentación

| Categoría | Documentos | Tamaño Total | Páginas Aprox. |
|-----------|------------|--------------|----------------|
| **Arquitectura** | 6 (3 MD + 3 imágenes) | ~500 KB | ~70 páginas |
| **Manuales TI** | 2 | ~29 KB | ~60 páginas |
| **Sistemas** | 3 | ~45 KB | ~70 páginas |
| **Navegación** | 2 | ~14 KB | ~10 páginas |
| **TOTAL** | **13 archivos** | **~588 KB** | **~210 páginas** |

---

## 🔄 Historial de Versiones

### v2.0.0 (Noviembre 2025) - Release Actual ✅
- ✅ Sistema de gestión de usuarios (SQLite + bcrypt)
- ✅ Sistema de auditoría (logs JSONL)
- ✅ 3 perfiles de usuario (Usuario, Analista, Admin)
- ✅ Actualización automática de datos
- ✅ Documentación técnica completa (13 docs)
- ✅ Manuales de despliegue y mantenimiento
- ✅ Arquitectura modular con Dash callbacks
- ✅ Dockerización (Dockerfile + docker-compose.yml)

### v1.0.0 (Octubre 2025)
- ✅ Dashboard interactivo con Dash/Plotly
- ✅ 6 módulos principales (Matrícula, Egresados, etc.)
- ✅ Mapas geográficos interactivos
- ✅ Sistema de filtros avanzados
- ✅ Tema claro/oscuro

---

## � Enlaces Útiles

### Repositorio y Código
- **GitHub**: [Visualizador-EMTP-Dash](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python)
- **README Principal**: [README.md](../README.md)
- **Guía de Contribución**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Licencia**: [LICENSE](../LICENSE) (MIT)

### Archivos de Configuración
- **Docker**: [Dockerfile](../Dockerfile), [docker-compose.yml](../docker-compose.yml)
- **Dependencias**: [requirements.txt](../requirements.txt)
- **Configuración**: [.env.example](../.env.example)

---

## 📞 Soporte y Contacto

### Consultas Técnicas
**Desarrollador Principal**  
📧 andres.lazcano@mineduc.cl

### Reportar Issues
**GitHub Issues**: [Crear nuevo issue](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python/issues)

---

**Mantenedor**: Andrés Lazcano  
**Licencia**: MIT  
**Última Revisión**: 17 de Noviembre 2025  
📞 +56 9 XXXX XXXX

---

## 📝 Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | Nov 2025 | Agregados manuales de sostenibilidad, gestión usuarios, auditoría |
| 1.0 | Oct 2025 | Documentación técnica inicial |

---

**Última actualización:** 17 de Noviembre 2025  
**Mantenedor:** Andrés Lazcano

---

💡 **Tip:** Marcar este documento como favorito para acceso rápido a toda la documentación.
