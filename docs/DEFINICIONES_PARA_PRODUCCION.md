# VISUALIZADOR EMTP - DEFINICIONES PARA PUESTA EN PRODUCCIÓN

**Fecha**: Noviembre 2025  
**Área**: Coordinación Nacional EMTP  
**Documento**: Definiciones estratégicas para implementación  
**Versión**: 1.0

---

## RESUMEN EJECUTIVO

El **Visualizador EMTP** es una plataforma web interactiva desarrollada para centralizar, analizar y visualizar datos del Sistema de Educación Media Técnico-Profesional. Actualmente se encuentra en estado de **prototipo funcional avanzado** con datos simulados.

Para avanzar a **producción** y ponerlo a disposición de usuarios finales, se requieren **definiciones estratégicas** en tres áreas clave:

1. **Modelo de Acceso y Usuarios** (¿Quiénes podrán usar el sistema?)
2. **Tipo de Plataforma** (¿Visualización, reportería, o ambas?)
3. **Fuentes de Datos** (¿De dónde se alimentará la información?)

Este documento presenta **opciones concretas** para cada área, sus implicancias y una propuesta de ruta de implementación.

---

## 📋 ÍNDICE

1. [Definición 1: Modelo de Acceso y Usuarios](#definición-1-modelo-de-acceso-y-usuarios)
2. [Definición 2: Tipo de Plataforma](#definición-2-tipo-de-plataforma)
3. [Definición 3: Fuentes y Conexión de Datos](#definición-3-fuentes-y-conexión-de-datos)
4. [Resumen de Decisiones Requeridas](#resumen-de-decisiones-requeridas)
5. [Próximos Pasos](#próximos-pasos)
6. [Anexos](#anexos)

---

## DEFINICIÓN 1: MODELO DE ACCESO Y USUARIOS

### ¿Quiénes podrán acceder al Visualizador EMTP?

El sistema actualmente tiene **capacidad técnica** para implementar múltiples modelos de acceso. Se requiere definir **quién** y **cómo** podrá utilizar la plataforma.

---

### OPCIONES DISPONIBLES

#### **Opción A: Acceso Público (Sin autenticación)**

**Descripción**: Cualquier persona con el enlace puede acceder a todas las visualizaciones.

**✅ Ventajas:**
- Máxima transparencia de datos EMTP
- Sin barreras de entrada
- No requiere gestión de usuarios
- Acceso inmediato para investigadores, prensa, académicos

**❌ Desventajas:**
- No hay control sobre quién accede
- No hay auditoría de uso
- No se puede restringir información sensible
- Riesgo de mal uso de datos

**📊 Casos de uso:**
- Datos generales de matrícula por región
- Estadísticas públicas de titulación
- Mapas de distribución territorial

**⚠️ Consideraciones:**
- Requiere cuidado con datos personalizados
- No permite secciones administrativas

---

#### **Opción B: Acceso con Perfiles (Recomendado)**

**Descripción**: Sistema de login con usuarios diferenciados según rol institucional.

**Perfiles propuestos:**

| Perfil | Acceso | Usuarios típicos | Funcionalidades |
|--------|--------|------------------|-----------------|
| **👤 Usuario Básico** | Solo visualización de datos públicos | Directores de establecimientos, Docentes EMTP | • Ver matrícula<br>• Ver titulación<br>• Ver mapas<br>❌ Sin acceso a proyectos |
| **👔 Analista SEEMTP** | Visualización + Reportería | Coordinadores regionales, Analistas de datos | • Todo lo anterior<br>• Ver proyectos y convenios<br>• Exportar reportes Excel/PDF<br>• Comparar períodos |
| **⚙️ Administrador** | Acceso total + Configuración | Jefatura SEEMTP, TI | • Todo lo anterior<br>• Gestionar usuarios<br>• Configurar parámetros<br>• Auditoría completa |

**✅ Ventajas:**
- Control granular de acceso
- Auditoría completa (quién vio qué, cuándo)
- Protección de información sensible
- Diferentes vistas según necesidad
- Cumplimiento normativo (Ley de Transparencia)

**❌ Desventajas:**
- Requiere proceso de registro de usuarios
- Gestión administrativa de credenciales
- Mayor complejidad técnica inicial

**📊 Casos de uso:**
- Información de convenios activos (solo SEEMTP)
- Rendiciones financieras (solo analistas)
- Datos sensibles por establecimiento

---

#### **Opción C: Modelo Híbrido (Público + Privado)**

**Descripción**: Sección pública para datos generales + Sección privada con login para datos sensibles.

**Estructura:**

```
┌─────────────────────────────────────┐
│     VISUALIZADOR EMTP (Público)     │
│  • Matrícula regional               │
│  • Mapas generales                  │
│  • Estadísticas agregadas           │
└─────────────────────────────────────┘
              ↓ Login
┌─────────────────────────────────────┐
│   VISUALIZADOR EMTP (Autenticado)   │
│  • Datos por establecimiento        │
│  • Proyectos y convenios            │
│  • Exportación de reportes          │
│  • Indicadores de gestión           │
└─────────────────────────────────────┘
```

**✅ Ventajas:**
- Balance entre transparencia y control
- Fomenta uso público de datos abiertos
- Protege información sensible
- Flexibilidad para evolucionar

**❌ Desventajas:**
- Requiere mantener dos tipos de contenido
- Mayor complejidad de desarrollo
- Riesgo de confusión sobre qué es público/privado

---

### 🎯 DEFINICIÓN REQUERIDA #1

**Pregunta clave**: ¿Qué modelo de acceso se implementará?

- [ ] **Opción A**: Acceso público sin autenticación
- [ ] **Opción B**: Acceso con perfiles diferenciados (Recomendado)
- [ ] **Opción C**: Modelo híbrido (público + privado)
- [ ] **Otra opción**: _________________________

**Complementarias:**

Si se elige Opción B o C:

1. **¿Quiénes crearán las cuentas de usuario?**
   - [ ] Área SEEMTP
   - [ ] Área TI MINEDUC
   - [ ] Autoregistro con aprobación

2. **¿Cómo se autenticarán los usuarios?**
   - [ ] Credenciales propias del sistema
   - [ ] Integración con Active Directory MINEDUC
   - [ ] Cuenta Microsoft institucional (Office 365)

3. **¿Se requiere auditoría de accesos?**
   - [ ] Sí, registro completo (quién, cuándo, qué consultó)
   - [ ] Solo registro de login/logout
   - [ ] No se requiere auditoría

---

## DEFINICIÓN 2: TIPO DE PLATAFORMA

### ¿Qué funcionalidades debe ofrecer el sistema?

El Visualizador actual es una **plataforma de análisis interactivo**. Se requiere definir si evolucionará hacia capacidades de **reportería programada**.

---

### OPCIONES DISPONIBLES

#### **Opción A: Solo Visualización Interactiva**

**Descripción**: Dashboard web donde los usuarios exploran datos en tiempo real con filtros dinámicos.

**Características:**
- ✅ Gráficos interactivos (clic para filtrar, zoom, hover para detalles)
- ✅ Mapas geográficos (choropleth regional y comunal)
- ✅ Filtros dinámicos (región, comuna, especialidad, año, etc.)
- ✅ Tablas resumen actualizables
- ✅ Comparación visual entre dimensiones

**📊 Ejemplo de uso:**
*"El coordinador regional de Valparaíso entra al sistema, filtra por su región, selecciona especialidad 'Gastronomía' y año '2024', y ve en tiempo real la evolución de matrícula en un gráfico de líneas."*

**✅ Ventajas:**
- Flexibilidad total para explorar datos
- Actualización instantánea al cambiar filtros
- No genera archivos estáticos obsoletos
- Menor carga de desarrollo inicial

**❌ Limitaciones:**
- No genera documentos para compartir fuera del sistema
- No permite reportes formales para autoridades
- Usuario debe estar conectado para ver datos

---

#### **Opción B: Visualización + Reportería Básica**

**Descripción**: Todo lo anterior + capacidad de exportar datos y gráficos a formatos estándar.

**Características adicionales:**
- ✅ Exportación Excel (.xlsx) con datos filtrados
- ✅ Exportación CSV para análisis externos
- ✅ Descarga de gráficos como imágenes (PNG/SVG)
- ✅ Generación de PDF con visualizaciones
- ✅ Reportes bajo demanda (usuario solicita, sistema genera)

**📊 Ejemplo de uso:**
*"La jefatura SEEMTP necesita presentar datos de matrícula 2024 en un informe ministerial. Filtra los datos necesarios en el visualizador y descarga un reporte PDF con gráficos y tablas formateadas."*

**✅ Ventajas:**
- Permite uso offline de datos
- Facilita presentaciones y documentos formales
- Archivos compartibles vía email
- Cumplimiento de solicitudes de información

**❌ Limitaciones:**
- Reportes generados manualmente (usuario debe solicitarlos)
- No hay envío automático

**📦 Esfuerzo de implementación**: 2-3 semanas

---

#### **Opción C: Plataforma Completa (Visualización + Reportería Programada)** ⭐

**Descripción**: Sistema integral con análisis interactivo + generación automática de reportes periódicos.

**Características adicionales a Opción B:**
- ✅ Reportes programados (diarios, semanales, mensuales)
- ✅ Envío automático vía email a destinatarios configurados
- ✅ Plantillas de reportes estandarizadas por tipo
- ✅ Alertas automáticas (ej: "Matrícula bajo meta en Región X")
- ✅ Comparación automática entre períodos (YoY, MoM)
- ✅ Dashboard ejecutivo con KPIs clave

**📊 Ejemplo de uso:**
*"Cada lunes a las 8:00 AM, los 16 coordinadores regionales reciben automáticamente por email un reporte PDF con el resumen semanal de su región: matrícula actualizada, nuevos titulados, proyectos en ejecución y alertas si hay caídas significativas."*

**✅ Ventajas:**
- Proactivo (la información llega automáticamente)
- Reduce trabajo manual repetitivo
- Estandarización de formatos
- Detección temprana de problemas
- Mejora toma de decisiones

**❌ Desventajas:**
- Mayor complejidad técnica
- Requiere infraestructura de email
- Necesita mantenimiento de plantillas

**📦 Esfuerzo de implementación**: 4-6 semanas

---

### 🔍 COMPARACIÓN DE OPCIONES

| Característica | Solo Visualización | + Reportería Básica | + Reportería Programada |
|----------------|:------------------:|:-------------------:|:-----------------------:|
| Gráficos interactivos | ✅ | ✅ | ✅ |
| Filtros dinámicos | ✅ | ✅ | ✅ |
| Mapas geográficos | ✅ | ✅ | ✅ |
| Exportar Excel/CSV | ❌ | ✅ | ✅ |
| Generar PDFs | ❌ | ✅ | ✅ |
| Reportes automáticos | ❌ | ❌ | ✅ |
| Alertas programadas | ❌ | ❌ | ✅ |
| **Esfuerzo desarrollo** | Base | +2-3 sem | +4-6 sem |

---

### 🎯 DEFINICIÓN REQUERIDA #2

**Pregunta clave**: ¿Qué tipo de plataforma necesita la EMTP?

- [ ] **Opción A**: Solo visualización interactiva
- [ ] **Opción B**: Visualización + reportería básica (exportación bajo demanda)
- [ ] **Opción C**: Plataforma completa con reportería programada (Recomendado)

**Complementarias:**

Si se elige Opción B o C:

1. **¿Qué formatos de exportación se requieren?**
   - [ ] Excel (.xlsx)
   - [ ] CSV (datos crudos)
   - [ ] PDF (documentos formales)
   - [ ] PowerPoint (.pptx) con gráficos
   - [ ] Todos los anteriores

2. **¿Se requiere auditoría de reportes generados?**
   - [ ] Sí, registro de quién generó qué reporte y cuándo
   - [ ] No se requiere

Si se elige Opción C:

3. **¿Qué reportes automáticos se necesitan?**
   - [ ] Resumen semanal por región
   - [ ] Consolidado mensual nacional
   - [ ] Alertas de caída de matrícula
   - [ ] Estado de proyectos activos
   - [ ] Avance de metas anuales
   - [ ] Otros: _________________________

4. **¿A quiénes se enviarían reportes automáticos?**
   - [ ] Coordinadores regionales (16)
   - [ ] Jefatura SEEMTP
   - [ ] Directores de establecimientos EMTP
   - [ ] Otros: _________________________

---

## DEFINICIÓN 3: FUENTES Y CONEXIÓN DE DATOS

### ¿De dónde se alimentará el sistema con información oficial?

Actualmente el Visualizador funciona con **datos simulados** almacenados en archivos CSV locales. Para producción, se requiere **conectar a fuentes de datos reales** de la EMTP.

---

### FUENTES DE DATOS IDENTIFICADAS

#### **A. Bases de Datos Institucionales (Coordinación con TI MINEDUC)**

**Descripción**: Sistemas transaccionales oficiales del Ministerio de Educación.

**Fuentes potenciales:**
- 🗄️ **SIGE (Sistema de Información General de Estudiantes)**
  - Matrícula oficial por establecimiento
  - Datos de estudiantes EMTP
  
- 🗄️ **Registro de Titulados**
  - Certificaciones y títulos otorgados
  - Seguimiento post-egreso

- 🗄️ **Sistema Financiero MINEDUC**
  - Convenios activos SEEMTP
  - Rendiciones de proyectos
  - Transferencias a establecimientos

- 🗄️ **Bases de Datos Regionales**
  - Datos específicos por DEPROV/SEREMI

**Ventajas:**
- ✅ Datos oficiales y validados
- ✅ Actualización sistemática
- ✅ Integridad de información
- ✅ Trazabilidad completa

**Desafíos:**
- ⚠️ Requiere coordinación formal con TI
- ⚠️ Permisos de acceso a bases de producción
- ⚠️ Posibles restricciones de seguridad
- ⚠️ Tiempos de respuesta de TI

**📋 Acción requerida**: Reunión con Jefe TI MINEDUC para:
1. Identificar bases de datos disponibles
2. Solicitar accesos de lectura (read-only)
3. Definir tipo de conexión (SQL Server, PostgreSQL, API REST)
4. Establecer ventanas de actualización de datos

---

#### **B. SharePoint MINEDUC**

**Descripción**: Archivos Excel/CSV almacenados en carpetas compartidas de SharePoint.

**Fuentes potenciales:**
- 📊 **Planillas de seguimiento regional**
  - Subidas manualmente por coordinadores regionales
  - Datos de proyectos específicos

- 📊 **Reportes consolidados**
  - Generados por otras áreas del MINEDUC
  - Datos históricos no sistematizados

- 📊 **Información geográfica**
  - Mapas y shapefiles oficiales
  - Datos territoriales

**Ventajas:**
- ✅ Acceso inmediato (sin depender de TI)
- ✅ Control directo del área EMTP
- ✅ Flexibilidad para agregar fuentes
- ✅ Familiaridad del equipo con SharePoint

**Desafíos:**
- ⚠️ Calidad de datos variable
- ⚠️ Posible duplicidad o inconsistencias
- ⚠️ Actualización manual (no automática)
- ⚠️ Requiere estandarización de formatos

**📋 Acción requerida**: 
1. Listar carpetas SharePoint relevantes
2. Estandarizar formatos de archivos (plantillas Excel)
3. Definir responsables de actualización
4. Establecer calendario de carga de datos

---

#### **C. APIs Externas (Opcional)**

**Descripción**: Servicios web de otras instituciones públicas.

**Fuentes potenciales:**
- 🌐 **Chile Atiende / Gobierno Transparente**
  - Datos públicos de educación
  
- 🌐 **DEMRE (Sistema de Acceso)**
  - Postulaciones a Ed. Superior de egresados EMTP

**Ventajas:**
- ✅ Datos oficiales de otras instituciones
- ✅ Actualización automática

**Desafíos:**
- ⚠️ Disponibilidad no garantizada
- ⚠️ Requiere integración técnica compleja

---

### ARQUITECTURA PROPUESTA DE CONEXIÓN

```
┌─────────────────────────────────────────────────────────┐
│                  VISUALIZADOR EMTP                      │
│              (Aplicación Web - Dash)                    │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │  Capa de Datos      │
        │  (ETL / Integración)│
        └──────────┬──────────┘
                   │
        ┌──────────┼──────────┬────────────┐
        │          │          │            │
   ┌────▼───┐ ┌───▼────┐ ┌───▼─────┐ ┌───▼────┐
   │ SIGE   │ │ Titula-│ │SharePoi-│ │  Otros │
   │(TI)    │ │ dos(TI)│ │ nt EMTP │ │        │
   └────────┘ └────────┘ └─────────┘ └────────┘
   
   SQL Server   SQL Server   Excel/CSV    APIs

        FRECUENCIA DE ACTUALIZACIÓN:
        ├─ Datos críticos: Diario (matrícula)
        ├─ Datos analíticos: Semanal (proyectos)
        └─ Datos históricos: Mensual (consolidados)
```

---

### 🎯 DEFINICIÓN REQUERIDA #3

**Pregunta clave**: ¿Qué fuentes de datos se conectarán al Visualizador?

1. **Bases de datos MINEDUC (vía TI)**
   - [ ] SIGE (matrícula y estudiantes)
   - [ ] Sistema de Titulados
   - [ ] Sistema Financiero (convenios/rendiciones)
   - [ ] Otras bases: _________________________

2. **SharePoint SEEMTP**
   - [ ] Planillas regionales de seguimiento
   - [ ] Reportes consolidados
   - [ ] Datos geográficos
   - [ ] Otras carpetas: _________________________

3. **APIs Externas** (opcional)
   - [ ] Chile Atiende
   - [ ] DEMRE
   - [ ] Otras: _________________________

**Complementarias:**

1. **¿Quién coordinará con TI la conexión a bases de datos?**
   - [ ] Jefatura SEEMTP
   - [ ] Coordinador del proyecto (área técnica)
   - [ ] Otro: _________________________

2. **¿Con qué periodicidad deben actualizarse los datos?**
   - [ ] Tiempo real (cada hora)
   - [ ] Diario (cada noche)
   - [ ] Semanal (lunes de cada semana)
   - [ ] Mensual (primer día del mes)
   - [ ] Otra: _________________________

3. **¿Se requiere histórico de datos?**
   - [ ] Sí, mantener todos los datos históricos
   - [ ] Solo últimos 2 años
   - [ ] Solo último año
   - [ ] No se requiere histórico

4. **¿Quién será responsable de validar la calidad de datos?**
   - [ ] Área SEEMTP
   - [ ] TI MINEDUC
   - [ ] Responsabilidad compartida
   - [ ] Otro: _________________________

---

## RESUMEN DE DECISIONES REQUERIDAS

### ✅ CHECKLIST DE DEFINICIONES

#### 📌 **1. ACCESO Y USUARIOS**

- [ ] **Modelo de acceso definido** (público / perfiles / híbrido)
- [ ] **Perfiles de usuario aprobados** (básico / analista / admin)
- [ ] **Método de autenticación seleccionado** (credenciales propias / AD / Office365)
- [ ] **Responsable de gestión de usuarios asignado**
- [ ] **Requerimientos de auditoría especificados** (completa / básica / sin auditoría)

#### 📌 **2. TIPO DE PLATAFORMA**

- [ ] **Funcionalidad principal definida** (visualización / + reportería básica / + reportería programada)
- [ ] **Formatos de exportación seleccionados** (Excel / CSV / PDF / PPT)
- [ ] **Reportes automáticos especificados** (si aplica)
- [ ] **Destinatarios de reportes automáticos definidos** (si aplica)
- [ ] **Auditoría de reportes requerida** (sí / no)

#### 📌 **3. FUENTES DE DATOS**

- [ ] **Bases de datos TI identificadas** (SIGE / Titulados / Financiero / otras)
- [ ] **Carpetas SharePoint definidas**
- [ ] **Coordinador con TI asignado**
- [ ] **Periodicidad de actualización establecida** (real-time / diario / semanal / mensual)
- [ ] **Política de histórico definida** (cuántos años mantener)
- [ ] **Responsable de calidad de datos asignado**

---

## PRÓXIMOS PASOS

### RUTA CRÍTICA PARA PUESTA EN PRODUCCIÓN

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINICIONES ESTRATÉGICAS (Esta reunión)           │
│ • Completar checklist de decisiones                        │
│ • Aprobar modelo de acceso                                 │
│ • Definir tipo de plataforma                               │
│ • Identificar fuentes de datos                             │
│ ⏱️ Tiempo estimado: 1-2 semanas                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 2: COORDINACIÓN TI (Paralelo a desarrollo)            │
│ • Reunión formal con Jefe TI MINEDUC                       │
│ • Solicitud de accesos a bases de datos                    │
│ • Definición de arquitectura de conexión                   │
│ • Acuerdos de niveles de servicio (SLA)                    │
│ ⏱️ Tiempo estimado: 2-3 semanas                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 3: DESARROLLO E INTEGRACIÓN                           │
│ • Implementar sistema de usuarios (si aplica)              │
│ • Conectar fuentes de datos reales                         │
│ • Desarrollar reportería (si aplica)                       │
│ • Pruebas de integración                                   │
│ ⏱️ Tiempo estimado: 4-8 semanas (según alcance)           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 4: PRUEBAS Y CAPACITACIÓN                             │
│ • Pruebas con usuarios piloto                              │
│ • Ajustes y correcciones                                   │
│ • Capacitación a usuarios finales                          │
│ • Documentación de uso                                     │
│ ⏱️ Tiempo estimado: 2-3 semanas                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 5: PUESTA EN PRODUCCIÓN                               │
│ • Migración a servidor productivo                          │
│ • Creación de usuarios                                     │
│ • Monitoreo inicial                                        │
│ • Soporte post-implementación                              │
│ ⏱️ Tiempo estimado: 1 semana                               │
└─────────────────────────────────────────────────────────────┘

📅 TIEMPO TOTAL ESTIMADO: 3-4 meses desde definiciones hasta producción
```

---

### ACCIONES INMEDIATAS (Esta semana)

1. **Coordinación Nacional EMTP**:
   - [ ] Revisar este documento con jefatura
   - [ ] Completar checklist de definiciones
   - [ ] Priorizar decisiones críticas

2. **Reunión con TI MINEDUC**:
   - [ ] Agendar reunión con Jefe TI
   - [ ] Presentar proyecto Visualizador EMTP
   - [ ] Solicitar inventario de bases de datos disponibles
   - [ ] Explorar opciones de autenticación (AD/Office365)

3. **Estandarización SharePoint**:
   - [ ] Listar carpetas SharePoint relevantes
   - [ ] Revisar calidad de datos actuales
   - [ ] Crear plantillas estandarizadas (si aplica)

---

## ANEXOS

### ANEXO A: Capacidades Técnicas Actuales del Visualizador

**✅ Implementado y funcional:**
- Dashboard interactivo con 7 secciones de análisis
- Mapas geográficos (16 regiones, 345 comunas)
- Sistema de filtros dinámicos (región, comuna, especialidad, año, género, etc.)
- Navegación jerárquica de 3 niveles
- Sistema de autenticación básico (preparado para escalar)
- Configuración centralizada para múltiples fuentes de datos
- Logging y monitoreo básico
- Responsive design (funciona en móvil/tablet/desktop)

**🟡 Preparado pero no implementado:**
- Conexión a SQL Server
- Conexión a PostgreSQL
- Integración con SharePoint
- Exportación de reportes (Excel/PDF)
- Sistema de caché (Redis)
- Auditoría completa de accesos

**❌ No desarrollado (requiere especificación):**
- Gestión de usuarios (crear/editar/eliminar)
- Reportes programados automáticos
- Integración con Active Directory
- Alertas automáticas
- Sistema de backup automático

### ANEXO B: Datos Simulados Actuales

El prototipo funciona con **178,700 registros simulados**:

- **Matrícula Regional**: 36,411 registros (2015-2024)
- **Matrícula Comunal**: 142,289 registros (345 comunas)
- **Egresados**: ~15,000 registros simulados
- **Titulación**: ~12,000 registros simulados
- **Establecimientos**: ~1,500 registros simulados
- **Docentes**: ~8,000 registros simulados
- **Proyectos SEEMTP**: ~500 registros simulados

**Cobertura geográfica**: 16 regiones, 345 comunas  
**Especialidades**: 17 especialidades EMTP  
**Período**: 10 años (2015-2024)

### ANEXO C: Requerimientos Técnicos Mínimos

**Servidor (ambiente productivo):**
- CPU: 4 cores
- RAM: 8 GB mínimo (16 GB recomendado)
- Disco: 50 GB SSD
- Sistema Operativo: Windows Server 2019+ o Linux (Ubuntu 20.04+)
- Python 3.10+

**Red:**
- Puerto HTTPS abierto (443)
- Acceso a bases de datos TI (según definiciones)
- Acceso a SharePoint (si aplica)

**Usuarios concurrentes estimados:**
- Configuración actual: hasta 50 usuarios simultáneos
- Escalable hasta 200+ con ajustes de infraestructura

### ANEXO D: Estimación de Esfuerzos por Opción

| Componente | Opción Básica | Opción Media | Opción Completa |
|------------|---------------|--------------|-----------------|
| **Acceso** | Público (0 sem) | Perfiles (3 sem) | Perfiles + AD (4 sem) |
| **Plataforma** | Solo visual (0 sem) | + Export (2 sem) | + Reportería auto (5 sem) |
| **Datos** | CSV local (0 sem) | SharePoint (2 sem) | BD TI + SharePoint (6 sem) |
| **TOTAL** | **0 semanas** | **7 semanas** | **15 semanas** |
| **Esfuerzo** | Prototipo actual | Producción básica | Producción avanzada |

### ANEXO E: Contactos Clave

**Coordinación Nacional EMTP:**
- Responsable Técnico: [Nombre]
- Email: [email]
- Teléfono: [teléfono]

**TI MINEDUC:**
- Jefe TI: [Nombre pendiente de reunión]
- Email: [pendiente]
- Área: [pendiente]

**Desarrollador/Soporte Técnico:**
- Desarrollador: Andrés Lazcano
- Email: andreslazcano@[dominio]
- GitHub: github.com/andreslazcano-bit/Visualizador-EMTP-Dash

---

## DOCUMENTO DE TRABAJO

Este documento debe ser completado en reunión con jefatura SEEMTP y posteriormente presentado a TI MINEDUC para coordinación técnica.

**Fecha de revisión propuesta**: _________________  
**Participantes**: _________________  
**Decisiones tomadas**: _________________

---

**Fin del documento**

*Visualizador EMTP v2.0 | Noviembre 2025 | Coordinación Nacional EMTP*
