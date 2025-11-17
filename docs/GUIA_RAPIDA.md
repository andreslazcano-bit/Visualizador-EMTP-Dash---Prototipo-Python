# ⚡ GUÍA RÁPIDA - Visualizador EMTP

**Versión 2.0** | Noviembre 2025

---

## 🚀 Inicio Rápido

### Acceso al Sistema
```
URL: http://[servidor-emtp]:8051
```

**Modo Usuario:** Click "Acceso como Usuario" (sin login)  
**Modo Admin:** Ingresar credenciales → "Acceso Administrador"

**Login por defecto (primer acceso):**
- Usuario: `admin`
- Contraseña: `admin123` ⚠️ **CAMBIAR INMEDIATAMENTE**

---

## 📱 Perfiles de Usuario

| Perfil | Login | Acceso |
|--------|-------|--------|
| 👤 **Usuario** | No | Dashboards básicos |
| 📊 **Analista** | Sí | Dashboards + Exportación |
| 🔧 **Admin** | Sí | Todo + Gestión Usuarios + Auditoría |

---

## 🎯 Tareas Comunes

### 1️⃣ Ver Dashboard de Matrícula

1. Click **"Matrícula"** (menú lateral)
2. Seleccionar sub-opción: "Evolución Temporal"
3. Navegar por gráficos y tablas

---

### 2️⃣ Aplicar Filtros

1. Seleccionar valores en dropdowns (Año, Región, etc.)
2. Click **"Aplicar Filtros"**
3. Click **"Limpiar Filtros"** para resetear

---

### 3️⃣ Exportar a Excel

1. Aplicar filtros (si se requieren)
2. Scroll hasta el final
3. Click **"📊 Descargar Excel"**
4. Archivo se descarga automáticamente

---

### 4️⃣ Crear Nuevo Usuario (Solo Admin)

1. Menú lateral → **"Gestión de Usuarios"**
2. Click **"+ Crear Nuevo Usuario"**
3. Completar formulario:
   - Nombre de Usuario (sin espacios)
   - Nombre Completo
   - Email (opcional)
   - Perfil (Usuario/Analista/Admin)
   - Contraseña (min. 8 caracteres)
4. Click **"Guardar"**
5. **Informar credenciales al usuario por canal seguro**

---

### 5️⃣ Desactivar Usuario (Solo Admin)

1. **"Gestión de Usuarios"** → Seleccionar usuario
2. Click **"Desactivar"**
3. Usuario ya no puede acceder (pero se conservan sus datos)

---

### 6️⃣ Ver Auditoría de Accesos (Solo Admin)

1. Menú lateral → **"Auditoría"**
2. Seleccionar filtros:
   - **Período:** Últimos 7 días
   - **Usuario:** Todos
   - **Acción:** Login/Logout
   - **Estado:** Fallido (para ver intentos fallidos)
3. Click **"🔄 Actualizar"**
4. Revisar tabla de logs

---

## 🔍 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| **No puedo acceder** | Verificar credenciales / Contactar admin |
| **Página en blanco** | Refrescar navegador (Ctrl+F5 / Cmd+Shift+R) |
| **Gráficos no cargan** | Verificar conexión internet / Limpiar caché |
| **Error al exportar** | Limpiar filtros / Intentar nuevamente |
| **Olvidé mi contraseña** | Contactar admin: ti@mineduc.cl |
| **No veo opción de Admin** | No tiene perfil Admin / Solicitar acceso |

---

## 🛠️ Para TI

### Verificar Estado del Servicio

**Linux:**
```bash
sudo systemctl status visualizador-emtp
```

**Windows:**
```cmd
nssm status VisualizadorEMTP
```

---

### Reiniciar Servicio

**Linux:**
```bash
sudo systemctl restart visualizador-emtp
```

**Windows:**
```cmd
nssm restart VisualizadorEMTP
```

---

### Ver Logs de Error

**Linux:**
```bash
tail -100 /opt/apps/visualizador-emtp/logs/app.log | grep ERROR
```

**Windows:**
```cmd
type C:\Apps\visualizador-emtp\logs\app.log | findstr ERROR
```

---

### Liberar Puerto 8051

**Linux:**
```bash
sudo lsof -ti:8051 | xargs kill -9
```

**Windows:**
```cmd
netstat -ano | findstr :8051
taskkill /PID [número] /F
```

---

### Backup Manual Urgente

**Linux:**
```bash
cp /opt/apps/visualizador-emtp/data/users.db \
   /backups/users_$(date +%Y%m%d_%H%M).db
```

**Windows:**
```cmd
copy C:\Apps\visualizador-emtp\data\users.db ^
     C:\Backups\users_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%.db
```

---

### Resetear Contraseña Admin (Emergencia)

**Generar hash de nueva contraseña:**
```bash
cd /opt/apps/visualizador-emtp
source venv/bin/activate
python -c "import bcrypt; print(bcrypt.hashpw(b'nueva_pass', bcrypt.gensalt(12)))"
```

**Actualizar en base de datos:**
```bash
sqlite3 /opt/apps/visualizador-emtp/data/users.db
UPDATE users SET password_hash = '[hash_generado]' WHERE username = 'admin';
.quit
```

---

## 📞 Contactos de Emergencia

### 🔴 Crítico (Sistema Caído)
**TI Nivel 2:** ti@mineduc.cl | +56 2 XXXX XXXX  
**Desarrollador:** andres.lazcano@mineduc.cl | +56 9 XXXX XXXX

### 🟡 No Crítico
**Soporte TI:** ti@mineduc.cl (9:00-18:00)  
**Soporte Funcional:** secretaria.emtp@mineduc.cl (9:00-17:00)

---

## 📊 Flujos Críticos

### Diagrama: Troubleshooting Sistema Caído

```
┌─────────────────────┐
│ Sistema no responde │
└──────────┬──────────┘
           │
           ↓
     ¿Responde ping?
           │
    ┌──────┴──────┐
    NO            SÍ
    │              │
    ↓              ↓
Verificar      ¿Puerto 8051
servidor       abierto?
físico            │
                ┌─┴─┐
                NO  SÍ
                │    │
                │    ↓
                │  Revisar
                │  logs de
                │  aplicación
                │    │
                │    ↓
                │  Reiniciar
                │  servicio
                │
                ↓
              Liberar
              puerto
                │
                ↓
              Iniciar
              servicio
```

---

### Checklist: Mantenimiento Diario

- [ ] Verificar servicio corriendo (`systemctl status`)
- [ ] Probar acceso web (http://localhost:8051)
- [ ] Revisar espacio en disco (`df -h`)
- [ ] Buscar errores en logs (`grep ERROR app.log`)

---

### Checklist: Mantenimiento Semanal

- [ ] Backup de `data/users.db`
- [ ] Backup de `logs/audit.jsonl`
- [ ] Revisar intentos fallidos de login (Auditoría)
- [ ] Verificar actualización de datos (lunes 6 AM)

---

### Checklist: Mantenimiento Mensual

- [ ] Backup completo (tar/zip)
- [ ] Rotación de logs
- [ ] Revisar usuarios inactivos (+30 días)
- [ ] Actualizar dependencias Python

---

## 🎨 Atajos de Teclado

| Acción | Atajo |
|--------|-------|
| Refrescar página | `Ctrl+R` (Win) / `Cmd+R` (Mac) |
| Limpiar caché | `Ctrl+Shift+R` / `Cmd+Shift+R` |
| Cambiar tema | Click en 🌙 |
| Cerrar sesión | Click en usuario → Cerrar Sesión |

---

## 📐 Especificaciones Técnicas

| Componente | Tecnología |
|------------|------------|
| **Backend** | Python 3.12 + Dash 2.14 |
| **Base de Datos** | SQLite 3 |
| **Autenticación** | bcrypt + JWT |
| **Frontend** | Plotly + Bootstrap 5 |
| **Puerto** | 8051 (por defecto) |
| **Logs** | Loguru + JSONL |

---

## 📚 Documentación Completa

- 📘 **Manual de Usuario:** `docs/MANUAL_USUARIO.md` (30 páginas)
- 🔧 **Manual de Despliegue:** `docs/MANUAL_DESPLIEGUE.md` (25 páginas)
- 🛠️ **Manual de Mantenimiento:** `docs/MANUAL_MANTENIMIENTO.md` (35 páginas)
- 🏗️ **Arquitectura:** `docs/ARQUITECTURA.md`
- 🗺️ **Roadmap:** `docs/ROADMAP.md`

---

## ✅ Checklist: Entrega a Producción

**Antes de poner en producción:**

- [ ] Python 3.12+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Puerto 8051 habilitado en firewall
- [ ] Servicio configurado (systemd/NSSM)
- [ ] Backup automático configurado (cron/tarea programada)
- [ ] Contraseña de `admin` cambiada
- [ ] Usuarios necesarios creados
- [ ] TI capacitado en procedimientos básicos
- [ ] Secretaría capacitada en uso del sistema
- [ ] Contactos de soporte documentados

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0  

---

💡 **Tip:** Imprimir esta guía y tenerla cerca del servidor para consultas rápidas.
