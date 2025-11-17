# VISUALIZADOR EMTP - PRESENTACIÓN PARA JEFATURA

> **Plantilla para presentación PowerPoint**  
> Convertir a PPT usando herramientas como Marp, Slidev, o manualmente

---

## DIAPOSITIVA 1: PORTADA

**VISUALIZADOR EMTP**  
Definiciones Estratégicas para Puesta en Producción

Coordinación Nacional EMTP  
Noviembre 2025

---

## DIAPOSITIVA 2: CONTEXTO

### ¿Dónde estamos?

**✅ LOGRADO:**
- Prototipo funcional completo
- 178,700 registros simulados
- 7 módulos de análisis
- Mapas interactivos (16 regiones, 345 comunas)
- Interfaz profesional y responsive

**⚠️ PARA PRODUCCIÓN:**
- Conectar datos reales
- Definir modelo de acceso
- Especificar funcionalidades finales

---

## DIAPOSITIVA 3: CAPACIDADES ACTUALES

### El Visualizador permite:

📊 **Análisis Interactivo**
- Matrícula, Titulación, Egresados
- Filtros dinámicos por región, comuna, especialidad
- Comparación entre períodos

🗺️ **Mapas Geográficos**
- Distribución territorial de matrícula
- Ubicación de establecimientos EMTP

📈 **Indicadores de Gestión**
- Proyectos activos y rendiciones
- Seguimiento de equipamiento
- Red Futuro Técnico (RFT)

---

## DIAPOSITIVA 4: DECISIÓN 1 - ACCESO

### ¿Quiénes podrán usar el sistema?

| Opción | Características | Recomendación |
|--------|-----------------|---------------|
| 🌍 **Público** | Acceso abierto sin login | Solo si todos los datos son públicos |
| 👥 **Con Perfiles** | 3 niveles: Usuario/Analista/Admin | ⭐ **RECOMENDADO** |
| 🔀 **Híbrido** | Público + Privado | Si hay datos mixtos |

**Si elegimos perfiles:**
- Usuario: Directores, Docentes → Solo visualización
- Analista: Coordinadores → Visualización + Reportes
- Admin: Jefatura, TI → Acceso total

---

## DIAPOSITIVA 5: DECISIÓN 2 - PLATAFORMA

### ¿Qué debe hacer el sistema?

**A. Solo Visualización** → Dashboard interactivo  
**B. + Reportería Básica** → + Exportar Excel/PDF  
**C. + Reportería Automática** → + Envío programado ⭐

### Ejemplo Opción C:
*"Cada lunes a las 8 AM, los 16 coordinadores regionales reciben por email un PDF con el resumen de su región: matrícula actualizada, nuevos titulados, proyectos en ejecución."*

**Beneficio:** Gestión proactiva vs. reactiva

---

## DIAPOSITIVA 6: DECISIÓN 3 - DATOS

### ¿De dónde vienen los datos?

```
┌─────────────────────────────────┐
│     VISUALIZADOR EMTP           │
└──────────┬──────────────────────┘
           │
    ┌──────┴──────┬──────────┐
    │             │          │
┌───▼────┐  ┌────▼───┐  ┌───▼────┐
│ SIGE   │  │Sistema │  │SharePo-│
│(TI)    │  │Financ. │  │int EMTP│
└────────┘  └────────┘  └────────┘
Matrícula   Convenios   Planillas
oficial     Rendiciones regionales
```

**Requiere coordinación con:**
- ✅ TI MINEDUC (bases de datos)
- ✅ Área EMTP (SharePoint)

---

## DIAPOSITIVA 7: RUTA CRÍTICA

### Cronograma estimado:

```
📋 Definiciones (HOY)        → 1-2 semanas
🤝 Coordinación TI          → 2-3 semanas
💻 Desarrollo               → 4-8 semanas
🧪 Pruebas y Capacitación   → 2-3 semanas
🚀 PRODUCCIÓN               → 

⏱️ TOTAL: 3-4 meses
```

**Factor crítico:** Tiempos de respuesta de TI

---

## DIAPOSITIVA 8: ESCENARIOS

### Comparación de opciones:

| Componente | Básico | Medio ⭐ | Completo |
|------------|--------|---------|----------|
| **Acceso** | Público | Perfiles | Perfiles + AD |
| **Funciones** | Visual | + Export | + Automático |
| **Datos** | SharePoint | SharePoint + BD | + APIs |
| **Tiempo** | 2 meses | 3 meses | 4 meses |

**Recomendación:** Escenario **Medio**  
(Balance funcionalidad/tiempo/costo)

---

## DIAPOSITIVA 9: BENEFICIOS ESPERADOS

### Con el Visualizador en producción:

✅ **Toma de decisiones informada**
- Datos actualizados y centralizados
- Visibilidad completa del sistema EMTP

✅ **Eficiencia operativa**
- Menos tiempo buscando datos
- Reportes automáticos (si se implementa)

✅ **Transparencia**
- Datos accesibles para todos los niveles
- Auditoría de accesos y reportes

✅ **Detección temprana**
- Alertas automáticas de problemas
- Seguimiento en tiempo real

---

## DIAPOSITIVA 10: RIESGOS Y MITIGACIÓN

### Riesgos identificados:

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Demoras de TI | Alto | Reunión temprana, seguimiento |
| Calidad de datos | Medio | Validación y estandarización |
| Adopción usuarios | Medio | Capacitación y soporte |
| Falta de recursos | Alto | Priorizar funcionalidades |

---

## DIAPOSITIVA 11: INVERSIÓN REQUERIDA

### Recursos necesarios:

**👨‍💻 Humanos:**
- Desarrollador: 3-4 meses (ya disponible)
- Coordinador SEEMTP: 20% tiempo (gestión)
- Soporte TI: A definir con TI MINEDUC

**💻 Técnicos:**
- Servidor productivo (coordinar con TI)
- Accesos a bases de datos (TI)
- Espacio SharePoint (ya disponible)

**💰 Presupuesto:**
- Desarrollo: Cubierto (recurso interno)
- Infraestructura: A coordinar con TI
- Capacitación: 1-2 sesiones (virtual)

---

## DIAPOSITIVA 12: PRÓXIMOS PASOS

### Acciones inmediatas (esta semana):

1. ✅ **Jefatura decide:**
   - Modelo de acceso
   - Tipo de plataforma
   - Prioridad de fuentes de datos

2. 📅 **Coordinador agenda:**
   - Reunión con Jefe TI MINEDUC
   - Presentación del proyecto

3. 📊 **Área EMTP prepara:**
   - Listado de carpetas SharePoint
   - Inventario de datos disponibles

---

## DIAPOSITIVA 13: PREGUNTAS CLAVE

### Para decidir hoy:

**ACCESO:**
❓ ¿Debe ser público o con control de usuarios?  
❓ ¿Necesitamos auditoría de quién consulta qué?

**PLATAFORMA:**
❓ ¿Solo visualización o también reportería automática?  
❓ ¿Quiénes recibirían reportes automáticos?

**DATOS:**
❓ ¿Qué bases de datos TI son prioritarias?  
❓ ¿Con qué frecuencia actualizamos datos?

---

## DIAPOSITIVA 14: DOCUMENTACIÓN

### Materiales disponibles:

📄 **Documento completo:**  
`docs/DEFINICIONES_PARA_PRODUCCION.md`
- 30+ páginas con todos los detalles
- Opciones, pros/contras, especificaciones

📄 **Resumen ejecutivo:**  
`docs/RESUMEN_EJECUTIVO_JEFATURA.md`
- 3 páginas con decisiones clave

💻 **Demo en vivo:**  
http://localhost:8051
- Prototipo funcional para mostrar

---

## DIAPOSITIVA 15: CIERRE

### Visualizador EMTP: De Prototipo a Producción

**Estamos listos técnicamente.**  
**Necesitamos definiciones estratégicas.**

**3 decisiones clave:**
1. ¿Quién accede? → Modelo de usuarios
2. ¿Qué hace? → Visualización + Reportería
3. ¿De dónde vienen datos? → TI + SharePoint

**Próximo hito:** Reunión con TI MINEDUC

---

## DIAPOSITIVA 16: CONTACTO

**Coordinación Nacional EMTP**  
Responsable Técnico: [Tu nombre]  
Email: [tu email]  
Teléfono: [tu teléfono]

**Repositorio GitHub:**  
github.com/andreslazcano-bit/Visualizador-EMTP-Dash

**Documentación:**  
`/docs` en el proyecto

---

**¿Preguntas?**

---

## NOTAS PARA EL PRESENTADOR

### Tips para la presentación:

1. **Diapositiva 1-3**: Contexto rápido (2-3 min)
2. **Diapositiva 4-6**: CORE - Las 3 decisiones (10-15 min)
3. **Diapositiva 7-8**: Tiempos y escenarios (5 min)
4. **Diapositiva 9-11**: Beneficios e inversión (5 min)
5. **Diapositiva 12-13**: Acciones y preguntas (5 min)
6. **Demo en vivo**: Si hay tiempo (5-10 min)

**Total recomendado:** 30-40 minutos + preguntas

### Materiales de apoyo:

- Tener el visualizador corriendo en http://localhost:8051
- Documento completo impreso para referencia
- Lista de bases de datos TI para discutir
- Contacto del Jefe TI para agendar reunión

### Posibles preguntas y respuestas:

**P: ¿Cuánto cuesta?**  
R: Desarrollo ya está cubierto (recurso interno). Solo requiere coordinación con TI para servidor e infraestructura.

**P: ¿Cuántos usuarios soporta?**  
R: Configuración actual: 50 simultáneos. Escalable a 200+ con infraestructura adecuada.

**P: ¿Qué pasa si TI demora?**  
R: Podemos empezar con SharePoint mientras se gestiona acceso a bases de datos TI.

**P: ¿Se puede integrar con otros sistemas?**  
R: Sí, la arquitectura es modular. Se pueden agregar conexiones a APIs externas.

**P: ¿Requiere capacitación?**  
R: Mínima. La interfaz es intuitiva. Se recomienda 1 sesión de 1 hora para coordinadores regionales.
