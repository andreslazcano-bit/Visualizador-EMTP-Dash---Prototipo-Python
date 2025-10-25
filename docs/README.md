# 📚 Documentación del Visualizador EMTP (Python/Dash)

Esta carpeta contiene documentos técnicos y funcionales del proyecto.

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
