# 📊 Configuración Power BI RFT 2025-2026

## Descripción

Esta pestaña permite incrustar un dashboard de Power BI externo dentro del Visualizador EMTP, específicamente diseñada para el informe de **Red Futuro Técnico (RFT) 2025-2026**.

**Características:**
- ✅ Fácilmente configurable
- ✅ Gestionado de forma independiente
- ✅ Fácilmente removible sin afectar el resto del sistema
- ✅ Actualizado por personal externo

---

## 🚀 Instrucciones de Configuración

### Paso 1: Publicar el Informe en Power BI Service

1. Abre tu informe `.pbix` en **Power BI Desktop**
2. Ve a **Archivo** > **Publicar** > **Publicar en Power BI**
3. Selecciona tu área de trabajo (workspace)
4. Espera a que se complete la publicación

### Paso 2: Obtener la URL de Inserción

1. Ve a [https://app.powerbi.com](https://app.powerbi.com)
2. Navega a tu área de trabajo y abre el informe RFT 2025-2026
3. Haz clic en **Archivo** > **Insertar informe** > **Sitio web o portal**
4. Aparecerá una ventana con dos opciones:
   - **Opción 1 (Recomendado)**: Obtén el enlace de inserción público
   - **Opción 2**: Obtén el código iframe completo

### Paso 3: Copiar la URL

**Si elegiste Opción 1:**
```
https://app.powerbi.com/view?r=XXXXXXXXXX
```

**Si elegiste Opción 2 (extrae solo la URL del src):**
```html
<iframe 
  src="https://app.powerbi.com/view?r=XXXXXXXXXX" 
  ...
</iframe>
```
Solo necesitas la parte: `https://app.powerbi.com/view?r=XXXXXXXXXX`

### Paso 4: Configurar en el Código

1. Abre el archivo: `src/callbacks/sidebar_callbacks.py`
2. Busca la línea ~**1290** (o busca por texto: `POWER_BI_URL_AQUI`)
3. Reemplaza `POWER_BI_URL_AQUI` con tu URL real:

**ANTES:**
```python
html.Iframe(
    src="POWER_BI_URL_AQUI",  # ⚠️ REEMPLAZAR con URL real
    style={...}
)
```

**DESPUÉS:**
```python
html.Iframe(
    src="https://app.powerbi.com/view?r=TU_CODIGO_AQUI",
    style={...}
)
```

### Paso 5: Ocultar el Mensaje de Placeholder

En la misma sección, busca esta línea (~línea 1320):
```python
style={"display": "block"})  # Cambiar a "none" cuando se configure la URL
```

Cámbiala a:
```python
style={"display": "none"})  # Oculta el placeholder cuando ya está configurado
```

### Paso 6: Reiniciar la Aplicación

```bash
# Detener la app si está corriendo
lsof -ti:8051 | xargs kill -9 2>/dev/null

# Reiniciar
source venv/bin/activate
python3 app_v2.py
```

---

## 🔐 Configuración de Permisos (Power BI)

### Para Acceso Público (Recomendado para visualización interna)

1. En Power BI Service, ve a la configuración del informe
2. **Configuración** > **Configuración del informe**
3. Activa **"Permitir que los usuarios inserten este informe"**
4. Activa **"Permitir compartir"** (si es necesario)

### Para Acceso Privado (Requiere autenticación)

Si necesitas que los usuarios se autentiquen en Power BI:
1. El iframe mostrará un login de Microsoft
2. Los usuarios necesitarán credenciales institucionales
3. Configura Row-Level Security (RLS) en Power BI si es necesario

---

## 🎨 Personalización del Iframe

### Ajustar Tamaño

En `src/callbacks/sidebar_callbacks.py`, modifica el style del iframe:

```python
style={
    'width': '100%',        # Ancho completo
    'height': '800px',      # ⬅️ Ajusta esta altura según necesites
    'border': 'none',
    'border-radius': '8px'
}
```

Alturas sugeridas:
- **800px**: Ideal para dashboards de una página
- **1200px**: Para dashboards con múltiples visualizaciones
- **600px**: Para vistas compactas

### Agregar Filtros por Defecto

Puedes agregar parámetros a la URL para filtros predefinidos:

```python
src="https://app.powerbi.com/view?r=XXXXX&filterPane=hidden&navContentPane=hidden"
```

Parámetros útiles:
- `filterPane=hidden`: Oculta el panel de filtros
- `navContentPane=hidden`: Oculta la navegación de páginas
- `$filter=Tabla/Campo eq 'Valor'`: Aplica filtros predefinidos

---

## 🗑️ Cómo Remover la Pestaña

Si necesitas eliminar completamente esta funcionalidad:

### Método 1: Comentar el Código

1. Abre `src/callbacks/sidebar_callbacks.py`
2. Busca la línea que dice: `# Tab: Power BI RFT 2025-2026` (~línea 1280)
3. Selecciona todo el bloque hasta (y sin incluir): 
   ```python
   ], id="tabs-fortalecimiento", active_tab="tab-equipamiento-regular", className="mb-3"),
   ```
4. Comenta todas las líneas seleccionadas con `#` al inicio

### Método 2: Eliminar el Código (Permanente)

1. Abre `src/callbacks/sidebar_callbacks.py`
2. Busca y **ELIMINA** el bloque completo desde:
   ```python
   # Tab: Power BI RFT 2025-2026
   dbc.Tab([
   ```
   
   Hasta (sin incluir):
   ```python
   ], id="tabs-fortalecimiento", active_tab="tab-equipamiento-regular", className="mb-3"),
   ```

3. **IMPORTANTE**: Asegúrate de mantener la coma final del tab anterior (`tab-slep`)

4. Guarda y reinicia la aplicación

---

## ❓ Solución de Problemas

### El iframe no se muestra

**Problema**: Pantalla en blanco o error de carga

**Soluciones:**
1. Verifica que la URL de Power BI sea correcta y pública
2. Verifica que el informe esté publicado en Power BI Service
3. Revisa la consola del navegador (F12) para errores de CORS
4. Asegúrate de que "Permitir insertar" esté activado en Power BI

### Requiere autenticación constantemente

**Problema**: Siempre pide login de Microsoft

**Soluciones:**
1. Configura el informe como público en Power BI Service
2. O asegúrate de que los usuarios tengan licencias Power BI Pro/Premium
3. Verifica que la URL sea de tipo `/view?r=` (no `/reportEmbed`)

### El dashboard se ve muy pequeño

**Problema**: Dashboard difícil de leer

**Soluciones:**
1. Aumenta la altura del iframe en el código (ej: `'height': '1200px'`)
2. Ajusta el diseño del informe en Power BI Desktop para ser más compacto
3. Usa modo de visualización responsive en Power BI

### Errores de CORS

**Problema**: "Blocked by CORS policy"

**Soluciones:**
1. Usa la URL de inserción pública de Power BI (`/view?r=`)
2. NO uses URLs locales o de desarrollo
3. Configura correctamente los permisos en Power BI Service

---

## 📝 Ejemplo Completo

Aquí hay un ejemplo funcional completo:

```python
# Tab: Power BI RFT 2025-2026
dbc.Tab([
    html.Div([
        html.H4([
            html.I(className="fas fa-chart-line me-2", style={"color": "var(--primary-color)"}),
            "Dashboard RFT 2025-2026"
        ], className="mt-3 mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                html.Iframe(
                    src="https://app.powerbi.com/view?r=eyJrIjoiMTIzNDU2Nzg5IiwidCI6Ijk4NzY1NDMyMSJ9",
                    style={
                        'width': '100%',
                        'height': '1000px',
                        'border': 'none',
                        'border-radius': '8px'
                    }
                )
            ], className="p-0")
        ], className="border-accent-custom shadow-sm")
    ], className="p-3")
], label="📊 Power BI RFT 2025-2026", tab_id="tab-powerbi-rft",
   label_style={"color": "#5A6E79"}, 
   active_label_style={"color": "#34536A", "font-weight": "bold"})
```

---

## 🔄 Actualización del Dashboard

Para actualizar el contenido del dashboard:

1. **Actualiza en Power BI Desktop**: Haz cambios en tu archivo `.pbix`
2. **Publica nuevamente**: Archivo > Publicar en Power BI
3. **No es necesario cambiar código**: El iframe mostrará automáticamente la versión actualizada

**¡Eso es todo!** El dashboard se actualiza automáticamente sin tocar la aplicación Dash.

---

## 📞 Soporte

**Desarrollador Visualizador EMTP**  
Andrés Lazcano  
ext.andres.lazcano@mineduc.cl  

**Última actualización**: 17 de noviembre de 2025
