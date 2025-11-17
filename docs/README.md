# Documentación Técnica - Visualizador EMTP v2.0

Esta carpeta contiene la documentación técnica oficial del proyecto.

## Documentos Disponibles

### Arquitectura y Diseño

| Documento | Descripción | Tamaño |
|-----------|-------------|--------|
| `ARQUITECTURA_DETALLADA.md` | Arquitectura completa del sistema | 19 KB |
| `ARQUITECTURA_VISION_GENERAL.md` | Visión general de alto nivel | 7.5 KB |
| `DIAGRAMA_FLUJOS_ARQUITECTURA.md` | Diagramas de flujos y componentes | 17 KB |
| `Arquitectura_Vision_General.svg` | Diagrama en formato SVG (escalable) | 53 KB |
| `Arquitectura_Vision_General.png` | Diagrama en PNG estándar | 17 KB |
| `Arquitectura_Vision_General_HQ.png` | Diagrama en PNG alta calidad | 345 KB |

### Manuales para TI

| Documento | Descripción | Tamaño |
|-----------|-------------|--------|
| `MANUAL_DESPLIEGUE.md` | Instalación y configuración del sistema | 11 KB |
| `MANUAL_MANTENIMIENTO.md` | Operaciones y mantenimiento | 18 KB |
| `GUIA_SOSTENIBILIDAD.md` | Plan de sostenibilidad y transición a TI | 24 KB |

### Sistemas Implementados

| Documento | Descripción | Tamaño |
|-----------|-------------|--------|
| `SISTEMA_USUARIOS_AUDITORIA.md` | Sistema de usuarios y auditoría | 19 KB |
| `ACTUALIZACION_AUTOMATICA.md` | Actualización automática de datos | 11 KB |
| `INTEGRACION_COMPLETADA.md` | Integración de componentes v2.0 | 15 KB |

### Índice y Navegación

| Documento | Descripción | Tamaño |
|-----------|-------------|--------|
| `INDICE.md` | Índice general de documentación | 6.8 KB |
| `README.md` | Este archivo (guía de navegación) | 6.1 KB |

## Navegación por Rol

### Para Desarrolladores

1. **Primeros pasos**:
   - Lee el [`README.md` principal](../README.md) en la raíz del proyecto
   - Revisa `ARQUITECTURA_VISION_GENERAL.md` para entender el sistema

2. **Profundizar en arquitectura**:
   - `ARQUITECTURA_DETALLADA.md` - Componentes y tecnologías
   - `DIAGRAMA_FLUJOS_ARQUITECTURA.md` - Flujos de datos

3. **Implementación de nuevas funcionalidades**:
   - `SISTEMA_USUARIOS_AUDITORIA.md` - Cómo funciona auth y audit
   - `ACTUALIZACION_AUTOMATICA.md` - Sistema de actualización de datos

### Para TI / DevOps

1. **Despliegue inicial**:
   - `MANUAL_DESPLIEGUE.md` - Instalación paso a paso

2. **Operaciones**:
   - `MANUAL_MANTENIMIENTO.md` - Backups, logs, troubleshooting
   - `ACTUALIZACION_AUTOMATICA.md` - Configuración de cron jobs

### Para Gestión de Proyecto

1. **Visión general**:
   - `INTEGRACION_COMPLETADA.md` - Estado actual del proyecto
   - Diagramas PNG/SVG para presentaciones

## Estado de la Documentación

**Última actualización**: Noviembre 2025  
**Versión del proyecto**: v2.0.0  
**Total documentos**: 13 archivos (568 KB)

### Documentación Completa

- Arquitectura del sistema (3 docs + 3 diagramas)
- Manuales de despliegue y mantenimiento
- Documentación de sistemas (usuarios, auditoría, actualización)
- Índice y guías de navegación

### Características v2.0 Documentadas

- Sistema de gestión de usuarios (SQLite + bcrypt)
- Sistema de auditoría (logs JSONL)
- 3 perfiles de usuario (Usuario, Analista, Admin)
- Actualización automática de datos
- Arquitectura modular con Dash callbacks

## Uso de los Diagramas

Los diagramas de arquitectura están disponibles en 3 formatos:

1. **SVG** (`Arquitectura_Vision_General.svg`) - **Recomendado**
   - Escalable sin pérdida de calidad
   - Ideal para documentación web
   - 53 KB
## Uso de los Diagramas

1. **SVG** (`Arquitectura_Vision_General.svg`)
   - Para visualización web
   - Escalable sin pérdida de calidad

2. **PNG Estándar** (`Arquitectura_Vision_General.png`)
   - Para visualización rápida
   - 17 KB

3. **PNG Alta Calidad** (`Arquitectura_Vision_General_HQ.png`)
   - Para presentaciones profesionales
   - 345 KB, máxima calidad

## Enlaces Útiles

- **Repositorio GitHub**: [Visualizador-EMTP-Dash](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python)
- **Documentación Principal**: [README.md](../README.md)
- **Guía de Contribución**: [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Mantenedor**: Andrés Lazcano  
**Licencia**: MIT
