# 📚 Documentación Técnica - Visualizador EMTP

Esta carpeta contiene la documentación técnica oficial del proyecto.

---

## 📄 Documentos Disponibles

### Documentación Técnica (en GitHub)

| Documento | Propósito | Última Actualización |
|-----------|-----------|---------------------|
| `PROPUESTA_TECNICA_INTEGRAL.md` | Propuesta técnica original (Fase I + II) | Oct 2025 |
| `RESUMEN_EJECUTIVO.md` | Resumen ejecutivo técnico | Oct 2025 |
| `README.md` | Este archivo (guía de navegación) | Nov 2025 |

---

## 📁 Documentos de Planificación (NO en GitHub)

Los documentos de planificación estratégica y toma de decisiones se encuentran en:
```
/Users/andreslazcano/ProyectosShiny/VisualizadorEMTP-Dash/_docs-planificacion/
```

Estos incluyen:
- Documentos para presentación a jefatura
- Memorándum para coordinación con TI
- Análisis de decisiones estratégicas
- Presentaciones y checklists

**Estos archivos NO se suben a GitHub** ya que son de uso interno y planificación personal.

---

## 🗄️ Archivo de Referencia (NO en GitHub)

Documentos obsoletos y de referencia histórica en:
```
/Users/andreslazcano/ProyectosShiny/VisualizadorEMTP-Dash/_archive/
```

Incluye:
- `/shiny-obsoleto/`: Archivos de la versión Shiny/R anterior
- `/docs-referencia/`: Documentos Word de referencia y propuestas antiguas

---

## 🔍 Navegación Rápida

### Para desarrolladores:
- **Arquitectura del sistema**: Ver código fuente en `/src`
- **Instalación y setup**: Ver `README.md` en raíz del proyecto
- **Propuesta técnica completa**: `PROPUESTA_TECNICA_INTEGRAL.md`

### Para gestión de proyecto:
- **Documentos de planificación**: `/_docs-planificacion/` (local)
- **Archivo de referencia**: `/_archive/` (local)

---

## 📋 Estado de la Documentación

**Última actualización**: Noviembre 2025  
**Versión del proyecto**: 2.0 (Python/Dash)

### Documentos activos (en GitHub):
✅ Propuesta técnica integral  
✅ Resumen ejecutivo  
✅ Documentación en código fuente  

### Documentos de planificación (locales):
📁 7 documentos estratégicos para toma de decisiones  
📁 No se incluyen en el repositorio público  

### Archivos obsoletos (archivados):
🗄️ Versión Shiny/R anterior  
🗄️ Documentos Word de referencia  
🗄️ Propuestas antiguas  

---

**Organización del proyecto**: Noviembre 2025  
**Responsable**: Andrés Lazcano

---

## 🎯 Documentos Principales para Presentación Institucional

### 📄 [PROPUESTA_TECNICA_INTEGRAL.md](PROPUESTA_TECNICA_INTEGRAL.md) ⭐ NUEVO
**Documento completo para presentación institucional** (20+ páginas)

Integra las propuestas de **centralización de datos** (Fase I) y **visualización interactiva** (Fase II) en un solo documento estructurado.

**Incluye:**
- Contexto y problemática actual (SharePoint desorganizado + datos fragmentados)
- Fase I: Centralización de datos (8 semanas, ETL automático, alertas)
- Fase II: Plataforma de visualización (6 semanas, 6 dashboards interactivos)
- Arquitectura técnica detallada (Python/Dash, diagramas, código ejemplo)
- Cronograma y Carta Gantt
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
