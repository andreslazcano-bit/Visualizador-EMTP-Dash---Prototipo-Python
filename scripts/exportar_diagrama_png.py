#!/usr/bin/env python3
"""
Script para exportar diagrama Mermaid a PNG usando la API de Mermaid.ink
"""

import base64
import urllib.request
import urllib.parse
import json

# Código Mermaid del diagrama (sin emojis que causan problemas)
MERMAID_CODE = """
graph TB
    subgraph USUARIOS["USUARIOS"]
        style USUARIOS fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
        U1["Usuario Basico<br/>Solo visualizacion"]
        U2["Analista SEEMTP<br/>Analisis + Exportacion"]
        U3["Administrador<br/>Gestion completa"]
    end

    subgraph AUTH["AUTENTICACION"]
        style AUTH fill:#FFF3E0,stroke:#F57C00,stroke-width:3px
        LOGIN["Login<br/>Usuario + Password"]
        BCRYPT["bcrypt<br/>Hash seguro"]
        JWT["JWT Token<br/>Expiracion: 24h"]
        VERIFY["Verificacion<br/>Permisos por perfil"]
    end

    subgraph FRONTEND["INTERFAZ DE USUARIO"]
        style FRONTEND fill:#E8F5E9,stroke:#388E3C,stroke-width:3px
        NAV["Sidebar<br/>Navegacion principal"]
        MAPAS["Mapas Geograficos<br/>Regiones y comunas"]
        DASHBOARDS["Dashboards<br/>Datos en tiempo real"]
        REPORTES["Reportes<br/>Excel/PDF futuro"]
    end

    subgraph BACKEND["LOGICA DE NEGOCIO"]
        style BACKEND fill:#FCE4EC,stroke:#C2185B,stroke-width:3px
        CALLBACKS["Callbacks Dash<br/>Reactividad"]
        FILTERS["Filtros<br/>Region Año Indicador"]
        PROCESS["Procesamiento<br/>Agregacion + Calculos"]
        PLOTLY["Plotly Engine<br/>Visualizaciones"]
    end

    subgraph DATA_ACTUAL["DATOS ACTUALES CSV"]
        style DATA_ACTUAL fill:#F3E5F5,stroke:#7B1FA2,stroke-width:3px
        CSV1["establecimientos.csv<br/>1,124 registros"]
        CSV2["matricula_region.csv<br/>144 registros"]
        CSV3["docentes_especialidad.csv<br/>960 registros"]
        CSV4["titulados_2023.csv<br/>1,124 registros"]
        CSV5["establecimientos_full.csv<br/>174,348 registros"]
    end

    subgraph DATA_FUTURO["DATOS FUTUROS Preparado"]
        style DATA_FUTURO fill:#E0F2F1,stroke:#00796B,stroke-width:3px,stroke-dasharray: 5 5
        SQL1["SQL Server - SIGE<br/>Sistema de matricula"]
        SQL2["SQL Server - Titulados<br/>Base titulados"]
        SQL3["SQL Server - Financiero<br/>Presupuestos"]
        SP["SharePoint MINEDUC<br/>Documentos Excel"]
    end

    subgraph GEO["GEODATOS"]
        style GEO fill:#FFF9C4,stroke:#F57F17,stroke-width:3px
        GEOJSON["GeoJSON Chile<br/>16 regiones<br/>345 comunas"]
    end

    U1 & U2 & U3 --> LOGIN
    LOGIN --> BCRYPT
    BCRYPT --> JWT
    JWT --> VERIFY
    VERIFY --> NAV

    NAV --> MAPAS
    NAV --> DASHBOARDS
    NAV --> REPORTES

    MAPAS & DASHBOARDS --> CALLBACKS
    CALLBACKS --> FILTERS
    FILTERS --> PROCESS

    CSV1 & CSV2 & CSV3 & CSV4 & CSV5 --> PROCESS
    GEOJSON --> PROCESS

    SQL1 & SQL2 & SQL3 & SP -.->|No conectado| PROCESS

    PROCESS --> PLOTLY
    PLOTLY --> MAPAS
    PLOTLY --> DASHBOARDS

    MAPAS --> |Interaccion usuario| CALLBACKS
    DASHBOARDS --> |Filtros dinamicos| CALLBACKS

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
"""

def export_mermaid_to_png():
    """
    Exporta el diagrama Mermaid a PNG usando Mermaid.ink API
    """
    
    # Preparar el payload para la API
    payload = {
        "code": MERMAID_CODE,
        "mermaid": {
            "theme": "default"
        }
    }
    
    # Codificar en base64
    graphbytes = MERMAID_CODE.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    
    # URL de la API de Mermaid.ink
    url = f"https://mermaid.ink/img/{base64_string}"
    
    print(f"🔗 URL del diagrama: {url}\n")
    print("📥 Descargando imagen PNG...")
    
    try:
        # Descargar la imagen
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            image_data = response.read()
            
            # Guardar la imagen
            output_file = "docs/Arquitectura_Vision_General.png"
            with open(output_file, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Imagen exportada exitosamente: {output_file}")
            print(f"📊 Tamaño: {len(image_data) / 1024:.2f} KB")
            print(f"\n💡 Puedes abrir la imagen con: open {output_file}")
            
            return True
            
    except urllib.error.HTTPError as e:
        print(f"❌ Error HTTP {e.code}: {e.reason}")
        print(f"\n📋 Intenta copiar esta URL en tu navegador:")
        print(f"{url}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n📋 URL del diagrama para abrir en navegador:")
        print(f"{url}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("  EXPORTAR DIAGRAMA DE ARQUITECTURA A PNG")
    print("  Visualizador EMTP - Dash")
    print("=" * 70)
    print()
    
    export_mermaid_to_png()
    
    print()
    print("=" * 70)
    print("  Alternativas si no funciona:")
    print("  1. Abre https://mermaid.live")
    print("  2. Copia el código del diagrama desde ARQUITECTURA_VISION_GENERAL.md")
    print("  3. Click en 'Actions' → 'PNG' para descargar")
    print("=" * 70)
