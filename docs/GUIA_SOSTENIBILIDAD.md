# Guía de Sostenibilidad del Proyecto

**Documento:** Análisis de Sostenibilidad y Mantenimiento  
**Versión:** 1.0  
**Fecha:** 17 de Noviembre 2025  
**Autor:** Andrés Lazcano con colaboración de IA

---

## Resumen Ejecutivo

**¿Puede el proyecto mantenerse con solo soporte de TI?**  
✅ **SÍ** - Para operación normal y mantenimiento rutinario  
⚠️ **NO** - Para nuevas funcionalidades o cambios en lógica de negocio

**Nivel de Sostenibilidad: 8/10**

---

## 1. Fortalezas para Sostenibilidad

### 1.1 Documentación Completa

El proyecto cuenta con 13 documentos técnicos (588 KB, ~210 páginas):

| Documento | Propósito | Audiencia |
|-----------|-----------|-----------|
| `MANUAL_DESPLIEGUE.md` | Instalación paso a paso | TI |
| `MANUAL_MANTENIMIENTO.md` | Operaciones día a día | TI |
| `ARQUITECTURA_DETALLADA.md` | Cómo funciona el sistema | Desarrolladores |
| `SISTEMA_USUARIOS_AUDITORIA.md` | Gestión de usuarios | TI/Desarrolladores |
| `ACTUALIZACION_AUTOMATICA.md` | Actualización de datos | TI |
| `README.md` | Visión general | Todos |

**Conclusión:** TI tiene toda la información necesaria para operar el sistema.

### 1.2 Tecnologías Estándar y Maduras

```
✅ Python 3.12        → Lenguaje común, mucho soporte
✅ SQLite             → Base de datos simple, sin servidor
✅ Dash/Plotly        → Framework maduro, bien documentado
✅ Docker             → Containerización estándar
✅ Git/GitHub         → Control de versiones profesional
```

**Conclusión:** Tecnologías con soporte de la comunidad, no dependientes del desarrollador.

### 1.3 Operación Simple

**Iniciar aplicación:**
```bash
source venv/bin/activate
python app_v2.py
```

**O con Docker (recomendado para producción):**
```bash
docker-compose up -d
```

**Conclusión:** TI puede arrancar/detener sin conocimientos avanzados de Python.

### 1.4 Sistema de Logs Implementado

```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Buscar errores
grep ERROR logs/app.log

# Ver auditoría de accesos
cat logs/audit.jsonl | jq '.'
```

**Conclusión:** Troubleshooting sin necesidad de debugger o IDE.

---

## 2. Tareas que TI Puede Realizar sin Desarrollador

### 2.1 Operación Diaria

| Tarea | Comando | Frecuencia |
|-------|---------|------------|
| Verificar app corriendo | `curl http://localhost:8051` | Diaria |
| Revisar logs | `tail -100 logs/app.log` | Diaria |
| Reiniciar app | `systemctl restart visualizador-emtp` | Según necesidad |
| Verificar espacio disco | `df -h` | Semanal |

### 2.2 Mantenimiento Semanal

```bash
# Backup de base de datos de usuarios
cp data/users.db backups/users_$(date +%Y%m%d).db

# Verificar actualización de datos
ls -lth data/processed/ | head

# Limpiar logs antiguos (opcional)
find logs/ -name "*.log" -mtime +90 -delete
```

### 2.3 Gestión de Usuarios

**Crear usuario (vía interfaz web):**
1. Login como admin
2. Ir a "Gestión de Usuarios"
3. Click "Crear Usuario"
4. Completar formulario

**Resetear contraseña (vía SQLite):**
```bash
sqlite3 data/users.db
UPDATE users SET password_hash = '<nuevo_hash>' WHERE username = 'usuario';
.quit
```

**Nota:** Para generar hash, contactar desarrollador o usar script incluido.

### 2.4 Troubleshooting Básico

| Problema | Síntoma | Solución |
|----------|---------|----------|
| App no carga | Error 404 | `systemctl restart visualizador-emtp` |
| Datos desactualizados | Fecha antigua en dashboard | Verificar cron job: `crontab -l` |
| Usuario no puede entrar | "Credenciales inválidas" | Verificar en users.db o resetear |
| Error en logs | Líneas con ERROR | Enviar a desarrollador |

---

## 3. Tareas que Requieren Desarrollador

### 3.1 Cambios en Lógica de Negocio

**Ejemplos:**
- "Agregar un nuevo módulo de análisis de empleabilidad"
- "Modificar el cálculo de tasas de titulación"
- "Cambiar los filtros disponibles en un dashboard"

**Razón:** Requiere modificar código Python, entender la arquitectura.

### 3.2 Cambios en Estructura de Datos

**Ejemplos:**
- "El MINEDUC cambió el formato del archivo CSV"
- "Necesitamos agregar una nueva columna a la base de datos"
- "Cambió el esquema de datos geográficos"

**Razón:** Requiere modificar scripts de ETL y procesamiento.

### 3.3 Integraciones con Otros Sistemas

**Ejemplos:**
- "Conectar con API de otro ministerio"
- "Exportar datos a SharePoint automáticamente"
- "Integrar con sistema de autenticación LDAP"

**Razón:** Requiere desarrollo de nuevas funcionalidades.

---

## 4. Áreas de Riesgo y Mitigación

### Riesgo 1: Actualización de Datos Falla

**Probabilidad:** Media  
**Impacto:** Alto (dashboards con datos desactualizados)

**Estado Actual:** ⚠️ **PENDIENTE DE DEFINIR CON TI MINEDUC**

**Situación:**
- SQLite se usa **SOLO** para gestión de usuarios de la aplicación (admin, analista, usuario)
- Los datos SIGE/MINEDUC se cargan desde archivos CSV/Parquet en `data/processed/`
- Actualmente NO hay conexión automática a fuentes de datos del MINEDUC

**✅ ACTUALIZACIÓN IMPORTANTE (Noviembre 2025):**

Según información de expertos del MINEDUC:
- **SIGE corre sobre SQL Server** (réplicas o DataMart institucional)
- **TI NO da acceso al transaccional**, pero SÍ a réplicas para análisis
- **La Opción 5 (SQL Server) es la MÁS PROBABLE** (80% probabilidad)
- Otras divisiones ya usan este método
- Proceso estándar: Usuario read-only en servidor de réplicas

**Opciones Disponibles (ordenadas por probabilidad):**

**⭐ Opción 5: SQL Server - Réplica del SIGE (MÁS PROBABLE - 80%)**
```python
# Conexión a réplica SQL Server (NO al transaccional)
import pyodbc

def conectar_replica_sige():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER=SQL-SIGE-REPLICA.mineduc.cl;"  # Servidor de réplicas
        f"DATABASE=SIGE_DataMart;"
        f"UID=readonly_emtp;"
        f"PWD={password}"
    )
    return conn
```
- ✅ **Es el estándar** del Gobierno de Chile
- ✅ TI ya tiene experiencia otorgando estos accesos
- ✅ Datos actualizados según frecuencia de réplica
- ⚠️ Requiere solicitud formal (2-4 semanas)
- 📄 **Ver:** `docs/PENDIENTE_ACTUALIZACION_DATOS.md` para solicitud completa

**Opción 2: SharePoint/OneDrive (Alternativa - 60%)**
```python
# Si TI prefiere no dar acceso a BD
from office365.sharepoint.client_context import ClientContext

def descargar_desde_sharepoint():
    ctx = ClientContext(site_url).with_credentials(credentials)
    file = ctx.web.get_file_by_server_relative_url('/datos/matricula.csv')
    file.download(open('data/raw/matricula.csv', 'wb'))
```
- ✅ Automático completamente
- ✅ Institucional, respaldado por MINEDUC
- ⚠️ Requiere credenciales de servicio
- ⚠️ Requiere coordinar con TI MINEDUC

**Opción 3: SFTP/FTP del MINEDUC (Si está disponible)**
```python
# Si MINEDUC tiene servidor FTP con datos
import paramiko

def descargar_desde_ftp():
    ssh = paramiko.SSHClient()
    ssh.connect('ftp.mineduc.cl', username='user', password='pass')
    sftp = ssh.open_sftp()
    sftp.get('/datos/matricula_2025.csv', 'data/raw/matricula_2025.csv')
```
- ✅ Estándar y confiable
- ⚠️ Requiere credenciales FTP
- ⚠️ Requiere que MINEDUC mantenga servidor FTP

**Opción 1: Manual (Temporal - Solo mientras se aprueba SQL Server)**
- Usar solo 1-3 meses mientras TI procesa solicitud
- TI descarga CSVs semanalmente

**Decisión Requerida:**

**🎯 ACCIÓN INMEDIATA RECOMENDADA:**

1. **Enviar solicitud formal a TI MINEDUC**
   - Usar plantilla en `docs/PENDIENTE_ACTUALIZACION_DATOS.md`
   - Solicitar: "Usuario read-only en réplica SQL Server del SIGE"
   - Especificar: Vistas de matrícula, egresados, establecimientos EMTP
   - Plazo esperado: 2-4 semanas

2. **Mientras se procesa solicitud:**
   - Mantener proceso manual temporal
   - Preparar código de conexión SQL Server
   - Identificar vistas/tablas necesarias

3. **Tras recibir credenciales:**
   - Implementar script de extracción automática (4-6 horas)
   - Probar en desarrollo (1 semana)
   - Activar cron job semanal
   - Monitorear primera semana

**Documentación completa:**
- 📄 `docs/PENDIENTE_ACTUALIZACION_DATOS.md` (20 páginas)
  - Solicitud formal lista para enviar
  - Código de implementación completo
  - Preguntas para reunión con TI
  - Contexto real del MINEDUC
   - Configurar credenciales seguras
   - Implementar logging y alertas
   - Documentar proceso completo

**Mitigación Temporal (Mientras se define):**
- Script `actualizar_datos_semanal.py` procesa archivos en `data/raw/`
- TI coloca archivos manualmente cada semana
- Logs detallados en `logs/app.log`
- Alerta si datos >8 días sin actualizar (implementar)

**Responsable de Definición:** Jefatura EMTP + TI MINEDUC  
**Fecha Límite Recomendada:** Antes del despliegue en producción  
**Criticidad:** 🔴 Alta - Afecta utilidad del sistema

### Riesgo 2: Cambios en Fuente de Datos

**Probabilidad:** Baja (1-2 veces al año)  
**Impacto:** Alto (requiere modificar código)

**Mitigación:**
- Documentar estructura actual de datos en `docs/ESTRUCTURA_DATOS.md`
- Mantener contacto con desarrollador original
- Tener freelancer de respaldo identificado

### Riesgo 3: Fallas de Hardware/Servidor

**Probabilidad:** Baja  
**Impacto:** Alto (servicio no disponible)

**Mitigación:**
- Backups automáticos diarios
- Documentación de proceso de restauración
- Docker permite migrar fácilmente a otro servidor

---

## 5. Recomendaciones para Sostenibilidad Total

### 5.1 Implementar Monitoreo Automático (30 min desarrollo)

```python
# scripts/healthcheck.py
import requests
import smtplib
from email.mime.text import MIMEText

def verificar_app():
    try:
        r = requests.get("http://localhost:8051", timeout=10)
        if r.status_code != 200:
            enviar_alerta("App no responde correctamente")
    except Exception as e:
        enviar_alerta(f"App caída: {e}")

def enviar_alerta(mensaje):
    # Configurar según sistema de alertas institucional
    msg = MIMEText(mensaje)
    msg['Subject'] = 'ALERTA: Visualizador EMTP'
    msg['From'] = 'sistema@mineduc.cl'
    msg['To'] = 'CONFIGURAR_EMAIL_SOPORTE'  # Definir email de soporte real
    
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

if __name__ == '__main__':
    verificar_app()
```

**Configurar en crontab:**
```bash
# Ejecutar cada 5 minutos
*/5 * * * * /path/to/venv/bin/python /path/to/scripts/healthcheck.py
```

### 5.2 Crear Checklist Visual para TI

Archivo: `docs/CHECKLIST_TI.md`

```markdown
# ✅ Checklist Semanal TI - Visualizador EMTP

**Semana del:** __________  
**Ejecutado por:** __________

## Verificación de Sistema

- [ ] App corriendo: `curl http://localhost:8051`
- [ ] Sin errores en logs: `tail -50 logs/app.log | grep ERROR`
- [ ] Espacio en disco >20%: `df -h`
- [ ] Backup realizado: `ls -lth backups/ | head`

## Verificación de Datos

- [ ] Datos actualizados esta semana: `ls -lth data/processed/`
- [ ] Cron job activo: `systemctl status cron`

## Acciones Correctivas (si aplica)

- [ ] Reiniciar app: `systemctl restart visualizador-emtp`
- [ ] Limpiar logs antiguos: `find logs/ -mtime +90 -delete`
- [ ] Contactar desarrollador: _______________

**Notas:** 
_________________________________________________
_________________________________________________
```

### 5.3 Contactos de Emergencia

Agregar en README y documentación:

```markdown
## 🆘 Soporte y Contactos

### Desarrollador
**Andrés Lazcano**  
Email: ext.andres.lazcano@mineduc.cl  
GitHub: @andreslazcano-bit

---

### 5.4 Backup Automático a Cloud (1 hora desarrollo)

```bash
#!/bin/bash
# scripts/backup_cloud.sh

# Backup de base de datos y datos procesados
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/

# Subir a S3 o similar
aws s3 cp backup_$(date +%Y%m%d).tar.gz s3://mineduc-backups/visualizador/

# Limpiar backups locales antiguos
find backups/ -name "*.tar.gz" -mtime +30 -delete

echo "Backup completado: $(date)" >> logs/backup.log
```

**Configurar en crontab:**
```bash
# Backup diario a las 2 AM
0 2 * * * /path/to/scripts/backup_cloud.sh
```

---

## 6. Plan de Transición (Recomendado)

### Antes de Transferir a TI

#### Sesión 1: Capacitación Operacional (2 horas)

**Agenda:**
1. **Demostración de la aplicación** (30 min)
   - Navegar por todos los módulos
   - Mostrar modo Usuario vs Admin
   - Explicar funcionalidad de cada dashboard

2. **Procedimientos básicos** (45 min)
   - Cómo iniciar/detener la app
   - Cómo ver logs
   - Cómo hacer backup manual
   - Cómo acceder al servidor

3. **Troubleshooting práctico** (30 min)
   - Simular app caída → reiniciar
   - Simular datos desactualizados → verificar cron
   - Simular usuario bloqueado → resetear en DB

4. **Preguntas y práctica** (15 min)

#### Sesión 2: Documentación y Escalamiento (1 hora)

**Agenda:**
1. **Recorrido por documentación** (20 min)
   - Dónde está cada manual
   - Cómo buscar información
   - Índice de documentos

2. **Cuándo contactar desarrollador** (20 min)
   - Problemas que TI puede resolver
   - Problemas que requieren desarrollador
   - Cómo reportar un issue en GitHub

3. **Procedimientos de emergencia** (20 min)
   - Script de "reset completo"
   - Cómo restaurar desde backup
   - A quién contactar en cada caso

### Material de Entrega

1. **USB con:**
   - Copia completa del repositorio
   - Toda la documentación en PDF
   - Backups de las últimas 4 semanas
   - Script de instalación rápida

2. **Documentos impresos:**
   - Checklist semanal TI
   - Top 5 problemas y soluciones
   - Contactos de emergencia
   - Credenciales de acceso (sobre sellado)

3. **Accesos:**
   - Credenciales del servidor
   - Acceso al repositorio GitHub
   - Credenciales admin del sistema
   - Acceso a backups en cloud (si aplica)

---

## 7. Script de "Botón de Pánico"

Para casos de emergencia crítica:

```bash
#!/bin/bash
# scripts/reset_completo.sh
# USO: Solo en emergencia cuando todo falla

echo "⚠️  ADVERTENCIA: Este script reiniciará el sistema completo"
echo "Presiona Ctrl+C para cancelar, Enter para continuar..."
read

echo "1. Deteniendo aplicación..."
docker-compose down 2>/dev/null || systemctl stop visualizador-emtp

echo "2. Creando backup de seguridad..."
mkdir -p backups/emergency
cp -r data/ backups/emergency/data_$(date +%Y%m%d_%H%M%S)
cp -r logs/ backups/emergency/logs_$(date +%Y%m%d_%H%M%S)

echo "3. Restaurando código desde GitHub..."
git fetch origin
git reset --hard origin/main

echo "4. Reinstalando dependencias..."
source venv/bin/activate
pip install -r requirements.txt

echo "5. Reiniciando aplicación..."
docker-compose up -d || systemctl start visualizador-emtp

echo "✅ Reset completo finalizado"
echo "📋 Backups guardados en: backups/emergency/"
echo "🔍 Verifica en: http://localhost:8051"
```

---

## 8. Matriz de Decisión para TI

| Situación | ¿TI puede resolver? | ¿Requiere desarrollador? | Prioridad |
|-----------|---------------------|--------------------------|-----------|
| App no carga | ✅ Sí - Reiniciar servicio | ❌ No | 🔴 Alta |
| Datos desactualizados | ✅ Sí - Verificar cron | ⚠️ Solo si estructura cambió | 🟡 Media |
| Usuario olvidó contraseña | ✅ Sí - Reset en DB | ❌ No | 🟢 Baja |
| Error en logs | ⚠️ Depende del error | ✅ Sí, si persiste | 🟡 Media |
| Agregar nuevo dashboard | ❌ No | ✅ Sí | 🟢 Baja |
| Cambió formato MINEDUC | ❌ No | ✅ Sí | 🔴 Alta |
| Servidor sin espacio | ✅ Sí - Limpiar logs | ❌ No | 🔴 Alta |
| Migrar a nuevo servidor | ⚠️ Con guía | ⚠️ Recomendado | 🟡 Media |

---

## 9. Indicadores de Éxito

Para medir si el proyecto es sostenible:

### KPIs de Operación (Medir mensualmente)

1. **Disponibilidad del servicio:** >99% (objetivo)
2. **Tiempo de resolución de incidentes:** <2 horas
3. **Actualización de datos:** 100% en plazo
4. **Incidentes que requieren desarrollador:** <1 por mes

### Señales de Alerta

🚨 **Contactar desarrollador si:**
- Más de 3 incidentes no resueltos en 1 semana
- Datos sin actualizar por más de 10 días
- Errores recurrentes en logs
- Solicitudes de nuevas funcionalidades acumuladas

---

## 10. Conclusiones

### ✅ El proyecto ES sostenible con solo TI para:

- ✅ Operación diaria y monitoreo
- ✅ Reinicio y troubleshooting básico
- ✅ Gestión de usuarios
- ✅ Backups y restauración
- ✅ Mantenimiento de servidor

### ⚠️ Se necesita desarrollador para:

- ⚠️ Nuevas funcionalidades
- ⚠️ Cambios en lógica de negocio
- ⚠️ Modificaciones en estructura de datos
- ⚠️ Integraciones con otros sistemas
- ⚠️ Problemas complejos no documentados

### 🎯 Recomendación Final

**El proyecto está bien preparado para sostenibilidad operacional.**

**Para sostenibilidad completa, implementar:**

1. ✅ Monitoreo automático con alertas (30 min)
2. ✅ Checklist visual para TI (15 min)
3. ✅ Contacto de freelancer de respaldo (identificar ya)
4. ✅ Backup automático a cloud (1 hora)
5. ✅ Sesión de capacitación con TI (3 horas)

**Nivel de criticidad del desarrollador original:**
- Para **mantenimiento:** 2/10 (baja dependencia)
- Para **evolución:** 9/10 (alta dependencia)

---

## Anexos

### A. Top 5 Problemas y Soluciones

#### 1. "La aplicación no carga"

**Síntomas:** Navegador muestra error 404 o no carga

**Solución:**
```bash
# Verificar si está corriendo
curl http://localhost:8051

# Si no responde, reiniciar
systemctl restart visualizador-emtp

# O con Docker
docker-compose restart

# Verificar que funcionó
curl http://localhost:8051
```

#### 2. "Los datos están desactualizados"

**Síntomas:** Dashboard muestra fecha antigua

**Solución:**
```bash
# Ver última actualización
ls -lth data/processed/ | head

# Verificar cron job
crontab -l | grep actualizar

# Ejecutar manualmente
source venv/bin/activate
python scripts/actualizar_datos_semanal.py

# Verificar logs
tail -f logs/app.log
```

#### 3. "Usuario no puede entrar"

**Síntomas:** "Credenciales inválidas" al hacer login

**Solución:**
```bash
# Verificar usuario existe
sqlite3 data/users.db "SELECT username, is_active FROM users;"

# Si está inactivo, activar
sqlite3 data/users.db "UPDATE users SET is_active=1 WHERE username='usuario';"

# Para resetear contraseña, contactar desarrollador
```

#### 4. "Errores en los logs"

**Síntomas:** Líneas con ERROR en logs/app.log

**Solución:**
```bash
# Ver últimos errores
tail -100 logs/app.log | grep ERROR

# Si es error de datos:
# → Verificar archivos en data/processed/

# Si es error de código:
# → Copiar error completo
# → Enviar a ext.andres.lazcano@mineduc.cl

# Si persiste:
# → Reiniciar aplicación
```

#### 5. "Se requiere nueva funcionalidad"

**Síntomas:** Usuario solicita "Quiero un nuevo dashboard de X"

**Solución:**
```
1. Documentar el requerimiento
2. Estimar complejidad (consultar con Andrés)
3. Opciones:
   a) Desarrollador original (consulta puntual)
   b) Freelancer (desarrollo completo)
   c) Proveedor externo (proyecto grande)

NO intentar modificar código sin experiencia Python
```

### B. Comandos Útiles de Referencia Rápida

```bash
# === OPERACIÓN ===

# Iniciar app
systemctl start visualizador-emtp
# o: docker-compose up -d

# Detener app
systemctl stop visualizador-emtp
# o: docker-compose down

# Reiniciar app
systemctl restart visualizador-emtp
# o: docker-compose restart

# Ver estado
systemctl status visualizador-emtp
# o: docker-compose ps

# === LOGS ===

# Ver logs en tiempo real
tail -f logs/app.log

# Ver últimos 100 líneas
tail -100 logs/app.log

# Buscar errores
grep ERROR logs/app.log

# Ver logs por fecha
grep "2025-11-17" logs/app.log

# === DATOS ===

# Listar archivos de datos
ls -lth data/processed/

# Ver tamaño de datos
du -sh data/

# Verificar última actualización
stat data/processed/matricula_completa.csv

# === BACKUPS ===

# Backup manual
cp data/users.db backups/users_$(date +%Y%m%d).db

# Restaurar backup
cp backups/users_20251117.db data/users.db

# Listar backups
ls -lth backups/

# === USUARIOS ===

# Ver todos los usuarios
sqlite3 data/users.db "SELECT * FROM users;"

# Crear usuario (usar interfaz web preferentemente)

# Desactivar usuario
sqlite3 data/users.db "UPDATE users SET is_active=0 WHERE username='usuario';"

# === SISTEMA ===

# Ver espacio en disco
df -h

# Ver uso de memoria
free -h

# Ver procesos Python
ps aux | grep python

# Matar proceso si es necesario
kill -9 <PID>
```

---

**Documento creado:** 17 de Noviembre 2025  
**Última actualización:** 17 de Noviembre 2025  
**Versión:** 1.0  
**Contacto:** ext.andres.lazcano@mineduc.cl
