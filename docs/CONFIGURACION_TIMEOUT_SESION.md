# Configuración de Timeout de Sesión

## Descripción General

El sistema implementa un mecanismo de timeout automático de sesión para mejorar la seguridad de la aplicación. Las sesiones expiran automáticamente después de un período de inactividad configurable.

## Características

### 1. **Timeout Automático por Inactividad**
- Las sesiones expiran automáticamente después de **30 minutos** de inactividad (configurable)
- El sistema verifica el estado de la sesión cada **60 segundos**
- Se considera "actividad" cualquier interacción del usuario:
  - Cambios de URL/navegación
  - Cambios de pestaña en el sidebar
  - Cualquier interacción con la interfaz

### 2. **Comportamiento Diferenciado por Perfil**

#### **Modo Usuario (sin contraseña)**
- Al expirar la sesión, se muestra un mensaje amigable
- El usuario es redirigido automáticamente a la pantalla de bienvenida
- Mensaje: "Tu sesión ha expirado por inactividad"
- Explicación sobre la política de timeout

#### **Modo Admin/Analista (con contraseña)**
- Al expirar la sesión, se solicita **re-autenticación**
- El usuario debe ingresar su contraseña nuevamente
- Si la contraseña es correcta, la sesión se renueva y continúa trabajando
- Si cancela o la contraseña es incorrecta, vuelve a la pantalla de bienvenida

### 3. **Seguridad Mejorada**
- Previene acceso no autorizado en equipos desatendidos
- Registro de eventos en auditoría:
  - `session_timeout`: Cuando una sesión expira
  - `reauth_success`: Re-autenticación exitosa
  - `reauth_failed`: Intento fallido de re-autenticación

## Configuración

### Variables de Entorno

Puedes configurar los tiempos de timeout editando el archivo `.env` o usando variables de entorno:

```bash
# Timeout de inactividad (minutos)
SESSION_TIMEOUT_MINUTES=30

# Tiempo de advertencia antes del timeout (minutos)
SESSION_WARNING_MINUTES=5

# Duración máxima de sesión (horas)
MAX_SESSION_DURATION_HOURS=8

# Intervalo de limpieza de sesiones expiradas (minutos)
SESSION_CLEANUP_INTERVAL_MINUTES=15
```

### Valores por Defecto

Si no se especifican, se usan los siguientes valores:

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `SESSION_TIMEOUT_MINUTES` | 30 | Tiempo de inactividad antes de expirar |
| `SESSION_WARNING_MINUTES` | 5 | Tiempo de advertencia (futuro) |
| `MAX_SESSION_DURATION_HOURS` | 8 | Duración máxima de sesión |
| `SESSION_CLEANUP_INTERVAL_MINUTES` | 15 | Frecuencia de limpieza |

### Configuración en Código

Las configuraciones se encuentran en `config/settings.py`:

```python
# Gestión de Sesiones
SESSION_TIMEOUT_MINUTES: int = int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))
SESSION_WARNING_MINUTES: int = int(os.getenv('SESSION_WARNING_MINUTES', 5))
MAX_SESSION_DURATION_HOURS: int = int(os.getenv('MAX_SESSION_DURATION_HOURS', 8))
SESSION_CLEANUP_INTERVAL_MINUTES: int = int(os.getenv('SESSION_CLEANUP_INTERVAL_MINUTES', 15))
```

## Arquitectura Técnica

### Componentes del Sistema

1. **SessionManager** (`src/utils/session.py`)
   - Gestiona el ciclo de vida de las sesiones
   - Valida timeouts
   - Actualiza actividad
   - Limpia sesiones expiradas

2. **Session Callbacks** (`src/callbacks/session_callbacks.py`)
   - `check_session_timeout()`: Verifica timeout cada minuto
   - `update_activity()`: Actualiza timestamp en cada interacción
   - `handle_reauth()`: Maneja re-autenticación de admin
   - `return_from_timeout()`: Vuelve a bienvenida

3. **Componentes UI** (en `app_v2.py`)
   - `session-check-interval`: Intervalo de verificación (60s)
   - `modal-session-timeout`: Modal para usuarios sin contraseña
   - `modal-reauth`: Modal de re-autenticación para admin

### Flujo de Funcionamiento

```
┌─────────────────┐
│ Usuario Activo  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Cada interacción:       │
│ - Actualiza timestamp   │
│ - last_activity = now() │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Cada 60 segundos:       │
│ - Verificar inactividad │
│ - Calcular tiempo       │
└────────┬────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌─────────┐
│Activo │ │Timeout? │
└───────┘ └────┬────┘
               │
          ┌────┴─────┐
          │          │
          ▼          ▼
    ┌──────────┐ ┌──────────┐
    │Usuario   │ │Admin/    │
    │          │ │Analista  │
    └────┬─────┘ └────┬─────┘
         │            │
         ▼            ▼
    ┌──────────┐ ┌──────────┐
    │Modal     │ │Modal     │
    │Timeout   │ │Re-auth   │
    └────┬─────┘ └────┬─────┘
         │            │
         ▼            ▼
    ┌──────────┐ ┌──────────┐
    │Volver    │ │Ingresar  │
    │Inicio    │ │Password  │
    └──────────┘ └────┬─────┘
                      │
                 ┌────┴────┐
                 │         │
                 ▼         ▼
            ┌────────┐ ┌────────┐
            │Correcta│ │Error   │
            │Renovar │ │Volver  │
            └────────┘ └────────┘
```

## Estructura de Datos de Sesión

### Almacenamiento en `session-store`

```python
{
    'authenticated': True,
    'last_activity': '2025-11-17T17:14:09.123456',  # ISO format
    'user_info': {
        'username': 'admin',
        'profile': 'admin',
        'full_name': 'Administrador',
        'hidden_sections': []
    }
}
```

### Campos Clave

- **`authenticated`**: Indica si hay sesión activa
- **`last_activity`**: Timestamp ISO de última actividad
- **`user_info`**: Información del usuario actual

## Registro de Auditoría

Todos los eventos de timeout y re-autenticación se registran en `logs/audit.jsonl`:

### Evento: Session Timeout
```json
{
  "timestamp": "2025-11-17T17:44:09.123456",
  "username": "admin",
  "event_type": "session_timeout",
  "details": {
    "profile": "admin",
    "inactive_minutes": 31.2
  }
}
```

### Evento: Re-autenticación Exitosa
```json
{
  "timestamp": "2025-11-17T17:45:09.123456",
  "username": "admin",
  "event_type": "reauth_success",
  "details": {
    "profile": "admin"
  }
}
```

### Evento: Re-autenticación Fallida
```json
{
  "timestamp": "2025-11-17T17:45:15.123456",
  "username": "admin",
  "event_type": "reauth_failed",
  "details": {
    "profile": "admin"
  }
}
```

## Consideraciones de Seguridad

### ✅ Implementado

- ✅ Timeout automático por inactividad
- ✅ Re-autenticación para usuarios con contraseña
- ✅ Registro de eventos en auditoría
- ✅ Limpieza de sesión al cerrar navegador (session storage)
- ✅ Validación de contraseña con bcrypt
- ✅ Timestamps en formato UTC

### ⚠️ Limitaciones Actuales

- Las sesiones se almacenan en el navegador (dcc.Store con `storage_type='session'`)
- No hay advertencia previa antes del timeout (implementación futura)
- No hay persistencia de sesiones en servidor

### 🔮 Mejoras Futuras

1. **Advertencia antes del timeout**
   - Mostrar alerta 5 minutos antes de expirar
   - Botón para extender sesión

2. **Gestión de sesiones en servidor**
   - Almacenar sesiones activas en Redis o base de datos
   - Permitir cerrar sesiones remotamente

3. **Dashboard de sesiones activas**
   - Visualizar sesiones activas en modo admin
   - Capacidad de cerrar sesiones de otros usuarios

## Pruebas

### Probar Timeout de Usuario

1. Acceder como "Usuario"
2. Esperar 30 minutos sin interactuar
3. Verificar que aparece modal de timeout
4. Confirmar redirección a pantalla de bienvenida

### Probar Re-autenticación Admin

1. Acceder como "Admin"
2. Esperar 30 minutos sin interactuar
3. Verificar que aparece modal de re-autenticación
4. Ingresar contraseña correcta
5. Verificar que sesión se renueva y continúa

### Probar Actualización de Actividad

1. Acceder como cualquier usuario
2. Navegar entre pestañas
3. Verificar en consola del navegador que `session-store` se actualiza
4. Campo `last_activity` debe tener timestamp reciente

## Troubleshooting

### La sesión expira muy rápido

**Solución**: Aumentar `SESSION_TIMEOUT_MINUTES` en `.env`

```bash
SESSION_TIMEOUT_MINUTES=60  # 1 hora
```

### La sesión no expira nunca

**Problema**: El intervalo de verificación no está funcionando

**Solución**: Verificar que `session-check-interval` existe en el layout

### Re-autenticación no funciona

**Problema**: Contraseña incorrecta o usuario no existe

**Solución**: 
1. Verificar que el usuario existe en `data/users.db`
2. Verificar logs de auditoría en `logs/audit.jsonl`
3. Revisar consola del navegador para errores

## Soporte

Para problemas o consultas:
- **Email**: ext.andres.lazcano@mineduc.cl
- **Logs**: Revisar `logs/app.log` y `logs/audit.jsonl`
- **Código**: `src/callbacks/session_callbacks.py`
