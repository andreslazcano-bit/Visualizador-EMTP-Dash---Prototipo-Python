# Diagrama de Flujos - Arquitectura Visualizador EMTP

Este documento contiene diagramas visuales de alta calidad para presentaciones y documentación técnica.

---

## 🎯 Diagrama Principal - Arquitectura de Flujos Completa

```mermaid
graph TB
    %% Definición de nodos principales
    subgraph USUARIOS["👥 USUARIOS"]
        style USUARIOS fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
        U1["👤 Usuario Básico<br/><small>Solo visualización</small>"]
        U2["👔 Analista SEEMTP<br/><small>Análisis + Exportación</small>"]
        U3["⚙️ Administrador<br/><small>Gestión completa</small>"]
    end

    subgraph AUTH["🔐 AUTENTICACIÓN"]
        style AUTH fill:#FFF3E0,stroke:#F57C00,stroke-width:3px
        LOGIN["📝 Login<br/><small>Usuario + Contraseña</small>"]
        BCRYPT["🔒 bcrypt<br/><small>Hash seguro</small>"]
        JWT["🎫 JWT Token<br/><small>Expiración: 24h</small>"]
        VERIFY["✅ Verificación<br/><small>Permisos por perfil</small>"]
    end

    subgraph FRONTEND["🖥️ INTERFAZ DE USUARIO"]
        style FRONTEND fill:#E8F5E9,stroke:#388E3C,stroke-width:3px
        NAV["🧭 Sidebar<br/><small>Navegación principal</small>"]
        MAPAS["🗺️ Mapas Geográficos<br/><small>Regiones y comunas</small>"]
        DASHBOARDS["📊 Dashboards<br/><small>Datos en tiempo real</small>"]
        REPORTES["📄 Reportes<br/><small>Excel/PDF (futuro)</small>"]
    end

    subgraph BACKEND["⚙️ LÓGICA DE NEGOCIO"]
        style BACKEND fill:#FCE4EC,stroke:#C2185B,stroke-width:3px
        CALLBACKS["🔄 Callbacks Dash<br/><small>Reactividad</small>"]
        FILTERS["🔍 Filtros<br/><small>Región, Año, Indicador</small>"]
        PROCESS["⚡ Procesamiento<br/><small>Agregación + Cálculos</small>"]
        PLOTLY["📈 Plotly Engine<br/><small>Visualizaciones</small>"]
    end

    subgraph DATA_ACTUAL["💾 DATOS ACTUALES (CSV)"]
        style DATA_ACTUAL fill:#F3E5F5,stroke:#7B1FA2,stroke-width:3px
        CSV1["📋 establecimientos.csv<br/><small>1,124 registros</small>"]
        CSV2["📋 matricula_region.csv<br/><small>144 registros</small>"]
        CSV3["📋 docentes_especialidad.csv<br/><small>960 registros</small>"]
        CSV4["📋 titulados_2023.csv<br/><small>1,124 registros</small>"]
        CSV5["📋 establecimientos_full.csv<br/><small>174,348 registros</small>"]
    end

    subgraph DATA_FUTURO["🔮 DATOS FUTUROS (Preparado)"]
        style DATA_FUTURO fill:#E0F2F1,stroke:#00796B,stroke-width:3px,stroke-dasharray: 5 5
        SQL1["💿 SQL Server - SIGE<br/><small>Sistema de matrícula</small>"]
        SQL2["💿 SQL Server - Titulados<br/><small>Base titulados</small>"]
        SQL3["💿 SQL Server - Financiero<br/><small>Presupuestos</small>"]
        SP["☁️ SharePoint MINEDUC<br/><small>Documentos Excel</small>"]
    end

    subgraph GEO["🗺️ GEODATOS"]
        style GEO fill:#FFF9C4,stroke:#F57F17,stroke-width:3px
        GEOJSON["🌎 GeoJSON Chile<br/><small>16 regiones<br/>345 comunas</small>"]
    end

    %% Flujo de autenticación
    U1 & U2 & U3 --> LOGIN
    LOGIN --> BCRYPT
    BCRYPT --> JWT
    JWT --> VERIFY
    VERIFY --> NAV

    %% Flujo de navegación
    NAV --> MAPAS
    NAV --> DASHBOARDS
    NAV --> REPORTES

    %% Flujo de datos a callbacks
    MAPAS & DASHBOARDS --> CALLBACKS
    CALLBACKS --> FILTERS
    FILTERS --> PROCESS

    %% Datos actuales
    CSV1 & CSV2 & CSV3 & CSV4 & CSV5 --> PROCESS
    GEOJSON --> PROCESS

    %% Datos futuros (líneas punteadas)
    SQL1 & SQL2 & SQL3 & SP -.->|"No conectado"| PROCESS

    %% Procesamiento a visualización
    PROCESS --> PLOTLY
    PLOTLY --> MAPAS
    PLOTLY --> DASHBOARDS

    %% Ciclo de retroalimentación
    MAPAS --> |"Interacción usuario"| CALLBACKS
    DASHBOARDS --> |"Filtros dinámicos"| CALLBACKS

    %% Estilos de nodos
    classDef userStyle fill:#4A90E2,stroke:#2E5C8A,color:#fff,stroke-width:2px
    classDef authStyle fill:#FFB84D,stroke:#CC8A3D,color:#000,stroke-width:2px
    classDef frontStyle fill:#50C878,stroke:#2E7D52,color:#fff,stroke-width:2px
    classDef backStyle fill:#E85D75,stroke:#B84A5F,color:#fff,stroke-width:2px
    classDef dataStyle fill:#9B59B6,stroke:#6C3E7E,color:#fff,stroke-width:2px
    classDef futureStyle fill:#34D1BF,stroke:#00796B,color:#000,stroke-width:2px,stroke-dasharray: 5 5
    classDef geoStyle fill:#FFD54F,stroke:#F57F17,color:#000,stroke-width:2px

    class U1,U2,U3 userStyle
    class LOGIN,BCRYPT,JWT,VERIFY authStyle
    class NAV,MAPAS,DASHBOARDS,REPORTES frontStyle
    class CALLBACKS,FILTERS,PROCESS,PLOTLY backStyle
    class CSV1,CSV2,CSV3,CSV4,CSV5 dataStyle
    class SQL1,SQL2,SQL3,SP futureStyle
    class GEOJSON geoStyle
```

---

## 🔄 Flujo 1: Autenticación de Usuario (Secuencia)

```mermaid
sequenceDiagram
    autonumber
    actor 👤 Usuario
    participant 🖥️ Login UI
    participant 🔐 Auth Module
    participant 🔒 bcrypt
    participant 🎫 JWT
    participant 🧭 Dashboard

    👤 Usuario->>🖥️ Login UI: 1. Ingresa credenciales
    🖥️ Login UI->>🔐 Auth Module: 2. Valida usuario/password
    🔐 Auth Module->>🔒 bcrypt: 3. Verifica hash
    
    alt ✅ Credenciales válidas
        🔒 bcrypt-->>🔐 Auth Module: 4. Hash coincide
        🔐 Auth Module->>🎫 JWT: 5. Genera token
        🎫 JWT-->>🔐 Auth Module: 6. JWT token (exp: 24h)
        🔐 Auth Module-->>🖥️ Login UI: 7. Autenticado ✓
        🖥️ Login UI->>🧭 Dashboard: 8. Redirección
        🧭 Dashboard-->>👤 Usuario: 9. Vista según perfil
    else ❌ Credenciales inválidas
        🔒 bcrypt-->>🔐 Auth Module: 4. Hash no coincide
        🔐 Auth Module-->>🖥️ Login UI: 5. Error autenticación
        🖥️ Login UI-->>👤 Usuario: 6. "Credenciales incorrectas"
    end

    Note over 👤 Usuario,🧭 Dashboard: Cada request incluye JWT en headers

    👤 Usuario->>🧭 Dashboard: 10. Navega a sección
    🧭 Dashboard->>🔐 Auth Module: 11. Verifica JWT
    
    alt ✅ Token válido
        🔐 Auth Module-->>🧭 Dashboard: 12. Perfil + Permisos
        🧭 Dashboard-->>👤 Usuario: 13. Contenido autorizado
    else ❌ Token expirado
        🔐 Auth Module-->>🧭 Dashboard: 12. Token inválido
        🧭 Dashboard->>🖥️ Login UI: 13. Redirección
        🖥️ Login UI-->>👤 Usuario: 14. "Sesión expirada"
    end
```

---

## 📊 Flujo 2: Visualización de Mapas Geográficos

```mermaid
flowchart LR
    %% Entrada del usuario
    START([👤 Usuario<br/>selecciona filtros])
    
    subgraph INPUT["📥 ENTRADA"]
        F1[🗺️ Región<br/><small>16 opciones</small>]
        F2[📅 Año<br/><small>2020-2025</small>]
        F3[📊 Indicador<br/><small>Matrícula/Docentes/etc</small>]
    end
    
    subgraph CALLBACK["🔄 CALLBACK"]
        CB[mapas_callbacks.py<br/>@callback<br/>actualizar_mapa()]
    end
    
    subgraph QUERY["🔍 CONSULTA"]
        SQL[Filtrar datos:<br/>WHERE region = X<br/>AND año = Y]
        AGG[Agrupar:<br/>GROUP BY comuna<br/>SUM/AVG/COUNT]
    end
    
    subgraph MERGE["🔗 FUSIÓN"]
        JOIN[Merge:<br/>datos + GeoJSON<br/>por código comuna]
    end
    
    subgraph DATA["💾 FUENTES"]
        CSV[(CSV Files<br/>178K registros)]
        GEO[(GeoJSON<br/>345 comunas)]
    end
    
    subgraph VIZ["📈 VISUALIZACIÓN"]
        PLOT[Plotly<br/>Choropleth Map]
        COLOR[Escala colores<br/>5 tonos institucionales]
        INTER[Interactividad<br/>Hover + Click + Zoom]
    end
    
    subgraph OUTPUT["📤 SALIDA"]
        MAP[🗺️ Mapa Interactivo<br/>en dashboard]
    end
    
    %% Flujo
    START --> F1 & F2 & F3
    F1 & F2 & F3 --> CB
    CB --> SQL
    SQL --> CSV
    SQL --> AGG
    AGG --> JOIN
    JOIN --> GEO
    GEO --> PLOT
    PLOT --> COLOR
    COLOR --> INTER
    INTER --> MAP
    MAP --> |Usuario interactúa| START
    
    %% Estilos
    style START fill:#4A90E2,stroke:#2E5C8A,color:#fff,stroke-width:3px
    style INPUT fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    style CALLBACK fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    style QUERY fill:#FCE4EC,stroke:#C2185B,stroke-width:2px
    style MERGE fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    style DATA fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    style VIZ fill:#FFF9C4,stroke:#F57F17,stroke-width:2px
    style OUTPUT fill:#E0F2F1,stroke:#00796B,stroke-width:2px
    
    classDef nodeStyle fill:#50C878,stroke:#2E7D52,color:#fff,stroke-width:2px
    class F1,F2,F3,CB,SQL,AGG,JOIN,CSV,GEO,PLOT,COLOR,INTER,MAP nodeStyle
```

---

## 🏗️ Flujo 3: Arquitectura por Capas

```mermaid
graph TD
    subgraph CAPA1["🎨 CAPA DE PRESENTACIÓN"]
        style CAPA1 fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
        UI1[Login Layout<br/>login_layout.py]
        UI2[Sidebar Layout<br/>sidebar_layout_clean.py]
        UI3[Mapas Layout<br/>mapas.py]
        UI4[Dashboards<br/>real_data_content.py]
    end
    
    subgraph CAPA2["⚙️ CAPA DE LÓGICA"]
        style CAPA2 fill:#FFF3E0,stroke:#F57C00,stroke-width:3px
        CB1[auth_callbacks.py<br/>Login/Logout]
        CB2[sidebar_callbacks.py<br/>Navegación]
        CB3[mapas_callbacks.py<br/>Visualizaciones]
        CB4[theme_callbacks.py<br/>Temas]
    end
    
    subgraph CAPA3["🛠️ CAPA DE SERVICIOS"]
        style CAPA3 fill:#E8F5E9,stroke:#388E3C,stroke-width:3px
        SRV1[auth.py<br/>bcrypt + JWT]
        SRV2[helpers.py<br/>Utilidades]
        SRV3[rate_limiter.py<br/>Seguridad]
    end
    
    subgraph CAPA4["💾 CAPA DE DATOS"]
        style CAPA4 fill:#F3E5F5,stroke:#7B1FA2,stroke-width:3px
        DATA1[(CSV<br/>Actual)]
        DATA2[(SQL Server<br/>Futuro)]
        DATA3[(SharePoint<br/>Futuro)]
    end
    
    subgraph CONFIG["⚙️ CONFIGURACIÓN"]
        style CONFIG fill:#FCE4EC,stroke:#C2185B,stroke-width:3px
        CFG[settings.py<br/>Variables entorno]
    end
    
    %% Flujos entre capas
    UI1 & UI2 & UI3 & UI4 --> CB1 & CB2 & CB3 & CB4
    CB1 & CB2 & CB3 & CB4 --> SRV1 & SRV2 & SRV3
    SRV1 & SRV2 & SRV3 --> DATA1
    SRV1 & SRV2 & SRV3 -.->|No conectado| DATA2 & DATA3
    
    %% Configuración afecta a todas las capas
    CFG -.-> CAPA1 & CAPA2 & CAPA3 & CAPA4
    
    %% Estilos
    classDef uiStyle fill:#4A90E2,stroke:#2E5C8A,color:#fff
    classDef logicStyle fill:#FFB84D,stroke:#CC8A3D,color:#000
    classDef serviceStyle fill:#50C878,stroke:#2E7D52,color:#fff
    classDef dataStyle fill:#9B59B6,stroke:#6C3E7E,color:#fff
    classDef configStyle fill:#E85D75,stroke:#B84A5F,color:#fff
    
    class UI1,UI2,UI3,UI4 uiStyle
    class CB1,CB2,CB3,CB4 logicStyle
    class SRV1,SRV2,SRV3 serviceStyle
    class DATA1,DATA2,DATA3 dataStyle
    class CFG configStyle
```

---

## 📱 Flujo 4: Estados de Navegación del Usuario

```mermaid
stateDiagram-v2
    [*] --> Login: 🌐 Acceso inicial
    
    Login --> ValidarCredenciales: 🔑 Submit
    
    ValidarCredenciales --> Login: ❌ Error
    ValidarCredenciales --> Dashboard: ✅ JWT válido
    
    state Dashboard {
        [*] --> Inicio
        
        Inicio --> Mapas: 🗺️ Click Mapas
        Inicio --> DatosReales: 📊 Click Datos
        Inicio --> Config: ⚙️ Click Config (Admin)
        
        state Mapas {
            [*] --> SeleccionarRegion
            SeleccionarRegion --> AplicarFiltros
            AplicarFiltros --> VerMapa
            VerMapa --> ExportarMapa: 📥 Exportar (Analista)
            VerMapa --> SeleccionarRegion: 🔄 Cambiar filtros
        }
        
        state DatosReales {
            [*] --> ConfigurarFiltros
            ConfigurarFiltros --> GenerarGraficos
            GenerarGraficos --> ExportarDatos: 📥 Excel (Analista)
            GenerarGraficos --> ConfigurarFiltros: 🔄 Ajustar
        }
        
        state Config {
            [*] --> GestionUsuarios
            GestionUsuarios --> CrearUsuario
            GestionUsuarios --> EditarUsuario
            GestionUsuarios --> EliminarUsuario
        }
        
        Mapas --> Inicio: 🏠 Volver
        DatosReales --> Inicio: 🏠 Volver
        Config --> Inicio: 🏠 Volver
    }
    
    Dashboard --> CerrarSesion: 🚪 Logout
    CerrarSesion --> [*]
    
    note right of ValidarCredenciales
        🔒 bcrypt verifica hash
        🎫 JWT genera token (24h)
        ✅ Store en session
    end note
    
    note right of Mapas
        🗺️ Choropleth maps
        📍 16 regiones, 345 comunas
        🎨 5 tonos institucionales
        🖱️ Hover + Click + Zoom
    end note
    
    note right of Config
        👤 Solo Admin
        ➕ CRUD usuarios
        🔐 Gestión perfiles
    end note
```

---

## 📋 Permisos por Perfil de Usuario

```mermaid
graph LR
    subgraph PERFILES["👥 PERFILES DE USUARIO"]
        style PERFILES fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
        U1[👤 Usuario Básico]
        U2[👔 Analista SEEMTP]
        U3[⚙️ Administrador]
    end
    
    subgraph PERMISOS["✅ PERMISOS"]
        style PERMISOS fill:#E8F5E9,stroke:#388E3C,stroke-width:3px
        
        subgraph READ["📖 LECTURA"]
            R1[Ver dashboards]
            R2[Ver mapas]
            R3[Ver datos]
        end
        
        subgraph FILTER["🔍 FILTROS"]
            F1[Filtros básicos]
            F2[Filtros avanzados]
            F3[Consultas custom]
        end
        
        subgraph EXPORT["📥 EXPORTACIÓN"]
            E1[Exportar Excel]
            E2[Exportar PDF]
            E3[Programar reportes]
        end
        
        subgraph ADMIN["⚙️ ADMINISTRACIÓN"]
            A1[Gestión usuarios]
            A2[Configuración sistema]
            A3[Logs auditoría]
        end
    end
    
    %% Usuario Básico
    U1 --> R1 & R2 & R3
    U1 --> F1
    U1 -.->|❌| F2 & F3 & E1 & E2 & E3 & A1 & A2 & A3
    
    %% Analista
    U2 --> R1 & R2 & R3
    U2 --> F1 & F2 & F3
    U2 --> E1 & E2
    U2 -.->|❌| E3 & A1 & A2 & A3
    
    %% Admin
    U3 --> R1 & R2 & R3
    U3 --> F1 & F2 & F3
    U3 --> E1 & E2 & E3
    U3 --> A1 & A2 & A3
    
    %% Estilos
    classDef allowStyle fill:#50C878,stroke:#2E7D52,color:#fff,stroke-width:2px
    classDef denyStyle fill:#E85D75,stroke:#B84A5F,color:#fff,stroke-width:2px,stroke-dasharray: 5 5
    
    class R1,R2,R3,F1,F2,F3,E1,E2,E3,A1,A2,A3 allowStyle
```

---

## 📊 Volumen de Datos - Distribución

```mermaid
pie title Distribución de Registros por Fuente (178,824 registros)
    "establecimientos_full.csv" : 174348
    "establecimientos.csv" : 1124
    "titulados_2023.csv" : 1124
    "financiero.csv" : 1124
    "docentes_especialidad.csv" : 960
    "matricula_region.csv" : 144
```

---

## 🚀 Roadmap de Implementación

```mermaid
gantt
    title Roadmap Técnico - Visualizador EMTP
    dateFormat YYYY-MM-DD
    section ✅ Completado
    Migración Python/Dash           :done, des1, 2024-10-01, 2024-10-15
    Autenticación JWT               :done, des2, 2024-10-16, 2024-10-20
    Mapas interactivos              :done, des3, 2024-10-21, 2024-10-31
    Datos simulados CSV             :done, des4, 2024-11-01, 2024-11-05
    Dockerización                   :done, des5, 2024-11-06, 2024-11-10
    
    section 🔄 En Desarrollo
    Conexión SQL Server             :active, dev1, 2024-11-17, 2024-11-30
    Cache Redis                     :active, dev2, 2024-11-20, 2024-12-05
    Exportación Excel/PDF           :dev3, 2024-12-01, 2024-12-15
    Dashboard tiempo real           :dev4, 2024-12-10, 2024-12-25
    
    section 🔜 Planificado
    SharePoint MINEDUC              :crit, plan1, 2025-01-05, 2025-01-20
    Reportería automatizada         :plan2, 2025-01-15, 2025-02-05
    API REST terceros               :plan3, 2025-02-01, 2025-02-20
    Machine Learning                :plan4, 2025-03-01, 2025-03-30
```

---

## 💡 Cómo Usar Estos Diagramas

### Para Presentaciones
1. Copia el código Mermaid
2. Usa herramientas como:
   - **Mermaid Live Editor**: https://mermaid.live
   - **VS Code Extension**: Markdown Preview Mermaid Support
   - **GitHub/GitLab**: Renderiza automáticamente en markdown

### Para Exportar como Imagen
1. Ve a https://mermaid.live
2. Pega el código del diagrama
3. Click en "Actions" → "PNG" o "SVG"
4. Descarga la imagen de alta resolución

### Diagramas Recomendados por Audiencia

| Audiencia | Diagrama Recomendado |
|-----------|---------------------|
| **Jefatura/Directivos** | Diagrama Principal (arquitectura completa) |
| **Equipo TI** | Flujo 3 (Arquitectura por capas) + Flujo 2 (Mapas) |
| **Analistas** | Flujo 4 (Estados navegación) + Permisos por perfil |
| **Desarrolladores** | Flujo 1 (Autenticación) + Flujo 2 (Visualizaciones) |

---

**Creado**: 17 de Noviembre 2025  
**Versión**: 1.0  
**Proyecto**: Visualizador EMTP Dash  
**Desarrollador**: Andrés Lazcano
