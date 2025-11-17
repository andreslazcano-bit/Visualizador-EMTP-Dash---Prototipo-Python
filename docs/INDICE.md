# 📚 Índice de Documentación - Visualizador EMTP

**Versión:** 2.0  
**Última Actualización:** 17 de Noviembre 2025

Este documento sirve como índice central para toda la documentación del proyecto.

---

## 📋 Índice General

### 📘 Para Dirección y Jefaturas
- [**Presentación Ejecutiva**](PRESENTACION_JEFATURA_ASPECTOS_CLAVE.md) - Aspectos clave para decisiones estratégicas
  - 📄 [Versión Word](PRESENTACION_JEFATURA_ASPECTOS_CLAVE.docx) (42 KB)
- [**Resumen del Proyecto**](../RESUMEN_PROYECTO.md) - Vista general del Visualizador EMTP
- [**Roadmap**](ROADMAP.md) - Plan de desarrollo y próximas funcionalidades

---

### 🔧 Para TI (Despliegue y Mantenimiento)
- [**Manual de Despliegue**](MANUAL_DESPLIEGUE.md) ⭐ **ESENCIAL**
  - Instalación paso a paso (sin necesidad de conocimientos Python)
  - Configuración del servidor
  - Primera ejecución
  - Configuración como servicio (Linux/Windows)
  - Troubleshooting

- [**Manual de Mantenimiento**](MANUAL_MANTENIMIENTO.md) ⭐ **ESENCIAL**
  - Verificaciones diarias/semanales/mensuales
  - Procedimientos de backup y restauración
  - Gestión de usuarios desde terminal
  - Monitoreo de logs
  - Rotación de logs
  - Actualización del sistema
  - Errores comunes y soluciones
  - Procedimientos de emergencia

- [**Guía Rápida**](GUIA_RAPIDA.md) ⭐ **REFERENCIA RÁPIDA**
  - Comandos esenciales
  - Troubleshooting rápido
  - Checklists de mantenimiento
  - Contactos de emergencia

---

### 👥 Para Usuarios Finales (Secretaría, Analistas)
- [**Manual de Usuario**](MANUAL_USUARIO.md) ⭐ **ESENCIAL**
  - Acceso al sistema
  - Navegación básica
  - Uso de dashboards
  - Aplicación de filtros
  - Exportación de datos
  - Funciones de administrador (gestión de usuarios + auditoría)
  - Preguntas frecuentes

- [**Guía Rápida**](GUIA_RAPIDA.md)
  - Tareas comunes en 5 pasos
  - Atajos de teclado
  - Contactos de soporte

---

### 🏗️ Para Desarrolladores
- [**Arquitectura del Sistema**](ARQUITECTURA.md)
  - Diseño técnico completo
  - Componentes principales
  - Flujo de datos
  - Stack tecnológico

- [**Sistema de Usuarios y Auditoría**](SISTEMA_USUARIOS_AUDITORIA.md)
  - Implementación técnica
  - Estructura de base de datos
  - Callbacks y componentes
  - Código de ejemplo

- [**Integración Completada**](INTEGRACION_COMPLETADA.md) ⭐ **NUEVO**
  - Resumen de todos los componentes integrados
  - Archivos creados/modificados
  - Pruebas realizadas
  - Estado del proyecto
  - Próximos pasos

- [**Migración de Datos**](MIGRACION_DATOS.md)
  - Proceso de migración desde RDS
  - Scripts de conversión
  - Conexión a SQL Server

- [**Actualización Automática**](ACTUALIZACION_AUTOMATICA.md)
  - Sistema de actualización semanal
  - Configuración de cron jobs
  - Validación de datos

---

## 📁 Estructura de Carpetas

```
docs/
├── INDICE.md                              ← Este archivo
│
├── 📊 DIRECCIÓN Y JEFATURAS
│   ├── PRESENTACION_JEFATURA_ASPECTOS_CLAVE.md
│   ├── PRESENTACION_JEFATURA_ASPECTOS_CLAVE.docx
│   ├── ROADMAP.md
│   └── ../RESUMEN_PROYECTO.md
│
├── 🔧 TI (OPERACIONES)
│   ├── MANUAL_DESPLIEGUE.md              ← Instalación
│   ├── MANUAL_MANTENIMIENTO.md           ← Día a día
│   └── GUIA_RAPIDA.md                    ← Referencia rápida
│
├── 👥 USUARIOS FINALES
│   ├── MANUAL_USUARIO.md                 ← Uso del sistema
│   └── GUIA_RAPIDA.md                    ← Tareas comunes
│
└── 🏗️ DESARROLLADORES
    ├── ARQUITECTURA.md                   ← Diseño técnico
    ├── SISTEMA_USUARIOS_AUDITORIA.md     ← Gestión usuarios + auditoría
    ├── INTEGRACION_COMPLETADA.md         ← Estado del proyecto
    ├── MIGRACION_DATOS.md                ← Migración de datos
    └── ACTUALIZACION_AUTOMATICA.md       ← Updates semanales
```

---

## 🎯 Guía de Lectura por Rol

### Si eres **Director o Jefe**:
1. Leer [PRESENTACION_JEFATURA_ASPECTOS_CLAVE.md](PRESENTACION_JEFATURA_ASPECTOS_CLAVE.md)
2. Revisar [ROADMAP.md](ROADMAP.md) para conocer el plan futuro

### Si eres **Administrador de TI** (y debes instalar el sistema):
1. ⭐ **LEER PRIMERO:** [MANUAL_DESPLIEGUE.md](MANUAL_DESPLIEGUE.md)
2. Configurar servidor siguiendo los pasos
3. Tener a mano [GUIA_RAPIDA.md](GUIA_RAPIDA.md) para consultas rápidas
4. Luego leer [MANUAL_MANTENIMIENTO.md](MANUAL_MANTENIMIENTO.md) para operaciones diarias

### Si eres **Administrador de TI** (y debes mantener el sistema):
1. ⭐ **LEER PRIMERO:** [MANUAL_MANTENIMIENTO.md](MANUAL_MANTENIMIENTO.md)
2. Configurar backups automáticos
3. Revisar checklists en [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
4. Tener a mano contactos de soporte

### Si eres **Usuario Final** (Secretaría, Analista):
1. ⭐ **LEER PRIMERO:** [MANUAL_USUARIO.md](MANUAL_USUARIO.md)
2. Practicar con el sistema (modo usuario sin login)
3. Consultar [GUIA_RAPIDA.md](GUIA_RAPIDA.md) para tareas específicas
4. Contactar soporte si tienes dudas

### Si eres **Administrador del Sistema** (gestión de usuarios):
1. Leer sección "Funciones de Administrador" en [MANUAL_USUARIO.md](MANUAL_USUARIO.md)
2. Practicar creación de usuarios
3. Revisar auditoría semanalmente

### Si eres **Desarrollador** (continuarás el proyecto):
1. Leer [ARQUITECTURA.md](ARQUITECTURA.md)
2. Revisar [INTEGRACION_COMPLETADA.md](INTEGRACION_COMPLETADA.md)
3. Estudiar [SISTEMA_USUARIOS_AUDITORIA.md](SISTEMA_USUARIOS_AUDITORIA.md)
4. Revisar código fuente en `src/`

---

## 📏 Estadísticas de Documentación

| Tipo | Archivos | Páginas Aprox. |
|------|----------|----------------|
| **Dirección** | 3 | 50 |
| **TI** | 3 | 66 |
| **Usuarios** | 2 | 36 |
| **Desarrolladores** | 5 | 80 |
| **TOTAL** | 13 | ~230 |

---

## 🔄 Actualizaciones Recientes

### Noviembre 2025 (v2.0)
- ✅ Agregado sistema de gestión de usuarios
- ✅ Agregado sistema de auditoría
- ✅ Creados manuales de despliegue y mantenimiento
- ✅ Creado manual de usuario completo
- ✅ Creada guía rápida de referencia
- ✅ Documentación de sostenibilidad para TI

---

## 📞 Contactos para Documentación

### Consultas sobre Manuales de Usuario
**Secretaría EMTP**  
📧 secretaria.emtp@mineduc.cl

### Consultas Técnicas (TI)
**Soporte TI**  
📧 ti@mineduc.cl  
📞 +56 2 XXXX XXXX

### Consultas de Desarrollo
**Desarrollador Original**  
📧 andres.lazcano@mineduc.cl  
📞 +56 9 XXXX XXXX

---

## 📝 Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | Nov 2025 | Agregados manuales de sostenibilidad, gestión usuarios, auditoría |
| 1.0 | Oct 2025 | Documentación técnica inicial |

---

**Última actualización:** 17 de Noviembre 2025  
**Mantenedor:** Andrés Lazcano

---

💡 **Tip:** Marcar este documento como favorito para acceso rápido a toda la documentación.
