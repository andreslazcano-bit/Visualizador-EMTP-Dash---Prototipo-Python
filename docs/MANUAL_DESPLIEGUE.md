# 📘 MANUAL DE DESPLIEGUE - Visualizador EMTP

**Versión:** 2.0  
**Fecha:** Noviembre 2025  
**Audiencia:** Personal de TI (sin necesidad de conocimientos de Python)

---

## 📋 Índice

1. [Información General](#información-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Paso a Paso](#instalación-paso-a-paso)
4. [Configuración del Servidor](#configuración-del-servidor)
5. [Primera Ejecución](#primera-ejecución)
6. [Verificación de Instalación](#verificación-de-instalación)
7. [Configurar como Servicio](#configurar-como-servicio)
8. [Troubleshooting](#troubleshooting)
9. [Contactos de Soporte](#contactos-de-soporte)

---

## 📌 Información General

### ¿Qué es el Visualizador EMTP?

Es una aplicación web que muestra datos del sistema de Educación Técnico-Profesional de Chile mediante:
- Dashboards interactivos
- Mapas geográficos
- Exportación de reportes
- Sistema de usuarios con auditoría

### Componentes Principales

```
Visualizador EMTP/
├── app_v2.py              ← Archivo principal (NO MODIFICAR)
├── data/
│   ├── users.db           ← Base de datos de usuarios
│   ├── processed/         ← Datos de la aplicación
│   └── raw/              ← Datos originales
├── logs/
│   ├── app.log           ← Logs de aplicación
│   └── audit.jsonl       ← Logs de auditoría
├── config/               ← Configuración (NO MODIFICAR)
└── venv/                ← Ambiente Python (generado automáticamente)
```

---

## 🔧 Requisitos Previos

### Software Necesario

| Software | Versión Mínima | Link de Descarga |
|----------|----------------|------------------|
| **Python** | 3.12 o superior | https://www.python.org/downloads/ |
| **Sistema Operativo** | Windows 10/Server 2016 o superior, macOS 11+, Linux (Ubuntu 20.04+) | - |

### Hardware Recomendado

- **CPU:** 2 cores o más
- **RAM:** 4 GB mínimo, 8 GB recomendado
- **Disco:** 10 GB disponibles
- **Red:** Conexión estable (para acceso de usuarios)

### Puertos de Red

- **Puerto 8051:** Puerto por defecto de la aplicación
- **Firewall:** Debe permitir conexiones entrantes en el puerto 8051

---

## 📦 Instalación Paso a Paso

### Paso 1: Obtener el Código

**Opción A: Desde Git (recomendado)**

```bash
cd C:\Apps  # o /opt/apps en Linux
git clone https://github.com/tu-organizacion/visualizador-emtp.git
cd visualizador-emtp
```

**Opción B: Desde archivo ZIP**

1. Descomprimir `visualizador-emtp.zip` en `C:\Apps\visualizador-emtp`
2. Abrir terminal/cmd en esa carpeta

---

### Paso 2: Verificar Python

**Windows:**
```cmd
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

Debe mostrar: `Python 3.12.x` o superior

❌ **Si no está instalado:**
1. Ir a https://www.python.org/downloads/
2. Descargar instalador (marcar "Add Python to PATH")
3. Instalar
4. Reiniciar terminal y verificar nuevamente

---

### Paso 3: Crear Ambiente Virtual

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ **Verificación:** El prompt debe mostrar `(venv)` al inicio

---

### Paso 4: Instalar Dependencias

**Con terminal activo (venv):**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

⏱️ Esto puede tomar 3-5 minutos. Esperar hasta que termine.

✅ **Verificación:**
```bash
pip list | grep dash  # Linux/Mac
pip list | findstr dash  # Windows
```

Debe mostrar: `dash 2.14.2` o similar

---

### Paso 5: Configurar Base de Datos

**¡AUTOMÁTICO! No requiere acciones.**

La primera vez que se ejecute la aplicación, se creará automáticamente:
- Base de datos SQLite: `data/users.db`
- Usuario administrador por defecto:
  - **Usuario:** `admin`
  - **Contraseña:** `admin123`

⚠️ **IMPORTANTE:** Cambiar esta contraseña en el primer acceso.

---

## 🌐 Configuración del Servidor

### Variables de Entorno (Opcional)

Crear archivo `.env` en la raíz del proyecto:

```bash
# Configuración de Puerto
PORT=8051

# Configuración de Host (0.0.0.0 para acceso desde red)
HOST=0.0.0.0

# Nivel de Logs (INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Conexión SQL Server (si aplica)
SQL_SERVER_HOST=tu-servidor.dominio.cl
SQL_SERVER_USER=usuario_lectura
SQL_SERVER_PASSWORD=contraseña_segura
SQL_SERVER_DATABASE=EMTP_DB
```

**Si NO se crea este archivo, se usan valores por defecto.**

---

### Configuración de Firewall

**Windows (PowerShell como Administrador):**

```powershell
New-NetFirewallRule -DisplayName "Visualizador EMTP" `
  -Direction Inbound `
  -LocalPort 8051 `
  -Protocol TCP `
  -Action Allow
```

**Linux (Ubuntu/Debian):**

```bash
sudo ufw allow 8051/tcp
sudo ufw reload
```

---

## ▶️ Primera Ejecución

### Modo Manual (para pruebas)

**Windows:**
```cmd
cd C:\Apps\visualizador-emtp
venv\Scripts\activate
python app_v2.py
```

**macOS/Linux:**
```bash
cd /opt/apps/visualizador-emtp
source venv/bin/activate
python app_v2.py
```

✅ **Salida esperada:**

```
2025-11-17 12:00:00 | INFO | ✅ Base de datos de usuarios inicializada
2025-11-17 12:00:00 | INFO | ✅ Usuario admin creado por defecto
2025-11-17 12:00:00 | INFO | 🚀 Iniciando Visualizador EMTP v2.0
Dash is running on http://0.0.0.0:8051/

 * Running on http://127.0.0.1:8051
 * Running on http://10.100.105.105:8051
```

---

## ✅ Verificación de Instalación

### 1. Verificar que el servidor está corriendo

Abrir navegador web y acceder a:
```
http://localhost:8051
```

Debe mostrar la pantalla de login.

---

### 2. Probar Login Administrador

- **Usuario:** `admin`
- **Contraseña:** `admin123`
- Hacer clic en "Acceso Administrador"

✅ **Debe acceder al dashboard completo con menú lateral**

---

### 3. Verificar Base de Datos

```bash
# Desde la carpeta del proyecto
ls -l data/users.db          # Linux/Mac
dir data\users.db           # Windows
```

Debe existir el archivo `users.db` (aproximadamente 8-12 KB)

---

### 4. Verificar Logs

```bash
# Desde la carpeta del proyecto
tail -f logs/app.log         # Linux/Mac
type logs\app.log            # Windows (ver últimas líneas)
```

No debe haber líneas con `ERROR` o `CRITICAL`

---

## 🔄 Configurar como Servicio

### Linux (systemd)

**1. Crear archivo de servicio:**

```bash
sudo nano /etc/systemd/system/visualizador-emtp.service
```

**2. Copiar esta configuración:**

```ini
[Unit]
Description=Visualizador EMTP - Dashboard Interactivo
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/apps/visualizador-emtp
Environment="PATH=/opt/apps/visualizador-emtp/venv/bin"
ExecStart=/opt/apps/visualizador-emtp/venv/bin/python app_v2.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**3. Activar servicio:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable visualizador-emtp
sudo systemctl start visualizador-emtp
```

**4. Verificar estado:**

```bash
sudo systemctl status visualizador-emtp
```

Debe mostrar: `Active: active (running)`

---

### Windows (NSSM - Non-Sucking Service Manager)

**1. Descargar NSSM:**
- Ir a: https://nssm.cc/download
- Descargar versión para Windows
- Extraer `nssm.exe` a `C:\Windows\System32`

**2. Instalar servicio (cmd como Administrador):**

```cmd
nssm install VisualizadorEMTP
```

**3. Configurar en la ventana que aparece:**

- **Path:** `C:\Apps\visualizador-emtp\venv\Scripts\python.exe`
- **Startup directory:** `C:\Apps\visualizador-emtp`
- **Arguments:** `app_v2.py`

**4. Iniciar servicio:**

```cmd
nssm start VisualizadorEMTP
```

**5. Verificar:**

```cmd
nssm status VisualizadorEMTP
```

Debe mostrar: `SERVICE_RUNNING`

---

## 🔍 Troubleshooting

### ❌ Error: "Puerto 8051 en uso"

**Problema:** Otro programa está usando el puerto 8051

**Solución 1 - Liberar puerto (Windows):**
```cmd
netstat -ano | findstr :8051
taskkill /PID [número_PID] /F
```

**Solución 2 - Cambiar puerto:**
Editar `.env` y cambiar `PORT=8052`

---

### ❌ Error: "ModuleNotFoundError: No module named 'dash'"

**Problema:** Ambiente virtual no está activado o dependencias no instaladas

**Solución:**
```bash
# Activar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

---

### ❌ Error: "Permission denied" al crear `data/users.db`

**Problema:** Usuario no tiene permisos en la carpeta `data/`

**Solución (Linux):**
```bash
sudo chown -R www-data:www-data /opt/apps/visualizador-emtp/data
sudo chmod -R 755 /opt/apps/visualizador-emtp/data
```

**Solución (Windows):**
1. Click derecho en carpeta `data`
2. Propiedades → Seguridad
3. Dar "Control Total" al usuario que ejecuta el servicio

---

### ❌ Error: "Database is locked"

**Problema:** SQLite está siendo accedido por múltiples procesos

**Solución:**
```bash
# Detener todas las instancias
ps aux | grep app_v2.py  # Linux/Mac
tasklist | findstr python  # Windows

# Matar procesos duplicados
kill -9 [PID]  # Linux/Mac
taskkill /PID [PID] /F  # Windows

# Reiniciar servicio
sudo systemctl restart visualizador-emtp  # Linux
nssm restart VisualizadorEMTP  # Windows
```

---

### ❌ La aplicación se cierra inesperadamente

**Solución:**

1. **Revisar logs:**
   ```bash
   tail -100 logs/app.log  # Linux/Mac
   type logs\app.log       # Windows
   ```

2. **Buscar líneas con ERROR o CRITICAL**

3. **Errores comunes:**
   - Memoria insuficiente → Aumentar RAM del servidor
   - Archivo de datos corrupto → Restaurar desde backup
   - Permiso denegado → Revisar permisos de archivos

---

## 📞 Contactos de Soporte

### Soporte Técnico - Desarrollo
**Rol:** Desarrollador del Sistema  
**Nombre:** Andrés Lazcano  
**Email:** ext.andres.lazcano@mineduc.cl  
**GitHub:** @andreslazcano-bit

---

## 📚 Documentos Relacionados

- **Manual de Mantenimiento:** `docs/MANUAL_MANTENIMIENTO.md`
- **Manual de Usuario:** `docs/MANUAL_USUARIO.md`
- **Arquitectura del Sistema:** `docs/ARQUITECTURA.md`
- **Roadmap de Desarrollo:** `docs/ROADMAP.md`

---

## 📝 Control de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | Nov 2025 | Versión inicial del manual |

---

**NOTA IMPORTANTE:** Este manual está diseñado para personal de TI sin conocimientos específicos de Python. Todos los pasos están documentados para ejecutarse mediante comandos de terminal. Si encuentra algún error no documentado aquí, contactar a soporte nivel 2.
