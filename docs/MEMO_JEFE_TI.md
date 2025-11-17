# MEMORÁNDUM - SOLICITUD DE REUNIÓN CON JEFE TI MINEDUC

**PARA:** Jefe de TI, Ministerio de Educación  
**DE:** Coordinación Nacional EMTP  
**ASUNTO:** Proyecto Visualizador EMTP - Solicitud de Reunión Técnica  
**FECHA:** [Completar]  
**REF:** Integración de Datos y Autenticación

---

## ANTECEDENTES

El área de Coordinación Nacional de Educación Media Técnico-Profesional (EMTP) ha desarrollado un **Visualizador de Datos EMTP**, plataforma web interactiva para centralizar y analizar información del sistema técnico-profesional.

Actualmente se encuentra en **estado de prototipo funcional** con datos simulados, y requiere coordinación con el área de TI para su puesta en producción.

---

## OBJETIVO DE LA REUNIÓN

Coordinar aspectos técnicos para conectar el Visualizador EMTP con fuentes de datos institucionales y definir método de autenticación de usuarios.

### Temas a tratar:

1. **Conexión a Bases de Datos MINEDUC**
   - Identificar bases disponibles (SIGE, Titulados, Sistema Financiero)
   - Solicitar accesos de lectura (read-only)
   - Definir tipo de conexión (SQL Server, PostgreSQL, API REST)
   - Establecer periodicidad de actualización de datos

2. **Autenticación de Usuarios**
   - Explorar integración con Active Directory MINEDUC
   - Alternativas: Office 365, credenciales propias
   - Definir perfiles de acceso (Usuario/Analista/Administrador)

3. **Infraestructura de Producción**
   - Requerimientos de servidor productivo
   - Arquitectura de red y seguridad
   - Políticas de backup y recuperación
   - Acuerdos de nivel de servicio (SLA)

---

## DESCRIPCIÓN DEL PROYECTO

### Visualizador EMTP - Características Técnicas

**Tecnología:**
- Framework: Python 3.12 + Dash (Plotly)
- Base de datos actual: CSV (datos simulados)
- Arquitectura: Aplicación web responsive
- Servidor web: Werkzeug (desarrollo) → Gunicorn (producción)

**Funcionalidades actuales:**
- Dashboard interactivo con 7 módulos de análisis
- Mapas geográficos (16 regiones, 345 comunas)
- Sistema de filtros dinámicos
- Autenticación básica (preparado para escalar)
- Logging y monitoreo

**Capacidad:**
- Usuarios concurrentes: 50+ (escalable a 200+)
- Registros procesados: 178,700 (prototipo simulado)
- Tiempo de respuesta: <2 segundos por consulta

---

## REQUERIMIENTOS TÉCNICOS

### 1. Acceso a Bases de Datos

**Bases de datos identificadas:**

| Base de Datos | Propósito | Datos Requeridos | Frecuencia |
|---------------|-----------|------------------|------------|
| **SIGE** | Matrícula oficial | Estudiantes EMTP por establecimiento | Diaria |
| **Sistema de Titulados** | Certificaciones | Títulos otorgados, seguimiento post-egreso | Semanal |
| **Sistema Financiero** | Gestión administrativa | Convenios SEEMTP, rendiciones, transferencias | Semanal |

**Tipo de acceso solicitado:**
- ✅ Solo lectura (read-only)
- ✅ Consultas parametrizadas (sin modificación de datos)
- ✅ Acceso desde IP específica (servidor productivo)

**Propuesta de conexión:**
```python
# Ejemplo: SQL Server
Driver: ODBC Driver 17 for SQL Server
Host: [servidor-bd.mineduc.cl]
Puerto: 1433
Database: [nombre_base]
Usuario: [usuario_readonly]
Password: [gestión segura]
```

---

### 2. Autenticación de Usuarios

**Perfiles propuestos:**

| Perfil | Usuarios típicos | Cantidad estimada | Permisos |
|--------|------------------|-------------------|----------|
| **Usuario Básico** | Directores EMTP, Docentes | ~100-200 | Solo visualización |
| **Analista SEEMTP** | Coordinadores regionales | ~30-50 | Visualización + Reportes |
| **Administrador** | Jefatura SEEMTP, TI | ~5-10 | Acceso total |

**Opciones de autenticación:**

**Opción A: Active Directory (Recomendado)**
- Integración con AD MINEDUC
- Usuarios usan credenciales institucionales
- Gestión centralizada de accesos

**Opción B: Office 365 / Microsoft Entra ID**
- Login con cuenta Microsoft institucional
- OAuth 2.0 / SAML
- Sin gestión local de usuarios

**Opción C: Sistema propio**
- Base de datos local de usuarios
- Gestión manual de credenciales
- Mayor autonomía, mayor carga administrativa

---

### 3. Infraestructura de Producción

**Requerimientos de servidor:**

| Componente | Especificación | Justificación |
|------------|----------------|---------------|
| **CPU** | 4 cores mínimo | Procesamiento de visualizaciones |
| **RAM** | 16 GB recomendado | Caché de datos, usuarios concurrentes |
| **Disco** | 100 GB SSD | Logs, datos temporales, backups |
| **Red** | Puerto 443 (HTTPS) | Acceso web seguro |
| **OS** | Windows Server 2019+ o Linux | Compatible con Python 3.12+ |

**Arquitectura propuesta:**

```
┌─────────────────────────────────────────┐
│          INTERNET                       │
└──────────────┬──────────────────────────┘
               │ HTTPS (443)
┌──────────────▼──────────────────────────┐
│   Firewall MINEDUC                      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Servidor Aplicación                   │
│   - Visualizador EMTP (Python/Dash)     │
│   - Gunicorn (WSGI)                     │
│   - Nginx (reverse proxy)               │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴───────┐
        │              │
┌───────▼────┐  ┌──────▼──────────┐
│ Active     │  │ Bases de Datos  │
│ Directory  │  │ MINEDUC         │
└────────────┘  └─────────────────┘
```

---

## DOCUMENTACIÓN TÉCNICA DISPONIBLE

1. **Código fuente completo:**  
   GitHub: `github.com/andreslazcano-bit/Visualizador-EMTP-Dash`

2. **Documentación técnica:**
   - `README.md`: Instalación y configuración
   - `ARQUITECTURA.md`: Diseño del sistema
   - `requirements.txt`: Dependencias Python

3. **Demo funcional:**  
   Disponible para revisión en ambiente de desarrollo

---

## CRONOGRAMA PROPUESTO

| Fase | Actividad | Responsable | Tiempo |
|------|-----------|-------------|--------|
| **1** | Reunión inicial TI + EMTP | Ambos | Esta semana |
| **2** | Inventario de BD disponibles | TI | 1 semana |
| **3** | Solicitud formal de accesos | EMTP → TI | 1 semana |
| **4** | Aprobación y creación de credenciales | TI | 2 semanas |
| **5** | Integración y pruebas | EMTP | 3-4 semanas |
| **6** | Despliegue en producción | TI + EMTP | 1 semana |

**Tiempo total estimado:** 8-10 semanas

---

## BENEFICIOS PARA MINEDUC

✅ **Centralización de datos EMTP**
- Información de múltiples fuentes en un solo lugar
- Reducción de solicitudes ad-hoc a TI

✅ **Reducción de carga operativa**
- Consultas self-service (usuarios buscan sus propios datos)
- Menos reportes manuales

✅ **Mejora en toma de decisiones**
- Datos actualizados y accesibles
- Visualización intuitiva de tendencias

✅ **Cumplimiento normativo**
- Auditoría de accesos
- Transparencia de datos públicos

---

## SOLICITUD ESPECÍFICA

**Se solicita agendar reunión técnica con:**
- Jefe de TI MINEDUC
- Arquitecto de Bases de Datos (si aplica)
- Responsable de Seguridad / Active Directory
- Coordinador Nacional EMTP

**Fecha propuesta:** [Sugerir 2-3 opciones]  
**Duración:** 60 minutos  
**Modalidad:** Presencial / Virtual (según preferencia)  
**Ubicación/Link:** A coordinar

---

## CONTACTO

**Coordinación Nacional EMTP**  
Responsable: [Tu nombre completo]  
Cargo: [Tu cargo]  
Email: [tu email institucional]  
Teléfono: [tu teléfono]  
Oficina: [ubicación física]

**Desarrollador Técnico**  
Nombre: Andrés Lazcano  
Email: [email]  
GitHub: github.com/andreslazcano-bit

---

## ANEXOS

1. Documento técnico completo: `DEFINICIONES_PARA_PRODUCCION.md`
2. Diagrama de arquitectura del sistema
3. Lista de dependencias técnicas (`requirements.txt`)
4. Capturas de pantalla del prototipo funcional

---

**Agradecemos su atención y colaboración para llevar este proyecto a producción en beneficio del sistema EMTP.**

---

**[Firma]**  
[Nombre]  
[Cargo]  
Coordinación Nacional EMTP  
Ministerio de Educación

---

## PLANTILLA DE EMAIL (Versión corta)

---

**Asunto:** Proyecto Visualizador EMTP - Solicitud de Reunión Técnica

Estimado/a [Nombre Jefe TI],

Junto con saludar, me dirijo a usted para solicitar una reunión técnica en el marco del proyecto **Visualizador de Datos EMTP** que hemos desarrollado en la Coordinación Nacional de Educación Técnico-Profesional.

**Contexto:**  
Hemos desarrollado una plataforma web interactiva para centralizar y visualizar datos del sistema EMTP. Actualmente funciona con datos simulados y está lista para conectarse a fuentes de datos reales del MINEDUC.

**Objetivo de la reunión:**  
Coordinar aspectos técnicos para:
1. Conexión a bases de datos institucionales (SIGE, Titulados, Sistema Financiero)
2. Integración con Active Directory / autenticación de usuarios
3. Despliegue en infraestructura productiva

**Documentación:**  
El proyecto es open-source y está disponible en GitHub para su revisión técnica:  
https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash

**Propuesta de reunión:**
- Duración: 60 minutos
- Participantes: Jefe TI, Arquitecto BD (si aplica), Coordinación EMTP
- Fechas sugeridas: [Opción 1], [Opción 2], [Opción 3]

Adjunto memorándum con detalles técnicos completos.

Quedo atento/a a su confirmación.

Saludos cordiales,

[Tu nombre]  
[Tu cargo]  
Coordinación Nacional EMTP  
[Email] | [Teléfono]

---
