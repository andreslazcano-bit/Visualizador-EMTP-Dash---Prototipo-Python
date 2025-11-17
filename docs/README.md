# 📚 Documentación Técnica - Visualizador EMTP v2.0

Esta carpeta contiene la documentación técnica oficial del proyecto.

---

## 📄 Documentos Disponibles

### Arquitectura y Diseño

| Documento | Descripción | Tamaño |
|-----------|-------------|--------|
| `ARQUITECTURA_DETALLADA.md` | Arquitectura completa del sistema | 19 KB |
| `ARQUITECTURA_VISION_GENERAL.md` | Visión general de alto nivel | 7.5 KB |
| `DIAGRAMA_FLUJOS_ARQUITECTURA.md` | Diagramas de flujos y componentes | 17 KB |
| `Arquitectura_Vision_General.svg` | Diagrama en formato SVG (escalable) | 53 KB |
| `Arquitectura_Vision_General.png` | Diagrama en PNG estándar | 17 KB |
| `Arquitectura_Vision_General_HQ.png` | Diagrama en PNG alta calidad | 345 KB |

### Manuales Técnicos

| Documento | Descripción | Tamaño |
|-----------|-------------|--------|
| `MANUAL_DESPLIEGUE.md` | Instalación y configuración del sistema | 11 KB |
| `MANUAL_MANTENIMIENTO.md` | Operaciones y mantenimiento | 18 KB |

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

---

## 🔍 Navegación por Rol

### 👨‍💻 Para Desarrolladores

1. **Primeros pasos**:
   - Lee el [`README.md` principal](../README.md) en la raíz del proyecto
   - Revisa `ARQUITECTURA_VISION_GENERAL.md` para entender el sistema

2. **Profundizar en arquitectura**:
   - `ARQUITECTURA_DETALLADA.md` - Componentes y tecnologías
   - `DIAGRAMA_FLUJOS_ARQUITECTURA.md` - Flujos de datos

3. **Implementación de nuevas funcionalidades**:
   - `SISTEMA_USUARIOS_AUDITORIA.md` - Cómo funciona auth y audit
   - `ACTUALIZACION_AUTOMATICA.md` - Sistema de actualización de datos

### 🛠️ Para TI / DevOps

1. **Despliegue inicial**:
   - `MANUAL_DESPLIEGUE.md` - Instalación paso a paso

2. **Operaciones**:
   - `MANUAL_MANTENIMIENTO.md` - Backups, logs, troubleshooting
   - `ACTUALIZACION_AUTOMATICA.md` - Configuración de cron jobs

### 📊 Para Gestión de Proyecto

1. **Visión general**:
   - `INTEGRACION_COMPLETADA.md` - Estado actual del proyecto
   - Diagramas PNG/SVG para presentaciones

---

## 📋 Estado de la Documentación

**Última actualización**: Noviembre 2025  
**Versión del proyecto**: v2.0.0  
**Total documentos**: 13 archivos (568 KB)

### ✅ Documentación Completa

- ✅ Arquitectura del sistema (3 docs + 3 diagramas)
- ✅ Manuales de despliegue y mantenimiento
- ✅ Documentación de sistemas (usuarios, auditoría, actualización)
- ✅ Índice y guías de navegación

### 🚀 Características v2.0 Documentadas

- Sistema de gestión de usuarios (SQLite + bcrypt)
- Sistema de auditoría (logs JSONL)
- 3 perfiles de usuario (Usuario, Analista, Admin)
- Actualización automática de datos
- Arquitectura modular con Dash callbacks

---

## 📖 Uso de los Diagramas

Los diagramas de arquitectura están disponibles en 3 formatos:

1. **SVG** (`Arquitectura_Vision_General.svg`) - **Recomendado**
   - Escalable sin pérdida de calidad
   - Ideal para documentación web
   - 53 KB

2. **PNG Estándar** (`Arquitectura_Vision_General.png`)
   - Para visualización rápida
   - 17 KB

3. **PNG Alta Calidad** (`Arquitectura_Vision_General_HQ.png`)
   - Para presentaciones profesionales
   - 345 KB, máxima calidad

---

## 🔗 Enlaces Útiles

- **Repositorio GitHub**: [Visualizador-EMTP-Dash](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python)
- **Documentación Principal**: [README.md](../README.md)
- **Guía de Contribución**: [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Mantenedor**: Andrés Lazcano  
**Licencia**: MIT
- Presupuesto detallado ($16.7M CLP)
- Equipo requerido y perfiles
- Beneficios cuantitativos y cualitativos
- Anexos técnicos (diccionario de datos, ETL, mockups)

**Audiencia:** Dirección SEEMTP, Coordinación, TI MINEDUC

---

### 📄 [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) ⭐ NUEVO
**Versión resumida para reuniones rápidas** (4 páginas)

Perfecto para presentaciones ejecutivas de 15-20 minutos.

**Incluye:**
- Resumen del problema (Antes vs Después)
- Solución en 2 fases con cronograma visual
- Comparativa de impacto (-85% tiempo reportes, -87% errores)
- Presupuesto resumido
- Próximos pasos claros
- FAQs anticipadas

**Audiencia:** Reuniones ejecutivas, aprobaciones rápidas

---

## 📋 Documentos de Origen (Referencia)

### 📄 Centralizacion Proyectos Gestión - Propuesta.docx
Propuesta original de centralización de datos de proyectos en SharePoint.

**Contenido clave:**
- Situación actual de datos en carpeta 07_Equipo Gestión
- Problemas identificados (dispersión, campos inconsistentes)
- Fases propuestas: diagnóstico, estandarización, piloto, automatización
- Roles y responsabilidades (practicante, equipo gestión)

### 📄 20250922_Minuta Propuesta de Proyecto Power BI_V3_CON_BRECHAS.docx
Propuesta original de sistema de visualización (Power BI).

**Contenido clave:**
- Antecedentes: datos EMTP dispersos
- Objetivos: centralización y dashboards
- Alcance: 7 módulos de datos (matrícula, titulación, docentes, proyectos, etc.)
- Metodología: 5 fases de implementación
- Perfil profesional externo requerido
- Visualizaciones esperadas detalladas

> **Nota:** Estos documentos fueron la base para crear **PROPUESTA_TECNICA_INTEGRAL.md**, que los integra y actualiza con la solución técnica actual (Python/Dash en lugar de Power BI).

---

## 🛠️ Índice de Documentos Técnicos del Proyecto



- ARQUITECTURA.md – Arquitectura general de la aplicación
- INDICE.md – Índice de documentación y convenciones
- MIGRACION_DATOS.md – Guía para migración y preparación de datos
- ROADMAP.md – Plan de trabajo y fases
- SISTEMA_ALERTAS_PROYECTOS.md – Diseño del sistema de alertas (Proyectos)
- ANALISIS_SEGURIDAD_AUTH.md – Análisis de autenticación y seguridad
- INDICE_SEGURIDAD.md – Índice de seguridad
- RESUMEN_SEGURIDAD.md – Resumen técnico de seguridad
- CAMBIOS_VISUALES_INSTITUCIONALES.md – Ajustes visuales y lineamientos
- CONECTIVIDAD_INSTITUCIONAL.md – Consideraciones de red / conectividad
- CORRECCION_COLORES_ICONOS.md – Cambios de estilo y colores
- CORRECCION_ICONOS_PROYECTOS.md – Ajustes en iconografía de Proyectos
- SESION_20OCT2025.md – Bitácora y acuerdos de la sesión

## Lecturas recomendadas

1. ARQUITECTURA.md → visión general
2. INICIO_RAPIDO.md (en la raíz) → ejecutar el proyecto rápido
3. MIGRACION_DATOS.md → preparar datos locales/simulados
4. ROADMAP.md → siguientes pasos del proyecto

## Cómo contribuir

- Sigue las convenciones descritas en INDICE.md
- Usa ramas por feature (feature/<nombre-corto>)
- Crea PRs con descripción clara y captura de pantallas cuando aplique
