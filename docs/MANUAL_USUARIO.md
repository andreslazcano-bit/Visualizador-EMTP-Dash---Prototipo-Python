# 📱 MANUAL DE USUARIO - Visualizador EMTP

**Versión:** 2.0  
**Fecha:** Noviembre 2025  
**Audiencia:** Secretaría EMTP, Analistas, Usuarios Finales

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Navegación Básica](#navegación-básica)
4. [Uso de Dashboards](#uso-de-dashboards)
5. [Aplicar Filtros](#aplicar-filtros)
6. [Exportar Datos](#exportar-datos)
7. [Funciones de Administrador](#funciones-de-administrador)
8. [Preguntas Frecuentes](#preguntas-frecuentes)
9. [Soporte](#soporte)

---

## 📘 Introducción

### ¿Qué es el Visualizador EMTP?

El **Visualizador EMTP** es una herramienta web que permite consultar y analizar datos del sistema de **Educación Media Técnico-Profesional de Chile** mediante:

- 📊 **Dashboards interactivos:** Gráficos y tablas dinámicas
- 🗺️ **Mapas geográficos:** Distribución por región y comuna
- 📑 **Exportación de reportes:** PDF, Excel, CSV
- 👥 **Gestión de usuarios:** Control de accesos (solo administradores)
- 📋 **Auditoría:** Registro de acciones (solo administradores)

---

### ¿Quién Puede Usar el Sistema?

| Perfil | Acceso | Funciones |
|--------|--------|-----------|
| **Usuario** | Público (sin login) | Ver dashboards básicos, aplicar filtros |
| **Analista** | Requiere login | Acceso a dashboards avanzados y exportación |
| **Administrador** | Requiere login | Todas las funciones + gestión de usuarios + auditoría |

---

## 🔐 Acceso al Sistema

### Paso 1: Abrir el Navegador Web

**URL del sistema:**
```
http://[servidor-emtp]:8051
```

💡 **Recomendación:** Usar Google Chrome, Firefox o Microsoft Edge (últimas versiones)

---

### Paso 2: Seleccionar Modo de Acceso

Al cargar la página, aparecerán **dos opciones:**

#### 🟢 Modo Usuario (Sin Login)
- Click en **"Acceso como Usuario"**
- Acceso inmediato sin credenciales
- Dashboards limitados (Matrícula, Egresados, Titulación, Docentes, Establecimientos)

#### 🔵 Modo Administrador (Con Login)
- Requiere credenciales
- Acceso completo a todas las funcionalidades
- Incluye: Gestión de Usuarios, Auditoría, Monitoreo de Proyectos

---

### Paso 3: Login Administrador

**Si es Administrador o Analista:**

1. Click en **"Acceso Administrador"**
2. Ingresar:
   - **Usuario:** (asignado por TI)
   - **Contraseña:** (asignada por TI)
3. Click **"Ingresar"**

⚠️ **Primer acceso:** Si es su primer login con usuario `admin`, la contraseña por defecto es `admin123`. **DEBE CAMBIARLA INMEDIATAMENTE.**

---

## 🧭 Navegación Básica

### Pantalla Principal

Después de acceder, verá:

1. **Barra Superior:**
   - Logo EMTP
   - Nombre del usuario (si está logueado)
   - Botón de tema claro/oscuro 🌙
   - Botón de cerrar sesión (si está logueado)

2. **Menú Lateral (Sidebar):**
   - Inicio 🏠
   - Matrícula 📚
   - Egresados 🎓
   - Titulación 📜
   - Establecimientos 🏫
   - Docentes 👨‍🏫
   - Mapas 🗺️
   - **Solo Admin:**
     - Monitoreo y Seguimiento de Proyectos 📊
     - Gestión de Usuarios 👥
     - Auditoría 📋

3. **Área de Contenido:**
   - Dashboards, gráficos y tablas

---

### Cambiar de Sección

**Para navegar entre módulos:**

1. Click en el módulo deseado en el menú lateral
   - Ejemplo: Click en **"Matrícula"** 📚

2. Se despliegan sub-opciones:
   - Evolución Temporal
   - Demografía Estudiantil
   - Retención y Deserción
   - Comparación Regional

3. Click en la sub-opción deseada
   - Ejemplo: Click en **"Evolución Temporal"**

4. El dashboard se carga en el área de contenido

---

### Cambiar Tema Visual

**Tema Claro vs Oscuro:**

- Click en el botón 🌙 (esquina superior derecha)
- Alterna entre tema claro (fondo blanco) y oscuro (fondo negro)
- **Recomendación:** Tema oscuro reduce fatiga visual en sesiones largas

---

## 📊 Uso de Dashboards

### Tipos de Visualizaciones

#### 1. **Tarjetas de KPI (Indicadores Clave)**

Muestran métricas importantes en formato de tarjeta:

```
┌─────────────────────────┐
│  📚 Matrícula Total     │
│     156,234             │
│     ▲ +2.3% vs año ant.│
└─────────────────────────┘
```

**Cómo leer:**
- **Número grande:** Valor actual del indicador
- **Flecha ▲/▼:** Tendencia (arriba = aumentó, abajo = disminuyó)
- **Porcentaje:** Cambio respecto al período anterior

---

#### 2. **Gráficos de Líneas**

Muestran evolución temporal:

**Cómo interactuar:**
- **Pasar mouse sobre puntos:** Ver valor exacto
- **Zoom:** Arrastrar área del gráfico
- **Restablecer zoom:** Doble click en el gráfico
- **Leyenda:** Click en etiqueta para ocultar/mostrar serie

---

#### 3. **Gráficos de Barras**

Comparan valores entre categorías:

**Cómo interactuar:**
- **Pasar mouse:** Ver valor exacto
- **Click en barra:** Filtrar por esa categoría (en algunas vistas)
- **Leyenda:** Click para ocultar/mostrar categoría

---

#### 4. **Gráficos de Torta (Pie)**

Muestran distribución porcentual:

**Cómo leer:**
- Cada sección = porcentaje del total
- Pasar mouse para ver valor absoluto y porcentaje

---

#### 5. **Mapas Geográficos**

Muestran distribución territorial:

**Cómo interactuar:**
- **Zoom:** Scroll del mouse o botones +/-
- **Pan:** Arrastrar el mapa
- **Información:** Click en región/comuna para ver detalles
- **Leyenda:** Escala de colores (valores bajos = claro, altos = oscuro)

---

#### 6. **Tablas de Datos**

Datos tabulares con opciones de ordenamiento:

**Cómo usar:**
- **Ordenar:** Click en encabezado de columna
- **Buscar:** Usar caja de búsqueda (si disponible)
- **Paginación:** Navegar con botones anterior/siguiente
- **Exportar:** Usar botones de exportación

---

## 🔍 Aplicar Filtros

### Panel de Filtros

La mayoría de dashboards tienen un **Panel de Filtros** en la parte superior:

```
┌─────────────────────────────────────────────┐
│  Filtros                                    │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │ Año     │ │ Región  │ │ Género  │      │
│  └─────────┘ └─────────┘ └─────────┘      │
│  [Aplicar Filtros]  [Limpiar Filtros]     │
└─────────────────────────────────────────────┘
```

---

### Paso a Paso: Aplicar Filtros

**Ejemplo: Ver matrícula 2024 solo en Región Metropolitana**

1. **Seleccionar Año:**
   - Click en dropdown "Año"
   - Seleccionar **"2024"**

2. **Seleccionar Región:**
   - Click en dropdown "Región"
   - Seleccionar **"Metropolitana de Santiago"**

3. **Aplicar:**
   - Click en botón **"Aplicar Filtros"**

4. **Resultado:**
   - Todos los gráficos y tablas se actualizan con los datos filtrados

---

### Limpiar Filtros

**Para volver a ver todos los datos:**

- Click en botón **"Limpiar Filtros"**
- Todos los filtros se resetean a "Todos"

---

### Filtros Combinados

**Puede combinar múltiples filtros:**

- **Año:** 2023
- **Región:** Valparaíso
- **Género:** Femenino
- **Dependencia:** Municipal

Resultado: Solo estudiantes mujeres de establecimientos municipales de Valparaíso en 2023

---

## 📥 Exportar Datos

### Tipos de Exportación

La mayoría de secciones permiten **exportar datos:**

| Formato | Uso Recomendado | Botón |
|---------|-----------------|-------|
| **PDF** | Reportes impresos, presentaciones | 📄 Descargar PDF |
| **Excel** | Análisis en Excel, tablas dinámicas | 📊 Descargar Excel |
| **CSV** | Importar a otros sistemas, análisis estadístico | 📋 Descargar CSV |

---

### Paso a Paso: Exportar a Excel

1. **Aplicar filtros deseados** (si corresponde)
   - Ejemplo: Año 2024, Región Metropolitana

2. **Scroll hacia abajo** hasta el final del dashboard

3. **Buscar sección "Exportar Datos":**
   ```
   ┌─────────────────────────────┐
   │  📥 Exportar Datos          │
   │  [📄 PDF] [📊 Excel] [📋 CSV] │
   └─────────────────────────────┘
   ```

4. **Click en "Descargar Excel"**

5. **Esperar descarga:**
   - Aparece spinner de carga
   - Archivo se descarga automáticamente

6. **Abrir archivo:**
   - Ubicación: Carpeta de Descargas
   - Nombre: `matricula_20241117.xlsx`

---

### Qué Incluye la Exportación

**Los archivos exportados contienen:**

- ✅ Datos **filtrados** (si aplicó filtros)
- ✅ Todas las tablas visibles en el dashboard
- ✅ Metadatos (fecha de generación, usuario que exportó)
- ❌ NO incluyen gráficos (solo datos)

---

## 🔧 Funciones de Administrador

**Las siguientes secciones solo están disponibles para usuarios con perfil "Admin"**

---

### 1. Gestión de Usuarios

**Ubicación:** Menú lateral → **"Gestión de Usuarios"** 👥

#### Ver Usuarios Existentes

**Pantalla principal:**

```
┌─────────────────────────────────────────────┐
│  Resumen                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │Total: 15 │ │Admin: 3  │ │Analista:7│   │
│  └──────────┘ └──────────┘ └──────────┘   │
│                                             │
│  [+ Crear Nuevo Usuario]                   │
│                                             │
│  Tabla de Usuarios:                        │
│  Usuario │ Nombre  │ Perfil │ Estado      │
│  ─────────────────────────────────────────│
│  admin   │ Admin   │ Admin  │ Activo      │
│  juan.p  │ Juan P. │ Analista│ Activo     │
│  ...                                        │
└─────────────────────────────────────────────┘
```

---

#### Crear Nuevo Usuario

**Pasos:**

1. **Click en "Crear Nuevo Usuario"**

2. **Completar formulario:**
   ```
   ┌─────────────────────────────┐
   │  Nombre de Usuario*         │
   │  [juan.perez]               │
   │                             │
   │  Nombre Completo*           │
   │  [Juan Pérez González]      │
   │                             │
   │  Email                      │
   │  [juan.perez@mineduc.cl]    │
   │                             │
   │  Perfil*                    │
   │  [▼ Analista]               │
   │                             │
   │  Contraseña* (min 8 car.)   │
   │  [••••••••]                 │
   │                             │
   │  [Cancelar]  [Guardar]      │
   └─────────────────────────────┘
   ```

3. **Campos obligatorios (*):**
   - **Nombre de Usuario:** Solo letras, números, punto, guión bajo (sin espacios)
   - **Nombre Completo:** Nombre real del usuario
   - **Email:** Email corporativo (opcional pero recomendado)
   - **Perfil:** Usuario / Analista / Admin
   - **Contraseña:** Mínimo 8 caracteres, combinación de letras y números

4. **Click en "Guardar"**

5. **Confirmar:**
   - Aparece mensaje: "✅ Usuario creado exitosamente"
   - La tabla se actualiza con el nuevo usuario

6. **Informar credenciales al usuario:**
   - ⚠️ **IMPORTANTE:** Anotar las credenciales en lugar seguro
   - Enviar por canal seguro (no por email sin cifrar)
   - Ejemplo de mensaje:
     ```
     Estimado/a Juan,
     
     Se ha creado tu usuario en el Visualizador EMTP:
     - Usuario: juan.perez
     - Contraseña temporal: [contraseña]
     
     Por favor cambiar contraseña en primer acceso.
     
     Acceso: http://[servidor]:8051
     ```

---

#### Editar Usuario Existente

**Pasos:**

1. **Seleccionar usuario en la tabla:**
   - Click en la fila del usuario

2. **Click en botón "Editar"**

3. **Modificar campos:**
   - **Usuario:** NO se puede modificar
   - **Nombre Completo:** Se puede modificar
   - **Email:** Se puede modificar
   - **Perfil:** Se puede cambiar (Usuario / Analista / Admin)
   - **Contraseña:** Dejar vacío para mantener contraseña actual, o ingresar nueva

4. **Click en "Guardar"**

5. **Confirmar:**
   - Mensaje: "✅ Usuario actualizado exitosamente"

---

#### Desactivar Usuario

**Cuándo usar:** Cuando un usuario deja la organización o temporalmente no debe tener acceso

**Pasos:**

1. **Seleccionar usuario en la tabla**
2. **Click en botón "Desactivar"**
3. **Confirmar acción**
4. **Resultado:**
   - Estado cambia a "Inactivo"
   - Usuario no puede hacer login
   - Datos del usuario se mantienen en el sistema

---

#### Reactivar Usuario

**Pasos:**

1. **Seleccionar usuario inactivo en la tabla**
2. **Click en botón "Activar"**
3. **Confirmar:**
   - Estado cambia a "Activo"
   - Usuario puede volver a hacer login

---

### 2. Auditoría

**Ubicación:** Menú lateral → **"Auditoría"** 📋

**¿Para qué sirve?**
- Ver quién accedió al sistema y cuándo
- Revisar qué acciones se realizaron (login, exportaciones, gestión de usuarios)
- Detectar intentos de acceso no autorizados
- Cumplir con normativas de trazabilidad

---

#### Panel de Auditoría

**Pantalla principal:**

```
┌─────────────────────────────────────────────┐
│  Filtros                                    │
│  [Últimos 7 días ▼] [Usuario ▼] [Acción ▼] │
│  [🔄 Actualizar]                            │
│                                             │
│  Estadísticas:                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
│  │1,234 │ │ 45   │ │ 123  │ │ 89   │      │
│  │Accion│ │Usuar │ │Login │ │Export│      │
│  └──────┘ └──────┘ └──────┘ └──────┘      │
│                                             │
│  Gráficos:                                  │
│  - Línea de tiempo de acciones              │
│  - Top 10 usuarios más activos              │
│  - Distribución por tipo de acción          │
│                                             │
│  Logs Detallados (últimos 100):            │
│  Fecha     │Usuario│Acción    │Estado      │
│  ─────────────────────────────────────────│
│  2024-11-17│admin  │login     │Exitoso     │
│  2024-11-17│juan.p │export_csv│Exitoso     │
│  ...                                        │
└─────────────────────────────────────────────┘
```

---

#### Filtrar Logs de Auditoría

**Por Período:**

1. Click en dropdown "Período"
2. Seleccionar:
   - **Últimas 24 horas**
   - **Últimos 7 días** (por defecto)
   - **Últimos 30 días**
   - **Últimos 90 días**
   - **Todos**

**Por Usuario:**

1. Click en dropdown "Usuario"
2. Seleccionar usuario específico o "Todos"

**Por Tipo de Acción:**

1. Click en dropdown "Acción"
2. Seleccionar:
   - **Todos**
   - **Login/Logout**
   - **Exportación de datos**
   - **Gestión de usuarios**
   - **Vista de dashboards**

**Por Estado:**

1. Click en dropdown "Estado"
2. Seleccionar:
   - **Todos**
   - **Exitoso**
   - **Fallido**

**Aplicar:**

- Click en botón **"🔄 Actualizar"**
- Todos los gráficos y tabla se actualizan

---

#### Casos de Uso Comunes

**1. Ver quién accedió ayer:**
- Período: "Últimas 24 horas"
- Acción: "Login/Logout"
- Estado: "Todos"

**2. Detectar intentos de acceso fallidos:**
- Período: "Últimos 7 días"
- Acción: "Login/Logout"
- Estado: "Fallido"
- **Si hay más de 5 del mismo usuario:** Posible ataque, reportar a TI

**3. Ver qué exportó un usuario específico:**
- Período: "Últimos 30 días"
- Usuario: "juan.perez"
- Acción: "Exportación de datos"

---

## ❓ Preguntas Frecuentes

### ¿Puedo cambiar mi contraseña?

**Sí, contactar al administrador del sistema:**
1. Enviar email a: **ti@mineduc.cl**
2. Solicitar cambio de contraseña
3. Administrador la cambiará desde "Gestión de Usuarios"

**En futuras versiones:** Opción de auto-cambio de contraseña.

---

### ¿Por qué no veo la sección "Gestión de Usuarios"?

**Solo usuarios con perfil "Admin" pueden ver esta sección.**

Si necesita acceso, contactar a:
- **Secretaría EMTP:** secretaria.emtp@mineduc.cl
- **TI:** ti@mineduc.cl

---

### Los datos no coinciden con mi fuente. ¿Por qué?

**Posibles causas:**

1. **Filtros aplicados:** Verifique que no haya filtros activos. Click en "Limpiar Filtros"
2. **Datos desactualizados:** El sistema se actualiza semanalmente (lunes a las 6 AM). Última actualización se muestra en la esquina inferior del dashboard
3. **Fuente diferente:** Este sistema usa datos de [fuente oficial]. Si usa otra fuente, puede haber diferencias

---

### ¿Cómo reporto un error o bug?

**Contactar a soporte:**

**Email:** ti@mineduc.cl  
**Asunto:** [Visualizador EMTP] Error en [sección]

**Incluir:**
- Descripción del problema
- Pasos para reproducir
- Captura de pantalla (si aplica)
- Navegador usado (Chrome, Firefox, etc.)

---

### ¿Puedo usar el sistema desde mi celular?

**Sí, pero con limitaciones:**

- La interfaz está optimizada para **computadores de escritorio**
- En celulares/tablets puede verse reducida
- **Recomendación:** Usar en modo horizontal (landscape)

Para mejor experiencia, usar:
- **Pantalla:** 13" o superior
- **Resolución:** 1366x768 o superior
- **Navegador:** Última versión de Chrome, Firefox o Edge

---

### ¿Cada cuánto se actualizan los datos?

**Actualización semanal automática:**
- **Día:** Lunes
- **Hora:** 6:00 AM (hora Chile)
- **Duración:** Aproximadamente 30 minutos

**Durante la actualización:**
- Sistema permanece disponible
- Puede haber lentitud temporal

---

### ¿Puedo compartir mis credenciales con un compañero?

**❌ NO. Está estrictamente prohibido.**

**Razones:**
- Seguridad de la información
- Trazabilidad (auditoría registra acciones por usuario)
- Incumple políticas de seguridad del MINEDUC

**Si necesita acceso para otra persona:**
- Solicitar creación de usuario nuevo a administrador
- Contactar: **ti@mineduc.cl**

---

## 📞 Soporte

### Soporte Técnico (Errores del Sistema)

**TI - Ministerio de Educación**  
📧 **Email:** ti@mineduc.cl  
📞 **Teléfono:** +56 2 XXXX XXXX  
🕒 **Horario:** Lunes a Viernes, 9:00 - 18:00

**Tiempo de Respuesta:**
- Crítico (sistema caído): 15 minutos
- Alta (funcionalidad importante): 2 horas
- Media: 1 día laboral
- Baja: 3 días laborales

---

### Soporte Funcional (Uso del Sistema)

**Secretaría EMTP**  
📧 **Email:** secretaria.emtp@mineduc.cl  
🕒 **Horario:** Lunes a Viernes, 9:00 - 17:00

**Consultas:**
- Cómo usar funcionalidades
- Interpretación de datos
- Solicitud de acceso
- Capacitación

---

### Desarrollador (Emergencias Críticas)

**Andrés Lazcano** (Desarrollador Original)  
📧 **Email:** andres.lazcano@mineduc.cl  
📞 **Teléfono:** +56 9 XXXX XXXX

**Solo contactar para:**
- Sistema completamente caído sin respuesta de TI
- Corrupción de datos
- Vulnerabilidad de seguridad detectada

---

## 📚 Documentos Adicionales

- **Manual de Despliegue (para TI):** `docs/MANUAL_DESPLIEGUE.md`
- **Manual de Mantenimiento (para TI):** `docs/MANUAL_MANTENIMIENTO.md`
- **Guía Rápida:** `docs/GUIA_RAPIDA.md`

---

## 📝 Control de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | Noviembre 2025 | Versión inicial del manual |

---

**¡Gracias por usar el Visualizador EMTP!** 🎉

Si tiene sugerencias para mejorar esta herramienta, no dude en contactarnos.
