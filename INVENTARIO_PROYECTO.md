# 📋 INVENTARIO DEL PROYECTO - VISUALIZADOR EMTP

**Fecha de organización**: Noviembre 2025  
**Versión**: 2.0 (Python/Dash)

---

## 📁 ESTRUCTURA ACTUALIZADA DEL PROYECTO

### ✅ ARCHIVOS EN USO (en GitHub)

```
VisualizadorEMTP-Dash/
├── app_v2.py                    # ✅ Aplicación principal (EN USO)
├── requirements.txt             # ✅ Dependencias Python (EN USO)
├── README.md                    # ✅ Documentación principal (EN USO)
├── .gitignore                   # ✅ Configuración git (ACTUALIZADO)
├── .env.example                 # ✅ Plantilla de variables de entorno
│
├── assets/                      # ✅ Recursos estáticos (EN USO)
│   ├── custom.css              
│   ├── navigation.js           
│   └── theme.js                
│
├── config/                      # ✅ Configuración (EN USO)
│   ├── __init__.py
│   └── settings.py             
│
├── data/                        # ✅ Datos (EN USO)
│   ├── processed/              # CSV con datos simulados
│   │   ├── matricula_simulada.csv
│   │   ├── matricula_comunal_simulada.csv
│   │   ├── egresados_simulados.csv
│   │   ├── titulacion_simulada.csv
│   │   ├── establecimientos_simulados.csv
│   │   └── docentes_simulados.csv
│   └── geographic/             # Datos geográficos (cacheados desde GitHub)
│
├── docs/                        # ✅ Documentación técnica (EN USO)
│   ├── README.md               # Guía de navegación
│   ├── PROPUESTA_TECNICA_INTEGRAL.md
│   └── RESUMEN_EJECUTIVO.md
│
├── scripts/                     # ✅ Scripts de utilidad (EN USO)
│   └── generate_comunal_data.py
│
├── src/                         # ✅ Código fuente (EN USO)
│   ├── __init__.py
│   ├── callbacks/              # Lógica de interacción
│   │   ├── __init__.py
│   │   ├── auth_callbacks.py
│   │   ├── sidebar_callbacks.py
│   │   ├── mapas_callbacks.py
│   │   └── theme_callbacks.py
│   ├── layouts/                # Interfaces visuales
│   │   ├── __init__.py
│   │   ├── login_layout.py
│   │   ├── welcome_screen.py
│   │   ├── sidebar_layout_clean.py
│   │   ├── mapas.py
│   │   └── real_data_content.py
│   └── utils/                  # Utilidades
│       ├── __init__.py
│       ├── auth.py
│       ├── helpers.py
│       └── rate_limiter.py
│
├── logs/                        # Logs de la aplicación (generados)
└── reports/                     # Reportes (preparado para futuro)
```

---

### 🗄️ ARCHIVOS ARCHIVADOS (NO en GitHub)

```
_archive/                        # 📁 Archivos obsoletos y de referencia
├── shiny-obsoleto/             # Versión Shiny/R anterior (OBSOLETO)
│   ├── app.R
│   ├── minuta_establecimiento.Rmd
│   └── resumen_territorio.Rmd
│
└── docs-referencia/            # Documentos de referencia (OBSOLETO)
    ├── 20250922_Minuta Propuesta de Proyecto Power BI_V3_CON_BRECHAS.docx
    ├── Centralizacion Proyectos Gestión - Propuesta.docx
    ├── PROPUESTA_TECNICA_INTEGRAL.docx
    ├── RESUMEN_EJECUTIVO.docx
    ├── centralizacion_extracted.txt
    ├── minuta_powerbi_extracted.txt
    └── plantilla_minuta.docx
```

---

### 📁 DOCUMENTOS DE PLANIFICACIÓN (NO en GitHub)

```
_docs-planificacion/            # 📁 Documentos estratégicos personales
├── RESUMEN_EJECUTIVO_JEFATURA.md
├── DEFINICIONES_PARA_PRODUCCION.md
├── PRESENTACION_JEFATURA.md
├── MEMO_JEFE_TI.md
├── INDICE.md
├── README_NUEVOS_DOCS.md
└── COMO_USAR_ESTOS_DOCUMENTOS.md
```

**Estos documentos son para uso interno y planificación personal. NO se suben a GitHub.**

---

## 🔧 ARCHIVOS DE CONFIGURACIÓN

| Archivo | Estado | Propósito |
|---------|--------|-----------|
| `.gitignore` | ✅ Actualizado | Excluye archivos personales, logs, datos grandes |
| `.env` | ⚠️ Local (no en git) | Variables de entorno (credenciales) |
| `.env.example` | ✅ En GitHub | Plantilla de variables de entorno |
| `requirements.txt` | ✅ En GitHub | Dependencias Python |
| `runtime.txt` | ✅ En GitHub | Versión de Python para deployment |
| `Procfile` | ✅ En GitHub | Configuración para Heroku |

---

## 📊 ESTADÍSTICAS DEL PROYECTO

### Código Python:
- **Archivos .py**: 20+
- **Líneas de código**: ~5,000+
- **Módulos principales**: 4 (callbacks, layouts, utils, config)

### Datos:
- **Registros totales**: 178,700+
- **Regiones**: 16
- **Comunas**: 345
- **Período**: 2015-2024 (10 años)

### Documentación:
- **Docs técnicos en GitHub**: 3 archivos
- **Docs de planificación (locales)**: 7 archivos
- **Archivos archivados**: 10+ archivos

---

## 🚫 LO QUE NO SE SUBE A GITHUB

Según `.gitignore` actualizado:

1. **Documentos de planificación**: `/_docs-planificacion/`
2. **Archivos obsoletos**: `/_archive/`
3. **Logs**: `*.log`, `run_app.log`
4. **Variables de entorno**: `.env`
5. **Datos grandes**: `matricula_comunal_simulada.csv` (142k registros)
6. **Archivos Word**: `*.docx`
7. **Archivos R obsoletos**: `*.R`, `*.Rmd`
8. **Cache Python**: `__pycache__/`, `*.pyc`
9. **Virtual environment**: `venv/`

---

## ✅ CAMBIOS REALIZADOS EN REORGANIZACIÓN

### Movimientos de archivos:

1. **Archivos Shiny/R obsoletos** → `_archive/shiny-obsoleto/`
   - `app.R`
   - `minuta_establecimiento.Rmd`
   - `resumen_territorio.Rmd`

2. **Documentos Word de referencia** → `_archive/docs-referencia/`
   - Minutas PowerBI
   - Propuestas antiguas en Word
   - Archivos extracted.txt

3. **Documentos de planificación** → `_docs-planificacion/`
   - 7 documentos estratégicos para toma de decisiones
   - Presentaciones para jefatura
   - Memorándum para TI

### Actualizaciones de configuración:

1. **`.gitignore`**: Actualizado para excluir:
   - `_docs-planificacion/`
   - `_archive/`
   - Logs y temporales
   - Archivos obsoletos

2. **`docs/README.md`**: Actualizado con nueva estructura

---

## 🎯 PRÓXIMOS PASOS

### Para mantener orden:

1. **Documentos nuevos de planificación**: Guardar en `_docs-planificacion/`
2. **Archivos obsoletos**: Mover a `_archive/` apropiado
3. **Documentación técnica**: Solo en `docs/` y debe estar en GitHub
4. **Código activo**: Solo en `src/`, `assets/`, `config/`

### Para colaboradores:

- Clonar repo solo obtendrá archivos necesarios
- Documentos de planificación están solo en tu máquina local
- Archivo de referencia está solo en tu máquina local

---

## 📞 CONTACTO

**Responsable del proyecto**: Andrés Lazcano  
**GitHub**: github.com/andreslazcano-bit/Visualizador-EMTP-Dash  
**Última organización**: Noviembre 2025

---

**Este inventario se actualizará cada vez que se reorganice el proyecto.**
