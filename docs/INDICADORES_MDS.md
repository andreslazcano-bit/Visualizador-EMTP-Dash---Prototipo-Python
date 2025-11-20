# Indicadores MDS - Ministerio de Desarrollo Social

**Fecha de Creación:** 20 de Noviembre 2025  
**Versión:** 1.### 2.1. Porcentaje de establecimientos de EMTP que han mejorado su equipamiento para especialidades por medio de Convenios con Mineduc, en los últimos 3 años

**Descripción:**
Mide el porcentaje acumulado de establecimientos de EMTP que han mejorado su equipamiento para especialidades técnicas mediante convenios con MINEDUC durante los últimos tres años.

**Fórmula de Cálculo:**
```
Indicador = (Número acumulado de establecimientos de EMTP que han mejorado su equipamiento para especialidades por medio de convenios con Mineduc desde el año t-3 / Número total de establecimientos de EMTP en el año t) × 100
```

**Componentes:**
- **Numerador**: Número acumulado de establecimientos de EMTP que han mejorado su equipamiento para especialidades por medio de convenios con Mineduc desde el año t-3
- **Denominador**: Número total de establecimientos de EMTP en el año t
- **Unidad**: Porcentaje (%)
- **Período**: Últimos 3 años (acumulado desde t-3 hasta t) Solo Administradores

> ⚠️ **IMPORTANTE**: Los datos mostrados actualmente son **SIMULADOS** con fines de demostración. No representan información real del sistema EMTP.

## Descripción General

Este módulo contiene los indicadores solicitados por el **Ministerio de Desarrollo Social (MDS)** para el seguimiento y evaluación del programa de Educación Media Técnico-Profesional (EMTP) de Chile.

Los indicadores se dividen en dos categorías principales:
1. **Indicadores de Propósito** (2 indicadores)
2. **Indicadores Complementarios** (3 indicadores)

---

## Ubicación en el Sistema

**Ruta de Navegación:**
- Iniciar sesión como **Admin**
- Hacer clic en **"Indicadores MDS"** en el menú lateral

**Visibilidad:**
- ✅ **Admin**: Acceso completo
- ❌ **Usuario**: No visible
- ❌ **Analista**: No visible (puede habilitarse según necesidad)

---

## 1. INDICADORES DE PROPÓSITO

### 1.1. Porcentaje de estudiantes egresados de EMTP que ingresa a educación superior

**Descripción:**
Mide el porcentaje de estudiantes egresados de EMTP que logra ingresar a instituciones de educación superior (universidades, institutos profesionales, centros de formación técnica) en el periodo siguiente a su egreso.

**Fórmula de Cálculo:**
```
Indicador = (Número de estudiantes egresados de la EMTP afectos a este programa en el periodo t-1 que ingresan a la Educación Superior en el periodo t / Número total de estudiantes egresados de la EMTP afectos a este programa en el periodo t-1) × 100
```

**Componentes:**
- **Numerador**: Número de estudiantes egresados de la EMTP afectos a este programa en el periodo t-1 que ingresan a la Educación Superior en el periodo t
- **Denominador**: Número total de estudiantes egresados de la EMTP afectos a este programa en el periodo t-1
- **Unidad**: Porcentaje (%)
- **Periodo**: Anual (t-1 para egreso, t para ingreso a ES)

**Fuentes de Datos:**
- MINEDUC: Registros de egresados EMTP
- SIES (Sistema de Información de Educación Superior): Registros de matrícula en ES

**Meta 2024:** 55%

**Visualizaciones Disponibles:**
1. **Evolución Temporal (2019-2024)**: Gráfico de línea mostrando tendencia histórica
2. **Distribución por Región**: Comparación regional del indicador
3. **Por Especialidad**: Desagregación según especialidad técnica

**KPIs Principales:**
- % Ingreso ES (2024)
- Variación vs año anterior
- Total de egresados
- Egresados que ingresaron a ES

---

### 1.2. Porcentaje de docentes de Formación Diferenciada Técnico Profesional que mejoran sus competencias de gestión curricular

**Descripción:**
Mide el porcentaje de docentes de Formación Diferenciada Técnico Profesional que aprueban exitosamente capacitaciones orientadas a mejorar sus competencias de gestión curricular, en el marco del programa EMTP.

**Fórmula de Cálculo:**
```
Indicador = (N° total de docentes que aprueban capacitaciones en el marco del programa, en cualquiera de sus componentes año t / N° total de docentes que participa de capacitaciones en el marco del programa, en cualquiera de sus componentes año t) × 100
```

**Componentes:**
- **Numerador**: N° total de docentes que aprueban capacitaciones en el marco del programa, en cualquiera de sus componentes año t
- **Denominador**: N° total de docentes que participa de capacitaciones en el marco del programa, en cualquiera de sus componentes año t
- **Unidad**: Porcentaje (%)
- **Periodo**: Anual

**Fuentes de Datos:**
- MINEDUC/CPEIP: Registros de capacitación docente
- Programa EMTP: Bases de datos de participantes y resultados

**Criterios de Mejora:**
Se considera "mejora" cuando el docente:
- Aprueba evaluación post-capacitación con puntaje ≥ 70%
- Implementa al menos 2 estrategias aprendidas en aula
- Recibe evaluación positiva de jefe UTP

**Fuentes de Datos:**
- CPEIP (Centro de Perfeccionamiento): Registros de capacitación docente
- Establecimientos EMTP: Evaluaciones de implementación

**Meta 2024:** 80%

**Visualizaciones Disponibles:**
1. **Evolución Anual (2020-2024)**: Tendencia de mejora en el tiempo
2. **Por Región**: Comparación regional del indicador

**KPIs Principales:**
- % Mejora (2024)
- Nº docentes capacitados
- Nº docentes que mejoraron
- Meta anual

---

## 2. INDICADORES COMPLEMENTARIOS

### 2.1. Mejora de Equipamiento

**Descripción:**
Mide el porcentaje de establecimientos de EMTP que han mejorado su equipamiento para especialidades por medio de Convenios con Mineduc, en los últimos 3 años (2022-2024).

**Fórmula de Cálculo:**
```
Indicador = (Nº EE con equipamiento mejorado / Total EE EMTP) × 100
```

**Componentes:**
- **Numerador**: Número de establecimientos que recibieron equipamiento mediante convenios MINEDUC
- **Denominador**: Total de establecimientos EMTP del país
- **Unidad**: Porcentaje (%)
- **Período**: Últimos 3 años (2022-2024)

**Criterios de "Mejora":**
Se considera que un establecimiento mejoró su equipamiento si recibió:
- Equipos tecnológicos (computadores, software, equipamiento audiovisual)
- Maquinaria industrial (según especialidad)
- Herramientas especializadas
- Renovación de laboratorios
- Mobiliario específico para talleres

**Fuentes de Datos:**
- MINEDUC: Registros de convenios y transferencias
- DAEM/Corporaciones: Inventarios de equipamiento

**Visualizaciones Disponibles:**
1. **Evolución Últimos 3 Años**: Cantidad anual y acumulado
2. **Por Tipo de Equipamiento**: Distribución según categoría
3. **Distribución Regional**: Cobertura por región

**KPIs Principales:**
- % EE mejorados
- Total EE EMTP
- Nº EE mejorados
- Período de medición

---

### 2.2. Porcentaje de SLEP cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional mejoran sus competencias para el acompañamiento en las especificidades de la EMTP

**Descripción:**
Mide el porcentaje de SLEP (Servicios Locales de Educación Pública) cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional (UAT-TP) concluyen exitosamente instancias de capacitación para el acompañamiento en las especificidades de la EMTP.

**Fórmula de Cálculo:**
```
Indicador = (Número SLEP cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional concluyen con éxito instancias de capacitación para el acompañamiento en las especificidades de la EMTP año t / Número total de SLEP en funcionamiento año t) × 100
```

**Componentes:**
- **Numerador**: Número SLEP cuyas Unidades de Apoyo Técnico Pedagógico Técnico Profesional concluyen con éxito instancias de capacitación para el acompañamiento en las especificidades de la EMTP año t
- **Denominador**: Número total de SLEP en funcionamiento año t
- **Unidad**: Porcentaje (%)
- **Periodo**: Anual

**Áreas de Competencia Evaluadas:**
1. Acompañamiento pedagógico especializado en EMTP
2. Gestión curricular técnico-profesional
3. Evaluación formativa en contexto técnico
4. Articulación con sector productivo
5. Seguimiento de trayectorias de egresados
6. Innovación pedagógica en EMTP

**Criterios de Mejora:**
Un SLEP se considera "mejorado" si su UAT-TP:
- Completa programa de formación especializada (≥ 80 horas)
- Implementa plan de acompañamiento a EE EMTP
- Obtiene evaluación positiva de establecimientos (≥ 4.0/5.0)

**Fuentes de Datos:**
- DEP (Dirección de Educación Pública): Evaluaciones UAT-TP
- SLEP: Planes de acompañamiento y reportes

**Contexto:**
Chile cuenta con 11 SLEP implementados, no todos tienen UAT-TP específica para EMTP.

**Visualizaciones Disponibles:**
1. **Progreso por SLEP**: Estado individual de cada SLEP
2. **Áreas de Competencia Mejoradas**: Desglose por área

**KPIs Principales:**
- % SLEP mejorados
- Total SLEP
- SLEP mejorados
- SLEP en programa

---

### 2.3. Porcentaje de establecimientos de EMTP que participa y desarrolla actividades en redes de trabajo colaborativo a nivel territorial a lo largo del año

**Descripción:**
Mide el porcentaje de establecimientos de EMTP que participa activamente y desarrolla actividades en redes de trabajo colaborativo a nivel territorial durante el año.

**Fórmula de Cálculo:**
```
Indicador = (Número de establecimientos de EMTP que participa y desarrolla actividades en redes de trabajo colaborativo a nivel territorial en el año t / Número total de establecimientos EMTP del país en el año t) × 100
```

**Componentes:**
- **Numerador**: Número de establecimientos de EMTP que participa y desarrolla actividades en redes de trabajo colaborativo a nivel territorial en el año t
- **Denominador**: Número total de establecimientos EMTP del país en el año t
- **Unidad**: Porcentaje (%)
- **Periodo**: Anual

**Tipos de Redes Consideradas:**
1. **Redes de Especialidad**: EE que comparten la misma especialidad
2. **Redes Territoriales**: EE de una misma comuna o región
3. **Redes de Innovación Pedagógica**: Intercambio de buenas prácticas
4. **Redes de Vinculación con Empresas**: Articulación con sector productivo
5. **Redes de Prácticas Profesionales**: Coordinación de prácticas

**Criterios de Participación Activa:**
Un EE se considera "participante activo" si:
- Asiste a al menos 70% de las reuniones anuales
- Desarrolla al menos 2 actividades colaborativas en el año
- Comparte experiencias o recursos con otros EE de la red

**Fuentes de Datos:**
- MINEDUC: Registros de redes formales
- SLEP/DAEM: Reportes de participación
- Coordinadores de redes: Actas de reuniones

**Visualizaciones Disponibles:**
1. **Participación por Región**: Comparación regional
2. **Tipos de Redes**: Distribución según tipo
3. **Frecuencia de Actividades**: Periodicidad de reuniones

**KPIs Principales:**
- % Participación
- Total EE EMTP
- EE en redes
- Nº redes activas

---

## Datos en el Sistema

### Estado Actual (Noviembre 2024)

**IMPORTANTE:** Los datos actualmente mostrados en el sistema son **SIMULADOS** con fines demostrativos.

Para poner en producción este módulo con datos reales, se requiere:

1. **Conexión a Fuentes de Datos:**
   - SIES (Sistema de Información de Educación Superior)
   - CPEIP (Centro de Perfeccionamiento)
   - DEP (Dirección de Educación Pública)
   - Registros MINEDUC de convenios y equipamiento

2. **Actualización de Datos:**
   - Frecuencia recomendada: Semestral
   - Responsable: Área de Estudios MINEDUC
   - Formato: CSV o conexión directa a base de datos

3. **Validación:**
   - Cruce de información con diferentes fuentes
   - Verificación con SLEP y establecimientos
   - Aprobación por MDS antes de publicación oficial

---

## Uso del Módulo

### Navegación

1. Iniciar sesión como **admin**
2. Hacer clic en **"Indicadores MDS"** en menú lateral
3. Seleccionar pestaña:
   - **📊 Indicadores de Propósito**
   - **📈 Indicadores Complementarios**

### Exportación de Datos

Cada indicador incluye opciones de exportación:
- **PNG**: Gráficos individuales
- **CSV**: Datos subyacentes
- **PDF**: Informe completo (requiere implementación futura)

### Interpretación

**Colores en Gráficos:**
- 🟢 Verde: Cumplimiento de meta o valor positivo
- 🔵 Azul: Valores neutros o informativos
- 🟠 Naranja: Advertencia, cerca de umbral
- 🔴 Rojo: Bajo desempeño o necesita atención

---

## Frecuencia de Actualización

| Indicador | Frecuencia Recomendada | Fuente Principal |
|-----------|----------------------|------------------|
| Ingreso a ES | Anual (marzo) | SIES |
| Competencias Docentes | Semestral | CPEIP |
| Mejora Equipamiento | Anual (diciembre) | MINEDUC |
| Competencias UAT-TP | Semestral | DEP |
| Redes Colaborativas | Anual (noviembre) | MINEDUC/SLEP |

---

## Configuración Técnica

### Archivos Relacionados

```
src/
├── layouts/
│   └── indicadores_mds.py          # Layout de indicadores
├── callbacks/
│   └── indicadores_mds_callbacks.py # Callbacks y datos
└── data/
    └── indicadores_mds/             # Datos (crear carpeta)
        ├── ingreso_es.csv
        ├── competencias_docentes.csv
        ├── equipamiento.csv
        ├── slep_uattp.csv
        └── redes_colaborativas.csv
```

### Permisos

Para habilitar acceso a otros perfiles, modificar:

**Archivo:** `src/callbacks/auth_callbacks.py`

```python
# Línea ~95
'hidden_sections': ['proyectos', 'gestion-usuarios', 'auditoria', 'indicadores-mds']
```

Remover `'indicadores-mds'` para el perfil que desee tener acceso.

---

## Mejoras Futuras

### Corto Plazo (1-3 meses)
- [ ] Conexión a fuentes de datos reales
- [ ] Exportación a PDF de informes completos
- [ ] Filtros por año y período
- [ ] Comparación entre períodos

### Mediano Plazo (3-6 meses)
- [ ] Dashboard ejecutivo con todos los indicadores
- [ ] Alertas automáticas si indicador bajo meta
- [ ] Proyecciones y tendencias con ML
- [ ] Integración con sistema MDS

### Largo Plazo (6-12 meses)
- [ ] API REST para consulta externa
- [ ] Actualización automática desde fuentes
- [ ] Reportes personalizables por usuario
- [ ] Módulo de análisis predictivo

---

## Contacto y Soporte

**Desarrollador:**  
Andrés Lazcano  
ext.andres.lazcano@mineduc.cl

**Equipo de Estudios MINEDUC:**  
Para actualización de datos y validación de indicadores

**Ministerio de Desarrollo Social:**  
Para consultas sobre definiciones y metodologías de indicadores

---

**Última Actualización:** 20 de Noviembre 2025  
**Versión del Documento:** 1.0
