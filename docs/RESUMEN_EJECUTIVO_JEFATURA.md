# VISUALIZADOR EMTP - RESUMEN EJECUTIVO PARA JEFATURA

**Documento**: Definiciones estratégicas para producción  
**Fecha**: Noviembre 2025  
**Área**: Coordinación Nacional EMTP

---

## 🎯 OBJETIVO

Definir **3 decisiones estratégicas** para llevar el Visualizador EMTP de prototipo a producción.

---

## ⚡ DECISIONES REQUERIDAS

### **1️⃣ ¿QUIÉNES TENDRÁN ACCESO?**

| Opción | Descripción | Pros | Contras |
|--------|-------------|------|---------|
| **A. Público** | Cualquiera con el enlace | ✅ Máxima transparencia<br>✅ Sin gestión de usuarios | ❌ Sin control<br>❌ Sin auditoría |
| **B. Con Perfiles** ⭐ | Login con roles (Usuario/Analista/Admin) | ✅ Control granular<br>✅ Auditoría completa<br>✅ Protección de datos sensibles | ❌ Requiere gestión de usuarios |
| **C. Híbrido** | Público para datos generales + Login para sensibles | ✅ Balance transparencia/control | ❌ Mayor complejidad |

**🔹 Decisión**: [ A ] [ B ] [ C ]

**Si B o C → Definir:**
- ¿Quién crea usuarios?: [ SEEMTP ] [ TI ] [ Autoregistro ]
- ¿Cómo se autentican?: [ Credenciales propias ] [ Active Directory ] [ Office 365 ]
- ¿Auditoría?: [ Completa ] [ Básica ] [ No ]

---

### **2️⃣ ¿QUÉ TIPO DE PLATAFORMA?**

| Opción | Características | Esfuerzo | Recomendado para |
|--------|-----------------|----------|------------------|
| **A. Solo Visualización** | Dashboards interactivos, filtros, mapas | Actual | Análisis exploratorio |
| **B. + Reportería Básica** | Lo anterior + exportar Excel/PDF | +2-3 sem | Informes bajo demanda |
| **C. + Reportería Programada** ⭐ | Lo anterior + reportes automáticos por email | +4-6 sem | Gestión proactiva |

**Ejemplos Opción C:**
- Cada lunes: Reporte semanal a coordinadores regionales
- Cada mes: Consolidado nacional a jefatura
- Alertas: Notificación si matrícula cae >10%

**🔹 Decisión**: [ A ] [ B ] [ C ]

**Si B o C → Definir:**
- Formatos: [ Excel ] [ CSV ] [ PDF ] [ PowerPoint ]
- ¿Auditoría de reportes?: [ Sí ] [ No ]

**Si C → Definir:**
- Reportes automáticos: [ Semanal regional ] [ Mensual nacional ] [ Alertas ] [ Otros: ______ ]
- Destinatarios: [ Coordinadores regionales ] [ Jefatura ] [ Directores ] [ Otros: ______ ]

---

### **3️⃣ ¿DE DÓNDE VIENEN LOS DATOS?**

**Actualmente**: Datos simulados en CSV (178,700 registros)  
**Para producción**: Conexión a fuentes reales

| Fuente | Tipo | Responsable | Datos |
|--------|------|-------------|-------|
| **Bases de datos TI** | SQL Server/PostgreSQL | Requiere coord. con TI | SIGE (matrícula)<br>Titulados<br>Sistema Financiero |
| **SharePoint SEEMTP** | Excel/CSV | Área EMTP | Planillas regionales<br>Seguimiento proyectos |
| **APIs Externas** | Servicios web | TI + EMTP | DEMRE, Chile Atiende |

**🔹 Fuentes a conectar:**
- [ ] SIGE (matrícula) - Requiere TI
- [ ] Sistema de Titulados - Requiere TI
- [ ] Sistema Financiero (convenios/rendiciones) - Requiere TI
- [ ] SharePoint SEEMTP (planillas regionales)
- [ ] Otras: _______________________

**Complementarias:**
- ¿Quién coordina con TI?: [ Jefatura ] [ Coord. Proyecto ] [ Otro: ______ ]
- Frecuencia actualización: [ Diario ] [ Semanal ] [ Mensual ]
- ¿Mantener histórico?: [ Sí, todo ] [ Solo 2 años ] [ Solo 1 año ]

---

## 📅 RUTA CRÍTICA

```
┌────────────────────────────┐
│ HOY: Definiciones          │ → 1-2 semanas
├────────────────────────────┤
│ Coordinación con TI        │ → 2-3 semanas (paralelo)
├────────────────────────────┤
│ Desarrollo e integración   │ → 4-8 semanas (según alcance)
├────────────────────────────┤
│ Pruebas y capacitación     │ → 2-3 semanas
├────────────────────────────┤
│ PRODUCCIÓN                 │
└────────────────────────────┘

⏱️ TIEMPO TOTAL: 3-4 meses
```

---

## ✅ ACCIONES INMEDIATAS

### Esta semana:
1. **Jefatura SEEMTP**: Revisar y decidir sobre las 3 opciones
2. **Coordinador**: Agendar reunión con Jefe TI MINEDUC
3. **Área EMTP**: Listar carpetas SharePoint relevantes

### Próximas 2 semanas:
4. **Reunión formal con TI**: Presentar proyecto y solicitar accesos
5. **Inventario de datos**: Identificar bases disponibles
6. **Plan de trabajo**: Cronograma detallado según decisiones

---

## 📊 ESCENARIOS ESTIMADOS

| Escenario | Decisiones | Tiempo | Esfuerzo |
|-----------|------------|--------|----------|
| **Básico** | Público + Solo visual + SharePoint | 2 meses | Bajo |
| **Medio** ⭐ | Perfiles + Reportería básica + SharePoint + BD TI | 3 meses | Medio |
| **Completo** | Perfiles + AD + Reportería auto + BD TI + APIs | 4 meses | Alto |

**Recomendación**: Escenario **Medio** (balance funcionalidad/tiempo)

---

## 📎 DOCUMENTOS COMPLEMENTARIOS

1. **Documento completo**: `docs/DEFINICIONES_PARA_PRODUCCION.md` (versión extendida con todos los detalles)
2. **README técnico**: `README.md` (estado actual del sistema)
3. **Prototipo funcional**: http://localhost:8051 (para demostración)

---

## 🎯 CHECKLIST DE DECISIONES

- [ ] **ACCESO**: Modelo seleccionado y método de autenticación
- [ ] **PLATAFORMA**: Tipo de funcionalidades (visual/reportería)
- [ ] **DATOS**: Fuentes identificadas y responsables asignados
- [ ] **COORDINACIÓN TI**: Reunión agendada
- [ ] **CRONOGRAMA**: Plan de trabajo aprobado

---

**Preparado por**: Área Técnica EMTP  
**Revisión**: Pendiente  
**Aprobación**: Pendiente

*Visualizador EMTP v2.0 | Noviembre 2025*
