# PROPUESTA TÉCNICA INTEGRAL
## Sistema de Centralización y Visualización de Datos EMTP

**Secretaría Ejecutiva de Educación Media Técnico Profesional (SEEMTP)**  
**Ministerio de Educación de Chile**

---

## 📋 RESUMEN EJECUTIVO

La presente propuesta integra dos componentes esenciales para la modernización de la gestión de datos de la SEEMTP:

1. **FASE I: Centralización y Estandarización de Datos** - Infraestructura base para consolidar información dispersa en SharePoint y múltiples fuentes
2. **FASE II: Plataforma de Visualización Interactiva** - Sistema web avanzado (Python/Dash) para análisis dinámico y toma de decisiones basada en evidencia

**Beneficio Integral:** Un ecosistema completo que transforma datos dispersos y no estructurados en información accionable mediante visualizaciones interactivas, alertas automáticas y análisis multidimensional.

---

## 1. CONTEXTO Y PROBLEMÁTICA

### 1.1 Situación Actual

La SEEMTP enfrenta dos desafíos críticos e interrelacionados:

#### **Problema A: Dispersión de Datos de Gestión de Proyectos**

- **Ubicación:** SharePoint > Carpeta General SEEMTP > 07_Equipo Gestión
- **Estructura actual:**
  - `001_EMTP`
  - `002_EQUIPAMIENTO_EMTP`
  - `003_EQUIPAMIENTO_SLEP`
  - `004_APOYO_SLEP`

**Impactos identificados:**
- ❌ Planillas Excel sin estandarización entre años (mismo proyecto, campos distintos)
- ❌ Datos incompletos, duplicados e inconsistentes
- ❌ Falta de alertas sobre vencimientos de rendiciones
- ❌ Imposibilidad de consolidar reportes comparativos
- ❌ Pérdida de trazabilidad en gestión de proyectos

#### **Problema B: Información Educativa Desagregada**

Datos provenientes de múltiples fuentes públicas e internas no estandarizadas:

1. Caracterización de estudiantes y establecimientos EMTP
2. Docentes del sistema EMTP
3. Egresados/as y Titulados/as
4. Egresados/as EMTP matriculados en ESUP
5. Proyectos SEEMTP y asignación de recursos
6. Rendiciones de recursos

**Consecuencias:**
- 🚫 No existen roles claros para gestión de datos
- 🚫 Información no sistematizada dificulta análisis estratégico
- 🚫 Procesos manuales demoran toma de decisiones

### 1.2 Necesidad de una Solución Integral

Ambos problemas requieren una solución sistémica que:
- **Unifique** datos dispersos en un repositorio centralizado
- **Estandarice** formatos y procesos de carga
- **Automatice** limpieza, validación y alertas
- **Visualice** información de forma interactiva para distintos perfiles

---

## 2. OBJETIVOS

### 2.1 Objetivo General

Implementar un **sistema integral de centralización y visualización de datos** que consolide información de la SEEMTP, automatice procesos de gestión y facilite la toma de decisiones basada en evidencia mediante dashboards interactivos.

### 2.2 Objetivos Específicos

#### **FASE I: Centralización**
1. Estandarizar estructura de datos de proyectos y rendiciones en SharePoint
2. Automatizar procesos ETL (Extract, Transform, Load) para limpieza y carga
3. Implementar sistema de alertas automáticas para vencimientos
4. Integrar datos de múltiples fuentes educativas en modelo unificado

#### **FASE II: Visualización**
5. Desarrollar plataforma web interactiva con dashboards dinámicos
6. Configurar accesos y permisos por rol de usuario
7. Habilitar exportación de reportes y análisis ad-hoc
8. Capacitar equipos SEEMTP en uso del sistema

---

## 3. ALCANCE DEL PROYECTO

### 3.1 Módulos de Datos a Centralizar

| Módulo | Fuente | Tipo de Dato |
|--------|--------|--------------|
| **Matrícula EMTP** | MINEDUC, registros internos | Estudiantes, evolución anual, género, región, especialidad |
| **Titulación** | Registros internos, SIGE | Egresados, titulados, tasas por cohorte |
| **EMTP en ESUP** | SIES, cruce interno | Transición a educación superior, carreras elegidas |
| **Establecimientos** | Directorio Oficial, MINEDUC | RBD, dependencia, SLEP, especialidades impartidas |
| **Docentes** | Registros internos, CPEIP | Perfil, contrato, formación, estabilidad laboral |
| **Proyectos SEEMTP** | SharePoint (07_Equipo Gestión) | Asignación recursos, rendiciones, estado ejecución |
| **Especialidades** | Catálogo MINEDUC | Beneficiadas por proyectos, distribución territorial |

### 3.2 Funcionalidades del Sistema

#### **Centralización (Backend)**
- ✅ Repositorio único en SharePoint estructurado o BD institucional
- ✅ Procesos ETL automáticos con Python/Power Automate
- ✅ Validación de integridad y detección de duplicados
- ✅ Alertas automáticas por correo y Teams (rendiciones, vencimientos)
- ✅ Auditoría de cambios y trazabilidad completa

#### **Visualización (Frontend)**
- ✅ Dashboards interactivos con filtros dinámicos
- ✅ Análisis multidimensional (región, año, especialidad, género, dependencia)
- ✅ Gráficos comparativos y evolutivos (tendencias, benchmarking)
- ✅ Exportación a Excel/PDF de reportes personalizados
- ✅ Acceso web responsive (desktop, tablet, móvil)
- ✅ Autenticación segura con perfiles diferenciados

---

## 4. METODOLOGÍA DE IMPLEMENTACIÓN

### 4.1 Arquitectura Tecnológica Propuesta

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE FUENTES DE DATOS                     │
├─────────────────────────────────────────────────────────────────┤
│  SharePoint (Proyectos)  │  SIGE  │  SIES  │  Registros MINEDUC │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CAPA DE INTEGRACIÓN Y TRANSFORMACIÓN                │
├─────────────────────────────────────────────────────────────────┤
│  • ETL Automatizado (Python / Power Automate)                   │
│  • Limpieza y validación de datos                               │
│  • Estandarización de formatos                                  │
│  • Detección de duplicados y anomalías                          │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CAPA DE ALMACENAMIENTO CENTRAL                  │
├─────────────────────────────────────────────────────────────────┤
│  • Base de Datos Relacional (SQL Server / PostgreSQL)           │
│  • SharePoint estructurado (alternativa)                        │
│  • Modelo de datos normalizado y documentado                    │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CAPA DE LÓGICA DE NEGOCIO                      │
├─────────────────────────────────────────────────────────────────┤
│  • API REST (Python/Flask/Dash)                                 │
│  • Validaciones y reglas de negocio                             │
│  • Sistema de alertas (correo, Teams)                           │
│  • Control de acceso y auditoría                                │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 CAPA DE VISUALIZACIÓN (FRONTEND)                 │
├─────────────────────────────────────────────────────────────────┤
│  • Aplicación Web Dash/Python (Dashboard interactivo)           │
│  • Gráficos Plotly (interactividad avanzada)                    │
│  • Filtros dinámicos y exportación                              │
│  • Autenticación y perfiles de usuario                          │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Stack Tecnológico

| Componente | Tecnología Propuesta | Justificación |
|------------|---------------------|---------------|
| **Backend** | Python 3.11+ | Ecosistema robusto para análisis de datos, integración nativa con Pandas/NumPy |
| **Framework Web** | Dash 2.x (Plotly) | Especializado en visualización interactiva, menor curva de aprendizaje que Power BI para desarrollo custom |
| **Base de Datos** | SQL Server (MINEDUC) o PostgreSQL | Compatibilidad con infraestructura existente, soporte institucional |
| **ETL** | Python (Pandas, SQLAlchemy) + Power Automate | Automatización robusta, integración con SharePoint |
| **Visualización** | Plotly.js | Gráficos interactivos de alta calidad, exportables |
| **Autenticación** | JWT + bcrypt | Seguridad estándar industria, compatible con SSO MINEDUC |
| **Deployment** | Docker + Gunicorn | Portabilidad, escalabilidad, facilita deployment en servidores institucionales |
| **Monitoreo** | Loguru | Trazabilidad completa de operaciones y errores |

**Ventaja vs Power BI:** Mayor control sobre lógica de negocio, personalización ilimitada, no requiere licencias adicionales de Microsoft, código abierto y auditable.

---

## 5. FASES DE IMPLEMENTACIÓN

### **FASE I: CENTRALIZACIÓN DE DATOS** (8 semanas)

#### **Semana 1-2: Diagnóstico y Levantamiento**

**Responsable:** Equipo Políticas + Practicante

**Actividades:**
1. Inventariar bases existentes en SharePoint (carpetas 001-004)
2. Mapear fuentes de datos educativas (SIGE, SIES, registros internos)
3. Identificar variables comunes y discrepancias entre archivos
4. Detectar problemas críticos: duplicados, datos faltantes, inconsistencias
5. Priorizar años a trabajar según calidad y relevancia

**Entregables:**
- 📄 Inventario completo de fuentes de datos (Excel actualizado)
- 📄 Reporte de diagnóstico con problemas identificados
- 📄 Propuesta de priorización de años

#### **Semana 3-4: Diseño del Modelo de Datos**

**Responsable:** Equipo Políticas + Contraparte TI + Desarrollador Externo

**Actividades:**
1. Definir diccionario de datos institucional (campos obligatorios, formatos, validaciones)
2. Diseñar modelo relacional normalizado (tablas, relaciones, claves)
3. Establecer protocolos de integración con plataformas MINEDUC
4. Documentar reglas de transformación y limpieza

**Entregables:**
- 📄 Diccionario de datos institucional (versión 1.0)
- 📄 Diagrama de modelo de datos (ER)
- 📄 Protocolos de integración y actualización

#### **Semana 5-6: Desarrollo ETL y Piloto**

**Responsable:** Desarrollador Externo + Practicante

**Actividades:**
1. Desarrollar scripts Python para ETL automatizado
2. Implementar validaciones y limpieza de datos
3. Configurar conexión a SharePoint y fuentes externas
4. Ejecutar piloto con 2 años de datos (validación de calidad)
5. Documentar incidencias y ajustar procesos

**Entregables:**
- 💻 Scripts ETL en Python (código versionado en GitHub)
- 📊 Reporte de calidad de datos piloto
- 📄 Documentación técnica de procesos ETL

#### **Semana 7-8: Migración Completa y Sistema de Alertas**

**Responsable:** Desarrollador Externo + Equipo Gestión

**Actividades:**
1. Migrar todas las bases históricas al repositorio central
2. Programar alertas automáticas (correo/Teams):
   - Rendiciones próximas a vencer (7, 3, 1 día antes)
   - Rendiciones vencidas (diario)
   - Revisiones pendientes (semanal)
3. Configurar permisos y roles de acceso
4. Establecer procesos de actualización periódica

**Entregables:**
- 🗄️ Base de datos centralizada completa y funcional
- 🔔 Sistema de alertas configurado y probado
- 📄 Manual de actualización de datos

---

### **FASE II: PLATAFORMA DE VISUALIZACIÓN** (6 semanas)

#### **Semana 9-10: Desarrollo de Módulos Base**

**Responsable:** Desarrollador Externo

**Actividades:**
1. Configurar estructura de la aplicación Dash
2. Implementar autenticación y gestión de usuarios
3. Desarrollar conectores a base de datos centralizada
4. Crear componentes reutilizables (filtros, gráficos, tablas)

**Código base ya disponible:**
```python
# Estructura actual del proyecto
app_v2.py                 # Punto de entrada
src/
  callbacks/              # Lógica de interacción
    auth_callbacks.py     # Sistema de autenticación
    sidebar_callbacks.py  # Navegación y filtros
    theme_callbacks.py    # Cambio de tema
  layouts/                # Interfaces visuales
    login_layout.py       # Pantalla de login
    welcome_screen.py     # Dashboard principal
    real_data_content.py  # Visualizaciones con datos
  utils/                  # Utilidades
    auth.py               # Gestión de usuarios
    rate_limiter.py       # Control de acceso
config/
  settings.py             # Configuración central
```

**Entregables:**
- 💻 Aplicación base funcional con login
- 🔐 Sistema de autenticación implementado
- 📊 Primeros dashboards interactivos (matrícula, titulación)

#### **Semana 11-13: Desarrollo de Dashboards Completos**

**Responsable:** Desarrollador Externo

**Módulos a implementar:**

**1. Dashboard Matrícula EMTP**
- Evolución anual por región, comuna, RBD, especialidad
- Segmentación: género, ruralidad, estudiantes extranjeros
- Tasa de retención y comparativa con matrícula total
- Filtros dinámicos: año, región, especialidad, género

**2. Dashboard Egresados EMTP en ESUP**
- Tasa de transición (al año y a los 3 años)
- Áreas y carreras elegidas, tipo de institución
- Comparación por especialidad de egreso y región
- Análisis de género

**3. Dashboard Titulación EMTP**
- Número de egresados/titulados por cohorte (10 años)
- Tasa de titulación al año y a los 3 años
- Comparación por especialidad, región, género, dependencia

**4. Dashboard Establecimientos EMTP**
- Distribución territorial (región, comuna)
- Dependencia, SLEP, tipo de administración
- Especialidades impartidas por establecimiento
- Evolución de apertura/cierre de especialidades

**5. Dashboard Docentes EMTP**
- Perfil docente: edad, género, contrato, jornada
- Titulación pedagógica y formación técnica
- Estabilidad laboral (permanencia año a año)
- Distribución territorial

**6. Dashboard Proyectos SEEMTP**
- Asignación de recursos por año, tipo, región, RBD
- Comparativa anual y evolución de montos
- Nivel de ejecución financiera (ejecutado, pendiente, rendido)
- Especialidades beneficiadas
- **NUEVO:** Alertas visuales de vencimientos en dashboard

**Entregables:**
- 📊 6 módulos de visualización completos y funcionales
- 📈 Más de 30 gráficos interactivos diferentes
- 🔍 Filtros dinámicos y exportación de datos

#### **Semana 14: Validación y Pruebas**

**Responsable:** Equipo Políticas + Contraparte TI + Usuarios Piloto

**Actividades:**
1. Pruebas funcionales con datos reales
2. Validación de cálculos y métricas
3. Evaluación de experiencia de usuario
4. Pruebas de carga y rendimiento
5. Ajustes según feedback

**Entregables:**
- 📄 Reporte de pruebas y validaciones
- 💻 Sistema ajustado según feedback
- 📊 Métricas de rendimiento documentadas

---

### **FASE III: CAPACITACIÓN Y PUESTA EN MARCHA** (2 semanas)

#### **Semana 15: Capacitación**

**Responsable:** Desarrollador Externo + Coordinación SEEMTP

**Actividades:**
1. Capacitación a equipos técnicos (gestión de datos, actualización)
2. Capacitación a usuarios finales (navegación, filtros, exportación)
3. Talleres prácticos por módulo
4. Sesión de Q&A y resolución de dudas

**Entregables:**
- 📄 Manual de usuario completo (con capturas de pantalla)
- 📄 Manual técnico de administración
- 🎥 Videos tutoriales grabados
- 📊 Presentación ejecutiva del sistema

#### **Semana 16: Gobernanza y Puesta en Producción**

**Responsable:** Equipo Gestión + Coordinación

**Actividades:**
1. Definir roles y responsabilidades (carga, validación, seguimiento)
2. Establecer protocolos de actualización de datos
3. Configurar procesos de auditoría interna
4. Deployment en servidor institucional
5. Monitoreo de estabilidad y performance

**Entregables:**
- 📄 Plan de gobernanza implementado
- 📄 Protocolos de operación y mantenimiento
- 🚀 Sistema en producción y operativo
- 📊 Dashboard de monitoreo de uso

---

## 6. PERFIL DEL EQUIPO REQUERIDO

### 6.1 Desarrollador/a Externo/a (Contratación)

**Perfil técnico:**
- ✅ Experiencia demostrable en Python (Pandas, Dash, Plotly)
- ✅ Conocimiento de bases de datos relacionales (SQL Server/PostgreSQL)
- ✅ Experiencia en desarrollo de aplicaciones web interactivas
- ✅ Familiaridad con integración de datos (ETL, APIs, SharePoint)
- ✅ Capacidad de documentación técnica clara

**Deseable:**
- Experiencia en sector educativo o análisis de políticas públicas
- Conocimiento de Power BI/Tableau (para migraciones)
- Experiencia con Docker y deployment en servidores Linux

**Dedicación:** 4 meses (marzo-junio 2025)

### 6.2 Equipo Interno SEEMTP

| Rol | Responsabilidad | Dedicación |
|-----|-----------------|------------|
| **Coordinador/a del Proyecto** | Supervisión general, articulación con TI, toma de decisiones | 20% tiempo |
| **Equipo Políticas** | Validación de métricas, requerimientos funcionales, testing | 30% tiempo |
| **Equipo Gestión** | Provisión de datos, validación de proyectos, definición alertas | 20% tiempo |
| **Practicante** | Apoyo en limpieza de datos, documentación, testing | 80% tiempo |
| **Contraparte TI MINEDUC** | Accesos a BD, deployment, seguridad, integración con plataformas | Según disponibilidad |

---

## 7. CRONOGRAMA Y PRODUCTOS ESPERADOS

### 7.1 Carta Gantt

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE                     │ Mar │ Abr │ May │ Jun │               │
├─────────────────────────────────────────────────────────────────┤
│ FASE I: Centralización   │ ███ │ ███ │     │     │               │
│  - Diagnóstico           │ ██  │     │     │     │               │
│  - Modelo de Datos       │  ██ │ ██  │     │     │               │
│  - Desarrollo ETL        │     │ ███ │     │     │               │
│  - Migración Completa    │     │  ██ │ ██  │     │               │
│                          │     │     │     │     │               │
│ FASE II: Visualización   │     │  ██ │ ███ │ ██  │               │
│  - Módulos Base          │     │  ██ │     │     │               │
│  - Dashboards Completos  │     │     │ ███ │     │               │
│  - Validación            │     │     │  ██ │ ██  │               │
│                          │     │     │     │     │               │
│ FASE III: Capacitación   │     │     │     │ ███ │               │
│  - Talleres              │     │     │     │ ██  │               │
│  - Puesta en Producción  │     │     │     │  ██ │               │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Entregables por Fase

#### **FASE I - Centralización**
1. 📄 Inventario de fuentes de datos
2. 📄 Reporte de diagnóstico
3. 📄 Diccionario de datos institucional
4. 📄 Diagrama de modelo relacional
5. 💻 Scripts ETL automatizados
6. 🗄️ Base de datos centralizada operativa
7. 🔔 Sistema de alertas configurado
8. 📄 Manual de actualización de datos

#### **FASE II - Visualización**
9. 💻 Aplicación web Dash completa
10. 📊 6 módulos de dashboards interactivos
11. 🔐 Sistema de autenticación y permisos
12. 📄 Documentación técnica de arquitectura
13. 📊 Reporte de validación y pruebas

#### **FASE III - Capacitación**
14. 📄 Manual de usuario ilustrado
15. 📄 Manual técnico de administración
16. 🎥 Videos tutoriales (6 módulos)
17. 📄 Plan de gobernanza
18. 📄 Protocolos de operación
19. 🚀 Sistema en producción

---

## 8. PRESUPUESTO ESTIMADO

### 8.1 Recursos Humanos

| Concepto | Cantidad | Costo Unitario | Total |
|----------|----------|----------------|-------|
| Desarrollador/a Externo (4 meses) | 1 | $2.500.000/mes | $10.000.000 |
| Practicante (4 meses) | 1 | $500.000/mes | $2.000.000 |
| **Subtotal RRHH** | | | **$12.000.000** |

### 8.2 Infraestructura y Licencias

| Concepto | Costo Mensual | Meses | Total |
|----------|---------------|-------|-------|
| Servidor Cloud (alternativa) | $150.000 | 12 | $1.800.000 |
| Almacenamiento adicional (opcional) | $50.000 | 12 | $600.000 |
| **Subtotal Infraestructura** | | | **$2.400.000** |

### 8.3 Otros Gastos

| Concepto | Total |
|----------|-------|
| Capacitaciones presenciales | $500.000 |
| Material de difusión | $300.000 |
| Contingencia (10%) | $1.520.000 |
| **Subtotal Otros** | **$2.320.000** |

### **TOTAL PROYECTO: $16.720.000 CLP**

> **Nota:** Si se utiliza infraestructura existente de MINEDUC (servidores, BD), el costo se reduce a **$14.320.000 CLP**.

---

## 9. BENEFICIOS ESPERADOS

### 9.1 Cuantitativos

| Beneficio | Antes | Después | Mejora |
|-----------|-------|---------|--------|
| **Tiempo promedio para generar reporte** | 4-6 horas | 15 minutos | -85% |
| **Errores en datos** | ~15% registros con problemas | <2% | -87% |
| **Tiempo de respuesta a solicitudes de información** | 2-3 días | Inmediato | -95% |
| **Alertas de vencimientos detectadas** | 0% (manual) | 100% (automático) | +100% |

### 9.2 Cualitativos

✅ **Toma de decisiones basada en evidencia** - Acceso instantáneo a datos actualizados  
✅ **Transparencia y trazabilidad** - Auditoría completa de cambios y accesos  
✅ **Autonomía de equipos** - Consultas ad-hoc sin depender de TI  
✅ **Mejora en rendiciones** - Sistema de alertas reduce incumplimientos  
✅ **Estandarización institucional** - Modelo de datos replicable a otras áreas  
✅ **Capacidad de análisis avanzado** - Identificación de tendencias y brechas  

---

## 10. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Calidad de datos históricos insuficiente | Media | Alto | Priorizar años con mejor calidad, proceso iterativo de limpieza |
| Resistencia al cambio de usuarios | Media | Medio | Capacitación intensiva, involucrar usuarios desde diseño |
| Integración compleja con sistemas MINEDUC | Alta | Alto | Coordinación temprana con TI, plan B con SharePoint estructurado |
| Cambios en estructura de datos de fuentes | Media | Medio | Capa de abstracción en ETL, monitoreo de cambios, alertas |
| Sobrecarga del practicante | Baja | Medio | Supervisión constante, distribución de tareas, apoyo del equipo |
| Delays en accesos a BD institucionales | Alta | Alto | Iniciar trámites en paralelo, usar datos simulados para desarrollo |

---

## 11. SOSTENIBILIDAD DEL SISTEMA

### 11.1 Gobernanza Post-Implementación

**Roles definidos:**

| Rol | Responsabilidad | Frecuencia |
|-----|-----------------|------------|
| **Administrador de Datos** | Validar carga de datos nuevos, resolver inconsistencias | Semanal |
| **Administrador del Sistema** | Mantenimiento técnico, actualización de software | Mensual |
| **Gestor de Usuarios** | Gestión de accesos, permisos, capacitación nuevos usuarios | Según demanda |
| **Revisor de Alertas** | Seguimiento de alertas de vencimientos, escalamiento | Diario |

### 11.2 Actualización de Datos

**Flujo automatizado:**

1. **Fuentes externas (SIGE, SIES):** ETL automático semanal
2. **SharePoint (proyectos):** ETL automático diario (detecta nuevos archivos)
3. **Datos manuales:** Formulario web de carga validada

**Monitoreo:**
- Dashboard de salud del sistema (última actualización, errores, registros procesados)
- Alertas automáticas si falla proceso ETL

### 11.3 Evolución del Sistema

**Roadmap futuro (post-implementación):**

- **Corto plazo (6 meses):** Incorporar nuevos módulos (especialidades emergentes, proyección de demanda)
- **Mediano plazo (1 año):** Integración con otros sistemas MINEDUC (asistencia, resultados SIMCE)
- **Largo plazo (2 años):** Módulo de Machine Learning para predicciones (deserción, demanda laboral)

---

## 12. ANEXOS

### ANEXO A: Diccionario de Datos (Extracto)

| Tabla | Campo | Tipo | Obligatorio | Descripción |
|-------|-------|------|-------------|-------------|
| `proyectos` | `id_proyecto` | INT | Sí | Identificador único del proyecto |
| `proyectos` | `rbd` | VARCHAR(10) | Sí | Código RBD del establecimiento beneficiario |
| `proyectos` | `tipo_proyecto` | VARCHAR(50) | Sí | 001_EMTP, 002_EQUIPAMIENTO_EMTP, 003_EQUIPAMIENTO_SLEP, 004_APOYO_SLEP |
| `proyectos` | `año` | INT | Sí | Año de ejecución del proyecto |
| `proyectos` | `monto_asignado` | DECIMAL(15,2) | Sí | Monto en pesos chilenos |
| `proyectos` | `fecha_inicio` | DATE | Sí | Fecha de inicio del proyecto |
| `proyectos` | `fecha_rendicion` | DATE | Sí | Fecha límite de rendición |
| `proyectos` | `estado_rendicion` | VARCHAR(20) | Sí | PENDIENTE, RENDIDO, VENCIDO, EN_REVISION |
| `proyectos` | `responsable` | VARCHAR(100) | Sí | Nombre del responsable del proyecto |

*Documento completo disponible post-contratación*

### ANEXO B: Arquitectura Técnica Detallada

```python
# Ejemplo de código ETL (extracto)

from src.utils.data_connector import DataConnector
import pandas as pd
from loguru import logger

def extract_proyectos_sharepoint():
    """Extrae datos de proyectos desde SharePoint"""
    # Conexión a SharePoint Office365
    from shareplum import Site, Office365
    
    site = Office365(settings.SHAREPOINT_URL, 
                      username=settings.SHAREPOINT_USER,
                      password=settings.SHAREPOINT_PASS).GetSite(settings.SHAREPOINT_SITE)
    
    folder = site.Folder('07_Equipo Gestión/001_EMTP')
    files = folder.files
    
    dataframes = []
    for file in files:
        if file.endswith('.xlsx'):
            df = pd.read_excel(file)
            df = transform_proyectos(df)  # Limpieza
            dataframes.append(df)
    
    return pd.concat(dataframes, ignore_index=True)

def transform_proyectos(df):
    """Limpia y estandariza datos de proyectos"""
    # Estandarizar nombres de columnas
    df.columns = df.columns.str.lower().str.strip()
    
    # Validar RBD (formato correcto)
    df['rbd'] = df['rbd'].astype(str).str.zfill(10)
    
    # Convertir fechas
    df['fecha_rendicion'] = pd.to_datetime(df['fecha_rendicion'], errors='coerce')
    
    # Detectar duplicados
    duplicados = df.duplicated(subset=['rbd', 'tipo_proyecto', 'año'])
    if duplicados.any():
        logger.warning(f"Detectados {duplicados.sum()} registros duplicados")
    
    return df

def load_to_database(df):
    """Carga datos limpios a base de datos"""
    engine = DataConnector.get_connection()
    df.to_sql('proyectos', engine, if_exists='append', index=False)
    logger.info(f"Cargados {len(df)} registros a BD")
```

### ANEXO C: Mockups de Dashboards

*(Disponibles en repositorio GitHub del proyecto)*

**Capturas actuales de prototipo funcional:**
- Login y autenticación
- Dashboard de bienvenida
- Visualización de matrícula con filtros
- Gráficos interactivos de tendencias

---

## 13. PRÓXIMOS PASOS

### Para SEEMTP

1. **Semana 1:** Revisión y aprobación de propuesta por Coordinación y Dirección
2. **Semana 2:** Gestión de presupuesto y aprobación financiera
3. **Semana 3:** Coordinación con TI MINEDUC para accesos y recursos
4. **Semana 4:** Llamado a contratación de desarrollador/a externo/a
5. **Semana 5:** Inicio Fase I del proyecto

### Para el Desarrollador Externo (una vez contratado)

1. **Día 1-3:** Reunión de kick-off, revisión de documentación, accesos
2. **Día 4-10:** Diagnóstico y levantamiento (junto a equipo)
3. **Día 11-15:** Diseño del modelo de datos
4. **Semana 3+:** Desarrollo según cronograma de fases

---

## 14. CONTACTO Y CONSULTAS

**Coordinador del Proyecto:**  
[Nombre y cargo]  
Email: [email]  
Teléfono: [teléfono]

**Desarrollador del Prototipo Actual:**  
Andrés Lazcano  
GitHub: [@andreslazcano-bit](https://github.com/andreslazcano-bit)  
Repositorio: [Visualizador-EMTP-Dash](https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python)

---

**Documento preparado:** Octubre 2025  
**Versión:** 1.0  
**Estado:** Propuesta para revisión interna
