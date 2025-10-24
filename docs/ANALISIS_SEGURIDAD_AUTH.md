# 🔒 ANÁLISIS DE SEGURIDAD - SISTEMA DE AUTENTICACIÓN
**Fecha:** 20 de octubre de 2025  
**Aplicación:** Visualizador EMTP v2.0  
**Analista:** GitHub Copilot

---

## 📊 RESUMEN EJECUTIVO

### Estado General: ⚠️ **MEDIO-ALTO RIESGO**

**Calificación de Seguridad:** 5.5/10

El sistema implementa algunas buenas prácticas de seguridad pero presenta **vulnerabilidades críticas** que deben ser corregidas antes de producción.

---

## 🔴 VULNERABILIDADES CRÍTICAS

### 1. **Contraseña Hardcodeada en Código** ⚠️ CRÍTICO
**Archivo:** `src/callbacks/auth_callbacks.py` línea 107
```python
if password == 'admin123':  # ❌ CONTRASEÑA EN TEXTO PLANO
```

**Impacto:** CRÍTICO
- La contraseña está visible en el código fuente
- Cualquiera con acceso al repositorio conoce la contraseña admin
- No se puede cambiar sin modificar código

**Solución:**
```python
# ✅ Usar comparación con hash almacenado
from src.utils.auth import AuthManager
user_data = AuthManager.authenticate_user('admin', password)
if user_data:
    # Autenticado correctamente
```

---

### 2. **Modo Usuario sin Autenticación** ⚠️ ALTO RIESGO
**Archivo:** `src/callbacks/auth_callbacks.py` línea 81-95

**Problema:**
- Cualquiera puede acceder al "Modo Usuario" sin credenciales
- No hay registro de quién accede
- No hay control de sesiones

**Recomendación:**
- Si el propósito es acceso público, documentarlo claramente
- Si no, implementar autenticación básica (usuario + PIN o token)

---

### 3. **Sesión sin Expiración** ⚠️ MEDIO RIESGO
**Archivo:** `app_v2.py` línea 73

**Problema:**
```python
dcc.Store(id='session-store', storage_type='session')
```
- Las sesiones persisten indefinidamente en el navegador
- No hay timeout de inactividad
- Token JWT generado pero no utilizado en frontend

**Solución:**
```python
# Implementar verificación de expiración
session_data = {
    'authenticated': True,
    'user_info': {...},
    'expires_at': datetime.now() + timedelta(hours=8),  # ✅ Expiración
    'token': user_data['token']  # ✅ Usar JWT
}
```

---

### 4. **Secrets Débiles en Configuración** ⚠️ ALTO RIESGO
**Archivo:** `config/settings.py` líneas 24, 99

```python
SECRET_KEY: str = os.getenv('SECRET_KEY', 'change-this-secret-key')  # ❌
JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')  # ❌
```

**Problema:**
- Valores por defecto predecibles
- No hay validación de complejidad
- Mismos secrets en todos los ambientes

**Solución:**
```python
import secrets

# ✅ Generar secret fuerte o validar
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY or SECRET_KEY == 'change-this-secret-key':
    if ENVIRONMENT == 'production':
        raise ValueError("SECRET_KEY debe configurarse en producción")
    SECRET_KEY = secrets.token_urlsafe(32)

# Validar longitud mínima
if len(SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY debe tener al menos 32 caracteres")
```

---

### 5. **Sin Protección contra Fuerza Bruta** ⚠️ ALTO RIESGO
**Archivo:** `src/callbacks/auth_callbacks.py` línea 107

**Problema:**
- No hay límite de intentos fallidos
- No hay CAPTCHA ni rate limiting
- Permite ataques de fuerza bruta ilimitados

**Solución:**
```python
# ✅ Implementar contador de intentos
from collections import defaultdict
from datetime import datetime, timedelta

login_attempts = defaultdict(list)
MAX_ATTEMPTS = 5
LOCKOUT_TIME = timedelta(minutes=15)

def check_rate_limit(username: str) -> bool:
    """Verifica si el usuario está bloqueado por intentos fallidos"""
    now = datetime.now()
    # Limpiar intentos antiguos
    login_attempts[username] = [
        attempt for attempt in login_attempts[username]
        if now - attempt < LOCKOUT_TIME
    ]
    
    if len(login_attempts[username]) >= MAX_ATTEMPTS:
        return False  # Bloqueado
    return True  # Permitido

def record_failed_attempt(username: str):
    """Registra un intento fallido"""
    login_attempts[username].append(datetime.now())
```

---

## 🟡 VULNERABILIDADES MEDIAS

### 6. **Logging Insuficiente de Eventos de Seguridad**
**Riesgo:** MEDIO

**Problemas:**
- No se registran intentos fallidos de login
- No hay auditoría de acciones administrativas
- Logs no incluyen IP del cliente

**Solución:**
```python
from flask import request

logger.warning(
    f"❌ Intento de login fallido - Usuario: {username}, IP: {request.remote_addr}"
)
logger.info(
    f"✅ Login exitoso - Usuario: {username}, IP: {request.remote_addr}, Perfil: {profile}"
)
```

---

### 7. **Sin Protección CSRF**
**Riesgo:** MEDIO

Dash maneja CSRF internamente pero no está explícitamente configurado.

**Verificar:**
```python
app.server.config['WTF_CSRF_ENABLED'] = True
app.server.config['WTF_CSRF_TIME_LIMIT'] = None
```

---

### 8. **Transmisión de Credenciales**
**Riesgo:** MEDIO

**Problema:**
- Contraseña se envía en callback (cifrada por HTTPS si está configurado)
- No hay indicación de si HTTPS está forzado

**Verificar:**
```python
# En producción
app.server.config['SESSION_COOKIE_SECURE'] = True  # Solo HTTPS
app.server.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible desde JS
app.server.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protección CSRF
```

---

## 🟢 ASPECTOS POSITIVOS

### ✅ Implementaciones Correctas:

1. **Hash de Contraseñas con bcrypt**
   - ✅ Usa bcrypt correctamente con salt automático
   - ✅ Algoritmo resistente a rainbow tables
   ```python
   salt = bcrypt.gensalt()
   hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
   ```

2. **JWT con Expiración**
   - ✅ Tokens JWT con fecha de expiración
   - ✅ Payload incluye permisos
   ```python
   'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
   ```

3. **Sistema de Permisos Granular**
   - ✅ Perfiles claramente definidos
   - ✅ Permisos por funcionalidad
   - ✅ Secciones ocultas por perfil

4. **Separación de Responsabilidades**
   - ✅ AuthManager centralizado
   - ✅ Configuración en settings.py
   - ✅ Callbacks separados

---

## 🔧 RECOMENDACIONES PRIORITARIAS

### 🔥 Urgente (Antes de Producción):

1. **Eliminar contraseña hardcodeada**
   ```python
   # Usar authenticate_user en lugar de comparación directa
   user_data = AuthManager.authenticate_user('admin', password)
   if user_data:
       # Autenticado
   ```

2. **Configurar secrets fuertes**
   ```bash
   # Generar secrets en terminal
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # Agregar a .env
   SECRET_KEY=<secret_generado>
   JWT_SECRET_KEY=<otro_secret_generado>
   ```

3. **Implementar rate limiting**
   - Usar Redis para contador distribuido
   - O implementar con diccionario temporal

4. **Forzar HTTPS en producción**
   ```python
   if ENVIRONMENT == 'production':
       from flask_talisman import Talisman
       Talisman(app.server, force_https=True)
   ```

5. **Logging de seguridad completo**
   ```python
   # Agregar IP y timestamp a todos los logs de auth
   logger.bind(ip=request.remote_addr, user=username).info("Login attempt")
   ```

---

### ⏰ Medio Plazo:

6. **Implementar autenticación de dos factores (2FA)**
   - TOTP con Google Authenticator
   - O código por email

7. **Base de datos para usuarios**
   - Eliminar DEMO_USERS hardcodeado
   - PostgreSQL o Redis para persistencia

8. **Gestión de sesiones avanzada**
   - Invalidación de tokens
   - Logout forzado remoto
   - Sesiones concurrentes limitadas

9. **Auditoría completa**
   - Log de todas las acciones críticas
   - Exportación de datos
   - Cambios de configuración

10. **Variables de entorno obligatorias**
    ```python
    required_vars = ['SECRET_KEY', 'JWT_SECRET_KEY', 'ADMIN_USERNAME']
    if ENVIRONMENT == 'production':
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"{var} requerida en producción")
    ```

---

### 🔮 Largo Plazo:

11. **OAuth2/OpenID Connect**
    - Integración con Azure AD / Google
    - SSO empresarial

12. **Política de contraseñas**
    - Complejidad mínima
    - Expiración periódica
    - Historial de contraseñas

13. **Monitoreo de seguridad**
    - Alertas de intentos sospechosos
    - Dashboard de auditoría
    - Integración con SIEM

---

## 📋 CHECKLIST DE SEGURIDAD PRE-PRODUCCIÓN

```markdown
### Configuración
- [ ] SECRET_KEY configurado con 32+ caracteres aleatorios
- [ ] JWT_SECRET_KEY configurado con 32+ caracteres aleatorios
- [ ] DEBUG=False en producción
- [ ] HTTPS forzado
- [ ] Cookies con flags Secure y HttpOnly

### Autenticación
- [ ] Contraseña admin cambiada desde admin123
- [ ] Contraseña almacenada como hash en .env o DB
- [ ] Rate limiting implementado (5 intentos / 15 min)
- [ ] Logging de intentos fallidos con IP
- [ ] Timeout de sesión configurado (8 horas)

### Código
- [ ] Sin contraseñas hardcodeadas
- [ ] Sin secrets en repositorio
- [ ] .env en .gitignore
- [ ] Variables sensibles validadas al inicio
- [ ] JWT verificado en callbacks críticos

### Monitoreo
- [ ] Logs centralizados
- [ ] Alertas de seguridad configuradas
- [ ] Backup de logs (30 días)
- [ ] Auditoría de accesos habilitada

### Pruebas
- [ ] Test de penetración básico
- [ ] Verificación de rate limiting
- [ ] Test de sesiones expiradas
- [ ] Validación de HTTPS
```

---

## 🎯 CÓDIGO DE MEJORAS SUGERIDAS

### Archivo: `src/utils/rate_limiter.py` (NUEVO)
```python
"""Rate limiter para protección contra fuerza bruta"""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List
from loguru import logger

class RateLimiter:
    """Limita intentos de login por usuario"""
    
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        self.max_attempts = max_attempts
        self.window = timedelta(minutes=window_minutes)
        self.attempts: Dict[str, List[datetime]] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Verifica si se permite el intento"""
        now = datetime.now()
        
        # Limpiar intentos antiguos
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if now - attempt < self.window
        ]
        
        # Verificar límite
        if len(self.attempts[identifier]) >= self.max_attempts:
            logger.warning(f"🚫 Rate limit excedido para: {identifier}")
            return False
        
        return True
    
    def record_attempt(self, identifier: str):
        """Registra un intento"""
        self.attempts[identifier].append(datetime.now())
    
    def reset(self, identifier: str):
        """Resetea contador (login exitoso)"""
        if identifier in self.attempts:
            del self.attempts[identifier]

# Instancia global
login_limiter = RateLimiter(max_attempts=5, window_minutes=15)
```

### Archivo: `src/callbacks/auth_callbacks.py` (MODIFICADO)
```python
# Importar rate limiter
from src.utils.rate_limiter import login_limiter
from flask import request

def access_admin_mode(n_clicks, password):
    """Acceso al modo admin con validación de contraseña"""
    if n_clicks and password:
        # ✅ Obtener IP del cliente
        client_ip = request.remote_addr
        identifier = f"admin_{client_ip}"
        
        # ✅ Verificar rate limit
        if not login_limiter.is_allowed(identifier):
            logger.warning(f"🚫 Rate limit excedido - IP: {client_ip}")
            return (
                no_update, no_update,
                dbc.Alert(
                    "Demasiados intentos. Intente en 15 minutos.",
                    color="danger"
                ),
                True
            )
        
        # ✅ Usar authenticate_user en lugar de comparación directa
        user_data = AuthManager.authenticate_user('admin', password)
        
        if user_data:
            # ✅ Login exitoso - resetear contador
            login_limiter.reset(identifier)
            logger.info(f"✅ Login admin exitoso - IP: {client_ip}")
            
            admin_session = {
                'authenticated': True,
                'user_info': user_data,
                'token': user_data['token'],  # ✅ Incluir JWT
                'expires_at': (datetime.now() + timedelta(hours=8)).isoformat()
            }
            return (
                create_authenticated_layout(admin_session['user_info']), 
                admin_session, 
                "", 
                False
            )
        else:
            # ❌ Contraseña incorrecta - registrar intento
            login_limiter.record_attempt(identifier)
            remaining = login_limiter.max_attempts - len(login_limiter.attempts[identifier])
            
            logger.warning(
                f"❌ Intento fallido - IP: {client_ip}, Intentos restantes: {remaining}"
            )
            
            return (
                no_update, no_update,
                dbc.Alert(
                    f"Contraseña incorrecta. Intentos restantes: {remaining}",
                    color="danger",
                    dismissable=True
                ),
                True
            )
    
    return no_update, no_update, no_update, no_update
```

### Archivo: `.env.example` (NUEVO)
```bash
# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD - NO COMMITEAR .env REAL
# ============================================================================

# Generar con: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=CAMBIAR_POR_SECRET_ALEATORIO_32_CHARS
JWT_SECRET_KEY=CAMBIAR_POR_OTRO_SECRET_ALEATORIO_32_CHARS

# Configuración de admin
ADMIN_USERNAME=admin
# Generar hash con: python src/utils/auth.py TU_PASSWORD_SEGURA
ADMIN_PASSWORD_HASH=HASH_GENERADO_CON_BCRYPT

# Ambiente
ENVIRONMENT=production
DEBUG=False

# Seguridad
JWT_EXPIRATION_HOURS=8
AUTH_ENABLED=True
```

---

## 📚 RECURSOS ADICIONALES

### Documentación Recomendada:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Dash Security Best Practices](https://dash.plotly.com/authentication)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)

### Herramientas de Testing:
- **Bandit**: Análisis estático de seguridad Python
  ```bash
  pip install bandit
  bandit -r src/ -f json -o security_report.json
  ```

- **Safety**: Verifica dependencias vulnerables
  ```bash
  pip install safety
  safety check
  ```

---

## ✅ CONCLUSIÓN

El sistema tiene una **base sólida** con bcrypt, JWT y permisos granulares, pero requiere:

1. **Correcciones críticas** antes de producción (contraseña hardcodeada, secrets débiles)
2. **Rate limiting** para prevenir fuerza bruta
3. **Logging robusto** para auditoría
4. **HTTPS forzado** en producción

**Tiempo estimado de correcciones urgentes:** 2-4 horas  
**Riesgo actual en producción:** ALTO  
**Riesgo después de correcciones:** BAJO-MEDIO

---

**Próxima revisión recomendada:** Después de implementar correcciones críticas

