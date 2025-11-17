# 🔧 MANUAL DE MANTENIMIENTO - Visualizador EMTP

**Versión:** 2.0  
**Fecha:** Noviembre 2025  
**Audiencia:** Personal de TI (Mantenimiento y Operaciones)

---

## 📋 Índice

1. [Verificaciones Diarias](#verificaciones-diarias)
2. [Tareas Semanales](#tareas-semanales)
3. [Tareas Mensuales](#tareas-mensuales)
4. [Procedimientos de Backup](#procedimientos-de-backup)
5. [Gestión de Usuarios](#gestión-de-usuarios)
6. [Monitoreo de Logs](#monitoreo-de-logs)
7. [Rotación de Logs](#rotación-de-logs)
8. [Actualización del Sistema](#actualización-del-sistema)
9. [Errores Comunes y Soluciones](#errores-comunes-y-soluciones)
10. [Procedimientos de Emergencia](#procedimientos-de-emergencia)

---

## ✅ Verificaciones Diarias

### 1. Verificar que la Aplicación está Corriendo

**Comando (Linux):**
```bash
sudo systemctl status visualizador-emtp
```

**Comando (Windows):**
```cmd
nssm status VisualizadorEMTP
```

**Salida esperada:**
- Linux: `Active: active (running)`
- Windows: `SERVICE_RUNNING`

❌ **Si está detenida:**
```bash
# Linux
sudo systemctl start visualizador-emtp

# Windows
nssm start VisualizadorEMTP
```

---

### 2. Verificar Acceso Web

**Desde el servidor:**
```bash
curl http://localhost:8051
```

**Desde cualquier navegador:**
```
http://[IP-del-servidor]:8051
```

✅ **Debe cargar la página de login (sin errores 500)**

---

### 3. Verificar Espacio en Disco

**Linux:**
```bash
df -h | grep -E 'Filesystem|/opt/apps'
```

**Windows:**
```cmd
wmic logicaldisk get size,freespace,caption
```

⚠️ **Alerta si queda menos de 2 GB disponibles**

---

### 4. Revisar Logs de Error

**Comando:**
```bash
# Linux/Mac
tail -50 /opt/apps/visualizador-emtp/logs/app.log | grep -i error

# Windows
type C:\Apps\visualizador-emtp\logs\app.log | findstr /i error
```

✅ **No debe haber nuevos errores en las últimas 24 horas**

---

## 📅 Tareas Semanales

### 1. Revisar Actividad de Usuarios

**Ver últimos logins (desde la app):**
1. Acceder como administrador
2. Ir a "Auditoría"
3. Filtrar por "Período: Últimos 7 días"
4. Revisar accesos fallidos

❌ **Alerta si hay más de 5 intentos fallidos del mismo usuario**
→ Posible intento de acceso no autorizado

---

### 2. Revisar Tamaño de Base de Datos

**Comando:**
```bash
# Linux/Mac
ls -lh /opt/apps/visualizador-emtp/data/users.db

# Windows
dir C:\Apps\visualizador-emtp\data\users.db
```

**Tamaño normal:** 8-50 KB (depende de cantidad de usuarios)

⚠️ **Alerta si supera 1 MB** → Posible corrupción

---

### 3. Verificar Actualización de Datos

**Revisar log de actualización semanal:**
```bash
# Linux/Mac
tail -50 /opt/apps/visualizador-emtp/logs/actualizacion_datos.log

# Windows
type C:\Apps\visualizador-emtp\logs\actualizacion_datos.log
```

Buscar líneas como:
```
✅ Actualización completada: 156,234 registros procesados
```

❌ **Si no hay actualizaciones en 7 días:**
1. Verificar conexión a SQL Server (si aplica)
2. Ejecutar manualmente: `python scripts/actualizar_datos_semanal.py`

---

### 4. Backup Semanal

**Ver sección: [Procedimientos de Backup](#procedimientos-de-backup)**

---

## 📆 Tareas Mensuales

### 1. Rotación de Logs

**Ver sección: [Rotación de Logs](#rotación-de-logs)**

---

### 2. Revisión de Usuarios Inactivos

**Comando (requiere acceso a SQLite):**
```bash
sqlite3 /opt/apps/visualizador-emtp/data/users.db \
  "SELECT username, last_login FROM users WHERE last_login < datetime('now', '-30 days');"
```

**Desactivar usuarios inactivos (desde la app):**
1. Acceder como admin → "Gestión de Usuarios"
2. Seleccionar usuario inactivo
3. Click "Desactivar"

---

### 3. Actualización de Dependencias

**Ver sección: [Actualización del Sistema](#actualización-del-sistema)**

---

### 4. Backup Mensual (Largo Plazo)

**Crear backup completo:**
```bash
# Linux/Mac
tar -czf backup_emtp_$(date +%Y%m).tar.gz \
  /opt/apps/visualizador-emtp/data \
  /opt/apps/visualizador-emtp/logs

# Windows (PowerShell)
Compress-Archive -Path C:\Apps\visualizador-emtp\data, C:\Apps\visualizador-emtp\logs `
  -DestinationPath C:\Backups\emtp_$(Get-Date -Format "yyyyMM").zip
```

**Mover a almacenamiento externo:**
- Copiar a servidor de backups: `\\servidor-backup\emtp\`
- O subir a AWS S3 / Azure Blob Storage

---

## 💾 Procedimientos de Backup

### ¿Qué Respaldar?

| Archivo/Carpeta | Prioridad | Frecuencia | Retención |
|----------------|-----------|------------|-----------|
| `data/users.db` | **CRÍTICO** | Diario | 30 días |
| `logs/audit.jsonl` | **ALTA** | Semanal | 90 días |
| `data/processed/*.parquet` | MEDIA | Semanal | 14 días |
| `logs/app.log` | BAJA | Mensual | 12 meses |

---

### Backup Diario (Automatizado)

**Linux (Cron Job):**

1. Crear script `/opt/apps/backup_daily.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups/visualizador-emtp"
DATE=$(date +%Y%m%d)

# Crear carpeta de backups
mkdir -p $BACKUP_DIR

# Backup de base de datos
cp /opt/apps/visualizador-emtp/data/users.db \
   $BACKUP_DIR/users_${DATE}.db

# Backup de auditoría
cp /opt/apps/visualizador-emtp/logs/audit.jsonl \
   $BACKUP_DIR/audit_${DATE}.jsonl

# Eliminar backups antiguos (>30 días)
find $BACKUP_DIR -name "users_*.db" -mtime +30 -delete
find $BACKUP_DIR -name "audit_*.jsonl" -mtime +30 -delete

echo "✅ Backup completado: $(date)" >> /var/log/emtp_backup.log
```

2. Dar permisos:
```bash
chmod +x /opt/apps/backup_daily.sh
```

3. Agregar a cron (ejecutar diariamente a las 2 AM):
```bash
sudo crontab -e
```

Agregar línea:
```
0 2 * * * /opt/apps/backup_daily.sh
```

---

**Windows (Tarea Programada):**

1. Crear script `C:\Apps\backup_daily.bat`:
```batch
@echo off
set BACKUP_DIR=C:\Backups\visualizador-emtp
set DATE=%date:~-4%%date:~3,2%%date:~0,2%

mkdir "%BACKUP_DIR%" 2>nul

copy "C:\Apps\visualizador-emtp\data\users.db" "%BACKUP_DIR%\users_%DATE%.db"
copy "C:\Apps\visualizador-emtp\logs\audit.jsonl" "%BACKUP_DIR%\audit_%DATE%.jsonl"

forfiles /P "%BACKUP_DIR%" /M users_*.db /D -30 /C "cmd /c del @path"
forfiles /P "%BACKUP_DIR%" /M audit_*.jsonl /D -30 /C "cmd /c del @path"

echo Backup completado: %date% %time% >> C:\Backups\emtp_backup.log
```

2. Crear tarea programada (cmd como Administrador):
```cmd
schtasks /create /tn "Backup Visualizador EMTP" /tr "C:\Apps\backup_daily.bat" /sc daily /st 02:00
```

---

### Restauración desde Backup

**1. Detener aplicación:**
```bash
# Linux
sudo systemctl stop visualizador-emtp

# Windows
nssm stop VisualizadorEMTP
```

**2. Restaurar base de datos:**
```bash
# Linux
cp /backups/visualizador-emtp/users_20251117.db \
   /opt/apps/visualizador-emtp/data/users.db

# Windows
copy C:\Backups\visualizador-emtp\users_20251117.db C:\Apps\visualizador-emtp\data\users.db
```

**3. Restaurar auditoría:**
```bash
# Linux
cp /backups/visualizador-emtp/audit_20251117.jsonl \
   /opt/apps/visualizador-emtp/logs/audit.jsonl

# Windows
copy C:\Backups\visualizador-emtp\audit_20251117.jsonl C:\Apps\visualizador-emtp\logs\audit.jsonl
```

**4. Reiniciar aplicación:**
```bash
# Linux
sudo systemctl start visualizador-emtp

# Windows
nssm start VisualizadorEMTP
```

---

## 👥 Gestión de Usuarios

### Resetear Contraseña de Usuario

**Opción 1 - Desde la Aplicación (Recomendado):**
1. Login como admin
2. "Gestión de Usuarios"
3. Seleccionar usuario
4. Click "Editar"
5. Ingresar nueva contraseña
6. Click "Guardar"

---

**Opción 2 - Desde Terminal (Emergencias):**

```bash
# Acceder a la base de datos
sqlite3 /opt/apps/visualizador-emtp/data/users.db

# Generar hash de nueva contraseña (ejemplo: "nuevapass123")
# NOTA: Usar el script de Python incluido
```

**Script para generar hash:**

Crear archivo `/tmp/gen_password.py`:
```python
import bcrypt

password = input("Ingrese nueva contraseña: ")
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
print(f"\nHash generado:\n{hashed.decode('utf-8')}")
```

Ejecutar:
```bash
cd /opt/apps/visualizador-emtp
source venv/bin/activate
python /tmp/gen_password.py
```

Copiar el hash y actualizar en la base de datos:
```sql
UPDATE users 
SET password_hash = '[hash-generado]', 
    updated_at = datetime('now') 
WHERE username = 'nombre_usuario';
```

---

### Desactivar Usuario Comprometido

**Desde la aplicación:**
1. Login como admin → "Gestión de Usuarios"
2. Seleccionar usuario
3. Click "Desactivar"

**Desde terminal:**
```bash
sqlite3 /opt/apps/visualizador-emtp/data/users.db \
  "UPDATE users SET is_active = 0 WHERE username = 'usuario_comprometido';"
```

---

### Crear Nuevo Usuario Administrador

**Desde la aplicación:**
1. Login como admin → "Gestión de Usuarios"
2. Click "Crear Nuevo Usuario"
3. Completar formulario:
   - **Perfil:** Admin
   - **Usuario:** nuevo_admin
   - **Contraseña:** [segura, min 8 caracteres]
4. Click "Guardar"

---

## 📊 Monitoreo de Logs

### Tipos de Logs

| Archivo | Contenido | Ubicación |
|---------|-----------|-----------|
| `app.log` | Logs generales de la aplicación | `logs/app.log` |
| `audit.jsonl` | Auditoría de accesos y acciones | `logs/audit.jsonl` |
| `actualizacion_datos.log` | Actualización semanal de datos | `logs/actualizacion_datos.log` |

---

### Revisar Logs en Tiempo Real

**Linux/Mac:**
```bash
# Logs de aplicación
tail -f /opt/apps/visualizador-emtp/logs/app.log

# Logs de auditoría
tail -f /opt/apps/visualizador-emtp/logs/audit.jsonl
```

**Windows:**
```cmd
# Usar PowerShell
Get-Content C:\Apps\visualizador-emtp\logs\app.log -Wait -Tail 50
```

---

### Buscar Errores Específicos

**Buscar errores críticos:**
```bash
# Linux/Mac
grep -i "ERROR\|CRITICAL" /opt/apps/visualizador-emtp/logs/app.log

# Windows
findstr /i "ERROR CRITICAL" C:\Apps\visualizador-emtp\logs\app.log
```

**Buscar intentos de login fallidos:**
```bash
# Linux/Mac
grep "login.*False" /opt/apps/visualizador-emtp/logs/audit.jsonl | tail -20

# Windows
findstr "login.*False" C:\Apps\visualizador-emtp\logs\audit.jsonl
```

---

## 🔄 Rotación de Logs

### ¿Por qué Rotar Logs?

Los logs pueden crecer indefinidamente y llenar el disco. Se recomienda:
- **app.log:** Rotar cuando supere 50 MB
- **audit.jsonl:** Rotar mensualmente

---

### Script de Rotación Automática

**Linux (logrotate):**

1. Crear `/etc/logrotate.d/visualizador-emtp`:
```
/opt/apps/visualizador-emtp/logs/*.log {
    weekly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
}

/opt/apps/visualizador-emtp/logs/audit.jsonl {
    monthly
    rotate 12
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
}
```

2. Probar configuración:
```bash
sudo logrotate -d /etc/logrotate.d/visualizador-emtp
```

---

**Windows (Script PowerShell):**

Crear `C:\Apps\rotate_logs.ps1`:
```powershell
$LogDir = "C:\Apps\visualizador-emtp\logs"
$ArchiveDir = "C:\Apps\visualizador-emtp\logs\archive"
$Date = Get-Date -Format "yyyyMMdd"

# Crear carpeta de archivo
New-Item -ItemType Directory -Path $ArchiveDir -Force

# Rotar app.log si supera 50 MB
$AppLog = Get-Item "$LogDir\app.log"
if ($AppLog.Length -gt 50MB) {
    Move-Item "$LogDir\app.log" "$ArchiveDir\app_${Date}.log"
    New-Item "$LogDir\app.log" -ItemType File
}

# Rotar audit.jsonl mensualmente (primer día del mes)
if ((Get-Date).Day -eq 1) {
    Move-Item "$LogDir\audit.jsonl" "$ArchiveDir\audit_${Date}.jsonl"
    New-Item "$LogDir\audit.jsonl" -ItemType File
}

# Eliminar archivos antiguos (>12 meses)
Get-ChildItem $ArchiveDir -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddMonths(-12) } | Remove-Item
```

Programar (cmd como Administrador):
```cmd
schtasks /create /tn "Rotar Logs EMTP" /tr "powershell.exe -File C:\Apps\rotate_logs.ps1" /sc monthly /d 1 /st 03:00
```

---

## 🔄 Actualización del Sistema

### Actualizar Dependencias de Python

**1. Activar ambiente virtual:**
```bash
# Linux/Mac
cd /opt/apps/visualizador-emtp
source venv/bin/activate

# Windows
cd C:\Apps\visualizador-emtp
venv\Scripts\activate
```

**2. Actualizar pip:**
```bash
pip install --upgrade pip
```

**3. Actualizar dependencias:**
```bash
pip install --upgrade -r requirements.txt
```

**4. Reiniciar aplicación:**
```bash
# Linux
sudo systemctl restart visualizador-emtp

# Windows
nssm restart VisualizadorEMTP
```

---

### Actualizar Código de la Aplicación

**Si se recibe nueva versión del desarrollador:**

**1. Hacer backup completo:**
```bash
# Linux
cp -r /opt/apps/visualizador-emtp /opt/apps/visualizador-emtp_backup_$(date +%Y%m%d)

# Windows
xcopy C:\Apps\visualizador-emtp C:\Apps\visualizador-emtp_backup_%date:~-4%%date:~3,2%%date:~0,2% /E /I
```

**2. Detener servicio:**
```bash
# Linux
sudo systemctl stop visualizador-emtp

# Windows
nssm stop VisualizadorEMTP
```

**3. Actualizar código:**
```bash
# Si se usa Git
cd /opt/apps/visualizador-emtp
git pull origin main

# Si se recibe archivo ZIP
# Extraer archivos EXCEPTO carpetas: data/, logs/, venv/
```

**4. Actualizar dependencias:**
```bash
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**5. Reiniciar servicio:**
```bash
# Linux
sudo systemctl start visualizador-emtp

# Windows
nssm start VisualizadorEMTP
```

**6. Verificar funcionamiento:**
```
http://localhost:8051
```

---

## ⚠️ Errores Comunes y Soluciones

### Error 1: "Database is locked"

**Síntoma:** Usuarios no pueden crear/editar otros usuarios

**Causa:** Múltiples procesos accediendo SQLite simultáneamente

**Solución:**
```bash
# 1. Verificar procesos duplicados
ps aux | grep app_v2.py  # Linux
tasklist | findstr python  # Windows

# 2. Matar procesos duplicados (dejar solo 1)
kill -9 [PID]  # Linux
taskkill /PID [PID] /F  # Windows

# 3. Reiniciar servicio
sudo systemctl restart visualizador-emtp  # Linux
nssm restart VisualizadorEMTP  # Windows
```

---

### Error 2: "Port 8051 already in use"

**Síntoma:** Aplicación no inicia

**Causa:** Puerto ocupado por otro proceso

**Solución:**
```bash
# Linux
sudo lsof -ti:8051 | xargs kill -9

# Windows
netstat -ano | findstr :8051
taskkill /PID [número] /F
```

---

### Error 3: Usuarios no pueden acceder (404 Not Found)

**Síntoma:** Página de login carga, pero al ingresar sale error 404

**Causa:** Callbacks no registrados o error en código

**Solución:**
```bash
# 1. Revisar logs de error
tail -100 /opt/apps/visualizador-emtp/logs/app.log | grep ERROR

# 2. Verificar integridad de archivos
ls -l /opt/apps/visualizador-emtp/src/callbacks/

# 3. Si faltan archivos, restaurar desde backup o contactar desarrollador
```

---

### Error 4: Datos no se actualizan semanalmente

**Síntoma:** Dashboard muestra datos desactualizados

**Causa:** Script de actualización semanal falló

**Solución:**
```bash
# 1. Revisar log de actualización
tail -100 /opt/apps/visualizador-emtp/logs/actualizacion_datos.log

# 2. Ejecutar actualización manualmente
cd /opt/apps/visualizador-emtp
source venv/bin/activate
python scripts/actualizar_datos_semanal.py

# 3. Si falla, verificar conexión a SQL Server
python scripts/test_connections.py
```

---

### Error 5: Gráficos no cargan (solo spinners)

**Síntoma:** Dashboard muestra "Cargando..." indefinidamente

**Causa:** Archivos de datos corruptos o faltantes

**Solución:**
```bash
# 1. Verificar archivos de datos
ls -lh /opt/apps/visualizador-emtp/data/processed/

# 2. Si faltan archivos, restaurar desde backup
# 3. Si están corruptos, re-procesar datos:
cd /opt/apps/visualizador-emtp
source venv/bin/activate
python scripts/convert_rds_to_parquet.py  # Si aplica
```

---

## 🚨 Procedimientos de Emergencia

### Emergencia 1: Aplicación Caída (No Responde)

**Pasos Inmediatos:**

1. **Verificar servicio:**
```bash
systemctl status visualizador-emtp  # Linux
nssm status VisualizadorEMTP  # Windows
```

2. **Intentar reinicio:**
```bash
systemctl restart visualizador-emtp  # Linux
nssm restart VisualizadorEMTP  # Windows
```

3. **Si no inicia, revisar logs:**
```bash
tail -200 /opt/apps/visualizador-emtp/logs/app.log
```

4. **Contactar a desarrollador con logs**

---

### Emergencia 2: Base de Datos Corrupta

**Síntoma:** Error "database disk image is malformed"

**Pasos:**

1. **Detener aplicación**
2. **Hacer backup del archivo corrupto:**
```bash
cp /opt/apps/visualizador-emtp/data/users.db \
   /opt/apps/visualizador-emtp/data/users_corrupted.db
```

3. **Intentar reparación:**
```bash
sqlite3 /opt/apps/visualizador-emtp/data/users.db
.recover
.output /tmp/users_recovered.sql
.dump
.quit

sqlite3 /opt/apps/visualizador-emtp/data/users_new.db < /tmp/users_recovered.sql
mv /opt/apps/visualizador-emtp/data/users_new.db \
   /opt/apps/visualizador-emtp/data/users.db
```

4. **Si falla, restaurar desde backup más reciente**

---

### Emergencia 3: Servidor Sin Espacio en Disco

**Pasos:**

1. **Identificar archivos grandes:**
```bash
du -sh /opt/apps/visualizador-emtp/* | sort -h
```

2. **Limpiar logs antiguos:**
```bash
find /opt/apps/visualizador-emtp/logs -name "*.log" -mtime +90 -delete
```

3. **Comprimir logs de auditoría:**
```bash
gzip /opt/apps/visualizador-emtp/logs/audit_*.jsonl
```

4. **Mover backups antiguos a almacenamiento externo**

---

## 📞 Escalamiento de Incidentes

| Severidad | Descripción | Tiempo de Respuesta | Contacto |
|-----------|-------------|---------------------|----------|
| **CRÍTICO** | App caída, todos los usuarios afectados | 15 minutos | Desarrollador (tel directo) |
| **ALTA** | Funcionalidad principal no disponible | 2 horas | TI Nivel 2 |
| **MEDIA** | Funcionalidad secundaria afectada | 1 día laboral | TI Nivel 1 |
| **BAJA** | Solicitud de mejora o pregunta | 3 días laborales | Soporte funcional |

---

## 📚 Documentos Relacionados

- **Manual de Despliegue:** `docs/MANUAL_DESPLIEGUE.md`
- **Manual de Usuario:** `docs/MANUAL_USUARIO.md`
- **Guía Rápida:** `docs/GUIA_RAPIDA.md`

---

## 📝 Registro de Mantenimientos

**Llevar registro en:** `/opt/apps/visualizador-emtp/MANTENIMIENTO.log`

**Formato:**
```
[2025-11-17 14:30] - Backup mensual realizado - TI: Juan Pérez
[2025-11-18 09:00] - Actualización de dependencias - TI: María González
[2025-11-19 11:15] - Reset password usuario "analista01" - TI: Juan Pérez
```

---

**Última Actualización:** Noviembre 2025  
**Versión del Manual:** 1.0
