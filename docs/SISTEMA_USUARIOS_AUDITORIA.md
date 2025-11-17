# 🔐 Sistema de Gestión de Usuarios y Auditoría - Resumen de Implementación

## ✅ Lo que ya está creado

### 1. **Sistema de Auditoría** (`src/utils/audit.py`)
- ✅ Clase `AuditLogger` con logging a archivo JSONL
- ✅ Métodos para registrar: login, logout, view_dashboard, export_data, user_management
- ✅ Filtrado de logs por fecha, usuario, acción, estado
- ✅ Estadísticas de uso (total acciones, usuarios activos, top users, top actions)
- ✅ Instancia global: `audit_logger`

### 2. **Gestión de Usuarios** (`src/utils/user_management.py`)
- ✅ Clase `UserManager` con base de datos SQLite
- ✅ Tabla `users` con campos: username, password_hash, profile, full_name, email, is_active, timestamps
- ✅ CRUD completo: create_user, get_user, get_all_users, update_user, deactivate_user, activate_user, delete_user
- ✅ Autenticación: authenticate_user con bcrypt
- ✅ Usuario admin por defecto (admin/admin123)
- ✅ Instancia global: `user_manager`

### 3. **Layout de Gestión de Usuarios** (`src/layouts/user_management.py`)
- ✅ Formulario modal para crear/editar usuarios
- ✅ Tabla interactiva con DataTable
- ✅ Botones de acción (editar, activar, desactivar)
- ✅ Tarjetas de resumen por perfil
- ✅ Función: `create_user_management_layout()`

### 4. **Layout de Auditoría** (`src/layouts/audit.py`)
- ✅ Filtros: período, usuario, acción, estado
- ✅ Tarjetas de estadísticas
- ✅ 4 gráficos: timeline, usuarios activos, distribución acciones, dashboards visitados
- ✅ Tabla detallada de logs (últimos 100)
- ✅ Función: `create_audit_layout()`

---

## 🔧 Pasos para Completar la Integración

### PASO 1: Crear Callbacks de Gestión de Usuarios

Crear archivo: `src/callbacks/user_management_callbacks.py`

```python
"""
Callbacks para gestión de usuarios
"""

from dash import Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

from src.utils.user_management import user_manager
from src.utils.audit import audit_logger
from src.layouts.user_management import create_users_table, create_user_summary_cards


def register_user_management_callbacks(app):
    """Registra callbacks de gestión de usuarios"""
    
    # Cargar datos iniciales
    @app.callback(
        [Output('users-table-container', 'children'),
         Output('user-summary-cards', 'children'),
         Output('audit-user-filter', 'options')],
        Input('url', 'pathname')
    )
    def load_users_data(pathname):
        if '/gestion-usuarios' not in str(pathname):
            return no_update, no_update, no_update
        
        # Obtener usuarios
        users = user_manager.get_all_users(include_inactive=True)
        users_df = pd.DataFrame(users)
        
        # Tabla
        table = create_users_table(users_df)
        
        # Tarjetas de resumen
        counts = user_manager.get_user_count_by_profile()
        cards = create_user_summary_cards(counts)
        
        # Opciones de filtro de auditoría
        user_options = [{'label': u['username'], 'value': u['username']} for u in users]
        
        return table, cards, user_options
    
    # Abrir modal para crear usuario
    @app.callback(
        [Output('modal-user-form', 'is_open'),
         Output('modal-user-title', 'children'),
         Output('user-form-mode', 'data'),
         Output('input-username', 'value'),
         Output('input-fullname', 'value'),
         Output('input-email', 'value'),
         Output('select-profile', 'value'),
         Output('input-password', 'value')],
        [Input('btn-new-user', 'n_clicks'),
         Input('btn-edit-user', 'n_clicks'),
         Input('btn-cancel-user', 'n_clicks'),
         Input('btn-save-user', 'n_clicks')],
        [State('users-datatable', 'selected_rows'),
         State('users-datatable', 'data'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def toggle_user_modal(n_new, n_edit, n_cancel, n_save, selected_rows, table_data, session):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Cerrar modal
        if button_id in ['btn-cancel-user', 'btn-save-user']:
            return False, '', 'create', '', '', '', 'usuario', ''
        
        # Crear nuevo usuario
        if button_id == 'btn-new-user':
            return True, 'Crear Nuevo Usuario', 'create', '', '', '', 'usuario', ''
        
        # Editar usuario
        if button_id == 'btn-edit-user' and selected_rows and table_data:
            selected_user = table_data[selected_rows[0]]
            username = selected_user['Usuario']
            user_data = user_manager.get_user(username)
            
            return (
                True,
                f'Editar Usuario: {username}',
                'edit',
                username,
                user_data['full_name'],
                user_data['email'] or '',
                user_data['profile'],
                ''
            )
        
        return no_update
    
    # Guardar usuario (crear o editar)
    @app.callback(
        Output('user-management-alert', 'children'),
        Input('btn-save-user', 'n_clicks'),
        [State('user-form-mode', 'data'),
         State('input-username', 'value'),
         State('input-fullname', 'value'),
         State('input-email', 'value'),
         State('select-profile', 'value'),
         State('input-password', 'value'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def save_user(n_clicks, mode, username, fullname, email, profile, password, session):
        if not n_clicks:
            return no_update
        
        admin_username = session.get('user_info', {}).get('username', 'unknown')
        
        # Crear usuario
        if mode == 'create':
            if not username or not fullname or not password:
                return dbc.Alert("❌ Username, nombre completo y contraseña son obligatorios", color="danger")
            
            if len(password) < 6:
                return dbc.Alert("❌ La contraseña debe tener al menos 6 caracteres", color="danger")
            
            result = user_manager.create_user(
                username=username,
                password=password,
                profile=profile,
                full_name=fullname,
                email=email,
                created_by=admin_username
            )
            
            if result['success']:
                audit_logger.log_user_management(admin_username, 'created', username, {'profile': profile})
                return dbc.Alert(f"✅ {result['message']}", color="success", duration=4000)
            else:
                return dbc.Alert(f"❌ {result['error']}", color="danger")
        
        # Editar usuario
        elif mode == 'edit':
            update_data = {
                'username': username,
                'full_name': fullname,
                'email': email,
                'profile': profile
            }
            
            if password:
                if len(password) < 6:
                    return dbc.Alert("❌ La contraseña debe tener al menos 6 caracteres", color="danger")
                update_data['password'] = password
            
            result = user_manager.update_user(**update_data)
            
            if result['success']:
                audit_logger.log_user_management(admin_username, 'updated', username, {'profile': profile})
                return dbc.Alert(f"✅ {result['message']}", color="success", duration=4000)
            else:
                return dbc.Alert(f"❌ {result['error']}", color="danger")
        
        return no_update
    
    # Activar/Desactivar botones según selección
    @app.callback(
        [Output('btn-edit-user', 'disabled'),
         Output('btn-deactivate-user', 'disabled'),
         Output('btn-activate-user', 'disabled')],
        Input('users-datatable', 'selected_rows'),
        State('users-datatable', 'data'),
        prevent_initial_call=True
    )
    def toggle_action_buttons(selected_rows, table_data):
        if not selected_rows or not table_data:
            return True, True, True
        
        selected_user = table_data[selected_rows[0]]
        is_active = '✅' in selected_user['Estado']
        
        return False, not is_active, is_active
    
    # Desactivar usuario
    @app.callback(
        Output('user-management-alert', 'children', allow_duplicate=True),
        Input('btn-deactivate-user', 'n_clicks'),
        [State('users-datatable', 'selected_rows'),
         State('users-datatable', 'data'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def deactivate_user(n_clicks, selected_rows, table_data, session):
        if not n_clicks or not selected_rows or not table_data:
            return no_update
        
        username = table_data[selected_rows[0]]['Usuario']
        admin_username = session.get('user_info', {}).get('username', 'unknown')
        
        result = user_manager.deactivate_user(username)
        
        if result['success']:
            audit_logger.log_user_management(admin_username, 'deactivated', username)
            return dbc.Alert(f"✅ {result['message']}", color="success", duration=4000)
        else:
            return dbc.Alert(f"❌ {result['error']}", color="danger")
    
    # Activar usuario
    @app.callback(
        Output('user-management-alert', 'children', allow_duplicate=True),
        Input('btn-activate-user', 'n_clicks'),
        [State('users-datatable', 'selected_rows'),
         State('users-datatable', 'data'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def activate_user(n_clicks, selected_rows, table_data, session):
        if not n_clicks or not selected_rows or not table_data:
            return no_update
        
        username = table_data[selected_rows[0]]['Usuario']
        admin_username = session.get('user_info', {}).get('username', 'unknown')
        
        result = user_manager.activate_user(username)
        
        if result['success']:
            audit_logger.log_user_management(admin_username, 'activated', username)
            return dbc.Alert(f"✅ {result['message']}", color="success", duration=4000)
        else:
            return dbc.Alert(f"❌ {result['error']}", color="danger")
```

### PASO 2: Crear Callbacks de Auditoría

Crear archivo: `src/callbacks/audit_callbacks.py`

```python
"""
Callbacks para auditoría
"""

from dash import Input, Output, State, no_update
from datetime import datetime, timedelta
import pandas as pd

from src.utils.audit import audit_logger
from src.layouts.audit import (
    create_audit_stats_cards,
    create_audit_logs_table,
    create_timeline_chart,
    create_users_chart,
    create_actions_chart,
    create_dashboards_chart
)


def register_audit_callbacks(app):
    """Registra callbacks de auditoría"""
    
    @app.callback(
        [Output('audit-stats-cards', 'children'),
         Output('audit-logs-table', 'children'),
         Output('audit-timeline-chart', 'figure'),
         Output('audit-users-chart', 'figure'),
         Output('audit-actions-chart', 'figure'),
         Output('audit-dashboards-chart', 'figure')],
        [Input('btn-refresh-audit', 'n_clicks'),
         Input('audit-date-range', 'value'),
         Input('audit-user-filter', 'value'),
         Input('audit-action-filter', 'value'),
         Input('audit-status-filter', 'value')],
        prevent_initial_call=False
    )
    def update_audit_dashboard(n_clicks, days, user_filter, action_filter, status_filter):
        # Calcular fechas
        start_date = datetime.now() - timedelta(days=days)
        
        # Preparar filtros
        filters = {'start_date': start_date}
        
        if user_filter:
            filters['username'] = user_filter
        
        if action_filter and action_filter != 'all':
            if action_filter == 'user_':
                # Filtrar acciones que empiezan con user_
                logs_df = audit_logger.get_audit_logs(**filters)
                logs_df = logs_df[logs_df['action'].str.startswith('user_')]
            else:
                filters['action'] = action_filter
                logs_df = audit_logger.get_audit_logs(**filters)
        else:
            logs_df = audit_logger.get_audit_logs(**filters)
        
        if status_filter and status_filter != 'all':
            filters['status'] = status_filter
            logs_df = audit_logger.get_audit_logs(**filters)
        
        # Obtener estadísticas
        stats = audit_logger.get_statistics(days=days)
        
        # Crear componentes
        stats_cards = create_audit_stats_cards(stats)
        logs_table = create_audit_logs_table(logs_df)
        timeline_chart = create_timeline_chart(logs_df)
        users_chart = create_users_chart(stats)
        actions_chart = create_actions_chart(stats)
        dashboards_chart = create_dashboards_chart(logs_df)
        
        return stats_cards, logs_table, timeline_chart, users_chart, actions_chart, dashboards_chart
```

### PASO 3: Actualizar Sistema de Autenticación

Modificar `src/utils/auth.py` para usar `user_manager`:

```python
# En la clase AuthManager, reemplazar método authenticate_user:

@staticmethod
def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Autentica un usuario usando user_manager
    
    Args:
        username: Nombre de usuario
        password: Contraseña
    
    Returns:
        Dict con info del usuario o None si falla
    """
    from src.utils.user_management import user_manager
    from src.utils.audit import audit_logger
    
    result = user_manager.authenticate_user(username, password)
    
    if result:
        audit_logger.log_login(username, success=True)
        logger.info(f"✅ Usuario autenticado: {username} ({result['profile']})")
        return result
    else:
        audit_logger.log_login(username, success=False)
        logger.warning(f"❌ Autenticación fallida: {username}")
        return None
```

### PASO 4: Actualizar Sidebar para Incluir Nuevas Secciones

Modificar `src/layouts/sidebar_layout_clean.py`:

```python
# En la función create_new_main_layout, agregar después de "Docentes":

# Solo para admin
if 'proyectos' not in hidden_sections:
    # ... código existente de proyectos ...
    
    # AGREGAR ESTAS SECCIONES:
    dbc.NavLink([
        html.I(className="fas fa-users-cog me-2"),
        "Gestión de Usuarios"
    ], href="/gestion-usuarios", id="link-gestion-usuarios", className="sidebar-link"),
    
    dbc.NavLink([
        html.I(className="fas fa-clipboard-list me-2"),
        "Auditoría"
    ], href="/auditoria", id="link-auditoria", className="sidebar-link"),
```

### PASO 5: Registrar Nuevos Callbacks en app.py

Modificar `app.py` para registrar los nuevos callbacks:

```python
# Importar nuevos módulos
from src.callbacks.user_management_callbacks import register_user_management_callbacks
from src.callbacks.audit_callbacks import register_audit_callbacks

# Registrar callbacks (después de los existentes)
register_user_management_callbacks(app)
register_audit_callbacks(app)
```

### PASO 6: Agregar Rutas en Callbacks del Sidebar

Modificar el callback de navegación en `src/callbacks/sidebar_callbacks.py`:

```python
# Agregar estos cases en el callback de navegación:

elif active_page == '/gestion-usuarios':
    from src.layouts.user_management import create_user_management_layout
    content = create_user_management_layout()

elif active_page == '/auditoria':
    from src.layouts.audit import create_audit_layout
    content = create_audit_layout()
```

### PASO 7: Registrar Acciones de Vista en Callbacks

En cada callback que carga un dashboard, agregar logging:

```python
from src.utils.audit import audit_logger

# En cada callback de dashboard:
@app.callback(...)
def update_dashboard(..., session):
    username = session.get('user_info', {}).get('username', 'unknown')
    audit_logger.log_view_dashboard(username, 'nombre_dashboard')
    # ... resto del código
```

---

## 📋 Checklist de Implementación

### Archivos Creados ✅
- [x] `src/utils/audit.py` - Sistema de auditoría
- [x] `src/utils/user_management.py` - Gestión de usuarios
- [x] `src/layouts/user_management.py` - UI de gestión de usuarios
- [x] `src/layouts/audit.py` - UI de auditoría

### Archivos por Crear 🔧
- [ ] `src/callbacks/user_management_callbacks.py` - Callbacks de gestión de usuarios
- [ ] `src/callbacks/audit_callbacks.py` - Callbacks de auditoría

### Archivos por Modificar 📝
- [ ] `src/utils/auth.py` - Usar user_manager para autenticación
- [ ] `src/layouts/sidebar_layout_clean.py` - Agregar links de nuevas secciones
- [ ] `src/callbacks/sidebar_callbacks.py` - Agregar rutas de navegación
- [ ] `app.py` - Registrar nuevos callbacks
- [ ] Callbacks de dashboards - Agregar logging de vistas

---

## 🧪 Cómo Probar

1. **Ejecutar la app**:
   ```bash
   python app.py
   ```

2. **Login como admin**:
   - Usuario: `admin`
   - Contraseña: `admin123`

3. **Probar Gestión de Usuarios**:
   - Ir a "Gestión de Usuarios" en el menú
   - Crear un nuevo usuario
   - Editar usuario existente
   - Desactivar/Activar usuario

4. **Probar Auditoría**:
   - Ir a "Auditoría" en el menú
   - Ver logs de acciones
   - Filtrar por usuario, fecha, acción
   - Ver gráficos de uso

5. **Verificar Logs**:
   - Archivo de auditoría: `logs/audit.jsonl`
   - Base de datos: `data/users.db`

---

## 🎯 Funcionalidades Implementadas

### Sistema de Auditoría
✅ Registro de login/logout  
✅ Registro de vistas de dashboards  
✅ Registro de exportaciones  
✅ Registro de gestión de usuarios  
✅ Filtrado avanzado de logs  
✅ Estadísticas de uso  
✅ Gráficos de actividad  

### Gestión de Usuarios
✅ Crear usuarios (admin, analista, usuario)  
✅ Editar información de usuarios  
✅ Cambiar contraseñas  
✅ Activar/Desactivar usuarios  
✅ Eliminar usuarios (permanente)  
✅ Base de datos SQLite persistente  
✅ Contraseñas con bcrypt (12 rounds)  

### Seguridad
✅ Solo admin puede gestionar usuarios  
✅ Solo admin puede ver auditoría  
✅ Contraseñas hasheadas  
✅ Registro de todas las acciones  
✅ No se puede desactivar admin principal  

---

## 📚 Estructura de Datos

### Base de Datos de Usuarios (SQLite)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    profile TEXT NOT NULL,  -- usuario, analista, admin
    full_name TEXT NOT NULL,
    email TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_login TEXT,
    created_by TEXT
)
```

### Archivo de Auditoría (JSONL)

**Ubicación**: `logs/audit.jsonl`

Cada línea es un evento JSON independiente:

```json
{
  "timestamp": "2025-11-17T14:30:00",
  "username": "admin",
  "action": "login",
  "status": "success",
  "details": {},
  "ip_address": "192.168.1.10",
  "user_agent": "Mozilla/5.0..."
}
```

---

## 📊 Sistema de Auditoría Completo (Actualización Nov 2025)

### ✅ **Qué se registra automáticamente:**

#### 1. **Autenticación**
```json
{
  "action": "login",
  "status": "success" | "failed",
  "username": "usuario",
  "timestamp": "2025-11-17T12:30:00"
}
```

#### 2. **Navegación por Dashboards**
```json
{
  "action": "view_dashboard",
  "username": "analista1",
  "details": {
    "dashboard": "matricula",
    "subtab": "evolucion"
  },
  "timestamp": "2025-11-17T12:35:00"
}
```

**Dashboards rastreados:**
- ✅ Inicio
- ✅ Matrícula (evolucion, demografia, retencion, comparacion)
- ✅ Egresados (transicion, empleabilidad)
- ✅ Titulación (tasas, tiempo)
- ✅ Establecimientos (geografia, infraestructura)
- ✅ Docentes (perfil, capacitacion)
- ✅ Mapas (regional, comunal)
- ✅ Gestión de Usuarios
- ✅ Auditoría

#### 3. **Exportación de Datos**
```json
{
  "action": "export_data",
  "username": "usuario",
  "details": {
    "export_type": "csv" | "excel" | "pdf",
    "dashboard": "matricula",
    "subtab": "evolucion",
    "section": "matricula-evolucion"
  },
  "timestamp": "2025-11-17T12:40:00"
}
```

**Formatos de exportación rastreados:**
- ✅ CSV
- ✅ Excel (.xlsx)
- ✅ PDF (en desarrollo)

**Secciones con exportación:**
- Matrícula: evolucion, demografia, retencion, comparacion
- Egresados: transicion, empleabilidad
- Titulación: tasas, tiempo
- Establecimientos: geografia, infraestructura
- Docentes: perfil, capacitacion

#### 4. **Gestión de Usuarios** (Solo Admin)
```json
{
  "action": "user_create" | "user_update" | "user_deactivate",
  "username": "admin",
  "details": {
    "target_user": "nuevo_usuario",
    "profile": "analista",
    ...
  },
  "timestamp": "2025-11-17T12:45:00"
}
```

### 📂 **Ubicación de Logs**

```
logs/
├── audit.jsonl          ← Auditoría completa (JSON Lines)
├── app.log             ← Logs generales de la aplicación
└── app_backup_*.log    ← Backups automáticos (rotación 10 MB)
```

### � **Cómo consultar la auditoría**

#### **Opción 1: Dashboard de Auditoría (Recomendada)**

1. Login como Admin
2. Ir a "Auditoría" en el menú
3. Filtrar por:
   - Período (últimas 24h, 7 días, 30 días)
   - Usuario específico
   - Tipo de acción
   - Estado (éxito, error, denegado)

**Visualizaciones disponibles:**
- 📈 Timeline de actividad
- 👥 Usuarios más activos
- 📊 Distribución de acciones
- 🗺️ Dashboards más visitados
- 📋 Tabla detallada con todos los registros

#### **Opción 2: Terminal (para TI)**

```bash
# Ver últimos 50 registros
tail -50 logs/audit.jsonl

# Buscar exportaciones
grep "export_data" logs/audit.jsonl

# Buscar por usuario específico
grep "\"username\": \"analista1\"" logs/audit.jsonl | tail -20

# Ver solo logins fallidos
grep "\"action\": \"login\"" logs/audit.jsonl | grep "\"status\": \"failed\""

# Formato legible (requiere jq)
cat logs/audit.jsonl | jq .

# Últimas 10 exportaciones
grep "export_data" logs/audit.jsonl | tail -10 | jq .
```

#### **Opción 3: Python (para análisis avanzado)**

```python
from src.utils.audit import audit_logger
import pandas as pd

# Obtener todos los logs del último mes
df = audit_logger.get_audit_logs(days=30)

# Exportaciones de un usuario específico
exports = df[
    (df['action'] == 'export_data') & 
    (df['username'] == 'analista1')
]
print(exports)

# Estadísticas generales
stats = audit_logger.get_audit_stats(days=7)
print(f"Total acciones: {stats['total_actions']}")
print(f"Usuarios únicos: {stats['unique_users']}")
print(f"Exportaciones: {stats['exports']}")
```

### 📊 **Ejemplos de Consultas Comunes**

**¿Quién exportó datos esta semana?**
```bash
grep "export_data" logs/audit.jsonl | \
  jq -r '.username' | \
  sort | uniq -c | \
  sort -nr
```

**¿Cuántos intentos de login fallidos?**
```bash
grep "login" logs/audit.jsonl | \
  grep "failed" | wc -l
```

**¿Qué dashboards son más visitados?**
```bash
grep "view_dashboard" logs/audit.jsonl | \
  jq -r '.details.dashboard' | \
  sort | uniq -c | \
  sort -nr
```

### 🔐 **Seguridad y Retención**

- **Formato**: JSONL (una línea = un evento)
- **Tamaño**: Sin límite (monitorear crecimiento)
- **Rotación**: Manual o con logrotate
- **Retención recomendada**: 1 año mínimo
- **Backup**: Incluido en backup general del sistema
- **Permisos**: Solo lectura para TI, Admin puede ver dashboard

### ⚡ **Performance**

- **Overhead**: Mínimo (~1-2ms por evento)
- **Escritura**: Asíncrona (no bloquea UI)
- **Búsqueda**: O(n) en archivo, usar filtros en dashboard
- **Recomendación**: Si supera 100k eventos, considerar BD separada

---

## �🚀 Próximos Pasos (Opcionales)

1. ✅ **Sistema de Auditoría Completo** (IMPLEMENTADO)
2. ✅ **Registro de Exportaciones** (IMPLEMENTADO)
3. ✅ **Registro de Vistas de Dashboards** (IMPLEMENTADO)
4. **Exportación de Logs**: Botón para descargar logs en Excel
5. **Alertas**: Email cuando hay logins fallidos repetidos
6. **Dashboard de Admin**: Vista resumen con KPIs del sistema
7. **Integración AD**: Autenticación con Active Directory
8. **API REST**: Endpoints para gestión de usuarios desde otras apps
9. **Roles Personalizados**: Crear perfiles custom con permisos específicos

---

**Última actualización**: 17 de noviembre de 2025  
**Implementado**: Sistema completo de auditoría con registro de vistas y exportaciones  
**Autor**: Andrés Lazcano
