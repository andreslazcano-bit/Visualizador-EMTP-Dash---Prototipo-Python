# 🏛️ Arquitectura del Sistema - Visualizador EMTP Dash

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO / NAVEGADOR                       │
│                     http://localhost:8050                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                                                                  │
│                     DASH APPLICATION (app.py)                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     LAYOUTS                               │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐           │  │
│  │  │ Matrícula │  │ Docentes  │  │   Mapas   │  ...      │  │
│  │  └───────────┘  └───────────┘  └───────────┘           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │                     CALLBACKS                            │  │
│  │  ┌────────────────┐  ┌────────────────┐                │  │
│  │  │ Interactividad │  │  Validación    │  ...           │  │
│  │  └────────────────┘  └────────────────┘                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │                   COMPONENTS                             │  │
│  │  ┌────────┐  ┌─────────┐  ┌────────┐  ┌───────────┐   │  │
│  │  │Filtros │  │Gráficos │  │ Tablas │  │   KPIs    │   │  │
│  │  └────────┘  └─────────┘  └────────┘  └───────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      DATA LAYER                                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    DATA LOADERS                           │  │
│  │  Carga desde múltiples fuentes de datos                  │  │
│  └─────────┬────────────┬────────────┬────────────┬─────────┘  │
│            │            │            │            │             │
│  ┌─────────▼──┐  ┌─────▼─────┐  ┌──▼──────┐  ┌─▼─────────┐  │
│  │ SQL Server │  │PostgreSQL │  │SharePoint│  │  Local    │  │
│  └────────────┘  └───────────┘  └──────────┘  └───────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  DATA PROCESSORS                          │  │
│  │  Limpieza, Transformación, Agregación                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  DATA VALIDATORS                          │  │
│  │  Validación de calidad y consistencia                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      UTILIDADES                                  │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │   Auth   │  │ Exports  │  │ Helpers  │  │   Cache      │  │
│  │          │  │          │  │          │  │  (Redis)     │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos

### 1. Carga Inicial
```
Usuario → app.py → Config → Data Loaders → Fuentes de Datos
                                         ↓
                                   Processors
                                         ↓
                                   Validators
                                         ↓
                                   Memoria/Cache
```

### 2. Interacción Usuario
```
Usuario → Filtro/Click → Callback → Data Processing → Gráfico/Tabla
                            ↓
                        Validación
                            ↓
                        Update UI
```

### 3. Exportación
```
Usuario → Botón Exportar → Export Manager → Formato (CSV/Excel/JSON)
                                         ↓
                                   Download
```

---

## 🗂️ Organización de Módulos

### Capa de Presentación (UI)
```
src/layouts/
  ├── main_layout.py      → Layout principal + navegación
  ├── matricula.py        → Dashboard de matrícula
  ├── docentes.py         → Dashboard de docentes
  └── mapas.py            → Dashboard geográfico

src/components/
  ├── filters.py          → Componentes de filtrado
  ├── charts.py           → Gráficos reutilizables
  └── tables.py           → Tablas interactivas
```

### Capa de Lógica (Business Logic)
```
src/callbacks/
  ├── matricula_callbacks.py  → Lógica de matrícula
  ├── docentes_callbacks.py   → Lógica de docentes
  └── mapa_callbacks.py       → Lógica de mapas

src/data/processors.py
  └── Transformaciones y agregaciones EMTP
```

### Capa de Datos (Data Access)
```
src/data/
  ├── loaders.py          → Carga desde fuentes
  ├── processors.py       → Transformaciones
  └── validators.py       → Validaciones

config/
  ├── settings.py         → Configuración global
  └── database.py         → Conexiones DB
```

---

## 🔌 Integración con Fuentes de Datos

### SQL Server
```python
# En data/loaders.py
df = data_loader.load_from_sql_server(
    query="SELECT * FROM matricula WHERE año = 2024"
)
```

### PostgreSQL
```python
df = data_loader.load_from_postgres(
    table="docentes"
)
```

### SharePoint
```python
df = data_loader.load_from_sharepoint(
    folder_path="Datos/Matricula",
    file_name="matricula_2024.xlsx"
)
```

### Archivos Locales
```python
# CSV
df = data_loader.load_from_csv("data/processed/matricula.csv")

# Excel
df = data_loader.load_from_excel("data/raw/docentes.xlsx")

# Parquet (Recomendado)
df = data_loader.load_from_parquet("data/processed/matricula.parquet")

# RDS (de R)
df = data_loader.load_from_rds("data/processed/matricula.rds")
```

---

## 🔐 Flujo de Autenticación

```
Usuario → Login Form
            ↓
    Validación (bcrypt)
            ↓
    Generación JWT Token
            ↓
    Almacenar en Session
            ↓
    Acceso a Features Protegidas
```

---

## 📦 Deployment Architecture

### Local Development
```
Python → Dash App → localhost:8050
```

### Docker
```
docker-compose.yml
    ├── app (Dash)
    ├── redis (Cache)
    └── postgres (DB - opcional)
```

### Cloud (Azure/AWS)
```
Load Balancer
    ├── Container 1 (Dash App)
    ├── Container 2 (Dash App)
    └── Container N
         ↓
    Redis Cluster
         ↓
    SQL Server Managed Instance
```

---

## 🚦 Estados de la Aplicación

### Estado Global
```
dcc.Store(id='session-data')      # Datos de sesión
dcc.Store(id='user-data')         # Info del usuario
dcc.Store(id='filtered-data')     # Datos filtrados
```

### Estado por Módulo
```
Matrícula:
  - Filtros activos
  - Datos cargados
  - Gráficos renderizados

Docentes:
  - Filtros activos
  - Especialidades seleccionadas
  - Distribución calculada
```

---

## 💾 Cache Strategy

### Niveles de Cache

1. **Memoria (Python Dict)**
   - Datos cargados en `data_loader.cache`
   - Más rápido, limitado por RAM

2. **Redis (Opcional)**
   - Cache distribuido
   - Compartido entre instancias
   - Persistente

3. **Archivo (Parquet)**
   - Pre-procesado guardado en disco
   - Reutilizable entre sesiones

---

## 🔄 Pipeline de Procesamiento

```
Raw Data → Validation → Cleaning → Transformation → Aggregation → Cache
    ↓          ↓           ↓            ↓              ↓           ↓
  .rds      Check      Remove       Filter         Group       Store
  .csv      Types      Nulls        Columns          By        Memory
  .xlsx     Schema     Dups         EMTP Codes    Region      /Redis
```

---

## 📊 Modelo de Datos

### Matrícula
```
Campos principales:
- rbd: Identificador establecimiento
- cod_ense: Código enseñanza (410-863)
- cod_grado: Grado
- nom_reg_rbd_a: Región
- nom_com_rbd: Comuna
- gen_alu: Género
```

### Docentes
```
Campos principales:
- rbd: Identificador establecimiento
- MRUN: RUN docente
- COD_ENS_1/2: Códigos enseñanza
- SUBSECTOR1/2: Especialidades
- Poblacion: Jóvenes/Adultos/Ambas
```

### Geográfico
```
- cod_comuna: Código comuna
- geometry: Geometría (polígono)
- nom_region: Nombre región
```

---

## 🛡️ Seguridad

### Capas de Seguridad

1. **Autenticación**
   - Bcrypt para passwords
   - JWT para sesiones
   - Expiración tokens

2. **Autorización**
   - Roles (admin, user)
   - Permisos por módulo

3. **Datos Sensibles**
   - Variables de entorno
   - No commit de credenciales
   - Encriptación en tránsito (HTTPS)

4. **Rate Limiting**
   - Límite de requests
   - Protección contra abuso

---

## 📈 Monitoring & Observability

### Logs
```
logs/
  └── app.log
      ├── INFO: Operaciones normales
      ├── WARNING: Situaciones atípicas
      ├── ERROR: Errores capturados
      └── DEBUG: Información detallada
```

### Métricas (Futuro)
- Requests por segundo
- Tiempo de respuesta
- Uso de memoria
- Errores por tipo

### Alertas (Futuro)
- Sentry para errores
- Email/Slack notificaciones
- Dashboard de salud

---

## 🔧 Configuración

### Prioridad de Configuración
```
1. Variables de entorno (.env)
2. Defaults en settings.py
3. Argumentos de línea de comandos
```

### Variables Críticas
- `SECRET_KEY`: Seguridad
- `DATABASE_URL`: Conexión DB
- `REDIS_URL`: Cache
- `DEBUG`: Modo desarrollo

---

## 🚀 Performance Optimization

### Estrategias
1. **Lazy Loading**: Cargar datos solo cuando se necesitan
2. **Caching**: Redis + memoria
3. **Pagination**: Limitar filas mostradas
4. **Async**: Procesamiento asíncrono
5. **CDN**: Assets estáticos
6. **Compression**: Gzip responses

---

## 📝 Notas Adicionales

- **Escalabilidad Horizontal**: Agregar más contenedores
- **Backup**: Implementar respaldos automáticos
- **CI/CD**: Pipeline de deployment
- **Tests**: Cobertura > 80%
- **Docs**: Mantener actualizada

---

**Esta arquitectura está diseñada para escalar y evolucionar con tu proyecto! 🚀**
