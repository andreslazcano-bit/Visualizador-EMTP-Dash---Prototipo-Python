# 🎯 VISUALIZADOR EMTP - ASPECTOS CLAVE PARA JEFATURA

> **Documento preparado para**: Reunión de presentación con jefatura SEEMTP  
> **Fecha**: Noviembre 2025  
> **Propósito**: Definir decisiones estratégicas y operativas para puesta en producción

---

## 📊 ÍNDICE DE CONTENIDOS

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Funcionalidades Implementadas](#2-funcionalidades-implementadas)
3. [Decisiones Estratégicas Requeridas](#3-decisiones-estratégicas-requeridas)
4. [Definiciones Técnicas Necesarias](#4-definiciones-técnicas-necesarias)
5. [Recursos y Coordinaciones](#5-recursos-y-coordinaciones)
6. [Riesgos y Mitigaciones](#6-riesgos-y-mitigaciones)
7. [Plan de Implementación](#7-plan-de-implementación)

---

## 1. RESUMEN EJECUTIVO

### ✅ Estado Actual del Proyecto

| Aspecto | Estado | Detalle |
|---------|--------|---------|
| **Desarrollo** | ✅ Funcional | Prototipo 100% operativo con datos simulados |
| **Stack Tecnológico** | ✅ Moderno | Python 3.12 + Dash 2.14.2 + Plotly 5.18.0 |
| **Arquitectura** | ✅ Documentada | Diagramas y documentación técnica completa |
| **Autenticación** | ✅ Implementada | Sistema de perfiles con bcrypt + JWT |
| **Visualizaciones** | ✅ Completas | 7 módulos + mapas geográficos interactivos |
| **Conexión BD** | 🟡 Pendiente TI | Scripts listos, requiere credenciales MINEDUC |
| **Producción** | ⏳ Requiere decisiones | Ver secciones 3 y 4 de este documento |

### 🎯 Valor del Proyecto

- **Centralización**: Un solo sistema para todos los datos EMTP (vs. múltiples Excel/R scripts dispersos)
- **Accesibilidad**: Dashboards interactivos accesibles desde cualquier navegador (vs. R/Shiny que requiere instalación)
- **Actualización**: Datos actualizados automáticamente cada semana (vs. actualización manual mensual)
- **Escalabilidad**: Arquitectura preparada para crecer con nuevas funcionalidades
- **Seguridad**: Control de acceso por perfiles + auditoría de uso

---

## 2. FUNCIONALIDADES IMPLEMENTADAS

### 📈 Módulos de Análisis (7 secciones)

#### 2.1 Matrícula EMTP
**¿Qué hace?**
- Evolución histórica de matrícula (últimos 10 años)
- Distribución por región, comuna, especialidad
- Análisis demográfico (género, edad, procedencia)
- Tasas de retención y deserción

**¿Para qué sirve?**
- Planificación de recursos educativos
- Identificación de especialidades con alta/baja demanda
- Focalización de programas de retención

**Usuarios principales**: Coordinadores regionales, Jefatura SEEMTP

---

#### 2.2 Egresados EMTP
**¿Qué hace?**
- Seguimiento de trayectorias post-egreso
- Transición a educación superior (%, carreras, instituciones)
- Inserción laboral temprana
- Articulación con CFT/IP/Universidades

**¿Para qué sirve?**
- Evaluar efectividad de articulación con educación superior
- Identificar brechas en transición educativa
- Ajustar programas de orientación vocacional

**Usuarios principales**: Analistas SEEMTP, Investigadores

---

#### 2.3 Titulación EMTP
**¿Qué hace?**
- Tasas de titulación por especialidad y región
- Tiempos promedio de titulación
- Comparación histórica
- Identificación de cuellos de botella

**¿Para qué sirve?**
- Detectar especialidades con problemas de titulación
- Implementar apoyos específicos
- Reportar indicadores a nivel ministerial

**Usuarios principales**: Jefatura SEEMTP, Supervisores regionales

---

#### 2.4 Establecimientos EMTP
**¿Qué hace?**
- Catastro de 1,124 establecimientos EMTP
- Distribución geográfica (16 regiones, 345 comunas)
- Tipo de dependencia (Municipal, Particular Subvencionado, etc.)
- Infraestructura y capacidad

**¿Para qué sirve?**
- Planificación territorial de programas
- Asignación de recursos (equipamiento, talleres)
- Identificación de brechas de cobertura

**Usuarios principales**: Coordinadores territoriales, Planificadores

---

#### 2.5 Docentes EMTP
**¿Qué hace?**
- Perfil profesional (~5,000 docentes)
- Especialidades por defecto/superávit
- Capacitación y perfeccionamiento
- Distribución geográfica

**¿Para qué sirve?**
- Planificación de programas de capacitación
- Detección de necesidades de contratación
- Asignación de especialistas

**Usuarios principales**: Recursos Humanos, Centros de Perfeccionamiento

---

#### 2.6 Mapas Geográficos Interactivos
**¿Qué hace?**
- **Mapa de Matrícula**: Visualización coroplética de distribución territorial
- **Mapa de Establecimientos**: Ubicación geográfica de los 1,124 centros
- Filtros dinámicos (región, comuna, especialidad)
- Tablas resumen asociadas

**¿Para qué sirve?**
- Visualización rápida de desigualdades territoriales
- Identificación de zonas desatendidas
- Presentaciones a autoridades con mapas impactantes

**Usuarios principales**: Todos los perfiles, especialmente jefatura para presentaciones

---

#### 2.7 Monitoreo y Seguimiento de Proyectos 🔒
**¿Qué hace?**
- **Gestión Administrativa**: Convenios activos, rendiciones, presupuesto
- **Fortalecimiento EMTP**: 
  - Equipamiento Regular
  - Equipamiento SLEP
  - Red Futuro Técnico
  - Apoyo SLEP

**¿Para qué sirve?**
- Control financiero de proyectos
- Seguimiento de ejecución presupuestaria
- Cumplimiento de hitos y compromisos

**Usuarios principales**: 🔒 Solo Administradores (datos sensibles)

---

### 🎨 Características Técnicas

| Característica | Implementación | Beneficio |
|----------------|----------------|-----------|
| **Mapas Reales** | GeoJSON oficial de Chile (16 regiones, 345 comunas) | Precisión geográfica, no mapas genéricos |
| **Colores Institucionales** | Paleta MINEDUC (#34536A, #B35A5A, #C2A869) | Coherencia visual con branding institucional |
| **Responsive Design** | Funciona en desktop, tablet, móvil | Acceso desde cualquier dispositivo |
| **Tema Claro/Oscuro** | Switch integrado | Comodidad visual para usuarios |
| **Filtros Dinámicos** | Por región, comuna, especialidad, año, género | Exploración flexible de datos |
| **Autenticación Segura** | bcrypt (12 rounds) + JWT (24h) | Protección de datos sensibles |
| **Logs de Auditoría** | Registro de accesos y acciones | Trazabilidad y compliance |

---

## 3. DECISIONES ESTRATÉGICAS REQUERIDAS

### 🔑 DECISIÓN 1: Modelo de Acceso y Usuarios

#### Opciones Disponibles

| Opción | Pros | Contras | ¿Cuándo usar? |
|--------|------|---------|---------------|
| **A. Público sin Login** | • Máxima transparencia<br>• Cero fricción de acceso<br>• Sin gestión de usuarios | • Sin control de acceso<br>• Sin auditoría<br>• Riesgo de mal uso de datos | Solo si TODOS los datos son públicos |
| **B. Perfiles con Login** ⭐ | • Control granular de acceso<br>• Auditoría completa<br>• Protección de datos sensibles<br>• Personalización por perfil | • Requiere gestión de usuarios<br>• Fricción inicial (login) | **RECOMENDADO** para datos institucionales |
| **C. Híbrido** | • Equilibrio transparencia/control<br>• Dashboards públicos + secciones privadas | • Mayor complejidad técnica<br>• Usuarios pueden confundirse | Si hay mix de datos públicos/privados |

#### ⭐ RECOMENDACIÓN: Opción B - Perfiles con Login

**Razones**:
1. **Sección "Monitoreo y Seguimiento de Proyectos" contiene datos sensibles** (convenios, rendiciones, presupuesto)
2. **Auditoría es crítica** para saber quién accede a qué información
3. **Escalabilidad**: Permite agregar más perfiles en el futuro (ej: "Director de establecimiento" con acceso solo a sus datos)
4. **Compliance**: Cumplimiento de normativas de protección de datos

**Perfiles propuestos**:

| Perfil | Usuarios Típicos | Permisos | Cantidad Estimada |
|--------|-----------------|----------|-------------------|
| **👤 Usuario Básico** | • Directores EMTP<br>• Docentes<br>• Sostenedores | • Ver dashboards públicos (Matrícula, Egresados, Titulación, Docentes)<br>• Ver mapas<br>❌ Sin acceso a Proyectos | ~100-200 usuarios |
| **👔 Analista SEEMTP** | • Coordinadores regionales<br>• Analistas de datos<br>• Investigadores | • Todo lo anterior<br>• Exportar datos (Excel/PDF)<br>• Filtros avanzados<br>• Acceso a Proyectos (solo lectura) | ~30-50 usuarios |
| **⚙️ Administrador** | • Jefatura SEEMTP<br>• Equipo TI<br>• Directores de área | • Acceso total<br>• Gestión de usuarios<br>• Configuración sistema<br>• Acceso completo a Proyectos | ~5-10 usuarios |

**Pregunta clave para jefatura**: 
> ❓ **¿Están de acuerdo con este modelo de perfiles? ¿Agregar/quitar algún perfil?**

---

### 🔐 DECISIÓN 2: Método de Autenticación

#### Opciones Disponibles

| Método | Ventajas | Desventajas | Esfuerzo TI |
|--------|----------|-------------|-------------|
| **A. Active Directory (AD)** | • Usuarios usan credenciales institucionales<br>• Gestión centralizada<br>• SSO (Single Sign-On)<br>• Sin contraseñas adicionales | • Requiere integración con AD MINEDUC<br>• Depende de infraestructura existente | 🟡 Medio (2-3 semanas) |
| **B. Microsoft 365 / Entra ID** ⭐ | • OAuth 2.0 estándar<br>• Usuarios ya tienen cuenta M365<br>• MFA (autenticación multifactor)<br>• Más moderno que AD | • Requiere permisos de API Azure<br>• Configuración inicial | 🟡 Medio (2-3 semanas) |
| **C. Credenciales Propias** | • No depende de sistemas externos<br>• Control total<br>• Rápido de implementar | • Usuarios deben recordar otra contraseña<br>• Gestión manual de cuentas<br>• Sin integración con ecosistema MINEDUC | 🟢 Bajo (1 semana) |

#### ⭐ RECOMENDACIÓN: Opción B - Microsoft 365 / Entra ID

**Razones**:
1. **Todos los funcionarios MINEDUC ya tienen cuenta Microsoft 365**
2. **Experiencia de usuario fluida**: "Iniciar sesión con Microsoft" (un click)
3. **Seguridad robusta**: MFA, políticas de contraseñas institucionales
4. **Sin gestión manual**: TI no tiene que crear/desactivar cuentas manualmente
5. **Estándar moderno**: OAuth 2.0 es el estándar de la industria

**Pregunta clave para jefatura**:
> ❓ **¿Prefieren integración con Microsoft 365 o gestionar credenciales propias?**

---

### 📊 DECISIÓN 3: Alcance de Funcionalidades

#### ¿Qué tipo de plataforma necesitamos?

| Alcance | Incluye | ¿Cuándo usar? | Esfuerzo Desarrollo |
|---------|---------|---------------|---------------------|
| **A. Solo Visualización** | • Dashboards interactivos<br>• Mapas<br>• Filtros básicos | Si el objetivo es solo explorar datos visualmente | ✅ Ya implementado |
| **B. Visualización + Reportería Básica** ⭐ | • Todo lo anterior<br>• **Exportar Excel**<br>• **Exportar PDF**<br>• Descargar tablas filtradas | **RECOMENDADO**: Analistas necesitan datos para informes | 🟡 +2 semanas |
| **C. Plataforma Completa** | • Todo lo anterior<br>• **Reportes programados** (envío automático por email)<br>• **Alertas** (notificaciones de umbrales)<br>• **Comparador temporal** (antes/después) | Si necesitan monitoreo proactivo y automatización | 🔴 +6 semanas |

#### ⭐ RECOMENDACIÓN: Opción B - Visualización + Reportería Básica

**Razones**:
1. **Analistas necesitan compartir datos** en reuniones, informes, presentaciones
2. **Excel es el formato estándar** de trabajo en el ministerio
3. **PDF para reportes ejecutivos** con gráficos incluidos
4. **Equilibrio esfuerzo/beneficio**: Gran valor con desarrollo moderado

**Ejemplos de uso**:
- Coordinador regional descarga tabla de matrícula por comuna → Excel → Informe mensual
- Jefatura exporta mapa de distribución → PDF → Presentación a Ministro
- Analista extrae datos de titulación → Excel → Análisis estadístico avanzado en R/SPSS

**Pregunta clave para jefatura**:
> ❓ **¿Es suficiente con exportación básica o necesitan reportes automatizados?**

---

### 📅 DECISIÓN 4: Frecuencia de Actualización de Datos

#### Opciones de Estrategia

| Frecuencia | Cómo Funciona | Ventajas | Desventajas |
|------------|---------------|----------|-------------|
| **Tiempo Real** | Consultas directas a SQL Server | • Datos siempre actuales | • Lento (5-10 segundos por dashboard)<br>• Sobrecarga de base de datos |
| **Diaria** | Cache actualizado cada noche | • Datos "casi" actuales<br>• Rápido | • Carga nocturna de servidor<br>• Innecesario para datos educativos |
| **Semanal** ⭐ | Cache actualizado cada lunes 2AM | • **Suficiente para datos educativos**<br>• Dashboards instantáneos<br>• Sin sobrecarga | • Datos con max 7 días de retraso |
| **Mensual** | Cache actualizado 1er día del mes | • Mínima carga de servidor | • Puede ser muy desactualizado |

#### ⭐ RECOMENDACIÓN: Actualización Semanal (cada lunes 2AM)

**Razones**:
1. **Datos educativos NO cambian minuto a minuto** (matrícula, titulación son anuales/semestrales)
2. **SIGE se actualiza semanalmente** → Sincronizamos después de su actualización
3. **Dashboards instantáneos**: 0.5 segundos vs. 5-10 segundos con SQL directo
4. **Sin sobrecarga de bases de datos productivas** de MINEDUC

**Sistema implementado** (ver `docs/ACTUALIZACION_AUTOMATICA.md`):
- ✅ Script de actualización automática (`scripts/actualizar_datos_semanal.py`)
- ✅ Cron job configurado para lunes 2AM
- ✅ Formato Parquet (10x más rápido que CSV, comprimido)
- ✅ Logs completos de actualización
- ✅ Fallback a CSV si cache falla

**Pregunta clave para jefatura**:
> ❓ **¿Es aceptable que los datos tengan máximo 7 días de antigüedad?**

---

## 4. DEFINICIONES TÉCNICAS NECESARIAS

### 🖥️ DEFINICIÓN TÉCNICA 1: Infraestructura de Hosting

#### Opciones Disponibles

| Opción | Características | Costo Mensual Estimado | Esfuerzo Despliegue |
|--------|----------------|------------------------|---------------------|
| **A. Servidor On-Premise MINEDUC** | • Servidor físico/virtual en datacenter MINEDUC<br>• Control total<br>• Sin costos cloud | $0 (usa infraestructura existente) | 🟡 Medio (TI debe provisionar) |
| **B. Azure (Microsoft)** ⭐ | • App Service Python<br>• Integración con M365<br>• Escalable automáticamente<br>• Backups automáticos | ~$50-100 USD/mes | 🟢 Bajo (deploy automático) |
| **C. AWS (Amazon)** | • EC2 + RDS<br>• Gran flexibilidad<br>• Más complejo | ~$80-150 USD/mes | 🔴 Alto (configuración manual) |
| **D. Heroku (Simple)** | • Despliegue ultra-simple<br>• Menos control<br>• Más caro a escala | ~$25-50 USD/mes (inicio) | 🟢 Muy bajo (git push) |

#### ⭐ RECOMENDACIÓN: Azure App Service

**Razones**:
1. **Ecosistema Microsoft**: MINEDUC ya usa M365, Teams, SharePoint → sinergia
2. **Integración nativa con Entra ID** para autenticación
3. **Compliance chileno**: Azure tiene datacenter en Brasil (latencia baja)
4. **Soporte técnico Microsoft** incluido
5. **Escalamiento automático**: Si usuarios crecen, el servidor se adapta

**Configuración recomendada**:
- **Tier**: B1 Basic (~$50 USD/mes) → Soporta hasta 500 usuarios concurrentes
- **Base de Datos**: Azure SQL Database (si no usan SQL Server on-premise)
- **Almacenamiento**: Azure Blob Storage para archivos Parquet/CSV
- **Región**: Brazil South (menor latencia desde Chile)

**Pregunta clave para jefatura**:
> ❓ **¿Tienen presupuesto para hosting cloud (~$600 USD/año) o prefieren servidor interno?**

---

### 🗄️ DEFINICIÓN TÉCNICA 2: Conexión a Bases de Datos MINEDUC

#### Bases de Datos Requeridas

| Base de Datos | Información | Frecuencia Actualización | Acceso Requerido |
|---------------|-------------|--------------------------|------------------|
| **SIGE** | • Matrícula EMTP<br>• Establecimientos<br>• Cursos y especialidades | Semanal | Read-only |
| **Sistema de Titulados** | • Titulación por especialidad<br>• Tiempos de titulación | Mensual | Read-only |
| **Sistema Financiero** | • Convenios (Proyectos)<br>• Rendiciones<br>• Presupuesto | Semanal | Read-only |
| **SharePoint SEEMTP** (opcional) | • Documentos de proyectos<br>• Informes regionales | Semanal | Read-only |

#### Coordinación con TI MINEDUC

**Necesitamos de TI**:

1. **Credenciales de acceso SQL Server**:
   ```
   - Hostname: sql-sige.mineduc.cl (ejemplo)
   - Database: SIGE_Produccion
   - Usuario: app_visualizador_readonly
   - Password: [generado por TI]
   - Puerto: 1433
   ```

2. **Configuración de red**:
   - ✅ Whitelist de IP del servidor de la app
   - ✅ Reglas de firewall para puerto 1433
   - ✅ VPN si es necesario (acceso desde Azure)

3. **Permisos de base de datos**:
   - ✅ Solo **lectura (SELECT)** en tablas específicas
   - ❌ **Sin permisos de escritura** (seguridad)

**Scripts ya implementados** (listos para usar cuando TI entregue credenciales):
- ✅ `scripts/test_connections.py` - Verificar conectividad
- ✅ `scripts/actualizar_datos_semanal.py` - Actualización automática
- ✅ `src/data/loaders.py` - Cargador de datos con cache

**Pregunta clave para jefatura**:
> ❓ **¿Pueden coordinar reunión con Jefe TI para solicitar estos accesos?** (ver `_docs-planificacion/MEMO_JEFE_TI.md`)

---

### 📧 DEFINICIÓN TÉCNICA 3: Notificaciones y Alertas (Opcional)

#### ¿Queremos que el sistema envíe notificaciones?

**Ejemplos de notificaciones útiles**:

| Tipo | Ejemplo | ¿Cuándo? |
|------|---------|----------|
| **Alertas de actualización** | "✅ Datos actualizados exitosamente (17/11/2025)" | Cada lunes después de actualización |
| **Errores críticos** | "❌ Error al actualizar datos de SIGE - Verificar conexión" | Cuando falla actualización |
| **Reportes programados** | "📊 Reporte semanal de matrícula - Adjunto Excel" | Cada viernes automático |
| **Umbrales** | "⚠️ Deserción en Región Metropolitana superó 15%" | Cuando KPI supera límite |

**Configuración necesaria**:
- Servidor SMTP MINEDUC (para enviar emails)
- Lista de destinatarios por tipo de alerta
- Configuración de horarios

**Pregunta clave para jefatura**:
> ❓ **¿Quieren notificaciones automáticas o prefieren revisar manualmente?**

---

## 5. RECURSOS Y COORDINACIONES

### 👥 Equipo Necesario

| Rol | Responsabilidad | Dedicación | ¿Quién? |
|-----|-----------------|------------|---------|
| **Líder de Proyecto** | Decisiones estratégicas, priorización | 20% (1 día/semana) | Jefatura SEEMTP |
| **Desarrollador Principal** | Desarrollo, mantenimiento, bugs | 100% (1-2 meses iniciales, luego 20%) | Actual (Andrés) |
| **TI MINEDUC** | Accesos BD, infraestructura, despliegue | 20% (durante setup) | Coordinador TI |
| **Analista Funcional** | Validación de datos, pruebas, feedback | 10% (durante desarrollo) | Analista SEEMTP senior |
| **Usuario Piloto** | Testing, feedback de usabilidad | 5% (2-3 sesiones) | 2-3 usuarios reales |

### 🤝 Coordinaciones Externas

#### Con TI MINEDUC
**Contacto**: Jefe de Infraestructura TI (ver `_docs-planificacion/MEMO_JEFE_TI.md`)

**Temas a coordinar**:
1. ✅ Acceso a bases de datos SQL Server (SIGE, Titulados, Financiero)
2. ✅ Provisión de servidor (on-premise o aprobación para Azure)
3. ✅ Configuración de red (firewalls, VPN)
4. ✅ Integración con Microsoft 365 / Entra ID (autenticación)
5. ✅ Soporte técnico post-producción

**Tiempo estimado de respuesta**: 2-4 semanas

---

#### Con Unidad de Datos MINEDUC (si existe)
**Temas**:
- Validación de consultas SQL (eficiencia, correctitud)
- Definición de indicadores clave (KPIs)
- Acceso a documentación de bases de datos

---

#### Con Unidad de Comunicaciones (Opcional)
**Temas**:
- Validación de paleta de colores institucional
- Logo MINEDUC para interfaz
- Textos de ayuda/instrucciones

---

### 💰 Presupuesto Estimado

| Ítem | Costo | Frecuencia | Detalle |
|------|-------|------------|---------|
| **Desarrollo inicial** | $0 | Una vez | Ya realizado (prototipo funcional) |
| **Hosting Azure** | $50-100 USD | Mensual | App Service B1 + Storage |
| **Base de datos Azure SQL** (si no usan on-premise) | $30-50 USD | Mensual | Tier básico |
| **Dominio personalizado** (ej: visualizador-emtp.mineduc.cl) | $12 USD | Anual | Opcional |
| **Certificado SSL** | $0 | - | Incluido en Azure |
| **Soporte técnico** | $0 | - | Microsoft 365 existente |
| **Mantenimiento** | 1-2 días/mes | Continuo | Bugs, actualizaciones menores |
| **TOTAL ANUAL** | ~$1,200 USD/año | - | Escenario cloud (Azure) |
| **ALTERNATIVA: On-premise** | $0 | - | Si TI provee servidor interno |

**Comparación de costos vs. alternativas**:
- Licencia Tableau: ~$70 USD/usuario/mes x 50 usuarios = **$42,000 USD/año** 😱
- Licencia Power BI Pro: ~$10 USD/usuario/mes x 50 usuarios = **$6,000 USD/año**
- **Esta solución**: ~$1,200 USD/año = **95% más barato que Power BI** ✅

---

## 6. RIESGOS Y MITIGACIONES

### ⚠️ Riesgo 1: Retraso en Acceso a Bases de Datos

**Probabilidad**: 🟡 Media  
**Impacto**: 🔴 Alto (bloquea conexión a datos reales)

**Mitigación**:
- ✅ Iniciar coordinación con TI **de inmediato** (memo ya preparado)
- ✅ Mientras tanto, seguir trabajando con **datos simulados** (ya funcionales)
- ✅ Pedir acceso solo de **lectura** (menos burocracia que permisos de escritura)
- ✅ Si demora >4 semanas, evaluar **exportación manual CSV** desde SIGE como plan B

---

### ⚠️ Riesgo 2: Cambios en Estructura de Bases de Datos

**Probabilidad**: 🟢 Baja (SIGE es estable)  
**Impacto**: 🟡 Medio (requiere actualizar queries)

**Mitigación**:
- ✅ Documentar todas las consultas SQL claramente
- ✅ Usar **vistas de base de datos** (TI crea vistas estables, aunque tablas cambien)
- ✅ Tests automáticos que detecten cambios de esquema
- ✅ Logs detallados de errores de actualización

---

### ⚠️ Riesgo 3: Sobrecarga de Usuarios (Escalabilidad)

**Probabilidad**: 🟢 Baja (inicialmente <100 usuarios)  
**Impacto**: 🟡 Medio (sistema lento)

**Mitigación**:
- ✅ **Azure autoscaling**: Servidor crece automáticamente si hay carga
- ✅ **Cache de datos**: Dashboards cargan desde archivos locales (no SQL directo)
- ✅ **Monitoreo**: Alertas si tiempo de respuesta >3 segundos
- ✅ **Plan de upgrade**: Si llega a >500 usuarios, subir a tier superior (~$100 USD/mes)

---

### ⚠️ Riesgo 4: Resistencia al Cambio (Usuarios Prefieren Excel/R)

**Probabilidad**: 🟡 Media (cambio cultural)  
**Impacto**: 🟡 Medio (baja adopción)

**Mitigación**:
- ✅ **Capacitación inicial**: Sesión de 1 hora mostrando beneficios
- ✅ **Usuarios piloto**: Seleccionar "early adopters" entusiastas
- ✅ **Exportación a Excel**: Permitir que usuarios lleven datos a su herramienta favorita
- ✅ **Comunicación de valor**: "En 10 segundos tienes un mapa que antes tomaba 2 horas"
- ✅ **No forzar**: Sistema coexiste con Excel/R, no los reemplaza inmediatamente

---

### ⚠️ Riesgo 5: Errores en Datos (Basura In → Basura Out)

**Probabilidad**: 🟡 Media (SIGE puede tener inconsistencias)  
**Impacto**: 🔴 Alto (decisiones erróneas basadas en datos malos)

**Mitigación**:
- ✅ **Validación de datos**: Scripts detectan valores fuera de rango (ej: matrícula negativa)
- ✅ **Auditoría**: Logs muestran de dónde viene cada dato
- ✅ **Comparación histórica**: Alertas si dato cambia >50% respecto a semana anterior
- ✅ **Disclaimer en dashboards**: "Datos provenientes de SIGE - Última actualización: XX/XX/XXXX"
- ✅ **Feedback loop**: Usuarios pueden reportar datos sospechosos

---

## 7. PLAN DE IMPLEMENTACIÓN

### 📅 Cronograma Estimado (12 semanas)

#### **Fase 1: Definiciones y Coordinación** (Semanas 1-2)

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Reunión de presentación a jefatura (esta presentación) | Desarrollador | ✅ Decisiones aprobadas |
| Elaborar memo para Jefe TI MINEDUC | Jefatura SEEMTP | ✅ Solicitud formal |
| Definir usuarios piloto (3-5 personas) | Jefatura | ✅ Lista de contactos |
| Aprobar presupuesto (si es Azure) | Administración | ✅ PO/facturación |

**Hito**: Decisiones estratégicas tomadas + Coordinación TI iniciada

---

#### **Fase 2: Configuración Técnica** (Semanas 3-5)

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| TI entrega credenciales SQL Server | TI MINEDUC | ✅ .env con credenciales |
| Configurar servidor (Azure o on-premise) | TI + Desarrollador | ✅ Servidor funcional |
| Probar conexiones a bases de datos | Desarrollador | ✅ Test exitoso |
| Primera actualización de datos reales | Desarrollador | ✅ Cache con datos SIGE |
| Configurar autenticación M365 (si aprobado) | TI + Desarrollador | ✅ Login con Office365 |

**Hito**: Sistema conectado a datos reales de MINEDUC

---

#### **Fase 3: Desarrollo de Funcionalidades Adicionales** (Semanas 6-8)

*Solo si se aprobó Opción B en Decisión 3 (Reportería Básica)*

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Implementar exportación a Excel | Desarrollador | ✅ Botón "Exportar Excel" funcional |
| Implementar exportación a PDF | Desarrollador | ✅ Botón "Exportar PDF" con gráficos |
| Agregar filtros avanzados para analistas | Desarrollador | ✅ Filtros por múltiples dimensiones |
| Validación con usuarios piloto | Usuarios piloto | ✅ Feedback documentado |

**Hito**: Funcionalidades de reportería implementadas

---

#### **Fase 4: Testing y Refinamiento** (Semanas 9-10)

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Testing de carga (simular 50 usuarios) | Desarrollador | ✅ Reporte de performance |
| Revisión de usabilidad (usuarios piloto) | Usuarios piloto | ✅ Ajustes de UX |
| Validación de datos vs. fuentes oficiales | Analista SEEMTP | ✅ Datos verificados |
| Documentación de usuario final | Desarrollador | ✅ Manual de usuario + videos |
| Configurar monitoreo y alertas | Desarrollador | ✅ Dashboard de salud del sistema |

**Hito**: Sistema validado y refinado

---

#### **Fase 5: Capacitación y Lanzamiento** (Semanas 11-12)

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Sesión de capacitación a usuarios finales (1h) | Desarrollador + Jefatura | ✅ Grabación + material |
| Crear usuarios en sistema (si login propio) | TI + Desarrollador | ✅ Cuentas activas |
| Comunicación oficial de lanzamiento | Jefatura | ✅ Email/Teams a usuarios |
| Soporte "hot" primera semana (chat/email) | Desarrollador | ✅ Resolución rápida de dudas |
| Monitoreo de adopción (analytics) | Desarrollador | ✅ Reporte de uso |

**Hito**: 🎉 **Sistema en producción y usuarios activos**

---

### 📊 Indicadores de Éxito (Post-Lanzamiento)

| Indicador | Meta | ¿Cómo medir? |
|-----------|------|--------------|
| **Adopción** | >60% de usuarios invitados acceden en primer mes | Google Analytics / Logs |
| **Uso recurrente** | >30% de usuarios acceden semanalmente | Logs de autenticación |
| **Satisfacción** | >80% de usuarios lo encuentran útil | Encuesta post-capacitación |
| **Performance** | Dashboards cargan en <3 segundos | Monitoreo automático |
| **Exportaciones** | >50 reportes exportados en primer mes | Logs de exportación |
| **Disponibilidad** | >99% uptime (máximo 7 horas caídas/mes) | Azure Monitor |

---

## 8. PRÓXIMOS PASOS INMEDIATOS

### ✅ Acciones Post-Reunión (Esta Semana)

1. **Jefatura SEEMTP**:
   - [ ] Revisar y aprobar decisiones estratégicas (Secciones 3.1 a 3.4)
   - [ ] Firmar memo para Jefe TI (ver `_docs-planificacion/MEMO_JEFE_TI.md`)
   - [ ] Aprobar presupuesto (si es Azure) con Administración
   - [ ] Seleccionar 3-5 usuarios piloto

2. **Desarrollador (Andrés)**:
   - [ ] Enviar memo a TI MINEDUC (después de aprobación jefatura)
   - [ ] Preparar demo en vivo para usuarios piloto
   - [ ] Crear manual de usuario inicial
   - [ ] Configurar servidor Azure (si se aprueba)

3. **TI MINEDUC** (después de recibir memo):
   - [ ] Provisionar credenciales SQL Server (read-only)
   - [ ] Configurar acceso de red (firewall, VPN)
   - [ ] Aprobar integración con Microsoft 365 (si se aprueba)

---

## 📎 ANEXOS

### Documentos de Referencia

| Documento | Ubicación | Propósito |
|-----------|-----------|-----------|
| **Diagramas de Arquitectura** | `docs/DIAGRAMA_FLUJOS_ARQUITECTURA.md` | 9 diagramas visuales para presentaciones |
| **Arquitectura Técnica Detallada** | `docs/ARQUITECTURA_DETALLADA.md` | Especificaciones técnicas completas |
| **Manual de Actualización Automática** | `docs/ACTUALIZACION_AUTOMATICA.md` | Cómo funciona el sistema de cache semanal |
| **Memo para Jefe TI** | `_docs-planificacion/MEMO_JEFE_TI.md` | Solicitud formal de accesos |
| **Definiciones para Producción** | `_docs-planificacion/DEFINICIONES_PARA_PRODUCCION.md` | Opciones detalladas de cada decisión |

### Diagramas Disponibles para Presentación

**Archivos listos para usar** (agregar a PowerPoint/Keynote):
- `docs/Arquitectura_Vision_General.svg` - **RECOMENDADO** (calidad infinita, 53KB)
- `docs/Arquitectura_Vision_General_HQ.png` - Alta resolución (345KB)

---

## 📧 Contacto

**Desarrollador del Proyecto**  
Andrés Lazcano  
📧 Email: [tu-email]  
📱 Teléfono: [tu-teléfono]

**Repositorio GitHub**  
🔗 https://github.com/andreslazcano-bit/Visualizador-EMTP-Dash---Prototipo-Python

---

## ✅ CHECKLIST DE DECISIONES

Usar en la reunión para marcar decisiones tomadas:

### Decisiones Estratégicas
- [ ] **Modelo de acceso**: Público / Con perfiles / Híbrido → **Decisión**: __________
- [ ] **Autenticación**: AD / Microsoft 365 / Credenciales propias → **Decisión**: __________
- [ ] **Alcance funcionalidades**: Solo viz / +Reportería / Plataforma completa → **Decisión**: __________
- [ ] **Actualización datos**: Tiempo real / Diaria / Semanal / Mensual → **Decisión**: __________

### Definiciones Técnicas
- [ ] **Hosting**: On-premise / Azure / AWS / Heroku → **Decisión**: __________
- [ ] **Presupuesto aprobado**: Sí / No / Pendiente → **Decisión**: __________
- [ ] **Notificaciones**: Sí / No / Solo errores → **Decisión**: __________

### Coordinaciones
- [ ] **Reunión con TI programada**: Fecha: __________
- [ ] **Usuarios piloto seleccionados**: Nombres: __________
- [ ] **Fecha tentativa de lanzamiento**: __________

---

**Última actualización**: 17 de noviembre de 2025  
**Versión**: 1.0
