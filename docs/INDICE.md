# 📚 Índice de Documentación

Bienvenido a la documentación del **Visualizador EMTP - Dash Python**.

---

## 🚀 Para Empezar

1. **[README.md](../README.md)** - Visión general del proyecto
2. **[INICIO_RAPIDO.md](../INICIO_RAPIDO.md)** - Guía de instalación y ejecución
3. **[RESUMEN_PROYECTO.md](../RESUMEN_PROYECTO.md)** - Resumen ejecutivo completo

---

## 📖 Guías de Uso

### Migración y Datos
- **[MIGRACION_DATOS.md](MIGRACION_DATOS.md)** - Cómo migrar datos desde R Shiny
  - Conversión de archivos .rds
  - Configuración de SQL Server
  - Integración con SharePoint
  - Archivos locales

### Desarrollo
- **[ROADMAP.md](ROADMAP.md)** - Plan de desarrollo y fases
  - Estado actual del proyecto
  - Funcionalidades pendientes
  - Timeline estimado

---

## 🔧 Referencias Técnicas

### Configuración
- **[.env.example](../.env.example)** - Todas las variables de configuración disponibles
- **[config/settings.py](../config/settings.py)** - Configuración del sistema
- **[config/database.py](../config/database.py)** - Gestión de bases de datos

### Módulos Principales
- **src/data/loaders.py** - Carga de datos desde múltiples fuentes
- **src/data/processors.py** - Procesamiento y transformación de datos
- **src/data/validators.py** - Validación de calidad de datos

### Componentes UI
- **src/layouts/** - Layouts de cada módulo
- **src/components/** - Componentes reutilizables
- **src/callbacks/** - Lógica interactiva

---

## 🛠️ Scripts de Utilidad

| Script | Descripción | Uso |
|--------|-------------|-----|
| **setup.sh** / **setup.bat** | Setup inicial automatizado | `./setup.sh` |
| **convert_rds_to_parquet.py** | Convierte archivos R a Parquet | `python scripts/convert_rds_to_parquet.py --all` |
| **test_connections.py** | Verifica conexiones a BD | `python scripts/test_connections.py` |

---

## 📊 Estructura del Proyecto

```
VisualizadorEMTP-Dash/
├── 📱 app.py                    # Aplicación principal
├── ⚙️  config/                  # Configuración
├── 🎨 src/                      # Código fuente
│   ├── data/                   # Manejo de datos
│   ├── layouts/                # Interfaces
│   ├── callbacks/              # Lógica interactiva
│   ├── components/             # Componentes reutilizables
│   └── utils/                  # Utilidades
├── 💾 data/                     # Datos
├── 📄 reports/                  # Reportes
├── 🎨 assets/                   # CSS, JS, imágenes
├── 🧪 tests/                    # Tests
├── 📜 scripts/                  # Scripts de utilidad
└── 📚 docs/                     # Esta documentación
```

---

## 🎯 Casos de Uso Comunes

### 1. Primera vez usando el proyecto
1. Lee [INICIO_RAPIDO.md](../INICIO_RAPIDO.md)
2. Ejecuta `./setup.sh` (o `setup.bat` en Windows)
3. Configura `.env`
4. Ejecuta `python app.py`

### 2. Migrar datos desde R
1. Lee [MIGRACION_DATOS.md](MIGRACION_DATOS.md)
2. Usa `scripts/convert_rds_to_parquet.py`
3. Valida con `src/data/validators.py`

### 3. Conectar a SQL Server
1. Configura variables en `.env`:
   - `SQL_SERVER_ENABLED=True`
   - `SQL_SERVER_HOST=...`
   - etc.
2. Prueba con `python scripts/test_connections.py`
3. Usa `data_loader.load_from_sql_server()`

### 4. Agregar nuevo módulo
1. Crea layout en `src/layouts/`
2. Crea callbacks en `src/callbacks/`
3. Registra en `src/callbacks/__init__.py`
4. Agrega tab en `src/layouts/main_layout.py`

### 5. Deployment a producción
1. Configura `.env` para producción
2. Usa Docker: `docker-compose up -d`
3. O despliega a Azure/AWS/Heroku
4. Configura variables de entorno en el servidor

---

## 🔐 Seguridad

### Variables Sensibles
- **NUNCA** commitear `.env` con credenciales reales
- Usar variables de entorno en producción
- Rotar passwords regularmente

### Autenticación
- Passwords hasheados con bcrypt
- JWT tokens con expiración
- Logging de accesos

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src

# Test específico
pytest tests/test_data.py
```

---

## 📞 Soporte

### Antes de pedir ayuda
1. ✅ Revisa esta documentación
2. ✅ Chequea los logs en `logs/app.log`
3. ✅ Ejecuta scripts de diagnóstico
4. ✅ Revisa ejemplos en el código

### Reportar problemas
- Describe el error claramente
- Incluye el traceback completo
- Menciona tu sistema operativo y versión de Python
- Indica qué has intentado

---

## 📝 Contribuir

Si quieres agregar funcionalidades:
1. Crea una rama nueva
2. Implementa tu feature
3. Escribe tests
4. Actualiza documentación
5. Crea pull request

---

## 🎓 Recursos Adicionales

### Dash
- [Documentación oficial de Dash](https://dash.plotly.com/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Plotly Python](https://plotly.com/python/)

### Python
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [FastAPI](https://fastapi.tiangolo.com/) (si necesitas API REST)

### Deployment
- [Docker Documentation](https://docs.docker.com/)
- [Azure App Service](https://azure.microsoft.com/services/app-service/)
- [Heroku Python](https://devcenter.heroku.com/categories/python)

---

## 📅 Historial de Versiones

- **v0.1.0** (Oct 2025) - Setup inicial y estructura base
- **v0.2.0** (Por definir) - Módulo de matrícula completo
- **v0.3.0** (Por definir) - Módulo de docentes
- **v1.0.0** (Por definir) - MVP completo en producción

---

## ✨ Créditos

Migrado desde la versión R Shiny original del Visualizador EMTP.

---

**Última actualización**: Octubre 2025
