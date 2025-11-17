# Checklist de Transición - Visualizador EMTP

**Para:** Equipo TI MINEDUC  
**De:** Andrés Lazcano  
**Fecha:** 17 de Noviembre 2025

---

## ✅ Checklist Pre-Transición

### Capacitación (3 horas total)

- [ ] **Sesión 1: Operación Básica** (2 horas)
  - [ ] Demostrar navegación en la app (todos los módulos)
  - [ ] Mostrar cómo iniciar/detener servicio
  - [ ] Practicar lectura de logs
  - [ ] Realizar backup manual
  - [ ] Simular y resolver 3 problemas comunes

- [ ] **Sesión 2: Documentación y Escalamiento** (1 hora)
  - [ ] Recorrido por carpeta `docs/`
  - [ ] Explicar cuándo contactar desarrollador
  - [ ] Mostrar procedimientos de emergencia

### Material Entregado

- [ ] **USB con:**
  - [ ] Copia completa del repositorio
  - [ ] PDFs de toda la documentación
  - [ ] Backups de últimas 4 semanas
  - [ ] Script de instalación rápida

- [ ] **Documentos impresos:**
  - [ ] Checklist semanal TI (esta hoja)
  - [ ] Top 5 problemas y soluciones
  - [ ] Contactos de emergencia
  - [ ] Credenciales (sobre sellado)

- [ ] **Accesos configurados:**
  - [ ] Credenciales del servidor
  - [ ] Acceso GitHub (read-only mínimo)
  - [ ] Usuario admin del sistema
  - [ ] Acceso a logs remotos (si aplica)

---

## 📋 Checklist Semanal de Operación

**Semana del:** __________  
**Responsable:** __________

### Lunes: Verificación Inicial

- [ ] App corriendo: `curl http://localhost:8051`
- [ ] Sin errores críticos: `tail -50 logs/app.log | grep ERROR`
- [ ] Datos actualizados: `ls -lth data/processed/ | head`

### Miércoles: Mantenimiento

- [ ] Espacio en disco >20%: `df -h`
- [ ] Backup semanal: `cp data/users.db backups/users_$(date +%Y%m%d).db`
- [ ] Limpiar logs antiguos >90 días: `find logs/ -name "*.log" -mtime +90 -delete`

### Viernes: Revisión

- [ ] Revisar logs de la semana
- [ ] Verificar actualizaciones pendientes
- [ ] Documentar incidentes (si hubo)

### Mensual

- [ ] Verificar backups automáticos funcionando
- [ ] Revisar uso de recursos (CPU/RAM)
- [ ] Actualizar esta checklist con nuevos aprendizajes

---

## 🆘 Guía Rápida de Problemas

### Problema 1: App no carga

```bash
# Paso 1: Verificar
curl http://localhost:8051

# Paso 2: Si no responde, reiniciar
systemctl restart visualizador-emtp

# Paso 3: Verificar logs
tail -20 logs/app.log
```

**Si persiste:** Contactar Andrés Lazcano

### Problema 2: Datos desactualizados

```bash
# Ver última actualización
ls -lth data/processed/

# Si >8 días, verificar cron
crontab -l | grep actualizar

# Ejecutar manualmente
source venv/bin/activate
python scripts/actualizar_datos_semanal.py
```

**Si falla:** Revisar logs, contactar desarrollador

### Problema 3: Usuario no puede entrar

```bash
# Verificar usuario existe y está activo
sqlite3 data/users.db "SELECT username, is_active FROM users;"

# Activar si está desactivado
sqlite3 data/users.db "UPDATE users SET is_active=1 WHERE username='usuario';"
```

**Para reset de contraseña:** Contactar Andrés Lazcano

### Problema 4: Errores en logs

```bash
# Ver errores recientes
tail -100 logs/app.log | grep ERROR

# Copiar error completo y enviar a:
# ext.andres.lazcano@mineduc.cl
```

### Problema 5: Servidor sin espacio

```bash
# Ver uso de disco
df -h

# Limpiar logs antiguos
find logs/ -mtime +30 -delete

# Limpiar backups antiguos
find backups/ -mtime +60 -delete
```

---

## 📞 Contactos de Emergencia

### Desarrollador
- **Nombre:** Andrés Lazcano
- **Email:** ext.andres.lazcano@mineduc.cl
- **GitHub:** @andreslazcano-bit

---

## 🚀 Comandos de Uso Frecuente

### Operación Básica

```bash
# Iniciar
systemctl start visualizador-emtp

# Detener
systemctl stop visualizador-emtp

# Reiniciar
systemctl restart visualizador-emtp

# Ver estado
systemctl status visualizador-emtp
```

### Logs

```bash
# Ver en tiempo real
tail -f logs/app.log

# Buscar errores
grep ERROR logs/app.log

# Ver logs de hoy
grep "$(date +%Y-%m-%d)" logs/app.log
```

### Backups

```bash
# Backup manual
cp data/users.db backups/users_$(date +%Y%m%d).db

# Listar backups
ls -lth backups/

# Restaurar
cp backups/users_20251117.db data/users.db
```

### Datos

```bash
# Ver archivos de datos
ls -lth data/processed/

# Ver tamaño
du -sh data/

# Última modificación
stat data/processed/matricula_completa.csv
```

---

## 🔴 Botón de Pánico (Emergencia)

**Solo usar si TODO falla y no hay otra opción:**

```bash
# Ejecutar script de reset completo
/path/to/scripts/reset_completo.sh

# Esto hará:
# 1. Backup de emergencia
# 2. Reset del código desde GitHub
# 3. Reinstalación de dependencias
# 4. Reinicio de la aplicación
```

**⚠️ IMPORTANTE:** Avisar inmediatamente a Andrés después de usar.

---

## 📊 Métricas de Éxito

Medir mensualmente:

- [ ] **Disponibilidad:** >99% del tiempo
- [ ] **Tiempo resolución incidentes:** <2 horas
- [ ] **Actualización datos:** 100% en plazo
- [ ] **Incidentes requiriendo desarrollador:** <1 por mes

Si alguna métrica falla consistentemente, revisar con desarrollador.

---

## 📝 Notas y Aprendizajes

Use este espacio para documentar nuevos problemas y soluciones:

**Fecha: ________**  
Problema: ____________________________________  
Solución: ____________________________________  
_______________________________________________

**Fecha: ________**  
Problema: ____________________________________  
Solución: ____________________________________  
_______________________________________________

**Fecha: ________**  
Problema: ____________________________________  
Solución: ____________________________________  
_______________________________________________

---

## ✅ Confirmación de Transición

- [ ] Capacitación completada
- [ ] Material entregado
- [ ] Accesos configurados
- [ ] Primera semana supervisada
- [ ] TI puede operar independientemente

**Fecha de transición:** __________  
**Firma TI:** __________  
**Firma Desarrollador:** __________

---

**Documento versión:** 1.0  
**Última actualización:** 17 de Noviembre 2025  
**Próxima revisión:** __________
